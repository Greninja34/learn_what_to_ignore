"""Build the Phase-1 report (.docx) from report/report.md in the PES department format.

Format (from format/Report.zip guidelines): A4, 2 cm margins, Times New Roman,
body 12 pt justified with 1.5 line spacing; chapter number + title centred 18 pt;
section 16 pt bold, subsection 14 pt bold, left; figures and tables numbered by
chapter; IEEE references numbered in order of first citation; header (project
title) and footer (Dept. of CSE / AUG-DEC, 2026 / page number) from the
Introduction on; a chapter's first page has the footer only.

Usage (research2 env, from ~/Desktop/research):
    python capstone/report/build_report.py
Output: capstone/report/Team147_Phase1_Report_DRAFT.docx
Open in Word and press Ctrl+A then F9 (or accept the "update fields" prompt) to
fill the table of contents and the lists of tables and figures.
"""
import os
import re
import zipfile

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_COLOR_INDEX, WD_LINE_SPACING, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # research/capstone
RESEARCH = os.path.dirname(ROOT)  # research/ (figure paths in report.md are relative to this)
SRC = os.path.join(ROOT, "report", "report.md")
OUT = os.path.join(ROOT, "report", "Team147_Phase1_Report_DRAFT.docx")
TEMPLATE_ZIP = os.path.join(ROOT, "format", "Report.zip")
FONT = "Times New Roman"

TITLE = "Learning What to Ignore: Deriving Invariance for Self-Supervised Text Recognition"
SHORT_TITLE = "Learning What to Ignore"
TEAM = [("Arvind Kothamangala", "PES2UG24CS628"), ("Atharv Sawarkar", "PES2UG24CS670"),
        ("Vignesh Nunna", "PES2UG24CS582"), ("Rohit Rajan", "PES2UG25CS821")]
GUIDE = "Dr. Chandrashekhar P Chavan"
GUIDE_DESIG = "⟦Designation⟧"

