"""Build the Phase-1 report from report.md (the source of truth) with pandoc.

ONE COMMAND (from ~/Desktop/research, conda env research2):
    python capstone/report/build_pandoc.py --pdf     # LaTeX PDF only  -> capstone/report/Team147_Phase1_Report.pdf
    python capstone/report/build_pandoc.py --docx    # Word file only  -> capstone/report/Team147_Phase1_Report.docx
    python capstone/report/build_pandoc.py           # both

PDF pipeline (LaTeX):
  1. preprocess report.md: strip comments, IEEE citations [n] in order of first use, reference list from
     build_report.BIB, placeholders -> yellow box, front-matter pages (title, certificate, declaration,
     acknowledgement, abstract, contents, list of tables, list of figures)
  2. pandoc: Markdown -> LaTeX body (report class: # = chapter, ## = section); LaTeX numbers chapters,
     sections, tables and figures itself (Table 3.1, Figure 7.2 ...); a Lua filter gives every caption a short
     form for the lists of tables and figures
  3. LuaLaTeX, three passes, with the preamble in PDF_PREAMBLE: A4, 12 pt Times New Roman (research/fonts),
     1.5 line spacing, chapter 18 pt / section 16 pt / subsection 14 pt, running header and footer from the
     Introduction on, roman page numbers in the front matter, long tables that break across pages
     Engine: lualatex or xelatex if they work; otherwise plain `luatex` with a lualatex format that this script
     builds once into _build/fmt/ (the Fedora TeX Live here has no working lualatex/xelatex binary).

DOCX pipeline: preprocess (manual numbering) -> pandoc -> python-docx department styles (finalize_docx.py).
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RESEARCH = os.path.dirname(os.path.dirname(HERE))  # ~/Desktop/research (figure paths in report.md start here)
sys.path.insert(0, HERE)
from build_report import BIB, TEAM, TITLE  # noqa: E402  (reference strings, team list, title)

SRC = os.path.join(HERE, "report.md")
BUILD = os.path.join(HERE, "_build")
DOCX = os.path.join(HERE, "Team147_Phase1_Report.docx")
FINAL_PDF = os.path.join(HERE, "Team147_Phase1_Report.pdf")
LOGO = os.path.join(HERE, "pes_logo.jpg")
FONTDIR = os.path.join(RESEARCH, "fonts")
GUIDE = "Dr. Chandrashekhar P Chavan"
FIG_SCALE = 0.85  # figures in report.md are sized in cm for a wider page
PLACEHOLDER = '[Designation to be filled]{custom-style="Placeholder"}'
MD_FORMATS = "markdown+fenced_divs+bracketed_spans+pipe_tables+raw_attribute+implicit_figures"
PB_DOCX = "```{=openxml}\n<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>\n```"
PB_TEX = "```{=latex}\n\\newpage\n```"


TEX = False  # set by build_markdown(): True when writing the LaTeX (PDF) source
TEX_WRAP = {"Center": ("\\begin{center}", "\\end{center}"),
            "Center Big": ("\\begin{center}\\LARGE", "\\end{center}"),
            "Front Title": ("\\begin{center}\\Large\\bfseries", "\\end{center}")}


def raw_tex(s):
    return "```{=latex}\n" + s + "\n```"


def div(style, text):
    if TEX:
        if style in TEX_WRAP:
            a, b = TEX_WRAP[style]
            return raw_tex(a) + "\n\n" + text + "\n\n" + raw_tex(b)
        return text
    return '::: {custom-style="%s"}\n%s\n:::' % (style, text)


def ref_text(key):
    """BIB entry as Markdown (<i> -> *...*)."""
    return re.sub(r"<i>(.*?)</i>", r"*\1*", BIB[key])


def tex_escape(s):
    return re.sub(r"([&%#_$])", r"\\\1", s)


def ref_tex(key):
    """BIB entry as LaTeX (<i> -> \\textit, URLs -> \\url, special characters escaped)."""
    parts = re.split(r"(https?://\S+?)(?=,|\s|$)", BIB[key])
    out = "".join("\\url{%s}" % p if p.startswith("http") else tex_escape(p) for p in parts)
    out = re.sub(r'"(.*?)"', "“\\1”", out)  # straight quotes would all print as closing quotes
    return re.sub(r"<i>(.*?)</i>", r"\\textit{\1}", out)


def team_lines():
    return "\n\n".join(f"{n} ({s})" for n, s in TEAM)


def front_matter(abstract_paras, pb, tex):
    """Title page, certificate, declaration, acknowledgement, abstract, then the table-of-contents pages."""
    team = team_lines()
    decl_team = "\n\n".join(f"{n} — {s}" for n, s in TEAM)
    sig = ("| Guide | Chairperson |\n|---|---|\n"
           f"|  |  |\n| {GUIDE} | Dr. Sandesh B J |\n| {PLACEHOLDER} | Professor & Chairperson |")
    viva = ("| Name of the Examiners | Signature with Date |\n|---|---|\n"
            "| 1. \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_ | \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_ |\n"
            "| 2. \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_ | \\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_ |")
    institute = ("**DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING**\n\n**FACULTY OF ENGINEERING**\n\n"
                 "**PES UNIVERSITY**\n\n(Established under Karnataka Act No. 16 of 2013)\n\n"
                 "Electronic City, Hosur Road, Bengaluru – 560 100, Karnataka, India")
    cert_head = ("**PES UNIVERSITY**\n\n(Established under Karnataka Act No. 16 of 2013)\n\n"
                 "Electronic City, Hosur Road, Bengaluru – 560 100, Karnataka, India\n\n**FACULTY OF ENGINEERING**")
    ack = [
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
        "continual support and encouragement we have received from our families and friends.",
    ]
    declaration = (f"We hereby declare that the Capstone Project Phase - 1 entitled “{TITLE}” has been carried out by us "
                   f"under the guidance of {GUIDE}, {PLACEHOLDER}, and submitted in partial fulfillment of the course "
                   "requirements for the award of the degree of Bachelor of Technology in Computer Science and "
                   "Engineering of PES University, Bengaluru during the academic semester Aug. – Dec. 2026. The matter "
                   "embodied in this report has not been submitted to any other university or institution for the "
                   "award of any degree.")
    certificate = (f"This is to certify that the dissertation entitled\n\n**‘{TITLE}’**\n\nis a bonafide work carried out by")
    certified = ("In partial fulfillment for the completion of Fifth-semester Capstone Project Phase - 1 (UE24CS320A) in "
                 "the Program of Study - Bachelor of Technology in Computer Science and Engineering under rules and "
                 "regulations of PES University, Bengaluru during the period Aug – Dec. 2026. It is certified that all "
                 "corrections/suggestions indicated for internal assessment have been incorporated in the report. The "
                 "dissertation has been approved as it satisfies the 5th-semester academic requirements in respect of "
                 "project work.")
    abstract = "\n\n".join(div("Body Text", p) for p in abstract_paras)
    # LaTeX: \tableofcontents etc. start their own pages with their own headings
    contents_pages = ["@@TOC@@\n\n@@LOT@@\n\n@@LOF@@"] if not tex else []
    if not tex:
        contents_pages = [pb, div("Front Title", "TABLE OF CONTENTS")] + contents_pages
    else:
        contents_pages = [raw_tex("\\begingroup\\setstretch{1.2}\\tableofcontents\\listoftables\\listoffigures"
                                  "\\endgroup")]
    single_on = [raw_tex("\\begin{singlespace}\\thispagestyle{empty}")] if tex else []
    single_off = [raw_tex("\\end{singlespace}")] if tex else []
    blocks = single_on + [
        div("Center Big", "Dissertation on"),
        div("Front Title", f"“{TITLE}”"),
        div("Center", "Submitted in partial fulfillment of the requirements for\n\n**Bachelor of Technology**\n\nin\n\n"
                      "**Computer Science & Engineering**\n\n**UE24CS320A – Capstone Project Phase - 1**"),
        div("Center", "Submitted by:\n\n" + team),
        div("Center", f"Under the guidance of\n\n**{GUIDE}**\n\n{PLACEHOLDER}\n\nPES University\n\nAug - Dec 2026"),
        f"![]({LOGO}){{width=4.5cm}}",
        div("Center", institute),
        pb,
        div("Center", cert_head),
        f"![]({LOGO}){{width=3cm}}",
        div("Front Title", "CERTIFICATE"),
        div("Center", certificate + "\n\n" + team),
        div("Body Text", certified),
        sig,
        div("Center", "**External Viva**"),
        viva,
    ] + single_off + [
        pb,
        div("Front Title", "DECLARATION"),
        div("Body Text", declaration),
        div("Center", decl_team),
        pb,
        div("Front Title", "ACKNOWLEDGEMENT"),
        "\n\n".join(div("Body Text", a) for a in ack),
        pb,
        div("Front Title", "ABSTRACT"),
        abstract,
    ] + contents_pages
    return "\n\n".join(blocks) + "\n\n"


def number_body(body):
    """Docx: number chapters (H1), sections (H2), tables and figures per chapter by hand.
    LaTeX: leave numbering to LaTeX (\\chapter, \\caption), only add page-style commands.
    Both: IEEE citations [n], placeholders, reference list."""
    out, ch, sec, tab, fig, appendix = [], 0, 0, 0, 0, False
    app_n = 0  # appendix count: \\appendix is emitted once, letters A, B, ... follow
    for ln in body.split("\n"):
        if ln.strip() == "::: appendix":
            appendix = True
            tab = 0  # appendix tables are A.1, A.2 ...
            continue
        if ln.strip() in (":::", "::::"):
            continue
        if ln.startswith("# "):
            title = ln[2:].strip()
            if appendix or title.startswith("Appendix"):
                app_n += 1
                tab = 0
                if TEX:
                    if app_n == 1:
                        out.append(raw_tex("\\appendix"))
                    out.append("# " + re.sub(r"^Appendix [A-Z]:\s*", "", title))
                else:
                    out.append("# " + title)
            else:
                if TEX and ch == 0:  # first chapter: arabic page numbers from 1, running header and footer
                    out.append(raw_tex("\\clearpage\\pagenumbering{arabic}\\pagestyle{main}\\mainplain"))
                ch += 1
                sec = tab = fig = 0
                out.append("# " + title if TEX else f"# {ch} {title}")
            continue
        if ln.startswith("## "):
            sec += 1
            out.append("## " + ln[3:].strip() if TEX else f"## {ch}.{sec} {ln[3:].strip()}")
            continue
        m = re.match(r"^Table: (.*)$", ln)
        if m:
            tab += 1
            label = f"{chr(64 + app_n)}.{tab}" if appendix else f"{ch}.{tab}"
            out.append(f"Table: {m.group(1)}" if TEX else f"Table: **Table {label}.** {m.group(1)}")
            out.append("")  # pandoc needs a blank line between a caption and its table
            continue
        m = re.match(r"^!\[(.*?)\]\((.+?)\)(\{w=([\d.]+)\})?\s*$", ln)
        if m:
            fig += 1
            width = float(m.group(4) or 15) * FIG_SCALE
            cap = m.group(1) if TEX else f"**Figure {ch}.{fig}.** {m.group(1)}"
            out.append(f"![{cap}]({m.group(2)}){{width={width:.1f}cm}}")
            continue
        out.append(ln)
    text = "\n".join(out)
    text = re.sub(r"⟦([^⟧]*)⟧", lambda m: "[" + m.group(1) + ']{custom-style="Placeholder"}', text)

    cites = []

    def cite(m):
        nums = []
        for key in re.findall(r"@(\w+)", m.group(0)):
            if key not in BIB:
                raise SystemExit(f"citation key not in BIB: {key}")
            if key not in cites:
                cites.append(key)
            nums.append(str(cites.index(key) + 1))
        return "\\[" + ", ".join(nums) + "\\]"

    text = re.sub(r"\[(@\w+(?:;\s*@\w+)*)\]", cite, text)
    if TEX:  # IEEE-style numbered list, hanging labels
        items = "\n".join(f"\\bibitem{{{k}}} {ref_tex(k)}" for k in cites)
        refs = [raw_tex("\\begin{thebibliography}{99}\\addcontentsline{toc}{chapter}{References}\n"
                        + items + "\n\\end{thebibliography}")]
    else:
        refs = ["", "# References"]
        for i, key in enumerate(cites, 1):
            refs.append(div("Reference", f"\\[{i}\\] {ref_text(key)}"))
    unused = sorted(set(BIB) - set(cites))
    if unused:
        print("note: BIB entries not cited:", unused)
    text = text.replace("@@REFERENCES@@", "\n\n".join(refs))
    return text, cites


def build_markdown(tex):
    global TEX
    TEX = tex
    src = re.sub(r"<!--.*?-->", "", open(SRC, encoding="utf8").read(), flags=re.S)
    m = re.search(r"::: abstract\n(.*?)\n:::", src, re.S)
    abstract = [p.strip() for p in m.group(1).split("\n\n") if p.strip()]
    src = src.replace(m.group(0), "")
    src = src.replace("::: references\n:::", "@@REFERENCES@@")
    body, cites = number_body(src[src.index("\n# ") + 1:])
    front = front_matter(abstract, PB_TEX if tex else PB_DOCX, tex)
    if not tex:
        front += "@@BODY@@\n\n"  # becomes the section break in finalize()
    md = front + body
    if tex:  # highlighted placeholders -> yellow box in LaTeX
        md = re.sub(r'\[([^\]]*)\]\{custom-style="Placeholder"\}', lambda m: "\\colorbox{yellow}{" + m.group(1) + "}", md)
    return md, cites


# --------------------------------------------------------------------------------------------- LaTeX / PDF

PDF_PREAMBLE = r"""\documentclass[12pt,a4paper,oneside]{report}
\usepackage[a4paper,margin=2cm,headheight=15pt,includehead,includefoot]{geometry}
\usepackage{fontspec}
\setmainfont{times}[Path=@FONTDIR@/,Extension=.ttf,UprightFont=times,BoldFont=timesbd,ItalicFont=timesi,BoldItalicFont=timesbi]
\setmonofont{consola}[Path=@FONTDIR@/,Extension=.ttf,UprightFont=consola,BoldFont=consolab,ItalicFont=consolai,BoldItalicFont=consolaz,Scale=0.88]
\usepackage{amsmath,amssymb}
\usepackage{setspace}
\onehalfspacing
\usepackage{xcolor}
\usepackage{graphicx}
\graphicspath{{@RESEARCH@/}}
\usepackage{longtable,booktabs,array,calc}
\usepackage{fancyvrb}
\usepackage{etoolbox}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage[font={small,stretch=1.1},labelfont=bf,labelsep=period,skip=6pt]{caption}
\usepackage{url}
\usepackage[hidelinks,bookmarksnumbered]{hyperref}
% paragraphs: no indent, space between (department Word format)
\setlength{\parindent}{0pt}
\setlength{\parskip}{6pt plus 2pt minus 1pt}
\clubpenalty=10000 \widowpenalty=10000 \displaywidowpenalty=10000
\emergencystretch=2em
% headings: chapter 18 pt centred, section 16 pt, subsection 14 pt
\titleformat{\chapter}[display]{\centering\bfseries\fontsize{18}{22}\selectfont}{\MakeUppercase{\chaptertitlename}\ \thechapter}{6pt}{}
\titleformat{name=\chapter,numberless}[display]{\centering\bfseries\fontsize{18}{22}\selectfont}{}{0pt}{}
\titlespacing*{\chapter}{0pt}{-24pt}{14pt}
\titleformat{\section}{\bfseries\fontsize{16}{19}\selectfont\raggedright}{\thesection}{0.6em}{}
\titleformat{\subsection}{\bfseries\fontsize{14}{17}\selectfont\raggedright}{\thesubsection}{0.6em}{}
\titlespacing*{\section}{0pt}{14pt}{4pt}
\titlespacing*{\subsection}{0pt}{10pt}{2pt}
\setcounter{secnumdepth}{2}
\setcounter{tocdepth}{1}
\renewcommand{\contentsname}{Table of Contents}
\renewcommand{\bibname}{References}
% page styles: front matter = roman number only; from the Introduction on = running header + department footer
\newcommand{\deptfooter}{\small Dept. of Computer Science \& Engineering \textperiodcentered\ PES University \textperiodcentered\ Aug – Dec 2026 \textperiodcentered\ \thepage}
\fancypagestyle{plain}{\fancyhf{}\fancyfoot[C]{\small\thepage}\renewcommand{\headrulewidth}{0pt}}
\fancypagestyle{main}{%
  \fancyhf{}%
  \fancyhead[R]{\small\itshape Learning What to Ignore \textperiodcentered\ Team 147 \textperiodcentered\ UE24CS320A Capstone Project Phase - 1}%
  \fancyfoot[C]{\deptfooter}%
  \renewcommand{\headrulewidth}{0.4pt}}
