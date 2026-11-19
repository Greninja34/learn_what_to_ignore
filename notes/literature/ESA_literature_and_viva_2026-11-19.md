# ESA prep, 19 Nov 2026: literature, research gap and answers to your slide questions

Part A is the literature: every paper in the deck, with its core idea, how it works (implementation), what it found, its limit for us, and a likely viva question.
Part B is the research gap and the literature survey as you would tell it.
Part C answers your questions (a)–(v) and lists every change made to the deck.

Labels used below: **[verified]** = checked today against the paper or its abstract; **[from memory]** = standard, well-known facts, not re-checked today.

---

## Part A. The papers

### A1. Garrido-Munoz & Calvo-Zaragoza, *Handwritten Text Recognition Lives in the High-Pixel Variance Subspace*, arXiv 2609.35473, Sep 2026, accepted at NeurIPS 2026 [verified: abstract]
- **Problem:** For natural photos, contrastive SSL usually beats pixel reconstruction. For handwriting, the opposite seems true. Why?
- **Core idea:** In handwriting images, the information needed to read the text sits in the **high-variance pixel directions** (think of the main components of a PCA on pixels: strokes vs paper). Methods that rebuild pixels are forced to model those directions, while contrastive/JEPA methods can ignore them.
- **How:** Six SSL methods from three families (masked image modelling = pixel reconstruction, JEPA, contrastive), all with the same encoder, data and evaluation. Six handwriting benchmarks, five languages. They measure how well each encoder lines up with the high-variance pixel subspace.
- **Findings:** Pixel-reconstruction methods get the lowest CER on every benchmark; they are the only family that gains from pretraining on real handwriting; they are more label-efficient; within each method, alignment with the high-variance subspace predicts CER.
- **Why it matters to us:** It is the reason we chose **reconstruction (MAE-style)** pretraining and not contrastive. It also made us reframe: the question is no longer "which SSL family" but "which damage should the model learn to see through".
- **Limit for us:** No damage study; clean benchmarks.
- **Viva Q:** *Why MAE and not contrastive?* → Because for handwriting, reconstruction wins (this paper); contrastive needs augmentations that keep the text identity, which is hard for text.

### A2. Penarrubia, Valero-Mas & Calvo-Zaragoza, *Self-Supervised Learning for Text Recognition: A Critical Survey*, IJCV 2025 [from memory]
- **What it is:** The survey of SSL for text recognition (handwritten and scene text).
- **Core content:** Sorts methods into **discriminative** (contrastive such as SeqCLR, non-contrastive), **generative** (masked image modelling, e.g. MAE-style, Text-DIAE) and hybrids. Shows that papers use different protocols (different backbones, label budgets, datasets), so results are hard to compare, and that **augmentations are picked ad hoc**.
- **Why it matters to us:** It is the evidence that "how to choose the augmentations / corruptions" is an open, recognised problem. Our gap starts here.
- **Viva Q:** *Is your gap real?* → The field's own survey says augmentations are chosen ad hoc and protocols are not standard.

### A3. Kišš & Hradiš, *Self-supervised Pre-training of Text Recognizers*, ICDAR 2024 [verified: abstract]
- **Problem:** Can unlabelled historical lines replace costly transcriptions?
- **How:** Pretrain a line recogniser's encoder on unlabelled lines, then fine-tune with different amounts of labels. Two families: **masked label prediction** (the model predicts a discrete code for masked parts; codes from Feature Quantization, VQ-VAE or Post-Quantized AE) and **joint-embedding** (VICReg, NT-Xent). They add an **image-shifting trick** so the joint-embedding model does not "cheat" by using only position encodings and ignoring the image. Data: historical handwriting (Bentham) and historical printed text. Code: github.com/DCGM/pero-pretraining (BSD-2).
- **Findings:** Pretraining on target-domain data is **very effective compared with training from scratch**, but it **struggles to beat transfer learning** from a closely related labelled domain.
- **Why it matters to us:** (1) supervised transfer is a mandatory baseline; (2) it shows SSL is not a free win; (3) it is our starting code reference.
- **Careful:** Our pilot did *not* beat scratch, which is weaker than their result. The honest reading is "our scale (30k lines, 34 min) was too small", not "pretraining never helps". The old slide said they found pretraining "does not always beat supervised training", which blurred this; the slide now states it correctly.
- **Viva Q:** *Your pretraining failed. Does the literature agree?* → Partly. K&H show pretraining beats scratch but not transfer; our failure to beat scratch most likely comes from scale (Lacuna used 750k lines, we used 30k).

