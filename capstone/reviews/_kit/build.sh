#!/usr/bin/env bash
# Build one review deck from its slides.md.
#   ./build.sh review1     (or review2, review3)
# Reads   reviews/<review>/deck/slides.md
# Writes  reviews/<review>/deck/out/<review>.pdf, .pptx (editable), .html (presenter view: press P)
# Needs the research2 conda env and an internet connection (Google Fonts).
set -euo pipefail
KIT="$(cd "$(dirname "$0")" && pwd)"
REVIEW="${1:?usage: ./build.sh review1|review2|review3}"
DECK="$KIT/../$REVIEW/deck"
[ -f "$DECK/slides.md" ] || { echo "no slides.md in $DECK"; exit 1; }
source "$HOME/miniconda3/etc/profile.d/conda.sh"
conda activate research2
OUT="$DECK/out"; mkdir -p "$OUT"; ln -sfn "$KIT/assets" "$OUT/assets"
cd "$KIT"
cp "$DECK/slides.md" _slides.md          # marp resolves assets/ next to the file, so build from the kit
m() { marp --theme theme.css --html --allow-local-files "$@" < /dev/null; }

m gantt.md --image png --image-scale 2 -o assets/img/gantt.png   # timeline slide picture
m _slides.md --pdf -o "$OUT/$REVIEW.pdf"
m _slides.md -o "$OUT/$REVIEW.html"
m --template bare _slides.md -o _bare.html
m --template bare gantt.md -o _gantt_bare.html
m --notes _slides.md -o _notes.txt
G=$(npm root -g)
DECK_MD=_slides.md NODE_PATH="$G:$G/@marp-team/marp-cli/node_modules" node tools/to_pptx.js _bare.html _gantt_bare.html _notes.txt "$OUT/$REVIEW.pptx"
rm -f _slides.md _bare.html _gantt_bare.html _notes.txt
echo "built $OUT/$REVIEW.pdf, .pptx, .html"
