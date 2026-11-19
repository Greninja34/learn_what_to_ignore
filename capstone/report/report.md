<!--
Phase-1 report, WITH-PILOT version: the template version plus the pilot study (Section 7.2) and the code walkthrough (Appendix B).
Build: python capstone/report/build_pandoc.py --src report.md --name Team147_Phase1_Report_with_pilot
The previous 33-page version is in git history.
-->

::: abstract
Text recognisers fail on damaged documents (faded ink, ink showing through from the back of the page, stains, darkened parchment), and these are exactly the collections with the fewest transcribed lines. Self-supervised learning (SSL) can learn from unlabelled lines by rebuilding a line from a corrupted copy, but the corruptions it learns to ignore are chosen by hand and re-tuned for every collection. This project, *Learning What to Ignore*, replaces that guess with a measurement: we measure the damage on real historical lines, model each damage type physically, derive how often and how strongly to apply it, and train the recogniser with this derived damage. We test whether it beats hand-picked damage when labels are few, whether the benefit transfers to unseen damage, media and scripts, and whether a model's invariance to a damage predicts how much that damage raises its error. In Phase 1 we completed the literature survey and the formulation; acquired and processed IAM (modern English handwriting) and a Latin and French subset of CATMuS Medieval (29,027 real manuscript lines from 11 projects); built a tool that measures eight damage statistics per line; showed that real medieval lines differ from clean ones mainly in paper tone and show-through; and derived a first damage recipe from these measurements. In a one-week pilot, pretraining the recogniser's CNN as a masked autoencoder did not beat training from scratch at this scale, but the same derived damage used as training augmentation lowered the character error rate on real medieval test lines from 33.8% to 31.6%, where hand-picked damage gave 33.6%.
:::

# Introduction

## Background

Optical character recognition (OCR) converts images of text into characters. On clean scans, line-level handwritten text recognition (HTR) reaches error rates of a few percent on benchmarks such as IAM [@iam]. Archives and libraries, however, hold millions of pages whose ink has faded, whose back-side text shows through, whose parchment has darkened or is stained, or that were captured under poor light. Accuracy drops sharply on such pages, and almost nobody has transcribed enough of their lines to train a model.

Self-supervised learning (SSL) is the usual answer to the shortage of labels: a model first learns from unlabelled lines through a task such as rebuilding a line from a corrupted copy, and is then fine-tuned on a few transcribed lines [@survey], [@kiss]. For handwriting, pixel-reconstruction pretraining has recently been shown to outperform contrastive methods [@garrido].

## Motivation and scope

Every SSL method decides, through its corruptions, what the model learns to ignore. In general vision, different tasks need different invariances [@ericsson], and robustness to a corruption depends on how similar the training augmentations are to it [@mintun]. For text recognition the corruptions are still chosen by hand [@textdiae]. Our question is therefore: *which damage should a recogniser learn to see through, and can that choice be derived from the documents themselves?*

The project studies single text lines already cut from the page, with small recognisers (5–25 million parameters) so that differences can be traced to the training method. Phase 1 covers two Latin-script datasets, IAM and CATMuS Medieval [@catmus]; an unseen script and camera capture are later tests. Layout analysis and large vision-language models are out of scope. The main beneficiaries are archives and digital-humanities projects that train a recogniser per collection from a few hundred transcribed lines, and low-resource scripts, including many Indian scripts, with many scans but few transcriptions.

# Problem Statement

Text recognisers fail on damaged documents, and damaged lines are exactly where labelled training data is scarcest. SSL can learn from unlabelled lines, but it must be told which variations to ignore, and today that choice is a hand-picked list of corruptions, re-tuned for every collection. **We derive that choice from the documents themselves:** model the main damage types physically, fit them to real historical lines, train with them, and test whether the learned invariance transfers to unseen damage, media and scripts, and whether it predicts where recognition fails.

