"""CER of a trained run on its test split, clean and under each damage family x severity.

The damage is seeded per line (seed, line index), so every model sees the
same damaged images.

Usage:
    python -m lwti.eval.robustness runs/iam_crnn_f1_s0 [runs/... ...]
Output: appends to results/robustness.csv
    run, data, model, tag, frac, seed, family, level, p, overlaps_text, cer, cer_clean, ratio
"""
import argparse
import csv
import json
import os

import torch
from torch.utils.data import DataLoader

from lwti.damage import families as F
from lwti.data.charset import charset_for
from lwti.data.dataset import BucketSampler, LineDataset, collate, load_frame, train_files
from lwti.train.train_ctc import RESULTS, BgnormAfter, build_model, evaluate


def load_run(run_dir, device):
    cfg = json.load(open(os.path.join(run_dir, "config.json")))
    cs = charset_for(cfg["data"], train_files(cfg["data"]))
    kw = {"head": cfg.get("head", "linear")} if cfg["model"] == "vit" else {}
    model = build_model(cfg["model"], len(cs), **kw).to(device)
    model.load_state_dict(torch.load(os.path.join(run_dir, "best.pt"), map_location=device))
    model.eval()
    return cfg, cs, model


def test_loader(df, cs, transform, workers=6, bgnorm=False):
    """bgnorm: the run was trained with --bgnorm, so normalise after the damage, as at training time."""
    if bgnorm:
        transform = BgnormAfter(transform)
    ds = LineDataset(df, cs, transform=transform, seed=1234)
    return DataLoader(ds, batch_sampler=BucketSampler(ds.widths, 32, False, 0), collate_fn=collate,
                      num_workers=workers, pin_memory=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--split", default="test")
    ap.add_argument("--families", default=",".join(F.FAMILIES))
    args = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    path = os.path.join(RESULTS, "robustness.csv")
    new = not os.path.exists(path)
    fh = open(path, "a", newline="")
    w = csv.writer(fh)
    if new:
        w.writerow(["run", "data", "model", "tag", "frac", "seed", "split", "family", "level", "p", "overlaps_text",
                    "cer", "cer_clean", "ratio"])
    for run in args.runs:
        cfg, cs, model = load_run(run, device)
        df = load_frame(cfg["data"], args.split)
        name = os.path.basename(run.rstrip("/"))
        clean, *_ = evaluate(model, test_loader(df, cs, None, bgnorm=cfg.get("bgnorm", False)), cs, device)
        print(f"[{name}] clean CER {clean * 100:.2f}%", flush=True)
        common = [name, cfg["data"], cfg["model"], cfg.get("tag", ""), cfg["frac"], cfg["seed"], args.split]
        w.writerow(common + ["clean", -1, "", "", round(clean, 5), round(clean, 5), 1.0])
        for fam in args.families.split(","):
            for lv in range(3):
                c, *_ = evaluate(model, test_loader(df, cs, F.fixed(fam, lv), bgnorm=cfg.get("bgnorm", False)), cs, device)
                w.writerow(common + [fam, lv, F.SEVERITY[fam][lv], F.OVERLAPS_TEXT[fam], round(c, 5), round(clean, 5),
                                     round(c / max(clean, 1e-6), 3)])
                fh.flush()
                print(f"  {fam:12s} level {lv}  CER {c * 100:6.2f}%  (x{c / max(clean, 1e-6):.2f})", flush=True)
    fh.close()


if __name__ == "__main__":
    main()
