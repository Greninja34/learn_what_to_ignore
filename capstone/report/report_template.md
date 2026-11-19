<!--
Phase-1 report, TEMPLATE-ONLY version (no pilot run). Generated from report.md on 19 Nov 2026.
Build: python capstone/report/build_pandoc.py --pdf --src report_template.md --name Team147_Phase1_Report_template
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
Text recognisers read clean scans well but fail on damaged documents (faded ink, ink showing through from the back of the page, stains, darkened parchment), and damaged collections are also where transcribed training data is scarcest. Self-supervised learning (SSL) can learn from unlabelled text lines by training a model to rebuild a line from a corrupted copy, but the corruptions it is trained to see through are chosen by hand and re-tuned for each collection, even in the strongest recent work. This project, *Learning What to Ignore*, replaces that guess with a measurement: we measure the damage on real historical lines, model the main damage types with simple physical forward models, fit their parameters to the measurements, and pretrain a masked autoencoder that reconstructs clean lines from lines damaged in this derived way. We then ask whether the derived corruptions beat plain masking and hand-chosen corruptions when few labels are available, which kinds of new damage, media and scripts the learned invariance transfers to, and whether a model's measured invariance to a damage type predicts how much that damage raises its error. In Phase 1 we completed the literature survey and the formulation of three research questions with falsifiable hypotheses; identified the research gap; acquired and processed the datasets, IAM (modern English handwriting) and a Latin and French subset of CATMuS Medieval (29,027 real manuscript lines from 11 projects), including the removal of a polygon fill that would have corrupted every damage measurement; built a tool that measures eight damage statistics per line; showed that real medieval lines differ from clean ones mainly in paper tone and show-through; and derived a first corruption recipe from these measurements. Phase 2 uses the derived damage to train recognisers in increasing order of cost (augmentation, consistency training, masked-autoencoder pretraining) and compares it with hand-chosen damage.
:::

# Introduction

## Background

Optical character recognition (OCR) converts images of text into machine-readable characters. On clean printed scans it is close to a solved problem, and line-level handwritten text recognition (HTR) reaches character error rates of a few percent on benchmarks such as IAM [@iam]. These systems are, however, trained and evaluated mostly on clean material. Libraries, archives and record rooms hold millions of pages whose ink has faded, whose back-side text shows through, whose paper or parchment has darkened or is stained, or that were captured with uneven light or a phone camera. On such pages accuracy drops sharply, and these are also the collections for which almost nobody has transcribed enough lines to train a model.

The usual way around the shortage of labels is self-supervised learning (SSL): a model is first trained on a pretext task that needs no labels, such as rebuilding a line image from a copy with parts hidden or corrupted, and is then fine-tuned with a few transcribed lines. SSL for text recognition is an active field [@survey], with contrastive [@seqclr], masked-prediction [@kiss] and reconstruction-based [@textdiae], [@garrido] methods.

## Motivation: what should a model learn to ignore?

Through its pretext task, every SSL method decides which variations the model should become insensitive to: a contrastive method treats two augmented views of an image as "the same", a denoising autoencoder a corrupted line and its clean version. What the model learns to ignore is therefore set by the corruptions the designer picks. In general vision, different downstream tasks need different, sometimes opposite, invariances [@ericsson], and robustness to a corruption depends on how similar the training augmentations are to it [@mintun].

For text recognition this choice is still made by hand. A critical survey finds no standard evaluation protocol and stresses that augmentations must suit text data, but gives no procedure for choosing them [@survey]; Text-DIAE picks its degradations by hand [@textdiae]; and the most recent large comparison of SSL methods for handwriting (NeurIPS 2026) uses "a fixed augmentation pipeline" whose blur, noise and contrast changes are described only as "small", "mild" or "low", with no ranges and no selection procedure [@garrido]. That paper also shows that pixel-reconstruction pretraining (masked autoencoders) clearly outperforms contrastive and joint-embedding methods for handwriting, because the information that separates characters lies in high-variance pixel directions. The open question therefore becomes: when a reconstruction model is trained to rebuild clean lines from damaged ones, *which damage* should it be shown, and can that choice be derived from the documents themselves instead of guessed?

