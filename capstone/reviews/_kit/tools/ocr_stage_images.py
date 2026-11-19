"""Run one document through PaddleOCR and save an image per OCR stage, for the
"How OCR works" slide. Stages match the slide: 1 acquisition & pre-processing,
2 layout analysis, 3 text detection, 4 text recognition, 5 post-processing.

Run with the `ocr` conda env (PaddleOCR 3.x):
    ~/miniconda3/envs/ocr/bin/python tools/ocr_stage_images.py tools/receipt.png
Writes PNGs into assets/img/ocr_stages/.

The input is a flat scan, so stage 1 first simulates a phone photo of it
(tilt, shadow, noise) and then lets PaddleOCR's DocPreprocessor undo it.
"""
import re
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from paddleocr import DocPreprocessor, LayoutDetection, TextDetection, TextRecognition

OUT = Path(__file__).resolve().parent.parent / "assets" / "img" / "ocr_stages"
W, H = 840, 1000                      # every stage image has the same size, so they line up on the slide
ACCENT = (0, 120, 205)                # deck blue, #0078CD
INK, META, CARD = (18, 21, 27), (89, 96, 107), (235, 240, 244)
NUNITO = Path.home() / ".local/share/fonts/nunito"
MONO = "/usr/share/fonts/urw-base35/NimbusMonoPS-Regular.otf"


def font(size, weight=400):
    return ImageFont.truetype(str(NUNITO / f"nunito-latin-{weight}-normal.ttf"), size)


def fit(img, w=W, h=H, bg=(255, 255, 255)):
    """Letterbox an RGB array into a w x h white canvas."""
    im = Image.fromarray(img)
    im.thumbnail((w, h), Image.LANCZOS)
    canvas = Image.new("RGB", (w, h), bg)
    canvas.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    return canvas


def simulate_capture(page):
    """A flat scan made to look like a phone photo: on a table, tilted, unevenly lit, noisy."""
    h, w = page.shape[:2]
    pad = int(0.18 * max(h, w))
    table = np.full((h + 2 * pad, w + 2 * pad, 3), (196, 188, 176), np.uint8)
    table[pad:pad + h, pad:pad + w] = page
    src = np.float32([[pad, pad], [pad + w, pad], [pad + w, pad + h], [pad, pad + h]])
    dst = src + np.float32([[60, 40], [-30, 90], [40, -20], [-50, -60]])
    warped = cv2.warpPerspective(table, cv2.getPerspectiveTransform(src, dst), table.shape[1::-1],
                                 borderValue=(196, 188, 176))
    yy, xx = np.mgrid[0:warped.shape[0], 0:warped.shape[1]]
    shade = 0.65 + 0.35 * (xx / warped.shape[1]) * (1 - 0.4 * yy / warped.shape[0])
    noisy = warped * shade[..., None] + np.random.default_rng(0).normal(0, 6, warped.shape)
    return cv2.GaussianBlur(np.clip(noisy, 0, 255).astype(np.uint8), (3, 3), 0)


def crop_poly(img, poly):
    """Perspective-crop a 4-point text polygon to an upright strip."""
    p = np.float32(poly)
    w = int(max(np.linalg.norm(p[0] - p[1]), np.linalg.norm(p[3] - p[2])))
    h = int(max(np.linalg.norm(p[0] - p[3]), np.linalg.norm(p[1] - p[2])))
    m = cv2.getPerspectiveTransform(p, np.float32([[0, 0], [w, 0], [w, h], [0, h]]))
    return cv2.warpPerspective(img, m, (w, h), borderMode=cv2.BORDER_REPLICATE)


def rows(polys, texts):
    """Group text boxes into printed rows (by vertical overlap), each read left to right."""
    items = sorted(zip(polys, texts), key=lambda pt: pt[0][:, 1].mean())
    out = []
    for p, t in items:
        cy, h = p[:, 1].mean(), np.ptp(p[:, 1])
        if out and abs(cy - out[-1]["cy"]) < 0.5 * h:
            out[-1]["parts"].append((p[:, 0].min(), t))
        else:
            out.append({"cy": cy, "parts": [(p[:, 0].min(), t)]})
    return ["  ".join(t for _, t in sorted(r["parts"])) for r in out]


def post_process(lines):
    """Turn raw OCR lines into checked fields: the kind of rules stage 5 applies."""
    text = "\n".join(lines)
    num = lambda pat: (m := re.search(pat, text, re.I)) and float(m.group(1))
    fields = {
        "Store": (m := re.search(r"Store\s*#\s*(\d+)", text)) and f"#{m.group(1)}",
        "Date": (m := re.search(r"(\d{1,2})/(\d{1,2})/(\d{2})\b", text)) and f"20{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}",
        "Time": (m := re.search(r"(\d{1,2}:\d{2}\s*[AP]M)", text, re.I)) and m.group(1).upper(),
        "Subtotal": num(r"Subtotal\s+(\d*\.\d{2})"),
        "Tax": num(r"Tax\s+(\d*\.\d{2})"),
        "Total": num(r"\bTotal\s+(\d*\.\d{2})"),
    }
    ok = None
    if all(isinstance(fields[k], float) for k in ("Subtotal", "Tax", "Total")):
        ok = abs(fields["Subtotal"] + fields["Tax"] - fields["Total"]) < 0.005
    return fields, ok


