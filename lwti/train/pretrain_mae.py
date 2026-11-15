"""MAE pretraining on unlabelled lines, with an optional corruption setting.

    --corrupt none        plain MAE (input = clean line)
    --corrupt handpicked  results/derived/handpicked.json
    --corrupt derived_v0  results/derived/derived_v0.json

Unlabelled pool: CATMuS train (minus the 5% used for validation) + IAM
train. No test or validation lines, labelled or not, are ever used.
Inputs are random 512-px crops (lines shorter than that are padded with
paper on the right).

Usage:
    python -m lwti.train.pretrain_mae --corrupt none --steps 20000
Output: runs/mae_<corrupt>/{encoder.pt, mae.pt, log.csv, recon.png, config.json}
"""
import argparse
import json
import math
import os
import time

import numpy as np
import pandas as pd
import torch
from PIL import Image
from torch.utils.data import DataLoader, Dataset

from lwti.damage.derive import CorruptionSampler, load_setting
from lwti.data.common import png_decode
from lwti.data.dataset import load_frame
from lwti.models.conv_mae import ConvMAE
from lwti.models.mae import LineMAE
from lwti.train.train_ctc import RUNS

CROP_W = 512


class CropPairs(Dataset):
    def __init__(self, pngs, sampler=None, seed=0):
        self.pngs = pngs
        self.sampler = sampler
        self.seed = seed
        self.epoch = 0

    def __len__(self):
        return len(self.pngs)

    def __getitem__(self, i):
        rng = np.random.default_rng((self.seed, self.epoch, i))
        g = png_decode(self.pngs[i])
        h, w = g.shape
        if w > CROP_W:
            x0 = int(rng.integers(0, w - CROP_W + 1))
            g = g[:, x0: x0 + CROP_W]
        elif w < CROP_W:
            g = np.pad(g, ((0, 0), (0, CROP_W - w)), constant_values=int(np.percentile(g, 90)))
        gin = self.sampler(g.copy(), rng) if self.sampler is not None else g
        to_t = lambda a: torch.from_numpy(1.0 - a.astype(np.float32) / 255.0)[None]
        return to_t(gin), to_t(g)


def save_recon(model, batch, path, device, n=6):
    model.eval()
    x_in, x_clean = (t[:n].to(device) for t in batch)
    with torch.no_grad(), torch.autocast("cuda", dtype=torch.bfloat16, enabled=device == "cuda"):
        _, pred, masked = model(x_in, x_clean)
    H, W = x_in.shape[2:]
    rec = model.unpatchify(pred.clamp(0, 1), H, W)
    m = model.unpatchify(masked[..., None].expand(-1, -1, pred.shape[-1]), H, W)
    shown = x_in * (1 - m) + 0.5 * m  # masked patches shown grey
    rows = []
    for k in range(x_in.shape[0]):
        for t in (x_in[k], shown[k], rec[k], x_clean[k]):
            rows.append((255 * (1 - t[0].float().cpu().numpy())).astype(np.uint8))
            rows.append(np.full((4, W), 255, np.uint8))
        rows.append(np.full((12, W), 200, np.uint8))
    Image.fromarray(np.vstack(rows)).save(path)
    model.train()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corrupt", default="none", help="none | handpicked | derived_v0")
    ap.add_argument("--steps", type=int, default=20000)
    ap.add_argument("--bs", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--wd", type=float, default=0.05)
    ap.add_argument("--mask", type=float, default=None, help="mask ratio (default 0.75 vit, 0.6 cnn)")
    ap.add_argument("--arch", default="vit", choices=["vit", "cnn"], help="vit: LineMAE; cnn: ConvMAE on the CRNN encoder")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--name", default=None)
    args = ap.parse_args()
    torch.manual_seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    pool = pd.concat([load_frame("catmus", "train", columns=["id", "png", "w"]),
                      load_frame("iam", "train", columns=["id", "png", "w"])], ignore_index=True)
    sampler = None if args.corrupt == "none" else CorruptionSampler(load_setting(args.corrupt))
    ds = CropPairs(pool.png.tolist(), sampler, args.seed)
    dl = DataLoader(ds, batch_size=args.bs, shuffle=True, num_workers=args.workers, drop_last=True,
                    pin_memory=True, persistent_workers=False)

    name = args.name or (f"mae_{args.corrupt}" if args.arch == "vit" else f"cmae_{args.corrupt}")
    out = os.path.join(RUNS, name)
    os.makedirs(out, exist_ok=True)
    json.dump(vars(args) | {"pool": len(pool), "crop_w": CROP_W}, open(os.path.join(out, "config.json"), "w"), indent=1)
    print(f"[{name}] pool {len(pool)} lines | corrupt={args.corrupt}", flush=True)

    if args.arch == "vit":
        model = LineMAE(mask_ratio=args.mask or 0.75).to(device)
        enc = model.encoder
    else:
        model = ConvMAE(mask_ratio=args.mask or 0.6).to(device)
        enc = model.cnn
    print(f"params: encoder {sum(p.numel() for p in enc.parameters()) / 1e6:.2f}M, "
          f"total {sum(p.numel() for p in model.parameters()) / 1e6:.2f}M", flush=True)
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.wd, betas=(0.9, 0.95))
    warm = max(1, args.steps // 20)
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt, lambda s: min(1.0, (s + 1) / warm) * 0.5 * (1 + math.cos(math.pi * min(1.0, s / args.steps))))

    log = open(os.path.join(out, "log.csv"), "w")
    log.write("step,loss,minutes\n")
    step, t0, losses, first = 0, time.time(), [], None
    while step < args.steps:
        for batch in dl:
            if first is None:
                first = batch
            x_in, x_clean = (t.to(device, non_blocking=True) for t in batch)
            with torch.autocast("cuda", dtype=torch.bfloat16, enabled=device == "cuda"):
                loss, _, _ = model(x_in, x_clean)
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            sched.step()
            losses.append(loss.item())
            step += 1
            if step % 500 == 0 or step == args.steps:
                mins = (time.time() - t0) / 60
                print(f"step {step:6d} | loss {np.mean(losses):.4f} | {mins:.1f} min", flush=True)
                log.write(f"{step},{np.mean(losses):.5f},{mins:.2f}\n")
                log.flush()
                losses = []
            if step >= args.steps:
                break
        ds.epoch += 1

    torch.save(model.state_dict(), os.path.join(out, "mae.pt"))
    if args.arch == "vit":
        torch.save({"encoder." + k: v for k, v in model.encoder.state_dict().items()}, os.path.join(out, "encoder.pt"))
    else:
        torch.save(model.encoder_state(), os.path.join(out, "encoder.pt"))
    save_recon(model, first, os.path.join(out, "recon.png"), device)
    print(f"[{name}] done in {(time.time() - t0) / 60:.1f} min -> {out}", flush=True)


if __name__ == "__main__":
    main()
