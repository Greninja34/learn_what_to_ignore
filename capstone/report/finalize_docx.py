"""python-docx pass on pandoc's output: the PES department format (see build_pandoc.py for the pipeline).

- A4, 2 cm margins; Times New Roman; body 12 pt, justified, 1.5 spacing
- chapter titles (Heading 1): 18 pt, bold, centred, new page; sections 16 pt bold; subsections 14 pt bold; left
- front matter (title page .. list pages) is its own section with no header or footer
- from the Introduction on: running header (project title) and footer (department, term, page number), numbering from 1
- TOC, list of tables and list of figures are Word fields (press F9 / Update field if they look empty)
"""
import copy

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from docx.text.paragraph import Paragraph

FONT = "Times New Roman"
TITLE_SHORT = "Learning What to Ignore · Team 147 · UE24CS320A Capstone Project Phase - 1"
FOOTER_TEXT = "Dept. of Computer Science & Engineering · PES University · Aug – Dec 2026 · "
BLACK = RGBColor(0, 0, 0)


def _style(doc, name, kind=WD_STYLE_TYPE.PARAGRAPH):
    try:
        return doc.styles[name]
    except KeyError:
        return doc.styles.add_style(name, kind)


def _font(st, size, bold=None, italic=None):
    st.font.name = FONT
    st.font.size = Pt(size)
    st.font.color.rgb = BLACK
    if bold is not None:
        st.font.bold = bold
    if italic is not None:
        st.font.italic = italic
    rpr = st.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), FONT)
    for attr in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rfonts.get(qn(attr)) is not None:
            del rfonts.attrib[qn(attr)]


def _para(st, align=None, spacing=None, before=None, after=None, keep_next=None, page_break=None,
          left=None, first=None):
    pf = st.paragraph_format
    if align is not None:
        pf.alignment = align
    if spacing is not None:
        pf.line_spacing = spacing
    if before is not None:
        pf.space_before = Pt(before)
    if after is not None:
        pf.space_after = Pt(after)
    if keep_next is not None:
        pf.keep_with_next = keep_next
    if page_break is not None:
        pf.page_break_before = page_break
    if left is not None:
        pf.left_indent = Cm(left)
    if first is not None:
        pf.first_line_indent = Cm(first)


def style_document(doc):
    J, C, L = WD_ALIGN_PARAGRAPH.JUSTIFY, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT
    for name in ("Normal", "Body Text", "First Paragraph"):
        st = _style(doc, name)
        _font(st, 12)
        _para(st, align=J, spacing=1.5, before=0, after=6)
    _font(_style(doc, "Compact"), 10.5)
    _para(_style(doc, "Compact"), align=L, spacing=1.0, before=0, after=0)

    h1 = _style(doc, "Heading 1")
    _font(h1, 18, bold=True)
    _para(h1, align=C, spacing=1.0, before=0, after=14, keep_next=True, page_break=True)
    h2 = _style(doc, "Heading 2")
    _font(h2, 16, bold=True)
    _para(h2, align=L, spacing=1.15, before=12, after=6, keep_next=True, page_break=False)
    h3 = _style(doc, "Heading 3")
    _font(h3, 14, bold=True)
    _para(h3, align=L, spacing=1.15, before=10, after=4, keep_next=True, page_break=False)

    _font(_style(doc, "Front Title"), 16, bold=True)
    _para(_style(doc, "Front Title"), align=C, spacing=1.15, before=0, after=14, keep_next=True)
    _font(_style(doc, "Center"), 12)
    _para(_style(doc, "Center"), align=C, spacing=1.15, before=0, after=6)
    _font(_style(doc, "Center Big"), 14)
    _para(_style(doc, "Center Big"), align=C, spacing=1.15, before=0, after=6)
    _font(_style(doc, "Reference"), 11)
    _para(_style(doc, "Reference"), align=L, spacing=1.0, before=0, after=4, left=0.8, first=-0.8)

    for name in ("Image Caption", "Table Caption"):
        st = _style(doc, name)
        _font(st, 11, italic=False)
        _para(st, align=C, spacing=1.0, before=4, after=10)
    _para(_style(doc, "Captioned Figure"), align=C, spacing=1.0, before=8, after=0, keep_next=True)

    ph = _style(doc, "Placeholder", WD_STYLE_TYPE.CHARACTER)
    ph.font.highlight_color = WD_COLOR_INDEX.YELLOW
    _style(doc, "Hyperlink", WD_STYLE_TYPE.CHARACTER)
    doc.core_properties.title = "Learning What to Ignore: Deriving Invariance for Self-Supervised Text Recognition"
    doc.core_properties.author = "Team 147"


def _borders(tbl):
    tblpr = tbl._tbl.tblPr
    old = tblpr.find(qn("w:tblBorders"))
    if old is not None:
        tblpr.remove(old)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "808080")
        borders.append(el)
    tblpr.append(borders)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER


def _field_runs(p_el, instr, placeholder):
    def add(child):
        r = OxmlElement("w:r")
        r.append(child)
        p_el.append(r)

    fc = OxmlElement("w:fldChar")
    fc.set(qn("w:fldCharType"), "begin")
    add(fc)
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = f" {instr} "
    add(it)
    fc = OxmlElement("w:fldChar")
    fc.set(qn("w:fldCharType"), "separate")
    add(fc)
    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = placeholder
    add(t)
    fc = OxmlElement("w:fldChar")
    fc.set(qn("w:fldCharType"), "end")
    add(fc)


