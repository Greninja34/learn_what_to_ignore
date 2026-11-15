# Landscape: self-supervised learning for degraded text recognition

Status as of 9 Nov 2026. Builds on the handoff (Part 5 and the Part 7 landscape notes, Oct 2026). Only the new searches from this pass are marked **[new]**.

## 1. The field in four lines

- **Generic SSL for scene and handwritten text** is mature. Contrastive (SeqCLR, CCD), distillation and masked-prediction methods all exist. A 2024 critical survey (IJCV 2025) found the methods were rarely compared fairly and used inconsistent protocols.
- **Degradation-aware pretraining** is the closest prior work to the project. Text-DIAE (AAAI 2023) pretrains on masking, blur and background-noise pretext tasks, and its degradations are hand-picked.
- **Masked autoencoding for handwriting** is growing. Text-MAE adapts a ConvNeXt-v2 masked autoencoder to handwritten lines with a text-specific masking strategy **[new]**. Kišš & Hradiš (ICDAR 2024) reports that target-domain SSL does not consistently beat transfer from a related domain.
- **The most important recent result** is arXiv 2609.35473 (Garrido-Munoz & Calvo-Zaragoza, Sep 2026). On six handwriting benchmarks, pixel-reconstruction pretraining gives the lowest CER, while contrastive and JEPA methods lose. Encoder alignment with the high-variance pixel subspace predicts CER across methods.

## 2. Closest work, by what it does

| Work | What it does | Relation to the project |
|---|---|---|
| Text-DIAE (arXiv 2203.04814, AAAI 2023) | Degradation-invariant autoencoder; masking, blur, noise pretext tasks | Closest on *degradation invariance*. Degradations are hand-picked, not derived |
| 2609.35473 (Sep 2026) | Six SSL methods, matched conditions; high-variance subspace explains CER | Sets the context. Reconstruction beats augmentation-invariance objectives for HTR |
| Text-MAE (IRISA) **[new]** | Fully convolutional MAE with a text-specific mask and a two-phase curriculum | Same objective family, different masking. Relevant as the MAE baseline |
| Lacuna Reconstruction (NAACL Findings 2022) **[new]** | Pretrains on masked regions by picking the true region over distractors from the same line | Claims invariance to scribal style and print noise. A non-pixel alternative to test against |
| CSSL-MHTR **[new]** | Continual MAE pretraining across scripts | Shows scripts can be added incrementally. Not about degradation |
| Kišš & Hradiš (arXiv 2405.00420, ICDAR 2024; 2503.22513, 2025) | Masked label prediction; 50M-line pretraining reported at up to about 30% relative CER reduction | Code base for the baseline (pero-pretraining). Their finding on transfer limits the claim |
| SeqCLR (2012.10873), CCD (2211.00288) | Contrastive / character-level SSL for STR | Motivate invariance questions, but neither studies erased diacritics or merged strokes |
| Critical survey (arXiv 2407.19889, IJCV 2025) | Review and protocol critique | Source for the "augmentation choice is ad hoc" claim |
| Augraphy (arXiv 2208.14558) | Document degradation library | Hand-designed degradations already exist, so the novelty must be in *deriving* the set |
| Ericsson et al. (arXiv 2111.11398) | Invariance and transfer in SSL (general vision) | Source of the invariance measures the project would use. Not yet replicated for text |

## 3. What the field does not yet answer

The 2609.35473 result sharpens the question. Nobody has yet:

1. **derived** the set of degradations for a reconstruction objective from measured statistics of real historical lines, rather than hand-picking them;
2. measured, per degradation family, how much the trained invariance matches the variation at test time, and whether that predicts CER increase on an unseen script or degradation.

Lacuna Reconstruction and Text-DIAE show that invariance-style reconstruction can help, but neither ties its invariance to a measurement of the variation.

## 4. Draft research-gap statement (for the ESA answer sheet)

> Self-supervised text-recognition pretraining relies on augmentations or degradations chosen by hand. Recent evidence shows that pixel-reconstruction objectives outperform augmentation-invariance objectives for handwriting, and that the discriminative signal lies in high-variance pixel directions. Still unknown is which degradations a reconstruction model should learn to ignore, derived from the measured statistics of real degraded text, and whether the invariance it learns predicts robustness on unseen degradations and scripts.

