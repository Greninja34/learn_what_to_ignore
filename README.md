# Research folder: index

Project: **Learning What to Ignore**, self-supervised text recognition under degradation (Team 147, UE24CS320A Capstone, PES University). Layout reorganised on 10 Nov 2026.

**What this repo contains:** the pilot code, results, run logs and research notes. The folders `capstone/`, `fonts/` and `_archive/`, and the checkpoint files `runs/**/*.pt`, are kept on the author's machine and are **not** in this repo (see `.gitignore`). Paths below that point to them will not exist after cloning.

| Folder | What |
|---|---|
| `capstone/` | *Not in this repo.* Everything that goes to the college: slides, report, weekly reports, templates, submitted files, team briefing |
| `lwti/` | Pilot code (plain PyTorch, conda env `research2`). Run as `python -m lwti....` from this folder |
| `results/` | Every number and figure: `runs.csv`, `pilot_summary.md`, `tables/`, `figures/`, `stats/`, `derived/` |
| `runs/` | Logs and CSVs of each training run. Checkpoints (`*.pt`, 1.3 GB in total) are *not* in this repo |
| `notes/` | Session handoff, research trail, literature landscape, brainstorming |
| `fonts/` | *Not in this repo* (licensed fonts). Segoe UI, Consolas and other fonts used by figures and pages; the code reads this folder, so clone-and-run needs a local copy |
| `_archive/` | *Not in this repo.* Superseded versions |

## capstone/ (not in this repo)

| Path | What |
|---|---|
| `reviews/` | **Start here for slides.** One folder per review (`review1/`, `review2/`, `review3/`), each with `deck/` (edit `slides.md`), `submission/` and `template/`. Index: `reviews/README.md`. Shared parts in `reviews/_kit/` |
| `report/` | Phase-1 report. Edit `report.md`, then run `python capstone/report/build_pandoc.py` (pandoc, research2 env) → `Team147_Phase1_Report.docx`. `build_report.py` (older python-docx build) is kept for its reference list; its `_DRAFT.docx` is superseded |
| `weekly_reports/` | Edit `reports.md`, run `make_reports.py` |
| `team_briefing/` | `Team147_Pilot_Briefing.pdf`, the briefing for teammates (the HTML source is in `notes/briefing_source.html`) |
| `format/` | Department templates for the weekly report and report guidelines (review templates moved into `reviews/*/template/`) |

## notes/

| Path | What |
|---|---|
| `HANDOFF_2026-11-10.md` | **Start here** for the pilot: state, results, decisions, to-do |
| `Vision SSL OCR research handoff.md` | Master record of the research trail (memo, critique, both research reports) |
| `Learning What to Ignore Project Starter Pack.md` | Reading path, datasets and licences |
| `literature/landscape_2026-11-09.md` | Closest work, the open question, draft research-gap statement |
| `brainstorming/` | Topic list, paper ideas, the OCR-hallucination and cube report |
| `pilot_explainer.html` | Explainer page for the pilot (numbers from 9 Nov evening, not final) |

## results/ quick map

| File | What |
|---|---|
| `pilot_summary.md` | A1–A4 verdicts and all tables (`python -m lwti.eval.summary`) |
| `tables/controls.md` | Extra checks from 10 Nov: invariance at fixed strength, across models, robustness by recipe (`python -m lwti.eval.controls`) |
| `runs.csv`, `robustness.csv`, `invariance.csv`, `reference.csv` | One row per run / damage setting |
