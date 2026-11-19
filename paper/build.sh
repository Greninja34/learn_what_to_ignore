#!/usr/bin/env bash
# Build paper/paper.pdf from paper/paper.md (the source of truth).
#   bash paper/build.sh            (from anywhere; uses conda env research2)
# Pipeline: pandoc (+ citeproc with ieee.csl, + floats.lua) -> _build/paper.tex -> luatex x2 -> paper.pdf
# Engine: the lualatex/xelatex binaries on this machine are broken, so (as in capstone/report/build_pandoc.py)
# plain `luatex` runs with a lualatex format that this script builds once into _build/fmt/.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESEARCH="$(dirname "$HERE")"
BUILD="$HERE/_build"
mkdir -p "$BUILD/fmt"

if ! command -v pandoc >/dev/null; then
  source ~/miniconda3/etc/profile.d/conda.sh && conda activate research2
fi

# 1. lualatex format for plain luatex (once)
if [ ! -f "$BUILD/fmt/lualatex.fmt" ]; then
  echo "building a lualatex format for luatex (once) ..."
  (cd "$BUILD/fmt" && luatex -ini -jobname=lualatex -progname=lualatex '*lualatex.ini' > fmt.log 2>&1) \
    || { echo "format build failed; see $BUILD/fmt/fmt.log"; exit 1; }
fi

# 2. Markdown -> LaTeX
pandoc "$HERE/paper.md" \
  --from markdown+raw_tex+pipe_tables+implicit_figures+link_attributes \
  --to latex --standalone --template "$HERE/template.tex" \
  --citeproc --bibliography "$HERE/refs.bib" --csl "$HERE/ieee.csl" \
  --lua-filter "$HERE/floats.lua" \
  -V fontdir="$RESEARCH/fonts" -V figroot="$RESEARCH" \
  -o "$BUILD/paper.tex"

# 3. LaTeX -> PDF (two passes for cross-references)
cd "$BUILD"
for pass in 1 2; do
  luatex --fmt="$BUILD/fmt/lualatex" --progname=lualatex --interaction=nonstopmode --halt-on-error paper.tex \
    > "$BUILD/luatex.log" 2>&1 || { tail -30 "$BUILD/paper.log"; exit 1; }
done
cp "$BUILD/paper.pdf" "$HERE/paper.pdf"
echo "undefined-reference warnings: $(grep -c "undefined" "$BUILD/paper.log" || true)"
grep -E "Overfull \\\\hbox \(([2-9][0-9]|[0-9]{3,})" "$BUILD/paper.log" | head -5 || true
echo "wrote $HERE/paper.pdf ($(pdfinfo "$HERE/paper.pdf" 2>/dev/null | awk '/^Pages/ {print $2}') pages)"
