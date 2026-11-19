# Word formatting: exact settings

Taken from the department guidelines and the template .docx files in
`capstone/format/report_template/`. Where the two disagree, the guidelines win
(noted below).

## 1. Page setup (whole document)

| Setting | Value | Where in Word |
|---|---|---|
| Paper size | **A4** (the template files are US Letter; the guidelines say A4) | Layout → Size → A4 |
| Margins | **2.00 cm** top, bottom, left, right | Layout → Margins → Custom Margins |
| Header / footer distance from edge | **1.0 cm** | Layout → Margins → Layout tab → From edge |
| Gutter | 0 | same dialog |

## 2. Text styles (set these once in the Styles pane: right-click → Modify)

| Style | Font | Size | Bold | Alignment | Spacing |
|---|---|---|---|---|---|
| Normal (body text) | Times New Roman | 12 | no | **Justified** | **1.5 lines**, 0 pt before, 6 pt after |
| Heading 1 (chapter) | Times New Roman | **18** | yes | **Centered** | single, 0 pt before, 18 pt after (no "page break before": the section break starts the new page) |
| Heading 2 (section, e.g. 2.1) | Times New Roman | **16** | yes | **Left** | single, 12 pt before, 6 pt after, "Keep with next" |
| Heading 3 (subsection, e.g. 2.1.1) | Times New Roman | **14** | yes | **Left** | single, 12 pt before, 6 pt after, "Keep with next" |
| Table text | Times New Roman | 11 (12 if it fits) | header row bold | Left | **single**, 0 pt before/after |
| Figure Caption (new style, based on Caption) | Times New Roman | 11 | label bold ("Figure 5.1:") | Centered | single, 6 pt before, 12 pt after; **below** the figure |
| Table Caption (new style, based on Caption) | Times New Roman | 11 | label bold ("Table 5.2:") | Centered | single, 12 pt before, 6 pt after; **above** the table |
| Code | Consolas | 10 | no | Left | single, light grey shading |
| References | Times New Roman | 12 | no | Justified, **hanging indent 1 cm** | single, 6 pt after |

Notes:
- Turn off Heading colours: Word's default headings are blue. Set font colour to **Automatic/black**.
- 1.5 spacing applies **only to body text** (guideline 7). Tables, captions, code and references at single spacing are allowed and save about two pages.
- Body is **justified**. Headings are **left-aligned**, except the chapter heading, which is **centred**.

## 3. Chapter heading layout (matches template "Page 9")

Type each chapter heading as one Heading 1 paragraph with a line break inside:

```
CHAPTER 1        ← Shift+Enter (line break, not Enter)
INTRODUCTION
```

Both lines centred, 18 pt bold, in capitals. Section and subsection numbers are
typed by hand ("1.1 Background", "1.2.1 ..."); do not use Word's auto-numbering.
It breaks easily when you paste text.

## 4. Header and footer (from template "Page 10 onwards")

**No header or footer on pages 1–8** (title, certificate, declaration,
acknowledgement, abstract, TOC, lists). They **start at Chapter 1**, and the
page number restarts at **1** there.

**Header** (Times New Roman 10):
- Left: short project title, **Learning What to Ignore**
- Right: the PES University logo (the template header already has it; keep it).
- A line under the header: Home → Borders → Bottom Border on the header paragraph (cleaner than the template's row of underscores).

**Footer** (Times New Roman 10), one line with a line above it:

```
Dept. of CSE                 Aug-Dec 2026                 1
(left)                       (centre)                 (right)
```

- Put a Top Border on the footer paragraph (Home → Borders → Top Border).
- Tab stops: centre tab at **8.5 cm**, right tab at **17 cm**. Type `Dept. of CSE`, Tab, `Aug-Dec 2026`, Tab, then Insert → Page Number → Current Position → Plain Number.
- The two template files spell it differently ("Aug-Dec 2026" and "AUG-DEC, 2026"). Use **Aug-Dec 2026** everywhere.

**First page of every chapter: footer only, no header** (guideline 15).

## 5. How to set up the sections (do this once)

1. Pages 1–8: separate pages with **Page Break** (Ctrl+Enter).
2. Before Chapter 1: Layout → Breaks → **Section Break (Next Page)**.
3. Double-click the Chapter 1 header. In the Header & Footer tab, **untick "Link to Previous"** for both header and footer, and **tick "Different First Page"**.
4. Fill in the header and footer as in section 4. Then go to the **first-page footer** of Chapter 1 and put the **same footer** there; leave the first-page header empty.
5. Header & Footer → Page Number → Format Page Numbers → **Start at: 1**, format 1, 2, 3.
6. Go back to section 1 (pages 1–8) and delete anything in its header and footer.
7. Before **every later chapter**, insert a **Section Break (Next Page)** instead of a page break. New sections copy the settings (keep "Link to Previous" **on** from Chapter 2 onwards). In Format Page Numbers choose **"Continue from previous section"**.


## 6. Front pages (1–5)

- Build pages 1–2 by **opening the template file itself** ("Page 1-2.docx"), filling in the names, then Save As your report file. This keeps the logo and layout exactly.
- Open "Page 3-8.docx", copy its pages, and paste into your file with **Keep Source Formatting** (Ctrl+V, then Ctrl → K). Insert a page break between pages.
- Set all front pages to Times New Roman. The template's default font is Liberation Serif, which shows up if you paste plain text.
- Abstract heading: "ABSTRACT", 18 pt bold, centred. Abstract text: 12 pt, justified, 1.5 spacing, about 250 words, fits one page.
- Declaration, Acknowledgement, Abstract, TOC and lists each start on a new page.

## 7. Table of contents and lists (pages 6–8)

1. TOC: References → Table of Contents → **Custom Table of Contents** → Show levels **2**, tick "Right align page numbers", tab leader dots. Title it "TABLE OF CONTENTS" (18 pt bold centred, not a Heading style, so it does not list itself).
2. List of Figures: References → Insert Table of Figures → Options → tick **Style**, choose **Figure Caption** → OK. Title "LIST OF FIGURES".
3. List of Tables: same, with style **Table Caption**. Title "LIST OF TABLES".
4. Type every caption by hand with chapter numbers: "Table 5.2: Damage statistics on IAM and CATMuS lines", "Figure 6.1: The proposed approach...". The numbers in `report.md` already follow this.
5. At the end: Ctrl+A, then **F9** → "Update entire table", to refresh all page numbers.

## 8. Figures, tables, equation

- Insert figures with Insert → Pictures, **In Line with Text** wrapping, centred, width at most 17 cm (the text width). Figures are in `figures/`.
- Tables: Insert → Table, style "Table Grid", header row bold. Set **Table Properties → Row → "Allow row to break across pages" off** for small tables, and "Repeat as header row" on for long ones.
- Equation 6.1: Insert → Equation, then press Tab and type **(6.1)** right-aligned (guideline 11 asks for decimal numbering).

## 9. Final checks

- Total pages: 20–25 including pages 1–8. If over, see the cut list in `README.md`.
- File → Export → PDF. Open the PDF and check that headers/footers do not appear before Chapter 1 and that each chapter's first page has a footer but no header.
- Run the plagiarism check (PESU library, at most 15%).
