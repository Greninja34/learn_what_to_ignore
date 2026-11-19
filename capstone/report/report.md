<!--
Source of the Phase-1 report. Build (research2 env), from research/:
  python capstone/report/build_pandoc.py --pdf     LaTeX PDF only (LuaTeX)
  python capstone/report/build_pandoc.py           .docx and PDF
Trimmed on 16 Nov 2026 so that chapters 1-8 fit in about 23 pages; the untrimmed text is in git (dbe52d6).
Syntax:
  # Title            chapter (new page, "CHAPTER n" line + centred title)
  ## Title           section n.m        ### Title   subsection n.m.k
  - item            bullet              1. item     numbered item
  Table: caption    caption line placed directly before a pipe table; the number of dashes per
                    column in the |---| row sets the relative column widths in the PDF
  ![caption](path)  figure (path relative to research/); optional {w=14} width in cm after it
  [@key]            citation -> [n], numbered in order of first use (keys in build_report.py BIB)
  **bold**  *italic*   ⟦text⟧ = yellow highlight (to fill / to check)
-->

::: abstract
Text recognisers read clean scans well but fail on damaged documents (faded ink, ink showing through from the back of the page, stains, darkened parchment), and damaged collections are also where transcribed training data is scarcest. Self-supervised learning (SSL) can learn from unlabelled text lines by training a model to rebuild a line from a corrupted copy, but the corruptions it is trained to see through are chosen by hand and re-tuned for each collection, even in the strongest recent work. This project, *Learning What to Ignore*, replaces that guess with a measurement: we measure the damage on real historical lines, model the main damage types with simple physical forward models, fit their parameters to the measurements, and pretrain a masked autoencoder that reconstructs clean lines from lines damaged in this derived way. We then ask whether the derived corruptions beat plain masking and hand-chosen corruptions when few labels are available, which kinds of new damage, media and scripts the learned invariance transfers to, and whether a model's measured invariance to a damage type predicts how much that damage raises its error. In Phase 1 we completed the literature survey and formulation, built the data pipeline for IAM (modern English handwriting) and a Latin and French subset of CATMuS Medieval (29,000 real manuscript lines from 11 projects), trained a supervised CRNN baseline that reaches 9.8% character error rate on the IAM test set (an off-the-shelf industrial recogniser reaches 11.4% on the same lines), built a tool that measures eight damage statistics per line, derived a first corruption setting from it, and ran the first pretraining loop end to end. In the pilot, pretraining the recogniser's own CNN with a convolutional masked autoencoder did not beat training from scratch at this scale (33.4% against 33.8% character error rate with 5% of the CATMuS labels), but using the same derived damage as plain training augmentation lowered the error on real medieval test lines from 33.8% to 31.6% (three seeds), including on the most damaged quarters of the test set; hand-picked damage gave 33.6%.
:::

# Introduction

## Background

Optical character recognition (OCR) converts images of text into machine-readable characters. On clean printed scans it is close to a solved problem, and line-level handwritten text recognition (HTR) reaches character error rates of a few percent on benchmarks such as IAM [@iam]. These systems are, however, trained and evaluated mostly on clean material. Libraries, archives and record rooms hold millions of pages whose ink has faded, whose back-side text shows through, whose paper or parchment has darkened or is stained, or that were captured with uneven light or a phone camera. On such pages accuracy drops sharply, and these are also the collections for which almost nobody has transcribed enough lines to train a model.

The usual way around the shortage of labels is self-supervised learning (SSL): a model is first trained on a pretext task that needs no labels, such as rebuilding a line image from a copy with parts hidden or corrupted, and is then fine-tuned with a few transcribed lines. SSL for text recognition is an active field [@survey], with contrastive [@seqclr], masked-prediction [@kiss] and reconstruction-based [@textdiae], [@garrido] methods.

## Motivation: what should a model learn to ignore?

Through its pretext task, every SSL method decides which variations the model should become insensitive to: a contrastive method treats two augmented views of an image as "the same", a denoising autoencoder a corrupted line and its clean version. What the model learns to ignore is therefore set by the corruptions the designer picks. In general vision, different downstream tasks need different, sometimes opposite, invariances [@ericsson], and robustness to a corruption depends on how similar the training augmentations are to it [@mintun].

For text recognition this choice is still made by hand. A critical survey notes that augmentations are chosen to fit the data, without a procedure [@survey]; Text-DIAE picks its degradations by hand [@textdiae]; and the most recent large comparison of SSL methods for handwriting (NeurIPS 2026) uses "a fixed augmentation pipeline" whose blur, noise and contrast changes are described only as "small", "mild" or "low", with no ranges and no selection procedure [@garrido]. That paper also shows that pixel-reconstruction pretraining (masked autoencoders) clearly outperforms contrastive and joint-embedding methods for handwriting, because the information that separates characters lies in high-variance pixel directions. The open question therefore becomes: when a reconstruction model is trained to rebuild clean lines from damaged ones, *which damage* should it be shown, and can that choice be derived from the documents themselves instead of guessed?

## Scope of the work

The project studies the recognition of single text lines already cut out of the page; layout analysis and line segmentation are left out, because their errors would blur the comparison between pretraining methods. The recogniser is kept small (5 to 25 million parameters), so that differences can be attributed to the pretraining and the method stays usable by an archive with modest hardware. We model three to seven physically describable damage types and evaluate on modern handwriting (IAM), real historical manuscripts (CATMuS Medieval [@catmus]) and, in later phases, an unseen script and camera-captured text. Large vision-language models and many languages at once are out of scope.

