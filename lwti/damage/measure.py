"""Per-line damage statistics (the "Measure" step).

All statistics are computed on the project's normalised line images
(gray uint8, height 64, paper bright, ink dark), so IAM and CATMuS are
measured at the same scale.

    contrast      (paper level - ink level) / 255, from an Otsu split
    paper         paper (background) level / 255  -> darkened / yellowed paper
    ink_frac      fraction of pixels classified as ink
    sharpness     variance of the Laplacian / (contrast*255)^2  (low = blurred)
    noise         robust sigma of the high-pass residual on paper pixels / 255
    stroke_w      mean stroke width in px  = 2 * ink area / ink perimeter
    bg_uneven     std of the large-scale paper level / 255 (stains, uneven light)
    midtone       fraction of paper pixels away from ink that are faintly grey
                  (smoothed level between ink+0.5c and paper-0.1c):
                  show-through / bleed-through proxy
    Ink vs paper is split by Otsu on a lightly smoothed copy (sigma 1 px),
    so pixel noise is not counted as ink.

Usage:
    python -m lwti.damage.measure --data iam --split train --n 3000
    python -m lwti.damage.measure --data catmus --split train --n 3000
Output: results/stats/<data>_<split>.csv
"""
import argparse
import os

import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm

from lwti.data.common import png_decode
from lwti.data.dataset import load_frame

STATS = ["contrast", "paper", "ink_frac", "sharpness", "noise", "stroke_w", "bg_uneven", "midtone"]


def line_stats(g: np.ndarray, valid: np.ndarray = None) -> dict:
    """Statistics of one line. `valid` (uint8/bool, same shape): real pixels;
    pixels outside it (e.g. CATMuS polygon fill) are ignored, and paper
    statistics also keep a 3-px margin from its edge."""
    g = g.astype(np.uint8)
    V = np.ones(g.shape, bool) if valid is None else valid > 0
    Vin = cv2.erode(V.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0  # 3-px margin
    if V.sum() < 200:
        return {k: np.nan for k in STATS}
    # find ink on a lightly smoothed copy so pixel noise is not mistaken for ink;
    # Otsu threshold from real pixels only
    sm = cv2.GaussianBlur(g, (0, 0), sigmaX=1.0)
    thr, _ = cv2.threshold(sm[V].reshape(-1, 1), 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    ink = (sm <= thr) & V
    n_ink = int(ink.sum())
    if n_ink < 10 or n_ink > 0.9 * V.sum():
        return {k: np.nan for k in STATS}
    paper_px = g[V & ~ink]
    ink_lvl = float(np.median(g[ink]))
    paper_lvl = float(np.median(paper_px))
    c = max(paper_lvl - ink_lvl, 1.0)

    lap = cv2.Laplacian(g.astype(np.float32), cv2.CV_32F, ksize=3)
    sharp = float(lap[Vin].var() / c ** 2) if Vin.sum() > 50 else np.nan

    resid = g.astype(np.float32) - cv2.medianBlur(g, 3).astype(np.float32)
    far = (cv2.dilate(ink.astype(np.uint8), np.ones((5, 5), np.uint8)) == 0) & Vin  # paper away from strokes
    r = resid[far]
    noise = float(1.4826 * np.median(np.abs(r - np.median(r)))) / 255 if r.size > 50 else np.nan

    grad = cv2.morphologyEx(ink.astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) & V
    perim = max(int(grad.sum()) / 2, 1)  # gradient band is ~2 px wide
    stroke_w = float(2 * n_ink / perim)

    paper_only = g.astype(np.float32).copy()
    paper_only[ink | ~V] = paper_lvl  # fill strokes and non-real pixels with paper before smoothing
    big = cv2.GaussianBlur(paper_only, (0, 0), sigmaX=12)
    bg_uneven = float(big[far].std()) / 255 if far.sum() > 50 else np.nan

    # mid-grey on the smoothed image (noise averages out, faint verso text stays)
    sm2 = cv2.GaussianBlur(g, (0, 0), sigmaX=1.5)
    lo, hi = ink_lvl + 0.5 * c, paper_lvl - 0.1 * c
    v = sm2[far]
    midtone = float(((v > lo) & (v < hi)).mean()) if v.size > 50 else np.nan

    return dict(contrast=c / 255, paper=paper_lvl / 255, ink_frac=n_ink / V.sum(), sharpness=sharp,
                noise=noise, stroke_w=stroke_w, bg_uneven=bg_uneven, midtone=midtone)


def measure_frame(df, n=None, seed=0):
    if n and len(df) > n:
        df = df.sample(n=n, random_state=seed)
    rows = []
    valids = df.valid if "valid" in df.columns else [None] * len(df)
    for i, b, v in tqdm(zip(df.id, df.png, valids), total=len(df), desc="measure"):
        rows.append(dict(id=i, **line_stats(png_decode(b), png_decode(v) if v is not None else None)))
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--split", default="train")
    ap.add_argument("--n", type=int, default=3000)
    args = ap.parse_args()
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out = os.path.join(root, "results", "stats")
    os.makedirs(out, exist_ok=True)
    df = load_frame(args.data, args.split)
    meta = [c for c in ("language", "project", "century") if c in df.columns]
    st = measure_frame(df, args.n)
    st = st.merge(df[["id"] + meta], on="id")
    path = os.path.join(out, f"{args.data}_{args.split}.csv")
    st.to_csv(path, index=False)
    print(f"wrote {path} ({len(st)} lines)")
    print(st[STATS].describe().T[["mean", "25%", "50%", "75%"]].round(4))


if __name__ == "__main__":
    main()
