"""Build results/pilot_summary.md from the result CSVs, with the go/no-go
verdicts computed mechanically from the criteria fixed in the plan:

A1  damage hurts:      CER at least doubles (ratio >= 2) for >= 2 families at
                       the medium severity, for the full-label IAM CRNN.
A2  data differ:       >= 3 damage statistics with KS D >= 0.5 (IAM vs CATMuS).
A3  SSL helps:         at >= 1 (data, budget), an MAE variant's mean test CER is
                       below the scratch ViT's by more than the seed spread
                       (spread = largest max-min range across seeds of the two).
A4  derived >= hand:   derived_v0 mean CER <= handpicked mean CER (indicative).

E1 / E0b (damage recipe as plain training augmentation of the scratch CRNN, and
background normalisation as a preprocessing baseline). These rules were written on
16 Nov 2026, BEFORE any E1/E0b result existed (lwti/scripts/e1_chain.sh was running;
no aug_* or bgnorm run had finished). Arms: scratch, aug_handpicked, aug_derived_v0,
bgnorm; same CRNN, same settings, seeds 0-2. "Damage measure" = mean test CER over
the 6 non-held-out damage families (ink loss is held out of both recipes and is
reported separately), medium strength, IAM 10% labels. Seed spread = half the
max-min range over seeds. A verdict is computed once every arm it needs has >= 2
seeds; otherwise it reads "pending".

B1  recipe helps:      aug_derived_v0 lowers the damage measure versus scratch by
                       >= 2 absolute CER points AND the gain exceeds the larger of
                       the two arms' seed spreads.
B2  derived > hand:    aug_derived_v0 has a lower damage measure than aug_handpicked.
B3  not just bgnorm:   aug_derived_v0 has a lower damage measure than bgnorm (the
                       recipe is worth more than a plain preprocessing baseline);
                       otherwise the evidence states that bgnorm explains the gain.
B4  clean cost:        clean test CER of aug_derived_v0 is within 1 absolute point
                       of scratch (mean derived - mean scratch <= 0.01; being better
                       is not a cost) on both IAM 10% and CATMuS 5%.
B5  real hard lines:   on the CATMuS 5% hard subset (lowest paper-level quartile,
                       highest midtone quartile, lowest contrast quartile;
                       results/tables/hard_subset.csv) aug_derived_v0 beats scratch
                       by more than the larger seed spread on >= 2 of the 3.

Usage: python -m lwti.eval.summary [--out PATH]
"""
import argparse
import os

import numpy as np
import pandas as pd

from lwti.eval.controls import recipe
from lwti.train.train_ctc import RESULTS

E_ARMS = ["scratch", "aug_handpicked", "aug_derived_v0", "bgnorm"]
E_NAMES = {"scratch": "no augmentation", "aug_handpicked": "aug: hand-picked damage",
           "aug_derived_v0": "aug: derived damage", "bgnorm": "background normalisation"}
E_SETTINGS = [("iam", 0.1), ("catmus", 0.05)]
HELD_OUT = "inkloss"


def pct(x):
    return "–" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x * 100:.1f}%"


def read(name):
    p = os.path.join(RESULTS, name)
    return pd.read_csv(p) if os.path.exists(p) else None


def hr(sv):
    return (sv.max() - sv.min()) / 2 if len(sv) else np.nan


def pm(sv, ratio=False):
    """mean ± half range (n) of a per-seed series."""
    if not len(sv):
        return "no runs yet"
    if ratio:
        return f"×{sv.mean():.2f} ±{hr(sv):.2f} (n={len(sv)})"
    return f"{pct(sv.mean())} ±{hr(sv) * 100:.1f} (n={len(sv)})"


def need(stats, arms):
    """None if every arm has >= 2 seeds, else the reason the verdict is pending."""
    short = [f"{a} n={len(stats.get(a, []))}" for a in arms if len(stats.get(a, [])) < 2]
    return None if not short else ("no runs yet" if all(len(stats.get(a, [])) == 0 for a in arms[1:])
                                   else "needs ≥ 2 seeds per arm (" + ", ".join(short) + ")")


