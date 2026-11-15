"""Download a language-filtered, project-diverse subset of CATMuS Medieval.

Uses catmus_index.csv (from catmus_index.py) to choose shards: round-robin
over projects, cheapest bytes-per-useful-line first, until the target number
of lines in the chosen languages is reached. Each shard is downloaded,
filtered, cleaned of the black polygon fill (see common.unmask_polygon),
downscaled to height 64 gray, written as one parquet part, and the raw shard
is deleted. A `valid` map (255 = real pixel, 0 = former polygon fill) is
stored per line so measurements can ignore the filled area. Re-running skips parts that already exist.

Usage:
    python -m lwti.data.prepare_catmus --split train --target 25000
    python -m lwti.data.prepare_catmus --split test  --target 2000
Output:
    ~/data/lwti/processed/catmus/<split>/part-<shard>.parquet
"""
import argparse
import collections
import concurrent.futures as cf
import io
import os
import time
import urllib.error
import urllib.request

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from PIL import Image

from lwti.data.catmus_index import BASE, hf_token
from lwti.data.common import (DATA_ROOT, mask_to_line, norm_text, png_bytes, processed_dir, to_line,
                              unmask_polygon)

META = ["language", "century", "script_type", "project", "shelfmark", "line_type", "genre"]


def useful_rows(langs: str, keep: set) -> int:
    n = 0
    for kv in langs.split(";"):
        k, v = kv.rsplit(":", 1)
        if k in keep:
            n += int(v)
    return n


def choose_shards(index: pd.DataFrame, split: str, keep: set, target: int):
    d = index[index.split == split].copy()
    d["useful"] = [useful_rows(L, keep) for L in d.languages]
    d = d[d.useful > 0]
    d["cost"] = d.bytes / d.useful
    d["project"] = [P.split(";")[0].rsplit(":", 1)[0] for P in d.projects]  # dominant project
    queues = {p: list(g.sort_values("cost").itertuples()) for p, g in d.groupby("project")}
    chosen, total = [], 0
    while total < target and any(queues.values()):
        for p in sorted(queues):  # one shard per project per round
            if queues[p] and total < target:
                r = queues[p].pop(0)
                chosen.append(r)
                total += r.useful
    return chosen, total


def download(url: str, dst: str, tries: int = 8):
    tok = hf_token()
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"} if tok else {})
            with urllib.request.urlopen(req, timeout=300) as r, open(dst + ".tmp", "wb") as fh:
                while chunk := r.read(1 << 20):
                    fh.write(chunk)
            os.replace(dst + ".tmp", dst)
            return
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ConnectionError):
            if k == tries - 1:
                raise
            time.sleep(min(60, 2 ** k * 2))


def process_shard(split: str, shard: int, keep: set, out_dir: str, tmp_dir: str) -> int:
    part = os.path.join(out_dir, f"part-{shard:03d}.parquet")
    if os.path.exists(part):
        return pq.read_metadata(part).num_rows
    raw = os.path.join(tmp_dir, f"{split}-{shard}.parquet")
    download(f"{BASE}/{split}/{shard}.parquet", raw)
    pf = pq.ParquetFile(raw)
    rows = []
    for rg in range(pf.num_row_groups):
        t = pf.read_row_group(rg).to_pylist()
        for j, ex in enumerate(t):
            if ex["language"] not in keep:
                continue
            text = norm_text(ex["text"] or "")
            if not text:
                continue
            img = Image.open(io.BytesIO(ex["im"]["bytes"]))
            w0, h0 = img.size
            filled, mask = unmask_polygon(img)  # remove the black polygon fill
            a = to_line(filled)
            valid = mask_to_line(mask, a.shape[1])
            rows.append(dict(id=f"catmus-{split}-{shard:03d}-{rg}-{j:04d}", split=split, text=text,
                             png=png_bytes(a), valid=png_bytes(valid), mask_frac=float(mask.mean()),
                             w=a.shape[1], h0=h0, w0=w0,
                             **{m: ex.get(m) for m in META}))
    if rows:
        pq.write_table(pa.Table.from_pylist(rows), part + ".tmp")
        os.replace(part + ".tmp", part)
    os.remove(raw)
    return len(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", required=True, choices=["train", "validation", "test"])
    ap.add_argument("--target", type=int, required=True, help="lines in the chosen languages")
    ap.add_argument("--languages", default="Latin,French")
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args()
    keep = set(args.languages.split(","))

    index = pd.read_csv(os.path.join(DATA_ROOT, "raw/catmus/catmus_index.csv"))
    chosen, total = choose_shards(index, args.split, keep, args.target)
    gb = sum(r.bytes for r in chosen) / 1e9
    print(f"{args.split}: {len(chosen)} shards, ~{total} useful lines, {gb:.2f} GB to download, "
          f"projects: {dict(collections.Counter(r.project for r in chosen))}")

    out_dir = processed_dir(f"catmus/{args.split}")
    tmp_dir = os.path.join(DATA_ROOT, "raw/catmus/tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    done = 0
    with cf.ThreadPoolExecutor(args.workers) as ex:
        futs = {ex.submit(process_shard, args.split, r.shard, keep, out_dir, tmp_dir): r.shard for r in chosen}
        for k, fu in enumerate(cf.as_completed(futs), 1):
            try:
                done += fu.result()
            except Exception as e:
                print(f"FAILED shard {futs[fu]}: {e}")
            print(f"[{k}/{len(chosen)}] {done} lines so far", flush=True)
    print(f"done: {done} lines in {out_dir}")


if __name__ == "__main__":
    main()