def main(path):
    OUT.mkdir(parents=True, exist_ok=True)
    page = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)

    # 1 · acquisition & pre-processing: simulated photo -> orientation fix + unwarping
    photo = simulate_capture(page)
    cv2.imwrite(str(OUT / "1_capture.png"), cv2.cvtColor(photo, cv2.COLOR_RGB2BGR))
    pre = DocPreprocessor(use_doc_orientation_classify=True, use_doc_unwarping=True)
    clean = pre.predict(str(OUT / "1_capture.png"))[0]["output_img"]   # BGR
    clean = cv2.cvtColor(clean, cv2.COLOR_BGR2RGB)
    pair = Image.new("RGB", (W, H), "white")
    for i, (im, lab) in enumerate([(photo, "captured"), (clean, "pre-processed")]):
        tile = fit(im, W // 2 - 20, H - 70)
        pair.paste(tile, (10 + i * W // 2, 10))
        ImageDraw.Draw(pair).text((W // 4 + i * W // 2, H - 40), lab, fill=META, font=font(30, 600), anchor="mm")
    pair.save(OUT / "1_preprocess.png")

    # 2 · layout analysis
    lay = LayoutDetection().predict(path)[0]["boxes"]
    M = 48                                               # white margin so every tag fits above its box
    im = Image.new("RGB", (page.shape[1] + 2 * M, page.shape[0] + 2 * M), "white")
    im.paste(Image.fromarray(page), (M, M))
    d = ImageDraw.Draw(im)
    for b in lay:
        x0, y0, x1, y1 = (int(v) + M for v in b["coordinate"])
        d.rectangle([x0, y0, x1, y1], outline=ACCENT, width=6)
        lab = f"{b['label']} {b['score']:.2f}"
        tw = d.textlength(lab, font=font(30, 700))
        ty = y0 - 40
        d.rectangle([x0, ty, x0 + tw + 16, ty + 40], fill=ACCENT)
        d.text((x0 + 8, ty + 2), lab, fill="white", font=font(30, 700))
    fit(np.array(im)).save(OUT / "2_layout.png")

    # 3 · text detection
    polys = [np.array(p, int) for p in TextDetection(model_name="PP-OCRv6_medium_det").predict(path)[0]["dt_polys"]]
    polys.sort(key=lambda p: (p[:, 1].mean() // 20, p[:, 0].min()))          # reading order: top-down, then left-right
    im = Image.fromarray(page)
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for p in polys:
        od.polygon([tuple(v) for v in p], fill=ACCENT + (40,), outline=ACCENT + (255,), width=4)
    fit(np.array(Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB"))).save(OUT / "3_detection.png")

    # 4 · text recognition: every line, then show a few crops with their predictions
    crops = [crop_poly(page, p) for p in polys]
    rec = TextRecognition(model_name="PP-OCRv6_medium_rec").predict(crops)
    lines = [(r["rec_text"], r["rec_score"]) for r in rec]
    show = [i for i, (t, _) in enumerate(lines) if re.search(r"Total|Cashier|SALE|Store", t)][:5]
    canvas = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(canvas)
    y = 30
    for i in show:
        c = Image.fromarray(crops[i])
        c.thumbnail((W - 60, 80), Image.LANCZOS)
        d.rectangle([28, y - 2, 32 + c.width, y + c.height + 2], outline=CARD, width=2)
        canvas.paste(c, (30, y))
        y += c.height + 12
        d.line([30, y + 22, 58, y + 22], fill=ACCENT, width=4)              # arrow drawn, not typed:
        d.polygon([(66, y + 22), (54, y + 14), (54, y + 30)], fill=ACCENT)    # Nunito has no "→"
        d.text((78, y), lines[i][0], fill=ACCENT, font=font(34, 700))
        d.text((W - 30, y + 4), f"{lines[i][1]:.2f}", fill=META, font=font(26, 600), anchor="ra")
        y += 70
    canvas.save(OUT / "4_recognition.png")

    # 5 · post-processing: raw lines -> checked fields
    text_rows = rows(polys, [t for t, _ in lines])
    fields, ok = post_process(text_rows)
    canvas = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(canvas)
    d.text((30, 30), "raw text", fill=META, font=font(28, 700))
    raw = [r for r in text_rows if re.search(r"Store|Cashier|Items|Tax|Total", r)][:7]
    for k, t in enumerate(raw):
        d.text((30, 75 + k * 38), t[:34], fill=INK, font=ImageFont.truetype(MONO, 28))
    y = 75 + len(raw) * 38 + 30
    d.line([30, y, W - 30, y], fill=CARD, width=3)
    d.text((30, y + 20), "fields", fill=META, font=font(28, 700))
    y += 70
    for k, v in fields.items():
        d.text((30, y), k, fill=META, font=font(32, 600))
        d.text((260, y), "–" if v is None else (f"{v:.2f}" if isinstance(v, float) else str(v)), fill=INK, font=font(32, 700))
        y += 50
    if ok is not None:
        msg = "subtotal + tax = total" if ok else "subtotal + tax ≠ total: flag for review"
        colour = ACCENT if ok else (219, 56, 55)
        d.text((30, y + 10), msg, fill=colour, font=font(32, 700))
        if ok:                                                                # tick drawn, not typed
            x = 30 + d.textlength(msg, font=font(32, 700)) + 18
            d.line([(x, y + 32), (x + 10, y + 44), (x + 30, y + 18)], fill=colour, width=5)
    canvas.save(OUT / "5_postprocess.png")

    print("\n".join(f"{s:.2f}  {t}" for t, s in lines))
    print(fields, "check:", ok)
    print("wrote", sorted(p.name for p in OUT.glob("*.png")))


if __name__ == "__main__":
    main(sys.argv[1])
