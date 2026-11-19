# ESA prep, 19 Nov 2026: literature, research gap and answers to your slide questions

Part A is the literature: every paper in the deck, with its core idea, how it works (implementation), what it found, its limit for us, and a likely viva question.
Part B is the research gap and the literature survey as you would tell it.
Part C answers your questions (a)–(v) and lists every change made to the deck.

All paper facts were checked against the papers on 19 Nov 2026.

---

## Part A. The papers

Every entry below was checked on 19 Nov 2026 against the paper itself (full text for the arXiv papers, the publisher or author page for the rest). Where a source could not be read in full, the entry says so.

### A1. Garrido-Munoz & Calvo-Zaragoza, *Handwritten Text Recognition Lives in the High-Pixel Variance Subspace*, arXiv 2609.35473, Sep 2026, accepted at NeurIPS 2026
- **Problem:** For natural photos, contrastive SSL usually beats pixel reconstruction. For handwriting, the opposite is true. Why?
- **Core idea:** The information that tells characters apart sits in the **high-variance pixel directions** of handwriting images. Pixel-reconstruction methods have to model these directions; contrastive and JEPA methods can ignore them.
- **How:** Six SSL methods from three families (pixel masked image modelling, JEPA, contrastive), all with the same encoder, data and evaluation. Six handwriting benchmarks in five languages. They measure how well each encoder lines up with the high-variance pixel subspace.
- **Findings:** Pixel-reconstruction methods get the lowest CER on every benchmark, they are the only family that gains from pretraining on real handwriting, and they need fewer labels. Within each method, alignment with the high-variance subspace predicts CER.
- **Why it matters to us:** It is why we chose reconstruction (MAE-style) pretraining, and why our question became "which damage" instead of "which SSL family".
- **Limit for us:** Fixed augmentation pipeline; no damage study.
- **Viva Q:** *Why MAE and not contrastive?* → For handwriting, reconstruction wins (this paper).

### A2. Penarrubia, Valero-Mas & Calvo-Zaragoza, *Self-Supervised Learning for Text Recognition: A Critical Survey*, IJCV 2025 (arXiv 2407.19889)
- **What it is:** The survey of SSL for text recognition (handwritten and scene text).
- **Taxonomy (from the paper):** **Discriminative** methods, split into contrastive learning, geometric and puzzle solvers, distillation, clustering and information maximisation (not all of these have been tried for text); **generative** methods (masked image modelling, image inpainting, GANs); and hybrids such as DiG, which combine both.
- **Main findings:** Results are hard to compare because there is **no standardised evaluation protocol**: for example, papers fine-tune on different label fractions. The authors propose standardisations. They also stress that data augmentation must **fit the nature of text data**: for example, horizontal crops and flips can destroy the reading order.
- **Careful:** The survey does **not** say "augmentations are chosen ad hoc". What it does say is that there is no standard protocol, that augmentations must suit text, and that it gives no procedure for choosing them. Quote it that way.
- **Why it matters:** It shows that choosing augmentations is a recognised, open problem and that the protocol must be fixed. We fixed ours on day one.

### A3. Kišš & Hradiš, *Self-supervised Pre-training of Text Recognizers*, ICDAR 2024 (arXiv 2405.00420)
- **Problem:** Can unlabelled historical lines replace expensive transcriptions?
- **How:** Pretrain the recogniser's encoder on unlabelled lines, then fine-tune with different amounts of labels.
  - **Masked label prediction:** the model predicts a discrete code for each masked region. Three ways to get the codes: Feature Quantization, VQ-VAE and Post-Quantized AE.
  - **Joint embedding:** VICReg and NT-Xent. They add an **image-shifting** trick so the model can't collapse by using only position encodings and ignoring the image.
  - **Data:** historical handwriting (Bentham) and historical printed text.
  - **Code:** github.com/DCGM/pero-pretraining.
- **Findings:** Pretraining on target-domain data is **very effective compared with training from scratch**, but it **struggles to beat transfer learning** from a closely related labelled domain.
- **Why it matters to us:** Supervised transfer must be a baseline, and SSL is not a free win.
- **Careful:** Our pilot did not even beat scratch. The likely reason is scale (see A4).

