#!/usr/bin/env bash
# E1 + E0b chain (written 15-16 Nov 2026, not yet run).
#   E1:  the damage recipes as plain TRAINING AUGMENTATION of the scratch CRNN
#        (--aug handpicked / derived_v0, redrawn every epoch, train lines only)
#   E0b: simple background normalisation on train, val and test lines (--bgnorm)
#   + scratch seed 2 (seeds 0 and 1 exist), so every arm has 3 seeds.
# Same settings as the scratch CRNN runs: IAM 10% and CATMuS 5%, 8000 steps, eval every 500.
# Then robustness + invariance on the new IAM-10% runs, pixel control, hard-subset table, summary.
# Finished runs (test_predictions.tsv present) are skipped, so the chain can be restarted.
# ~20 training runs x ~10 min + ~20 min eval = about 3.5-4 GPU hours.
set -u
cd "$(dirname "$0")/../.."
PY=~/miniconda3/envs/research2/bin/python
L=~/data/lwti/logs
mkdir -p $L
say() { echo "$(date +%H:%M) $*"; }
done_run() { [ -f "runs/$1/test_predictions.tsv" ]; }
finished() { for r in $(ls -d $1 2>/dev/null); do done_run "$(basename $r)" && echo "$r"; done; }  # finished runs matching a glob

flags() {  # tag -> train_ctc flags
  case $1 in
    aug_handpicked) echo "--aug handpicked" ;;
    aug_derived_v0) echo "--aug derived_v0" ;;
    bgnorm) echo "--bgnorm" ;;
    "") echo "" ;;
  esac
}

run() {  # run <data> <frac> <seed> <tag or "">
  local data=$1 frac=$2 seed=$3 tag=$4
  local name="${data}_crnn${tag:+_$tag}_f${frac}_s${seed}"
  done_run "$name" && { say "skip $name"; return; }
  say "$name"
  $PY -m lwti.train.train_ctc --data "$data" --model crnn --frac "$frac" --seed "$seed" --steps 8000 \
      --eval-every 500 --name "$name" ${tag:+--tag "$tag"} $(flags "$tag") > "$L/$name.log" 2>&1
  grep -h "TEST CER" "$L/$name.log"
}

run iam 0.1 2 ""
run catmus 0.05 2 ""
for seed in 0 1 2; do
  for tag in aug_handpicked aug_derived_v0 bgnorm; do
    run iam 0.1 $seed $tag
    run catmus 0.05 $seed $tag
  done
done

say "robustness + invariance (IAM-10% runs not yet in results/robustness.csv)"
NEW=""
for r in $(finished "runs/iam_crnn*_f0.1_s*"); do
  grep -q "^$(basename $r)," results/robustness.csv || NEW="$NEW $r"
done
if [ -n "$NEW" ]; then
  $PY -m lwti.eval.robustness $NEW > $L/robustness_e1.log 2>&1
  $PY -m lwti.eval.invariance $NEW --n 500 > $L/invariance_e1.log 2>&1
else
  say "no new IAM-10% runs to score"
fi
say "pixel control, hard subset, summary"
$PY -m lwti.eval.pixel_control > $L/pixel_control.log 2>&1
$PY -m lwti.eval.hard_subset $(finished "runs/catmus_crnn*_f0.05_s*") > $L/hard_subset.log 2>&1
$PY -m lwti.eval.summary > $L/summary.log 2>&1
say "chain finished"
