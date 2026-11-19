# Literature update, 15–16 Nov 2026 (paper-scout searches)

Method: six `paperscout find` queries (prof-scout's OpenAlex + Semantic Scholar search, summaries by a free LLM). **Everything below comes from titles and abstracts only. Nothing here was read in full.** Check each item with `bin/paperscout read <id>` before citing a number. Titles for some entries were cut off in the search table; verify the exact title and venue.

Builds on `landscape_2026-11-09.md` (still valid for the main claim).

## 1. Biggest correction to our novelty claim

Estimating degradation-model parameters from real scans, and using the fitted model to generate training data, is **old work (1994–2007)**. Our "derive the damage from measurements" step is therefore not new in itself.

| Work (abstract level) | What it did |
|---|---|
| Document Degradation Models: Parameter Estimation and Model Validation (1994) | Hypothesis-testing method to estimate and validate degradation parameters from real page images |
| Estimation of morphological degradation parameters (1995) | Nonparametric estimation of structuring-element sizes from real scans to make similar synthetic data |
| Document degradation models and a methodology for validation (1996); Global and local document degradation models (2002, Kanungo/Baird line) | Local pixel-level and perspective/illumination models; large synthetic training sets with ground truth |
| A statistical, nonparametric methodology for degradation model validation (2000) | Permutation tests to pick the model closest to real data |
| Document image quality: making fine discriminations (1999) | Bootstrapping test; about 25 reference images suffice to estimate six parameters |
| Morphological degradation models and their use in restoration (2002) | Estimated parameters reduced CER by 16.1% (relative reading of the abstract; check) |
| The State of the Art of Document Image Degradation Modelling (2007) | Review; open problems: comparing models, sound use of synthetic data |

**Consequence:** cite these as the root of the "fit the degradation to real data" step. The new part must be: (a) doing it for *deep recognisers that learn what to ignore*, (b) the link recipe → trained invariance → measured robustness (RQ3), (c) the comparison against hand-picked recipes on real damaged lines. Reword the research-gap statement accordingly.

## 2. Closest recent work (abstract level)

| Work | Relevance |
|---|---|
| Learning Beyond Labels: Self-Supervised HTR (LoGo-HTR, Mar 2026) | SSL pretraining on 10M word images, dual loss; reported gains with 20–80% labels. Scale far above ours |
| Self-supervised Pre-training of Text Recognizers (Kišš & Hradiš, 2024) | Target-domain SSL is effective but struggles to beat transfer from a closely related domain. Explains our A3 result |
| Optimal Transport for HTR in a Low-Resource Regime (Sep 2025) | Iterative pseudo-labelling of high-confidence alignments; supports self-training as the engine (E2) |
| Self-training for handwritten word recognition and retrieval (2024) | Synthetic-data initial models then self-training beat adaptation-free methods |
| Training transformer architectures on few annotated data: historical HTR (2024) | Small-data strategy; relevant baseline for the few-label setting |
| Text-MAE (Jan 2026) | MAE for handwritten lines, ConvNeXt-v2 style; venue still unverified |
| Handwritten Text Recognition Lives in the High-Pixel Variance Subspace (2609.35473, Sep 2026) | Already read in full on 9 Nov |
| Efficient Domain Adaptation for Text Line Recognition (Feb 2026); Synthetic Lines from Historical Manuscripts (Jan 2024); Danish HTR synthetic lines (Aug 2026) | Domain-adaptation and synthetic-line work for historical HTR; check for the closest baselines to E1/E4 |
| MaskAug: corruption-aware augmentation (Sep 2026) | Architecture-agnostic, corruption-aware augmentation (domain unclear from the title); check whether it matches augmentation to test-time corruption |

**Not found:** consistency regularisation evaluated for HTR with few labels (the search said direct evidence is absent). That is an opening for E2, but "not found" is not "absent".

## 3. Side project / fallback (VLM OCR hallucination)

Hits: *Seeing is Believing? Mitigating OCR Hallucinations in multimodal LLMs* (Jan 2025), *Perceptual Hallucination in Vision–Language Models* (Jan 2026), and several general object-hallucination papers. The general-hallucination literature is large; hallucination **under controlled document damage**, with a ground-truth-free detector, was not found in this search. Needs a focused second pass before committing.

## 4. Still to do

- Read in full: LoGo-HTR, Kišš & Hradiš, Optimal Transport HTR, Text-MAE, one Kanungo/Baird estimation paper, MaskAug.
- Check the two "check figures" flagged items (Training transformers on few data; Self-training word recognition).
- Venue and deadline list (ICDAR 2027, DAS, ICFHR, WACV workshops, IJDAR) from the conference sites, not from memory.
- Dataset check for a same-script, different-damage pair (E4).
- Raw outputs: `paper-scout/reports/2026-11-15-*.md`.
