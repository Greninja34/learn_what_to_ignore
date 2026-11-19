# Reviews (Team 147)

Pick the folder for the review you need. Every review folder has the same four things.

| Folder | Review | When | Edit this | Handed in |
|---|---|---|---|---|
| `review1/` | ISA Review 1 | held 15 Oct, submitted 26 Oct | `deck/slides.md` (later edits: approval slide etc.; the submitted version is in `submission/`) | `submission/` |
| `review2/` | ISA Review 2 (with the guide) | Fri 13 Nov | `deck/slides.md` | `submission/` |
| `review3/` | End-semester assessment (ESA) | Tue 17 Nov | `deck/slides.md` | `submission/` |

Inside each review folder:

- `deck/slides.md`: the slides. Edit this one file.
- `deck/out/`: the PDF, editable PPTX and HTML presenter view built from it.
- `submission/`: what was or will be handed in (PDF + PPTX without speaker notes).
- `template/`: the college template for that review.

To rebuild a deck: `cd _kit && ./build.sh review2` (needs the `research2` conda env). It overwrites that review's `deck/out/`.

`_kit/` holds the shared parts (theme, images, fonts, build script). Don't put review content there. See `_kit/README.md`.
