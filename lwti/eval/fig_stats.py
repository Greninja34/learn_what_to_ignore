"""Figure 1 + A2 table: per-line statistics, IAM (clean) vs CATMuS (real historical).

A2 criterion (fixed before computing D, after seeing medians):
a statistic is "clearly separated" if the two-sample KS statistic D >= 0.5.
stroke_w and ink_frac are reported but classed as scale / script
differences, not damage (CATMuS line crops are tighter around the text).

Usage: python -m lwti.eval.fig_stats
Output: results/figures/fig1_stats_iam_vs_catmus.png
        results/tables/a2_effect_sizes.csv (+ .md)
"""
import os

import matplotlib
import matplotlib.ticker
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GREY, GREEN = "#8A9099", "#00893E"
INK, META, RULE = "#12151B", "#59606B", "#DFE6EB"

LABEL = {
    "paper": ("Paper level", "lower = darker paper"),
    "midtone": ("Faint grey on paper", "higher = more show-through"),
    "bg_uneven": ("Background unevenness", "higher = stains, uneven light"),
    "contrast": ("Ink–paper contrast", "lower = faded ink"),
    "sharpness": ("Sharpness", "lower = blur"),
    "noise": ("Pixel noise (grey levels)", "higher = noisier; coarse estimate"),
    "stroke_w": ("Stroke width (px)", "scale, not damage"),
    "ink_frac": ("Ink fraction", "scale, not damage"),
}
SCALE = {"stroke_w", "ink_frac"}


MS_FONTS = os.path.join(ROOT, "fonts")  # Microsoft fonts copied into the research folder


def setup_fonts():
    """Segoe UI from research/fonts (DejaVu Sans as fallback for glyphs it lacks, e.g. the Tironian et)."""
    from matplotlib import font_manager
    for f in ("segoeui.ttf", "seguisb.ttf", "segoeuib.ttf", "segoeuii.ttf"):
        p = os.path.join(MS_FONTS, f)
        if os.path.exists(p):
            font_manager.fontManager.addfont(p)
    plt.rcParams.update({"font.family": ["Segoe UI", "DejaVu Sans"], "font.size": 11, "axes.edgecolor": RULE,
                         "axes.labelcolor": META, "xtick.color": META, "ytick.color": META, "axes.titlecolor": INK})


def main():
    setup_fonts()
    a = pd.read_csv(os.path.join(ROOT, "results/stats/iam_train.csv"))
    b = pd.read_csv(os.path.join(ROOT, "results/stats/catmus_train.csv"))
    rows = []
    for s in LABEL:
        x, y = a[s].dropna(), b[s].dropna()
        D = ks_2samp(x, y).statistic
        rows.append(dict(stat=s, label=LABEL[s][0], kind="scale/script" if s in SCALE else "damage",
                         iam_median=x.median(), catmus_median=y.median(), ks_D=D,
                         separated=bool(D >= 0.5), n_iam=len(x), n_catmus=len(y)))
    t = pd.DataFrame(rows)
    os.makedirs(os.path.join(ROOT, "results/tables"), exist_ok=True)
    t.round(4).to_csv(os.path.join(ROOT, "results/tables/a2_effect_sizes.csv"), index=False)
    with open(os.path.join(ROOT, "results/tables/a2_effect_sizes.md"), "w") as fh:
        fh.write("| Statistic | Kind | IAM median | CATMuS median | KS D | Separated (D ≥ 0.5) |\n|---|---|---|---|---|---|\n")
        for r in rows:
            fh.write(f"| {r['label']} | {r['kind']} | {r['iam_median']:.4f} | {r['catmus_median']:.4f} | "
                     f"{r['ks_D']:.2f} | {'yes' if r['separated'] else 'no'} |\n")

    fig, axes = plt.subplots(2, 4, figsize=(14, 6.2))
    for ax, r in zip(axes.flat, rows):
        s = r["stat"]
        x, y = a[s].dropna(), b[s].dropna()
        if s == "noise":  # show in grey levels (0-255) rather than fractions
            x, y = x * 255, y * 255
        lo, hi = np.nanpercentile(np.r_[x, y], [0.5, 99.5])
        bins = np.linspace(lo, hi, 40)
        ax.hist(y.clip(lo, hi), bins=bins, density=True, color=GREEN, alpha=0.55, edgecolor="white", linewidth=0.6)
        ax.hist(x.clip(lo, hi), bins=bins, density=True, histtype="step", color=GREY, linewidth=2)
        ax.set_title(LABEL[s][0], loc="left", fontsize=13, fontweight="semibold", pad=18)
        ax.text(0, 1.03, f"{LABEL[s][1]}   ·   KS D = {r['ks_D']:.2f}", transform=ax.transAxes, fontsize=10,
                color=META)
        ax.set_yticks([])
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
        ax.tick_params(axis="x", labelsize=9)
        ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5))
    # one legend for the whole figure (two series), plus direct identity via outline vs fill
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    fig.legend(handles=[Line2D([], [], color=GREY, lw=2, label="IAM: modern English handwriting (outline)"),
                        Patch(facecolor=GREEN, alpha=0.55, label="CATMuS: medieval Latin + French manuscripts (fill)")],
               loc="upper left", ncol=2, frameon=False, fontsize=11, bbox_to_anchor=(0.01, 1.0))
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    out = os.path.join(ROOT, "results/figures/fig1_stats_iam_vs_catmus.png")
    fig.savefig(out, dpi=180, facecolor="white")
    print(f"wrote {out}")
    print(t[["label", "kind", "iam_median", "catmus_median", "ks_D", "separated"]].round(3).to_string(index=False))


if __name__ == "__main__":
    main()
