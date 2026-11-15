#!/usr/bin/env bash
# Live view of the pilot: comparison table, run in progress, chain log, GPU.
# Refreshes every 10 s. Quit with Ctrl+C.
#   bash ~/Desktop/research/lwti/scripts/watch.sh
L=~/data/lwti/logs
PY=~/miniconda3/envs/research2/bin/python
watch -n 10 -t "
$PY ~/Desktop/research/lwti/scripts/progress.py 2>/dev/null
echo; echo '=== chain (latest steps) ==='; tail -4 $L/overnight_cnn.log 2>/dev/null
echo; nvidia-smi --query-gpu=utilization.gpu,memory.used,temperature.gpu --format=csv,noheader | sed 's/^/GPU: /'
"