### A4. Vogler, Allen, Miller & Berg-Kirkpatrick, *Lacuna Reconstruction: Self-Supervised Pre-Training for Low-Resource Historical Document Transcription*, Findings of NAACL 2022 (arXiv 2112.08692)
- **Core idea:** Like BERT's masked-word task, but on images. Hide regions of a line image and make the model **pick the true hidden region out of distractors** taken from the same line. It is contrastive, not pixel rebuilding.
- **How:** A convolutional feature extractor, then an LSTM or Transformer for context. Pretrained on unlabelled lines, then fine-tuned with CTC on very few transcribed lines. Data: Islamicate (Arabic-script) manuscripts and early-modern English print (Old Bailey).
- **Findings:** Gains over scratch with as few as **30 labelled lines**. With **750k pretraining lines**, CER on the Attar-Mubhij manuscripts drops from **60.4% to 23.7%** in the 30-line setting (checked in the paper's text).
- **Why it matters:** SSL works with tiny label budgets on historical data, but it used ~25× more unlabelled lines than our pilot's 30k.

### A5. Mitra, Mondal & Jawahar (IIIT Hyderabad), *Learning Beyond Labels: Self-Supervised Handwritten Text Recognition (LoGo-HTR)*, WACV 2026, pp. 6653–6663
- **Core idea:** Two pretraining losses. A **local contrastive loss** keeps nearby parts of a word image consistent; a **global decorrelation loss** keeps the features varied so they don't all collapse to the same thing.
- **How:** Pretrain on their new **SSL-HWD** set (about 10M word images from 852 writers: 2.08M labelled, 7.92M unlabelled), then fine-tune a transformer decoder with limited labels.
- **Findings:** Beats prior state of the art on HTR benchmarks, including multilingual and historical ones, even with only 20% of the labels.
- **Limit for us:** Contrastive family, word level, no damage study. Scale again: 10M images.
- (Source: the WACV page and project page, logo-ssl.github.io. The full PDF was not readable here.)

### A6. Aberdam, Litman, Tsiper, Anschel, Slossberg, Mazor, Manmatha & Perona, *Sequence-to-Sequence Contrastive Learning for Text Recognition (SeqCLR)*, CVPR 2021 (arXiv 2012.10873)
- **Core idea:** The first contrastive SSL for text. A text image is a **sequence**, so each feature map is split into several **instances**, and matching instances from two augmented views are contrasted. One image gives several positive pairs.
- **Three ways to form instances:** all-to-instance (average all frames; most robust to misalignment), window-to-instance (average a window of frames), frame-to-instance (each frame on its own).
- **Augmentation lesson:** Horizontal flips and aggressive horizontal crops break the left-to-right alignment between the two views. This is why augmentation choice is delicate for text.
- **Findings:** Beats non-sequential contrastive methods, beats supervised training when labels are few, and with all labels reaches state of the art on handwriting. Word error falls by 9.5% on IAM and 20.8% on RIMES. Datasets: IIIT5K (scene text), IAM and RIMES.

### A7. Souibgui, Biswas, Mafla, Biten, Fornés, Kessentini, Lladós, Gomez & Karatzas, *Text-DIAE: A Self-Supervised Degradation Invariant Autoencoder for Text Recognition and Document Enhancement*, AAAI 2023 (arXiv 2203.04814)
- **Core idea:** A **ViT-based autoencoder** pretrained to undo three degradations: **masking, blur and added background noise**. The input is degraded and the target is the clean image (unmasking, deblurring, denoising).
- **Downstream tasks:** word-level handwritten recognition, scene-text recognition, and document enhancement (binarisation, deblurring).
- **Findings, as the authors state them:**
  - The best set of pretext tasks depends on the downstream task.
  - **The closer a pretext task is to the downstream task, the better the model.**
  - Faster convergence, and state of the art with **43× (handwriting) and 45× (scene text) less pretraining data** than contrastive methods such as SeqCLR.
  - In the ablations, **adding noise did not help** recognition.
- **Why it is our closest neighbour:** "Pretrain with damage, rebuild the clean image" is exactly our ConvMAE setup. Their own finding ("closer pretext task = better") supports our idea of matching the damage to real pages.
- **Gap:** The degradations and their strengths are hand-picked, and nothing is tested on held-out damage, media or scripts.
- **Viva Q:** *How are you different from Text-DIAE?* → They choose the damage by hand; we derive which damage, how often and how strong from real pages, and test on held-out damage.

### A8. Guan, Lin, Xu, Liu, Zhao, Fan, Xu & Greene, *PreP-OCR: A Complete Pipeline for Document Image Restoration and Enhanced OCR Accuracy*, ACL 2025 (arXiv 2505.20429)
- **Core idea:** Fix the image first, then fix the text.
- **How:**
  1. Render plain text with varied fonts and layouts, apply degradations in random order, and train an image-restoration model on these pairs. It uses multi-directional patch extraction and fusion for large pages.
  2. Run OCR.
  3. A ByT5 language model, fine-tuned on synthetic historical text pairs, corrects what errors remain.
- **Findings:** On 13,831 real historical pages (English, French, Spanish), CER falls by 63.9–70.3% compared with OCR on the raw images.
- **Limit for us:** Synthetic damage with hand-set ranges; it restores images instead of making the recogniser robust.

### A9. Kanungo, Haralick, Baird, Stuetzle & Madigan, *A Statistical, Nonparametric Methodology for Document Degradation Model Validation*, IEEE TPAMI 22(11):1209–1223, 2000
- **Starting point:** Printing, photocopying and scanning degrade documents, and statistical models of that degradation are needed for document-image research.
- **Idea:** Validating a degradation model becomes a **nonparametric hypothesis test**. Compare real and synthetic character images with simple character-distance functions, using a **permutation test** whose null distribution is built empirically.
- **Findings:** With a large enough sample, the model can be rejected. The validation and power procedures work for any degradation model, and two models can be compared through their p-values.
- **Background:** Kanungo's earlier (1993) model for black-and-white scans flips pixels with a probability that depends on their distance from a stroke edge, then applies a morphological closing.
- **Why it matters:** This is the old root of "fit damage to real scans", so it is **not** our novelty. Our step is linking the fit to what a **deep** recogniser learns to ignore. Our A2 check echoes it: it also compares two distributions (KS distance instead of a permutation test).

### A10. Baird, *The State of the Art of Document Image Degradation Modelling*, in *Digital Document Processing* (B. B. Chaudhuri, ed.), Springer 2007, pp. 261–279
- **What it is:** A survey of degradation models for printed documents. It separates two kinds of model: **explanatory** (physics: optics blur, pixel sensitivity, thresholding, jitter) and **descriptive** (statistics of what the damage looks like). It also covers estimating parameters from real images and validating models.
- **Why it matters:** It supports our "physical form + fitted parameters" step, and our claim that only some damage has clean physical models.
- (Bibliographic details and the explanatory/descriptive split checked via secondary sources. The chapter itself is behind Springer's paywall.)

### A11. Groleau, Chee, Larson, Maini & Boarman, *Augraphy: A Data Augmentation Library for Document Images*, arXiv 2208.14558 (v2 2023; published at ICDAR 2023)
- **What it is:** A Python library with **26 augmentations**, arranged as a pipeline that follows a document's life in **three phases**:
  - **Ink:** how ink goes onto the page (bleed, low ink, etc.).
  - **Paper:** the paper itself; this phase includes **BleedThrough**.
  - **Post:** what happens to the printed page afterwards (folding, stains, lighting, scanning, faxing).
- **Uses shown in the paper:** making training data for document denoising (a denoising CNN trained on Augraphy data), and making hard test data for robustness checks.
- **Limit for us:** Which effects to use, and how strong, is left to the user. That is exactly the choice we derive.
- **Our implementation:** We wrote our own 7 simple damage functions (lwti/damage/families.py) so we can control and measure each one.

### A12. Ericsson, Gouk & Hospedales, *Why Do Self-Supervised Models Transfer? On the Impact of Invariance on Downstream Tasks*, BMVC 2022 (arXiv 2111.11398; the v1 title read "Investigating the Impact of Invariance...")
- **Core idea:** Contrastive SSL models learn to ignore ("be invariant to") the augmentations used in pretraining. This invariance partly carries over to real pose and lighting changes. Different downstream tasks favour **opposing** invariances, so the standard augmentation recipe can hurt some tasks.
- **How they measure invariance:** Two measures between an image and its transformed copy, averaged over images:
  1. the **Mahalanobis distance** between the two feature vectors (small = invariant);
  2. the **cosine similarity** after standardising the features: subtract the mean feature and whiten with the full feature covariance, via a Cholesky factor.
- **Proposed fix:** Fuse representations with complementary invariances, which transfers better across tasks.
- **Our use, and an honest difference:** Our score is their cosine version, but we standardise **each feature separately** (mean 0, spread 1). That is a diagonal approximation, not the full-covariance whitening. If asked, say: "a simplified, per-feature version of Ericsson's measure."

### A13. Mintun, Kirillov & Xie, *On Interaction Between Augmentations and Corruptions in Natural Corruption Robustness*, NeurIPS 2021 (arXiv 2102.11273)
- **Core idea:** They build a feature space for image transforms and define the **Minimal Sample Distance (MSD)** between an augmentation and a test corruption. It measures how close the nearest augmentation samples come to the corruption, not how close the two distributions' centres are (which is what MMD measures).
- **Findings:**
  - Robustness correlates strongly with this similarity: augmentations perceptually close to the corruptions help most.
  - Recent augmentation methods lose much of their gain when the test corruptions are sampled to be perceptually **dissimilar** from ImageNet-C. For this they build new benchmark sets of dissimilar corruptions.
  - Gains carry over among perceptually similar transforms.
- **Why it matters:** It is the strongest argument for deriving damage from real pages (match training damage to test damage), and for holding out ink loss (test on damage the model never saw).

### A14. He, Chen, Xie, Li, Dollár & Girshick, *Masked Autoencoders Are Scalable Vision Learners (MAE)*, CVPR 2022 (arXiv 2111.06377)
- **How:** Cut the image into patches and hide a large random subset (**75%**). The encoder sees only the visible patches; a light decoder rebuilds the hidden pixels. The loss is the mean squared error on the hidden patches (pixels normalised per patch). The decoder is thrown away after pretraining.
- **Why such a high mask:** It makes the task hard enough that the model can't solve it by copying from neighbours.
- **Our version (lwti/models/conv_mae.py):** The same idea on the CRNN's own CNN. We hide 60% of 8-px vertical strips and rebuild the **clean** pixels from a damaged input, so it is a masked and denoising autoencoder.

### A15. Shi, Bai & Yao, *An End-to-End Trainable Neural Network for Image-based Sequence Recognition and Its Application to Scene Text Recognition (CRNN)*, TPAMI 2017 (arXiv 1507.05717)
- **How:** Three parts.
  1. Convolutional layers turn the image into a sequence of feature frames.
  2. A deep bidirectional LSTM gives a label distribution for each frame.
  3. A transcription layer (CTC) turns the frames into text, with no need to know where each character is.
- **Findings:** Trained end to end, no character segmentation needed, handles any text length, and has far fewer parameters than standard deep CNNs. Strong on scene-text benchmarks.
- **Our version (lwti/models/crnn.py):** 7.4M parameters, 64-px-high grey lines; the CNN outputs 384 numbers per column (one column per 4 px).
- **CTC (Graves et al., ICML 2006):** The model outputs a letter or "blank" for each frame. Repeats and blanks are collapsed ("hh-e-ll-ll-o" → "hello"), and the loss sums over every alignment that gives the right text.

### A16. Clérice, Pinche, Vlachou-Efstathiou, Chagué, Camps, Gille Levenson, Brisville-Fertin, Boschetti, Fischer, Gervers, Boutreux, Manton, Gabay, O'Connor, Haverals, Kestemont, Vandyck & Kiessling, *CATMuS Medieval: A Multilingual Large-Scale Cross-Century Dataset in Latin Script for Handwritten Text Recognition and Beyond*, ICDAR 2024 (LNCS 14806, pp. 174–194)
- **Content:**
  - The paper: about 200 manuscripts and incunabula, 8th–16th century, more than 160,000 lines and about 5 million characters, around 10 languages (Latin, Old and Middle French, Spanish, Italian, Middle Dutch and others).
  - Shared transcription guidelines: graphemic, abbreviations kept as written.
  - The Hugging Face release has grown to about 195k lines (153k train / 19.4k validation / 22.6k test), CC BY 4.0.
- **Our use:** The source of real damage (measuring, pretraining, testing). Its test split comes from manuscripts not seen in training.
- **Say it this way:** "about 195k lines in the current release (more than 160k in the paper)".

### A17. Marti & Bunke, *The IAM-database: An English Sentence Database for Off-line Handwriting Recognition*, IJDAR 5:39–46, 2002
- 657 writers, 1,539 scanned pages, 5,685 sentences, **13,353 text lines** and 115,320 words. The text comes from the LOB corpus of British English. Non-commercial research use only; registration is needed on the official site.
- **Our version:** Teklia/IAM-line on Hugging Face, 6,482 train / 976 validation / 2,915 test lines (10,373 in total, because this split doesn't use all 13,353 lines). The split is writer-independent: no writer appears in both train and test.

### A18. PaddleOCR (PP-OCR series), PaddlePaddle, GitHub toolkit
- An industrial OCR toolkit: text detection, then orientation classification, then a line recogniser. We used its recogniser off the shelf as a "what does a ready-made OCR get" reference: 11.4% CER on IAM, 52.5% on CATMuS (it was never trained on medieval script). It is cited as a software repository, not a paper.

### A19. Background named in the deck or report
- **VICReg** (Bardes, Ponce & LeCun, ICLR 2022): joint-embedding SSL with three terms. **V**ariance keeps each feature dimension spread out, **i**nvariance makes two views give similar features, and **c**ovariance stops dimensions from repeating each other. Variance and covariance are applied to each branch separately. It is in our objective 4 as a non-reconstruction control (not run yet).
- **Salerno & Tonazzini**, *Highly Degraded Recto-Verso Document Image Processing and Understanding*, ERCIM News 95, 2013 (the reference in our report):
  - **Model:** Each side of the page = its own ink + a **blurred and attenuated** copy of the other side, as two coupled nonlinear equations in optical density. The blur kernels are fixed; the strength (gain) of the show-through varies across the page. The nonlinearity follows Sharma's work on show-through.
  - **Removal:** Estimate the blur kernels, compute the per-pixel gains in closed form, then recover the front and back by constrained maximum likelihood.
  - **Our show-through function is a simplified version:** mirrored, shifted, blurred back page, one global opacity `p`, and it can only darken.

---

## Part B. Literature survey and research gap, as you would say them

**The story in four steps:**
1. **SSL for text works, but its recipe is hand-made.** SeqCLR, Lacuna, Text-DIAE, Kišš & Hradiš and LoGo-HTR all pretrain on unlabelled lines and gain when labels are few. The survey (Penarrubia 2025) finds no standard evaluation protocol and stresses that augmentations must fit text data, but gives no procedure for choosing them. Text-DIAE itself found that the closer the pretext task is to the downstream task, the better. Garrido-Munoz 2026 shows reconstruction is the right family for handwriting.
2. **Damage simulation is mature, but its settings are left to the user.** Augraphy and PreP-OCR simulate damage well, but someone has to pick which damage and how strong.
3. **Fitting damage to real scans is old.** Kanungo/Haralick/Baird did it for binary pages and classic OCR. It was never linked to what a deep recogniser learns.
4. **Invariance and robustness theory says the choice matters.** Ericsson: different tasks need different invariances. Mintun: augmentations help when they resemble the test corruptions.

**Gap (one sentence):** Nobody derives *which* damage a deep text recogniser should learn to ignore (and how often and how strongly) from measurements of real pages, and then checks on held-out damage, media and scripts that the model actually ignores it and that this predicts its errors.

**What is not our novelty (say this before they do):** fitting damage models to scans (Kanungo 2000), damage augmentation libraries (Augraphy), degradation-invariant pretraining (Text-DIAE), the invariance measure (Ericsson). **What is new:** connecting them: measured damage → recipe → what the model ignores → error on real damaged lines.

---

## Part C. Your questions, (a) to (v)

**(a) Slide 9.** Rewritten: "Where labels are few, the error rises quickly, and that is the gap we target. In the literature, SSL reaches parity with supervised training rather than a clear win, so we always keep a supervised baseline beside it." The photo stays; its caption and the "as the picture shows" phrase are gone.

**(b)** This file, Parts A and B.

**(c) "SSL may not beat supervised learning", is that a fact?** It is listed as a **risk**, not stated as a fact, and the risk is real: Kišš & Hradiš 2024 found SSL beats scratch but struggles to beat supervised transfer, and in our pilot it did not even beat scratch. The row now cites Kišš & Hradiš so it reads as a documented risk.

**(d) Objectives status.** Close, with nuance:
1. Pipeline + baselines: **done**.
2. Measurement tool + how real lines differ: **done** (A2 is the answer).
3. Damage models with derived frequency and strength: **first version done** (recipe v0). The 7 damage functions are simple simulators; properly fitted physical models (v1) are Phase 2.
4. Pretraining with derived vs none / masking / hand-picked: **done**; the VICReg control is **not** done → partial.
5. Transfer to held-out damage / medium / script: **only a first look** (held-out ink loss on IAM). Media and script are future.
6. Invariance vs error rise: **first look done** on IAM synthetic damage (the RQ3 numbers, now removed from the slides). CATMuS is future.
So: 1–2 done, 3 done as v0, 4 partial, 5–6 mostly future with a first look.

**(e) Why all of IAM but only part of CATMuS?** IAM is small (10.4k lines, a few hundred MB), so we use it all, with its official split. CATMuS is about 195k lines and 22.5 GB. Reasons for the subset: (1) **time and compute**: one pilot week on an 8 GB laptop GPU; (2) **consistency**: we kept two languages (Latin + French) that are large in both train and test, so the character set stays manageable (195 symbols) and the test still has unseen manuscripts; (3) **variety**: the download script picked shards round-robin across projects, so the 11 projects cover many manuscripts. 25k lines was also enough to measure damage statistics stably (we measured 3,000 sampled lines).

**(f) CATMuS line counts.** They were consistent but written two ways. 25,005 downloaded training lines = **23,762 train + 1,243 validation** (5% held out); **4,022 test**. 5% of 23,762 = **1,188** labelled lines (baselines). Pretraining pool = 23,762 CATMuS + 6,482 IAM = **30,244** ("30k"). Both slides now use the same exact numbers.

**(g) Approach diagram.** Yes, the pilot is **iteration 1 of the loop**: (1) Measure: done. (2) Model: done as v0 (simple damage functions, frequency and strength derived; no physical fitting yet). (3) Train: pretraining tried (A3 failed) and E1 augmentation done; E2–E4 planned. (4) Evaluate: first look only (held-out ink loss, real CATMuS test); new media and scripts are future. (5) Analyse: first look on IAM (invariance vs error). The arrow back ("refine and repeat") is Phase 2.

**(h) Dataset numbers.** IAM 6,482 / 976 / 2,915, 657 writers: correct. CATMuS ~195k lines (194,808): matches the HF split sizes. Two fixes: **IIIT-INDIC-HW-WORDS** is 872K words in **8** scripts (10 only when you add the older Devanagari and Telugu sets), and **Muharaf**'s 36,311 lines is the **whole** dataset; only 1,216 of 1,644 pages are public. Both fixed on the slide.

**(i) "What we compared" box.** Redone: **Baseline** (few labelled lines, random start) → **Test 1, pretraining** (no damage / hand-picked / derived) → **Test 2, augmentation, no pretraining** (same three plus the clean-up control).

**(j) Baselines: why some cells were empty.** Each dataset was run only at its own label budgets: IAM at 10% (648 lines) and 1% (65), CATMuS at 5% (1,188). 5% of CATMuS gives about the same number of labelled lines as 10% of IAM (~1k), and the pilot week had no time for every combination. The table is now "all / few / very few labels" with the line counts, and the one missing run says "not run". The note on repeats was also wrong (the all-labels rows have 1 run each); fixed.

**(k) Slides 28–29, the A2 graphs, from zero.**
- **Purpose:** Our whole idea is "copy the damage of real pages". That only makes sense if real damaged pages are *measurably different* from clean ones. A2 checks this. If nothing differed, the derived recipe would be "no damage".
- **What each graph is:** We compute one number per line (e.g. how bright the paper is) for 3,000 clean IAM lines and 3,000 real CATMuS lines, and draw two histograms on top of each other (grey outline = IAM, green = CATMuS). If the two shapes sit in different places, that kind of damage is really present in old pages.
- **Why 8 graphs but 6 damage measures and 7 damage types:** 8 graphs = 6 damage measures + 2 "scale" measures (stroke width, ink fraction). Each of the 6 damage types we train with has one measure (tone → paper level, show-through → faint grey, stain → background unevenness, fade → contrast, blur → sharpness, noise → pixel noise). The 7th type, **ink loss**, is held out for testing, and its measure (ink fraction) mostly reflects pen size and script (CATMuS strokes are thicker), so it is not a damage signal. A note on slide 29 now says this.
- **Why KS D:** The two-sample Kolmogorov–Smirnov distance compares two whole distributions, not just their averages. Sort each dataset's values, draw "share of lines at or below x" for both, and D is the biggest vertical gap between the two curves. It needs no assumption that the data is bell-shaped (ours is skewed), it is always between 0 and 1, and it does not depend on the units of the measure, so all 8 measures can share one threshold.
- **Why 0.5:** D = 0.5 means there is a cut-off value where, say, 75% of CATMuS lines are below it but only 25% of IAM lines are: half the lines on one side, clearly separated. It is a judgement call for a "large" difference, set **after seeing the medians but before computing D** (say this plainly if asked).
- **Result:** only paper level (0.82) and faint grey / show-through (0.84) pass; 3 were needed → A2 fails. What it means: real old pages differ mainly in **paper tone and show-through**, which is why the derived recipe applies tone to 84% and show-through to 89% of lines.

**(l) How the damage is chosen.**
- **Hand-picked** (the usual practice, lwti/damage/derive.py `handpicked()`): every one of the 6 damage types is applied with a 50% chance, at a strength drawn evenly between our "low" and "high" levels, chosen by eye before any results. No measuring at all.
- **Derived** (recipe v0, lwti/damage/derive.py):
  1. **Strength scale:** add one damage (say tone) to clean IAM lines at 11–15 strengths and measure its statistic each time (paper level). That gives a curve: strength → measured value.
  2. **Which real lines are damaged:** for each CATMuS line, look at its paper level. If it is darker than 95% of clean IAM lines (outside IAM's 5–95% band), call it "damaged by tone", and read its strength off the curve.
  3. **Recipe:** share of damaged lines = how often to apply that damage (tone 84%, show-through 89%, stain 37%, fade 26%, noise 11%, blur 5%); their strengths = how strong (sampled from the stored distribution).
- **Limit of v0:** a gap between IAM and CATMuS also includes script, pen and scanner differences, not only damage. Phase 2 fits a physical model per damage type.

**(m) Pretraining: numbers and process.** All table numbers match results/runs.csv (CATMuS 5%: 33.8 / 33.3 / 35.0 / 33.4; IAM 10%: 19.9 / 20.4 / 21.0 / 20.5; IAM 1%: 43.3 / 43.8 / 44.7 / 43.9). Scratch is the mean of 3 runs (2 for IAM 1%), pretrained columns of 2.
**Process:** (1) Pool = 30,244 unlabelled lines (CATMuS + IAM training lines with their text thrown away; no validation or test lines). (2) Random 512-px crops, batch 64, 12,000 steps, ~34 min each. (3) Optional damage (none / hand-picked / derived) is added to the crop, then 60% of the 8-px vertical strips are blanked. (4) The CRNN's CNN encodes the masked line, and a small decoder must rebuild the **clean** pixels; loss = mean squared error on the hidden strips. (5) Keep the CNN weights, put them into a fresh CRNN, and train the whole CRNN with CTC on the few labelled lines (8,000 steps; 3,000 for IAM 1%). Note: the two CATMuS derived runs differ by 1.5 points (32.7 vs 34.2), so the seed spread is sometimes larger than 0.5.

**(n)** "Read with care" removed from A4 (slide 31 box and the speaker notes of slide 25).

**(o) Why-pretraining slide.** "Wrong yardstick" card removed. Three cards remain (too little data, now with the Lacuna 750k-line comparison; start washed out; easy task). The Kišš & Hradiš box now explains the paper properly (see A3), including the correction that they *did* beat scratch.

**(p) Augmentation, from the top.** Intuition: a student sees the same sentence printed on stained, faded, blurred copies, and the answer is always the same. To get it right, they learn to ignore the stains. That is augmentation: change the training image, keep its label. We add fake damage to the labelled training lines, drawn anew on every pass, so the model never sees the same damaged copy twice. No pretraining, no extra data. Four versions are compared: none, hand-picked damage, derived damage, and a control that removes paper tone with a filter instead of learning (does simple clean-up do the same?). **The picture**, top to bottom: 4 real CATMuS training lines as they are; the same 4 with hand-picked damage (2 random draws each: noise, blur, heavy fade); with derived damage (2 draws each: mostly greyer paper and faint ghost strokes, like real pages); after the clean-up filter. Validation and test lines are never damaged. The slide now opens with the intuition and explains the picture.

**(q) Derived damage on clean IAM, and slide 34's conclusions.** The derived recipe was copied from **CATMuS's** damage (dark paper, show-through). Clean IAM test lines have none of that, so the derived damage has nothing to target there; it only acts as general noise, the same as hand-picked. Hand-picked is broader (blur, noise, fade at 50% each), which is a slight general regulariser on IAM. 18.8% vs 18.9% is a tie within noise, not a win. On real CATMuS lines, where the copied damage exists, derived wins clearly (31.6% vs 33.6%). Slide 34 now has three conclusion boxes: real-line gain (≈3× the seed spread); not just a clean-up (filter only 33.0%); clean IAM is a tie and why. Honest footnote kept: the gain on damaged quarters is about the same as on all lines, so we say "helps on CATMuS", not "targets damage".

**(r)** Robustness slide deleted.

**(s) Invariance, explained.** Invariance = "the model's inner picture of the line does not change when the damage is added", i.e. the model has learned to ignore that damage. Your summary is correct: take 500 IAM test lines; for each, run the clean line and the same line with one synthetic damage through the **CNN** (before the BiLSTM); the CNN gives **384 numbers per column**; average along the line → one 384-number vector per line; standardise each of the 384 numbers using the clean lines' mean and spread (so no single big feature dominates); cosine similarity between the clean and damaged vectors (1 = pointing the same way = damage ignored); average over the 500 lines. That is one invariance score per damage type and strength (7 × 3 = 21). Then compare with the **CER rise** = damaged CER ÷ clean CER. Title is now "How we measure invariance (our current choice)", and the step cards mention 384 numbers and IAM lines. (Code: lwti/eval/invariance.py, `pooled_features` and `invariance`.)

**(t)** RQ3 preview slide removed. The speaker note on the research-gap slide that pointed to it was updated. If a panel member asks anyway: "Across 21 damage settings, the more a model ignored a damage, the less it raised the error (rank correlation about −0.9), on IAM with synthetic damage; it survives a control for raw pixel change. CATMuS is next."

**(u) Conclusion.** Removed the CER full form, the seeds bracket, the honest-summary band and the RQ3 line; added "A4 pass: derived damage is never worse than hand-picked"; E1 now says what it is.
- **Seed** = the random number that fixes a run's random choices (starting weights, order of lines, which damage is drawn). Running the same experiment with seeds 0, 1, 2 gives three repeats; their spread shows how much of a difference could be luck (~0.5–1 point here).
- **E1 augmentation** = experiment 1: labelled lines shown with fake damage while keeping the same text (see p). It is the first rung of the Phase 2 ladder and the one result that clearly worked.

**(v) Next steps.** Title now "Next steps (Phase 2 plan, tentative and subject to change)".
- **E2, consistency:** use unlabelled lines. Show the model a clean and a damaged copy of the same line and train it to give the **same reading** for both (no transcription needed). Cheaper than full pretraining, uses unlabelled data, and directly trains the invariance we measure, so it is the real test of H3 (the sign-flip prediction).
- **E3, one bounded SSL retry:** fix the pilot's likely problems: about 10× more unlabelled lines (e.g. more of CATMuS, run on Kaggle), a gentler fine-tuning schedule, a public pretrained encoder. Fixed stop date, whatever the result.
- **E4, new damage:** a second pair of datasets in the **same** script but with different damage, to check that the gain comes from damage and not from IAM-vs-CATMuS script differences.
- **Phase 3, script transfer:** not "transfer learning" in the usual sense. The model cannot read a new script without retraining: a new script needs its own character set and its own recogniser. The question is whether our **method** carries over: measure the new collection's damage, derive its recipe, train, and see whether the derived damage still helps and invariance still predicts errors. The deck used to name only Arabic (Muharaf, because it has real damaged manuscript lines). It now says "e.g. an Indic script (IIIT-INDIC) or Arabic manuscripts (Muharaf)". Note: IIIT-INDIC is word images, not lines, and has no stated licence, so Indic needs a check with the authors.

### Other deck changes made today
- Slide 23: CATMuS numbers written exactly (23,762 / 1,243 / 4,022).
- Slide 31: the pretraining box states the pool (30,244 lines) and that the model must rebuild the clean line.
- Slide 35 (invariance): the x-axis/y-axis wording referred to the deleted chart; it now says "pairs".
- Literature slide and references: PreP-OCR venue → ACL 2025, result now numeric.
- The deck is 42 slides (was 44). Backup of the old source: /tmp/claude-1000/-home-vignesh-Desktop-research/d812886f-ac72-4483-9c19-74992d7616cb/scratchpad/slides_before_1119.md (temporary folder).