## Scope of the work

The project studies the recognition of single text lines already cut out of the page; layout analysis and line segmentation are left out, because their errors would blur the comparison between pretraining methods. The recogniser is kept small (5 to 25 million parameters), so that differences can be attributed to the pretraining and the method stays usable by an archive with modest hardware. We model three to seven physically describable damage types and evaluate on modern handwriting (IAM), real historical manuscripts (CATMuS Medieval [@catmus]) and, in later phases, an unseen script and camera-captured text. Large vision-language models and many languages at once are out of scope.

## Who benefits

- **Archives, libraries and digital humanities projects**, which today train a recogniser per collection from a few hundred transcribed lines: if damage derived from a collection's own pages lowers the error, fewer lines must be transcribed and no corruption recipe has to be tuned by trial and error.
- **Low-resource scripts**, including many Indian scripts, with many scanned manuscripts but very few transcribed lines, where learning mostly from unlabelled pages is the only route that scales.
- **Practitioners planning a transcription effort**: if measured invariance predicts which damage hurts a model, a sample of pages is enough to decide where to spend the labelling budget.
- **SSL researchers**, by turning the choice of corruptions from a guess into a measurement procedure that can be checked.

## Organisation of the report

Chapter 2 states the problem, research questions and hypotheses; Chapter 3 surveys the literature; Chapter 4 identifies the research gap and the challenges in closing it; Chapter 5 lists the objectives and the approach; Chapter 6 describes the datasets, their preprocessing and the damage they contain; Chapter 7 summarises the Phase 1 work; and Chapter 8 gives the plan for Phase 2. Appendix A defines the terms used.

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

**Critical survey (Penarrubia, Valero-Mas and Calvo-Zaragoza, IJCV 2025)** [@survey]. Organises SSL methods for text recognition into discriminative families (contrastive, geometric and puzzle solvers, distillation, clustering, information maximisation), generative families (masked image modelling, inpainting, GANs) and hybrids. Its main finding for us is methodological: methods are rarely compared under the same conditions, there is no standardised evaluation protocol (label fractions, image height and character sets differ), and augmentations must be chosen to suit text, for which no procedure is given. We therefore fix the protocol on day one and treat the choice of corruptions as a research question rather than a setting.

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
| Penarrubia et al., IJCV 2025 [@survey] | Critical survey of SSL for text recognition | No standard protocol; augmentations must suit text data | No method proposed for choosing them |
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

1. **E1, augmentation:** train the CRNN on labelled lines damaged with the derived recipe;
2. **E2, consistency training:** on unlabelled lines, train the CRNN with CTC to give the same output for a clean and a damaged view;
3. **E3, SSL pretraining:** masked-autoencoder pretraining of the recogniser's encoder with the derived damage on a large unlabelled pool, compared with plain masking and hand-chosen damage, stopped at a fixed decision date;
4. **E4, a new dataset pair:** the same script with different damage, to test whether the derived recipe tracks the damage of the target.

Supervised transfer from a related labelled dataset and an off-the-shelf recogniser are the outside reference points.

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

**Do real damaged lines differ measurably from clean ones?** Only partly. Two damage statistics separate the datasets strongly: the paper of the historical lines is much darker (D = 0.82), and far more of it is faintly grey (D = 0.84), consistent with show-through and parchment texture. Background unevenness differs moderately (0.42); contrast, sharpness and noise differ little. The finding is still informative: real medieval damage is concentrated in paper-side effects (tone, show-through), not in the blur and noise that hand-picked recipes emphasise, and the derived setting reflects that (Section 7.1). Stroke width and ink fraction also differ strongly, but reflect the tighter cropping and denser script of the manuscripts, not damage, and are not used for fitting.

# Conclusion of Capstone Project Phase-1

## Work completed

Phase 1 set out to define the problem precisely, survey the literature, secure the data and build the measurement side of the approach. The following is complete:

