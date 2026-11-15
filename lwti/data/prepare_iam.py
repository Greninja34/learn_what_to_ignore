"""Download IAM-line (Teklia, Hugging Face) and store it in the project format.

Official writer-independent split from the dataset card:
train 6,482 / validation 976 / test 2,915 lines.

Usage:
    python -m lwti.data.prepare_iam
Output:
    ~/data/lwti/processed/iam/{train,validation,test}.parquet
"""
import io
import os

import pyarrow as pa
import pyarrow.parquet as pq
from datasets import load_dataset
from PIL import Image
from tqdm import tqdm

from lwti.data.common import norm_text, png_bytes, processed_dir, to_line


def main():
    out = processed_dir("iam")
    ds = load_dataset("Teklia/IAM-line")
    for split in ["train", "validation", "test"]:
        rows = []
        for i, ex in enumerate(tqdm(ds[split], desc=split)):
            img = ex["image"]
            if not isinstance(img, Image.Image):
                img = Image.open(io.BytesIO(img["bytes"]))
            w0, h0 = img.size
            a = to_line(img)
            rows.append(dict(id=f"iam-{split}-{i:05d}", split=split, text=norm_text(ex["text"]),
                             png=png_bytes(a), w=a.shape[1], h0=h0, w0=w0))
        path = os.path.join(out, f"{split}.parquet")
        pq.write_table(pa.Table.from_pylist(rows), path)
        print(f"{split}: {len(rows)} lines -> {path}")


if __name__ == "__main__":
    main()
