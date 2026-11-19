"""Weekly status reports (UE24CS320A Capstone Phase I) from reports.md.

Writes one filled copy of the department template per week to docx/ and one combined,
print-ready PDF (an HTML replica of the template, printed with headless Chrome).

    conda activate research2
    python make_reports.py
"""
import copy
import datetime as dt
import html
import pathlib
import subprocess

import docx
from docx.enum.text import WD_COLOR_INDEX
from docx.shared import Inches, Pt

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE.parent / 'format' / '5thsem_Weekly Report.docx'
SIGNATURE = HERE / 'guide_signature.png'
LOGO = HERE / 'pes_logo.jpg'
CHROME = '/usr/bin/google-chrome'
PDF = HERE / '147_Phase1_Weekly_Reports_Aug-Oct_2026.pdf'

SECTIONS = {'Activities Completed': 'completed', 'In Progress': 'progress', 'Plan for Next Week': 'next'}


def load(path):
    """Parse reports.md: header fields, a Members table, then '## Week n: start to end' blocks."""
    data = {'members': [], 'weeks': []}
    week = rows = None
    for line in path.read_text().splitlines():
        line = line.strip()
        for key, field in [('Project Title:', 'title'), ('Batch No:', 'batch'), ('Guide:', 'guide')]:
            if line.startswith(key):
                data[field] = line[len(key):].strip()
        if line == '## Members':
            rows = data['members']
        elif line.startswith('## Week'):
            start, end = line.split(':', 1)[1].split(' to ')
            week = {'start': start.strip(), 'end': end.strip(), 'completed': [], 'progress': [], 'next': []}
            data['weeks'].append(week)
        elif line.startswith('### ') and week is not None:
            rows = week[SECTIONS[line[4:].strip()]]
        elif line.startswith('|') and rows is not None:
            cells = [c.strip() for c in line.strip('|').split('|')]
            if set(cells[0]) <= set('-') or cells[0] in ('#', 'Name'):
                continue   # header or separator row
            if rows is data['members']:
                rows.append({'name': cells[0], 'srn': cells[1]})
            else:
                rows.append(cells[1:4])
    return data


data = load(HERE / 'reports.md')


def day(s):
    return dt.date.fromisoformat(s).strftime('%d.%m.%Y')


def is_placeholder(text):
    return '___' in text


# ---------- docx ----------

def put(cell, lines, size=11, bold=False):
    """Replace a cell's text with one paragraph per line, Cambria like the template."""
    if isinstance(lines, str):
        lines = [lines]
    paras = cell.paragraphs
    for p in paras[1:]:
        p._element.getparent().remove(p._element)
    first = paras[0]
    for r in list(first.runs):
        r._element.getparent().remove(r._element)
    for i, line in enumerate(lines):
        p = first if i == 0 else cell.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(line)
        run.font.name = 'Cambria'
        run.font.size = Pt(size)
        run.bold = bold
        if is_placeholder(line):
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW


def fill_rows(table, rows, first_row, task_col):
    for i, (task, date, remark) in enumerate(rows[:2]):
        cells = table.rows[first_row + i].cells
        put(cells[task_col], task)
        put(cells[4], date, size=10)   # dd.mm.yyyy only just fits the narrow Date column
        put(cells[5], remark)


def make_docx(week, n):
    d = docx.Document(TEMPLATE)
    t = d.tables[0]
    put(t.rows[0].cells[3], data['title'], bold=True)
    put(t.rows[1].cells[3], data['batch'])
    put(t.rows[2].cells[3], day(week['start']))
    put(t.rows[2].cells[6], day(week['end']))
    put(t.rows[3].cells[3], [m['name'] for m in data['members']])
    put(t.rows[3].cells[6], [m['srn'] for m in data['members']])
    fill_rows(t, week['completed'], 6, 2)
    fill_rows(t, week['progress'], 10, 1)
    fill_rows(t, week['next'], 14, 2)
    sig = d.tables[1].rows[0].cells
    put(sig[1], '')
    sig[1].paragraphs[0].add_run().add_picture(str(SIGNATURE), width=Inches(1.9))
    put(sig[2], data['guide'])
    out = HERE / 'docx' / f"Week{n:02d}_{week['start']}_to_{week['end']}.docx"
    out.parent.mkdir(exist_ok=True)
    d.save(out)
    return out


# ---------- pdf (HTML replica of the template) ----------

def esc(s):
    s = html.escape(s)
    return f'<mark>{s}</mark>' if is_placeholder(s) else s