Check the wording against the final literature list before the review.

## 4b. Update, 9 Nov 2026 (evening): full read of 2609.35473 and a 2026 sweep

**2609.35473 is now verified on arxiv.org** (v1 28 Sep, v2 16 Oct 2026, **accepted at NeurIPS 2026**). Read in full via the arXiv HTML; figures were not readable.

- Compares MAE, SimMIM, I-JEPA, V-JEPA-2, MoCo-v3 and SigLIP with one ViT-B-scale encoder (≈114M params, 64×4 px vertical-strip patches, 64×1024 canvas) on IAM, RIMES, Bentham, LAM, Rodrigo and Parzival. Pretraining uses ≈12.5M synthetic rendered lines or the union of the six real training sets.
- Frozen encoder + BiLSTM-CTC probe, full labels, mean CER: MAE 5.5%, SimMIM 8.7%, V-JEPA-2 10.6%, SigLIP 14.5%, I-JEPA 14.7%, MoCo-v3 19.2%. MAE at 10% labels reaches 8.8%, below every JEPA or contrastive method at 100%. At 1% labels everything struggles (Parzival: MAE 95.6% CER).
- Their predictor of CER is an "R²-gap" between high- and low-variance pixel-PCA directions. It works on PCA directions, not on types of damage.
- **Augmentation is hand-picked and unspecified:** "a fixed augmentation pipeline" of affine, blur, brightness/contrast jitter, "low-amplitude" noise, ink dilation/erosion and cutout, described only as "small", "mild" and "low", with no numeric ranges and no stated selection procedure. Degradation, bleed-through and robustness are not studied, and future work does not mention them.
- **Consequence for us:** it confirms the method choice (reconstruct pixels) and leaves the gap intact. Their augmentation section is a direct example of the problem statement.

**2026 sweep (extended web search, 9 Nov).** Nothing found that derives image corruptions for text-recognition pretraining from measured statistics of real lines. New items to cite:

| Work | What it does | Relation |
|---|---|---|
| LoGo-HTR (WACV 2026) | Contrastive SSL pretraining then supervised fine-tuning for HTR | Another SSL-for-HTR baseline, contrastive family |
| FP-THD (arXiv 2601.17040, Jan 2026) | MAE + ViT line recogniser inside a full-page historical pipeline | MAE is becoming standard for historical lines; not about degradation |
| WSCL-2HTR (Springer 2026, snippet only) | Continual SSL pretraining for historical HTR | Not about degradation |
| ICDAR 2026 HIPE-OCRepair (arXiv 2607.08143) | Synthetic OCR errors from confusion matrices **estimated from the data** | Closest "fit the corruption to data" idea, but at the **text** level (post-correction), not image |
| RAG Hanja restoration (arXiv 2607.21936) | Corruption rate sampled to match the real damage distribution | Same idea, text level |
| PreP-OCR (arXiv 2505.20429) | Synthetic degradations for restoration before OCR | Hand-set degradation levels; restoration, not pretraining |

**Sharpened claim:** fitting corruption statistics to real data has been done for *text-level* OCR errors. Doing it for *image-level* damage, to choose what a reconstruction-pretrained recogniser should ignore, and testing whether per-damage invariance predicts the CER rise, still appears open as of 9 Nov 2026. ("Not found" is not "proven absent.")

## 5. Gaps in this pass

- The search tool returned almost nothing from 2026 for any query other than 2609.35473. This does not show that no 2026 work exists. A proper check needs arXiv listing searches for "handwritten text recognition", "text recognition self-supervised" and "document OCR pretraining", filtered to 2026, or an extended search.
- ~~2609.35473 was checked through a mirror page~~ Verified on arxiv.org and read in full on 9 Nov (see 4b). Its figures could not be read, so per-budget JEPA/contrastive numbers are still unchecked.
- Kišš & Hradiš was checked from search summaries. Check the paper itself before citing its numbers.
- Text-MAE was found through the IRISA project page. Its date and venue are not confirmed.