\newcommand{\mainplain}{\fancypagestyle{plain}{\fancyhf{}\fancyfoot[C]{\deptfooter}\renewcommand{\headrulewidth}{0pt}}}
% tables: smaller, single-spaced, full width, break across pages with the header repeated
\AtBeginEnvironment{longtable}{\small\setstretch{1.05}}
\setlength{\LTpre}{8pt}\setlength{\LTpost}{8pt}
\renewcommand{\arraystretch}{1.15}
\setlength{\tabcolsep}{4pt}
% figures: keep near the text
\renewcommand{\topfraction}{0.85}\renewcommand{\textfraction}{0.1}\renewcommand{\floatpagefraction}{0.75}
\setcounter{topnumber}{2}\setcounter{totalnumber}{3}
% pandoc helpers
\providecommand{\tightlist}{\setlength{\itemsep}{2pt}\setlength{\parskip}{0pt}}
\providecommand{\pandocbounded}[1]{#1}
\newcounter{none} % pandoc: unnumbered (front-matter) tables
\makeatletter\patchcmd\longtable{\par}{\if@noskipsec\mbox{}\fi\par}{}{}\makeatother
\makeatletter\def\fps@figure{htbp}\makeatother
\begin{document}
\pagenumbering{roman}
\pagestyle{plain}
\input{report_body.tex}
\end{document}
"""

LUA_FILTER = r"""
-- short captions for the lists of tables and figures: the first sentence without parentheses
local function short(long)
  local s = pandoc.utils.stringify(long)
  s = s:gsub("%s*%b()", "")
  s = s:match("^(.-%.)%s") or s
  return pandoc.Inlines(s)
end
function Figure(f)
  if #f.caption.long > 0 then f.caption.short = short(f.caption.long) end
  return f
end
function Table(t)
  if #t.caption.long > 0 then t.caption.short = short(t.caption.long) end
  return t
end
"""


def tex_command():
    """Return the command that runs LuaLaTeX/XeLaTeX on a file name."""
    for exe in ("lualatex", "xelatex"):
        path = shutil.which(exe)
        if path and subprocess.run([path, "--version"], capture_output=True).returncode == 0:
            return [path]
    luatex = shutil.which("luatex")
    if not luatex:
        raise SystemExit("no LuaLaTeX, XeLaTeX or luatex found: install a TeX engine")
    fmt_dir = os.path.join(BUILD, "fmt")
    if not os.path.exists(os.path.join(fmt_dir, "lualatex.fmt")):
        print("building a lualatex format for luatex (once) ...")
        os.makedirs(fmt_dir, exist_ok=True)
        r = subprocess.run([luatex, "-ini", "-jobname=lualatex", "-progname=lualatex", "*lualatex.ini"],
                           cwd=fmt_dir, capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(os.path.join(fmt_dir, "lualatex.fmt")):
            raise SystemExit("could not build the lualatex format; see " + fmt_dir)
    return [luatex, "--fmt=" + os.path.join(fmt_dir, "lualatex"), "--progname=lualatex"]


def build_pdf():
    md, cites = build_markdown(tex=True)
    md_path = os.path.join(BUILD, "report_tex.md")
    open(md_path, "w", encoding="utf8").write(md)
    lua = os.path.join(BUILD, "short_captions.lua")
    open(lua, "w", encoding="utf8").write(LUA_FILTER)
    body = os.path.join(BUILD, "report_body.tex")
    subprocess.run(["pandoc", md_path, "-f", MD_FORMATS, "-t", "latex", "--top-level-division=chapter",
                    "--syntax-highlighting=none", "--lua-filter", lua, "-o", body], check=True)
    tex = open(body, encoding="utf8").read()
    # code listings: framed, small, single-spaced
    tex = re.sub(r"\\begin\{verbatim\}(.*?)\\end\{verbatim\}",
                 lambda m: "\\begin{singlespace}\\begin{Verbatim}[fontsize=\\small,frame=single,framesep=6pt]"
                           + m.group(1) + "\\end{Verbatim}\n\\end{singlespace}", tex, flags=re.S)

    def keep_short(m):
        """\\\\* forbids a page break after a row: tables of up to 4 body rows never split, and longer ones
        never leave a single row alone at the top or bottom of a page."""
        t = m.group(0)
        head, sep, rows = t.partition("\\endlastfoot\n")
        if not sep:
            return t
        n = rows.count("\\\\\n")
        if n <= 5:
            return head + sep + rows.replace("\\\\\n", "\\\\*\n")
        parts = rows.split("\\\\\n")  # n+1 parts; protect the breaks after row 1 and before the last row
        for i in (0, n - 2):
            parts[i] += "\\\\*"
        return head + sep + "\n".join(p if p.endswith("\\\\*") else p + "\\\\" for p in parts[:-1]) + "\n" + parts[-1]

    tex = re.sub(r"\\begin\{longtable\}.*?\\end\{longtable\}", keep_short, tex, flags=re.S)
    open(body, "w", encoding="utf8").write(tex)
    main_tex = os.path.join(BUILD, "Team147_Phase1_Report.tex")
    pre = PDF_PREAMBLE.replace("@FONTDIR@", FONTDIR).replace("@RESEARCH@", RESEARCH)
    open(main_tex, "w", encoding="utf8").write(pre)
    cmd = tex_command() + ["-interaction=nonstopmode", "-halt-on-error", "Team147_Phase1_Report.tex"]
    for i in range(3):  # TOC, lists, longtable column widths
        r = subprocess.run(cmd, cwd=BUILD, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-3000:])
            raise SystemExit("LaTeX failed; log: " + os.path.join(BUILD, "Team147_Phase1_Report.log"))
    shutil.copy(os.path.join(BUILD, "Team147_Phase1_Report.pdf"), FINAL_PDF)
    log = open(os.path.join(BUILD, "Team147_Phase1_Report.log"), encoding="utf8", errors="replace").read()
    over = re.findall(r"Overfull \\hbox \((\d+\.\d+)pt", log)
    big = [o for o in over if float(o) > 2]
    missing = sorted(set(re.findall(r"Missing character: There is no (.) ", log)))
    info = subprocess.run(["pdfinfo", FINAL_PDF], capture_output=True, text=True).stdout
    pages = re.search(r"Pages:\s+(\d+)", info).group(1)
    print(f"wrote {FINAL_PDF} ({pages} pages, {len(cites)} references; "
          f"overfull boxes > 2pt: {len(big)}; missing glyphs: {''.join(missing) or 'none'})")


def build_docx():
    from finalize_docx import finalize  # noqa: E402  (python-docx pass, separate file for readability)

    md, cites = build_markdown(tex=False)
    md_path = os.path.join(BUILD, "report_docx.md")
    open(md_path, "w", encoding="utf8").write(md)
    raw = os.path.join(BUILD, "raw.docx")
    subprocess.run(["pandoc", md_path, "-f", MD_FORMATS, "-t", "docx", "--resource-path", RESEARCH, "-o", raw],
                   check=True)
    finalize(raw, DOCX)
    print(f"wrote {DOCX} ({len(cites)} references)")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pdf", action="store_true", help="build only the LaTeX PDF")
    ap.add_argument("--docx", action="store_true", help="build only the .docx")
    ap.add_argument("--src", default="report.md", help="Markdown source in capstone/report/ (default report.md)")
    ap.add_argument("--name", default="Team147_Phase1_Report", help="output file name without extension")
    a = ap.parse_args()
    global SRC, DOCX, FINAL_PDF
    SRC = os.path.join(HERE, a.src)
    DOCX = os.path.join(HERE, a.name + ".docx")
    FINAL_PDF = os.path.join(HERE, a.name + ".pdf")
    os.makedirs(BUILD, exist_ok=True)
    if a.docx or not a.pdf:
        build_docx()
    if a.pdf or not a.docx:
        build_pdf()


if __name__ == "__main__":
    main()