## Who benefits

- **Archives, libraries and digital humanities projects**, which today train a recogniser per collection from a few hundred transcribed lines: if damage derived from a collection's own pages lowers the error, fewer lines must be transcribed and no corruption recipe has to be tuned by trial and error.
- **Low-resource scripts**, including many Indian scripts, with many scanned manuscripts but very few transcribed lines, where learning mostly from unlabelled pages is the only route that scales.
- **Practitioners planning a transcription effort**: if measured invariance predicts which damage hurts a model, a sample of pages is enough to decide where to spend the labelling budget.
- **SSL researchers**, by turning the choice of corruptions from a guess into a measurement procedure that can be checked.

## Organisation of the report

Chapter 2 states the problem, research questions and hypotheses; Chapter 3 surveys the literature; Chapter 4 identifies the research gap and the challenges in closing it; Chapter 5 lists the objectives and the approach; Chapter 6 describes the datasets, their preprocessing and the damage they contain; Chapter 7 summarises the Phase 1 work and preliminary results; and Chapter 8 gives the plan for Phase 2. Appendix A defines the terms used, and Appendix B shows and explains the key parts of the code.

# Problem Statement

## Problem statement

Text recognisers fail on damaged documents (faded ink, bleed-through, stains, poor scans), and damaged lines are exactly where labelled training data is scarcest. SSL can learn from unlabelled lines, but it must be told which variations to ignore, and today that choice is a hand-picked list of corruptions, re-tuned for every new collection. Since reconstruction pretraining now outperforms contrastive methods for handwriting [@garrido], the question becomes which damage a reconstruction model should learn to see through.

**We derive that choice from the documents themselves:** model the main damage types physically, fit them to real historical lines, pretrain with them, and test whether the learned invariance transfers to unseen damage, media and scripts, and whether it predicts where recognition fails.

## Research questions

- **RQ1. Does it help?** Do physics-derived, data-fitted corruptions beat plain masking and hand-chosen corruptions when few labelled lines are available?
- **RQ2. What transfers?** Does the benefit carry over to a damage type held out of pretraining, to a new writing medium, and to an unseen script, and in which order does it shrink?
- **RQ3. What governs the match?** Does a model's measured invariance to a damage type predict how much that damage increases its character error rate?

## Hypotheses

Each hypothesis states in advance what would show it to be wrong (Table 2.1).

Table: Falsifiable hypotheses.
| | Hypothesis | Wrong if |
|---|--------------------|----------|
| H1 | Derived corruptions lower the character error rate on real historical lines at the smallest label budget, compared with both plain masking and hand-chosen corruptions. | The gap is within the seed-to-seed spread, or hand-chosen corruptions match it. |
| H2 | Transfer shrinks as conditions move away from what was fitted: held-out damage, then a new medium, then a new script. | Script transfer equals or beats damage transfer. |
| H3 | Invariance helps when a damage type leaves the character-carrying pixels alone (paper tone, show-through, stains) and hurts when it overlaps them (ink loss, merged strokes): a sign flip between the two groups. | One monotone relationship across all families, or no correlation. |
| H4 (control) | A joint-embedding model (VICReg [@vicreg]) trained on the same derived damage loses to the derived-corruption masked autoencoder, reproducing [@garrido] at small scale. | VICReg matches or beats it. |

# Literature Survey

This chapter reviews the work the project builds on, grouped by the question each line of work answers; Table 3.1 at the end summarises the closest papers by methodology, result and limitation.

## Self-supervised learning for text recognition

**Critical survey (Penarrubia, Valero-Mas and Calvo-Zaragoza, IJCV 2025)** [@survey]. Organises SSL methods for text recognition into contrastive, masked-prediction and generative families. Its main finding for us is methodological: methods are rarely compared under the same conditions, protocols (image height, character set, label budgets) differ, and augmentations are chosen per dataset without a stated procedure. We therefore fix the protocol on day one and treat the choice of corruptions as a research question rather than a setting.

**Contrastive methods.** SeqCLR (CVPR 2021) [@seqclr] contrasts horizontal windows of the feature maps of two augmented views, improved few-label recognition on handwriting and scene text, and established that contrastive SSL is viable for text. LoGo-HTR (WACV 2026) [@logo] pretrains with local and global contrastive objectives and reports clear gains with scarce labels. In both, the invariances are set entirely by hand-picked augmentations, damage is not studied, and both belong to the family that [@garrido] finds weaker than reconstruction for handwriting.

**Self-supervised pre-training of text recognisers (Kišš and Hradiš, ICDAR 2024)** [@kiss]. Pretrains recognisers on large unlabelled historical collections with masked feature prediction (public code). Pretraining helps, but pretraining on the target domain does not consistently beat simple supervised transfer from a related labelled dataset. This makes supervised transfer a mandatory baseline and is the main risk we track.

**Lacuna reconstruction (Vogler et al., NAACL Findings 2022)** [@lacuna]. Masks regions of a historical line and asks the model to pick the true region among distractors from the same line. Pretrained on 750,000 unlabelled lines, it reduced the character error rate on an Arabic-script manuscript collection from 60.4% to 23.7% with only 30 labelled lines: masked pretraining can matter a great deal at very low label budgets, given a large unlabelled pool.

## Reconstruction versus joint-embedding objectives

