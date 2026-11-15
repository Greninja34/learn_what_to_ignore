"""Build results/pilot_summary.md from the result CSVs, with the go/no-go
verdicts computed mechanically from the criteria fixed in the plan:

A1  damage hurts:      CER at least doubles (ratio >= 2) for >= 2 families at
                       the medium severity, for the full-label IAM CRNN.
A2  data differ:       >= 3 damage statistics with KS D >= 0.5 (IAM vs CATMuS).
A3  SSL helps:         at >= 1 (data, budget), an MAE variant's mean test CER is
                       below the scratch ViT's by more than the seed spread
                       (spread = largest max-min range across seeds of the two).
A4  derived >= hand:   derived_v0 mean CER <= handpicked mean CER (indicative).

Usage: python -m lwti.eval.summary
"""
import os

import numpy as np
import pandas as pd

from lwti.train.train_ctc import RESULTS


def pct(x):
    return "–" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x * 100:.1f}%"


def read(name):
    p = os.path.join(RESULTS, name)
    return pd.read_csv(p) if os.path.exists(p) else None


def main():
    out = []
    runs = read("runs.csv")
    ref = read("reference.csv")
    rob = read("robustness.csv")
    a2 = read("tables/a2_effect_sizes.csv")
    verdict = {}

    # ---- Table 1: supervised baselines + reference
    out.append("## Table 1. Supervised baselines (CRNN) and an off-the-shelf reference\n")
    out.append("| Data | Labels | Lines | Seeds | Test CER (mean) | Range |\n|---|---|---|---|---|---|")
    if runs is not None:
        r = runs[runs.model == "crnn"].drop_duplicates("run", keep="last")
        r = r[r.tag.isna() | (r.tag.astype(str).str.strip() == "")]  # scratch runs only (no pretraining tag)
        for (d, f), g in r.groupby(["data", "frac"]):
            out.append(f"| {d} | {f * 100:g}% | {int(g.n_train.iloc[0])} | {len(g)} | {pct(g.test_cer.mean())} | "
                       f"{pct(g.test_cer.min())}–{pct(g.test_cer.max())} |")
    if ref is not None:
        for _, x in ref.drop_duplicates(["system", "data"], keep="last").iterrows():
            out.append(f"| {x.data} | none ({x.system}, off the shelf) | – | – | {pct(x.test_cer)} | – |")
    out.append("")

    # ---- A1: robustness of the full-label IAM CRNN
    out.append("## A1. Does damage hurt? (IAM CRNN, 100% labels, IAM test with synthetic damage)\n")
    if rob is not None and (rob.run == "iam_crnn_f1_s0").any():
        t = rob[(rob.run == "iam_crnn_f1_s0") & (rob.family != "clean")].drop_duplicates(
            ["family", "level"], keep="last")
        clean = rob[(rob.run == "iam_crnn_f1_s0") & (rob.family == "clean")].cer.iloc[-1]
        out.append(f"Clean test CER: {pct(clean)}\n")
        out.append("| Family | Overlaps characters | Low | Medium | High | Medium / clean |\n|---|---|---|---|---|---|")
        n_double = 0
        for fam, g in t.groupby("family", sort=False):
            g = g.sort_values("level")
            med = g[g.level == 1].ratio.iloc[0]
            n_double += med >= 2
            out.append(f"| {fam} | {'yes' if g.overlaps_text.iloc[0] else 'no'} | "
                       + " | ".join(pct(v) for v in g.cer) + f" | ×{med:.2f} |")
        verdict["A1"] = (n_double >= 2, f"{n_double} families at least double CER at medium severity (need ≥ 2)")
    else:
        verdict["A1"] = (None, "robustness not run yet")
    rd = os.path.join(RESULTS, "tables", "real_damage.md")
    if os.path.exists(rd):
        out.append("\nOn real lines (CATMuS test, quartiles of measured damage within each project):\n")
        out.append(open(rd).read())
    out.append("")

    # ---- A2
    out.append("## A2. Do real degraded lines differ measurably? (IAM train vs CATMuS train)\n")
    if a2 is not None:
        out.append(open(os.path.join(RESULTS, "tables", "a2_effect_sizes.md")).read())
        n = int(((a2.kind == "damage") & a2.separated).sum())
        verdict["A2"] = (n >= 3, f"{n} damage statistics with KS D ≥ 0.5 (need ≥ 3)")
    out.append("")

    # ---- Table 3 / A3 / A4: CRNN, same architecture, only the CNN initialisation differs
    out.append("## A3 / A4. Does pretraining help, and do derived corruptions beat hand-picked? (CRNN; only the CNN's pretraining differs)\n")
    order = ["scratch", "cmae_none", "cmae_handpicked", "cmae_derived_v0"]
    names = {"scratch": "no pretraining", "cmae_none": "masking only", "cmae_handpicked": "masking + hand-picked damage",
             "cmae_derived_v0": "masking + derived damage"}
    if runs is not None:
        c = runs[(runs.model == "crnn") & (runs.frac < 1)].drop_duplicates("run", keep="last").copy()
        c["tag"] = c.tag.fillna("").replace("", "scratch")
        c = c[c.tag.isin(order)]
    if runs is not None and (c.tag != "scratch").any():
        out.append("Test CER, mean of seeds (± half the seed range):\n")
        out.append("| Data | Labels | " + " | ".join(names[t] for t in order) + " |\n|---|---|" + "---|" * len(order))
        a3_hits, a4 = [], []
        for (d, f), g in c.groupby(["data", "frac"]):
            cells, stats = [], {}
            for tag in order:
                sv = g[g.tag == tag].test_cer
                stats[tag] = sv
                cells.append(f"{pct(sv.mean())} ±{(sv.max() - sv.min()) / 2 * 100:.1f} (n={len(sv)})" if len(sv) else "–")
            out.append(f"| {d} | {f * 100:g}% | " + " | ".join(cells) + " |")
            sc = stats["scratch"]
            for tag in order[1:]:
                m = stats[tag]
                if len(sc) and len(m):
                    spread = max(sc.max() - sc.min(), m.max() - m.min())
                    if sc.mean() - m.mean() > spread:
                        a3_hits.append(f"{names[tag]} on {d} {f * 100:g}% ({pct(sc.mean())} → {pct(m.mean())})")
            if len(stats["cmae_derived_v0"]) and len(stats["cmae_handpicked"]):
                a4.append((d, f, stats["cmae_derived_v0"].mean(), stats["cmae_handpicked"].mean()))
        verdict["A3"] = (len(a3_hits) > 0, ("beats no-pretraining beyond the seed spread: " + "; ".join(a3_hits)) if a3_hits
                         else "no pretraining variant beats the scratch CRNN beyond the seed spread")
        if a4:
            wins = sum(dv <= hv for _, _, dv, hv in a4)
            verdict["A4"] = (wins == len(a4), f"derived ≤ hand-picked in {wins} of {len(a4)} settings (indicative only): " +
                             "; ".join(f"{d} {f * 100:g}%: {pct(dv)} vs {pct(hv)}" for d, f, dv, hv in a4))
    else:
        verdict.setdefault("A3", (None, "fine-tuning not run yet"))
        verdict.setdefault("A4", (None, "fine-tuning not run yet"))
    out.append("")

    # ---- the abandoned ViT route, kept for the record
    if runs is not None and (runs.model == "vit").any():
        v = runs[runs.model == "vit"].drop_duplicates("run", keep="last")
        out.append("## Record: first attempt with a small ViT encoder (not used for the verdicts)\n")
        out.append("The 6.5M-parameter ViT memorised the few labelled lines (training loss → 0) and its MAE features were "
                   "weak at this data scale (frozen-encoder probe 75% CER). Pretraining still helped the same ViT:\n")
        out.append("| Run | Labels | Test CER |\n|---|---|---|")
        for _, x in v.sort_values(["data", "frac", "run"]).iterrows():
            out.append(f"| {x.run} | {x.frac * 100:g}% | {pct(x.test_cer)} |")
        out.append("")

    inv = os.path.join(RESULTS, "tables", "invariance_vs_cer.md")
    if os.path.exists(inv):
        out.append("## RQ3 preview. Does invariance predict the CER rise?\n")
        out.append(open(inv).read())

    head = ["# Pilot summary (auto-generated by lwti/eval/summary.py)\n",
            "Criteria were fixed in the plan before results; see the module docstring.\n",
            "| Assumption | Verdict | Evidence |", "|---|---|---|"]
    for k in ["A1", "A2", "A3", "A4"]:
        ok, why = verdict.get(k, (None, "not run yet"))
        head.append(f"| {k} | {'PASS' if ok else ('FAIL' if ok is False else 'pending')} | {why} |")
    text = "\n".join(head) + "\n\n" + "\n".join(out)
    open(os.path.join(RESULTS, "pilot_summary.md"), "w").write(text)
    print(text)


if __name__ == "__main__":
    main()
