# Key points per chapter (skeleton, not prose)

Write the report text from these in your own words. Numbers: source file in brackets. Cite keys = `build_report.py` BIB.
`PS` = `results/pilot_summary.md`.

## Abstract
- Problem: recognisers fail on damaged docs; damaged collections have fewest labels
- SSL learns from unlabelled lines, but corruption recipe is hand-picked, re-tuned per collection
- Ours: measure damage on real lines → physical models → fit params → use the derived damage in training
- Questions: beats hand-picked with few labels? transfers to unseen damage/media/scripts? invariance predicts error rise?
- Phase 1 done: survey, pipeline (IAM + CATMuS Latin/French, ~29k lines, 11 projects), CRNN 9.8% IAM vs PaddleOCR 11.4%, 8-statistic damage tool, derived recipe v0, pilot
- Results: pretraining no gain at this scale (CATMuS 5%: scratch 33.6% 2 seeds / 33.8% 3 seeds; derived-pretrained 33.4%) [PS A3/A4]
- Derived damage as augmentation: CATMuS 5% 33.8% → 31.6%, 3 seeds; hand-picked 33.6% [PS E1/E0b]
- Invariance predicts error rise, ρ ≈ −0.9; survives pixel-distance control [PS RQ3; results/tables/pixel_control.md]

## 1 Introduction
- Damage types: show-/bleed-through, fading, foxing/stains, capture (blur, noise, compression)
- Show-through physical form: front + α · blur_σ(mirror(back)) — cite [salerno]
- Motivation: what a model learns to ignore = its augmentations/corruptions [ericsson]; robustness depends on match to test damage [mintun]
- Scope: single cut lines, small models, 7 damage types, IAM + CATMuS now, unseen script later; no layout, no large VLMs
- Who benefits: archives, libraries, digital humanities with damaged, unlabelled collections

## 2 Problem Statement
- Problem statement (one paragraph; same as deck slide)
- RQ1: derived vs hand-picked vs none, few labels
- RQ2: transfer to held-out damage type, medium, script
- RQ3: does per-damage invariance predict CER rise?
- Hypotheses H1–H4 unchanged; H3 = sign flip (helps for background damage, hurts for stroke damage) — still untested
- Note: "derived" now means the damage is used in training in any form (augmentation, consistency, pretraining), not only pretraining

## 3 Literature Survey
- SSL for text: [seqclr], [lacuna] (60.4% → 23.7% CER with 30 labels), [kiss] (target-domain SSL not always > supervised transfer), [logo], [survey] (protocols inconsistent, augmentations ad hoc)
- Reconstruction > contrastive for handwriting: [garrido] (MAE best; 5.5% mean CER frozen, 8.8% at 10% labels)
- Degradation-aware: [textdiae] (hand-picked degradations; masking most useful), [augraphy], [prepocr] (hand-set damage, restoration), [salerno]
- NEW paragraph: degradation-model estimation is old
  - Kanungo, Haralick, Baird et al.: model validation as nonparametric permutation test [kanungo] (TPAMI 22(11):1209–1223, 2000)
  - earlier work estimated parameters from real scans, generated synthetic training data (1994–2002 line; MVA 1994 workshop paper — not yet in BIB, verify before citing)
  - Baird 2007 review: open problems = comparing models, sound use of synthetic data [baird07]
  - Limitation for us: binary images, classical OCR; not what a deep model learns to ignore
- Invariance and transfer: [ericsson], [mintun]
- Text-level fitted corruption: [hipe], [hanja]
- Summary table: now 11 rows (Kanungo added)
- Still unread in full (notes/literature/landscape_2026-11-16.md): Kanungo/Baird papers, LoGo-HTR full text, Text-MAE, MaskAug, optimal-transport HTR, self-training HTR — check before quoting numbers from them

