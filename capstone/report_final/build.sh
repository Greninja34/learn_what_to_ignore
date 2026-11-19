#!/usr/bin/env bash
# Builds report.tex (and report.pdf as a preview) from report.md.
# Linux: conda run -n research2 ./build.sh   |   Windows: install pandoc + MiKTeX, run the two pandoc lines.
set -e
cd "$(dirname "$0")"
pandoc report.md -s -N --toc --top-level-division=chapter \
  -V documentclass=report -V papersize=a4 -V geometry:margin=2cm -V fontsize=12pt -V fontenc=OT1 \
  -V lof -V lot -H header.tex -o report.tex
pandoc report.md -N --toc --top-level-division=chapter \
  -V documentclass=report -V papersize=a4 -V geometry:margin=2cm -V fontsize=12pt -V fontenc=OT1 \
  -V lof -V lot -H header.tex --pdf-engine=pdflatex -o report.pdf
