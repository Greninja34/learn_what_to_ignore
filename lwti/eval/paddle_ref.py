"""Off-the-shelf reference: PaddleOCR PP-OCRv6 text recognition on our test lines.

Three steps, because PaddleOCR lives in the `ocr` conda env:

  1. (research2) export test lines to PNG + a list file
       python -m lwti.eval.paddle_ref export --data iam
  2. (ocr env) recognise them -- standalone, no lwti imports
       ~/miniconda3/envs/ocr/bin/python lwti/eval/paddle_ref.py run --data iam
  3. (research2) score with the project's CER and append to results/reference.csv
       python -m lwti.eval.paddle_ref score --data iam

The model is used as shipped (no fine-tuning), on the same height-64 gray
line images our models see. It answers "why not just use an existing OCR?".
"""
import argparse
import os
import sys

WORK = os.path.expanduser("~/data/lwti/paddle_ref")
MODEL = "PP-OCRv6_medium_rec"


def export(data):
    from PIL import Image
    from lwti.data.common import png_decode
    from lwti.data.dataset import load_frame
    d = os.path.join(WORK, data)
    os.makedirs(os.path.join(d, "img"), exist_ok=True)
    df = load_frame(data, "test")
    with open(os.path.join(d, "list.tsv"), "w") as fh:
        for i, t, b in zip(df.id, df.text, df.png):
            p = os.path.join(d, "img", f"{i}.png")
            Image.fromarray(png_decode(b)).save(p)
            fh.write(f"{i}\t{p}\t{t}\n")
    print(f"exported {len(df)} lines to {d}")


def run(data, device):
    from paddleocr import TextRecognition
    d = os.path.join(WORK, data)
    items = [l.rstrip("\n").split("\t") for l in open(os.path.join(d, "list.tsv"))]
    rec = TextRecognition(model_name=MODEL, device=device)
    with open(os.path.join(d, "pred.tsv"), "w") as fh:
        for k in range(0, len(items), 64):
            chunk = items[k: k + 64]
            out = rec.predict([p for _, p, _ in chunk], batch_size=32)
            for (i, _, _), r in zip(chunk, out):
                fh.write(f"{i}\t{r['rec_text']}\n")
            print(f"{min(k + 64, len(items))}/{len(items)}", flush=True)


def score(data):
    import csv
    import datetime
    from lwti.eval.cer import cer
    from lwti.data.common import norm_text
    d = os.path.join(WORK, data)
    refs = {l.split("\t")[0]: l.rstrip("\n").split("\t")[2] for l in open(os.path.join(d, "list.tsv"))}
    preds = {}
    for l in open(os.path.join(d, "pred.tsv")):
        i, _, h = l.rstrip("\n").partition("\t")
        preds[i] = norm_text(h)
    ids = list(refs)
    c = cer([refs[i] for i in ids], [preds.get(i, "") for i in ids])
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path = os.path.join(root, "results", "reference.csv")
    new = not os.path.exists(path)
    with open(path, "a", newline="") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(["date", "system", "data", "split", "n_lines", "test_cer", "note"])
        w.writerow([datetime.datetime.now().isoformat(timespec="minutes"), f"PaddleOCR {MODEL}", data, "test",
                    len(ids), round(c, 5), "off the shelf, no fine-tuning"])
    print(f"PaddleOCR {MODEL} on {data} test: CER {c * 100:.2f}% ({len(ids)} lines)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["export", "run", "score"])
    ap.add_argument("--data", required=True)
    ap.add_argument("--device", default="cpu")
    a = ap.parse_args()
    if a.step == "run":
        run(a.data, a.device)
    elif a.step == "export":
        export(a.data)
    else:
        score(a.data)
