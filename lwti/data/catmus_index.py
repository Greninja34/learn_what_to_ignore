"""Index CATMuS Medieval parquet shards without downloading them.

Reads each shard's parquet footer over HTTP range requests and records
rows, size and the language / project mix (from the first row group's
`language` and `project` columns, which are small).

Output: <out>/catmus_index.csv with columns
    split, shard, bytes, rows, languages, projects

Usage:
    python -m lwti.data.catmus_index --out ~/data/lwti/raw/catmus
"""
import argparse
import collections
import concurrent.futures as cf
import csv
import io
import os
import time
import urllib.error
import urllib.request

import pyarrow.parquet as pq

BASE = "https://huggingface.co/api/datasets/CATMuS/medieval/parquet/default"
N_SHARDS = {"train": 252, "validation": 43, "test": 51}


def hf_token():
    """HF token from $HF_TOKEN or the file `hf auth login` writes (higher rate limits)."""
    tok = os.environ.get("HF_TOKEN")
    path = os.path.expanduser("~/.cache/huggingface/token")
    if not tok and os.path.exists(path):
        tok = open(path).read().strip()
    return tok


class HTTPRangeFile(io.RawIOBase):
    """Minimal seekable read-only file over HTTP range requests."""

    def __init__(self, url):
        # resolve redirects once and learn the size
        # auth only on the hub request; the redirect target is a signed CDN URL
        tok = hf_token()
        req = urllib.request.Request(url, method="HEAD", headers={"Authorization": f"Bearer {tok}"} if tok else {})
        with urllib.request.urlopen(req, timeout=60) as r:
            self.url = r.geturl()
            self.size = int(r.headers["Content-Length"])
        self.pos = 0

    def readable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, offset, whence=0):
        if whence == 0:
            self.pos = offset
        elif whence == 1:
            self.pos += offset
        else:
            self.pos = self.size + offset
        return self.pos

    def read(self, n=-1):
        if n is None or n < 0:
            n = self.size - self.pos
        if n == 0 or self.pos >= self.size:
            return b""
        end = min(self.pos + n, self.size) - 1
        req = urllib.request.Request(self.url, headers={"Range": f"bytes={self.pos}-{end}"})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        self.pos += len(data)
        return data

    def readinto(self, b):
        data = self.read(len(b))
        b[: len(data)] = data
        return len(data)


def with_retry(fn, tries=8):
    """Retry on HTTP 429 / transient errors with exponential backoff."""
    for k in range(tries):
        try:
            return fn()
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            if k == tries - 1:
                raise
            time.sleep(min(60, 2 ** k * 2))


def index_shard(split, i):
    return with_retry(lambda: _index_shard(split, i))


def _index_shard(split, i):
    url = f"{BASE}/{split}/{i}.parquet"
    f = HTTPRangeFile(url)
    pf = pq.ParquetFile(f)
    rows = pf.metadata.num_rows
    langs, projs = collections.Counter(), collections.Counter()
    for rg in range(pf.num_row_groups):
        t = pf.read_row_group(rg, columns=["language", "project"])
        langs.update(t.column("language").to_pylist())
        projs.update(t.column("project").to_pylist())
    fmt = lambda c: ";".join(f"{k}:{v}" for k, v in c.most_common())
    return dict(split=split, shard=i, bytes=f.size, rows=rows, languages=fmt(langs), projects=fmt(projs))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    out = os.path.expanduser(args.out)
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "catmus_index.csv")
    rows = []
    if os.path.exists(path):  # resume: keep shards already indexed
        with open(path) as fh:
            rows = [dict(r, shard=int(r["shard"]), bytes=int(r["bytes"]), rows=int(r["rows"])) for r in csv.DictReader(fh)]
    done = {(r["split"], r["shard"]) for r in rows}
    jobs = [(s, i) for s, n in N_SHARDS.items() for i in range(n) if (s, i) not in done]
    print(f"{len(done)} shards already indexed, {len(jobs)} to go")
    with cf.ThreadPoolExecutor(args.workers) as ex:
        futs = {ex.submit(index_shard, s, i): (s, i) for s, i in jobs}
        for fu in cf.as_completed(futs):
            try:
                rows.append(fu.result())
            except Exception as e:  # keep going; report failures
                s, i = futs[fu]
                print(f"FAILED {s}/{i}: {e}")
    rows.sort(key=lambda r: (r["split"], r["shard"]))
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {path}: {len(rows)} shards")


if __name__ == "__main__":
    main()