### A4. Vogler, Allen, Miller & Berg-Kirkpatrick, *Lacuna Reconstruction: Self-Supervised Pre-Training for Low-Resource Historical Document Transcription*, Findings of NAACL 2022 [verified: paper text]
- **Core idea:** Like BERT's masked-word task, but on images: hide regions of a line image and make the model **pick the true hidden region out of distractors** taken from the same line (contrastive, not pixel rebuilding).
- **How:** Convolutional feature extractor, then an LSTM or Transformer for context; pretrained on unlabelled lines; fine-tuned with CTC on very few transcribed lines. Data: Islamicate (Arabic-script) manuscripts and early-modern English printed books (Old Bailey).
- **Findings:** Gains over training from scratch with as few as **30 labelled lines**. With **750k pretraining lines**, CER on Attar-Mubhij drops from **60.4% to 23.7%** in the 30-line setting.
- **Why it matters:** Shows SSL works with tiny label budgets on historical data, and that it used ~25× more unlabelled lines than our pilot.
- **Limit for us:** Masking/corruption is not matched to real damage.

### A5. Mitra, Mondal & Jawahar (IIIT Hyderabad), *Learning Beyond Labels: Self-Supervised Handwritten Text Recognition (LoGo-HTR)*, WACV 2026 [verified: search results]
- **Core idea:** Two losses during pretraining: a **local contrastive loss** (neighbouring parts of the same word image should stay consistent) and a **global decorrelation loss** (features should not all collapse to the same thing; like VICReg's covariance term).
- **How:** Pretrain on **SSL-HWD**, a new word-level set of about 10M images from 852 writers (2.08M labelled, 7.92M unlabelled); then fine-tune a transformer decoder with limited labels.
- **Findings:** Beats prior state of the art on HTR benchmarks, including multilingual and historical ones, even with 20% of the labels.
- **Limit for us:** Contrastive/decorrelation family, word level, no damage study. Note the scale: 10M images.

### A6. Aberdam et al., *Sequence-to-Sequence Contrastive Learning for Text Recognition (SeqCLR)*, CVPR 2021 [from memory]
- **Core idea:** The first contrastive SSL for text. A text image is a **sequence**, so instead of contrasting whole images it splits the feature sequence into small windows ("instances") and contrasts matching windows between two augmented views.
- **Key detail:** Augmentations must keep left-to-right alignment (no big horizontal crops or flips), which shows how **delicate augmentation choice** is for text.
- **Findings:** Better than supervised training in low-label settings on handwriting (IAM, RIMES, CVL) and scene text.
- **Use in our deck:** Named in the research-gap table as an example of hand-chosen augmentations.

### A7. Souibgui et al., *Text-DIAE: A Self-Supervised Degradation Invariant Autoencoder for Text Recognition and Document Enhancement*, AAAI 2023 [from memory]
- **Core idea:** Pretrain a transformer autoencoder to **undo three degradations**: masking, blur and added background noise. Input is degraded, target is the clean image, so it learns degradation-invariant features.
- **How:** ViT-style encoder, a light decoder for pretraining; afterwards the encoder is used for text recognition (with a sequence decoder) or for document enhancement.
- **Findings:** Competitive or better than contrastive methods like SeqCLR on handwritten and scene-text recognition, with less pretraining data and no negative pairs.
- **Why it is our closest neighbour:** It is "pretrain with damage, rebuild the clean image", exactly our ConvMAE setup. **Gap:** its degradations and strengths are hand-picked, and it does not test on held-out damage types, media or scripts.
- **Viva Q:** *How are you different from Text-DIAE?* → They choose the damage by hand; we derive which damage, how often and how strong from measurements of real pages, and test on damage held out of training.

### A8. Guan et al., *PreP-OCR: A Complete Pipeline for Document Image Restoration and Enhanced OCR Accuracy*, ACL 2025 [verified: abstract]
- **Core idea:** Fix the image first, then fix the text.
- **How:** (1) Make synthetic training pairs by rendering plain text with varied fonts and layouts and applying randomly ordered degradations; train an image-restoration model (with multi-directional patch extraction and fusion for large pages). (2) Run OCR. (3) A ByT5 language model, fine-tuned on synthetic historical text pairs, corrects remaining errors.
- **Findings:** On 13,831 real historical pages (English, French, Spanish), CER is 63.9–70.3% lower than OCR on raw images.
- **Limit for us:** Damage is synthetic with hand-set ranges; it restores images instead of making the recogniser robust.
- **Deck fix:** the venue was wrong (arXiv); it is ACL 2025. Fixed on the literature slide and in the references.

### A9. Kanungo, Haralick, Baird, Stuetzle & Madigan, *A Statistical, Nonparametric Methodology for Document Degradation Model Validation*, TPAMI 2000 [from memory]
- **Background:** Kanungo's earlier degradation model (1993) for **binary** (black/white) scans: pixels flip with a probability that depends on their distance from a stroke edge, then a morphological closing.
- **This paper's idea:** How do you know a degradation model is realistic? Treat it as a statistics question: compare **distributions** of local pixel patterns in real vs synthetic images with a nonparametric two-sample test (permutation/bootstrap), and pick the parameters that make them indistinguishable.
- **Why it matters:** This is the old root of "fit damage to real scans". It is **not** our novelty, and we say so. Our step is to link the fit to what a **deep** recogniser learns to ignore.
- **Echo in our work:** Our A2 check also compares distributions (with the KS distance).

### A10. Baird, *The State of the Art of Document Image Degradation Modelling*, in *Digital Document Processing*, Springer 2007 [from memory]
- **What it is:** A survey of physics-based degradation models (blur from the optics, thresholding, pixel sensitivity, jitter, speckle), how to estimate their parameters from real images, and how to validate them.
- **Why it matters:** Supports our "physical form + fitted parameters" step and our claim that only some damage (capture, show-through) has clean physical models.

### A11. Groleau et al., *Augraphy: A Data Augmentation Library for Document Images*, arXiv 2208.14558, 2022 (ICDAR 2023) [from memory]
- **What it is:** A Python library of realistic document damage organised in three phases: **ink** (bleed, low ink, ink shifts), **paper** (texture, stains, folding, bleed-through) and **post** (lighting, shadows, JPEG, scanner effects). Each effect is a class, so you can switch one off.
- **Use:** Made the ShabbyPages dataset; used for denoising and robustness.
- **Limit for us:** Which effects to use, and how strong, is left to the user. That is exactly the choice we try to derive.
- **Our implementation note:** In the pilot we wrote our own 7 simple damage functions (lwti/damage/families.py) instead of Augraphy, so we can control and measure each one.

### A12. Ericsson, Gouk & Hospedales, *Why Do Self-Supervised Models Transfer? Investigating the Impact of Invariance on Downstream Tasks*, BMVC 2022 [from memory]
- **Core idea:** SSL models learn to ignore ("be invariant to") the augmentations used in pretraining. Different downstream tasks need different invariances: e.g. ignoring colour helps object recognition but hurts tasks where colour matters.
- **How they measure it:** Pass an image and its transformed version through the encoder, standardise the features, and take the cosine similarity: high = invariant.
- **Findings:** Invariances to different augmentations (spatial vs appearance) help different tasks; mixing models with different invariances transfers better.
- **Our use:** Our invariance score follows their style (see C-s below). **Limit:** natural images only; we apply it to text recognition and to document damage.

### A13. Mintun, Kirillov & Xie, *On Interaction Between Augmentations and Corruptions in Natural Corruption Robustness*, NeurIPS 2021 [from memory]
- **Core idea:** Augmentations help robustness mainly when they are **similar to the test corruptions**. They define a distance between augmentation and corruption distributions (Minimal Sample Distance) and show it predicts the error.
- **Striking result:** Models tuned on ImageNet-C partly overfit to its corruption types; on a new set of dissimilar corruptions (ImageNet-C̄) the gains shrink.
- **Why it matters:** It is the strongest argument for deriving damage from real pages: if training damage must resemble test damage, measure the test damage. It is also why we hold out ink loss: to test damage the model never saw.

### A14. He et al., *Masked Autoencoders Are Scalable Vision Learners (MAE)*, CVPR 2022 [from memory]
- **How:** Cut the image into patches, hide 75% at random, encode only the visible ones, a light decoder rebuilds the hidden pixels, loss = mean squared error on hidden patches. After pretraining, the decoder is thrown away.
- **Our version (ConvMAE, lwti/models/conv_mae.py):** Same idea on the CRNN's own CNN: hide 60% of 8-px vertical strips of the line, rebuild the clean pixels; damage is added to the input before masking, so the model must rebuild the clean line (masked + denoising autoencoder). We moved from a ViT to a CNN because the small ViT memorised the few labelled lines.

### A15. Shi, Bai & Yao, *An End-to-End Trainable Neural Network for Image-based Sequence Recognition (CRNN)*, TPAMI 2017 [from memory]
- **How:** CNN turns the line into a sequence of feature columns → bidirectional LSTM reads the sequence → **CTC** loss aligns the output with the text without per-character positions. No character segmentation needed.
- **Our version (lwti/models/crnn.py):** 7.4M parameters, 64-px high grey lines, CNN outputs 384 numbers per column (one column per 4 px of width).
- **CTC in one line (Graves et al., ICML 2006):** the model outputs a letter or "blank" for each column; repeats and blanks are collapsed ("hh-e-ll-ll-o" → "hello"), and the loss sums over all alignments that give the right text.

### A16. Clérice et al., *CATMuS Medieval: a multilingual large-scale cross-century dataset in Latin script for HTR*, ICDAR 2024 [partly verified]
- Medieval manuscript lines from many projects, 8th–16th century, about 10 languages, all in Latin script, with shared transcription guidelines (abbreviations kept as written). On Hugging Face: about 195k lines (153k train / 19.4k val / 22.6k test), CC BY 4.0.
- **Our use:** the source of **real damage**: measuring it, pretraining, and testing. The test split is from manuscripts not seen in training.

### A17. Marti & Bunke, *The IAM-database*, IJDAR 2002 [from memory]
- Modern English handwriting, 657 writers. We use the Teklia/IAM-line version on Hugging Face: 6,482 train / 976 validation / 2,915 test lines, writer-independent split (no writer appears in both train and test).
- **Our use:** clean baseline, and the clean base onto which we add synthetic damage.

### A18. PaddleOCR (PP-OCR series), PaddlePaddle [from memory]
- An industrial OCR toolkit: text detection → orientation check → line recogniser. We use only its recogniser, off the shelf, as a "what does a ready-made OCR get" reference: 11.4% CER on IAM, 52.5% on CATMuS (it was never trained on medieval script).

### A19. Background named in the deck but not in the reference list
- **VICReg** (Bardes, Ponce & LeCun, ICLR 2022): joint-embedding SSL with three terms: **v**ariance (keep each feature dimension spread out), **i**nvariance (two views should give similar features), **c**ovariance (dimensions should not be redundant). In our objective 4 as a "non-reconstruction" control. Not run yet.
- **Recto–verso / show-through models** (e.g. Sharma, IEEE TIP 2001, show-through cancellation in duplex scans): show-through is modelled as a blurred, attenuated, mirrored copy of the back page added to the front. Our show-through damage follows this idea in simplified form.

---

## Part B. Literature survey and research gap, as you would say them

**The story in four steps:**
1. **SSL for text works, but its recipe is hand-made.** SeqCLR, Lacuna, Text-DIAE, Kišš & Hradiš and LoGo-HTR all pretrain on unlabelled lines and gain when labels are few. The survey (Penarrubia 2025) notes that augmentations are chosen ad hoc. Garrido-Munoz 2026 shows reconstruction is the right family for handwriting.
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