def section(name, rows):
    body = ''.join(
        f'<tr class="item"><td class="c">{i}</td><td>{esc(t)}</td><td class="c">{esc(d)}</td><td>{esc(r)}</td></tr>'
        for i, (t, d, r) in enumerate(rows[:2], 1))
    return (f'<tr><th colspan="4" class="sec">{name}</th></tr>'
            '<tr class="hd"><th>#</th><th>Tasks</th><th>Date</th><th>Remarks</th></tr>' + body)


def page(week):
    names = '<br>'.join(esc(m['name']) for m in data['members'])
    srns = '<br>'.join(esc(m['srn']) for m in data['members'])
    return f'''
<div class="page">
  <header><img src="{LOGO.name}"><span>UE24CS320A–– Capstone Project Phase – I - Weekly Status Report</span></header>
  <table class="top">
    <colgroup><col style="width:1.71in"><col style="width:1.82in"><col style="width:1.52in"><col style="width:1.63in"></colgroup>
    <tr><th>Project Title</th><td colspan="3"><b>{esc(data['title'])}</b></td></tr>
    <tr><th>Batch No</th><td colspan="3">{esc(data['batch'])}</td></tr>
    <tr><th>Week Starting Date</th><td>{day(week['start'])}</td><th>Week Ending Date</th><td>{day(week['end'])}</td></tr>
    <tr><th>Name</th><td>{names}</td><th>SRN</th><td>{srns}</td></tr>
  </table>
  <table class="tasks">
    <colgroup><col style="width:.46in"><col style="width:3.08in"><col style="width:.85in"><col style="width:2.29in"></colgroup>
    {section('Activities Completed', week['completed'])}
    {section('In Progress', week['progress'])}
    {section('Plan for Next Week', week['next'])}
  </table>
  <table class="sig"><tr>
    <th>Digital Signature of<br>Project Guide With Name</th>
    <td><img src="{SIGNATURE.name}"></td>
    <td>{esc(data['guide'])}</td></tr></table>
  <footer><span>PESU Confidential</span><span>Page 1 of 1</span></footer>
</div>'''


CSS = '''
@page { size: 8.5in 11in; margin: 0; }
* { box-sizing: border-box; }
body { margin: 0; font-family: 'Caladea', Cambria, serif; font-size: 11pt; color: #000; }
.page { width: 8.5in; height: 11in; padding: 1in 1in 0; position: relative; page-break-after: always; overflow: hidden; }
.page:last-child { page-break-after: auto; }
header { position: absolute; top: .5in; left: 1in; right: 1in; height: .5in; border-bottom: .75pt solid #000;
         display: flex; align-items: flex-end; justify-content: center; font-weight: 700; font-size: 12pt; padding-bottom: 2pt; }
header img { position: absolute; left: -.26in; top: .03in; height: .5in; }
header span { margin-left: 1.1in; }
footer { position: absolute; bottom: .5in; left: 1in; right: 1in; display: flex; justify-content: space-between; font-size: 11pt; }
table { border-collapse: collapse; width: 6.68in; table-layout: fixed; }
td, th { border: .75pt solid #000; padding: 3pt 5pt; vertical-align: middle; text-align: left; font-size: 11pt; }
th { font-weight: 700; font-size: 12pt; }
.top { margin-top: .12in; }
.top td, .top th { height: .35in; }
.tasks tr:first-child th { border-top: none; }
.sec { text-align: left; height: .3in; }
.hd th { height: .3in; }
.item td { height: .55in; }
.c { text-align: center; }
.sig { width: 6.2in; margin: .35in 0 0 .3in; }
.sig td, .sig th { border: none; vertical-align: middle; }
.sig th { width: 1.87in; }
.sig td:nth-child(2) { width: 2.42in; }
.sig img { width: 1.9in; display: block; }
mark { background: #ff0; }
'''


def make_pdf():
    pages = ''.join(page(w) for w in data['weeks'])
    doc = ('<!doctype html><html><head><meta charset="utf-8">'
           '<link href="https://fonts.googleapis.com/css2?family=Caladea:ital,wght@0,400;0,700;1,400&display=block" rel="stylesheet">'
           f'<style>{CSS}</style></head><body>{pages}</body></html>')
    src = HERE / '.weekly_reports.html'
    src.write_text(doc)
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--no-pdf-header-footer', '--virtual-time-budget=8000',
                    f'--print-to-pdf={PDF}', src.as_uri()], check=True, stdin=subprocess.DEVNULL,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == '__main__':
    for n, week in enumerate(data['weeks'], 1):
        print(make_docx(week, n).name)
    make_pdf()
    print(PDF.name)