BIB = {
    "iam": 'U.-V. Marti and H. Bunke, "The IAM-database: An English sentence database for offline handwriting recognition," <i>International Journal on Document Analysis and Recognition</i>, vol. 5, no. 1, pp. 39–46, 2002.',
    "catmus": 'T. Clérice et al., "CATMuS Medieval: A multilingual large-scale cross-century dataset in Latin script for handwritten text recognition and beyond," in <i>Proc. International Conference on Document Analysis and Recognition (ICDAR)</i>, 2024.',
    "survey": 'C. Penarrubia, J. J. Valero-Mas, and J. Calvo-Zaragoza, "Self-supervised learning for text recognition: A critical survey," <i>International Journal of Computer Vision</i>, 2025, arXiv:2407.19889.',
    "seqclr": 'A. Aberdam, R. Litman, S. Tsiper, O. Anschel, R. Slossberg, S. Mazor, R. Manmatha, and P. Perona, "Sequence-to-sequence contrastive learning for text recognition," in <i>Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)</i>, 2021.',
    "kiss": 'M. Kišš and M. Hradiš, "Self-supervised pre-training of text recognizers," in <i>Proc. International Conference on Document Analysis and Recognition (ICDAR)</i>, 2024, arXiv:2405.00420.',
    "textdiae": 'M. A. Souibgui, S. Biswas, A. Mafla, A. F. Biten, A. Fornés, Y. Kessentini, J. Lladós, L. Gomez, and D. Karatzas, "Text-DIAE: A self-supervised degradation invariant autoencoder for text recognition and document enhancement," in <i>Proc. AAAI Conference on Artificial Intelligence</i>, 2023, arXiv:2203.04814.',
    "garrido": 'C. Garrido-Munoz and J. Calvo-Zaragoza, "Handwritten text recognition lives in the high-pixel variance subspace," in <i>Advances in Neural Information Processing Systems (NeurIPS)</i>, 2026, arXiv:2609.35473.',
    "ericsson": 'L. Ericsson, H. Gouk, and T. M. Hospedales, "Why do self-supervised models transfer? Investigating the impact of invariance on downstream tasks," in <i>Proc. British Machine Vision Conference (BMVC)</i>, 2022, arXiv:2111.11398.',
    "mintun": 'E. Mintun, A. Kirillov, and S. Xie, "On interaction between augmentations and corruptions in natural corruption robustness," in <i>Advances in Neural Information Processing Systems (NeurIPS)</i>, 2021, arXiv:2102.11273.',
    "logo": 'S. Mitra, A. Mondal, and C. V. Jawahar, "Learning beyond labels: Self-supervised handwritten text recognition," in <i>Proc. IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)</i>, 2026.',
    "lacuna": 'N. Vogler, J. P. Allen, M. T. Miller, and T. Berg-Kirkpatrick, "Lacuna reconstruction: Self-supervised pre-training for low-resource historical document transcription," in <i>Findings of the Association for Computational Linguistics: NAACL</i>, 2022, arXiv:2112.08692.',
    "mae": 'K. He, X. Chen, S. Xie, Y. Li, P. Dollár, and R. Girshick, "Masked autoencoders are scalable vision learners," in <i>Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)</i>, 2022.',
    "vicreg": 'A. Bardes, J. Ponce, and Y. LeCun, "VICReg: Variance-invariance-covariance regularization for self-supervised learning," in <i>Proc. International Conference on Learning Representations (ICLR)</i>, 2022.',
    "ijepa": 'M. Assran, Q. Duval, I. Misra, P. Bojanowski, P. Vincent, M. Rabbat, Y. LeCun, and N. Ballas, "Self-supervised learning from images with a joint-embedding predictive architecture," in <i>Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)</i>, 2023.',
    "augraphy": 'A. Groleau, K. W. Chee, S. Larson, S. Maini, and J. Boarman, "Augraphy: A data augmentation library for document images," arXiv:2208.14558, 2022.',
    "prepocr": 'S. Guan et al., "PreP-OCR: A complete pipeline for document image restoration and enhanced OCR accuracy," in <i>Proc. Annual Meeting of the Association for Computational Linguistics (ACL)</i>, 2025, arXiv:2505.20429.',
    "salerno": 'E. Salerno and A. Tonazzini, "Highly degraded recto-verso document image processing and understanding," <i>ERCIM News</i>, no. 95, 2013.',
    "hipe": '"ICDAR 2026 HIPE-OCRepair competition on LLM-assisted OCR post-correction for historical documents," arXiv:2607.08143, 2026.',
    "hanja": '"Leveraging external knowledge for historical document restoration via retrieval-augmented large language models," arXiv:2607.21936, 2026.',
    "crnn": 'B. Shi, X. Bai, and C. Yao, "An end-to-end trainable neural network for image-based sequence recognition and its application to scene text recognition," <i>IEEE Transactions on Pattern Analysis and Machine Intelligence</i>, vol. 39, no. 11, pp. 2298–2304, 2017.',
    "ctc": 'A. Graves, S. Fernández, F. Gomez, and J. Schmidhuber, "Connectionist temporal classification: Labelling unsegmented sequence data with recurrent neural networks," in <i>Proc. International Conference on Machine Learning (ICML)</i>, 2006, pp. 369–376.',
    "paddle": 'PaddlePaddle Authors, "PaddleOCR: Awesome multilingual OCR toolkits based on PaddlePaddle (PP-OCRv6)," GitHub repository, https://github.com/PaddlePaddle/PaddleOCR, accessed Nov. 2026.',
    "kanungo": 'T. Kanungo, R. M. Haralick, H. S. Baird, W. Stuetzle, and D. Madigan, "A statistical, nonparametric methodology for document degradation model validation," <i>IEEE Transactions on Pattern Analysis and Machine Intelligence</i>, vol. 22, no. 11, pp. 1209–1223, 2000.',
    "baird07": 'H. S. Baird, "The state of the art of document image degradation modelling," in <i>Digital Document Processing: Major Directions and Recent Advances</i>, B. B. Chaudhuri, Ed. London, U.K.: Springer, 2007, pp. 261–279.',
}