Table: Research questions and how each can be shown wrong.
| | Question and claim | Wrong if |
|---|--------------------|----------|
| RQ1 | Does derived damage beat plain masking and hand-picked damage when few labels exist? Claim: it lowers the error on real historical lines. | The gap is within the run-to-run spread, or hand-picked damage matches it |
| RQ2 | What transfers? Claim: the benefit shrinks from unseen damage, to a new medium, to a new script. | Script transfer equals or beats damage transfer |
| RQ3 | Does a model's invariance to a damage predict how much it raises the error? Claim: invariance to paper-only damage helps; to damage on the strokes it does not. | One relationship holds for all damage types, or there is none |

# Literature Survey

**SSL for text recognition.** SeqCLR [@seqclr] introduced contrastive learning for text by contrasting parts of the feature sequence of two augmented views, and showed that augmentations which break the reading order (horizontal flips and crops) must be avoided. Lacuna Reconstruction [@lacuna] masks regions of historical lines and asks the model to find the true region among distractors; with 750,000 unlabelled lines it cut the error from 60.4% to 23.7% using only 30 labelled lines. Kišš and Hradiš [@kiss] showed that pretraining on unlabelled historical lines clearly beats training from scratch, but struggles to beat transfer from a related labelled dataset. LoGo-HTR [@logo] pretrains on about ten million word images with local contrastive and global decorrelation losses. A critical survey [@survey] finds no standard evaluation protocol and stresses that augmentations must suit text data, without giving a procedure for choosing them.

**Reconstruction and degradation.** Masked autoencoders [@mae] rebuild hidden image patches in pixel space, and for handwriting this family outperforms contrastive and joint-embedding methods [@garrido]. Text-DIAE [@textdiae] pretrains an autoencoder to undo masking, blur and background noise, and reports that the closer a pretext task is to the downstream task, the better the model; its degradations and strengths, however, are hand-picked. Augraphy [@augraphy] offers 26 document-damage effects and PreP-OCR [@prepocr] restores damaged pages before OCR; in both, which damage to use and how strong is left to the user.

**Fitting damage and measuring invariance.** Kanungo, Haralick, Baird and colleagues [@kanungo], [@baird07] fitted degradation models to real scans and validated them with nonparametric tests, for binary images and classical OCR. Ericsson et al. [@ericsson] measure how invariant a representation is to each augmentation, and Mintun et al. [@mintun] show that augmentations help most when they resemble the test corruptions. Table 3.1 summarises the closest work.

Table: Summary of the closest related work.
| Paper | Methodology | Result | Limitation for this project |
|--------------|--------------|------------|------------|
| Garrido-Munoz & Calvo-Zaragoza, NeurIPS 2026 [@garrido] | Six SSL methods compared on six HTR benchmarks | Pixel reconstruction best for handwriting | Fixed augmentation; no damage study |
| Penarrubia et al., IJCV 2025 [@survey] | Critical survey of SSL for text recognition | No standard protocol; augmentations must suit text | No procedure for choosing them |
| Kišš & Hradiš, ICDAR 2024 [@kiss] | Masked and joint-embedding pretraining on historical lines | Beats scratch; struggles against supervised transfer | Damage not studied |
| Vogler et al., NAACL Findings 2022 [@lacuna] | Masked-region pretraining with distractors | CER 60.4% → 23.7% with 30 labels | Corruptions not matched to real damage |
| Souibgui et al. (Text-DIAE), AAAI 2023 [@textdiae] | Autoencoder undoing masking, blur and noise | Degradation-invariant features | Degradations hand-picked |
| Ericsson et al., BMVC 2022 [@ericsson] | Per-augmentation invariance measurement | Tasks need different invariances | Natural images only |
| Mintun et al., NeurIPS 2021 [@mintun] | Augmentation–corruption similarity | Similarity predicts robustness | Augmentations not derived from data |
| Kanungo et al., TPAMI 2000 [@kanungo] | Validating degradation models on real scans | Statistically realistic synthetic pages | Binary images, classical OCR |
| Augraphy, 2023 [@augraphy]; PreP-OCR, ACL 2025 [@prepocr] | Synthetic document damage; restoration before OCR | Realistic damage; much lower OCR error | Which damage, how strong: left to the user |

# Research Gap

SSL helps text recognition when labels are scarce [@lacuna], [@kiss]; pixel reconstruction is the strongest family for handwriting [@garrido]; and what a model learns to ignore is decided by its corruptions [@ericsson], [@mintun]. Yet in every text-recognition method we found, the corruptions are chosen by hand [@textdiae], [@prepocr]. To our knowledge:

