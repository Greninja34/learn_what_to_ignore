"""Shared line preprocessing and storage format.

Every line image in the project goes through `to_line`: grayscale, height
LINE_H (aspect kept), width capped at MAX_W. Text is NFC-normalised.

Processed data is stored as parquet files under DATA_ROOT/processed/<name>/
with one row per line:
    id, split, text, png (bytes, uint8 gray, height LINE_H), w (width after resize),
    h0, w0 (original size), plus dataset-specific metadata columns.
"""
import io
import os
import unicodedata

import numpy as np
from PIL import Image

LINE_H = 64
MAX_W = 2048
DATA_ROOT = os.path.expanduser(os.environ.get("LWTI_DATA", "~/data/lwti"))


def norm_text(s: str) -> str:
    """NFC, collapse whitespace runs, strip ends."""
    s = unicodedata.normalize("NFC", s)
    return " ".join(s.split())


def to_line(img: Image.Image, h: int = LINE_H, max_w: int = MAX_W) -> np.ndarray:
    """Grayscale uint8 array of height h; width scaled with aspect, capped at max_w."""
    g = img.convert("L")
    w0, h0 = g.size
    w = max(8, round(w0 * h / h0))
    if w > max_w:  # very long line: squeeze rather than crop, so no text is lost
        w = max_w
    g = g.resize((w, h), Image.Resampling.LANCZOS if h < h0 else Image.Resampling.BICUBIC)
    return np.asarray(g, dtype=np.uint8)


def unmask_polygon(img: Image.Image, thr: int = 3, grow: int = 2):
    """Remove the black fill outside a line polygon (CATMuS crops lines along a
    polygon and paints the rest pure black).

    Pixels whose RGB channels are all <= thr AND that are connected to the
    image border form the mask (grown by `grow` px). They are filled with
    the local paper tone: per column, the 80th percentile of the unmasked
    pixels, smoothed across columns. Returns (filled PIL 'L' image,
    mask bool array at full resolution, True = was polygon fill).
    """
    import cv2
    rgb = np.asarray(img.convert("RGB"))
    g = np.asarray(img.convert("L")).copy()
    black = (rgb.max(axis=2) <= thr).astype(np.uint8)
    if black.sum() == 0:
        return Image.fromarray(g), np.zeros(g.shape, bool)
    n, lab = cv2.connectedComponents(black, connectivity=8)
    border = np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])
    border = border[border != 0]
    mask = np.isin(lab, border)
    if grow:
        mask = cv2.dilate(mask.astype(np.uint8), np.ones((2 * grow + 1, 2 * grow + 1), np.uint8)) > 0
    if mask.all():
        return Image.fromarray(g), mask
    gm = np.where(mask, np.nan, g.astype(np.float32))
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)  # fully masked columns give NaN, interpolated below
        col = np.nanpercentile(gm, 80, axis=0)
    idx = np.arange(len(col))
    ok = ~np.isnan(col)
    col = np.interp(idx, idx[ok], col[ok])
    k = max(3, g.shape[0] // 2) | 1  # smooth over ~half a line height
    col = np.convolve(np.pad(col, k // 2, mode="edge"), np.ones(k) / k, mode="valid")
    fill = np.broadcast_to(col[None, :], g.shape)
    g[mask] = np.clip(fill[mask], 0, 255).astype(np.uint8)
    return Image.fromarray(g), mask


def mask_to_line(mask: np.ndarray, w: int, h: int = LINE_H) -> np.ndarray:
    """Full-res polygon mask -> uint8 'valid' map at line size (255 = real pixel)."""
    m = Image.fromarray((~mask).astype(np.uint8) * 255).resize((w, h), Image.Resampling.BOX)
    return (np.asarray(m) > 250).astype(np.uint8) * 255  # valid only if entirely real


def bg_normalise(g: np.ndarray, k: int = 21) -> np.ndarray:
    """Simple background normalisation of a uint8 gray line (dark ink on light paper).

    Background estimate: grayscale morphological closing with a k x k square
    (removes ink strokes thinner than k px; LINE_H = 64, strokes ~3-8 px),
    then a k x k median blur. The line is divided by it (paper -> 1) and the
    result stretched to the full 0-255 range between its 1st percentile
    and 255. Removes slow paper tone / stain / show-through gradients.
    """
    import cv2
    bg = cv2.morphologyEx(g, cv2.MORPH_CLOSE, np.ones((k, k), np.uint8))
    bg = cv2.medianBlur(bg, k)
    n = np.minimum(g.astype(np.float32) / np.maximum(bg.astype(np.float32), 1.0), 1.0)
    lo = np.percentile(n, 1)
    if lo > 0.98:  # (almost) blank line: nothing to stretch
        return np.full_like(g, 255)
    return np.clip((n - lo) / (1.0 - lo) * 255.0 + 0.5, 0, 255).astype(np.uint8)


def png_bytes(a: np.ndarray) -> bytes:
    buf = io.BytesIO()
    Image.fromarray(a).save(buf, format="PNG", optimize=False, compress_level=3)
    return buf.getvalue()


def png_decode(b: bytes) -> np.ndarray:
    return np.asarray(Image.open(io.BytesIO(b)).convert("L"), dtype=np.uint8)


def processed_dir(name: str) -> str:
    d = os.path.join(DATA_ROOT, "processed", name)
    os.makedirs(d, exist_ok=True)
    return d