# ---------------------------------------------------------------- low-level helpers
def set_cell_shading(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tcPr.append(shd)


def para_border(p, side="bottom", sz=6):
    pPr = p._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    el = OxmlElement(f"w:{side}")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(sz))
    el.set(qn("w:space"), "1")
    el.set(qn("w:color"), "000000")
    bdr.append(el)
    pPr.append(bdr)


def add_field(p, instr, placeholder=""):
    """Insert a complex field (TOC, PAGE, ...) into paragraph p."""
    r = p.add_run()
    b = OxmlElement("w:fldChar")
    b.set(qn("w:fldCharType"), "begin")
    b.set(qn("w:dirty"), "true")
    r._r.append(b)
    r = p.add_run()
    t = OxmlElement("w:instrText")
    t.set(qn("xml:space"), "preserve")
    t.text = f" {instr} "
    r._r.append(t)
    r = p.add_run()
    s = OxmlElement("w:fldChar")
    s.set(qn("w:fldCharType"), "separate")
    r._r.append(s)
    if placeholder:
        p.add_run(placeholder)
    r = p.add_run()
    e = OxmlElement("w:fldChar")
    e.set(qn("w:fldCharType"), "end")
    r._r.append(e)


def set_font(run, size=None, bold=None, italic=None):
    run.font.name = FONT
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(a), FONT)
    if size:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


INLINE = re.compile(r"(\*\*.+?\*\*|\*[^*\s][^*]*?\*|⟦.+?⟧|<i>.+?</i>|\[@[\w-]+\])")


