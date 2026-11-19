"""Train (or fine-tune) a CTC line recogniser and report CER.

Examples:
    # supervised CRNN on 10% of IAM, seed 1
    python -m lwti.train.train_ctc --data iam --model crnn --frac 0.1 --seed 1
    # overfit sanity check on 64 lines
    python -m lwti.train.train_ctc --data iam --model crnn --overfit 64 --steps 1500
    # fine-tune a pretrained ViT encoder
    python -m lwti.train.train_ctc --data iam --model vit --init runs/mae_plain/encoder.pt --frac 0.1

Model selection: best validation CER (evaluated every --eval-every steps),
early stop after --patience evaluations without improvement. The best
checkpoint is then scored on the test split; one row per run is appended
to results/runs.csv.
"""
import argparse
import csv
import datetime
import json
import math
import os
import time

import numpy as np
import torch
from torch.utils.data import DataLoader

from lwti.data.charset import charset_for
from lwti.data.common import bg_normalise
from lwti.data.dataset import BucketSampler, LineDataset, collate, load_frame, subset, train_files
from lwti.eval.cer import cer

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # research/
RUNS = os.path.join(ROOT, "runs")
RESULTS = os.path.join(ROOT, "results")


def build_model(name, n_classes, **kw):
    if name == "crnn":
        from lwti.models.crnn import CRNN
        return CRNN(n_classes)
    if name == "vit":
        from lwti.models.vit_line import ViTLineCTC
        return ViTLineCTC(n_classes, **kw)
    raise ValueError(name)


@torch.no_grad()
def evaluate(model, loader, cs, device, max_batches=None):
    model.eval()
    refs, hyps, ids = [], [], []
    for k, b in enumerate(loader):
        if max_batches and k >= max_batches:
            break
        with torch.autocast("cuda", dtype=torch.bfloat16, enabled=device == "cuda"):
            lp = model(b["x"].to(device, non_blocking=True), b["widths"])
        lens = model.out_lengths(b["widths"]).tolist()
        best = lp.argmax(-1).T.cpu().numpy()  # B, T
        for r, seq, L in zip(b["texts"], best, lens):
            refs.append(r)
            hyps.append(cs.decode_greedy(seq[:L]))
        ids += b["ids"]
    model.train()
    return cer(refs, hyps), refs, hyps, ids


def loader(ds, bs, shuffle, seed, workers, tag_epoch=False):
    return DataLoader(ds, batch_sampler=BucketSampler(ds.widths, bs, shuffle, seed, tag_epoch=tag_epoch),
                      collate_fn=collate, num_workers=workers, pin_memory=True, persistent_workers=workers > 0)