- **Literature survey and formulation**, updated in November 2026 with a full reading of [@garrido] and a search of 2026 work. The research gap was re-confirmed, and the novelty claim was narrowed after finding that fitting degradation models to real scans dates back to the 1990s [@kanungo], [@baird07].
- **Research questions and hypotheses** (Chapter 2), each with a stated condition that would show it wrong.
- **Data pipeline**: IAM and a 29,027-line Latin and French subset of CATMuS Medieval, cleaned (including the removal of the polygon fill), resized to a fixed height, normalised to Unicode NFC and stored with metadata, fixed splits and character sets built from the training splits only.
- **Damage-measurement tool**: eight per-line statistics, validated by checking that each synthetic damage type moves its statistic monotonically with strength, and an analysis of how real medieval lines differ from clean ones (Section 6.4).
- **Damage models**: seven damage types, each a simple forward model with one physical parameter (paper tone, show-through, stains, noise, fading, blur and ink loss). Ink loss is held out of all training as unseen damage for the transfer test.
- **Derived damage recipe (first version)**: frequency and strength of each damage type derived from the measurements by inverting a response curve per type (Section 7.1).

## The derived damage recipe

For each damage type, the type is first applied to clean IAM lines at a range of strengths and its statistic is measured, giving a curve from strength to measured value. A real CATMuS line whose statistic lies beyond the range of clean lines (outside their 5–95% band) is counted as damaged by that type, and its strength is read off the curve. The share of damaged lines gives how often the damage is applied, and their strengths give how strong (Table 7.1, Figure 7.1). The usual practice, a hand-picked recipe, applies every type to half of the lines at a strength drawn from a range chosen by eye.

![What a model trained with each recipe sees: real CATMuS lines (top), and one clean IAM line under four random draws of the hand-picked recipe and four of the derived recipe.](results/figures/fig_corruptions_handpicked_vs_derived.png){w=10}

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

The two recipes are very different: the derived one concentrates on paper-side damage, which real medieval pages show, while the hand-picked one spends half of its corruptions on blur and noise, which the measurements show to be rare. This first version has a known limitation: a difference between IAM and CATMuS also reflects script, pen and scanner, not only damage. Phase 2 replaces it with a physical fit for each damage type.

## Utility of the work

The measurement tool and derived recipe turn the choice of corruptions, today a guess repeated for every collection, into a procedure that any archive can run on a sample of its own pages. The cleaned and documented data pipeline, the fixed protocol and the falsifiable hypotheses make the Phase 2 comparisons reproducible, and the narrowed novelty claim keeps the contribution defensible.

## Lessons from Phase 1

The polygon fill of CATMuS images would have silently made every damage measurement wrong (Section 6.3); it was found only because the measurements were checked against the images, so every new dataset now passes the same check. Repeating the literature search as the claim sharpened moved the claimed novelty from fitting damage to real documents, which is old, to what a deep recogniser learns from the fitted damage. Finally, the order of experiments matters: the cheapest use of the derived damage (augmentation) is tested before the most expensive (pretraining).

# Plan of Work for Capstone Project Phase-2

## Phase 2 tasks (January – May 2027)

Phase 2 climbs the ladder of Section 5.2 from E1 to E4, builds the damage models properly, and runs the comparison that answers RQ1 and RQ2 (Table 8.1).

Table: Phase 2 tasks.
| Task | Months | Output |
|--------------------|-------|----------|
| Physical damage models fitted per type (show-through with verso modelling, ink fading, paper tone, stains, capture blur); tag a few hundred real CATMuS test lines by damage type | Jan – Mar | Fitted damage settings v1; real damage-tagged test set |
| E1: the derived damage as training augmentation of the CRNN, against no augmentation, hand-chosen damage and a background-normalisation control; supervised baselines at 1%, 10% and 100% of the labels | Jan | Does derived damage lower the error on real lines? |
| E2: consistency training on unlabelled lines with the derived damage (CRNN + CTC, clean and damaged views), three seeds | Jan – Feb | Does unlabelled data add to E1? |
| E3: masked-autoencoder pretraining with the derived damage (large unlabelled pool on Kaggle) against plain masking and hand-chosen damage | Feb – Mar, fixed decision date | Go or stop on SSL pretraining |
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


:::
