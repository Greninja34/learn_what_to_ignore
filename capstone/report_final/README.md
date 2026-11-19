# Phase 1 report: content for the Word version

| File | What it is |
|---|---|
| `00_front_matter.md` | What goes on pages 1–4 (you build these in Word from `capstone/format/report_template/`), the full **abstract** for page 5, and how to auto-generate the TOC / list of tables / list of figures |
| `report.md` | **Pages 6 onwards**: all chapters, references (IEEE, numbered in order of first citation) and Appendix A |
| `report.tex` | The same content as a plain LaTeX `report` (pandoc output, no styling) |
| `report.pdf` | Preview only, to check flow. Not the submission. |
| `figures/` | The 4 figures used in the report |
| `WORD_FORMATTING.md` | Exact Word settings: page setup, styles, header/footer, sections, TOC |
| `build.sh` | Rebuilds `report.tex` / `report.pdf` from `report.md` |

Chapters follow the template TOC: Introduction · Problem Statement · Literature
Survey · Research Gap and Objectives · Overview of Datasets (Description, Data
Attributes) · Proposed Approach and Pilot Results (the light code/results part) ·
Conclusion and Plan of Work (guideline 9 asks for the conclusion and the Phase 2
plan together) · References · Appendix A.

## Page budget (limit: 20–25 pages including front matter)

Front matter in Word = about 8 pages (title, certificate, declaration,
acknowledgement, abstract, TOC, list of tables, list of figures). The body in the
LaTeX preview is about 22 pages, but LaTeX wastes space on narrow tables and
chapter openings; in Word (Times New Roman 12, 1.5 spacing, 2 cm margins) expect
roughly 17–19. If the total goes over 25, cut in this order:

1. Figure 5.2 (statistic histograms): Table 5.2 already has the numbers. (~0.5 page)
2. Figure 5.1 (sample lines). (~0.5 page)
3. The code block in 6.1 (the equation and prose explain it). (~0.3 page)
4. Shorten 3.1 to one paragraph per paper. (~0.5 page)

## Things to check or fill in before submitting

- Template certificate typos: UE23CS320A → UE24CS320A, "Aug 2025" → Aug 2026.
- Two references lack first-author initials (LoGo-HTR [11]: "Mitra, Mondal";
  PreP-OCR [16]: "Guan et al."). Look them up and add initials.
- The panel asked for user statistics. Section 1.2 backs the use case with our
  own measured numbers (PaddleOCR 52.5% CER on medieval lines, error rising
  from 19.9% to 43.3% as labels drop). If you add outside numbers (for example,
  how many manuscripts an archive or national mission holds), cite a source
  for each one.
- Captions: in Word use Insert Caption so tables and figures are numbered by
  chapter (Table 2.1, Figure 5.1, ...). The text already refers to Table 5.2,
  Table 6.1 and Figure 6.1; the equation is numbered (6.1).
- The guidelines allow at most 15% plagiarism. The text is written fresh, but
  run it through the checker and reword any flagged lines.

## Rebuilding on Windows (optional)

Install pandoc. `pandoc report.md -o report.docx` gives a quick Word draft you
can paste from (tables and figures come across). For LaTeX, install MiKTeX and
run the two `pandoc` lines in `build.sh`.