1. fitting degradation models to real scans is well established for classical OCR [@kanungo], [@baird07], but nobody has used the measured damage of real historical lines to **derive what a deep recogniser should learn to ignore** (which damage, how often, how strong), compared with hand-picked recipes on real damaged lines;
2. nobody has followed the chain **recipe → learned invariance → error on damaged lines** for text recognition, per damage type, including damage types, media and scripts held out of training.

**Challenges.** SSL may not beat supervised transfer [@kiss], so that baseline is always run. A model trained on synthetic damage may only learn its own simulator, so every claim is also tested on real damaged lines. Some damage has no clean physical model, so we model what physics allows (paper tone, show-through, blur) and mark the rest as approximate.

# Objectives

## Objectives of the project

1. A reproducible line-recognition pipeline with a fixed protocol and strong supervised baselines.
2. A per-line damage-measurement tool, and a study of how real historical lines differ from clean ones.
3. Physical damage models whose frequency and strength are **derived** from the measurements.
4. Training with the derived damage (as augmentation, consistency training and masked-autoencoder pretraining), compared with no damage, plain masking, hand-picked damage and a VICReg [@vicreg] control.
5. Transfer to a held-out damage type, a new medium and an unseen script.
6. Per-damage invariance of every model compared with the rise in error.

## Approach

The approach is a loop of five steps (Figure 5.1): **measure** damage statistics on real lines; **model** each damage type with a physical form and fitted parameters; **train** the recogniser to ignore the damage; **evaluate** on held-out damage, media and scripts; and **analyse** whether invariance predicts the error. The train step is climbed from the cheapest use of the damage to the most expensive: E1 augmentation (done in the pilot), E2 consistency training on unlabelled lines, E3 masked-autoencoder pretraining, and E4 a new dataset pair with different damage.

![The five-step approach. The derive step (measure, model and fit) is what distinguishes this project from hand-picked corruption recipes.](capstone/reviews/_kit/assets/img/approach_diagram.jpg){w=15.5}

# Overview of Datasets

## Description

Table: Datasets, their source, size and role.
| Dataset | Source and licence | Size | Role | Status |
|----------|----------|--------------|----------|--------|
| IAM-line [@iam] | Teklia on Hugging Face; IAM terms (research use) | 6,482 train / 976 validation / 2,915 test lines, 657 writers | Baseline, clean test, base for synthetic damage | Processed |
| CATMuS Medieval [@catmus] | Hugging Face, CC BY 4.0 | about 195,000 lines, 8th–16th century, about 10 languages | Real damage: measuring, training, testing | Subset processed |
| CATMuS subset used | Latin + French, 11 projects | 23,762 train / 1,243 validation / 4,022 test lines | As above | Processed |
| IIIT-INDIC-HW-WORDS | CVIT, IIIT Hyderabad | 872,000 word images, 8 Indian scripts | Unseen-script test | Planned |
| Muharaf | NeurIPS 2024 Datasets track | 36,311 Arabic lines; 1,216 of 1,644 pages public | Unseen-script test | Planned |

**IAM** is modern English handwriting on clean forms; we use the official writer-independent split. **CATMuS Medieval** gathers transcribed medieval manuscript lines from many projects. Its training split alone is 22.5 GB, so we took a Latin and French subset, the two languages that are large in both training and test splits, with shards chosen across 11 projects; its test lines come from manuscripts not seen in training. All lines are converted to grey-scale, resized to a height of 64 pixels and stored with Unicode NFC text. In 99% of CATMuS images the area outside the line polygon is painted pure black; we fill it with the local paper tone and store a mask of real pixels, so that the black frame is not measured as ink. Figure 6.1 shows sample lines.

![Sample lines from IAM (top two) and the CATMuS Latin and French subset (bottom three), with their transcriptions.](results/figures/samples_iam_catmus.png){w=10}

## Data attributes and features

Each record holds the line image (grey-scale, height 64 px), its transcription (Unicode NFC), a mask of real pixels (CATMuS), the original size, and provenance metadata (language, project, century, script type, shelfmark). Character sets are built from the training splits only: 79 characters for IAM and 195 for CATMuS, which keeps medieval abbreviation marks.

