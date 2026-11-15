#!/usr/bin/env bash
# Pilot queue: fine-tune every encoder on the same label budgets, then score
# robustness and invariance. Waits for the CRNN baselines and the three MAE
# pretraining runs to finish first. Safe to re-run: finished runs are skipped.
#
#   bash lwti/scripts/pilot_queue.sh            (from ~/Desktop/research)
#
# Logs: ~/data/lwti/logs/<run>.log
set -u
cd "$(dirname "$0")/../.."
PY=~/miniconda3/envs/research2/bin/python
L=~/data/lwti/logs
mkdir -p "$L"

# wait for running baselines / pretraining
while pgrep -f "lwti.train.(train_ctc|pretrain_mae)" > /dev/null; do sleep 60; done
for c in none handpicked derived_v0; do
  [ -f runs/mae_$c/encoder.pt ] || { echo "missing runs/mae_$c/encoder.pt"; exit 1; }
done

done_run() { [ -f "runs/$1/test_predictions.tsv" ]; }

ft() {  # ft <data> <frac> <seed> <steps> <tag> [init]
  local data=$1 frac=$2 seed=$3 steps=$4 tag=$5 init=${6:-}
  local name="${data}_vit_${tag}_f${frac}_s${seed}"
  done_run "$name" && { echo "skip $name"; return; }
  echo "$(date +%H:%M) $name"
  $PY -m lwti.train.train_ctc --data "$data" --model vit --frac "$frac" --seed "$seed" --steps "$steps" \
      --tag "$tag" --name "$name" ${init:+--init "$init"} --eval-every $([ "$frac" = "0.01" ] && echo 250 || echo 500) \
      > "$L/$name.log" 2>&1
  grep -h "TEST CER" "$L/$name.log"
}

# CRNN reference on CATMuS
for f in 1.0 0.05; do
  n="catmus_crnn_f${f}_s0"
  done_run "$n" || { echo "$(date +%H:%M) $n"; $PY -m lwti.train.train_ctc --data catmus --model crnn --frac $f --seed 0 \
      --steps $([ $f = 1.0 ] && echo 30000 || echo 8000) --name "$n" > "$L/$n.log" 2>&1; grep -h "TEST CER" "$L/$n.log"; }
done

# ViT: scratch vs three pretrainings, same budgets and seeds
for seed in 0 1; do
  for tag in scratch mae_none mae_handpicked mae_derived_v0; do
    init=""; [ "$tag" != scratch ] && init="runs/$tag/encoder.pt"
    ft catmus 0.05 $seed 8000 $tag $init
    ft iam 0.1 $seed 8000 $tag $init
    ft iam 0.01 $seed 3000 $tag $init
  done
done

# robustness (IAM test, all families x 3 levels) + invariance for the IAM models
IAM_RUNS=$(ls -d runs/iam_* | grep -v overfit)
$PY -m lwti.eval.robustness $IAM_RUNS > "$L/robustness.log" 2>&1
$PY -m lwti.eval.invariance $IAM_RUNS --n 500 > "$L/invariance.log" 2>&1
echo "$(date +%H:%M) queue finished"