**Masked autoencoders (He et al., CVPR 2022)** [@mae] encode a random 25% of image patches and reconstruct the hidden 75% in pixel space; this simple, scalable objective is the one our pretraining builds on. Joint-embedding methods such as VICReg [@vicreg] and I-JEPA [@ijepa] instead align or predict features, not pixels.

## Degradation-aware pretraining and document degradation

**Text-DIAE (Souibgui et al., AAAI 2023)** [@textdiae]. A degradation-invariant autoencoder pretrained with masking, blur and background-noise pretext tasks and used for recognition and document enhancement: the closest prior work on degradation invariance. Its degradations and strengths are chosen by hand, and its ablations found masking the most useful task while added noise did not help, which suggests that the choice of degradations matters and is not obvious.

**Simulating and removing damage.** Augraphy [@augraphy] is a library of hand-designed document degradations (ink bleed, bleed-through, low ink, noise textures, JPEG artefacts, shadows), so our novelty cannot lie in simulating damage, only in *deriving* which damage to simulate and how strongly. PreP-OCR [@prepocr] restores degraded images with a model trained on hand-set synthetic degradations and post-corrects the OCR output; it restores before OCR rather than pretraining a recogniser. Salerno and Tonazzini [@salerno] model show-through and bleed-through as the front-side text mixed with a mirrored, attenuated back side; our show-through family follows this forward model.

## Invariance and transfer

Ericsson, Gouk and Hospedales (BMVC 2022) [@ericsson] measure how invariant a pretrained representation is to each augmentation (the similarity of the features of an image and its transformed copy) and show that different downstream tasks benefit from different, sometimes opposite, invariances. We use this measurement for RQ3; it has not been applied to text recognition or document damage. Mintun, Kirillov and Xie (NeurIPS 2021) [@mintun] show, for natural images and supervised training, that robustness to a test-time corruption depends on how perceptually similar the training augmentations are to it, which motivates matching training corruptions to real damage; they neither derive the augmentations from data nor study text.

## Fitting degradation models to real data

**Document degradation models (Kanungo, Haralick, Baird and colleagues, 1994–2007)** [@kanungo], [@baird07]. Long before deep learning, this line of work modelled how printing and scanning degrade a page (pixel flips near stroke edges, blur, thresholding, morphological thickening), estimated the parameters from real page images, and used the fitted models to generate synthetic training sets with ground truth. Kanungo et al. turned "does this degradation model match real scans?" into a nonparametric two-sample permutation test [@kanungo], and Baird's 2007 review lists comparing degradation models and the sound use of synthetic data as open problems [@baird07]. This is the root of our "measure, model and fit" step, so fitting damage to real documents is not new; but it targeted binary images and classical OCR, and did not ask what a learned recogniser should be trained to ignore, nor whether the invariance it acquires predicts its errors.

Two 2026 works fit synthetic corruption to real data at the level of *text*, not images: the ICDAR 2026 HIPE-OCRepair competition generates OCR errors from character confusion matrices estimated on its data [@hipe], and a retrieval-augmented restoration method for historical Korean documents samples its corruption rate to match the real damage distribution [@hanja]. Neither concerns image damage or recogniser training. "Fit the corruption to the data" is thus an established idea; our contribution lies in what a deep recogniser learns from the fitted damage and whether that can be measured.

## Summary of the most relevant papers

Table: Summary of the closest related work.
| Paper | Methodology | Result | Limitation for this project |
|--------------|--------------|------------|------------|
| Garrido-Munoz & Calvo-Zaragoza, NeurIPS 2026 [@garrido] | Six SSL methods, one ViT-B encoder, six HTR benchmarks; pixel-variance analysis | MAE best: 5.5% mean CER (frozen), 8.8% at 10% labels | Hand-picked, unquantified augmentation; no damage study |
| Penarrubia et al., IJCV 2025 [@survey] | Critical survey of SSL for text recognition | Protocols inconsistent; augmentations chosen ad hoc | No method proposed for choosing them |
| Kišš & Hradiš, ICDAR 2024 [@kiss] | Masked pretraining on unlabelled historical lines | Gains from pretraining; public code | Target-domain SSL not always better than supervised transfer |
| Souibgui et al. (Text-DIAE), AAAI 2023 [@textdiae] | Autoencoder with masking, blur and noise pretext tasks | Degradation-invariant features for recognition and enhancement | Degradations and strengths hand-picked |
| Vogler et al. (Lacuna), NAACL Findings 2022 [@lacuna] | Masked-region pretraining with distractors | CER 60.4% → 23.7% with 30 labels | Not about matching real damage |
| Mitra et al. (LoGo-HTR), WACV 2026 [@logo] | Local–global contrastive pretraining, then fine-tuning | Gains with scarce labels | Contrastive family; no damage study |
| Ericsson et al., BMVC 2022 [@ericsson] | Per-augmentation invariance measurement | Tasks need different invariances | Natural images only; not text |
| Mintun et al., NeurIPS 2021 [@mintun] | Augmentation–corruption similarity | Similarity predicts robustness | Supervised, natural images; augmentations not derived |
| Kanungo et al., TPAMI 2000 [@kanungo] | Fit and validate degradation models against real scans with permutation tests | Synthetic pages statistically close to real ones | Binary images and classical OCR; not what a deep model learns to ignore |
| Groleau et al. (Augraphy), 2022 [@augraphy] | Library of document degradations | Realistic synthetic damage | Which damage, how strong: left to the user |
| Guan et al. (PreP-OCR), ACL 2025 [@prepocr] | Restoration trained on synthetic damage + language-model post-correction | CER 63.9–70.3% lower on 13,831 historical pages | Hand-set damage; restoration, not pretraining |

