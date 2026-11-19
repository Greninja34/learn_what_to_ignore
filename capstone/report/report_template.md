<!--
Phase-1 report, TEMPLATE-ONLY version (no pilot run), cut to the department template and 20-25 pages in total.
Build: python capstone/report/build_pandoc.py --pdf --src report_template.md --name Team147_Phase1_Report_template
The previous 33-page version is in git history.
-->

::: abstract
Text recognisers fail on damaged documents (faded ink, ink showing through from the back of the page, stains, darkened parchment), and these are exactly the collections with the fewest transcribed lines. Self-supervised learning (SSL) can learn from unlabelled lines by rebuilding a line from a corrupted copy, but the corruptions it learns to ignore are chosen by hand and re-tuned for every collection. This project, *Learning What to Ignore*, replaces that guess with a measurement: we measure the damage on real historical lines, model each damage type physically, derive how often and how strongly to apply it, and train the recogniser with this derived damage. We test whether it beats hand-picked damage when labels are few, whether the benefit transfers to unseen damage, media and scripts, and whether a model's invariance to a damage predicts how much that damage raises its error. In Phase 1 we completed the literature survey and the formulation; acquired and processed IAM (modern English handwriting) and a Latin and French subset of CATMuS Medieval (29,027 real manuscript lines from 11 projects); built a tool that measures eight damage statistics per line; showed that real medieval lines differ from clean ones mainly in paper tone and show-through; and derived a first damage recipe from these measurements.
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

The approach is a loop of five steps (Figure 5.1): **measure** damage statistics on real lines; **model** each damage type with a physical form and fitted parameters; **train** the recogniser to ignore the damage; **evaluate** on held-out damage, media and scripts; and **analyse** whether invariance predicts the error. The train step is climbed from the cheapest use of the damage to the most expensive: E1 augmentation, E2 consistency training on unlabelled lines, E3 masked-autoencoder pretraining, and E4 a new dataset pair with different damage.

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

For every line, our measurement tool also computes eight features that describe its damage (Table 6.2). On 3,000 lines of each dataset, real medieval lines differ from clean ones mainly in **paper level** (darker paper) and **faint grey on the paper** (show-through), with two-sample Kolmogorov–Smirnov distances of 0.82 and 0.84 (0 = identical, 1 = no overlap). Contrast, sharpness and noise differ little. Stroke width and ink fraction also differ strongly, but because of pen and script, not damage.

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

## Utility

The derived recipe concentrates on the paper-side damage that real medieval pages show, while a hand-picked recipe spends half of its corruptions on blur and noise, which the measurements show to be rare. The measurement tool and recipe turn the choice of corruptions, today a guess repeated for every collection, into a procedure any archive can run on a sample of its own pages. The current version has one known limitation: a difference between IAM and CATMuS also reflects script, pen and scanner, so Phase 2 fits a physical model per damage type.

# Plan of Work for Capstone Project Phase-2

Table: Phase 2 tasks (January – May 2027).
| Task | Months | Output |
|--------------------|-------|----------|
| Fitted physical damage models; a few hundred real test lines tagged by damage type | Jan – Mar | Damage recipe v1; tagged real test set |
| E1: derived damage as training augmentation, against no damage, hand-picked damage and a clean-up control; baselines at 1%, 10% and 100% of labels | Jan | Does derived damage lower the error on real lines? |
| E2: consistency training on unlabelled lines (clean and damaged views) | Jan – Feb | Does unlabelled data add to E1? |
| E3: masked-autoencoder pretraining with the derived damage, with a fixed decision date | Feb – Mar | Go or stop on SSL pretraining |
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
:::
