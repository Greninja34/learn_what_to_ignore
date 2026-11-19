"""Invariance scores per damage family x severity (Ericsson et al. 2021 style).

For a trained run: take N test lines, compute sequence features
(model.features -> [B, D, T]), mean-pool over the valid (unpadded) time
steps, standardise each feature with the clean set's mean/std, and report
    invariance = mean cosine similarity(f(clean line), f(damaged line))
1.0 = the representation ignores that damage completely.

Then join with results/robustness.csv (CER ratio for the same run, family,
level) and report Spearman correlations, overall and per H3 group
(families that overlap the characters vs paper-only families).

Usage:
    python -m lwti.eval.invariance runs/iam_crnn_f1_s0 runs/... --n 500
Output: results/invariance.csv, results/tables/invariance_vs_cer.md
"""
import argparse
import os

import numpy as np
import pandas as pd
import torch
from scipy.stats import spearmanr

from lwti.damage import families as F
from lwti.data.dataset import load_frame
from lwti.eval.robustness import load_run, test_loader
from lwti.train.train_ctc import RESULTS


@torch.no_grad()
def pooled_features(model, loader, device):
    feats, ids = [], []
    for b in loader:
        x = b["x"].to(device)
        with torch.autocast("cuda", dtype=torch.bfloat16, enabled=device == "cuda"):
            f = model.features(x, b["widths"]).float()  # B, D, T
        T, Wp = f.shape[2], x.shape[3]
        valid = torch.clamp(torch.ceil(b["widths"].to(device) * T / Wp), 1, T).long()
        m = (torch.arange(T, device=device)[None] < valid[:, None]).float()  # B, T
        feats.append(((f * m[:, None]).sum(2) / m.sum(1, keepdim=True)).cpu())
        ids += b["ids"]
    order = np.argsort(ids)  # loaders bucket by width; align by id
    return torch.cat(feats)[order], [ids[i] for i in order]


def invariance(model, df, cs, device, bgnorm=False):
    clean, ids0 = pooled_features(model, test_loader(df, cs, None, bgnorm=bgnorm), device)
    mu, sd = clean.mean(0), clean.std(0) + 1e-6
    z0 = (clean - mu) / sd
    out = {}
    for fam in F.FAMILIES:
        for lv in range(3):
            dmg, ids = pooled_features(model, test_loader(df, cs, F.fixed(fam, lv), bgnorm=bgnorm), device)
            assert ids == ids0
            z = (dmg - mu) / sd
            out[(fam, lv)] = torch.nn.functional.cosine_similarity(z0, z, dim=1).mean().item()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--n", type=int, default=500)
    args = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    rows = []
    for run in args.runs:
        cfg, cs, model = load_run(run, device)
        df = load_frame(cfg["data"], "test").sample(args.n, random_state=0).reset_index(drop=True)
        name = os.path.basename(run.rstrip("/"))
        for (fam, lv), v in invariance(model, df, cs, device, cfg.get("bgnorm", False)).items():
            rows.append(dict(run=name, family=fam, level=lv, overlaps_text=F.OVERLAPS_TEXT[fam], invariance=v))
        print(f"[{name}] done", flush=True)
    inv = pd.DataFrame(rows)
    path = os.path.join(RESULTS, "invariance.csv")
    if os.path.exists(path):
        old = pd.read_csv(path)
        inv = pd.concat([old[~old.run.isin(inv.run.unique())], inv], ignore_index=True)
    inv.to_csv(path, index=False)

    rob = pd.read_csv(os.path.join(RESULTS, "robustness.csv"))
    rob = rob[rob.family != "clean"].drop_duplicates(["run", "family", "level"], keep="last")
    rob["level"] = rob.level.astype(int)
    j = inv.merge(rob[["run", "family", "level", "ratio", "cer"]], on=["run", "family", "level"])
    lines = ["| Run | Group | n | Spearman ρ (invariance vs CER ratio) | p |", "|---|---|---|---|---|"]
    for run, g in j.groupby("run"):
        for grp, sub in [("all families", g), ("overlap characters", g[g.overlaps_text]),
                         ("paper only", g[~g.overlaps_text])]:
            if len(sub) >= 4:
                r = spearmanr(sub.invariance, sub.ratio)
                lines.append(f"| {run} | {grp} | {len(sub)} | {r.statistic:.2f} | {r.pvalue:.3f} |")
    os.makedirs(os.path.join(RESULTS, "tables"), exist_ok=True)
    open(os.path.join(RESULTS, "tables", "invariance_vs_cer.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