# Research Gap

The literature establishes that self-supervised pretraining helps text recognition when labels are scarce [@lacuna], [@kiss], [@logo]; that for handwriting pixel reconstruction clearly beats contrastive and joint-embedding objectives [@garrido]; and that what a model learns to ignore is decided by its corruptions [@ericsson], with robustness depending on how well these match the test-time damage [@mintun]. What has not been done is to bring these together for damaged text. In every text-recognition method we found, including the strongest recent one [@garrido] and the degradation-aware ones [@textdiae], [@prepocr], the corruptions are chosen by hand. To our knowledge (as of November 2026; "not found" is not "proven absent", and the search continues through Phase 2):

1. fitting degradation models to real scans is well established for classical OCR [@kanungo], [@baird07], and corruption has recently been fitted to data for text-level OCR errors [@hipe], [@hanja]; but nobody has used the measured damage of real historical lines to **derive what a deep recogniser should learn to ignore** (which corruptions, how strong), compared with hand-picked recipes on real damaged lines;
2. nobody has followed the chain **recipe → learned invariance → robustness** for text recognition: measured, per damage type, whether a recogniser's invariance predicts its rise in error, including on unseen damage types or scripts.

Table 4.1 lists the practical challenges in closing the gap and how the project handles each.

Table: Challenges in closing the gap and how we handle them.
| Challenge | How we handle it |
|-------------|-----------------|
| SSL may not beat supervised transfer [@kiss] | Always run that baseline; the invariance analysis (RQ3) is a result either way |
| "You only learned your own simulator" | Always also test on real damaged lines, tagged by damage type |
| Some damage has no clean physical model | Model what physics allows (paper tone, show-through, stains, blur); label the rest approximate |
| Statistics also differ because of script, pen and resolution; test data could leak into the fit | Fit only damage statistics (not scale or script ones), only on pretraining data; official writer-independent splits |
| Protocols differ between papers [@survey]; other groups work in this area | Fix image height, character set and Unicode normalisation from day one; move fast: workshop paper first |

# Objectives

## Objectives of the project

1. Build a reproducible pipeline for line-level text recognition on modern and historical handwriting, with a fixed protocol (line height, character set, Unicode NFC normalisation, official splits) and strong supervised baselines.
2. Build a tool that measures, for every line, statistics describing its damage, and use it to characterise how real historical lines differ from clean ones.
3. Model the main damage types with simple physical forward models and **derive** their frequency and strength from the measured statistics.
4. Train the recogniser with the derived corruptions, in increasing order of cost: as training augmentation, as consistency training on unlabelled lines, and as masked-autoencoder pretraining; compare each with no corruption, hand-chosen corruptions and simple controls (RQ1, H1, H4).
5. Evaluate transfer to a damage type held out of pretraining, a new medium and an unseen script (RQ2, H2).
6. Measure per-damage invariance of every model and test whether it predicts the increase in character error rate (RQ3, H3).
7. Release the code, the fitted damage settings and a set of real lines tagged by damage type.

## Approach

The approach is a loop of five steps (Figure 5.1): **measure** damage statistics on real lines; **model and fit** each damage type; **train** the recogniser with the derived damage; **evaluate** on held-out damage, media and scripts; and **analyse** whether invariance predicts the error. The first loop is deliberately simple (a supervised baseline, then plain masked reconstruction), and each later loop adds one element chosen by what the previous one showed. The research questions, hypotheses, held-out tests, baselines and reporting protocol are fixed from the start; the damage types, model size, masking ratio and label budgets are decided by evidence.

The **train** step is climbed as a ladder, from the cheapest use of the derived damage to the most expensive, each rung compared with no corruption and with hand-chosen corruption under one recogniser and one set of training settings:

1. **E1, augmentation (done in the pilot):** train the CRNN on labelled lines damaged with the derived recipe;
2. **E2, consistency training:** on unlabelled lines, train the CRNN with CTC to give the same output for a clean and a damaged view;
3. **E3, one bounded attempt to rescue SSL pretraining:** masked-autoencoder pretraining with protocol fixes, a ten times larger unlabelled pool and a public pretrained encoder, stopped at a fixed decision date;
4. **E4, a new dataset pair:** the same script with different damage, to test whether the derived recipe tracks the damage of the target.

The pilot's pretraining variants (plain masking, hand-chosen and derived damage) remain in the comparison; supervised transfer from a related labelled dataset and an off-the-shelf recogniser are the outside reference points.

![The five-step approach. The derive step (measure, model and fit) is what distinguishes this project from hand-picked corruption recipes.](capstone/reviews/_kit/assets/img/approach_diagram.jpg){w=15.5}

# Overview of Datasets

## Description

The project needs clean labelled handwriting for baselines and as the base onto which damage is applied; real damaged historical lines for measuring damage, unlabelled pretraining and testing; and held-out scripts and media for transfer. Table 6.1 lists the datasets; everything used in Phase 1 is free for research and was downloaded and processed in the project's pipeline.

