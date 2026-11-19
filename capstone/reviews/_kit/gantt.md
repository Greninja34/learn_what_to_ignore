---
marp: true
theme: lwti
size: 16:9
paginate: false
header: '![PES](assets/pes_emblem.png)'
title: "Learning What to Ignore: timeline"
---

<!--
HOW TO EDIT
- 16 month columns: Sep 2026 (column 2) ... Dec 2027 (column 17). Column 1 is the task label.
- A bar's span is  grid-column: <first month col> / <last month col + 1>.
  e.g. Sep–Oct 2026 = 2 / 4.
- Phases: I = Sep–Dec 2026 (2 / 6), II = Jan–May 2027 (6 / 11), III = Jun–Dec 2027 (11 / 18).
  Each phase has one colour (p1 blue, p2 green, p3 red); give a bar its phase's class.
- No review markers or legend, by request.
- Phase months are indicative; align them with the department calendar.
-->

<style scoped>
section { --p1: #0078CD; --p2: #00893E; --p3: #DB3837; --p1-fill: #EEF5FC; --p2-fill: #EDF6EF; --p3-fill: #FDEEEC; }
.gantt { position: relative; display: flex; flex-direction: column; gap: 4px; font-size: 15px; }
.gantt .gr { display: grid; grid-template-columns: 290px repeat(16, 1fr); align-items: center; min-height: 22px; position: relative; }
.gantt .gr > * { grid-row: 1; }
/* tinted phase columns and month gridlines, behind everything */
.gantt .bg { position: absolute; inset: 0; display: grid; grid-template-columns: 290px repeat(16, 1fr); }
.gantt .bg > div { border-left: 1px solid rgba(18, 21, 27, .06); }
.gantt .bg .p1 { background: var(--p1-fill); } .gantt .bg .p2 { background: var(--p2-fill); } .gantt .bg .p3 { background: var(--p3-fill); }
.gantt .mh { font-family: var(--mono); font-size: 13px; font-weight: 600; color: var(--meta); text-align: center; }
.gantt .yr { font-family: var(--mono); font-size: 13px; font-weight: 600; color: var(--ink); text-align: center; }
.gantt .ph { font-family: var(--mono); font-size: 13px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;
  text-align: center; border-radius: 6px; padding: 4px 0; margin: 0 3px; color: #FFFFFF; }
.gantt .ph.p1 { background: var(--p1); } .gantt .ph.p2 { background: var(--p2); } .gantt .ph.p3 { background: var(--p3); }
.gantt .lab { color: var(--body); white-space: nowrap; padding-right: 10px; }
.gantt .sec { font-family: var(--mono); font-size: 13px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; padding-top: 8px; }
.gantt .sec.p1 { color: var(--p1); } .gantt .sec.p2 { color: var(--p2); } .gantt .sec.p3 { color: var(--p3); }
.gantt .bar { height: 14px; border-radius: 999px; margin: 0 4px; }
.gantt .bar.p1 { background: var(--p1); } .gantt .bar.p2 { background: var(--p2); } .gantt .bar.p3 { background: var(--p3); }
</style>

# Timeline

<div class="gantt">
<div class="bg"><div style="border:none;"></div><div class="p1"></div><div class="p1"></div><div class="p1"></div><div class="p1"></div><div class="p2"></div><div class="p2"></div><div class="p2"></div><div class="p2"></div><div class="p2"></div><div class="p3"></div><div class="p3"></div><div class="p3"></div><div class="p3"></div><div class="p3"></div><div class="p3"></div><div class="p3"></div></div>

<!-- years, months, phases -->
<div class="gr"><div></div><div class="yr" style="grid-column: 2 / 6;">2026</div><div class="yr" style="grid-column: 6 / 18;">2027</div></div>
<div class="gr"><div></div><div class="mh">Sep</div><div class="mh">Oct</div><div class="mh">Nov</div><div class="mh">Dec</div><div class="mh">Jan</div><div class="mh">Feb</div><div class="mh">Mar</div><div class="mh">Apr</div><div class="mh">May</div><div class="mh">Jun</div><div class="mh">Jul</div><div class="mh">Aug</div><div class="mh">Sep</div><div class="mh">Oct</div><div class="mh">Nov</div><div class="mh">Dec</div></div>
<div class="gr"><div></div><div class="ph p1" style="grid-column: 2 / 6;">Phase I</div><div class="ph p2" style="grid-column: 6 / 11;">Phase II</div><div class="ph p3" style="grid-column: 11 / 18;">Phase III</div></div>

<div class="gr"><div class="lab sec p1">Foundations</div></div>
<div class="gr"><div class="lab">Literature survey and formulation</div><div class="bar p1" style="grid-column: 2 / 4;"></div></div>
<div class="gr"><div class="lab">Data pipeline and supervised baseline</div><div class="bar p1" style="grid-column: 3 / 6;"></div></div>
<div class="gr"><div class="lab">Damage-measurement tool</div><div class="bar p1" style="grid-column: 4 / 6;"></div></div>
<div class="gr"><div class="lab">Pilot: pretraining, E1 augmentation</div><div class="bar p1" style="grid-column: 5 / 7;"></div></div>

<div class="gr"><div class="lab sec p2">Damage models and main runs</div></div>
<div class="gr"><div class="lab">Damage models v1, E2 consistency</div><div class="bar p2" style="grid-column: 6 / 9;"></div></div>
<div class="gr"><div class="lab">E3 bounded SSL rescue (stop date)</div><div class="bar p2" style="grid-column: 7 / 9;"></div></div>
<div class="gr"><div class="lab">E4 same-script, new-damage pair</div><div class="bar p2" style="grid-column: 8 / 11;"></div></div>
<div class="gr"><div class="lab">Held-out evaluation (RQ1, RQ2)</div><div class="bar p2" style="grid-column: 9 / 11;"></div></div>

<div class="gr"><div class="lab sec p3">Analysis and release</div></div>
<div class="gr"><div class="lab">Invariance–error analysis (RQ3)</div><div class="bar p3" style="grid-column: 11 / 14;"></div></div>
<div class="gr"><div class="lab">Script and medium transfer</div><div class="bar p3" style="grid-column: 12 / 15;"></div></div>
<div class="gr"><div class="lab">Ablations and seeds</div><div class="bar p3" style="grid-column: 14 / 16;"></div></div>
<div class="gr"><div class="lab">Paper, code and data release</div><div class="bar p3" style="grid-column: 15 / 18;"></div></div>

</div>
