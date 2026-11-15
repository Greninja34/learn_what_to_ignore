"""Character set for CTC: index 0 is the blank, 1..N are characters.

Built from the TRAIN split only, saved as JSON next to the data, so every
model on a dataset shares the same output layer. Characters in val/test
that are not in the charset are kept in the reference text (so they count
as errors) but cannot be predicted.
"""
import collections
import json
import os

import pandas as pd


class Charset:
    def __init__(self, chars):
        self.chars = list(chars)
        self.idx = {c: i + 1 for i, c in enumerate(self.chars)}

    def __len__(self):  # number of CTC classes incl. blank
        return len(self.chars) + 1

    def encode(self, text):
        return [self.idx[c] for c in text if c in self.idx]

    def decode_greedy(self, ids):
        """Collapse repeats, drop blanks."""
        out, prev = [], 0
        for i in ids:
            if i != prev and i != 0:
                out.append(self.chars[i - 1])
            prev = i
        return "".join(out)

    def save(self, path):
        with open(path, "w") as fh:
            json.dump(self.chars, fh, ensure_ascii=False, indent=0)

    @classmethod
    def load(cls, path):
        with open(path) as fh:
            return cls(json.load(fh))

    @classmethod
    def build(cls, texts, min_count=1):
        c = collections.Counter(ch for t in texts for ch in t)
        return cls(sorted(ch for ch, n in c.items() if n >= min_count))


def charset_for(name, train_parquets, min_count=1):
    """Load the dataset's charset, building it from the train texts if missing."""
    from lwti.data.common import processed_dir
    path = os.path.join(processed_dir(name), "charset.json")
    if os.path.exists(path):
        return Charset.load(path)
    texts = pd.concat([pd.read_parquet(p, columns=["text"]) for p in train_parquets]).text
    cs = Charset.build(texts, min_count)
    cs.save(path)
    return cs