Table: Datasets, their source, size and role.
| Dataset | Source and licence | Size | Role in the project | Status |
|----------|----------|--------------|----------|--------|
| IAM-line [@iam] | Teklia on Hugging Face; original IAM terms (research use) | 10,373 lines: 6,482 train / 976 validation / 2,915 test (writer-independent) | Supervised baseline, clean test, base for synthetic damage | Downloaded, processed |
| CATMuS Medieval [@catmus] | Hugging Face, CC BY 4.0 | 194,808 lines in total (152,816 / 19,402 / 22,590), many languages | Measuring real damage, unlabelled pretraining, real-damage test | Latin + French subset processed |
| CATMuS subset used | Selected by us (11 projects in train, 6 in test) | 23,762 train / 1,243 validation / 4,022 test lines (test: 3,003 Latin, 1,019 French) | As above | Processed |
| IIIT-INDIC-HW-WORDS | CVIT, IIIT Hyderabad | 872,000 word images, 8 Indian scripts | Unseen-script test (Phase 3) | Planned |
| Muharaf | NeurIPS 2024 Datasets track | 36,311 Arabic manuscript lines in total; 1,216 of 1,644 pages public | Unseen-script test (Phase 3) | Planned |
| Scene text (IIIT5k, IC13, IC15) | Public benchmark bundles | Several thousand words | Camera-capture test (Phase 3) | Planned |

**IAM** contains modern English handwriting by 657 writers on clean white forms; we use Teklia's line-level version with the official writer-independent split, so no writer of a test line is seen in training. **CATMuS Medieval** gathers transcribed medieval manuscript lines from many projects, centuries, scripts and languages. Its training split alone is 22.5 GB, so we selected a Latin and French subset: the only two languages that are large in both the training and test splits, which keeps the character set manageable and the test set matched to the training data. Shards were chosen round-robin over projects so that the subset covers 11 collections. Figure 6.1 shows sample lines.

![Sample lines from IAM (top two) and the CATMuS Latin and French subset (bottom three), with their transcriptions. CATMuS keeps medieval abbreviation marks.](results/figures/samples_iam_catmus.png){w=10.5}

## Data attributes and features

Each processed record contains a line image, its transcription and metadata (Table 6.2).

Table: Attributes of a processed line record.
| Attribute | Type | Description |
|------------|--------|--------------------|
| id | string | Unique line identifier (dataset, split, shard, index) |
| text | string | Transcription, Unicode NFC, whitespace collapsed |
| png | image | Grey-scale line image, height 64 px, aspect ratio kept, width at most 2048 px |
| valid | image (CATMuS) | Mask of real pixels (0 where the original was polygon fill) |
| w, h0, w0 | integers | Width after resizing; original height and width |
| language, project, century, script_type, shelfmark, genre | strings (CATMuS) | Provenance metadata used for stratified analysis |

The character sets are built from the training splits only: 79 characters for IAM and 195 for the CATMuS subset, which keeps medieval abbreviation marks and special letters (for example the Tironian *et* and macrons over letters). Characters that appear only in validation or test lines remain in the reference text, so they count as errors.

## Preprocessing

All lines are converted to grey-scale, resized to a height of 64 pixels with the aspect ratio kept, and stored with their transcription in Unicode NFC form. During preprocessing we found that **99% of CATMuS line images have the area outside the line's polygon painted pure black**, about 15% of each image on average. Left untreated, this black frame is read as ink by any measurement and creates artificial grey edges. We therefore detect the black pixels connected to the image border at full resolution, fill them with the local paper tone, and store a mask of real pixels with every line (Figure 6.2). All damage measurements use only real pixels, with a 3-pixel margin from the former polygon edge.

![Removing the polygon fill from CATMuS lines. In each group: the original line, the cleaned line, and the mask of real pixels (white).](results/figures/unmask_examples_short.png){w=9.5}

## Exploratory analysis: how real damage differs from clean lines

The measurement tool computes eight statistics for every line, on the same normalised images that the models see. Ink and paper are separated with Otsu's threshold on a lightly smoothed copy, so pixel noise is not counted as ink. Figure 6.3 compares their distributions on 3,000 IAM and 3,000 CATMuS training lines, and Table 6.3 defines each statistic and gives the separation as the two-sample Kolmogorov–Smirnov statistic D (0 = identical, 1 = no overlap).

![Distributions of the eight statistics for IAM (outline) and CATMuS (fill).](results/figures/fig1_stats_iam_vs_catmus.png){w=13.5}

Table: Per-line statistics, what they reflect, and how strongly they separate real historical lines from clean lines.
| Statistic | Definition (what it reflects) | IAM median | CATMuS median | KS D |
|----------|--------------------|-----|-----|----|
| Paper level | Median paper intensity / 255 (darkened paper or parchment) | 0.980 | 0.804 | 0.82 |
| Faint grey on paper | Share of paper pixels that are faintly grey (show-through, bleed-through) | 0.002 | 0.077 | 0.84 |
| Background unevenness | Std. dev. of the large-scale paper level (stains, uneven light) | 0.005 | 0.009 | 0.42 |
| Ink–paper contrast | (paper − ink level) / 255 (faded ink) | 0.478 | 0.408 | 0.26 |
| Sharpness | Laplacian variance / contrast² (blur) | 1.084 | 0.939 | 0.11 |
| Pixel noise | Robust std. dev. of the high-pass residual on paper (noise) | 0.000 | 0.006 | 0.16 |
| Stroke width (px) | 2 × ink area / ink perimeter (pen and scale, not damage) | 3.33 | 4.81 | 0.73 |
| Ink fraction | Share of pixels classified as ink (script density, not damage) | 0.119 | 0.260 | 0.94 |