def e1_section(runs, rob, hs, verdict):
    """E1/E0b: damage recipe as training augmentation; fills verdict B1-B5."""
    out = ["## E1/E0b. Damage recipe as training augmentation (CRNN scratch, same settings)\n"]
    # clean test CER per arm and setting
    clean = {}
    if runs is not None:
        e = runs[runs.model == "crnn"].drop_duplicates("run", keep="last").copy()
        e["arm"] = e.tag.fillna("").astype(str).str.strip().replace("", "scratch")
        for d, f in E_SETTINGS:
            g = e[(e.data == d) & np.isclose(e.frac, f)]
            for a in E_ARMS:
                clean[(d, a)] = g[g.arm == a].sort_values("seed").test_cer
    out.append("Clean test CER, mean of seeds (± half the seed range):\n")
    out.append("| Arm | " + " | ".join(f"{d} {f * 100:g}%" for d, f in E_SETTINGS) + " |\n|---|" + "---|" * len(E_SETTINGS))
    for a in E_ARMS:
        out.append(f"| {E_NAMES[a]} | " + " | ".join(pm(clean.get((d, a), pd.Series(dtype=float))) for d, _ in E_SETTINGS) + " |")
    out.append("")

    # synthetic damage on IAM 10%: per run, mean over the 6 non-held-out families, and ink loss alone
    per = pd.DataFrame()
    if rob is not None:
        r = rob[(rob.data == "iam") & (rob.model == "crnn") & np.isclose(rob.frac, 0.1) & (rob.family != "clean")].copy()
        r = r.drop_duplicates(["run", "family", "level"], keep="last")
        r["arm"] = r.run.map(recipe)
        r = r[r.arm.isin(E_ARMS)]
        if len(r):
            six, ink = r[r.family != HELD_OUT], r[r.family == HELD_OUT]
            per = pd.concat({"cer6": six.groupby(["arm", "seed", "level"]).cer.mean(),
                             "ratio6": six.groupby(["arm", "seed", "level"]).ratio.mean(),
                             "cer_ink": ink.groupby(["arm", "seed", "level"]).cer.mean(),
                             "ratio_ink": ink.groupby(["arm", "seed", "level"]).ratio.mean()}, axis=1).reset_index()

    def col(arm, level, c):
        if per.empty:
            return pd.Series(dtype=float)
        return per[(per.arm == arm) & (per.level == level)].sort_values("seed")[c].dropna()

    out.append("IAM 10%, IAM test with synthetic damage. Mean over the 6 damage families in the recipes "
               f"(ink loss is held out of both recipes, so it is shown on its own). CER / clean is the CER ratio.\n")
    for lvl, name in [(1, "Medium"), (2, "High")]:
        out.append(f"{name} strength:\n")
        out.append("| Arm | CER, 6 families | CER / clean, 6 families | CER, ink loss | CER / clean, ink loss |\n"
                   "|---|---|---|---|---|")
        for a in E_ARMS:
            if col(a, lvl, "cer6").empty:
                out.append(f"| {E_NAMES[a]} | no runs yet | – | – | – |")
                continue
            out.append(f"| {E_NAMES[a]} | {pm(col(a, lvl, 'cer6'))} | {pm(col(a, lvl, 'ratio6'), True)} | "
                       f"{pm(col(a, lvl, 'cer_ink'))} | {pm(col(a, lvl, 'ratio_ink'), True)} |")
        out.append("")

    # CATMuS 5% hard subset
    hard, hcols = {}, [("paper", "Q4 paper level (low)"), ("midtone", "Q4 midtone / show-through (high)"),
                       ("contrast", "Q4 contrast (low)")]
    if hs is not None:
        h = hs[hs.run.str.startswith("catmus_crnn") & np.isclose(hs.frac, 0.05)].drop_duplicates("run", keep="last").copy()
        h["arm"] = h.tag.fillna("").astype(str).str.strip().replace("", "scratch")
        for a in E_ARMS:
            hard[a] = h[h.arm == a].sort_values("seed")
    out.append("CATMuS 5%, most-damaged quartile of real test lines (results/tables/hard_subset.csv):\n")
    if hs is None:
        out.append("hard_subset.csv not present yet.\n")
    else:
        out.append("| Arm | All lines | " + " | ".join(n for _, n in hcols) + " |\n|---|---|" + "---|" * len(hcols))
        for a in E_ARMS:
            g = hard[a]
            if g.empty:
                out.append(f"| {E_NAMES[a]} | no runs yet |" + " – |" * len(hcols))
            else:
                out.append(f"| {E_NAMES[a]} | {pm(g['all'])} | " + " | ".join(pm(g[c]) for c, _ in hcols) + " |")
        out.append("")

    # ---- verdicts B1-B5
    med = {a: col(a, 1, "cer6") for a in E_ARMS}
    sc, dv = med["scratch"], med["aug_derived_v0"]
    why = need(med, ["scratch", "aug_derived_v0"])
    if why:
        verdict["B1"] = (None, why)
    else:
        gain, spread = sc.mean() - dv.mean(), max(hr(sc), hr(dv))
        verdict["B1"] = (gain >= 0.02 and gain > spread,
                         f"6-family medium-damage CER {pct(sc.mean())} → {pct(dv.mean())} (gain {gain * 100:.1f} pts; "
                         f"need ≥ 2.0 and > seed spread {spread * 100:.1f})")
    why = need(med, ["aug_handpicked", "aug_derived_v0"])
    verdict["B2"] = (None, why) if why else (
        dv.mean() < med["aug_handpicked"].mean(),
        f"derived {pct(dv.mean())} vs hand-picked {pct(med['aug_handpicked'].mean())} (6-family medium-damage CER)")
    why = need(med, ["bgnorm", "aug_derived_v0"])
    if why:
        verdict["B3"] = (None, why)
    else:
        bg = med["bgnorm"].mean()
        verdict["B3"] = (dv.mean() < bg, (f"derived {pct(dv.mean())} vs bgnorm {pct(bg)} (6-family medium-damage CER)"
                                          if dv.mean() < bg else
                                          f"bgnorm explains the gain: bgnorm {pct(bg)} ≤ derived {pct(dv.mean())}"))
    whys = [need({a: clean.get((d, a), []) for a in ["scratch", "aug_derived_v0"]}, ["scratch", "aug_derived_v0"])
            for d, _ in E_SETTINGS]
    if any(whys):
        verdict["B4"] = (None, "; ".join(f"{d}: {w}" for (d, _), w in zip(E_SETTINGS, whys) if w))
    else:
        diffs = [(d, f, clean[(d, "aug_derived_v0")].mean() - clean[(d, "scratch")].mean()) for d, f in E_SETTINGS]
        verdict["B4"] = (all(x <= 0.01 for _, _, x in diffs),
                         "clean CER derived − scratch: " + "; ".join(f"{d} {f * 100:g}% {x * 100:+.1f} pts" for d, f, x in diffs)
                         + " (need ≤ +1.0 on both)")
    if hs is None:
        verdict["B5"] = (None, "hard_subset.csv not present yet")
    else:
        why = need(hard, ["scratch", "aug_derived_v0"])
        if why:
            verdict["B5"] = (None, why)
        else:
            hits = []
            for c, _ in hcols:
                s_, d_ = hard["scratch"][c], hard["aug_derived_v0"][c]
                hits.append((c, s_.mean() - d_.mean() > max(hr(s_), hr(d_)), s_.mean(), d_.mean()))
            n = sum(h for _, h, _, _ in hits)
            verdict["B5"] = (n >= 2, f"derived beats scratch beyond the seed spread on {n} of 3 (need ≥ 2): " +
                             "; ".join(f"{c} {pct(s_)} → {pct(d_)}{' ✓' if h else ''}" for c, h, s_, d_ in hits))
    return out


def main(out_path=None):
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

    out += e1_section(runs, rob, read("tables/hard_subset.csv"), verdict)

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
            "Criteria were fixed in the plan before results; see the module docstring.",
            "B1–B5 (E1/E0b) were added on 16 Nov 2026, before any E1/E0b run had finished.\n",
            "| Assumption | Verdict | Evidence |", "|---|---|---|"]
    for k in ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "B5"]:
        ok, why = verdict.get(k, (None, "not run yet"))
        head.append(f"| {k} | {'PASS' if ok else ('FAIL' if ok is False else 'pending')} | {why} |")
    text = "\n".join(head) + "\n\n" + "\n".join(out)
    open(out_path or os.path.join(RESULTS, "pilot_summary.md"), "w").write(text)
    print(text)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None, help="write here instead of results/pilot_summary.md")
    main(ap.parse_args().out)