class Report:
    def __init__(self):
        self.doc = Document()
        self.cites = {}  # key -> number
        self.chapter = 0
        self.chap_label = ""
        self.fig = 0
        self.tab = 0
        self.setup_styles()

    # ---------------------------------------------------------------- styles
    def setup_styles(self):
        d = self.doc
        st = d.styles
        normal = st["Normal"]
        normal.font.name = FONT
        normal.font.size = Pt(12)
        normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
        pf = normal.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        pf.space_after = Pt(6)
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for name, size, align in (("Heading 1", 18, WD_ALIGN_PARAGRAPH.CENTER), ("Heading 2", 16, WD_ALIGN_PARAGRAPH.LEFT),
                                  ("Heading 3", 14, WD_ALIGN_PARAGRAPH.LEFT)):
            s = st[name]
            s.font.name = FONT
            s.font.size = Pt(size)
            s.font.bold = True
            s.font.italic = False
            s.font.color.rgb = RGBColor(0, 0, 0)
            rpr = s.element.get_or_add_rPr()
            rf = rpr.find(qn("w:rFonts"))
            if rf is None:
                rf = OxmlElement("w:rFonts")
                rpr.insert(0, rf)
            for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
                rf.set(qn(a), FONT)
            for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
                if rf.get(qn(a)) is not None:
                    del rf.attrib[qn(a)]
            s.paragraph_format.alignment = align
            s.paragraph_format.space_before = Pt(18 if size > 14 else 12)
            s.paragraph_format.space_after = Pt(10 if size > 14 else 6)
            s.paragraph_format.keep_with_next = True
            s.paragraph_format.line_spacing = 1.15
        for name in ("Figure Caption", "Table Caption"):
            s = st.add_style(name, 1)
            s.base_style = st["Normal"]
            s.font.size = Pt(11)
            s.font.bold = True
            s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            s.paragraph_format.space_before = Pt(4)
            s.paragraph_format.space_after = Pt(12)
            s.paragraph_format.line_spacing = 1.0
            s.paragraph_format.keep_with_next = name == "Table Caption"
        sec = d.sections[0]
        sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
        for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
            setattr(sec, m, Cm(2.0))
        # ask Word to refresh TOC / lists when the file is opened
        settings = d.settings.element
        uf = OxmlElement("w:updateFields")
        uf.set(qn("w:val"), "true")
        settings.append(uf)

    # ---------------------------------------------------------------- text
    def cite(self, key):
        if key not in BIB:
            raise KeyError(f"unknown citation key {key}")
        if key not in self.cites:
            self.cites[key] = len(self.cites) + 1
        return f"[{self.cites[key]}]"

    def runs(self, p, text, size=None, bold=None):
        for part in INLINE.split(text):
            if not part:
                continue
            b, i, hl = bold, None, False
            if part.startswith("**") and part.endswith("**"):
                part, b = part[2:-2], True
            elif part.startswith("<i>"):
                part, i = part[3:-4], True
            elif part.startswith("*") and part.endswith("*") and len(part) > 2:
                part, i = part[1:-1], True
            elif part.startswith("⟦"):
                part, hl = part[1:-1], True
            elif part.startswith("[@"):
                part = self.cite(part[2:-1])
            r = p.add_run(part)
            set_font(r, size, b, i)
            if hl:
                r.font.highlight_color = WD_COLOR_INDEX.YELLOW

    def para(self, text, align=None, size=None, bold=None, space_after=None, style=None, indent=None):
        p = self.doc.add_paragraph(style=style)
        if align is not None:
            p.alignment = align
        if space_after is not None:
            p.paragraph_format.space_after = Pt(space_after)
        if indent is not None:
            p.paragraph_format.left_indent = Cm(indent)
        self.runs(p, text, size, bold)
        return p

    def center(self, text, size=12, bold=False, after=4):
        p = self.para(text, WD_ALIGN_PARAGRAPH.CENTER, size, bold, after)
        p.paragraph_format.line_spacing = 1.15
        return p

    def page_break(self):
        self.doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    # ---------------------------------------------------------------- blocks
    def bullet(self, text, numbered=None):
        if numbered is None:
            p = self.doc.add_paragraph(style="List Bullet")
        else:
            p = self.doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.9)
            p.paragraph_format.first_line_indent = Cm(-0.6)
            r = p.add_run(f"{numbered}.\t")
            set_font(r)
        p.paragraph_format.space_after = Pt(3)
        self.runs(p, text)

    def figure(self, caption, path, width_cm=15.0):
        full = os.path.join(RESEARCH, path)
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.space_after = Pt(2)
        if os.path.exists(full):
            p.add_run().add_picture(full, width=Cm(min(width_cm, 17.0)))
        else:
            r = p.add_run(f"[missing figure: {path}]")
            r.font.highlight_color = WD_COLOR_INDEX.YELLOW
        self.fig += 1
        cp = self.doc.add_paragraph(style="Figure Caption")
        self.runs(cp, f"Figure {self.chap_label}.{self.fig}: {caption}")

    def table(self, caption, rows):
        self.tab += 1
        cp = self.doc.add_paragraph(style="Table Caption")
        self.runs(cp, f"Table {self.chap_label}.{self.tab}: {caption}")
        ncol = len(rows[0])
        t = self.doc.add_table(rows=len(rows), cols=ncol)
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        # column widths proportional to content length, within 17 cm
        lens = [max(min(len(re.sub(r"\[@[\w-]+\]", "[00]", r[c])), 60) for r in rows) + 4 for c in range(ncol)]
        total = sum(lens)
        widths = [Cm(17.0 * l / total) for l in lens]
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                cell = t.cell(i, j)
                cell.width = widths[j]
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.space_after = Pt(2)
                self.runs(p, val.strip(), size=10.5, bold=True if i == 0 else None)
                if i == 0:
                    set_cell_shading(cell, "E7E9EC")
        sp = self.doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(6)

    # ---------------------------------------------------------------- headers / footers
    def body_section(self, first=False):
        sec = self.doc.add_section(WD_SECTION.NEW_PAGE)
        sec.different_first_page_header_footer = True
        if first:
            # restart page numbering at 1 from the Introduction
            pg = OxmlElement("w:pgNumType")
            pg.set(qn("w:start"), "1")
            sec._sectPr.append(pg)
            for hdr in (sec.header, sec.first_page_header):
                hdr.is_linked_to_previous = False
            for ftr in (sec.footer, sec.first_page_footer):
                ftr.is_linked_to_previous = False
            # running header: title, rule
            hp = sec.header.paragraphs[0]
            hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = hp.add_run(TITLE)
            set_font(r, 10, italic=True)
            para_border(hp, "bottom")
            sec.first_page_header.paragraphs[0].text = ""
            for ftr in (sec.footer, sec.first_page_footer):
                fp = ftr.paragraphs[0]
                para_border(fp, "top")
                fp.paragraph_format.tab_stops.add_tab_stop(Cm(8.5), WD_TAB_ALIGNMENT.CENTER)
                fp.paragraph_format.tab_stops.add_tab_stop(Cm(17.0), WD_TAB_ALIGNMENT.RIGHT)
                for txt in ("Dept. of CSE\tAUG-DEC, 2026\tPage No. ",):
                    set_font(fp.add_run(txt), 10)
                add_field(fp, "PAGE", "1")
                for r in fp.runs:
                    set_font(r, 10)
        return sec

    # ---------------------------------------------------------------- front matter
    def front_matter(self, abstract):
        logo = self.logo_path()
        # --- title page
        self.center("Dissertation on", 14, after=6)
        self.center(f"“{TITLE}”", 18, True, 10)
        for line in ("Submitted in partial fulfillment of the requirements for", "Bachelor of Technology", "in",
                     "Computer Science & Engineering", "UE24CS320A – Capstone Project Phase - 1"):
            self.center(line, 13 if line.startswith(("Bachelor", "Computer")) else 12, line.startswith(("Bachelor", "Computer", "UE24")))
        self.center("Submitted by:", 12, after=4)
        t = self.doc.add_table(rows=len(TEAM), cols=2)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for i, (n, s) in enumerate(TEAM):
            for j, v in enumerate((n, s)):
                p = t.cell(i, j).paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_after = Pt(0)
                set_font(p.add_run(v), 12, bold=j == 0)
        self.center("", after=2)
        self.center("Under the guidance of", 12, after=2)
        self.center(GUIDE, 13, True, 0)
        self.center(GUIDE_DESIG, 12, after=0)
        self.center("PES University", 12, after=6)
        self.center("Aug - Dec 2026", 12, after=8)
        if logo:
            p = self.doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.add_run().add_picture(logo, width=Cm(4.5))
        for line, b in (("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", True), ("FACULTY OF ENGINEERING", True),
                        ("PES UNIVERSITY", True), ("(Established under Karnataka Act No. 16 of 2013)", False),
                        ("Electronic City, Hosur Road, Bengaluru – 560 100, Karnataka, India", False)):
            self.center(line, 12, b, 0)
        self.page_break()

        # --- certificate
        for line, b, s in (("PES UNIVERSITY", True, 14), ("(Established under Karnataka Act No. 16 of 2013)", False, 11),
                           ("Electronic City, Hosur Road, Bengaluru – 560 100, Karnataka, India", False, 11),
                           ("FACULTY OF ENGINEERING", True, 12)):
            self.center(line, s, b, 0)
        if logo:
            p = self.doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.add_run().add_picture(logo, width=Cm(3.0))
        self.center("CERTIFICATE", 16, True, 10)
        self.center("This is to certify that the dissertation entitled", 12, after=2)
        self.center(f"‘{TITLE}’", 13, True, 2)
        self.center("is a bonafide work carried out by", 12, after=4)
        t = self.doc.add_table(rows=len(TEAM), cols=2)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for i, (n, s) in enumerate(TEAM):
            for j, v in enumerate((n, s)):
                p = t.cell(i, j).paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_after = Pt(0)
                set_font(p.add_run(v), 12)
        self.para("In partial fulfillment for the completion of Fifth-semester Capstone Project Phase - 1 "
                  "(⟦UE24CS320A⟧) in the Program of Study - Bachelor of Technology in Computer Science and Engineering "
                  "under rules and regulations of PES University, Bengaluru during the period ⟦Aug – Dec. 2026⟧. It is "
                  "certified that all corrections/suggestions indicated for internal assessment have been incorporated "
                  "in the report. The dissertation has been approved as it satisfies the 5th-semester academic "
                  "requirements in respect of project work.")
        # signature blocks exactly as in the department template: guide and chairperson
        sig = self.doc.add_table(rows=4, cols=2)
        vals = [["", ""], ["Signature", "Signature"], [GUIDE, "Dr. Sandesh B J"], [GUIDE_DESIG, "Chairperson"]]
        for i, row in enumerate(vals):
            for j, v in enumerate(row):
                p = sig.cell(i, j).paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_after = Pt(0)
                self.runs(p, v, 11)
        self.center("External Viva", 12, True, 2)
        ex = self.doc.add_table(rows=3, cols=2)
        for i, row in enumerate([["Name of the Examiners", "Signature with Date"],
                                 ["1. __________________________", "__________________________"],
                                 ["2. __________________________", "__________________________"]]):
            for j, v in enumerate(row):
                p = ex.cell(i, j).paragraphs[0]
                p.paragraph_format.space_after = Pt(2)
                set_font(p.add_run(v), 11, bold=i == 0)
        self.page_break()

        # --- declaration
        self.center("DECLARATION", 16, True, 12)
        self.para(f"We hereby declare that the Capstone Project Phase - 1 entitled “{TITLE}” has been carried out by us "
                  f"under the guidance of {GUIDE}, {GUIDE_DESIG}, and submitted in partial fulfillment of the course "
                  "requirements for the award of the degree of Bachelor of Technology in Computer Science and "
                  "Engineering of PES University, Bengaluru during the academic semester Aug. – Dec. 2026. The matter "
                  "embodied in this report has not been submitted to any other university or institution for the "
                  "award of any degree.")
        t = self.doc.add_table(rows=len(TEAM), cols=3)
        for i, (n, s) in enumerate(TEAM):
            for j, v in enumerate((s, n, "")):
                p = t.cell(i, j).paragraphs[0]
                p.paragraph_format.space_after = Pt(14)
                set_font(p.add_run(v), 12)
        self.page_break()

        # --- acknowledgement
        self.center("ACKNOWLEDGEMENT", 16, True, 12)
        for txt in (
            f"We would like to express our gratitude to {GUIDE}, Department of Computer Science and Engineering, PES "
            "University, for the continuous guidance, assistance and encouragement throughout the development of this "
            "UE24CS320A - Capstone Project Phase – 1.",
            "We are grateful to all Capstone Project Coordinators for organizing, managing and helping with the entire process.",
            "We take this opportunity to thank Dr. Sandesh B J, Professor & Chairperson, Department of Computer Science "
            "and Engineering, PES University, for all the knowledge and support we have received from the department.",
            "We are deeply grateful to Late Dr. M. R. Doreswamy, Founder, PES University, whose vision and dedication "
            "continue to inspire generations of learners. We would also like to express our sincere gratitude to Prof. "
            "Jawahar Doreswamy, Chancellor, PES University, Dr. Suryaprasad J, Vice-Chancellor, PES University and Prof. "
            "Nagarjuna Sadineni, Pro Vice-Chancellor, PES University for providing us various opportunities and "
            "enlightenment every step of the way. Finally, this project could not have been completed without the "
            "continual support and encouragement we have received from our families and friends."):
            self.para(txt)
        self.page_break()

        # --- abstract
        self.center("ABSTRACT", 16, True, 12)
        for ptxt in abstract:
            self.para(ptxt)
        self.page_break()

        # --- TOC and lists
        self.center("TABLE OF CONTENTS", 16, True, 12)
        p = self.doc.add_paragraph()
        add_field(p, 'TOC \\o "1-3" \\h \\z \\u', "Right-click here and choose Update Field to build the table of contents.")
        self.page_break()
        self.center("LIST OF TABLES", 16, True, 12)
        p = self.doc.add_paragraph()
        add_field(p, 'TOC \\h \\z \\t "Table Caption,1"', "Right-click here and choose Update Field to build the list of tables.")
        self.page_break()
        self.center("LIST OF FIGURES", 16, True, 12)
        p = self.doc.add_paragraph()
        add_field(p, 'TOC \\h \\z \\t "Figure Caption,1"', "Right-click here and choose Update Field to build the list of figures.")

    def logo_path(self):
        out = os.path.join(ROOT, "report", "pes_logo.jpg")
        if not os.path.exists(out) and os.path.exists(TEMPLATE_ZIP):
            with zipfile.ZipFile(TEMPLATE_ZIP) as z:
                inner = [n for n in z.namelist() if n.endswith("Page 1-2.docx")][0]
                import io
                with zipfile.ZipFile(io.BytesIO(z.read(inner))) as d:
                    open(out, "wb").write(d.read("word/media/image1.jpg"))
        return out if os.path.exists(out) else None

    # ---------------------------------------------------------------- chapters
    def chapter_heading(self, title, appendix=False):
        if appendix:
            self.chap_label = "A"
            h = self.doc.add_heading(title.upper(), level=1)
        else:
            self.chapter += 1
            self.chap_label = str(self.chapter)
            c = self.center(f"CHAPTER {self.chapter}", 18, True, 0)
            c.paragraph_format.space_before = Pt(0)
            c.paragraph_format.keep_with_next = True
            h = self.doc.add_heading(title.upper(), level=1)
        self.fig = self.tab = 0
        self.sec_n = self.sub_n = 0
        return h

    def references(self):
        self.doc.add_heading("REFERENCES", level=1)
        order = sorted(self.cites, key=self.cites.get)
        for k in order:
            p = self.doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(1.0)
            p.paragraph_format.first_line_indent = Cm(-1.0)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            set_font(p.add_run(f"[{self.cites[k]}]\t"), 12)
            self.runs(p, BIB[k], 12)

    # ---------------------------------------------------------------- markdown driver
    def build(self, md):
        md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
        abstract = re.search(r"::: abstract\n(.*?)\n:::", md, flags=re.S).group(1).strip().split("\n\n")
        md = re.sub(r"::: abstract\n.*?\n:::", "", md, flags=re.S)
        self.front_matter(abstract)

        lines = md.split("\n")
        i, first_chapter, in_appendix, pending_caption = 0, True, False, None
        num = 0
        while i < len(lines):
            ln = lines[i].rstrip()
            if ln.startswith("::: references"):
                self.body_section()
                self.references()
                i += 1
                continue
            if ln.startswith("::: appendix"):
                in_appendix = True
                i += 1
                continue
            if ln == ":::":
                i += 1
                continue
            if ln.startswith("# "):
                self.body_section(first=first_chapter)
                first_chapter = False
                self.chapter_heading(ln[2:].strip(), appendix=in_appendix)
            elif ln.startswith("## "):
                self.sec_n += 1
                self.sub_n = 0
                self.doc.add_heading(f"{self.chap_label}.{self.sec_n} {ln[3:].strip()}", level=2)
            elif ln.startswith("### "):
                self.sub_n += 1
                self.doc.add_heading(f"{self.chap_label}.{self.sec_n}.{self.sub_n} {ln[4:].strip()}", level=3)
            elif ln.startswith("Table: "):
                pending_caption = ln[7:].strip()
            elif ln.startswith("|"):
                rows = []
                while i < len(lines) and lines[i].startswith("|"):
                    cells = [c for c in lines[i].strip().strip("|").split("|")]
                    if not all(re.fullmatch(r"\s*:?-+:?\s*", c) for c in cells):
                        rows.append(cells)
                    i += 1
                self.table(pending_caption or "", rows)
                pending_caption = None
                continue
            elif ln.startswith("!["):
                m = re.match(r"!\[(.*)\]\((.+?)\)(\{w=([\d.]+)\})?", ln)
                self.figure(m.group(1), m.group(2), float(m.group(4)) if m.group(4) else 15.0)
            elif ln.startswith("- "):
                self.bullet(ln[2:])
            elif re.match(r"\d+\. ", ln):
                n, txt = ln.split(". ", 1)
                self.bullet(txt, numbered=int(n))
            elif ln.strip():
                # join soft-wrapped paragraph lines
                buf = [ln]
                while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r"(#|- |\d+\. |\||!\[|Table: |:::)", lines[i + 1]):
                    i += 1
                    buf.append(lines[i].rstrip())
                self.para(" ".join(buf))
            i += 1
        unused = set(BIB) - set(self.cites)
        if unused:
            print("note: BIB entries not cited:", sorted(unused))
        self.doc.save(OUT)
        print(f"wrote {OUT}: {self.chapter} chapters, {len(self.cites)} references")


if __name__ == "__main__":
    Report().build(open(SRC, encoding="utf8").read())
