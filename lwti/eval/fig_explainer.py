"""The explainer's result charts, redrawn in Python from the result files.

What a chart shows (all of them use the same "dot plot"):
    one row per arm (scratch, hand-picked damage, derived damage, background normalisation)
    dot  = mean test CER over the seeds of that arm
    bar  = seed range (lowest seed to highest seed); a short bar means the seeds agree
    the highlighted (blue) row is the derived-damage arm
Two arms differ for real only when their bars are clearly apart. A gap inside the bars can be luck.

Where each number comes from:
    clean CER        results/runs.csv          column test_cer, one row per training run
    hard subsets     results/tables/hard_subset.csv  CER on the most damaged quarter of CATMuS test lines
    synthetic damage results/robustness.csv    CER of each IAM model with each damage type added at 3 strengths

Usage (research2 env, from the research folder):
    python -m lwti.eval.fig_explainer
Output: results/figures/fig_e1_*.png
"""
import os

import matplotlib.pyplot as plt
import pandas as pd

from lwti.eval.fig_stats import setup_fonts  # Segoe UI from research/fonts

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RES = os.path.join(ROOT, "results")
OUT = os.path.join(RES, "figures")

# The four arms of the E1 experiment, in display order. The tag is the name used in runs.csv ("" = no tag = scratch).
ARMS = [("", "No augmentation"), ("aug_handpicked", "Hand-picked damage"),
        ("aug_derived_v0", "Derived damage"), ("bgnorm", "Background norm")]
HIGHLIGHT = "aug_derived_v0"
ACCENT, GREY, GRID = "#1f6fc4", "#8a97a3", "#e8edf2"


def summarise(df, value):
    """Per arm: mean, min and max of `value` over seeds. df needs columns tag and `value`."""
    rows = []
    for tag, label in ARMS:
        v = df.loc[df.tag == tag, value]
        if len(v):
            rows.append(dict(tag=tag, label=label, mean=v.mean(), lo=v.min(), hi=v.max(), n=len(v)))
    return pd.DataFrame(rows)


def dot_plot(ax, s, title, xlabel="Test CER (%)"):
    """Draw one dot plot from summarise() output (values are fractions, shown as %)."""
    for i, r in enumerate(s.itertuples()):
        y = len(s) - 1 - i  # first arm at the top
        c = ACCENT if r.tag == HIGHLIGHT else GREY
        ax.plot([r.lo * 100, r.hi * 100], [y, y], color=c, lw=2, solid_capstyle="round")  # seed range
        ax.scatter([r.mean * 100], [y], s=70, color=c, edgecolor="white", linewidth=1.5, zorder=3)  # mean
        ax.text(r.hi * 100, y, f"  {r.mean * 100:.1f}", va="center", fontsize=9, color=c)
    ax.set_yticks(range(len(s)), list(s.label)[::-1])
    ax.set_title(title, loc="left", fontsize=11)
    ax.set_xlabel(xlabel)
    ax.grid(axis="x", color=GRID)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(axis="y", length=0)


def main():
    setup_fonts()
    os.makedirs(OUT, exist_ok=True)

    # 1. Clean test CER per arm, from runs.csv. Only scratch-initialised CRNN runs (no --init) at the E1 label budgets.
    runs = pd.read_csv(os.path.join(RES, "runs.csv"))
    runs["tag"] = runs.tag.fillna("")
    runs = runs[(runs.model == "crnn") & runs.init.isna()]
    fig, axes = plt.subplots(1, 2, figsize=(10, 2.8))
    for ax, (data, frac, title) in zip(axes, [("catmus", 0.05, "CATMuS, 5% labels"), ("iam", 0.1, "IAM, 10% labels")]):
        d = runs[(runs.data == data) & (runs.frac == frac)]
        dot_plot(ax, summarise(d, "test_cer"), title)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_e1_clean.png"), dpi=200)

    # 2. CATMuS hard subsets: CER on the most damaged quarter of real test lines, per damage measurement.
    hs = pd.read_csv(os.path.join(RES, "tables", "hard_subset.csv"))
    hs["tag"] = hs.tag.fillna("")
    hs = hs[hs.frac == 0.05]
    cols = [("all", "All test lines"), ("paper", "Darkest-paper quarter"),
            ("midtone", "Most show-through quarter"), ("contrast", "Lowest-contrast quarter")]
    fig, axes = plt.subplots(2, 2, figsize=(10, 5.4))
    for ax, (col, title) in zip(axes.flat, cols):
        dot_plot(ax, summarise(hs, col), title)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_e1_hard_subset.png"), dpi=200)

    # 3. IAM under synthetic damage at medium strength (level 1).
    #    Left: mean over the 6 damage types that are in the recipes (partly circular: trained on them).
    #    Right: ink loss, which no recipe contains (the fair test).
    rb = pd.read_csv(os.path.join(RES, "robustness.csv"))
    rb["tag"] = rb.tag.fillna("")
    rb = rb[(rb.data == "iam") & (rb.frac == 0.1) & (rb.level == 1)]
    rb = rb.drop_duplicates(["run", "family", "level"], keep="last")  # robustness.py appends; keep the newest row
    six = rb[rb.family != "inkloss"].groupby(["run", "tag"], as_index=False).cer.mean()
    ink = rb[rb.family == "inkloss"][["run", "tag", "cer"]]
    fig, axes = plt.subplots(1, 2, figsize=(10, 2.8))
    dot_plot(axes[0], summarise(six, "cer"), "Damage types used in training (mean of 6)")
    dot_plot(axes[1], summarise(ink, "cer"), "Ink loss (never trained on)")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_e1_robustness.png"), dpi=200)
    print("wrote", ", ".join(f"fig_e1_{k}.png" for k in ("clean", "hard_subset", "robustness")))


if __name__ == "__main__":
    main()
