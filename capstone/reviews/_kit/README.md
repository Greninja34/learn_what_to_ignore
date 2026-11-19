# _kit: shared parts for all review decks

| Path | What |
|---|---|
| `build.sh` | Builds one review: `./build.sh review1`, `review2` or `review3` (writes to that review's `deck/out/`) |
| `theme.css` | The slide theme (also used by the VS Code Marp preview) |
| `gantt.md` | The timeline slide; `build.sh` makes `assets/img/gantt.png` from it |
| `assets/` | Images, damage strips, hand-drawn sketches, PES emblem |
| `fonts_for_powerpoint/` | Install these before opening a `.pptx` (see its `README.txt`) |
| `tools/to_pptx.js` | Builds the editable PPTX from the rendered slides |
| `tools/make_sketches.js`, `tools/ocr_stage_images.py` | Regenerate the sketches and the OCR stage images |
| `tools/strip_notes.py`, `tools/shrink_pptx.py` | Make the review-submission copy (no speaker notes, smaller file) |
| `design/` | Claude Design template and design brief |

Rebuilding a review overwrites its `deck/out/` files, so check `submission/` before you rebuild if it matters which version was handed in.