class BgnormAfter:
    """transform, then background normalisation (picklable for DataLoader workers)."""

    def __init__(self, tf):
        self.tf = tf

    def __call__(self, g, rng):
        return bg_normalise(self.tf(g, rng) if self.tf is not None else g)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="iam", choices=["iam", "catmus"])
    ap.add_argument("--model", default="crnn", choices=["crnn", "vit"])
    ap.add_argument("--frac", type=float, default=1.0, help="label budget: fraction of train lines")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--steps", type=int, default=20000)
    ap.add_argument("--bs", type=int, default=16)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--wd", type=float, default=0.01)
    ap.add_argument("--eval-every", type=int, default=500)
    ap.add_argument("--patience", type=int, default=8)
    ap.add_argument("--init", default=None, help="pretrained encoder checkpoint (vit only)")
    ap.add_argument("--freeze-steps", type=int, default=0, help="keep the pretrained encoder frozen this long")
    ap.add_argument("--overfit", type=int, default=0, help="sanity check: train and eval on N train lines")
    ap.add_argument("--tag", default="", help="free-text label for results/runs.csv (e.g. pretraining name)")
    ap.add_argument("--head", default="linear", choices=["linear", "lstm"], help="vit only: output head")
    ap.add_argument("--aug", default="none", choices=["none", "light", "handpicked", "derived_v0"],
                    help="training-time augmentation; handpicked / derived_v0 = that damage recipe "
                         "(lwti.damage.derive), resampled every epoch, train lines only")
    ap.add_argument("--bgnorm", action="store_true",
                    help="background normalisation (lwti.data.common.bg_normalise) on train, val and test lines")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--name", default=None)
    args = ap.parse_args()

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch.backends.cudnn.benchmark = False  # True re-tunes for every line width: very slow here

    cs = charset_for(args.data, train_files(args.data))
    tr = subset(load_frame(args.data, "train"), args.frac, args.seed)
    va = load_frame(args.data, "validation")
    te = load_frame(args.data, "test")
    if args.overfit:
        tr = tr.iloc[: args.overfit]
        va = te = tr
    name = args.name or f"{args.data}_{args.model}{'_' + args.tag if args.tag else ''}_f{args.frac:g}_s{args.seed}" + (
        f"_overfit{args.overfit}" if args.overfit else "")
    out = os.path.join(RUNS, name)
    os.makedirs(out, exist_ok=True)
    json.dump(vars(args) | {"n_train": len(tr), "n_classes": len(cs)}, open(os.path.join(out, "config.json"), "w"), indent=1)
    print(f"[{name}] train {len(tr)} | val {len(va)} | test {len(te)} | classes {len(cs)}", flush=True)

    train_tf = None
    if args.aug == "light":
        from lwti.data.augment import light_affine
        train_tf = light_affine
    elif args.aug in ("handpicked", "derived_v0"):
        from lwti.damage.derive import CorruptionSampler, load_setting
        train_tf = CorruptionSampler(load_setting(args.aug))
    eval_tf = BgnormAfter(None) if args.bgnorm else None
    if args.bgnorm:
        train_tf = BgnormAfter(train_tf)
    # damage recipes are redrawn every epoch (rng seeded with (seed, line, epoch)); none / light keep (seed, line)
    per_epoch = args.aug in ("handpicked", "derived_v0")
    tl = loader(LineDataset(tr, cs, transform=train_tf, seed=args.seed), args.bs, True, args.seed, args.workers,
                tag_epoch=per_epoch)
    vl = loader(LineDataset(va, cs, transform=eval_tf), 32, False, 0, args.workers)

    kw = {"head": args.head} if args.model == "vit" else {}
    model = build_model(args.model, len(cs), **kw).to(device)
    if args.init:
        missing, unexpected = model.load_encoder(args.init)
        print(f"loaded encoder from {args.init}; missing={len(missing)} unexpected={len(unexpected)}")
    n_params = sum(p.numel() for p in model.parameters())
    print(f"params: {n_params / 1e6:.2f}M", flush=True)

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.wd)
    warm = min(1000, args.steps // 10)
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt, lambda s: min(1.0, (s + 1) / warm) * 0.5 * (1 + math.cos(math.pi * min(1.0, s / args.steps))))
    ctc = torch.nn.CTCLoss(blank=0, zero_infinity=True)

    if args.freeze_steps and hasattr(model, "set_encoder_trainable"):
        model.set_encoder_trainable(False)

    best, bad, step, t0 = 1e9, 0, 0, time.time()
    log = open(os.path.join(out, "log.csv"), "w")
    log.write("step,loss,val_cer,lr,minutes\n")
    run_loss = []
    while step < args.steps and bad < args.patience:
        for b in tl:
            if args.freeze_steps and step == args.freeze_steps and hasattr(model, "set_encoder_trainable"):
                model.set_encoder_trainable(True)
            x = b["x"].to(device, non_blocking=True)
            with torch.autocast("cuda", dtype=torch.bfloat16, enabled=device == "cuda"):
                lp = model(x, b["widths"])
            loss = ctc(lp, b["targets"], model.out_lengths(b["widths"]), b["tlens"])
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            opt.step()
            sched.step()
            run_loss.append(loss.item())
            step += 1
            if step % args.eval_every == 0 or step == args.steps:
                v, *_ = evaluate(model, vl, cs, device)
                mins = (time.time() - t0) / 60
                print(f"step {step:6d} | loss {np.mean(run_loss):.3f} | val CER {v * 100:.2f}% | {mins:.1f} min", flush=True)
                log.write(f"{step},{np.mean(run_loss):.4f},{v:.5f},{sched.get_last_lr()[0]:.2e},{mins:.2f}\n")
                log.flush()
                run_loss = []
                if v < best - 1e-4:
                    best, bad = v, 0
                    torch.save(model.state_dict(), os.path.join(out, "best.pt"))
                elif best < 0.99:  # only count patience once CTC has left the all-blank phase
                    bad += 1
            if step >= args.steps or bad >= args.patience:
                break

    model.load_state_dict(torch.load(os.path.join(out, "best.pt"), map_location=device))
    tel = loader(LineDataset(te, cs, transform=eval_tf), 32, False, 0, args.workers)
    test_cer, refs, hyps, ids = evaluate(model, tel, cs, device)
    minutes = (time.time() - t0) / 60
    print(f"[{name}] best val CER {best * 100:.2f}% | TEST CER {test_cer * 100:.2f}% | {minutes:.1f} min", flush=True)
    with open(os.path.join(out, "test_predictions.tsv"), "w") as fh:
        fh.write("id\tref\thyp\n")
        for i, r, h in zip(ids, refs, hyps):
            fh.write(f"{i}\t{r}\t{h}\n")

    if not args.overfit:
        os.makedirs(RESULTS, exist_ok=True)
        path = os.path.join(RESULTS, "runs.csv")
        new = not os.path.exists(path)
        with open(path, "a", newline="") as fh:
            w = csv.writer(fh)
            if new:
                w.writerow(["date", "run", "data", "model", "tag", "init", "frac", "n_train", "seed", "steps_done",
                            "val_cer", "test_cer", "minutes", "params_M"])
            w.writerow([datetime.datetime.now().isoformat(timespec="minutes"), name, args.data, args.model, args.tag,
                        args.init or "", args.frac, len(tr), args.seed, step, round(best, 5), round(test_cer, 5),
                        round(minutes, 1), round(n_params / 1e6, 2)])


if __name__ == "__main__":
    main()