## 4 Research Gap
- Established: SSL helps with few labels [lacuna] [kiss] [logo]; reconstruction wins [garrido]; augmentations decide invariance [ericsson]; match decides robustness [mintun]
- NOT new: fitting degradation models to real scans [kanungo] [baird07]; fitting text-level corruption [hipe] [hanja]
- Gap 1 (reworded): using measured damage of real lines to derive what a deep recogniser should learn to ignore, compared with hand-picked recipes on real damaged lines
- Gap 2: chain recipe → learned invariance → robustness, per damage type, incl. unseen damage/scripts
- "Not found" ≠ "absent"; consistency regularisation for few-label HTR not found in the 16 Nov search (opening for E2)
- Challenges (since 16 Nov: no separate section, Table 4.1 inside the gap chapter, 5 rows): SSL may lose to supervised transfer [kiss]; "you learned your own simulator" → real damaged lines; no clean physical model for some damage; script vs damage statistics + test leakage; protocols differ [survey] + competition

## 5 Objectives
- 7 objectives; objective 4 now = train with derived damage in order of cost: augmentation → consistency → MAE pretraining
- Approach loop: measure → model/fit → train → evaluate → analyse (Figure 5.1, results/figures/pipeline.png)
- Ladder:
  - E1 augmentation — done in pilot
  - E2 consistency training on unlabelled lines (CRNN + CTC, clean vs damaged view)
  - E3 one bounded SSL-pretraining rescue (protocol fixes, 10× unlabelled pool on Kaggle, public pretrained encoder), fixed decision date (date still to set)
  - E4 same-script, different-damage dataset pair
- Fixed: RQs, hypotheses, held-out tests, baselines, protocol. Decided by evidence: damage types, model size, strengths, label budgets
- Reference points: supervised transfer, off-the-shelf recogniser [paddle]

## 6 Overview of Datasets
- IAM-line [iam]: 6,482 / 976 / 2,915 lines, 657 writers, official writer-independent split
- CATMuS Medieval [catmus]: 194,808 lines; subset Latin + French, 11 projects: 25,005 train (5% kept for val) / 4,022 test; test = unseen manuscripts
- Phase 3 unseen scripts: IIIT-INDIC-HW-WORDS (872k words, 10 scripts), Muharaf (36,311 Arabic lines)
- Protocol: grey, height 64 px, Unicode NFC; charsets from train only (79 IAM, 195 CATMuS)
- Finding: 99% of CATMuS images have pure-black polygon fill (~15% of image) → filled with local paper tone + mask
- A2: paper level KS 0.82, faint grey 0.84; bg unevenness 0.42; contrast, sharpness, noise < 0.5 → A2 FAIL (need ≥ 3) [PS A2; results/tables/a2_effect_sizes.md; fig1_stats_iam_vs_catmus.png]. Full A2 discussion lives here (Section 6.4) since 16 Nov; Chapter 7 only refers back in one sentence
- Derived recipe v0: tone 84%, show-through 89%, stain 37%, fading 26%, noise 11%, blur 5%; ink loss held out [report Table 7.1; results/derived/]