For every line, our measurement tool also computes eight features that describe its damage (Table 6.2). On 3,000 lines of each dataset, real medieval lines differ from clean ones mainly in **paper level** (darker paper) and **faint grey on the paper** (show-through), with two-sample Kolmogorov–Smirnov distances of 0.82 and 0.84 (0 = identical, 1 = no overlap). Contrast, sharpness and noise differ little. Stroke width and ink fraction also differ strongly, but because of pen and script, not damage. The pilot had fixed in advance that at least three damage features should reach D ≥ 0.5 (assumption A2); with two, this check narrowly failed, and we report it as such.

Table: Per-line damage features, the damage each tracks, and how strongly it separates CATMuS from IAM.
| Feature | Tracks | IAM median | CATMuS median | KS D |
|----------|----------|-----|-----|----|
| Paper level | paper tone | 0.980 | 0.804 | 0.82 |
| Faint grey on paper | show-through | 0.002 | 0.077 | 0.84 |
| Background unevenness | stains | 0.005 | 0.009 | 0.42 |
| Ink–paper contrast | fading | 0.478 | 0.408 | 0.26 |
| Sharpness | blur | 1.084 | 0.939 | 0.11 |
| Pixel noise | noise | 0.000 | 0.006 | 0.16 |
| Stroke width (px) | pen and scale, not damage | 3.33 | 4.81 | 0.73 |
| Ink fraction | script density, not damage | 0.119 | 0.260 | 0.94 |

# Conclusion of Capstone Project Phase-1

## Work completed

- **Literature survey and formulation:** research questions with stated conditions that would prove them wrong; the gap re-checked in November 2026, which narrowed the novelty from fitting damage to real scans (old [@kanungo]) to what a deep recogniser learns from it.
- **Data pipeline:** IAM and a 29,027-line CATMuS subset, cleaned (including the polygon-fill removal), normalised and split, with character sets from the training splits.
- **Damage-measurement tool:** eight per-line features, each checked to move steadily as its damage is added; real lines differ mainly in paper tone and show-through.
- **Damage models:** seven damage types, each a simple forward model with one physical parameter (paper tone, show-through, stains, noise, fading, blur, ink loss). Ink loss is held out of all training as unseen damage.
- **Derived damage recipe (first version):** for each damage type, a CATMuS line whose feature lies outside the range of clean IAM lines counts as damaged; the share of such lines sets how often the damage is applied, and their values, read back through a strength curve, set how strong (Table 7.1).

Table: Derived damage recipe compared with the usual hand-picked one.
| Damage type | Derived: share of lines | Derived: median strength | Hand-picked |
|------------|----------|------------|--------------|
| Paper tone | 84% | brightness × 0.80 | 50%, guessed range |
| Show-through | 89% | opacity 0.40 | 50% |
| Stain | 37% | depth 0.08 | 50% |
| Fading | 26% | contrast × 0.52 | 50% |
| Noise | 11% | σ ≈ 3.5 grey levels | 50% |
| Blur | 5% | σ ≈ 1.1 px | 50% |

## Pilot study

Before the review, we ran a one-week pilot to test the pipeline end to end and four assumptions, each with a pass/fail rule written down before the runs (Table 7.2).

**Setup.** The recogniser is a CRNN [@crnn]: a CNN, a two-layer bidirectional LSTM and CTC [@ctc], 7.4 million parameters, identical in every run. "Few labels" means only 1%, 5% or 10% of the training lines keep their text. *Pretraining* trains the CRNN's own CNN as a masked and denoising autoencoder: damage is added to an unlabelled line, 60% of its 8-pixel strips are hidden, and the CNN must rebuild the clean line (Figure 7.1); 30,244 unlabelled lines (CATMuS and IAM training lines, text discarded), 34 minutes. *Augmentation* (experiment E1) instead adds the damage to the labelled training lines, drawn afresh on every pass, with no pretraining (Figure 7.2). Each setting is repeated with two or three random seeds. A first 6.5-million-parameter vision transformer memorised the few labelled lines (60–75% CER) and was set aside.

