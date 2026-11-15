#!/usr/bin/env bash
# Waits for the overnight chain to finish, then appends the results to the handoff file.
# Runs independently of the Claude session.
H=~/Desktop/research/notes/HANDOFF_2026-11-10.md
until grep -q "chain finished" ~/data/lwti/logs/overnight_cnn.log 2>/dev/null; do
  pgrep -f "overnight_cn[n].sh" > /dev/null || break   # chain died: append whatever exists
  sleep 60
done
{
  echo
  echo "_Appended $(date '+%d %b %Y %H:%M')._"
  echo
  echo "### Chain log"
  echo '```'
  cat ~/data/lwti/logs/overnight_cnn.log
  echo '```'
  echo
  echo "### Comparison table"
  echo '```'
  ~/miniconda3/envs/research2/bin/python ~/Desktop/research/lwti/scripts/progress.py
  echo '```'
  echo
  echo "### results/pilot_summary.md"
  echo
  cat ~/Desktop/research/results/pilot_summary.md 2>/dev/null || echo "(summary missing — run python -m lwti.eval.summary)"
} >> "$H"
