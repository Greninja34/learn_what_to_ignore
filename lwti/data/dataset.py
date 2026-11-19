"""Line datasets, width-bucketed batching and collate.

Images become float tensors in [0, 1] with INK = 1, BACKGROUND = 0
(x = 1 - gray/255), so zero padding on the right is blank paper.

Dataset names:
    iam             -> processed/iam/{train,validation,test}.parquet
    catmus          -> processed/catmus/{train,test}/part-*.parquet
                       (we download no CATMuS validation shards, so a fixed
                        random 5% of the downloaded train lines, seed 0, is
                        used as "validation" for model selection only; the
                        official test split is untouched)
"""
import glob
import os
import random

import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, Sampler

from lwti.data.common import DATA_ROOT, png_decode

CATMUS_VAL_FRAC = 0.05


def _files(name, split):
    root = os.path.join(DATA_ROOT, "processed", name)
    if name == "iam":
        return [os.path.join(root, f"{split}.parquet")]
    if name == "catmus":
        s = "train" if split in ("train", "validation") else split
        return sorted(glob.glob(os.path.join(root, s, "part-*.parquet")))
    raise ValueError(name)


def load_frame(name, split, columns=None):
    files = _files(name, split)
    if not files:
        raise FileNotFoundError(f"no processed data for {name}/{split}")
    df = pd.concat([pd.read_parquet(f, columns=columns) for f in files], ignore_index=True)
    if name == "catmus" and split in ("train", "validation"):
        rng = np.random.default_rng(0)
        is_val = rng.random(len(df)) < CATMUS_VAL_FRAC
        df = df[is_val if split == "validation" else ~is_val].reset_index(drop=True)
    return df


def train_files(name):
    return _files(name, "train")


def subset(df, frac, seed):
    """Random label-budget subset (fraction of lines), reproducible per seed."""
    if frac >= 1.0:
        return df
    n = max(8, round(len(df) * frac))
    return df.sample(n=n, random_state=seed).reset_index(drop=True)


class LineDataset(Dataset):
    """Yields (image float32 [1,H,W], text, target ids, id).

    transform: optional fn(np.uint8 gray HxW, rng) -> np.uint8 gray HxW
               applied before the ink inversion (used for damage families).
               rng is seeded with (seed, i), so a line gets the same transform
               every time; with an index (i, epoch) (BucketSampler(tag_epoch=True))
               it is seeded with (seed, i, epoch) and redrawn every epoch.
    """

    def __init__(self, df, charset=None, transform=None, seed=0):
        self.texts = df.text.tolist()
        self.pngs = df.png.tolist()
        self.ids = df.id.tolist()
        self.widths = df.w.tolist()
        self.cs = charset
        self.transform = transform
        self.seed = seed

    def __len__(self):
        return len(self.pngs)

    def __getitem__(self, i):
        if isinstance(i, tuple):  # (line, epoch)
            key = (self.seed, i[0], i[1])
            i = i[0]
        else:
            key = (self.seed, i)
        g = png_decode(self.pngs[i])
        if self.transform is not None:
            g = self.transform(g, np.random.default_rng(key))
        x = torch.from_numpy(1.0 - g.astype(np.float32) / 255.0)[None]
        y = self.cs.encode(self.texts[i]) if self.cs is not None else []
        return x, self.texts[i], torch.tensor(y, dtype=torch.long), self.ids[i]


def collate(batch):
    xs, texts, ys, ids = zip(*batch)
    H = xs[0].shape[1]
    W = max(x.shape[2] for x in xs)
    W = (W + 31) // 32 * 32  # multiple of 32 for the encoders
    out = torch.zeros(len(xs), 1, H, W)
    for k, x in enumerate(xs):
        out[k, :, :, : x.shape[2]] = x
    widths = torch.tensor([x.shape[2] for x in xs])
    targets = torch.cat(ys) if ys else torch.empty(0, dtype=torch.long)
    tlens = torch.tensor([len(y) for y in ys])
    return dict(x=out, widths=widths, texts=list(texts), targets=targets, tlens=tlens, ids=list(ids))


class BucketSampler(Sampler):
    """Batches of similar width (less padding). Shuffled per epoch if shuffle.

    tag_epoch: yield (index, epoch) pairs instead of indices, so LineDataset
    draws a fresh transform for every line every epoch.
    """

    def __init__(self, widths, batch_size, shuffle=True, seed=0, bucket=50, tag_epoch=False):
        self.widths = np.asarray(widths)
        self.bs = batch_size
        self.shuffle = shuffle
        self.seed = seed
        self.bucket = bucket  # batches per sorted chunk
        self.epoch = 0
        self.tag_epoch = tag_epoch

    def __iter__(self):
        rng = random.Random(self.seed + self.epoch)
        ep = self.epoch
        self.epoch += 1
        idx = list(range(len(self.widths)))
        if self.shuffle:
            rng.shuffle(idx)
        chunk = self.bs * self.bucket
        batches = []
        for s in range(0, len(idx), chunk):
            c = sorted(idx[s: s + chunk], key=lambda i: self.widths[i])
            batches += [c[k: k + self.bs] for k in range(0, len(c), self.bs)]
        if self.shuffle:
            rng.shuffle(batches)
        if self.tag_epoch:
            batches = [[(i, ep) for i in b] for b in batches]
        return iter(batches)

    def __len__(self):
        return (len(self.widths) + self.bs - 1) // self.bs
