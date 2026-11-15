"""Damage families: simple forward models on gray line images.

Every family takes (g: uint8 HxW, paper bright / ink dark, p: float, rng)
and returns a uint8 image. `p` is the family's single physical parameter,
in its own units (documented per family). The statistic each family
mainly moves is listed, so `derive.py` can fit `p` to real lines.

    family        parameter p                         moves stat     overlaps characters?
    tone          paper brightness multiplier (0..1]  paper           no (whole line darkens)
    fade          ink-to-paper contrast kept (0..1]   contrast        yes (ink loss of density)
    blur          Gaussian sigma in px at H=64        sharpness       yes (strokes merge)
    noise         additive Gaussian sigma / 255       noise           no (mostly paper)
    showthrough   opacity of the mirrored verso text  midtone         no (paper only)
    stain         depth of low-frequency darkening    bg_uneven       no (paper only)
    inkloss       fraction of ink removed in blobs    ink_frac        yes (broken strokes)

`overlaps characters` is the H3 grouping: families that damage the
character-carrying pixels vs. families that only change the paper.

`tone` was added after the first measurement (9 Nov 2026): paper level was
the largest IAM-vs-CATMuS difference and no other family moved it.

SEVERITY gives three fixed levels (low / medium / high) per family, used
for the robustness tables. They are chosen by hand to span "barely
visible" to "hard to read", BEFORE looking at any CER result.
"""
import cv2
import numpy as np

OVERLAPS_TEXT = {"tone": False, "fade": True, "blur": True, "noise": False, "showthrough": False, "stain": False, "inkloss": True}

SEVERITY = {
    "tone": [0.9, 0.8, 0.65],         # paper brightness kept
    "fade": [0.6, 0.35, 0.2],         # contrast kept
    "blur": [0.8, 1.5, 2.5],          # sigma px
    "noise": [0.04, 0.10, 0.18],      # sigma / 255
    "showthrough": [0.15, 0.30, 0.50],  # verso opacity
    "stain": [0.15, 0.30, 0.50],      # darkening depth
    "inkloss": [0.15, 0.35, 0.55],    # fraction of ink removed
}
FAMILIES = list(SEVERITY)


def _paper_level(g):
    return float(np.percentile(g, 90))


def tone(g, p, rng):
    """Darker / tinted paper (parchment, aged paper, dim scan): whole line scaled."""
    return np.clip(g.astype(np.float32) * p, 0, 255).astype(np.uint8)


def fade(g, p, rng):
    paper = _paper_level(g)
    f = g.astype(np.float32)
    out = paper - (paper - f) * p
    return np.clip(out, 0, 255).astype(np.uint8)


def blur(g, p, rng):
    if p <= 0:
        return g
    return cv2.GaussianBlur(g, (0, 0), sigmaX=p)


def noise(g, p, rng):
    out = g.astype(np.float32) + rng.normal(0, p * 255, g.shape)
    return np.clip(out, 0, 255).astype(np.uint8)


def _smooth_field(shape, scale, rng):
    """Low-frequency random field in [0, 1]."""
    h, w = shape
    sh, sw = max(2, h // scale + 2), max(2, w // scale + 2)
    small = rng.random((sh, sw)).astype(np.float32)
    f = cv2.resize(small, (w, h), interpolation=cv2.INTER_CUBIC)
    f = cv2.GaussianBlur(f, (0, 0), sigmaX=scale / 4)
    f -= f.min()
    return f / max(f.max(), 1e-6)


def showthrough(g, p, rng):
    """Verso text seen through the paper: mirrored, shifted, blurred, faint."""
    h, w = g.shape
    verso = g[:, ::-1]
    dy = int(rng.integers(-h // 4, h // 4 + 1))
    dx = int(rng.integers(0, w))
    verso = np.roll(np.roll(verso, dy, axis=0), dx, axis=1)
    verso = cv2.GaussianBlur(verso, (0, 0), sigmaX=1.5).astype(np.float32)
    paper = _paper_level(g)
    dark = (paper - verso).clip(0, None) * p  # how much the verso darkens the recto paper
    out = np.minimum(g.astype(np.float32), paper - dark)
    return np.clip(out, 0, 255).astype(np.uint8)


def stain(g, p, rng):
    """Multiplicative low-frequency darkening (water stains, foxing, uneven light)."""
    f = _smooth_field(g.shape, scale=48, rng=rng)
    f = f ** 2  # few dark patches rather than a uniform tint
    out = g.astype(np.float32) * (1 - p * f)
    return np.clip(out, 0, 255).astype(np.uint8)


def inkloss(g, p, rng):
    """Remove ink in blobs (abraded / flaked ink): ink pixels inside a random mask go to paper."""
    paper = _paper_level(g)
    f = _smooth_field(g.shape, scale=6, rng=rng)
    mask = f < np.quantile(f, p)  # p = fraction of the area hit
    out = g.copy()
    out[mask] = np.maximum(g[mask], np.uint8(paper))
    return out


FN = {"tone": tone, "fade": fade, "blur": blur, "noise": noise, "showthrough": showthrough, "stain": stain, "inkloss": inkloss}


def apply(g, family, p, rng):
    return FN[family](g, p, rng)


def fixed(family, level):
    """Transform for LineDataset: one family at one of the three SEVERITY levels."""
    p = SEVERITY[family][level]
    return lambda g, rng: apply(g, family, p, rng)