def _replace_with_field(doc, marker, instr, placeholder):
    for p in doc.paragraphs:
        if p.text.strip() == marker:
            new = OxmlElement("w:p")
            p._p.addprevious(new)
            _field_runs(new, instr, placeholder)
            p._p.getparent().remove(p._p)
            return
    raise SystemExit(f"marker not found: {marker}")


def _page_field(p):
    r = OxmlElement("w:r")
    fc = OxmlElement("w:fldChar")
    fc.set(qn("w:fldCharType"), "begin")
    r.append(fc)
    p._p.append(r)
    r = OxmlElement("w:r")
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = " PAGE "
    r.append(it)
    p._p.append(r)
    r = OxmlElement("w:r")
    fc = OxmlElement("w:fldChar")
    fc.set(qn("w:fldCharType"), "separate")
    r.append(fc)
    p._p.append(r)
    r = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "1"
    r.append(t)
    p._p.append(r)
    r = OxmlElement("w:r")
    fc = OxmlElement("w:fldChar")
    fc.set(qn("w:fldCharType"), "end")
    r.append(fc)
    p._p.append(r)


def _set_page(sectpr):
    pg = sectpr.find(qn("w:pgSz"))
    if pg is None:
        pg = OxmlElement("w:pgSz")
        sectpr.insert(0, pg)
    pg.set(qn("w:w"), str(int(21 / 2.54 * 1440)))
    pg.set(qn("w:h"), str(int(29.7 / 2.54 * 1440)))
    pg.attrib.pop(qn("w:orient"), None)
    mar = sectpr.find(qn("w:pgMar"))
    if mar is None:
        mar = OxmlElement("w:pgMar")
        pg.addnext(mar)
    for k, v in {"top": 1134, "bottom": 1134, "left": 1134, "right": 1134, "header": 567, "footer": 567,
                 "gutter": 0}.items():
        mar.set(qn(f"w:{k}"), str(v))


def split_sections(doc):
    """@@BODY@@ becomes the end of the front-matter section; the Introduction starts the body section."""
    marker = None
    for p in doc.paragraphs:
        if p.text.strip() == "@@BODY@@":
            marker = p
            break
    if marker is None:
        raise SystemExit("@@BODY@@ marker missing")
    body_sect = doc.element.body.sectPr  # pandoc's final section properties
    front = copy.deepcopy(body_sect)
    for tag in ("w:headerReference", "w:footerReference", "w:titlePg"):
        for el in front.findall(qn(tag)):
            front.remove(el)
    _set_page(front)
    new = OxmlElement("w:p")
    ppr = OxmlElement("w:pPr")
    ppr.append(front)
    new.append(ppr)
    marker._p.addprevious(new)
    marker._p.getparent().remove(marker._p)
    _set_page(body_sect)
    # every chapter (and References, Appendix) starts its own section, so its first page can have no header
    heads = [p for p in doc.paragraphs if p.style.name == "Heading 1"]
    for h in heads[1:]:
        brk = OxmlElement("w:p")
        ppr2 = OxmlElement("w:pPr")
        ppr2.append(copy.deepcopy(body_sect))
        brk.append(ppr2)
        h._p.addprevious(brk)
    pgnum = body_sect.find(qn("w:pgNumType"))
    if pgnum is None:
        pgnum = OxmlElement("w:pgNumType")
        body_sect.append(pgnum)
    pgnum.set(qn("w:start"), "1")


def header_footer(doc):
    secs = doc.sections
    sec = secs[1]  # the Introduction's section; the other body sections inherit from it
    for s_ in secs[1:]:
        s_.different_first_page_header_footer = True  # first page of a chapter: footer only
    sec.first_page_header.is_linked_to_previous = False  # left empty
    fpf = sec.first_page_footer
    fpf.is_linked_to_previous = False
    fpf.paragraphs[0].text = FOOTER_TEXT
    fpf.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in fpf.paragraphs[0].runs:
        r.font.size = Pt(9)
        r.font.name = FONT
    _page_field(fpf.paragraphs[0])
    sec.header.is_linked_to_previous = False
    sec.footer.is_linked_to_previous = False
    hp = sec.header.paragraphs[0]
    hp.text = TITLE_SHORT
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for r in hp.runs:
        r.font.size = Pt(9)
        r.font.name = FONT
        r.font.italic = True
    ppr = hp._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    for k, v in (("w:val", "single"), ("w:sz", "4"), ("w:space", "1"), ("w:color", "808080")):
        bottom.set(qn(k), v)
    bdr.append(bottom)
    ppr.append(bdr)
    sec.different_first_page_header_footer = True
    fp = sec.footer.paragraphs[0]
    fp.text = FOOTER_TEXT
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in fp.runs:
        r.font.size = Pt(9)
        r.font.name = FONT
    _page_field(fp)


def finalize(raw, out):
    doc = Document(raw)
    style_document(doc)
    for tbl in doc.tables:
        _borders(tbl)
    split_sections(doc)
    _replace_with_field(doc, "@@TOC@@", 'TOC \\o "1-2" \\h \\z \\u', "Right-click and choose Update Field to build the table of contents.")
    _replace_with_field(doc, "@@LOT@@", 'TOC \\h \\z \\t "Table Caption,1"', "Update field to build the list of tables.")
    _replace_with_field(doc, "@@LOF@@", 'TOC \\h \\z \\t "Image Caption,1"', "Update field to build the list of figures.")
    header_footer(doc)
    settings = doc.settings.element
    upd = OxmlElement("w:updateFields")
    upd.set(qn("w:val"), "true")
    settings.append(upd)  # Word asks to refresh the fields when the file opens
    doc.save(out)