## 7 Conclusion of Phase 1
### Work completed
- Survey re-checked Nov 2026; pipeline; CRNN [crnn] + CTC [ctc], 7.4M params; damage tool (8 stats); 7 damage models; ConvMAE pilot; E1 augmentation; robustness + invariance analysis
- ViT (6.5M) memorised few labels (60–75% CER) → set aside [PS "Record" section]
### Preliminary results (numbers)
- Baselines [PS Table 1]: IAM 100% 9.8%; CATMuS 100% 20.0%; IAM 10% 19.9% (3 seeds; 19.6% with 2); IAM 1% 43.3%; CATMuS 5% 33.8% (3 seeds; 33.6% with 2); PaddleOCR 11.4% IAM, 52.5% CATMuS [paddle]
- A1 PASS: medium damage × CER — ink loss 7.6, noise 4.9, tone 3.4, blur 3.1; show-through/fading/stains ≤ 1.4 [PS A1; results/robustness.csv]
- Real CATMuS: lowest-contrast quartile 1.35–1.47× worse than highest; paper/noise/unevenness 0.93–1.08×; sharpness 0.75× (confounded) [results/tables/real_damage.md]
- A3 FAIL: CATMuS 5% scratch 33.8 / masking 33.3 / hand-picked 35.0 / derived 33.4; IAM 10% 19.9 / 20.4 / 21.0 / 20.5; IAM 1% 43.3 / 43.8 / 44.7 / 43.9 [PS A3/A4]; consistent with [kiss]
- A4 PASS (read with care): derived ≤ hand-picked 3/3, but derived ≈ masking only → hand-picked hurts, derived no harm
- Recipe trace (pretraining, seeds 0/1): blur high 64.1/63.6 hand-picked vs 79.2/79.6 scratch; tone medium 32.1/26.4 derived vs 39.9/39.4 scratch; nothing helps on ink loss [results/robustness.csv]
- E1 augmentation, 3 seeds [PS E1/E0b; results/tables/hard_subset.md]:
  - CATMuS 5% all: 33.8 / hand 33.6 / derived 31.6 (±0.5) / bgnorm 33.0
  - hardest quartiles (darkest paper / most show-through / lowest contrast): scratch 35.6 / 35.7 / 39.4 → derived 33.0 / 32.9 / 37.0
  - IAM 10% clean: 19.9 / 18.8 / 18.9 / 19.8
  - Verdicts B1, B3, B4, B5 PASS; B2 pending [PS verdict table]
- E1 caveats (must appear):
  - (a) IAM synthetic medium 37.9 → 19.4 is partly circular (same 6 families trained and tested); held-out ink loss CER ratio ×3.82 → ×3.59 derived, ×3.27 hand-picked
  - (b) CATMuS hard-quartile gain 2.4–2.8 ≈ all-lines gain 2.2 → "helps on CATMuS", not "damage-specific"
  - (c) hand-picked wins on IAM (incl. synthetic damage), derived wins on CATMuS
  - (d) 3 seeds, one recogniser, one source/target pair
- RQ3: ρ = −0.92 (21 settings, full-label IAM baseline); −0.78 to −0.95 in all 9 pilot models; fixed strength −0.81 to −0.88; across 8 IAM-10% models negative in 21/21 settings, mean −0.69 [PS RQ3; results/tables/invariance_vs_cer.md; results/tables/controls.md]
- Pixel control: partial ρ (feature invariance | pixel cosine) −0.56 to −0.87, mean −0.80, p ≤ 0.01 in the 9 pilot models (new 3rd scratch seed −0.76); weak in augmented / bgnorm models (mean over all 19 runs −0.53) [results/tables/pixel_control.md]
  - exact: 6 augmented models −0.12 to −0.39 (none significant); 3 bgnorm models −0.51 to +0.01 → the report now says RQ3 holds clearly only for models not trained on the damage
### Lessons
- CATMuS polygon fill + ViT padding attention: would have silently invalidated results; now checked
- Sanity check (memorise small set) before any run; every number from a script
- Test the cheapest use of an idea first (augmentation before pretraining)
- Synthetic tests built from training families flatter the recipe → held-out damage + real lines
- Repeat the literature search as the claim sharpens (Kanungo/Baird moved the novelty)

## 8 Plan of Work for Phase 2
- Jan–Mar: damage models v1 fitted per type; tag a few hundred real CATMuS test lines
- Jan–Feb: E2 consistency training, 3 seeds
- Feb–Mar: E3 bounded SSL rescue, fixed decision date (set the date with the guide)
- Mar–May: E4 same-script / different-damage pair (dataset still to choose)
- Apr–May: held-out evaluation (unseen damage, medium), supervised-transfer baseline → RQ1, RQ2
- Fallback side project: VLM-OCR hallucination under controlled damage (literature check needed)
- Phase 3 (Jun–Dec 2027): RQ3 analysis, unseen scripts, camera capture, ablations/seeds, paper (ICDAR workshop → main track / IJDAR; check deadlines on conference sites)
- Gantt: capstone/reviews/_kit/assets/img/gantt.png (from _kit/gantt.md)
- Effort table: Vignesh row now = E1–E3
