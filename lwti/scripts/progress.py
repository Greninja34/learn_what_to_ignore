"""Print the pilot comparison table (test CER %, one value per seed) and the run in progress.

    ~/miniconda3/envs/research2/bin/python ~/Desktop/research/lwti/scripts/progress.py
(watch.sh calls this every 10 s.)
"""
import glob
import os
import re

import pandas as pd

ROOT = os.path.expanduser("~/Desktop/research")
LOGS = os.path.expanduser("~/data/lwti/logs")
NAMES = {"scratch": "no pretrain", "cmae_none": "masking", "cmae_handpicked": "+ hand-picked",
         "cmae_derived_v0": "+ derived"}
SETTINGS = [("catmus", 0.05), ("iam", 0.1), ("iam", 0.01)]

r = pd.read_csv(os.path.join(ROOT, "results", "runs.csv"))
r = r[(r.model == "crnn") & (r.frac < 1)].drop_duplicates("run", keep="last").copy()
r["tag"] = r.tag.fillna("").replace("", "scratch")
rows, done = [], 0
for d, f in SETTINGS:
    row = {"setting": f"{d} {f * 100:g}%"}
    for t, n in NAMES.items():
        v = r[(r.data == d) & (r.frac == f) & (r.tag == t)].sort_values("seed").test_cer.tolist()
        done += len(v) if t != "scratch" else 0
        row[n] = " / ".join(f"{x * 100:.1f}" for x in v) if v else "…"
    rows.append(row)
print(f"pretrained fine-tunes finished: {done} / 18   (test CER %, seed 0 / seed 1; lower is better)\n")
print(pd.DataFrame(rows).to_string(index=False))

logs = sorted(glob.glob(os.path.join(LOGS, "*crnn*.log")) + glob.glob(os.path.join(LOGS, "cmae_*.log")),
              key=os.path.getmtime)
if logs:
    last = logs[-1]
    steps = [l for l in open(last, errors="ignore") if re.match(r"step\s+\d+", l)]
    finished = any("TEST CER" in l for l in open(last, errors="ignore"))
    status = "finished" if finished else (steps[-1].strip() if steps else "starting")
    print(f"\nlatest run: {os.path.basename(last)[:-4]}\n  {status}")
