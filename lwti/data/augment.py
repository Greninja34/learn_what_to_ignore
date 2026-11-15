"""Light training-time augmentation for line images (fine-tuning only).

Small random affine: rotation within ±1.5°, horizontal shear within ±0.25,
width scale 0.85–1.15, height scale 0.92–1.05, vertical shift within ±3 px.
Empty areas are filled with the line's paper level. Applied identically to
every model that uses --aug light, never to validation or test lines.
"""
import cv2
import numpy as np


def light_affine(g, rng):
    h, w = g.shape
    paper = int(np.percentile(g, 90))
    sx, sy = rng.uniform(0.85, 1.15), rng.uniform(0.92, 1.05)
    shear = rng.uniform(-0.25, 0.25)
    ang = np.deg2rad(rng.uniform(-1.5, 1.5))
    new_w = max(8, int(round(w * sx)))
    c, s = np.cos(ang), np.sin(ang)
    # scale, shear (x depends on y), rotate about the line centre, shift
    A = np.array([[c, -s], [s, c]]) @ np.array([[sx, shear], [0, sy]])
    cx, cy = w / 2, h / 2
    t = np.array([new_w / 2, h / 2 + rng.uniform(-3, 3)]) - A @ np.array([cx, cy])
    M = np.hstack([A, t[:, None]]).astype(np.float32)
    return cv2.warpAffine(g, M, (new_w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=paper)
