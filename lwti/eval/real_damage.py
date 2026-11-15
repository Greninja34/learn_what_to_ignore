"""A1 on real lines: does CER rise with measured damage on the CATMuS test set?

For a CATMuS-trained run, join its test predictions with the measured
per-line statistics (results/stats/catmus_test.csv), split lines into
quartiles of each damage statistic, and report corpus CER per quartile.

Quartiles are computed WITHIN each project, then pooled, so the comparison
is "more vs less damaged lines of the same manuscript collection", not
"one collection vs another" (collections also differ in script and hand).
Pre-binarised lines (contrast and paper level both > 0.98) are excluded:
their statistics measure the binarisation, not the parchment.

Usage: python -m lwti.eval.real_damage runs/catmus_crnn_f1.0_s0 [...]
Output: results/tables/real_damage.csv (+ .md)
"""
import argparse
import os

import pandas as pd

from lwti.eval.cer import levenshtein
from lwti.train.train_ctc import RESULTS

# statistic -> direction in which the line is MORE damaged
DAMAGE = {"paper": -1, "midtone": +1, "bg_uneven": +1, "contrast": -1, "sharpness": -1, "noise": +1}


def per_line(run):
    p = pd.read_csv(os.path.join(run, "test_predictions.tsv"), sep="\t", keep_default_na=False, quoting=3)
    p["edits"] = [levenshtein(r, h) for r, h in zip(p.ref, p.hyp)]
    p["chars"] = p.ref.str.len()
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+")
    args = ap.parse_args()
    st = pd.read_csv(os.path.join(RESULTS, "stats", "catmus_test.csv"))
    st = st[~((st.contrast > 0.98) & (st.paper > 0.98))]
    rows = []
    for run in args.runs:
        name = os.path.basename(run.rstrip("/"))
        d = per_line(run).merge(st, on="id")
        for s, sign in DAMAGE.items():
            # within-project quartile, oriented so Q4 = most damaged
            q = d.groupby("project")[s].transform(
                lambda v: pd.qcut((sign * v).rank(method="first"), 4, labels=False) if len(v) >= 8 else pd.NA)
            d2 = d.assign(q=q).dropna(subset=["q"])
            for k in range(4):
                g = d2[d2.q == k]
                rows.append(dict(run=name, stat=s, quartile=f"Q{k + 1}", n=len(g),
                                 cer=g.edits.sum() / max(g.chars.sum(), 1)))
    t = pd.DataFrame(rows)
    t.to_csv(os.path.join(RESULTS, "tables", "real_damage.csv"), index=False)
    w = t.pivot_table(index=["run", "stat"], columns="quartile", values="cer").reset_index()
    w["Q4/Q1"] = w.Q4 / w.Q1
    lines = ["| Run | Statistic | Q1 (least damaged) | Q2 | Q3 | Q4 (most damaged) | Q4/Q1 |", "|---|---|---|---|---|---|---|"]
    for _, r in w.iterrows():
        lines.append(f"| {r.run} | {r.stat} | {r.Q1 * 100:.1f}% | {r.Q2 * 100:.1f}% | {r.Q3 * 100:.1f}% | "
                     f"{r.Q4 * 100:.1f}% | ×{r['Q4/Q1']:.2f} |")
    open(os.path.join(RESULTS, "tables", "real_damage.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
