"""Derive corruption settings from measured statistics (the "Model + fit" step, v0).

For each damage family f with statistic s_f (see families.py):
  1. Response curve: apply f at a grid of parameter values p to clean source
     lines (IAM train) and record the median of s_f -> monotone curve m_f(p).
  2. Each target line (CATMuS train) with s_f beyond the clean source range
     (outside the source's 5-95% band, in the damage direction) is "damaged by
     f"; its strength is p = m_f^-1(s_f) (interpolated, clipped to the grid).
  3. Derived setting: prob_f = fraction of target lines damaged by f;
     strength_f = empirical distribution (quantiles) of their p.

v0 limitation, stated up front: a statistic difference between two datasets
also reflects script, pen and resolution, not only damage. Phase II replaces
this with per-family physical fits.

HELD_OUT families are never used in pretraining (test-only damage, RQ2).

The "handpicked" setting is the usual practice: every family with prob 0.5
and p ~ Uniform over the hand-chosen severity range.

Usage:
    python -m lwti.damage.derive --target results/stats/catmus_train.csv
Output: results/derived/derived_v0.json, results/derived/response_curves.csv,
        results/derived/handpicked.json
"""
import argparse
import json
import os

import numpy as np
import pandas as pd

from lwti.damage import families as F
from lwti.damage.measure import line_stats
from lwti.data.common import png_decode
from lwti.data.dataset import load_frame

STAT = {"tone": "paper", "fade": "contrast", "blur": "sharpness", "noise": "noise", "showthrough": "midtone", "stain": "bg_uneven",
        "inkloss": "ink_frac"}
DIRECTION = {"paper": -1, "contrast": -1, "sharpness": -1, "noise": +1, "midtone": +1, "bg_uneven": +1, "ink_frac": -1}
GRID = {
    "tone": np.linspace(1.0, 0.5, 11),
    "fade": np.linspace(1.0, 0.1, 13),
    "blur": np.linspace(0.0, 3.5, 15),
    "noise": np.linspace(0.0, 0.25, 13),
    "showthrough": np.linspace(0.0, 0.7, 15),
    "stain": np.linspace(0.0, 0.7, 15),
    "inkloss": np.linspace(0.0, 0.7, 15),
}
HELD_OUT = ["inkloss"]
IDENTITY = {"tone": 1.0, "fade": 1.0}  # parameter value meaning "no damage" (default 0)
ORDER = ["tone", "stain", "showthrough", "fade", "blur", "noise"]  # paper, then ink, then capture


def response_curves(src_imgs, seed=0):
    rows = []
    for fam, grid in GRID.items():
        st = STAT[fam]
        for p in grid:
            rng = np.random.default_rng(seed)
            vals = [line_stats(F.apply(g, fam, p, rng) if p != IDENTITY.get(fam, 0.0) else g)[st]
                    for g in src_imgs]
            rows.append(dict(family=fam, stat=st, p=float(p), median=float(np.nanmedian(vals))))
    return pd.DataFrame(rows)


def invert(curve, s):
    """p for statistic values s on a monotone response curve (clipped to grid)."""
    c = curve.sort_values("median")
    x, y = c["median"].to_numpy(), c["p"].to_numpy()
    return np.interp(s, x, y)


def derive(src_stats, tgt_stats, curves):
    out = {}
    for fam in F.FAMILIES:
        st, d = STAT[fam], DIRECTION[STAT[fam]]
        clean = src_stats[st].dropna()
        edge = clean.quantile(0.95 if d > 0 else 0.05)
        t = tgt_stats[st].dropna()
        hit = t[(t > edge) if d > 0 else (t < edge)]
        p = invert(curves[curves.family == fam], hit.to_numpy()) if len(hit) else np.array([])
        out[fam] = dict(
            stat=st, direction=d, source_edge=float(edge), prob=float(len(hit) / max(len(t), 1)),
            p_quantiles=[float(v) for v in (np.quantile(p, np.linspace(0, 1, 21)) if len(p) else [])],
            p_median=float(np.median(p)) if len(p) else None, n_target=int(len(t)),
            held_out=fam in HELD_OUT,
        )
    return out


def handpicked():
    return {fam: dict(prob=0.5, p_range=[min(F.SEVERITY[fam]), max(F.SEVERITY[fam])], held_out=fam in HELD_OUT)
            for fam in F.FAMILIES}


class CorruptionSampler:
    """Callable fn(g uint8, rng) -> g uint8 applying a derived or hand-picked setting.

    Families are applied in a fixed physical order; each with its own prob.
    Held-out families are skipped.
    """

    def __init__(self, setting):
        self.s = setting

    def strength(self, fam, rng):
        cfg = self.s[fam]
        if "p_quantiles" in cfg:  # derived: inverse-CDF sampling from the stored quantiles
            q = np.asarray(cfg["p_quantiles"])
            return float(np.interp(rng.random(), np.linspace(0, 1, len(q)), q))
        lo, hi = cfg["p_range"]
        return float(rng.uniform(lo, hi))

    def __call__(self, g, rng):
        for fam in ORDER:
            cfg = self.s.get(fam)
            if cfg is None or cfg.get("held_out") or not cfg.get("p_quantiles", True):
                continue
            if rng.random() < cfg["prob"]:
                g = F.apply(g, fam, self.strength(fam, rng), rng)
        return g


def load_setting(name, root=None):
    root = root or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                                "results", "derived")
    return json.load(open(os.path.join(root, f"{name}.json")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="iam")
    ap.add_argument("--source-stats", default="results/stats/iam_train.csv")
    ap.add_argument("--target", default="results/stats/catmus_train.csv")
    ap.add_argument("--n-curve", type=int, default=300, help="source lines used for the response curves")
    args = ap.parse_args()
    out = "results/derived"
    os.makedirs(out, exist_ok=True)
    src_stats, tgt_stats = pd.read_csv(args.source_stats), pd.read_csv(args.target)
    df = load_frame(args.source, "train").sample(args.n_curve, random_state=0)
    imgs = [png_decode(b) for b in df.png]
    curves = response_curves(imgs)
    curves.to_csv(f"{out}/response_curves.csv", index=False)
    d = derive(src_stats, tgt_stats, curves)
    json.dump(d, open(f"{out}/derived_v0.json", "w"), indent=1)
    json.dump(handpicked(), open(f"{out}/handpicked.json", "w"), indent=1)
    for fam, v in d.items():
        print(f"{fam:12s} stat={v['stat']:10s} prob={v['prob']:.2f} median p={v['p_median']}"
              f"{'  (held out)' if v['held_out'] else ''}")


if __name__ == "__main__":
    main()