**Do real damaged lines differ measurably from clean ones (pilot assumption A2)?** Only partly. Two damage statistics separate the datasets strongly: the paper of the historical lines is much darker (D = 0.82), and far more of it is faintly grey (D = 0.84), consistent with show-through and parchment texture. Background unevenness differs moderately (0.42); contrast, sharpness and noise differ little. We had fixed in advance that the "derive" step is meaningful if at least three damage statistics separate with D ≥ 0.5; with two, this pilot criterion is narrowly not met, and we report it as such. The finding is still informative: real medieval damage is concentrated in paper-side effects (tone, show-through), not in the blur and noise that hand-picked recipes emphasise, and the derived setting reflects that (Table 7.1). Stroke width and ink fraction also differ strongly, but reflect the tighter cropping and denser script of the manuscripts, not damage, and are not used for fitting.

# Conclusion of Capstone Project Phase-1

## Work completed

Phase 1 set out to complete the literature survey and formulation, the data pipeline, a supervised baseline, the damage-measurement tool and the first pretraining loop. All five are done:

- **Literature survey and formulation**, updated in November 2026 with a full reading of [@garrido] and a search of 2026 work; the research gap was re-confirmed.
- **Data pipeline**: IAM and a 29,000-line Latin and French subset of CATMuS Medieval, cleaned (including the removal of polygon fill), normalised and stored with metadata, fixed splits and character sets.
- **Supervised baseline**: a CRNN [@crnn] (convolutional layers, a two-layer bidirectional LSTM and CTC [@ctc], 7.4 million parameters) trained on IAM.
- **Damage-measurement tool**: eight per-line statistics, validated by checking that each synthetic damage type moves its statistic monotonically with strength.
- **Damage models and derived setting (first version)**: seven damage types, each controlled by one physical parameter (paper tone, show-through, stains, noise, fading, blur and ink loss), with ink loss held out of all pretraining as unseen damage. Frequency and strength are derived from the measurements by inverting a response curve per type (Figure 7.1, Table 7.1).
- **First pretraining loop**: a convolutional masked autoencoder (ConvMAE) that rebuilds clean lines from masked and damaged copies and pretrains the CRNN's own CNN, which is then fine-tuned inside the CRNN with exactly the baseline settings. A first 6.5-million-parameter ViT encoder memorised the few labelled lines (60–75% CER against 20–43% for the CRNN) and was set aside for the pilot; a transformer encoder remains a Phase 2 option.
- **Damage as training augmentation (E1)**: the same recipes, and a background-normalisation control, used as plain augmentation of the scratch CRNN, three seeds each, on IAM and CATMuS.
- **Robustness and invariance tools**: the baseline was tested under each synthetic damage type at three strengths (Figure 7.2), and a per-damage invariance score (Appendix B) was implemented for the RQ3 analysis in Phase 2.

![What the encoder sees during pretraining: real CATMuS lines (top), and one clean IAM line under four random draws of the hand-picked corruption recipe and four of the derived recipe.](results/figures/fig_corruptions_handpicked_vs_derived.png){w=10}

Table: Derived corruption setting (first version) compared with the hand-picked recipe.
| Damage type | Derived: share of real lines | Derived: median strength | Hand-picked |
|------------|----------|------------|--------------|
| Paper tone | 84% | brightness × 0.80 | 50%, strength uniform in a guessed range |
| Show-through | 89% | opacity 0.40 | 50% |
| Stain / uneven light | 37% | depth 0.08 | 50% |
| Fading | 26% | contrast × 0.52 | 50% |
| Noise | 11% | σ ≈ 3.5 grey levels | 50% |
| Blur | 5% | σ ≈ 1.1 px | 50% |
| Ink loss | held out | – | held out |

## Preliminary results

Table 7.2 gives the first results. The supervised CRNN reaches a character error rate of 9.83% on the IAM test set (6.42% on validation), trained for 50 minutes on a laptop GPU without data augmentation; an off-the-shelf industrial recogniser (PaddleOCR PP-OCRv6 [@paddle]) reaches 11.39% on the same lines without adaptation. This answers the panel's suggestion from Review 1 that achievable accuracy be demonstrated: a small specialised model trained in under an hour is already competitive, and it is the baseline the pretrained models must beat. The same off-the-shelf recogniser gets more than half of the characters wrong (52.50%) on the real medieval test lines, which shows why damaged historical collections need specialised models. With fewer labels the baseline degrades quickly (19.9% CER with 648 lines, mean of three seeds; 43.3% with 65 lines, two seeds), and seeds differ by about 0.5 points, so gains of a point or more are distinguishable from noise. On CATMuS the CRNN reaches 20.0% with all labels and 33.8% with 5% of them (1,188 lines, three seeds); the gap to IAM reflects harder, more varied manuscripts and a test set drawn from manuscripts not seen in training.

Table: Preliminary results (character error rate on the test split; lower is better; pretrained rows are the mean of two seeds, few-label supervised rows of three, two for IAM 1%).
| Model | Training labels | IAM test CER | CATMuS test CER |
|--------------------|--------------|---------|-------|
| PaddleOCR PP-OCRv6, off the shelf | none | 11.39% | 52.50% |
| CRNN, supervised | 100% | 9.83% | 20.02% |
| CRNN, supervised | 10% / 1% of IAM; 5% of CATMuS | 19.94% / 43.32% | 33.77% |
| CRNN + ConvMAE, plain masking | same | 20.40% / 43.85% | 33.34% |
| CRNN + ConvMAE + hand-picked damage | same | 21.00% / 44.72% | 34.96% |
| CRNN + ConvMAE + derived damage (ours) | same | 20.50% / 43.91% | 33.44% |

