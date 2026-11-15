#!/usr/bin/env bash
# Night of 9-10 Nov 2026, second chain: the comparison moved from the ViT to the CRNN encoder.
# (The small ViT memorised the few labelled lines; see results/pilot_summary.md.)
#   1. ConvMAE pretraining of the CRNN's CNN: plain, hand-picked, derived (12k steps each)
#   2. CRNN fine-tunes from each pretrained CNN with the SAME settings as the scratch CRNN runs
#      (IAM 10% and 1%, CATMuS 5%; seeds 0 and 1) + the missing scratch CATMuS 5% seed 1
#   3. robustness + invariance on the IAM 100% and 10% runs, real-damage table, summary
set -u
cd "$(dirname "$0")/../.."
PY=~/miniconda3/envs/research2/bin/python
L=~/data/lwti/logs
say() { echo "$(date +%H:%M) $*"; }
done_run() { [ -f "runs/$1/test_predictions.tsv" ]; }

for c in none handpicked derived_v0; do
  if [ -f runs/cmae_$c/encoder.pt ]; then say "skip pretraining cmae_$c"; continue; fi
  say "ConvMAE pretraining: $c"
  $PY -m lwti.train.pretrain_mae --arch cnn --corrupt $c --steps 12000 > $L/cmae_$c.log 2>&1
  tail -1 $L/cmae_$c.log
done

ft() {  # ft <data> <frac> <seed> <steps> <eval_every> <tag or "">
  local data=$1 frac=$2 seed=$3 steps=$4 ev=$5 tag=$6
  local name="${data}_crnn${tag:+_$tag}_f${frac}_s${seed}"
  done_run "$name" && { say "skip $name"; return; }
  say "$name"
  $PY -m lwti.train.train_ctc --data "$data" --model crnn --frac "$frac" --seed "$seed" --steps "$steps" \
      --eval-every "$ev" --name "$name" ${tag:+--tag "$tag" --init runs/$tag/encoder.pt} > "$L/$name.log" 2>&1
  grep -h "TEST CER" "$L/$name.log"
}

ft catmus 0.05 1 8000 500 ""
for seed in 0 1; do
  for tag in cmae_none cmae_handpicked cmae_derived_v0; do
    ft catmus 0.05 $seed 8000 500 $tag
    ft iam 0.1 $seed 8000 500 $tag
    ft iam 0.01 $seed 3000 250 $tag
  done
done

say "robustness + invariance"
RUNS="runs/iam_crnn_f1_s0 $(ls -d runs/iam_crnn*_f0.1_s* | tr '\n' ' ')"
$PY -m lwti.eval.robustness $RUNS > $L/robustness.log 2>&1
$PY -m lwti.eval.invariance $RUNS --n 500 > $L/invariance.log 2>&1
say "real damage + summary"
$PY -m lwti.eval.real_damage $(ls -d runs/catmus_crnn*) > $L/real_damage.log 2>&1
$PY -m lwti.eval.summary > $L/summary.log 2>&1
say "chain finished"
