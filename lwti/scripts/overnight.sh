#!/usr/bin/env bash
# Overnight chain after the CATMuS rebuild (9 Nov 2026):
#   wait for rebuild -> re-measure -> re-derive -> figures -> PaddleOCR on CATMuS (CPU, in parallel)
#   -> 3 MAE pretrainings -> fine-tuning queue (pilot_queue.sh, incl. robustness + invariance)
#   -> real-damage table -> summary
# Each step logs to ~/data/lwti/logs/; progress lines go to overnight.log.
#   bash lwti/scripts/overnight.sh     (from ~/Desktop/research)
set -u
cd "$(dirname "$0")/../.."
PY=~/miniconda3/envs/research2/bin/python
OCR=~/miniconda3/envs/ocr/bin/python
L=~/data/lwti/logs
say() { echo "$(date +%H:%M) $*"; }

say "waiting for CATMuS rebuild"
while pgrep -f "lwti.data.prepare_catmu[s]" > /dev/null; do sleep 30; done
n=$(ls ~/data/lwti/processed/catmus/train/part-*.parquet 2>/dev/null | wc -l)
[ "$n" -ge 40 ] || { say "rebuild looks incomplete ($n parts); stopping"; exit 1; }

say "re-measuring (IAM train, CATMuS train + test)"
$PY -m lwti.damage.measure --data iam --split train --n 3000 > $L/measure_iam.log 2>&1
$PY -m lwti.damage.measure --data catmus --split train --n 3000 > $L/measure_catmus_train.log 2>&1
$PY -m lwti.damage.measure --data catmus --split test --n 5000 > $L/measure_catmus_test.log 2>&1

say "re-deriving corruption settings"
$PY -m lwti.damage.derive > $L/derive.log 2>&1 && grep -E "prob=" $L/derive.log

say "figures"
$PY -m lwti.eval.fig_stats > $L/fig_stats.log 2>&1
$PY -m lwti.eval.fig_corruptions > $L/fig_corruptions.log 2>&1

say "PaddleOCR on CATMuS test (CPU, background)"
( $PY -m lwti.eval.paddle_ref export --data catmus && $OCR lwti/eval/paddle_ref.py run --data catmus --device cpu \
  && $PY -m lwti.eval.paddle_ref score --data catmus ) > $L/paddle_catmus.log 2>&1 &

for c in none handpicked derived_v0; do
  say "MAE pretraining: $c"
  rm -rf runs/mae_$c
  $PY -m lwti.train.pretrain_mae --corrupt $c --steps 20000 > $L/mae_$c.log 2>&1
  tail -1 $L/mae_$c.log
done

say "fine-tuning queue"
bash lwti/scripts/pilot_queue.sh > $L/pilot_queue.log 2>&1
tail -3 $L/pilot_queue.log

say "real-damage table + summary"
$PY -m lwti.eval.real_damage runs/catmus_* > $L/real_damage.log 2>&1
wait
$PY -m lwti.eval.summary > $L/summary.log 2>&1
say "overnight chain finished"