![Medium-strength synthetic damage raises the baseline's error on IAM test lines; four of the seven damage types at least double it.](results/figures/fig_robustness.png){w=11}

**Does damage hurt (A1)?** Yes. At medium strength, ink loss multiplies the baseline's error by 7.6, noise by 4.9, paper tone by 3.4 and blur by 3.1, while show-through, fading and stains raise it by at most 1.4 times (Figure 7.2); the pilot's rule (at least two damage types doubling the error) is met. On real CATMuS lines, grouped into quartiles of measured damage within each manuscript project, lower ink–paper contrast goes with higher error (the most faded quartile is 1.35–1.47 times worse than the least faded), whereas paper level, noise and background unevenness show no clear effect (0.93–1.08 times). Sharpness moves the opposite way (0.75 times); we think it is confounded with stroke width and line density and draw no conclusion from it. Assumption A2, that real damaged lines differ measurably from clean ones, narrowly failed by the rule fixed in advance (two of the three required statistics; Section 6.4).

**Does pretraining help (A3), and do derived corruptions beat hand-picked ones (A4)?** Not yet for the first question: no pretrained variant beats the supervised baseline by more than the seed spread (about 0.5 points). With 5% CATMuS labels the means are 33.8% (scratch), 33.3% (plain masking), 33.4% (derived) and 35.0% (hand-picked), and on IAM pretraining is slightly worse than scratch in both label settings. Derived damage is at least as good as hand-picked damage in all three settings (33.4% against 35.0%, 43.9% against 44.7%, 20.5% against 21.0%) but indistinguishable from plain masking, so the honest reading is that hand-picked damage hurts and derived damage does no harm, not that derived damage helps. Kišš and Hradiš [@kiss] found that target-domain pretraining does beat training from scratch, but struggles to beat supervised transfer from a related labelled dataset; our pilot did not even beat scratch. We expect the scale of our pretraining to be the main reason: 30,244 lines for 34 minutes, against 750,000 lines in [@lacuna]. Rather than tuning it open-endedly, Phase 2 gives pretraining one bounded rescue attempt (E3, Chapter 8) with a fixed decision date.

**Does the same damage help when used as plain training augmentation (E1)?** Yes, on real lines. We trained the scratch CRNN with exactly the baseline settings, three seeds per arm, with each training line damaged by the hand-picked or the derived recipe and, as a cheap control, with background normalisation of every input line instead (Table 7.3). With 5% of the CATMuS labels, derived augmentation lowers the error on real medieval test lines from 33.8% to 31.6% (seed spread at most ±0.5 points), while hand-picked augmentation gives 33.6% and background normalisation 33.0%. The gain holds on the most damaged quarter of the test lines by each of three measured statistics (darkest paper, most show-through, lowest contrast), each formed within the manuscript project. With 10% of the IAM labels both recipes lower the clean error by about one point (19.9% to 18.8–18.9%). Of the criteria fixed before these runs (B1–B5 in `results/pilot_summary.md`), B1, B3, B4 and B5 are met; B2 (derived beats hand-picked under synthetic damage on IAM) is not met (19.4% against 18.9%), while on real CATMuS lines derived is better (31.6% against 33.6%).

Table: Damage as training augmentation of the scratch CRNN (test CER, mean of three seeds). The CATMuS quarters are the most damaged 25% of test lines by the named statistic.
| Training | IAM 10%, clean | CATMuS 5%, all lines | Darkest paper | Most show-through | Lowest contrast |
|--------------|-------|-------|-------|-------|-------|
| No augmentation | 19.9% | 33.8% | 35.6% | 35.7% | 39.4% |
| Hand-picked damage | 18.8% | 33.6% | 34.7% | 35.1% | 38.1% |
| Derived damage (ours) | 18.9% | 31.6% | 33.0% | 32.9% | 37.0% |
| Background normalisation | 19.8% | 33.0% | 35.0% | 34.7% | 38.2% |

Four limits qualify this result. (a) On IAM with synthetic damage, augmentation cuts the error at medium strength from 37.9% to 19.4%, but this is partly circular, because the models were trained on the same six damage families they are tested on. The fair check is ink loss, held out of both recipes: the ratio of damaged to clean error falls from 3.82 to 3.59 with derived and to 3.27 with hand-picked augmentation. (b) On CATMuS the gain on the hardest quarters (2.4–2.8 points) is about the same as on all lines (2.2 points), so we can say that derived augmentation helps on CATMuS, not that its benefit is specific to damage. (c) Hand-picked augmentation is slightly better on IAM, including under synthetic damage, while derived augmentation is better on CATMuS, where the damage is real and large. (d) The evidence is three seeds, one recogniser and one source–target pair.

## Lessons from Phase 1

Two problems would have silently invalidated results, and both are now guarded against by checks in the pipeline: the polygon fill of CATMuS images made the first damage measurements wrong (Section 6.3), and the transformer encoder initially attended to the padding added to short lines in a batch, so a line could be read differently depending on its neighbours (fixed with an attention mask, verified by identical outputs alone and in a padded batch). The failed ViT attempt is kept in the records rather than hidden. Both reinforce the rule that every model must first pass a sanity check (memorising a small set of lines) and that every reported number must come from a script, not be typed by hand.

Three further lessons shape Phase 2. First, test the cheapest use of an idea first: the derived damage gave no gain through pretraining but a clear gain on real lines as plain augmentation, a result we could have had a week earlier. Second, a synthetic test built from the training recipe's own damage families flatters that recipe, so every robustness claim needs a held-out damage type and real damaged lines. Third, repeat the literature search as the claim sharpens: our late search found that fitting degradation models to real scans goes back to the 1990s [@kanungo], [@baird07], which moved the claimed novelty from the fitting itself to what a deep recogniser learns from it.

# Plan of Work for Capstone Project Phase-2

## Phase 2 tasks (January – May 2027)

Phase 2 climbs the ladder of Section 5.2 from E1, finished in the pilot, to E4, builds the damage models properly, and runs the comparison that answers RQ1 and RQ2 (Table 8.1).

Table: Phase 2 tasks.
| Task | Months | Output |
|--------------------|-------|----------|
| Physical damage models fitted per type (show-through with verso modelling, ink fading, paper tone, stains, capture blur); tag a few hundred real CATMuS test lines by damage type | Jan – Mar | Fitted damage settings v1; real damage-tagged test set |
| E2: consistency training on unlabelled lines with the derived damage (CRNN + CTC, clean and damaged views), three seeds | Jan – Feb | Does unlabelled data add to E1? |
| E3: one bounded SSL-pretraining rescue (protocol fixes, ten times larger unlabelled pool on Kaggle, public pretrained encoder) | Feb – Mar, fixed decision date | Go or stop on SSL pretraining |
| E4: a same-script dataset pair with different damage | Mar – May | Does the derived recipe follow the target's damage? |
| Held-out evaluation: unseen damage, new medium; supervised-transfer baseline | Apr – May | Answers to RQ1 and RQ2 |

If E2–E4 stall, a fallback side project is ready: hallucination of vision-language OCR models under controlled document damage.

Phase 3 (June – December 2027) then covers the invariance–error analysis (RQ3), transfer to unseen scripts (Indic and Arabic) and camera capture, ablations and additional seeds, and the paper, code and data release, aiming first at an ICDAR workshop and then a main-track conference or IJDAR. Figure 8.1 shows the full timeline.

![Project timeline, September 2026 to December 2027 (Phase I blue, Phase II green, Phase III red).](capstone/reviews/_kit/assets/img/gantt.png){w=14.5}

## Effort plan

Table: Planned effort by individual (tentative).
| Member | Owns | Main tasks | Phases |
|---------|---------|----------------|----|
| Arvind Kothamangala | Data and baselines | Data loaders, character set and splits, supervised baselines, CER tooling | I – II |
| Atharv Sawarkar | Damage modelling | Damage-measurement tool, physical damage models, parameter fitting, tagging real lines | I – II |
| Vignesh Nunna | Training with derived damage | Augmentation (E1), consistency training (E2), bounded SSL rescue (E3) | I – III |
| Rohit Rajan | Evaluation and analysis | Fine-tuning, held-out tests, invariance scores, transfer experiments | II – III |
| All members | Writing and release | Weekly and phase reports, paper, code and data release | I – III |

::: references
:::

::: appendix
# Appendix A: Definitions, Acronyms and Abbreviations

Table: Definitions and acronyms.
| Term | Meaning |
|-----|-----------------|
| CER | Character error rate: the number of character insertions, deletions and substitutions needed to turn the output into the reference, divided by the reference length |
| CTC | Connectionist temporal classification: a loss that trains a sequence model to output text without character positions |
| CRNN | Convolutional recurrent neural network: convolutions followed by a recurrent layer and CTC |
| HTR | Handwritten text recognition |
| OCR | Optical character recognition |
| SSL | Self-supervised learning: learning from unlabelled data by solving a pretext task |
| MAE | Masked autoencoder: reconstructs hidden image patches from visible ones |
| ViT | Vision transformer: a transformer applied to image patches |
| VICReg | Variance–invariance–covariance regularisation, a joint-embedding SSL method |
| JEPA | Joint-embedding predictive architecture |
| Invariance score | Similarity of a model's features for a clean line and its damaged copy (1 = the damage is ignored) |
| KS D | Two-sample Kolmogorov–Smirnov statistic: maximum distance between two cumulative distributions |
| NFC | Unicode normalisation form C (composed characters) |
| Label budget | Fraction of the labelled training lines used for fine-tuning |
| Held-out damage | A damage type never used in pretraining, used only for testing transfer |

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

**How it works.** The encoder is exactly the CNN of the CRNN, so after pretraining its weights are copied into the recogniser without any change. A line is damaged by the sampler (B.2), then 60% of its 8-pixel vertical strips are blanked. The CNN turns the masked line into 384 numbers per 4-pixel column, and a small decoder predicts the pixels of every column. The target is the **clean** line, so the model must both fill in hidden strips (masked autoencoding, as in MAE [@mae]) and remove the damage (denoising). The loss is the mean squared error on hidden columns plus a quarter-weighted error on visible columns, which forces the visible part to be cleaned too. With no damage, this is plain masking; with the hand-picked or derived recipe, it becomes the pretraining compared in Table 7.2.

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