![The pretraining task, with outputs of the derived-damage run: damaged input, input with 60% of the strips hidden, the model's rebuild, and the clean target.](capstone/reviews/_kit/assets/img/pilot/fig_pretrain_mask_rebuild.png){w=15}

Table: Pilot assumptions, rules fixed in advance, and outcomes.
| | Assumption | Rule | Outcome |
|---|----------|----------|---|
| A1 | Damage hurts a model trained on clean lines | At least 2 of 7 damage types double the error at medium strength | Pass (4 of 7) |
| A2 | Real damaged lines differ measurably from clean ones | At least 3 damage features with KS D ≥ 0.5 | Fail (2 of 3) |
| A3 | Pretraining beats training from scratch | Gain larger than the run-to-run spread (about 0.5 points) | Fail |
| A4 | Derived damage is at least as good as hand-picked damage in pretraining | Derived ≤ hand-picked in every setting | Pass (3 of 3) |

**Baselines.** The supervised CRNN reaches 9.8% CER on the IAM test set with all labels, trained in 50 minutes on a laptop GPU, against 11.4% for an off-the-shelf industrial recogniser (PaddleOCR PP-OCRv6 [@paddle]); on real medieval CATMuS lines the same recogniser gets 52.5% wrong, while our CRNN reaches 20.0%. With few labels the error climbs quickly (Table 7.3).

**Damage hurts (A1).** On clean IAM test lines with synthetic damage at medium strength, ink loss multiplies the baseline's error by 7.6, noise by 4.9, paper tone by 3.4 and blur by 3.1; show-through, fading and stains raise it by at most 1.4 times.

**Pretraining (A3, A4).** No pretrained version beats training from scratch by more than the run-to-run spread (Table 7.3). Derived damage is never worse than hand-picked damage (A4 passes), but only because hand-picked damage hurts; derived damage is no better than plain masking. Kišš and Hradiš [@kiss] found that pretraining beats scratch but struggles against supervised transfer; our pilot did not even beat scratch, most likely because of scale: 30,244 unlabelled lines for 34 minutes, against 750,000 lines in [@lacuna].

Table: Test CER of the CRNN (mean of two or three seeds; lower is better).
| Training | IAM 10% labels (648 lines) | IAM 1% (65 lines) | CATMuS 5% (1,188 lines) |
|--------------------|-------|-------|-------|
| From scratch | 19.9% | 43.3% | 33.8% |
| Pretrained, plain masking | 20.4% | 43.8% | 33.3% |
| Pretrained, hand-picked damage | 21.0% | 44.7% | 35.0% |
| Pretrained, derived damage | 20.5% | 43.9% | 33.4% |

![Augmentation: one real CATMuS training line, as it is, with two random draws of hand-picked and of derived damage, and after the clean-up filter.](capstone/reviews/_kit/assets/img/pilot/fig_aug_one_line.png){w=13}

**Damage as augmentation (E1).** Used as plain training augmentation, the derived damage lowers the error on real CATMuS test lines from 33.8% to 31.6% (three seeds; about three times the run-to-run spread), and the gain holds on the most damaged quarter of the test lines by each of three features (Table 7.4). Hand-picked damage gives 33.6%, and a clean-up filter that flattens the paper tone, with no learning, gives 33.0%. On clean IAM lines the two recipes tie (18.8% and 18.9%), since the derived recipe copies CATMuS damage that clean IAM lines do not have.

Table: Damage as training augmentation (test CER, mean of three seeds). The CATMuS quarters are the 25% most damaged test lines by the named feature.
| Training | IAM 10%, clean | CATMuS 5%, all | Darkest paper | Most show-through | Lowest contrast |
|--------------|-------|-------|-------|-------|-------|
| No augmentation | 19.9% | 33.8% | 35.6% | 35.7% | 39.4% |
| Hand-picked damage | 18.8% | 33.6% | 34.7% | 35.1% | 38.1% |
| Derived damage | 18.9% | 31.6% | 33.0% | 32.9% | 37.0% |
| Clean-up filter (control) | 19.8% | 33.0% | 35.0% | 34.7% | 38.2% |

**Limits.** The gain on the damaged quarters (2.4–2.8 points) is about the same as on all lines (2.2 points), so we claim that derived augmentation helps on CATMuS, not yet that its benefit is specific to damage; E4 tests this. The evidence is three seeds, one recogniser and one pair of datasets. **Lessons:** test the cheapest use of an idea first (augmentation worked where pretraining did not), and check every measurement against the images (the CATMuS polygon fill would otherwise have corrupted all damage features).

## Utility

The derived recipe concentrates on the paper-side damage that real medieval pages show, while a hand-picked recipe spends half of its corruptions on blur and noise, which the measurements show to be rare. The measurement tool and recipe turn the choice of corruptions, today a guess repeated for every collection, into a procedure any archive can run on a sample of its own pages. The current version has one known limitation: a difference between IAM and CATMuS also reflects script, pen and scanner, so Phase 2 fits a physical model per damage type.

# Plan of Work for Capstone Project Phase-2

Table: Phase 2 tasks (January – May 2027).
| Task | Months | Output |
|--------------------|-------|----------|
| Fitted physical damage models; a few hundred real test lines tagged by damage type | Jan – Mar | Damage recipe v1; tagged real test set |
| E1 extended (done in the pilot on CATMuS 5% and IAM 10%): more seeds and label budgets, invariance on CATMuS | Jan | Is the E1 gain robust? |
| E2: consistency training on unlabelled lines (clean and damaged views) | Jan – Feb | Does unlabelled data add to E1? |
| E3: one bounded retry of pretraining (ten times more unlabelled lines, gentler fine-tuning, a public pretrained encoder), with a fixed decision date | Feb – Mar | Go or stop on SSL pretraining |
| E4: a same-script dataset pair with different damage | Mar – May | Does the recipe follow the target's damage? |
| Held-out evaluation and supervised-transfer baseline | Apr – May | Answers to RQ1 and RQ2 |

Phase 3 (June – December 2027) covers the invariance–error analysis (RQ3), transfer to an unseen script and camera capture, and the paper and code release (Figure 8.1).

![Project timeline, September 2026 to December 2027 (Phase I blue, Phase II green, Phase III red).](capstone/reviews/_kit/assets/img/gantt.png){w=14}

Table: Planned effort by individual (tentative).
| Member | Owns | Phases |
|---------|----------------|----|
| Arvind Kothamangala | Data loaders, splits, supervised baselines, CER tooling | I – II |
| Atharv Sawarkar | Damage measurement, physical damage models, fitting, tagging real lines | I – II |
| Vignesh Nunna | Training with derived damage: E1, E2, E3 | I – III |
| Rohit Rajan | Evaluation: held-out tests, invariance scores, transfer | II – III |

::: references
:::

::: appendix
# Appendix A: Definitions, Acronyms and Abbreviations

Table: Definitions and acronyms.
| Term | Meaning |
|-----|-----------------|
| CER | Character error rate: character insertions, deletions and substitutions divided by the reference length |
| CTC | Connectionist temporal classification: a loss that trains a sequence model without character positions |
| HTR / OCR | Handwritten text recognition / optical character recognition |
| SSL | Self-supervised learning: learning from unlabelled data through a pretext task |
| MAE | Masked autoencoder: rebuilds hidden image patches from visible ones |
| VICReg | Variance–invariance–covariance regularisation, a joint-embedding SSL method |
| Invariance score | Similarity of a model's features for a clean line and its damaged copy (1 = damage ignored) |
| KS D | Two-sample Kolmogorov–Smirnov statistic: maximum distance between two cumulative distributions |
| NFC | Unicode normalisation form C |
| Held-out damage | A damage type never used in training, used only to test transfer |

# Appendix B: Key Code and How It Works

The pilot code is written in plain PyTorch and NumPy (package `lwti`, about 3,000 lines). This appendix shows the five pieces that carry the project's idea, shortened for reading (logging and argument handling removed), and explains each one. Table B.1 maps the main files to the steps of the approach in Figure 5.1.

Table: Main files of the pilot code and their role.
| File | Step | What it does |
|------------|------|--------------------|
| `lwti/data/prepare_catmus.py`, `common.py` | Data | Downloads the CATMuS subset, removes the black polygon fill, resizes to 64 px |
| `lwti/damage/measure.py` | Measure | Eight statistics per line (paper level, show-through, contrast, ...) |
| `lwti/damage/families.py` | Model | Seven damage forward models, each with one strength parameter |
| `lwti/damage/derive.py` | Fit | Derives how often and how strongly to apply each damage (B.1), and applies it (B.2) |
| `lwti/models/crnn.py`, `conv_mae.py` | Train | The CRNN recogniser and its masked-autoencoder pretraining (B.4) |
| `lwti/train/train_ctc.py`, `pretrain_mae.py` | Train | Supervised CTC training (with optional augmentation) and pretraining |
| `lwti/eval/robustness.py`, `invariance.py` | Evaluate, analyse | Error under synthetic damage; invariance score (B.5) |

## Deriving the damage recipe from real lines (the novel step)

This is the part that differs from existing work. Every SSL method for text needs a list of corruptions with a probability and a strength range; elsewhere these are chosen by hand. Here they are computed from the data.

```
def derive(src_stats, tgt_stats, curves):
    out = {}
    for fam in FAMILIES:                      # tone, fade, blur, noise, ...
        st, d = STAT[fam], DIRECTION[STAT[fam]]  # tone -> paper level, darker
        clean = src_stats[st].dropna()        # the statistic on clean IAM lines
        edge = clean.quantile(0.95 if d > 0 else 0.05)
        t = tgt_stats[st].dropna()            # the same statistic on real CATMuS lines
        hit = t[(t > edge) if d > 0 else (t < edge)]   # lines beyond the clean range
        p = invert(curves[curves.family == fam], hit.to_numpy())  # their strengths
        out[fam] = dict(prob=len(hit) / len(t),                    # how often
                        p_quantiles=np.quantile(p, np.linspace(0, 1, 21)))  # how strong
    return out
```

**How it works.** Before this function runs, `response_curves` adds each damage type to clean IAM lines at 11–15 strengths and records the median of its statistic, giving a curve from strength to measured value (for paper tone: how much the paper brightness drops). `derive` then (1) finds the range of the statistic on clean lines (the 5–95% band); (2) marks every real CATMuS line outside that band, in the direction of the damage, as damaged by this type; (3) converts each marked line's statistic back into a strength by reading the curve backwards (`invert`, a linear interpolation); and (4) stores the share of marked lines as the probability and 21 quantiles of their strengths as the strength distribution. The result for the pilot is Table 7.1: paper tone on 84% of lines and show-through on 89%, but blur on only 5%.

**Why it matters.** The recipe now follows the damage of the target collection. A different collection gives a different recipe with no manual tuning, and every number in it can be traced back to a measurement. The limitation (v0) is that a difference between IAM and CATMuS also contains script, pen and scanner differences; Phase 2 replaces the single curve per type with a physical fit.

## Applying a recipe: the corruption sampler

```
class CorruptionSampler:
    def strength(self, fam, rng):
        cfg = self.s[fam]
        if "p_quantiles" in cfg:              # derived: measured strengths
            q = np.asarray(cfg["p_quantiles"])
            return float(np.interp(rng.random(), np.linspace(0, 1, len(q)), q))
        lo, hi = cfg["p_range"]               # hand-picked: guessed range
        return float(rng.uniform(lo, hi))

    def __call__(self, g, rng):
        for fam in ORDER:                     # paper first, then ink, then capture
            cfg = self.s.get(fam)
            if cfg is None or cfg.get("held_out"):
                continue                      # ink loss is never used in training
            if rng.random() < cfg["prob"]:
                g = apply(g, fam, self.strength(fam, rng), rng)
        return g
```

**How it works.** The same sampler is used for pretraining and for augmentation, so the hand-picked and derived recipes differ only in their numbers, never in code. For each damage type in a fixed physical order (paper effects, then ink effects, then capture effects such as blur and noise), it flips a biased coin with the recipe's probability and, if it comes up, draws a strength. For the derived recipe the strength is drawn by inverse-transform sampling from the stored quantiles, so strengths follow the distribution measured on real lines; for the hand-picked recipe it is uniform in a range chosen by eye. Ink loss is marked `held_out` and skipped, which keeps it unseen for the transfer test (RQ2).

## A damage forward model: show-through

```
def showthrough(g, p, rng):
    """Verso text seen through the paper: mirrored, shifted, blurred, faint."""
    h, w = g.shape
    verso = g[:, ::-1]                                    # back page is mirrored
    verso = np.roll(np.roll(verso, rng.integers(-h // 4, h // 4 + 1), axis=0),
                    rng.integers(0, w), axis=1)  # misaligned with the front
    verso = cv2.GaussianBlur(verso, (0, 0), sigmaX=1.5)   # paper scatters light
    paper = paper_level(g)
    dark = (paper - verso).clip(0, None) * p              # p = opacity of the paper
    return np.minimum(g, paper - dark).clip(0, 255)       # ink can only darken
```

**How it works.** Each damage type is a small forward model of a physical process with one strength parameter `p`. Show-through follows the recto–verso mixing model of [@salerno]: the back page's text is mirrored, misaligned, blurred by the paper and attenuated by its opacity `p`, and it can only darken the front page (`np.minimum`). The other six types are written the same way: paper tone scales the paper level, fading compresses ink–paper contrast, stains add smooth low-frequency patches, blur is a Gaussian point-spread function, noise is additive sensor noise, and ink loss erases random parts of strokes.

## Pretraining: masked and denoising autoencoder on the recogniser's own CNN

```
def forward(self, x_in, x_clean):          # x_in = damaged line, x_clean = original
    B, _, H, W = x_in.shape
    m = (torch.rand(B, W // 8) < self.mask_ratio).float()      # hide 60% of 8-px strips
    m_px = m.repeat_interleave(8, dim=1)[:, None, None, :]
    f = self.cnn(x_in * (1 - m_px)).squeeze(2)                 # B x 384 x W/4 features
    pred = self.dec(f).transpose(1, 2)                         # predicted pixel columns
    err = ((pred - self.patchify(x_clean)) ** 2).mean(-1)  # vs the CLEAN line
    masked = m.repeat_interleave(2, dim=1)                     # per feature column
    return (err * masked).sum() / masked.sum() \
         + 0.25 * (err * (1 - masked)).sum() / (1 - masked).sum()
```

**How it works.** The encoder is exactly the CNN of the CRNN, so after pretraining its weights are copied into the recogniser without any change. A line is damaged by the sampler (B.2), then 60% of its 8-pixel vertical strips are blanked. The CNN turns the masked line into 384 numbers per 4-pixel column, and a small decoder predicts the pixels of every column. The target is the **clean** line, so the model must both fill in hidden strips (masked autoencoding, as in MAE [@mae]) and remove the damage (denoising). The loss is the mean squared error on hidden columns plus a quarter-weighted error on visible columns, which forces the visible part to be cleaned too. With no damage, this is plain masking; with the hand-picked or derived recipe, it becomes the pretraining compared in Table 7.3.

## The invariance score

```
def invariance(model, df, device):
    clean = pooled_features(model, loader(df, damage=None))   # 500 lines x 384
    mu, sd = clean.mean(0), clean.std(0) + 1e-6
    z0 = (clean - mu) / sd                                    # standardise each feature
    out = {}
    for fam in FAMILIES:
        for level in range(3):                                # low, medium, high
            dmg = pooled_features(model, loader(df, damage=fixed(fam, level)))
            z = (dmg - mu) / sd                               # same scaling as clean
            out[(fam, level)] = F.cosine_similarity(z0, z, dim=1).mean().item()
    return out
```

**How it works.** For 500 test lines, the model's CNN features (384 numbers per column, averaged along the line) are computed once for the clean line and once for the same line with one damage at a fixed strength. Each feature is standardised with the clean lines' mean and spread, so that no single large feature dominates, and the cosine similarity between the clean and damaged vectors is averaged over the lines. A score of 1 means the damage did not change the model's internal representation at all: the model ignores it. One score per damage type and strength (7 × 3 = 21) is then compared with the rise in error under the same damage, which is the analysis behind RQ3; the measure follows the style of Ericsson et al. [@ericsson].
:::
