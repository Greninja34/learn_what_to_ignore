"""Figure: what the pretraining encoder sees under each corruption setting.

Rows: real CATMuS lines (top), then the same clean IAM line under 4 random
draws of the hand-picked setting and 4 of the derived_v0 setting.

Usage: python -m lwti.eval.fig_corruptions
Output: results/figures/fig_corruptions_handpicked_vs_derived.png
"""
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from lwti.damage.derive import CorruptionSampler, load_setting  # noqa: E402
from lwti.data.common import png_decode  # noqa: E402
from lwti.data.dataset import load_frame  # noqa: E402
from lwti.eval.fig_stats import INK, META, ROOT, setup_fonts  # noqa: E402

W = 640


def crop(g):
    g = g[:, :W]
    return np.pad(g, ((0, 0), (0, W - g.shape[1])), constant_values=255) if g.shape[1] < W else g


def main():
    setup_fonts()
    iam = load_frame("iam", "train").sample(50, random_state=3)
    line = crop(png_decode(iam.png.iloc[0]))
    cat = load_frame("catmus", "train", columns=["png", "project"])
    cat = cat[cat.project.isin(["HTRomance", "Gallicorpora", "Eutyches"])].sample(3, random_state=1)
    real = [crop(png_decode(b)) for b in cat.png]
    hp, dv = CorruptionSampler(load_setting("handpicked")), CorruptionSampler(load_setting("derived_v0"))
    rows = [("Real CATMuS lines", real), ("Hand-picked recipe (same clean IAM line, 4 draws)",
            [hp(line.copy(), np.random.default_rng(k)) for k in range(4)]),
            ("Derived from CATMuS measurements (same line, 4 draws)",
             [dv(line.copy(), np.random.default_rng(k)) for k in range(4)])]
    n = sum(len(r) for _, r in rows)
    fig, axes = plt.subplots(n, 1, figsize=(8, 0.72 * n + 1.1))
    k = 0
    for title, imgs in rows:
        for j, g in enumerate(imgs):
            ax = axes[k]
            ax.imshow(g, cmap="gray", vmin=0, vmax=255, aspect="auto")
            ax.set_axis_off()
            if j == 0:
                ax.set_title(title, loc="left", fontsize=11, color=INK, fontweight="semibold", pad=6)
            k += 1
    fig.text(0.01, 0.005, "Ink loss is held out of both recipes (test-only damage).", fontsize=9, color=META)
    fig.tight_layout(h_pad=0.4)
    out = os.path.join(ROOT, "results/figures/fig_corruptions_handpicked_vs_derived.png")
    fig.savefig(out, dpi=170, facecolor="white")
    print("wrote", out)


if __name__ == "__main__":
    main()
