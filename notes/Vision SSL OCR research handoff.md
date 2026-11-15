# Handoff: Vision SSL / OCR research planning — full context

Exported 2026-10-13 from a Claude (Cowork) session for use in a Claude Code session.

**Who:** MN (undergrad-level researcher, India, timezone Asia/Calcutta). Knows some ML and maths.
**Hardware:** one RTX 4060 Mobile laptop GPU (8 GB VRAM), plus free Kaggle (P100 / 2×T4, ~30 h/week) and Colab.
**Current decision:** pursue **Idea 1 — "Learning What to Ignore: Deriving Invariance for Self-Supervised Text Recognition"** (reconstruction-based SSL, derived corruptions). Side ideas the user may do alone: Rubik's-cube training-distribution study, VLM OCR-hallucination study, possibly an Indian-language OCR benchmark.
**Next step the user said:** "I will get back to you after I have an understanding of it myself" — i.e. they are studying, then want help implementing.

## File layout of this handoff

1. Part 1 (this part): conversation log — every user message verbatim, a faithful account of each assistant reply, and all artifact links.
2. Part 2: content of the two Claude Docs created (crash course + project starter pack), with every link.
3. Part 3: the user's original memo "Twelve Openings in Vision SSL" (artifact text, HTML stripped).
4. Part 4: the friend's critique (pasted by the user, verbatim).
5. Part 5: Deep-research report 1 — "Vision SSL ideas reality check".
6. Part 6: Deep-research report 2 — "OCR hallucination cube and benchmarks".
7. Part 7: All raw research notes behind both reports (with URLs and [UNVERIFIED] flags).

## Artifacts / links created in the session

| What | Link |
|---|---|
| User's original memo "Twelve Openings in Vision SSL" (HTML artifact, rev. 2, Aug 2026) | https://claude.ai/code/artifact/af4d48c4-1297-4048-9314-57d76f948d3a |
| Doc: "One-Week Crash Course: Physics-Derived Augmentation for Degraded Documents" | https://claude.ai/code/artifact/747a7731-e76c-4f0d-bae4-597504465231 |
| Doc: "Learning What to Ignore: Project Starter Pack" | https://claude.ai/code/artifact/14a3f2a6-95a0-4ee1-bc0c-bf82e9ceda08 |
| Report file: "Vision SSL ideas reality check.md" | delivered as a file (included in Part 5) |
| Report file: "OCR hallucination cube and benchmarks.md" | delivered as a file (included in Part 6) |

---

## Conversation log

### Turn 1 — User
> (System context: fetch the artifact https://claude.ai/code/artifact/af4d48c4-1297-4048-9314-57d76f948d3a and review it.)
>
> "givne this artifact, what are teh concpets i need to be famialr with given this is the area i want to try and do smtg, not sure if i would do these only but smt gin the realm of this only is fine but still. find outeb videos blogs and courses that i can binge watch in a week to have some idea on these matters. assume i knwo a bit of ml and math that's all"

### Turn 1 — Assistant
Read the memo (Part 3). Created a Claude Doc (crash course, 7 days) with a concept checklist and day-by-day videos/blogs/courses. Started generic (ViTs, SSL, invariance, image formation, VLM/interpretability, graphs/small-world/Cayley, RL/MARL). Interrupted by the user mid-build.

### Turn 2 — User
> "i chose the phsyics aug one would liek to elarn those cocnepts first ok?"

### Turn 2 — Assistant
Refocused the doc on memo idea 06 (physics-derived augmentations for degraded manuscripts, SSL + OCR). Final 7-day plan: Day 1 Transformers/ViTs; Day 2 SSL; Day 3 symmetry/invariance/augmentations; Day 4 image formation & processing (Nayar FPCV); Day 5 physics of degraded documents (show-through, bleed-through, iron-gall corrosion, foxing, fading; Augraphy, DocCreator); Day 6 OCR/HTR (CTC, Scheidl, TrOCR, SeqCLR); Day 7 hands-on. Noted the user had pasted memo text into the Day 6 section (left in place).

### Turn 3 — User (the exact problem statement)
> "This is problem statement exactly
> **Learning What to Ignore: Deriving Invariance for Self-Supervised Text Recognition**
> Self-supervised learning requires choosing which input variations a representation should discard, yet this choice is made by hand and retuned for every new domain. We ask whether it can be derived instead. Text and document images are an ideal testbed: the variation to be discarded - degradation, medium, script, capture conditions - is severe, highly structured, and often physically modellable, while labels are scarcest where it is worst. We investigate which sources of derived invariance transfer to conditions unseen during pretraining, and what governs the match between trained invariance and encountered variation."

### Turn 3 — Assistant
Updated the crash-course doc: added "The problem" section (statement + table mapping each phrase to concepts/days); rewrote the concept checklist (added variation axes, learned invariance, transfer/domain shift, measuring invariance); Day 6 added the IJCV critical survey of SSL for text recognition (2407.19889) and Union14M scene text; Day 7 morning became "Which invariances transfer, and how to measure the match" (Ericsson et al. 2111.11398 + code, LooC 2008.05659, Amortised Invariance 2302.12712, Augerino 2010.11882, RandAugment 1909.13719, Gulrajani & Lopez-Paz 2007.01434, CKA 1905.00414); afternoon hands-on. Flagged arXiv 2609.35473 ("Handwritten Text Recognition Lives in the High-Pixel Variance Subspace", Sep 2026) as relevant but unread at that time (rate-limited).

### Turn 4 — User
> "given u have gone through this artifact: is the ranking still holding for today's era of research done so far across the ideas presented to u here?? I feel like my #1 choice is hard to do as 1. no idea on the pipeline and 2. the dataset for it at all. also this is what my friend sent me on this artifact an analysis. give ur 2 cents on this now/deep-research"
> [followed by the friend's full critique — see Part 4]

### Turn 4 — Assistant (deep research → report "Vision SSL ideas reality check", Part 5)
Summary given in chat:
- Memo ranking only partly holds. Idea 01 (effective dataset size) — drop as stated: Joshi & Mirzasoleiman ICML 2023 already selects by augmentation similarity on CIFAR-100/STL-10/Tiny-ImageNet. Idea 07 (registers) mostly taken (Lappe & Giese 2025; Jiang et al. 2506.08010; Varma et al. 2610.03698). Small-world attention: BigBird explicitly builds on Watts–Strogatz. Small-world MARL: a 2026 EAAI paper "Small-World Topology and Graph Attention RL for dynamic traffic optimization" exists. Cube idea misdescribes DeepCubeA (uniform scramble length 1–30; 36 h on 2 Titan V + 6 GPUs data gen). Still alive: idea 03 ordinal vs metric depth probe on DINO; idea 02 medium risk (Mintun et al. 2021 predecessor).
- Friend's critique mostly right; slips: Dutch COLING 2025 paper never says "small"; Dual-Pathway Circuits 2605.13156 is object hallucination, not OCR; 2603.19790 is now titled "Geometric Risk Control for Vision-Language Model OCR".
- Keep #1 with a reframe: arXiv 2609.35473 (Garrido-Munoz & Calvo-Zaragoza, 28 Sep 2026) finds pixel-reconstruction pretraining beats contrastive and JEPA on six HTR benchmarks, preserving per-character position info. So "derived invariance" = corruptions applied to the input of a masked/denoising autoencoder, ranges fitted to real historical-line statistics; "what governs the match" = per-family invariance scores (Ericsson) vs CER rise on held-out conditions.
- Datasets: IAM-line on HF (Teklia), HTR-United catalogue, CATMuS Medieval, PARSeq scene-text LMDBs, IIIT-INDIC-HW-WORDS, Muharaf public part. Code: pero-pretraining (Kišš & Hradiš, ICDAR 2024), Augraphy. Always a supervised-transfer baseline.
- 4-week plan: supervised baseline at 1/10/100% → MAE vs contrastive at laptop scale → fit corruptions + pretrain hand-picked vs derived → evaluate held-out conditions + invariance correlation.

### Turn 5 — User
> "give me the exact problem statement now for the idea stat
> also quickly just provide some some insoght on the cubing statemnet and teh oc rhallunications one want to do them myself, also there has been a recent recent paper on pixel to structure bascily a ocr benchamnrk paper, lol even i can do that, there are a very basic shit paper on ocr on korean lanuage and these are in huge as confrences and ajournals, lol even i can do it no?? /deep-research"

### Turn 5 — Assistant (deep research → report "OCR hallucination cube and benchmarks", Part 6)
**Final problem statement (reframed):**
> **Learning What to Ignore: Deriving Invariance for Self-Supervised Text Recognition**
> Self-supervised learning requires choosing which input variations a representation should discard, yet this choice is made by hand and retuned for every new domain. We ask whether it can be derived instead. For handwriting, reconstruction pretraining now beats contrastive and joint-embedding methods, so the choice moves from an augmentation list to the corruptions a masked or denoising autoencoder must see through. Text and document images are an ideal testbed: the variation to be discarded — degradation, medium, script, capture conditions — is severe, highly structured, and often physically modellable, while labels are scarcest where it is worst. We fit corruption ranges to measured statistics of real historical lines, then investigate which sources of derived invariance transfer to conditions unseen during pretraining, and what governs the match between trained invariance and encountered variation.

- RQ1: Do corruptions fitted to real line statistics beat plain MAE and hand-picked (SeqCLR-style) corruptions at 1%, 10%, 100% labels?
- RQ2: Which derived invariances transfer when a whole degradation family, medium, script or capture condition is held out?
- RQ3: Do per-family invariance scores (and overlap with the character-carrying high-variance pixel subspace) predict the CER rise under each held-out family?
- H1 derived < plain MAE and hand-picked in CER at 1% labels (3 seeds); H2 transfer degrades degradation > medium > script; H3 invariance helps for degradations outside the character-carrying subspace and hurts for those overlapping it (ink loss, merged strokes, diacritics) — sign flip; H4 control: VICReg on same derived set loses to derived-corruption MAE.
- Must cite: Text-DIAE (AAAI 2023, hand-picked degradations), Mintun et al. 2102.11273, Ericsson et al. 2111.11398, IJCV survey 2407.19889. Caveat: 2609.35473 only read at abstract level.

**Cube insight:** no paper shows more data *hurts*; EfficientCube (2106.03157) scaling keeps improving; CayleyPy cube paper (2502.13266) flat at 4B/8B/16B states. Open: at fixed budget, distribution over *true* distance × label source (walk length vs non-backtracking vs Bellman vs exact BFS). A 2×2×2 script (3,674,160 states, diameter 14 HTM, ~36 s CPU) showed 10-move random walks end on average 6.44 moves from solved (8.63 for non-backtracking; 52% closer than 10). Closest prior: Hadar, Agostinelli & Shperberg 2511.10264 (sampled vs search-visited distribution mismatch). Code: cayleypy, cayleypy-cube, efficientcube, DeepCubeA, deepxube, gfn-pathfinding.

**OCR hallucination insight:** VLMs "repairing" nonwords into real words is already shown (2601.03714 DeepSeek-OCR study; TextHalu-Bench 2506.05551; "Reading or Guessing" 2605.27750; PAR ACL 2026; CALRD 2606.17953; Grounded Layer Correction). Open: ground-truth-free *detection* of those misreads per token — confidence vs image gain vs logit-lens flip layer vs attention — across legibility × word type (common, misspelling, nonword, random, digits, rare name) × script (Latin + Devanagari). Small models: Qwen3-VL-2B/4B, Qwen2.5-VL-3B, SmolVLM (Spectra library github.com/clemneo/vlm-spectra); PaddleOCR control. Metrics: AUROC, risk–coverage.

**"Even I can do it?" — half right:** "From Pixels to Structure: Lightweight VLMs for Document OCR and Structured JSON Extraction" (arXiv 2610.11818, ICDAR 2026) is a comparison of 8 small VLMs on 3 heritage collections with senior co-authors. Korean: KRETA (EMNLP 2025 main, 2,577 human-reviewed Qs), KOCRBench (arXiv only, 250 Qs), KOFFVQA (CVPR 2025 workshop). NeurIPS "Evaluations & Datasets" track requires public data at submission, Croissant metadata with RAI fields, clear licences. Realistic gap: Indian-language document benchmark (forms, old print, rare scripts, government key-field extraction — Krutrim 2602.16430 says no public benchmark for gov key-field extraction). Plan: 200–500 pages with rights, ~20% double-annotated, 8–15 systems, 3–6 months part-time; target workshop → ICDAR / ACL Findings / IJDAR.

### Turn 6 — User
> "okay say we still go for idea 1
> 1. need like the basics to understnd the field in its entirety please, like yotube videos lectures, pdfs, blogs jsut to udnerstnd what i am tackling
> 2. scope feasibitliy use cases bg datasets literarutre surveya dna ll
> 3. main conern is still datasets like synthetic or ones from google adn akggle should do or is htis lieka s eparate task itself
> 4. implementation rough skcth i will get back to u after i hev a undersatnding on it myself"

### Turn 6 — Assistant
Created doc "Learning What to Ignore: Project Starter Pack" (full content in Part 2): Part 1 learning path (15 ordered resources), Part 2 background/use cases/scope/feasibility/literature, Part 3 datasets (official vs Kaggle vs synthetic; download table; "the one real data task" = tagging a few hundred real test lines by degradation type), Part 4 pipeline diagram + 7-stage implementation table. Verified: CATMuS Medieval on HF ≈195k lines (153k/19.4k/22.6k), CC-BY-4.0, not gated; pero-pretraining repo = "Self-supervised Pre-training of Text Recognizers" (Kišš & Hradiš, ICDAR 2024, arXiv 2405.00420), BSD-2; Teklia HF hosts IAM-line, NorHand v1–v3, POPP, Himanis, Belfort line sets.

### Turn 7 — User
> "Push all the context of this chat everything every message and every link into a MD file please would like to pass it to seesion in Claude code"

### Turn 7 — Assistant
Produced this file.

---

## Suggested first message for the Claude Code session

"Read this handoff. I'm working on 'Learning What to Ignore' (Part 1, Turn 5 problem statement; implementation sketch in Part 2 → Starter Pack Part 4). Hardware: RTX 4060 Mobile 8 GB + Kaggle. Help me set up stage 0: load Teklia/IAM-line from Hugging Face, build a charset, train a small CNN+BiLSTM+CTC (or PARSeq-tiny) baseline at 1%/10%/100% labels, and report CER with jiwer."

---

# Part 2 — Content of the two Claude Docs

## Doc A: One-Week Crash Course: Physics-Derived Augmentation for Degraded Documents
Link: https://claude.ai/code/artifact/747a7731-e76c-4f0d-bae4-597504465231 (as of 2026-10-06; ⭐ = must-do)

### The problem
(Problem statement as in Part 1, Turn 3.) Mapping of statement → concepts → day:
| Part of the statement | Concepts | Day |
|---|---|---|
| "which input variations a representation should discard" | SSL objectives; augmentations define the invariance | 2, 3 |
| "made by hand … can it be derived instead" | Group actions, forward models, learned/automated augmentation | 3, 5, 7 |
| "degradation, medium, script, capture conditions" | Image formation, degradation physics, handwriting vs print vs scene text | 4, 5, 6 |
| "labels are scarcest where it is worst" | Low-label fine-tuning, low-resource HTR | 6 |
| "which sources … transfer to conditions unseen" | Domain generalisation, held-out-domain evaluation | 7 |
| "what governs the match …" | Measuring invariance, invariance–task mismatch | 3, 7 |

### Concept checklist
| Cluster | Concepts | Why it matters |
|---|---|---|
| Transformers & ViTs | Self-attention, patch tokens, encoder–decoder, ViT vs CNN | Backbones and TrOCR are transformers |
| SSL core | SimCLR/InfoNCE, BYOL/DINO, MAE, collapse, linear probing, low-label fine-tuning | The setting |
| Augmentations as invariance | Views, content vs style, InfoMin | "which variations to discard" |
| Symmetry | Groups, actions, orbits, invariance vs equivariance | Vocabulary for "deriving" |
| Image formation | Radiometry, transmittance, sensor noise, blur as convolution, Fourier | Capture/degradation are physical |
| Document degradation | Show-through, bleed-through, ink spread, foxing, iron-gall corrosion, fading | Physically modellable source |
| Text recognition | Line segmentation, CRNN+CTC, attention decoders, TrOCR, CER/WER | How you measure |
| Variation axes | Handwriting/print/scene text, scripts, writers, camera vs scanner | The four axes |
| Learned invariance | AutoAugment/RandAugment, Augerino, LooC, amortised invariance | Alternatives to compare against |
| Transfer & domain shift | Domain generalisation, leave-one-domain-out | "transfer to unseen conditions" |
| Measuring invariance | Invariance scores, CKA, probing | "what governs the match" |

### Day 1 — Transformers and ViTs
- ⭐ 3Blue1Brown: Transformers (DL ch.5) — https://www.3blue1brown.com/lessons/gpt (30 min)
- ⭐ 3Blue1Brown: Attention in transformers (DL ch.6) — https://www.3blue1brown.com/lessons/attention (30 min)
- ⭐ Jay Alammar: The Illustrated Transformer — https://jalammar.github.io/illustrated-transformer/ (45 min)
- ⭐ Hugging Face Community Computer Vision Course (CNN + ViT units) — https://huggingface.co/learn/computer-vision-course (3 h)
- Karpathy: Let's build GPT from scratch — https://www.youtube.com/watch?v=kCc8FmEb1nY (2 h)
- Check: why does a ViT need position embeddings; what is the CLS token for?

### Day 2 — Self-supervised learning
- ⭐ Lilian Weng: Self-Supervised Representation Learning — https://lilianweng.github.io/posts/2019-11-10-self-supervised/
- ⭐ Lilian Weng: Contrastive Representation Learning — https://lilianweng.github.io/posts/2021-05-31-contrastive/
- ⭐ NYU Deep Learning Week 10 (Ishan Misra, SSL in vision) — https://atcold.github.io/NYU-DLSP21/en/week10/10/ (also 10.1 https://atcold.github.io/NYU-DLSP21/en/week10/10-1/, 10.2 https://atcold.github.io/NYU-DLSP21/en/week10/10-2/)
- ⭐ UvA DL Tutorial 17: SimCLR (code) — https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial17/SimCLR.html
- Google Research blog: SimCLR — https://research.google/blog/advancing-self-supervised-and-semi-supervised-learning-with-simclr/
- Meta AI blog: DINOv2 — https://ai.meta.com/blog/dino-v2-computer-vision-self-supervised-learning/
- NYU Week 15: Joint embedding methods — https://atcold.github.io/NYU-DLSP21/en/week15/15-1/ and https://atcold.github.io/NYU-DLSP21/en/week15/15-2/
- A Cookbook of Self-Supervised Learning — https://arxiv.org/abs/2304.12210
- MAE — https://arxiv.org/abs/2111.06377
- Also referenced: Meta I-JEPA blog https://ai.meta.com/blog/yann-lecun-ai-model-i-jepa/ ; DINO paper https://arxiv.org/abs/2104.14294

### Day 3 — Symmetry, invariance, what augmentations do
- ⭐ 3Blue1Brown: Group theory and the monster — https://www.3blue1brown.com/lessons/groups-and-monsters
- ⭐ Visual Algebra lectures (Matt Macauley) — https://www.math.clemson.edu/~macaule/visualalgebra/youtube/
- ⭐ Geometric Deep Learning course — https://geometricdeeplearning.com/lectures/ ; Lecture 3 Geometric Priors I https://youtu.be/qEjWMhRlXgY ; Lecture 8 Groups https://youtu.be/SGiQ3pm06nI (Taco Cohen); Lecture 4 Geometric Priors II https://youtu.be/DpnA8NNUtyU ; Tutorial 2 Group Equivariant NNs Colab https://colab.research.google.com/drive/1h7U15-qFC2yy6roRIfLPk5TSlo6sONsm
- ⭐ What Makes for Good Views for Contrastive Learning (InfoMin) — https://arxiv.org/abs/2005.10243
- SSL with Data Augmentations Provably Isolates Content from Style — https://arxiv.org/abs/2106.04619
- GDL Seminar 3: Equivariance in ML (Geordie Williamson) — https://youtu.be/XPVrVeRmMY0
- Check: if ink bleed is an augmentation, what does the model learn to ignore, and what must it still see?

### Day 4 — Image formation and processing
- Anchor: Shree Nayar, First Principles of Computer Vision — https://fpcv.cs.columbia.edu/ (monographs: https://fpcv.cs.columbia.edu/Monographs)
- ⭐ Image Formation — https://cave.cs.columbia.edu/Statics/monographs/Image%20Formation%20FPCV-1-1.pdf
- ⭐ Image Sensing — https://cave.cs.columbia.edu/Statics/monographs/Image%20Sensing%20FPCV-1-2.pdf
- ⭐ Image Processing I/II — https://cave.cs.columbia.edu/Statics/monographs/Image%20Processing%201%20FPCV-1-4.pdf , https://cave.cs.columbia.edu/Statics/monographs/Image%20Processing%202%20FPCV-1-5.pdf
- ⭐ 3Blue1Brown: Fourier Transform — https://www.3blue1brown.com/lessons/fourier-transforms
- Radiometry and Reflectance — https://cave.cs.columbia.edu/Statics/monographs/Radiometry%20and%20Reflectance%20FPCV-3-1.pdf
- FPCV Binary Images module (thresholding)
- Narasimhan & Nayar: Vision and the Atmosphere — https://www.ri.cmu.edu/publications/vision-and-the-atmosphere (template for a physical forward model)

### Day 5 — Physics of degraded documents
| Degradation | Physics | Image effect | Read |
|---|---|---|---|
| Show-through | light through thin paper | faint blurred mirrored verso | Salerno & Tonazzini, ERCIM News https://ercim-news.ercim.eu/en95/special/highly-degraded-recto-verso-document-image-processing-and-understanding |
| Bleed-through | ink seeps through | stronger, spatially varying | full paper https://openportal.isti.cnr.it/data/2011/206989/2011_206989.pdf |
| Iron-gall corrosion | H2SO4 + Fe(II) attack cellulose | browning halos, cracks, holes | Neevel & Mensch 1999 https://mci.si.edu/node/1254250 |
| Foxing | fungi / metal oxidation | reddish-brown spots | https://www.conservation-wiki.com/wiki/BPG_Foxing |
| Fading/spread/breaks | ink density loss, fibre spread | thin/broken strokes | Kieu et al. ICPR 2012 https://b3p.univ-lr.fr/mvisani/articles/KVC_ICPR12-preprint.pdf |
| Print/scan noise | sensor/print artefacts | speckle, edges | Kanungo https://kanungo.com/ocr.html |
- ⭐ Augraphy https://github.com/sparkfish/augraphy + paper https://arxiv.org/abs/2208.14558 (docs: https://augraphy-doc.readthedocs.io/en/latest/doc/source/augmentations/bleedthrough.html)
- ⭐ DocCreator https://doc-creator.labri.fr/
- H-DIBCO 2014 report https://iapr.org/archives/icfhr2014/wp-content/uploads/2015/02/ICFR2014-H-DIBCO.pdf
- Enhance to Read Better https://arxiv.org/abs/2105.12710
- Exercise: write the show-through forward model in one line; which parameters vary between manuscripts = your random augmentation parameters.

### Day 6 — OCR and HTR
- ⭐ Distill: Sequence Modeling with CTC — https://distill.pub/2017/ctc/
- ⭐ Harald Scheidl: Build a HTR system — https://harald-scheidl.medium.com/build-a-handwritten-text-recognition-system-using-tensorflow-2326a3487cd5
- ⭐ TrOCR — https://arxiv.org/abs/2109.10282 ; HF docs https://huggingface.co/docs/transformers/model_doc/trocr
- ⭐ SeqCLR — https://arxiv.org/abs/2012.10873
- DiG — https://arxiv.org/abs/2207.00193
- HTR survey 2025 — https://arxiv.org/abs/2502.08417
- Historical document DL survey — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8321201/
- kraken — https://kraken.re/main/
- ICDAR 2026 HIPE-OCRepair — https://arxiv.org/abs/2607.08143
- ⭐ SSL for Text Recognition: A Critical Survey — https://arxiv.org/abs/2407.19889
- Union14M (Revisiting STR: A Data Perspective) — https://arxiv.org/abs/2307.08723
- (Note: the user pasted memo idea-06 text into this section of the doc; left in place.)

### Day 7 — Which invariances transfer, and how to measure the match
- ⭐ Ericsson et al., Why Do SSL Models Transfer? — https://arxiv.org/abs/2111.11398 ; code https://github.com/linusericsson/ssl-invariances
- ⭐ LooC: What Should Not Be Contrastive — https://arxiv.org/abs/2008.05659
- ⭐ Amortised Invariance Learning — https://arxiv.org/abs/2302.12712
- Augerino — https://arxiv.org/abs/2010.11882
- RandAugment — https://arxiv.org/abs/1909.13719
- In Search of Lost Domain Generalization — https://arxiv.org/abs/2007.01434
- CKA — https://arxiv.org/abs/1905.00414
- Afternoon hands-on: (1) IAM data https://fki.tic.heia-fr.ch/databases/iam-handwriting-database ; (2) degrade with Augraphy BleedThrough/InkBleed + own show-through fn; (3) pretrain with lightly https://github.com/lightly-ai/lightly or solo-learn https://github.com/vturrisi/solo-learn ; (4) CRNN+CTC fine-tune at 1/10/100%; (5) one-page plan: claim, forward models, held-out condition, baselines (generic, RandAugment, Augraphy), invariance measurement.

### After the week
- Optimal Transport for HTR in a Low-Resource Regime — https://arxiv.org/abs/2509.16977
- The OCR Quest for Generalization — https://arxiv.org/abs/2506.06761
- SSL Cookbook — https://arxiv.org/abs/2304.12210

---

## Doc B: Learning What to Ignore: Project Starter Pack
Link: https://claude.ai/code/artifact/14a3f2a6-95a0-4ee1-bc0c-bf82e9ceda08 (2026-10-12)

**The project in one paragraph.** Pretrain a small text-line encoder on unlabelled line images with a reconstruction objective (mask or corrupt the input, rebuild the clean line). The corruptions are *derived* — ranges fitted to measured statistics of real degraded lines — not hand-picked. Fine-tune a recogniser with few labels, test on conditions held out from pretraining (degradation type, medium, script, capture), and measure whether "how invariant the model is to X" predicts "how much CER rises under X". Data: no need to build a dataset; the synthetic part is your degradation code, which is the contribution.

### Part 1 — Learn the field (ordered)
| # | Resource | What to take |
|---|---|---|
| 1 | https://www.3blue1brown.com/lessons/attention | how transformers mix tokens |
| 2 | https://huggingface.co/learn/computer-vision-course (CNN, ViT units) | encoders |
| 3 | https://lilianweng.github.io/posts/2019-11-10-self-supervised/ | map of SSL |
| 4 | https://atcold.github.io/NYU-DLSP21/en/week10/10/ | why augmentations decide what's learned |
| 5 | MAE https://arxiv.org/abs/2111.06377 | reconstruction objective |
| 6 | https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial17/SimCLR.html | hands-on augmentations |
| 7 | https://www.3blue1brown.com/lessons/groups-and-monsters + https://youtu.be/qEjWMhRlXgY | invariance vocabulary |
| 8 | https://fpcv.cs.columbia.edu/ (Image Formation, Image Processing) | blur, noise, frequency |
| 9 | Salerno & Tonazzini https://ercim-news.ercim.eu/en95/special/highly-degraded-recto-verso-document-image-processing-and-understanding | physical degradation model |
| 10 | https://distill.pub/2017/ctc/ | CTC |
| 11 | Scheidl HTR blog (link above) | HTR pipeline end to end |
| 12 | https://arxiv.org/abs/2407.19889 | SSL-for-text map |
| 13 | Kišš & Hradiš 2024 https://arxiv.org/abs/2405.00420 | closest prior work + code |
| 14 | https://arxiv.org/abs/2609.35473 | why reconstruction beats contrastive for HTR |
| 15 | https://arxiv.org/abs/2111.11398 | measuring invariance |
Weekend-only: 3, 5, 10, 12, 14.

### Part 2 — Scope, feasibility, use cases, background
Background: SSL learns what its corruptions tell it to ignore (Ericsson: tasks want opposite invariances). For text the choice is by hand (IJCV survey: "best fit the nature of the data"; Text-DIAE https://ojs.aaai.org/index.php/AAAI/article/download/25328/25100 uses hand-picked degradations). Sep 2026: pixel reconstruction beat contrastive/JEPA on six HTR benchmarks (2609.35473). Closest outside text: Mintun et al. https://arxiv.org/abs/2102.11273 (augmentation–corruption similarity predicts robustness; natural images, supervised).
Use cases: archives/libraries new collections; low-resource scripts; damaged records; camera capture.
Scope in: line-level images; one 5–25M encoder; 3–5 degradation families; clean HW + one real degraded set + one held-out medium/script; CER at 1/10/100% + invariance scores. Out: layout/segmentation; large VLMs; every damage type; many languages; LMs/post-correction.
Feasibility: compute fits (est. 4–12 GPU-h per pretrain, Kaggle for long ones); data fits; code fits (pero-pretraining https://github.com/DCGM/pero-pretraining , PARSeq https://github.com/baudm/parseq , Augraphy); novelty medium risk; main risk: SSL may not beat supervised transfer from a related labelled set (Kišš & Hradiš) → mandatory baseline.
Literature: IJCV survey 2407.19889; HTR survey 2502.08417; historical DL survey PMC8321201; Kišš & Hradiš 2405.00420; 2609.35473; Text-DIAE; SeqCLR 2012.10873, DiG 2207.00193, CCD 2211.00288; Ericsson 2111.11398, Mintun 2102.11273; Augraphy 2208.14558.

### Part 3 — Datasets
Short answer: ~one week of plumbing, not a separate project.
| Option | Use for | Not for | Verdict |
|---|---|---|---|
| Official research datasets (HF, HTR-United, Zenodo) | everything reported | — | main source |
| Kaggle / Google Dataset Search | finding, quick tests | reported results | many are IAM re-uploads with unclear licences; trace to source |
| Synthetic | derived corruptions on real lines; font rendering for new script | sole test set | must also test on real degraded lines |

| Role | Dataset | Size | Access |
|---|---|---|---|
| Clean HW | Teklia/IAM-line https://huggingface.co/datasets/Teklia/IAM-line | ~10.4k lines 6.48k/976/2.92k | free; cite original IAM terms https://fki.tic.heia-fr.ch/databases/iam-handwriting-database |
| Real degraded | CATMuS Medieval https://huggingface.co/datasets/CATMuS/medieval | ~195k lines 153k/19.4k/22.6k | CC-BY-4.0, not gated |
| More historical | HTR-United https://htr-united.github.io/ (catalog.json; repo https://github.com/HTR-United/htr-united) | dozens | per-dataset licence |
| More line-level | Teklia HF https://huggingface.co/Teklia (NorHand v1–v3, POPP, Himanis, Belfort) | varies | check cards |
| Unseen script Indic | IIIT-INDIC-HW-WORDS https://cvit.iiit.ac.in/research/projects/cvit-projects/iiit-indic-hw-words | 872k words, 10 scripts | word-level, no stated licence |
| Unseen script Arabic | Muharaf https://arxiv.org/abs/2406.09630 | 36,311 lines; 1,216/1,644 pages public | public part |
| Camera capture | PARSeq LMDB bundles https://github.com/baudm/parseq | IIIT5k, IC13, IC15… | free |
| Degradation code | Augraphy https://github.com/sparkfish/augraphy (PyPI https://pypi.org/project/augraphy/) | InkBleed, BleedThrough, LowInk, NoiseTexturize, Jpeg, ShadowCast; no fading/foxing class | MIT, last release Dec 2023 |
Start with: IAM-line + CATMuS Medieval + one held-out probe.
The one real data task: tag a few hundred real test lines by degradation type (not transcription).
Pitfalls: new charset head + Unicode NFC; transcription conventions differ; IAM writer-independent split, never pretrain on test lines; fit derived ranges only on pretraining data; Augraphy page-level effects on lines; pre-render if CPU-bound.

### Part 4 — Implementation sketch
Pipeline diagram (text form):
Row 1 (derive): Real degraded lines (CATMuS, HTR-United) → Measure statistics (contrast, blur, noise, ink) → Fit corruption ranges (hold one family out)
Row 2 (pretrain): Unlabelled lines (IAM + historical) → Corrupt the input (derived damage + masking) → Reconstruct clean line (MAE-style encoder–decoder)
Row 3 (experiment): pretrained encoder → Fine-tune recogniser (CTC head, 1/10/100%) → Test held-out conditions (damage, medium, script: CER); pretrained encoder → Measure invariance (score per damage family)
Row 4: Does invariance predict the CER rise? (correlate across families and severities)

| Stage | Build | Tools | Cost (est.) |
|---|---|---|---|
| 0 Baseline | supervised recogniser on IAM at 1/10/100%; CER via jiwer | PARSeq-tiny or CNN+BiLSTM+CTC | 1–3 h/full run |
| 1 Measure | per-line stats on real degraded lines: contrast, blur (var. of Laplacian), noise, stroke width, bleed | NumPy, OpenCV | minutes |
| 2 Derive | stats → parameter ranges per family; hold one family out | Augraphy + own forward models | main coding |
| 3 Pretrain | corrupted (+masked) input → reconstruct clean; runs: plain MAE, hand-picked, derived | pero-pretraining as base; h=32–64 px; 5–25M params | 4–12 GPU-h each |
| 4 Fine-tune | CTC head, 1/10/100%, 3 seeds at 1% | same as stage 0 | minutes–1 h |
| 5 Test | clean IAM, IAM+held-out damage, real tagged degraded lines, scene text / unseen script | PARSeq LMDB, IIIT, Muharaf | minutes |
| 6 Match | Ericsson invariance score per family×severity vs CER rise | mean-pooled features, whitened distance | minutes |
Build order: 0 end-to-end → 3 with plain MAE → 1–2 → 5–6. Paper comparisons: derived vs hand-picked vs plain MAE vs supervised transfer, on held-out conditions.
Unchecked: Union14M terms, KHATT, Bentham, READ 2016. 2609.35473 read at abstract level only. Compute times are estimates.

---

# Part 3 — User's original memo: "Twelve Openings in Vision SSL" (rev. 2, Aug 2026)
Source: https://claude.ai/code/artifact/af4d48c4-1297-4048-9314-57d76f948d3a (HTML stripped to text)

Twelve Openings in Vision SSL

- 

- 

- 

 Research planning memo · rev. 2Sorted by your interest rankingAugust 2026

### Twelve openings in vision SSL

 Your thirteen directions, assessed against the literature and sharpened into research questions — ordered by the ranking in ideas.md, sized for one 8 GB laptop GPU.

 01 — THE BINDING CONSTRAINT

### What a single 8 GB mobile 4060 actually runs

 This is a meaningfully tighter budget than two desktop cards, and it changes the sequencing rather than the ideas. Being precise about it is what makes the rest of this document honest.

 The 4060 Mobile has 8 GB on a 128-bit bus — about 256 GB/s. For transformer training, memory bandwidth binds before compute does, and the laptop TGP (35–115 W depending on chassis) means sustained multi-day runs will thermally throttle well below peak. Two further details people forget: it is also your display GPU, so usable VRAM is closer to 7.2 GB, and long runs will make the machine unpleasant to use for anything else.

 Sweepable

 ~12 hrsCIFAR-100 / STL-10 / Tiny-ImageNet SSL, ViT-Tiny or ViT-S. Overnight. Run these in dozens.

 Once per paper

 1–2 weeksImageNet-100 DINO-style pretrain, ViT-S, 200 epochs. Multi-crop costs you 4–6×. Not sweepable.

 Effectively free

 ViT-L/14Frozen fp16 inference ≈ 0.6 GB. Probing, activation patching, feature analysis.

 Free cloud top-up

 30 hrs/wkKaggle gives a P100 or 2× T4 — 16 GB, more VRAM than your laptop. Use it for the runs that don't fit.

 That last row matters more than it looks. Kaggle's free weekly allocation and Colab's free T4 both give you more VRAM than your local card. The right pattern is: develop and debug locally where iteration is instant, then push the one or two long runs per paper to free cloud. You likely do not need to pay for compute at all for anything in this document.

 Two practical settings worth applying on day one: cap the GPU with nvidia-smi -pl to something sustainable so thermal throttling doesn't corrupt your timing measurements, and checkpoint every epoch, because laptop runs get interrupted.

 The real consequence: your sweep budget is CIFAR/STL-scale, and your confirmation budget is one ImageNet-100 run. Any idea whose central claim can only be seen at ImageNet-1K scale is out. Any idea whose central claim shows up at CIFAR scale, or on frozen models, is wide open to you.

 02 — YOUR THIRTEEN

### Honest verdicts, in your ranking order

 The single most useful thing I can tell you: most of these are phrased as topic A + topic B. That is a domain, not a research question. "SSL + OCR on degraded documents" does not yet contain a claim anyone could be wrong about — and reviewers reject on exactly that gap. Everything below is about closing it.

 Assessment against current literature · ranked by ideas.md interest

 Your directionTopicsVerdict

 | How little unlabelled data SSL needs | SSL · 1 | Reframe → strong

 | Green SSL | SSL · 1 | Merge into the above

 | SSL + object detection, hard weather | SSL·1 Det·4 SD·6 | Reframe → strong

 | SSL + monocular depth | SSL·1 Depth·5 | Reframe → probe, not method

 | SSL + OCR, historical / low-resource | SSL·1 OCR·3 | Reframe → strong testbed

 | Robust semseg under rain / fog / night | SemSeg · 2 | Crowded as framed

 | Hierarchical attention, high-res semseg | SemSeg · 2 | Avoid — architecture race

 | Hallucination in OCR / VLMs | OCR·3 VLM·7 | Strong

 | Small VLMs + KD for driving perception | VLM·7 SD·6 | Avoid — worst hardware fit

 | Small-world networks + ViTs | SW·8 ViT·7 | Strong — unoccupied

 | Small-world networks + multi-agent RL | SW · 8 | Open — see note

 | Small-world networks + GNNs | SW · 8 | Crowded — surveys exist

 | Too much data as a Cayley/RL bottleneck | Rubik · 9 | Strong — best instinct here

 Two findings worth stating plainly, because they change what you should do:

 Small-world + MARL is more open than it looks. There is a December 2025 paper, Rethinking Multi-Agent Intelligence Through the Lens of Small-World Networks, that sounds like it takes the idea. It does not — it studies LLM-based multi-agent debate with GPT-4o-mini on ARC and GSM8K, not reinforcement learning with learned policies. Small-world communication topology in actual MARL, with credit assignment and learned coordination, is still unclaimed. Its future-work section even hands you the questions: how shortcut density affects consensus, and whether topology can be learned end-to-end.

 Small-world + GNNs is the opposite. This one is genuinely saturated — graph rewiring for over-squashing has multiple surveys, expander graph propagation, curvature-based rewiring, temporal graph rewiring. Going in as an undergraduate means competing with people who have been building that theory for five years. The over-squashing machinery is still valuable to you, but as a tool you import into the ViT and MARL work, not as a target.

 And the one instinct I'd most encourage: "too much data is a bottleneck for Cayley/RL cube solving" is the sharpest thing on your list. It names a counterintuitive effect rather than a topic pair. More on it below.

 03 — THE THREAD

### What almost all of these actually share

 Working through your thirteen, one question keeps reappearing underneath them:

 Does the structure the objective sees match the structure the task needs?

- SSL data efficiency — the augmentation group determines how many of your images are genuinely distinct samples.

- Weather robustness — fog and rain are transformations that sit outside the augmentation group, which is why invariance training doesn't cover them.

- Degraded historical documents — the degradation group is physically modellable, so it can be derived rather than hand-tuned.

- Small-world ViTs and MARL — the graph structure of information flow versus the structure the task's dependencies actually have.

- Rubik's cube — the Cayley graph geometry of where your training data lands versus where you need it.

 That is a research identity, and a defensible one for someone without a large cluster: structure-matching between objective and task. It is a question about what a learning system is looking at, which is answerable at small scale, rather than a question about how much of it — which is not.

 You do not need to commit to that framing now. But it means the ideas below reinforce each other rather than scattering, and by paper four you will have an argument rather than a list.

 Interest rank 1 · Self-supervised learning

### Four SSL-anchored questions

 Your top interest, and — usefully — the area where your compute constraint is least binding, because the open questions here are about mechanism rather than scale.

 01

### The effective size of an unlabelled dataset

 your #13 + #6SSL

### The gap

 The existing literature asks quantity versus diversity, and answers roughly "diversity matters, sometimes more than quantity." That framing has been worked over — surgical vision, uncurated data, pretraining diversity studies. What nobody has asked is the question underneath it: what makes two images count as one sample rather than two, from the objective's point of view?

 Your "green SSL" idea belongs here rather than standing alone. On its own it becomes a measurement paper — CodeCarbon numbers on existing methods — which is exactly the benchmarking shape you said you want to avoid. Attached to a mechanism, the efficiency result arrives as a consequence.

### The claim

 A dataset's effective size for SSL is not its image count. It is the number of distinct equivalence classes under the augmentation group you chose. Two images related by something already inside your augmentation set are one sample to the objective, not two — so strengthening augmentations reduces effective data even while nominal data is constant.

### First experiment

- Define an effective-sample-size estimator: cluster a dataset in a space quotiented by the augmentation group, and count classes rather than images.

- Predict, before training, how far each of CIFAR-100, STL-10 and Tiny-ImageNet can be pruned with no loss under a given augmentation set. Then prune and verify.

- Test the counterintuitive half directly: hold the dataset fixed and strengthen augmentations. Effective size should fall, and downstream performance should fall with it past some point — even though every paper treats stronger augmentation as free.

- Compare objectives. Contrastive, masked modelling and the JEPA family estimate different statistics, so they should have measurably different sample complexity for the same data. Nobody has a theory of why.

### Why this fits you specifically

 The whole experiment lives at CIFAR and STL scale, which is your sweepable range — the constraint becomes the research question rather than an obstacle. And the byproduct is genuinely useful to you: a principled way to prune datasets before training is worth real hours on a laptop GPU.

 Compute
Ideal fit Dozens of CIFAR/STL runs; one ImageNet-100 confirmation

 Prerequisite
Group actions; clustering; some sample-complexity reading

 Novelty risk
Low Diversity work is adjacent, not this

 Venue
ICLR / NeurIPS, or a data-centric-ML workshop first

 02

### Why doesn't SSL give weather robustness for free?

 your #2 + #8SSLSemantic segObject detSelf-driving

### The gap

 Adverse-condition segmentation as normally framed is saturated. ACDC has been the benchmark since 2021, and there is a steady stream of domain-generalisation methods — RFGLNet, BTSeg, multi-teacher photometric mixing, and many more. Another method with better ACDC mIoU is a hard paper to place and a harder one to win.

 But there is an obvious question the entire literature steps over. SSL's foundational premise is invariance to nuisance transformations. Weather is a nuisance transformation. So why does SSL pretraining not confer weather robustness for free? That nobody asks this is the opening.

### The claim

 Because the standard augmentation group does not span the weather manifold. Fog is a depth-dependent, low-frequency, multiplicative transform. Rain is high-frequency additive occlusion with motion structure. Night is a non-linear tone remap plus a noise-floor change. Crop, colour jitter and blur span none of these — so invariance is never trained where it is needed.

### First experiment

- Characterise each weather transform spectrally and geometrically on paired ACDC data, which conveniently gives you the same scenes in clear and adverse conditions.

- Measure the overlap between each weather transform and the span of standard augmentation groups. This is the core measurement and it costs almost nothing.

- Predict robustness from that overlap alone, in advance, then verify against frozen SSL backbones. If the prediction holds, you have explained the field's results rather than adding to them.

- The consequence is a method: derive the minimal augmentation set that spans the weather manifold, and show it beats hand-designed weather augmentation — because it was derived rather than guessed.

### Why the reframe matters

 The same experiments that would have been a leaderboard entry become an explanation. And it reaches three of your interests at once — segmentation, detection, and driving — without needing a fleet or a cluster, because the claim is about transformation geometry, not scale.

 Compute
Mostly frozen ACDC is small; probing + light heads

 Prerequisite
Signal processing; image formation models

 Novelty risk
Low The explanatory framing is unoccupied

 Venue
CVPR / ICCV, or WACV as a friendlier first target

 03

### What does an SSL representation encode about depth, if not scale?

 your #4SSLDepth

### The gap

 Self-supervised monocular depth is a mature field with a well-known wall: scale ambiguity is fundamental, not a bug. Purely self-supervised monocular methods cannot recover metric scale without external priors — ranking-based formulations recover depth only up to an affine transform. Chasing that wall with another photometric-consistency variant is a poor use of your two years.

 Meanwhile, a strange fact sits unexplained nearby: frozen DINOv3 features linearly predict relative depth remarkably well, having never seen a depth label or a stereo pair. Where does that come from?

### The claim

 Emergent depth in SSL features is not learned geometry. It is learned occlusion ordering — a partial order over surfaces, recoverable from the crop-and-match objective, which is exactly the structure that survives when metric scale cannot. That predicts a specific failure signature: SSL depth probes should be near-perfect on ordinal comparisons across occlusion boundaries and much weaker within continuous surfaces.

### First experiment

 Probe frozen SSL backbones for three separable things — ordinal depth across occlusion boundaries, ordinal depth within surfaces, and metric depth — on NYUv2 and KITTI. The prediction is a sharp dissociation between the first and second. Then test causally by retraining small models with occlusion structure manipulated in the augmentation pipeline. This is the depth analogue of asking why segmentation emerges from DINO, and it is a great deal cheaper.

 Compute
Frozen probing Plus small controlled retrains

 Prerequisite
Multi-view geometry basics; probing methodology

 Novelty risk
Low Method space is crowded; the probe question is not

 Venue
3DV / BMVC, then CVPR

 04

### Instantiating the anisotropy oracle for dense tasks

 carried forwardSSLSemantic segDepth

### The gap

 Keeping this from the first pass, because it is still the most theoretically valuable item and it sits in your top interest. LeJEPA proved the isotropic Gaussian is optimal for worst-case downstream risk. Beyond Isotropy in JEPAs then proved that when downstream geometry H is known, the optimum is (c/d)·H⁻¹ — and states plainly that it does not learn or recover H, evaluating only on classification.

 For dense prediction, H is not unknown. Depth labels live on a low-dimensional ordinal manifold; segmentation labels are a partition with known adjacency. You can write H down and test the oracle where the oracle is knowable.

### One caution on scale

 The relevant prior work published on CIFAR-100 and ImageNet-100, which establishes that your scale is acceptable for this line. But this is the most active area in the document — SPHERE-JEPA and its regulariser family arrived within months. If you want this one, it needs to be started within roughly six months, and it is the idea most likely to be taken from under you.

 Compute
Fits, tight CIFAR-100 sweeps; ImageNet-100 via Kaggle

 Prerequisite
Heaviest maths here Covariance and spectral arguments

 Novelty risk
Moderate and rising

 Venue
ICLR / NeurIPS main track

 Interest rank 2–3 · Semantic segmentation, OCR

### Three questions in your middle band

 Your segmentation ideas both need reframing — idea 02 above already absorbs the adverse-weather one. What follows is the remaining segmentation angle plus the two OCR directions, one of which is the strongest standalone item on your list.

 05

### The handoff layer: where the language prior overrides the pixels

 your #5OCRVLM

### The gap

 The empirical signature of OCR hallucination is already documented and it is very specific: VLM substitutions are fluent, in-vocabulary words, whereas classical OCR errors are local recognition noise. The models are reconstructing plausible text rather than transcribing shapes, which makes the errors harder to catch precisely because they read well. Work on ancient Greek editions frames this as "reading or guessing." Robustness studies show over 35% degradation under visual noise.

 All of this is characterisation. The mechanistic question is untouched: at what point in the network does the language prior take over from the visual evidence?

### The claim

 There is a measurable handoff layer. Below it, the output is determined by visual evidence; above it, by the language model's prior. Hallucination is what happens when visual evidence is weak at that specific depth — which means hallucination should be predictable in advance from the evidence strength at the handoff, before any text is generated.

### First experiment

- Take a small open VLM. Use logit lens and activation patching across layers on text crops of controlled legibility — clean, blurred, occluded, low-contrast.

- Locate the crossover: patch visual features from a clean image into a degraded run, layer by layer, and find where it stops changing the output.

- Build the predictor. If evidence strength at the handoff layer predicts hallucination, you have a detection method that needs no ground truth — which is the byproduct application, and a genuinely valuable one.

- Test the sharpest version: hallucination rate should track the language model's prior probability of the invented word, not the visual similarity of the true word. That distinguishes your account from "it just misread."

### Why this is the strongest standalone item on your list

 It is inference-only on frozen models, so your hardware is irrelevant. It hits two of your interests. The phenomenon is real, well-documented and unexplained. And unlike most interpretability work it has an immediate, obvious application — confidence estimation for document pipelines that currently have none. That combination is unusual.

 Compute
Trivial Frozen small VLM inference; 8 GB is plenty

 Prerequisite
Activation patching, logit lens. Very learnable.

 Novelty risk
Low Hallucination work is crowded; the OCR mechanism is not

 Venue
Interpretability workshop → ICLR, or ICDAR

 06

### Deriving augmentations from physics: degraded manuscripts as the ideal testbed

 your #1SSLOCR

### The gap

 SSL for historical and degraded text exists, and it works the way you would expect — apply masking, blur and background noise, learn to undo them. Every method hand-designs its degradation set. Meanwhile the field's stated blockers for historical manuscripts are unknown alphabets, absent language models, scarce labels and degraded images. Low-resource scripts are exactly where you cannot afford to hand-tune an augmentation policy per script.

### The claim

 Historical degradation is physically modellable in a way weather and generic augmentation are not — ink bleed, show-through from the verso, foxing, parchment texture, iron-gall corrosion all have known image-formation models. So the correct augmentation group can be derived from the physics of the document rather than guessed, and a derived group should transfer to a new script with no tuning at all.

### First experiment

 Build forward models for the main degradation processes. Derive the invariance group each implies, and pretrain with it. The decisive test is transfer: take a script the augmentation set was never tuned on — and low-resource scripts are plentiful — and show the physics-derived group matches or beats a hand-tuned one. This is the same structure-matching claim as ideas 01 and 02, validated in the one domain where the true transformation group is actually knowable.

 Worth knowing: ICDAR ran a 2026 competition on LLM-assisted OCR post-correction for historical documents, so there is an active, welcoming community and a natural venue here.

 Compute
Fits well Text recognition datasets are small

 Prerequisite
Image formation modelling; a text recognition pipeline

 Novelty risk
Low Derivation framing is unoccupied

 Venue
ICDAR, then a broader SSL venue for the general claim

 07

### Attention artifacts as a global-prior channel

 carried forwardSemantic segDepthViT

### In brief

 Retained from the first pass as the best low-risk starter project. Since Vision Transformers Need Registers, the settled story is that high-norm outlier tokens in low-information regions are artifacts that harm dense prediction. But outliers occupy low-texture patches — blank walls, sky, road — which are exactly where local evidence for depth is weakest and a global prior is most needed. The field has assumed correlation implies defect.

 The test is cheap and the design is the whole contribution: stratify dense-prediction error by local image entropy, then ablate or redirect the sink using the existing test-time register method. If removing the artifact helps textured regions and hurts low-texture ones, it was a functional channel, not noise.

 It sits at interest rank 2 and 5 rather than 1, so it ranks below the SSL work — but it is inference-only, it is realistically three months, and it builds exactly the probing skills that ideas 03 and 05 need.

 Compute
Trivial Frozen inference + linear probes

 Prerequisite
Careful experimental design. Little maths.

 Novelty risk
Low

 Venue
Workshop → CVPR / ICCV

 Interest rank 7–9 · ViTs, small-world networks, Rubik's cube

### Three from the lower half of your ranking

 Ranked lower by your own ordering, so treat these as parallel side-projects rather than the main line. Two caveats to that: the small-world ViT work is genuinely unoccupied, and the cube idea is the best-formed instinct on your list.

 08

### Small-world attention: inductive bias or just a speedup?

 your #3Small-worldViT

### The gap

 I searched specifically for Watts–Strogatz rewiring applied to ViT attention masks and found nothing, which is surprising given how developed the ingredients are separately. Small-world topology is established in spiking networks and sparse MLPs; 2026 work shows evolutionarily-optimised biological topology beats random sparse graphs as a structural prior. And there is a theoretical hook: recent analysis of transformers through a GNN lens found global attention exacerbates topological bottlenecks rather than resolving them.

### The claim

 Read attention as a graph over patches. Full attention is the complete graph — path length 1, no locality prior. Window attention is a ring lattice — high clustering, long paths. Small-world sits between, giving O(log N) path length from a fraction β of long-range edges. If topology is a real inductive bias, some β* beats full attention on sample efficiency, not merely on cost.

### The discipline this requires

 Sample efficiency is the dependent variable, and that framing is the entire contribution. Every existing sparse-attention paper motivates itself by FLOPs. The moment yours becomes "our sparse attention is fast," it joins a crowded field and loses. Measure the graph quantities directly — characteristic path length, clustering coefficient, Ricci curvature — and predict the depth needed for full mixing as a function of β before verifying it.

 One happy consequence for you: sparse attention makes the experiments cheaper, so this is among the most comfortable ideas here to run on a laptop.

 Compute
Very comfortable Tiny ViTs, CIFAR / Tiny-ImageNet

 Prerequisite
Graph theory basics; networkx does the work

 Novelty risk
Low But dodge the efficiency framing

 Venue
ICLR, or NeurIPS workshop then main track

 09

### Small-world communication topology in genuine multi-agent RL

 your #12Small-world

### Why this is still open

 As noted above, the December 2025 small-world multi-agent paper studies LLM debate, not RL. Learned policies, credit assignment and emergent coordination under a small-world communication graph remain unclaimed, and that paper's own future-work list names the open questions: how shortcut placement and density affect consensus, optimal configurations across tasks, dynamic shortcut pruning, and end-to-end topology learning.

 The sharp version for RL specifically: in MARL the communication graph determines the credit-assignment path length. A small-world graph should give you the sample-efficiency benefit of dense communication at the bandwidth cost of local communication — and there should be a critical β below which credit assignment fails outright. That is a phase transition you can locate, which is a much better result than a reward curve.

 Compute is fine — particle environments and small SMAC-like tasks run comfortably in 8 GB. The real cost is that MARL is a separate literature to learn, and it sits at rank 8 in your ordering. Take it only if the topology thread genuinely grabs you.

 Compute
Fits Small environments; CPU-bound more than GPU-bound

 Prerequisite
New field MARL is a separate literature

 Novelty risk
Low Existing SW paper is LLM-debate, not RL

 Venue
AAMAS, or a NeurIPS workshop

 10

### Why more data doesn't help: the Cayley graph geometry of cube training

 your #10Rubik's cubeSmall-world

### Your instinct is correct, and there's a precise reason

 DeepCubeA and its successors generate training states by random scrambles from the solved state. Here is what that does. The cube group has about 4.3 × 10¹⁹ elements and a diameter of 20 — God's number. The Cayley graph therefore expands so fast that almost every random scramble lands at nearly the same distance from solved, out near the diameter.

 So the training distribution massively over-samples far states and starves the near-solved region. And crucially, more random scrambles do not fix this — they pile up at the same distance. That is exactly the "too much data is a bottleneck" effect you intuited, and it is a graph-geometry phenomenon rather than a quantity one.

### The claim

 The bottleneck in learned combinatorial search is the mismatch between the sampling distribution induced by random walks on a rapidly-expanding Cayley graph and the distribution a value function needs to be accurate on. Data quantity cannot fix a distribution defect. The fix is geometric — sample by distance, not by walk length.

### Why this is a genuinely good paper

 It is a crisp, counterintuitive, correct claim about why scaling fails in a specific setting, and the setting is small enough that you can prove it rather than gesture at it. The concentration of random-walk endpoints is analytically tractable. There is existing scaffolding to build on — CayleyPy RL, and work on cube-graph node classification with GNNs — so you are not starting from zero.

 It also unifies two of your listed interests, since the expansion property doing the damage is the same small-world property you are interested in elsewhere. And it generalises: the 15-puzzle, Sokoban and Lights Out have the same structure, so the claim is about learned search in general, not about cubes.

 The honest caveat is that it sits at rank 9 in your ordering. I would not make it your main line against your own stated interests — but the ratio of insight to GPU-hours is the best in this document, and it is the idea I would pick up first if a main-line run were blocked.

 Compute
Negligible Self-generated data; small networks

 Prerequisite
Group theory; random walks on graphs; some RL

 Novelty risk
Low Small field, clear gap

 Venue
NeurIPS / ICLR — counterintuitive scaling results travel well

 04 — WHAT TO DROP

### Three of your thirteen I would not pursue

### Hierarchical attention for high-resolution segmentation

 This is an architecture race, and a busy one — RingFormer-Seg, TDBAN, UNeXt, Mamba-decoder hybrids, spatially adaptive interaction networks, all in the last two years. Architecture papers for segmentation also collapsed to roughly 1.2% of CVPR highlights. You would be competing on engineering throughput against groups with more compute, for a shrinking slice of attention.

### Small VLMs with knowledge distillation for driving perception

 The worst hardware fit on your list. Distillation needs teacher inference and student training together, which is precisely what 8 GB makes painful. It is also engineering-flavoured — the contribution tends to be a recipe — and it competes directly with industry groups who do this for deployment reasons and have the fleet data.

### Small-world networks + GNNs, as a standalone

 Genuinely saturated. Graph rewiring for over-squashing has multiple surveys, expander propagation, curvature methods, temporal variants. Import the over-squashing machinery as a tool for ideas 08 and 09, where it is underused, rather than entering the GNN theory arena directly.

### And one general warning

 "Green SSL" as a standalone becomes energy measurements of existing methods — a benchmarking paper by another name, which is the shape you said you want to avoid. Folded into idea 01 it works, because the efficiency result then follows from a mechanism instead of standing in for one.

 05 — SEQUENCING

### A revised two-year arc

 Reordered for your interest ranking and the single-GPU reality. The shape: start with something inference-only to build tooling and get a submission out, then move into the SSL core once you know what you are doing.

 Months 0–4

 Idea 05 — the handoff layer in OCR hallucination Inference-only, hits interest ranks 3 and 7, and the strongest standalone item you proposed. Builds the probing toolkit everything else needs. Alternative if you want a gentler start: idea 07.

 Months 3–10

 Idea 01 — effective size of an unlabelled dataset Your top interest, your best hardware fit, and it absorbs the green-SSL idea. CIFAR/STL sweeps run overnight on your card.

 Months 8–15

 Idea 02 — why SSL doesn't confer weather robustness Extends idea 01's group-structure argument into segmentation, detection and driving. Three interests at once, mostly frozen models.

 Months 6–14

 Idea 08 or 10 — small-world ViTs, or the cube data bottleneck Runs in parallel as a deliberately independent line. Both are cheap enough to progress while a main-line run occupies the GPU.

 Months 14–22

 Idea 06 or 03 — physics-derived augmentation, or emergent depth Pick on what ideas 01 and 02 turn up. Idea 06 gives you the ICDAR community; idea 03 stays in the vision mainstream.

 If it survives

 Idea 04 — the anisotropy oracle Highest theoretical value, but the space is moving fast. Check arXiv before committing; if SPHERE-JEPA's successors have taken it, drop it without regret.

 Aim workshop-first on the opening two. At this stage reviewer feedback on a three-month cycle is worth more than the venue prestige, and workshop papers can be extended into main-track submissions.

 06 — SOURCES

### What this is built on

 Load-bearing citations, roughly by how much weight they carry above.

 Rethinking Multi-Agent Intelligence Through the Lens of Small-World Networks — arXiv:2512.18094. LLM debate, not RL — this is why idea 09 is still open.

 LeJEPA — arXiv:2511.08544, and Beyond Isotropy in JEPAs — arXiv:2605.20107, which proves the (c/d)·H⁻¹ oracle and leaves recovering H open.

 SPHERE-JEPA — arXiv:2605.26900, and its regulariser family, arXiv:2606.17603. Evidence of how fast this space moves.

 Reading or Guessing? Visual Grounding Failures of VLMs for OCR in Ancient Greek Editions — arXiv:2605.27750. Fluent in-vocabulary substitutions.

 How Robust is OCR-Reasoning? — arXiv:2606.26041. The 35% degradation under visual noise.

 From Plausibility to Verifiability: Risk-Controlled Generative OCR — arXiv:2603.19790.

 Solving the Rubik's cube with deep RL and search — DeepCubeA, Nature MI 2019.

 CayleyPy RL: Pathfinding and RL on Cayley Graphs — arXiv:2502.18663, and Node Classification and Search on the Rubik's Cube Graph with GNNs — arXiv:2501.18580.

 Vision Transformers Need Registers — ICLR 2024, and Vision Transformers Don't Need Trained Registers — arXiv:2506.08010.

 Understanding the Failure Modes of Transformers through the Lens of GNNs — arXiv:2512.09182. Global attention exacerbates bottlenecks.

 Graph Rewiring in GNNs to Mitigate Over-Squashing: A Survey — arXiv:2605.00951. Why small-world + GNN is saturated.

 Evolutionarily Optimized Network Topology as a Structural Prior — bioRxiv 2026.

 ACDC: The Adverse Conditions Dataset with Correspondences — ICCV 2021. Paired clear/adverse scenes make idea 02 cheap.

 RFGLNet — Sci Rep 2026, and BTSeg — arXiv:2308.16819. Representative of the crowded adverse-weather method space.

 Exploring the Effect of Dataset Diversity in SSL — arXiv:2407.17904, and On Pretraining Data Diversity for SSL — arXiv:2403.13808.

 Are Large-scale Datasets Necessary for Self-Supervised Pre-training? — arXiv:2112.10740.

 ICDAR 2026 HIPE-OCRepair Competition — arXiv:2607.08143. Active community for idea 06.

 Optimal Transport for Handwritten Text Recognition in a Low-Resource Regime — arXiv:2509.16977, and The OCR Quest for Generalization — arXiv:2506.06761.

 Adaptive Depth-converted-Scale Convolution for Self-supervised Monocular Depth — arXiv:2604.07665. Current state of the scale-ambiguity wall.

 Emerging Properties in Self-Supervised Vision Transformers — DINO, and DINOv3 — arXiv:2508.10104.

 CVPR 2026 accepted-paper trends — source of the subfield-share figures.

 Revision 2 · August 2026 · Recalibrated for a single 8 GB RTX 4060 Mobile and reordered to the ideas.md ranking. The JEPA-geometry line (idea 04) is moving fastest — re-check arXiv before committing to it.

---

# Part 4 — Friend's critique of the memo (pasted by the user, verbatim)

**My strongest recommendations are character-preserving SSL for OCR, evidence-aware OCR correction, and OCR-aware document retrieval.** They connect several of your interests, support clear experiments, and can be scoped to the 8 GB GPU budget described in your memo.

I read the entire linked artifact and searched related research. **The memo is useful for brainstorming, but its claims of "unoccupied," "low novelty risk," and "trivial compute" are often too strong.** Below is my assessment, based on literature accessible on 11 October 2026. These are promising research directions, not certified novelty claims.

**Where the memo needs correcting**

1. **Augmentation-aware SSL data selection already has close prior work.** ICML 2023 research selects examples using expected augmentation similarity and gives generalization guarantees. Your effective-dataset-size idea needs to go beyond counting augmentation-equivalent samples—for example, predicting which pruning strategies transfer between objectives. [Data-Efficient Contrastive SSL](https://proceedings.mlr.press/v202/joshi23b.html)

2. **OCR language-prior hallucination is already being studied mechanistically.** PAR investigates models "reciting" familiar text and intervenes on positional encoding and visual attention. Activation-patching work also identifies hallucination pathways in VLMs. An OCR-specific causal study could contribute, but "find where language overrides vision" is no longer enough by itself. [PAR, ACL 2026](https://aclanthology.org/2026.acl-long.1065/), [Dual-Pathway Circuits](https://arxiv.org/abs/2605.13156)

3. **Small-world attention and MARL are not empty territory.** BigBird combines local, random, and global connections; Vision Big Bird extends related ideas to vision. I also found work explicitly combining small-world topology with MARL for traffic optimization. This does not settle your precise hypothesis, but it invalidates the broad "unclaimed" framing. [BigBird](https://arxiv.org/abs/2007.14062), [Vision Big Bird](https://arxiv.org/abs/2311.05988), [Small-World Traffic Optimization](https://www.sciencedirect.com/science/article/pii/S0952197626002009)

4. **Several mathematical claims are hypotheses presented as facts.** Cropping, occlusion, and ink loss are generally not invertible, so they do not automatically form transformation groups. Likewise, having segmentation labels does not immediately identify the positive-definite downstream geometry assumed by the JEPA oracle result. That mapping would itself require justification. [Beyond Isotropy in JEPAs](https://arxiv.org/abs/2605.20107)

5. **Frozen inference still has a compute budget.** Activation patching requires repeated forward passes and activation storage. Sparse attention only saves runtime if implemented efficiently; applying a mask to dense attention may save little. Distillation can use cached teacher outputs, so teacher and student need not occupy GPU memory simultaneously.

**Evaluation of your existing directions**

| Your direction | Verdict | How I would sharpen it |
|---|---|---|
| How little unlabeled data SSL needs | **Keep; substantial overlap** | Predict when a selected subset remains useful across objectives and downstream tasks. Compare against augmentation-similarity selection and random subsets. |
| Green SSL | **Keep as an evaluation axis** | Measure total compute, including selection and tuning, at matched downstream quality. It can also stand alone if the methodological contribution is strong. |
| SSL + detection in difficult weather | **Worth a pilot** | Test whether robustness transfers across corruption types and severities under fixed pretraining budgets. Start with one downstream task. |
| SSL + monocular depth | **Good probing project** | Separate occlusion cues, perspective, texture, and familiar-object size through controlled interventions. Do not assume depth is "only occlusion ordering." |
| SSL + historical/low-resource OCR | **Top choice** | Study which augmentations preserve character identity and transfer to unseen writers, fonts, or scripts. |
| Segmentation under rain/fog/night | **Needs narrowing** | Focus on a specific failure: small objects, boundaries, uncertainty, or adaptation without forgetting. |
| Hierarchical attention for high-resolution segmentation | **Lower priority** | Worth pursuing only with a concrete memory/accuracy constraint and a distinctive hypothesis. |
| OCR/VLM hallucination | **Top choice after reframing** | Study failures on rare names, numbers, deliberate misspellings, and unfamiliar scripts; compare against existing grounding interventions. |
| Small VLM distillation for driving | **Scope-dependent** | Restrict to one perception task and cache teacher outputs. Feasible as an engineering project; research differentiation is harder. |
| Small-world networks + ViTs | **Interesting, medium-to-high novelty risk** | Test sample efficiency at matched edge count, parameter count, and training budget—not topology against an unfair baseline. |
| Small-world networks + MARL | **Higher-risk side project** | Study topology under communication delay, dropped messages, or bandwidth limits. Compare with learned communication graphs. |
| Small-world networks + GNNs | **Too broad as stated** | Pick a measurable rewiring failure or application constraint. A crowded field can still contain useful narrow questions. |
| Excess data in cube/RL training | **Interesting hypothesis; explanation unproven** | Separate dataset size, state distribution, repeated states, and optimizer steps. Begin with a small puzzle where exact distances are available. |

For the cube idea, **"more data does not help" and "more data hurts" are different claims**. Also, sampling by exact distance can be computationally difficult. The official DeepCubeA implementation describes substantial training resources, so "negligible compute" is inappropriate for reproducing the full system. [DeepCubeA repository](https://github.com/forestagostinelli/DeepCubeA)

| Additional proposal | Assessment |
|---|---|
| JEPA anisotropy oracle for dense tasks | **Potentially valuable, mathematically demanding.** First establish what geometry is available without leaking downstream labels into an allegedly self-supervised setup. |
| Attention artifacts as a global-prior channel | **Useful starter experiment, weaker novelty than claimed.** The registers paper already interprets background tokens as being repurposed for internal computation. Texture-dependent causal effects would be the more specific contribution. [Original paper](https://arxiv.org/abs/2309.16588) |
| Physics-derived manuscript augmentations | **Promising component of an OCR project.** A physical simulator does not guarantee character preservation or transfer. Test against simpler corruptions at matched severity on genuinely degraded documents. |

**Six research ideas I would seriously consider**

**1. When does SSL invariance erase distinctions needed for OCR?** *SSL + OCR + representation learning.* Question: Can an augmentation make representations robust to scanning damage while also making different characters indistinguishable? (losing a diacritic, merging adjacent strokes, erasing a small component.) Experiment: controlled character pairs; vary degradation severity; compare generic, text-specific, and identity-preserving policy. Baselines: supervised, SeqCLR, character-level SSL. Measure: CER, confusable-character errors, several label budgets. Contribution: boundary between useful nuisance invariance and harmful semantic invariance. [SeqCLR](https://arxiv.org/abs/2012.10873), [Character-to-Character Distillation](https://arxiv.org/abs/2211.00288). My assessment: best match to your interests and hardware.

**2. When should an OCR correction model leave text unchanged?** *OCR + LLMs + NLP + uncertainty.* Preserve rare but correct names, dates, identifiers, historical spellings. Experiment: mix genuine OCR errors with correctly recognized rare strings; give image crop. Baselines: raw OCR, unrestricted LLM correction, small seq2seq corrector, confidence-based editing. Measure: errors repaired, correct characters damaged, entity exact match, accuracy vs abstention. [Historical Dutch OCR correction](https://aclanthology.org/2025.coling-main.690/), [Geometric Risk Control](https://arxiv.org/abs/2603.19790). Assessment: strong practical project.

**3. Which OCR errors deserve the limited correction budget in a RAG system?** *OCR + IR + LLMs + DS.* Experiment: document QA data; controlled error types; selectively reprocess suspicious spans. Baselines: none, correct all, lowest-confidence first, random. Measure: Recall@k, answer accuracy, evidence correctness, cost. [OHRBench](https://arxiv.org/abs/2412.02592), [When Good OCR Is Not Enough](https://arxiv.org/abs/2605.00911). Assessment: best OCR+LLM+NLP intersection.

**4. Is an SSL subset useful because of the data—or because of the objective used to select it?** *SSL + data selection.* Select subsets with cheap criteria, train two objectives on each; matched steps and matched compute incl. selection overhead. Measure downstream accuracy, robustness, minority-class performance, transfer of subset rankings. Baseline: [ICML 2023 paper](https://proceedings.mlr.press/v202/joshi23b.html). Assessment: best if SSL is main priority.

**5. Do OCR confidence estimates fail specifically on rare words and numbers?** *OCR + VLMs + calibration.* Vary visual legibility and linguistic familiarity with controlled renderings, validate on real images. Baselines: token probabilities, repeated-decoding agreement, geometric consistency, small trained confidence predictor. Measure: error detection and risk–coverage per names/numbers/common/unfamiliar. [Geometric Risk Control](https://arxiv.org/abs/2603.19790), [PAR](https://aclanthology.org/2026.acl-long.1065/). Assessment: good inference-focused start.

**6. Does tabular SSL learn useful structure or shortcuts from missing values?** *SSL + DS + tabular.* Hold task fixed while changing missingness mechanism between train and test. Baselines: trees, supervised NN, masked reconstruction, contrastive tabular SSL. Measure accuracy, calibration, degradation under missingness shift. [Structured missingness](https://arxiv.org/abs/2304.01429), [Recent tabular SSL study](https://arxiv.org/abs/2608.24381). Assessment: best DS alternative.

**What I would choose:** 1. Character-preserving SSL for OCR; 2. Selective OCR correction without damaging rare text; 3. Cross-objective transfer of SSL data selection. Start with one small falsifiable experiment, two credible baselines, and a held-out distribution; postpone the memo's two-year sequence until a pilot gives a reproducible result.

---

# Part 5 — Deep-research report 1: Vision SSL ideas reality check

# Keep the text idea, change its engine

Your #1 problem still deserves to be your #1, but not in its August form. A September 2026 paper, arXiv 2609.35473, finds that **pixel-reconstruction pretraining (masked image modelling) gives the lowest error on all six handwriting benchmarks it tests, while contrastive and JEPA methods, the ones driven by augmentations, lose** ([Garrido-Munoz & Calvo-Zaragoza](https://arxiv.org/abs/2609.35473)). That is a direct hit on a project built around "choosing which variations to ignore" through augmentations. The way forward is to move the question into the reconstruction setting: **derive which degradations to apply to the input of a masked or denoising autoencoder, and measure when that derived invariance carries over to conditions the model has never seen.** Nobody in the notes has derived the invariance set from a model of the real variation, or measured how well trained invariance matches the variation met at test time, for text. Elsewhere, the August memo was too optimistic. Idea 01 (effective dataset size) is largely pre-empted by Joshi & Mirzasoleiman (ICML 2023), and idea 07 (registers) is largely pre-empted by 2025–2026 work. Your friend's critique is factually solid: every cited paper exists. Three things in it are wrong: the friend calls the Dutch paper's models "small" when the paper doesn't, cites a hallucination paper that has no OCR content as if it were about OCR, and gives the wrong title for a 2026 OCR paper. My recommendation is to **keep #1 in its reframed form and start with a cheap two-week warm-up that sits on the same path**: reproduce the reconstruction-vs-contrastive gap on IAM at laptop scale. This report checks nine of the memo's twelve ideas. The other three were not part of this research and are not rated here.

## Three memo ideas fell, two survived in narrower form

The biggest change since August is in the ideas the memo marked "low risk". **Idea 01** proposed that an unlabelled dataset's effective size is its number of augmentation equivalence classes. It runs straight into Joshi & Mirzasoleiman, who already select examples by how similar their augmentations are, claim guarantees, and can remove **about 20% of CIFAR-100 and about 40% of STL-10 and Tiny-ImageNet** without hurting downstream accuracy. Those are the same three datasets the memo planned to use ([PMLR](https://proceedings.mlr.press/v202/joshi23b.html)). The math also needs repair. Crops and occlusions cannot be undone, so augmentations form at best a semigroup, not a group, and the existing non-group tool is the augmentation graph of HaoChen et al. ([arXiv 2106.04156](https://arxiv.org/abs/2106.04156)). **Idea 07** (registers as a global-prior channel) is mostly taken. Lappe & Giese show that global information in large ViTs is dominated by register tokens ([arXiv 2505.05892](https://arxiv.org/abs/2505.05892)). Jiang et al. add registers at test time without any training ([arXiv 2506.08010](https://arxiv.org/abs/2506.08010)). Varma et al., posted on 2 Oct 2026, tie register features to high-level meaning and high-norm outlier tokens to background and texture ([arXiv 2610.03698](https://arxiv.org/abs/2610.03698)).

Two ideas survive in narrower form. **Idea 03** (depth in DINO features): probing frozen features for depth is established, and El Banani et al. found DINOv2 best ([CVPR 2024](https://openaccess.thecvf.com/content/CVPR2024/papers/Banani_Probing_the_3D_Awareness_of_Visual_Foundation_Models_CVPR_2024_paper.pdf)). What I could not find is anyone separating *ordinal* depth (which surface is in front) from *metric* depth. That narrower question is a cheap experiment on frozen features. **Idea 04** (an anisotropy oracle for JEPA on dense tasks) still has a gap: Beyond Isotropy evaluates only classification ([arXiv 2605.20107](https://arxiv.org/abs/2605.20107)), and so does SPHERE-JEPA, which argues for spherical uniformity instead ([arXiv 2605.26900](https://arxiv.org/abs/2605.26900)). But the theory needs a known matrix H that segmentation labels do not give you, and the project requires pretraining JEPAs, so on 8 GB it is a poor bet.

The small-world ideas are weaker than the memo said. BigBird's paper **explicitly builds its attention pattern on Watts–Strogatz small-world graphs** ([ar5iv](https://ar5iv.labs.arxiv.org/html/2007.14062)), and Vision Big Bird carries the same idea over to ViTs ([arXiv 2311.05988](https://arxiv.org/abs/2311.05988)). The only open part is a sweep of the rewiring probability p as a data-efficiency bias. Small-world communication in multi-agent RL is not "unclaimed" either: a 2026 EAAI paper puts small-world topology and graph-attention RL in its title ([record](https://www.synapsesocial.com/papers/69a75c06c6e9836116a24609)). The Rubik's-cube idea misdescribes DeepCubeA. That method **samples scramble length uniformly from 1 to 30**, not only long scrambles, and it trained for **36 hours on two Titan V GPUs, with six more GPUs generating data** ([DeepCubeA PDF](https://deepcube.igb.uci.edu/static/files/SolvingTheRubiksCubeWithDeepReinforcementLearningAndSearch_Final.pdf)). It is only viable if you move it to a puzzle where every state's true distance can be computed exactly, such as the 2×2×2 cube or the 8-puzzle.

## Your friend's facts check out; the shortlist needs one swap

Your friend did careful homework. Every citation resolves, and the technical objections are correct: augmentations are "not a group", H cannot be read off segmentation masks, and the DeepCubeA compute is not negligible. There are three errors and one understatement.

| Friend's citation / claim | Exists? | Says what friend claims? | Note |
|---|---|---|---|
| Joshi & Mirzasoleiman, ICML 2023 (pre-empts idea 01) | Yes | **Yes** | Same datasets, augmentation-similarity selection, guarantees ([PMLR](https://proceedings.mlr.press/v202/joshi23b.html)) |
| Registers paper 2309.16588 (weakens idea 07) | Yes | **Mostly** | Abstract says the artifact tokens sit in background regions and are "repurposed for internal computations"; the "global info" claim is in Lappe & Giese ([arXiv](https://arxiv.org/abs/2309.16588)) |
| Augmentations aren't a group | n/a (math) | **Correct** | The group framework of Chen et al. assumes groups ([arXiv 1907.10905](https://arxiv.org/abs/1907.10905)) |
| Beyond Isotropy needs known H, classification only | Yes | **Yes** | ([arXiv 2605.20107](https://arxiv.org/abs/2605.20107)) |
| BigBird already does small-world attention | Yes | **Understated** | BigBird cites Watts–Strogatz by name ([ar5iv](https://ar5iv.labs.arxiv.org/html/2007.14062)) |
| DeepCubeA compute not negligible | Yes | **Yes** | 36 h, 2+6 GPUs, batch 10,000 ([PDF](https://deepcube.igb.uci.edu/static/files/SolvingTheRubiksCubeWithDeepReinforcementLearningAndSearch_Final.pdf)) |
| SeqCLR 2012.10873, CCD 2211.00288 (motivate char-preserving SSL) | Yes | **Partly** | Real SSL text papers, but neither studies erased diacritics or merged strokes ([SeqCLR](https://arxiv.org/abs/2012.10873), [CCD](https://arxiv.org/abs/2211.00288)) |
| COLING 2025 Dutch post-correction: "small" seq2seq beat generative | Yes | **Overstated** | It says seq2seq models "generally outperform" generative ones (mBART best); "small" is the friend's word ([ACL](https://aclanthology.org/2025.coling-main.690/)) |
| 2603.19790 "From Plausibility to Verifiability…" | Yes | **Wrong title** | Current title: "Geometric Risk Control for Vision-Language Model OCR"; abstains unless views agree ([arXiv](https://arxiv.org/abs/2603.19790)) |
| OHRBench 2412.02592; 2605.00911 (OCR hurts RAG) | Yes | **Yes** | Both benchmark OCR noise in RAG ([OHRBench](https://arxiv.org/abs/2412.02592), [2605.00911](https://arxiv.org/abs/2605.00911)) |
| PAR, ACL 2026 (OCR "recites" rather than reads) | Yes | **Yes** | RoPE phase noise plus attention recycling, about 12% lower CER ([ACL](https://aclanthology.org/2026.acl-long.1065/)) |
| Dual-Pathway Circuits 2605.13156 (as OCR evidence) | Yes | **No** | Object hallucination only, no OCR content; usable as a method template ([arXiv](https://arxiv.org/abs/2605.13156)) |
| Structured missingness 2304.01429; tabular SSL 2608.24381 | Yes | **Yes** | 2608.24381 finds SSL often *hurts* under high native missingness ([arXiv](https://arxiv.org/abs/2608.24381)) |

The shortlist is where I disagree. **Character-preserving SSL (friend's #1)** is now partly pre-empted. 2609.35473 already shows that only reconstruction-based pretraining keeps per-position character information ([arXiv](https://arxiv.org/abs/2609.35473)). It works best as the evaluation axis inside your #1, not as a separate project. **Selective OCR correction (#2)** is a good pick. The ICDAR 2026 HIPE-OCRepair competition names over-correction of clean text as a recurring failure ([arXiv 2607.08143](https://arxiv.org/abs/2607.08143)), and framing it as calibrated abstention is still open. But it is an NLP project, not vision SSL. **Cross-objective data selection (#4)** is the honest rescue of idea 01: does a subset chosen for contrastive learning also help MAE and JEPA? It fits on 8 GB with CIFAR and ResNet-18. Before claiming novelty, you must first search for MAE or JEPA pruning papers from 2024–2026. Of the ideas the friend left out, the **tabular missingness-shortcut** idea deserves more credit than it got. 2608.24381 shows SSL hurting under heavy native missingness but does not test the mechanism, and the test is cheap.

## Revised ranking of every idea

| Rank | Idea (source) | Verdict | Reason |
|---|---|---|---|
| 1 | Learning What to Ignore, reframed (memo #1) | **Keep, reframe** | Derived invariance and the trained-vs-encountered match are both open for text; must move to reconstruction pretraining after 2609.35473 |
| 2 | Selective OCR correction (friend) | Strong alternative | Over-correction is a named open problem ([HIPE](https://arxiv.org/abs/2607.08143)); feasible; off your SSL track |
| 3 | Ordinal vs metric depth in DINO (memo 03) | Good backup | Frozen-feature, cheap; ordinal angle not found in prior work |
| 4 | Cross-objective SSL data selection (friend) | Viable | Turns idea 01 into an extension of Joshi et al.; check MAE/JEPA pruning work first |
| 5 | Tabular SSL missingness shortcuts (friend) | Viable, off-topic | Mechanism untested in [2608.24381](https://arxiv.org/abs/2608.24381); laptop-cheap |
| 6 | Character-preserving SSL (friend) | Fold into #1 | Partly pre-empted by [2609.35473](https://arxiv.org/abs/2609.35473) |
| 7 | SSL weather robustness / augmentation coverage (memo 02) | Medium risk | Mintun et al. already link augmentation–corruption distance to robustness ([arXiv 2102.11273](https://arxiv.org/abs/2102.11273)); a version on real weather images (ACDC) is still possible |
| 8 | OCR confidence on rare words and numbers / "handoff layer" (friend) | Crowded | PAR, OCR heads and late "prior-override" heads already published ([PAR](https://aclanthology.org/2026.acl-long.1065/), [2606.28273](https://arxiv.org/abs/2606.28273)); fitting a VLM on 8 GB is unverified |
| 9 | Small-world attention masks in ViTs (memo) | Narrow only | Mechanism is BigBird; only the p-sweep for data efficiency remains |
| 10 | Rubik's-cube training distribution (memo) | Reframe or drop | DeepCubeA already samples k uniformly; only viable on exact-distance puzzles |
| 11 | JEPA anisotropy for dense tasks (memo 04) | Drop for now | H is ill-posed for dense tasks; JEPA pretraining is too costly for 8 GB |
| 12 | Registers as global prior (memo 07) | Mostly taken | Lappe & Giese, Jiang et al., Varma et al.; only a texture-stratified ablation remains |
| 13 | Effective dataset size = augmentation classes (memo 01) | Drop as stated | Joshi et al.; survives only as #4 |
| 14 | Small-world MARL communication (memo) | Drop | "Unclaimed" is false ([EAAI 2026](https://www.synapsesocial.com/papers/69a75c06c6e9836116a24609)) |
| 15 | OCR-error budget in RAG (friend) | Drop | Two benchmarks already exist; systems/NLP, far from your skills |

## The pipeline, with datasets you can download this week

You said #1 feels hard because you can't see the pipeline and don't know the datasets. Both have concrete answers. The pipeline has five parts: data, pretraining, fine-tuning, evaluation and measurement.

**First, the data.** Your clean labelled set is **IAM lines on Hugging Face (Teklia/IAM-line): about 10.4k lines in fixed train/validation/test splits of 6.48k/976/2.92k, downloadable without registration** ([HF](https://huggingface.co/datasets/Teklia/IAM-line)). The mirror carries an MIT tag, but you should cite the original IAM terms. Your source of real degradation is **HTR-United**, a catalogue of historical HTR ground truth. Its `catalog.json` file lets you filter by script and period, and every dataset lists its own licence and transcription rules ([GitHub](https://github.com/HTR-United/htr-united)). The large medieval set **CATMuS Medieval** is also available on [Zenodo](https://zenodo.org/records/15030337/latest). For scene text as a different capture condition, use the ready-made LMDB archives linked from PARSeq (IIIT5k, IC13, IC15 and others) ([GitHub](https://github.com/baudm/parseq)). For an unseen script, use the **IIIT-INDIC-HW-WORDS** sets: 872K handwritten words in 8 scripts. They are word-level, not line-level ([CVIT](https://cvit.iiit.ac.in/research/projects/cvit-projects/iiit-indic-hw-words)). Another option is the public part of **Muharaf**: historical Arabic, 36,311 lines, but only 1,216 of its 1,644 pages are public ([arXiv 2406.09630](https://arxiv.org/html/2406.09630v2)). For degradations, **Augraphy** (MIT licence) provides InkBleed, BleedThrough, LowInk, Jpeg, ShadowCast, Folding and others as separate classes, which makes it easy to hold out a whole family. Its last release was in December 2023, so pin your dependency versions ([PyPI](https://pypi.org/project/augraphy/)).

**Second, pretraining.** This is the reframing. Your "derived invariance" is the set of corruptions applied to the *input* of a reconstruction objective, with the clean line as the target. You derive the corruption distribution by measuring real historical lines (ink/background contrast, blur, noise level, stroke width) and fitting Augraphy's parameter ranges to those numbers. You fit only on pretraining data, never on test conditions. Compare four encoders, each with the same small CNN or ViT-tiny backbone at line height 64:

1. plain masked autoencoding, with no degradation;
2. masked autoencoding with hand-picked SeqCLR-style corruptions;
3. masked autoencoding with your derived corruptions;
4. a VICReg contrastive model using the derived set, as the invariance-based control.

The **pero-pretraining** code from Kišš & Hradiš already contains masked-prediction and VICReg/NT-Xent variants for historical lines. It also includes their "image shifting" fix, which stops joint-embedding models from collapsing onto the positional encoding ([arXiv 2405.00420](https://arxiv.org/abs/2405.00420); [code](https://github.com/DCGM/pero-pretraining)). Do not start from CCD's code. Its README recommends multiple RTX 3090s for pretraining ([GitHub](https://github.com/TongkunGuan/CCD)).

**Third, fine-tuning.** Attach a CTC head and fine-tune on 1%, 10% and 100% of IAM-train, which is about 65, 650 and 6,500 lines. Use three seeds at 1%, because results vary a lot there. Always include a supervised baseline that transfers from a related labelled domain: Kišš & Hradiš found that target-domain SSL is **not consistently better than that kind of transfer** ([arXiv 2405.00420](https://arxiv.org/abs/2405.00420)).

**Fourth, evaluation.** Hold out whole conditions, not random lines:

- one Augraphy family, e.g. BleedThrough;
- the medium: printed historical lines and scene text;
- the script: Indic or Arabic, with a new character set.

**Fifth, measurement.** This answers "what governs the match". For each degradation family, compute the invariance scores from Ericsson et al.: the Mahalanobis distance and whitened cosine between features of clean and transformed lines ([arXiv 2111.11398](https://arxiv.org/pdf/2111.11398v2)). Also compute 2609.35473's alignment-with-high-variance-pixel-subspace score, then correlate both with the increase in CER under that family. The testable hypothesis: **derived invariance helps when the degradation lies in pixel directions that carry no character information, and hurts when it overlaps the high-variance directions that carry it** (ink loss, merged strokes, diacritics). Your friend's character-preserving idea becomes the test of that hypothesis. One caveat: I saw only the abstract of 2609.35473, so read its exact definition of the subspace measure before you build on it.

Expect plumbing to cause more trouble than the method. The critical survey of SSL for text recognition (IJCV 2025) found that methods were often developed without comparison to each other and with inconsistent protocols ([arXiv 2407.19889](https://arxiv.org/abs/2407.19889)). So fix the image height, character set, case handling and Unicode normalisation on day one, and use the official writer-independent IAM split.

## Conclusion: keep #1, start with a two-week warm-up on the same path

2609.35473 doesn't kill your project. It gives it a sharper question and a ready-made explanatory variable. Before September, "derive the invariance" competed with a crowded augmentation literature. Now the question is narrower: **reconstruction pretraining wins for handwriting, but nobody knows which corruptions it should be trained to see through, or why some of them transfer**. That is a smaller and more answerable question, and your laptop can run small controlled studies of this kind. The real risk is that derived corruptions turn out no better than hand-picked ones. Even then, the per-family invariance-vs-CER analysis is a publishable negative result. Switching to selective OCR correction would trade your SSL focus for an NLP benchmark race. Keep ordinal-depth probing (idea 03) as the fallback if the HTR plumbing stalls.

A plan for the first four weeks follows. The runtimes are my estimates, not measured figures.

| Week | Goal | Concrete output |
|---|---|---|
| 1 | Data and supervised baseline | IAM-line loaded at height 64, character set fixed, CRNN-CTC trained at 1/10/100% labels, CER/WER logged (about 1–3 GPU-hours) |
| 2 | **Warm-up result**: reproduce the reconstruction-vs-contrastive gap | Plain MAE vs VICReg (pero-pretraining) on unlabelled IAM plus about 20k historical lines, fine-tuned at 1%. If MAE wins, you have matched 2609.35473 at laptop scale |
| 3 | Derived corruptions | Measure contrast, blur and noise statistics on CATMuS/HTR-United lines; fit Augraphy ranges; pre-render views; hold out BleedThrough; pretrain MAE with hand-picked vs derived corruptions (offload long runs to Kaggle) |
| 4 | First answer to "what governs the match" | Fine-tune all encoders; evaluate on clean, held-out-degradation, real historical and IC13 scene text; compute per-family Ericsson invariance and correlate it with the CER increase |

---

# Part 6 — Deep-research report 2: OCR hallucination cube and benchmarks

# Keep the SSL question, run two side bets

Your #1 project has a final, defensible problem statement: **derive the corruptions that a masked or denoising autoencoder learns to see through by fitting them to measured statistics of real historical lines, then test which of them transfer to unseen degradations, media, scripts and capture conditions, and whether invariance scores predict the CER cost.** That wording takes on board the September 2026 result that pixel-reconstruction pretraining beats contrastive and JEPA methods on all six HTR benchmarks tested ([arXiv 2609.35473](https://arxiv.org/abs/2609.35473)). It also keeps your original voice. Both side ideas are doable on your laptop, but only in their sharper forms. The Rubik's-cube idea is not "too much data hurts", because nobody has shown that. It is about **which distances the training states come from and how they are labelled, at a fixed budget**, and I confirmed in 36 seconds on a CPU that walk-length labels are badly biased on the 2×2×2 cube. The OCR-hallucination idea cannot simply re-show that VLMs "fix" nonwords into real words, because several 2026 papers already did that. Its open part is **which ground-truth-free signal flags those misreads, broken down by legibility and word type.** On benchmarks, you are half right. The method in those papers really is basic. But the ones at good venues won on real, licensed, human-checked data, broad evaluation and senior co-authors, and the "very basic Korean" ones are mostly arXiv preprints or workshop papers. A careful Indian-language document benchmark is a realistic target for a workshop, for ICDAR or for IJDAR. It is not a realistic target for CVPR.

## 1. The final problem statement

**Title:** Learning What to Ignore: Deriving Invariance for Self-Supervised Text Recognition

**Statement (≈130 words, your voice):**

> Self-supervised learning requires choosing which input variations a representation should discard, yet this choice is made by hand and retuned for every new domain. We ask whether it can be derived instead. For handwriting, reconstruction pretraining now beats contrastive and joint-embedding methods, so the choice moves from an augmentation list to the corruptions a masked or denoising autoencoder must see through. Text and document images are an ideal testbed: the variation to be discarded — degradation, medium, script, capture conditions — is severe, highly structured, and often physically modellable, while labels are scarcest where it is worst. We fit corruption ranges to measured statistics of real historical lines, then investigate which sources of derived invariance transfer to conditions unseen during pretraining, and what governs the match between trained invariance and encountered variation.

**Research questions.**
**RQ1.** Does a masked or denoising autoencoder whose input corruptions are *fitted to real line statistics* beat (a) plain masked autoencoding and (b) the same model with hand-picked, SeqCLR-style corruptions, at 1%, 10% and 100% of the labels?
**RQ2.** Which sources of derived invariance transfer when you hold out a whole degradation family, a medium (print or scene text), a script, or a capture condition?
**RQ3.** What governs the match? Specifically, do per-family invariance scores and overlap with the character-carrying pixel subspace predict how much CER rises under each held-out family?

| # | Falsifiable hypothesis | What would falsify it |
|---|---|---|
| H1 | Derived corruptions lower CER on real historical lines at 1% labels compared with both plain MAE and hand-picked MAE | The gap is within seed spread (3 seeds), or hand-picked corruptions match it |
| H2 | Transfer shrinks as conditions move away from what was fitted: held-out degradation > medium > script | Script transfer equals or beats degradation transfer |
| H3 | Invariance helps when a degradation lies **outside** the high-variance, character-carrying pixel directions, and hurts when it overlaps them (ink loss, merged strokes, diacritics). This shows up as a sign flip in the correlation between invariance score and CER increase across the two groups | One monotone relationship holds across all families, or there is no correlation |
| H4 (control) | VICReg trained on the same derived set loses to derived-corruption MAE, which reproduces 2609.35473 at small scale | VICReg matches or wins. That would mean the reframing itself needs rethinking |

**Why this is new, and what you must cite.** **Text-DIAE** already trains a degradation-invariant autoencoder for text, but with hand-picked degradations, and it found masking the most useful one ([AAAI 2023](https://ojs.aaai.org/index.php/AAAI/article/download/25328/25100); summarised in the [IJCV survey](https://arxiv.org/html/2407.19889v2)). Mintun et al. link augmentation–corruption similarity to robustness, but only on natural images ([arXiv 2102.11273](https://arxiv.org/abs/2102.11273)). Ericsson et al. supply the invariance measures (Mahalanobis distance and whitened cosine between clean and transformed features), but not for text ([arXiv 2111.11398](https://arxiv.org/pdf/2111.11398v2)). The IJCV survey itself says augmentations are chosen to "best fit the nature of the data" and offers no procedure for choosing them ([survey](https://arxiv.org/html/2407.19889v2)). Your contribution is the *derivation* step plus the *match measurement* for text. One caution: I have only seen the abstract of 2609.35473, so read its exact definition of the high-variance-subspace measure before you build H3 on it. Also, a handful of degradation families gives very few points to correlate, so compute the scores per family × severity level.

## 2. The cube idea: label bias is a 36-second fact, so the paper is what follows from it

**Taken vs open**

| Already done | Still open |
|---|---|
| Uniform scramble length k ∈ [1,30] (DeepCubeA) ([PDF](https://deepcube.igb.uci.edu/static/files/SolvingTheRubiksCubeWithDeepReinforcementLearningAndSearch_Final.pdf)) | The **shape** of the training distribution over *true* distance as a variable at fixed budget. Every paper uses uniform k or all prefixes up to K_max, and CayleyPy says it does not study K_max ([arXiv 2502.13266](https://arxiv.org/html/2502.13266v1)) |
| Data scaling: EfficientCube's power law keeps rewarding more data ([arXiv 2106.03157](https://arxiv.org/pdf/2106.03157v5)). CayleyPy is flat at 4B/8B/16B states (21.16/21.12/21.19 moves) ([arXiv 2502.13266](https://arxiv.org/html/2502.13266v1)) | A factorial of label source × distribution, with an exact BFS oracle, on a puzzle where every distance is known |
| "More random walks does not always improve the model". Non-backtracking walks are essential. Spearman correlation vs true distance on small permutation (LRX) graphs ([arXiv 2502.18663](https://arxiv.org/html/2502.18663v2)) | Per-distance-bin bias and its effect on search (nodes expanded, optimality) |
| Train/deploy state mismatch causes "heuristic depression" ([arXiv 2511.10264](https://arxiv.org/html/2511.10264)). Exact-shortest-path GFlowNets ([arXiv 2603.01786](https://arxiv.org/abs/2603.01786)). Overestimating heuristics ([arXiv 2606.04860](https://arxiv.org/abs/2606.04860)) | Whether more walk-labelled data ever *hurts* specific distance bins (nobody shows harm, only saturation) |

**Sharp framing.** *At a fixed sample budget, the distribution of training states over true distance and the source of their labels, not their number, determine heuristic accuracy where search needs it.* This is what "too much data is a bottleneck" was reaching for, stated so it can be tested.

**I ran the pilot.** The script below builds the full 2×2×2 table (**3,674,160 states, God's number 14 in the quarter-turn metric**, matching the known values) and asks what true distance a random walk of length k actually reaches. For simple walks, k = 10 lands at a mean true distance of **6.44**, and 91% of those states are closer than 10. Even with non-backtracking walks (CayleyPy's choice), k = 10 gives a mean of **8.63**, and **52%** are mislabelled as too far. Beyond k ≈ 14, labels keep rising while true distance flattens near 10.5. So H1 from the notes ("walk labels are biased upward in the middle range") is true, and checking it takes no training at all. That makes it **Figure 1, not the paper**. The paper is H2–H4. **H2:** at fixed budget, changing the distribution moves optimality and nodes expanded more than a 10× increase in budget does. **H3:** with walk labels, more data stalls or hurts in specific distance bins, while with BFS labels it keeps improving. **H4:** a mismatch between the training and test distance distributions explains most of the search failures.

**Minimal experiment.** Hold the budget fixed at B ∈ {10⁵, 10⁶} samples, below the 3.67M states so the model cannot just memorise the table. Cross 4 distributions (uniform in k, uniform in true d, uniform random states, near-goal-heavy) with 3 label sources (simple walk, non-backtracking walk, BFS-exact). Use 3 seeds and a small MLP on one-hot stickers. Run A* and beam search on a test set stratified by true distance. Report MAE per distance bin, the admissibility-violation rate, solve rate, optimality gap and nodes expanded.

```python
# cube2.py — tested: 3,674,160 states, God's number 14 QTM, ~36 s and ~670 MB RAM on CPU
import numpy as np
from collections import deque
stickers = [(p, n) for p in np.array(np.meshgrid([-1,1],[-1,1],[-1,1])).T.reshape(-1,3)
            for n in np.eye(3, dtype=int) * p[:, None] if n.any()]
stickers = [(tuple(p), tuple(n)) for p, n in stickers]; idx = {s: i for i, s in enumerate(stickers)}
def move_perm(axis):                      # quarter turn of the +1 layer; corner (-1,-1,-1) stays fixed
    R = np.eye(3, dtype=int); a, b = [i for i in range(3) if i != axis]
    R[[a, a, b, b], [a, b, a, b]] = [0, -1, 1, 0]; perm = np.arange(24)
    for i, (p, n) in enumerate(stickers):
        if p[axis] == 1: perm[idx[(tuple(R @ p), tuple(R @ n))]] = i
    return perm
MOVES = [m for p in map(move_perm, range(3)) for m in (p, p[p[p]])]   # R R' U U' F F'
INV = [1, 0, 3, 2, 5, 4]
SOLVED = np.array([2 * [x != 0 for x in n].index(True) + (sum(n) > 0) for _, n in stickers], np.int8)
def bfs():
    dist = {SOLVED.tobytes(): 0}; q = deque([SOLVED])
    while q:
        s = q.popleft(); d = dist[s.tobytes()]
        for m in MOVES:
            t = s[m]
            if t.tobytes() not in dist: dist[t.tobytes()] = d + 1; q.append(t)
    return dist
def walk_table(dist, K=20, n=20000, nonback=True, seed=0):   # out[k, d] = walks of length k ending at true d
    rng = np.random.default_rng(seed); out = np.zeros((K + 1, 15), int)
    for _ in range(n):
        s, last = SOLVED, None
        for k in range(1, K + 1):
            last = rng.choice([m for m in range(6) if not (nonback and last is not None and m == INV[last])])
            s = s[MOVES[last]]; out[k, dist[s.tobytes()]] += 1
    return out
```

From there, the training loop is ordinary PyTorch. Bucket the BFS keys by distance to sample "uniform in true d", feed the 24 stickers as a 144-dim one-hot vector, regress the label, then plug the network into A*. Starting points for search code are [CayleyPy](https://github.com/cayleypy/cayleypy) (MIT, `pip install cayleypy`), [cayleypy-cube](https://github.com/k1242/cayleypy-cube) and [DeepXube](https://github.com/forestagostinelli/deepxube).

**8 GB note.** No problem at all. BFS runs on the CPU (measured above), and a sub-4M-parameter MLP trains in minutes per run. CayleyPy's single-epoch runs take 1–5 minutes on a P100 ([arXiv 2502.18663](https://arxiv.org/html/2502.18663v2)). By my estimate, the full factorial of about 100–200 runs takes days, not weeks. The only real risk is novelty: no paper I found runs this factorial, but that is "not found", not proven.

## 3. VLM OCR hallucination: the behaviour is known, the detector is open

**Taken vs open**

| Already done | Still open |
|---|---|
| VLM OCR "repairs" toward real words. On random strings, DeepSeek-OCR precision is 19.84% / 42.12% / 61.70% (Tiny/Small/Base). VLMs drop 51–68 points while PaddleOCR drops only ~4.9 ([arXiv 2601.03714](https://arxiv.org/pdf/2601.03714)) | A full **legibility × word-type × script** grid on small open VLMs |
| TextHalu-Bench: 1,740 items; GPT-4o F1 45.3 vs humans 96.8 ([arXiv 2506.05551](https://arxiv.org/html/2506.05551v2)). KIE-HVQA refusal benchmark (NeurIPS 2025) ([arXiv 2506.20168](https://arxiv.org/abs/2506.20168)) | **Ground-truth-free, token-level error detection** scored by AUROC and risk–coverage, compared *across cells*. I found no paper doing this |
| Per-token "image gain" on Ancient Greek, which turns out to be model-specific: olmOCR lexical errors 0.17 vs perceptual 1.40, Qwen3-VL-8B 1.97 vs 1.30 ([arXiv 2605.27750](https://arxiv.org/html/2605.27750v1)) | Whether confidence is overconfident on repaired misspellings while image gain is not, and where that flips |
| Mitigation: PAR ([ACL 2026](https://aclanthology.org/2026.acl-long.1065/)), grounded-layer fusion ([2506.05551](https://arxiv.org/html/2506.05551v2)), late-layer text override CALRD ([2606.17953](https://arxiv.org/html/2606.17953)), cross-view abstention GRC ([2603.19790](https://arxiv.org/abs/2603.19790)) | A non-Latin script: Devanagari errors cluster on conjuncts, matras and nukta ([arXiv 2606.29213](https://arxiv.org/html/2606.29213)), and unfamiliar scripts get swapped for look-alike scripts ([GlotOCR](https://arxiv.org/html/2604.12978v1)) |

**Sharp framing.** *When does the prior win? We map where the language prior overrides visual evidence in small VLMs across a legibility × lexical-familiarity × script grid, and test which ground-truth-free signals (confidence, image gain, logit-lens crossover) flag prior-driven misreads.* Lead with the detector comparison. Your "handoff layer" becomes one of the signals, not the headline, because CALRD and grounded-layer fusion already claim the mechanism.

**Minimal experiment.** Use 4 word types (frequent word, one-swap misspelling, random string, digit string) × 6 blur levels × about 200 items, with Latin first and Devanagari second (render it with a Noto font and correct shaping, or with the GlotOCR renderer). For each output, record exact match, the **repair rate** (wrong *and* a dictionary word), the blur level at which 50% of items are still correct for each word type, and the AUROC of minimum token log-prob vs minimum image gain for predicting an error. Add PaddleOCR or Tesseract as the "no-prior" control. The script below covers the whole loop. I tested the rendering and stimulus parts, but the model part is **untested** here because I had no GPU.

```python
# pip install "transformers>=4.57" accelerate pillow wordfreq pandas scikit-learn
import random, string, torch
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from wordfreq import top_n_list
LEX = top_n_list("en", 50000); LEXSET = set(LEX); rng = random.Random(0)
def make_items(n):
    words = [w for w in LEX[500:5000] if w.isalpha() and 5 <= len(w) <= 9]; items = []
    for w in rng.sample(words, n):
        items.append(("word", w))
        for _ in range(20):                                  # one interior letter swap that is NOT a word
            i = rng.randrange(1, len(w) - 2); m = w[:i] + w[i+1] + w[i] + w[i+2:]
            if m != w and m not in LEXSET: items.append(("misspelling", m)); break
        items.append(("random", "".join(rng.choices(string.ascii_lowercase, k=len(w)))))
        items.append(("digits", "".join(rng.choices(string.digits, k=len(w)))))
    return items
def render(text, blur, size=40):                             # use a Noto TTF for Devanagari
    font = ImageFont.load_default(size=size); w = int(font.getlength(text)) + 40
    img = Image.new("RGB", (max(w, 160), size + 40), "white")
    ImageDraw.Draw(img).text((20, 20), text, fill="black", font=font)
    return img.filter(ImageFilter.GaussianBlur(blur)) if blur else img
PROMPT = "Transcribe the text in the image exactly, letter by letter. Output only the text."
def load(mid="Qwen/Qwen3-VL-2B-Instruct"):
    from transformers import AutoProcessor, AutoModelForImageTextToText
    return (AutoProcessor.from_pretrained(mid),
            AutoModelForImageTextToText.from_pretrained(mid, torch_dtype=torch.bfloat16, device_map="cuda").eval())
def _inp(proc, img):
    msgs = [{"role": "user", "content": [{"type": "image", "image": img}, {"type": "text", "text": PROMPT}]}]
    return proc.apply_chat_template(msgs, tokenize=True, add_generation_prompt=True, return_dict=True, return_tensors="pt")
@torch.no_grad()
def read(proc, model, img):
    x = _inp(proc, img).to(model.device); out = model.generate(**x, max_new_tokens=24, do_sample=False)
    return proc.batch_decode(out[:, x["input_ids"].shape[1]:], skip_special_tokens=True)[0].strip()
@torch.no_grad()
def token_logprobs(proc, model, img, target):                 # teacher-forced log p(target | image, prompt)
    x = _inp(proc, img); t = proc.tokenizer(target, add_special_tokens=False, return_tensors="pt")["input_ids"]
    x["input_ids"] = torch.cat([x["input_ids"], t], 1)
    x["attention_mask"] = torch.cat([x["attention_mask"], torch.ones_like(t)], 1); x = x.to(model.device)
    lp = model(**x).logits[0, -t.shape[1] - 1:-1].float().log_softmax(-1)
    return lp.gather(-1, t[0].to(model.device)[:, None])[:, 0].cpu()
def image_gain(proc, model, img, text):                       # real image vs blank image of the same size
    return token_logprobs(proc, model, img, text) - token_logprobs(proc, model, Image.new("RGB", img.size, "white"), text)
if __name__ == "__main__":
    import pandas as pd; from sklearn.metrics import roc_auc_score
    proc, model = load(); rows = []
    for cls, text in make_items(50):
        for blur in range(6):
            img = render(text, blur); out = read(proc, model, img) or " "
            rows.append(dict(cls=cls, blur=blur, text=text, out=out, correct=out == text,
                             repaired=out != text and out.lower() in LEXSET,
                             min_logp=token_logprobs(proc, model, img, out).min().item(),
                             min_gain=image_gain(proc, model, img, out).min().item()))
    df = pd.DataFrame(rows); df.to_csv("cube_results.csv", index=False)
    print(df.groupby(["cls", "blur"])[["correct", "repaired"]].mean().unstack())
    for cls, g in df.groupby("cls"):
        if g.correct.nunique() == 2:
            print(cls, {s: round(roc_auc_score(~g.correct, -g[s]), 3) for s in ["min_logp", "min_gain"]})
```

**8 GB note.** These are my estimates, not measurements. A 2B model in bf16 needs roughly 4–5 GB for its weights, and single-word images keep the visual-token count small, so Qwen3-VL-2B (used in the Greek study) fits, as does SmolVLM. A 3–4B model in bf16 is borderline. 4-bit quantisation fits, but it makes logit-lens and patching hooks awkward. Stay at 2B for the internal-signal work. The Greek study used about 100 GPU-hours, but on full pages ([arXiv 2605.27750](https://arxiv.org/html/2605.27750v1)). The single-word grid above is far cheaper. For hooks, Spectra supports Qwen2.5-VL, Qwen3-VL, SmolVLM and LLaVA-1.5 ([ACL 2026 demo](https://preview.aclanthology.org/ingest-acl/2026.acl-demo.78/)).

## 4. "Even I can do a benchmark paper": half right, and here is the other half

**The papers you're probably thinking of**

| Paper | What it actually contributed | Where it appeared | Team / data |
|---|---|---|---|
| **From Pixels to Structure** ([arXiv 2610.11818](https://arxiv.org/abs/2610.11818)) | Not a big benchmark. A careful comparison of 8 open VLMs (≤7B) on 3 university heritage collections: zero-shot, few-shot and fine-tuned, with ablations on preprocessing and multi-stage training. Metrics: CER, ANLS* and mAP-F1 | **ICDAR 2026**, Springer LNCS (17 pp.) | 4 authors, including senior document-analysis researchers (Christlein, Maier). Annotated real institutional data |
| KRETA ([EMNLP 2025](https://aclanthology.org/2025.emnlp-main.1696.pdf)) | 2,577 Korean text-rich VQA items from native images (including the authors' own photos), a reusable generation-plus-review pipeline, about 19 models evaluated | **EMNLP 2025 main** | 5 authors across startups, a university and big tech |
| KOCRBench ([arXiv 2510.02543](https://arxiv.org/html/2510.02543v1)) | Only 250 questions. The real contribution is a 55M-parameter OCR model trained for about 500 GPU-hours | **arXiv only** | 2 authors at a company |
| KOFFVQA ([CVF](https://openaccess.thecvf.com/content/CVPR2025W/BEAM/papers/Kim_KOFFVQA_An_Objectively_Evaluated_Free-form_VQA_Benchmark_for_Large_Vision-Language_CVPRW_2025_paper.pdf)) | Free-form Korean VQA benchmark | **CVPR 2025 workshop**, not the main conference | — |
| OCRTurk ([arXiv 2602.03693](https://arxiv.org/html/2602.03693v1)) | 180 Turkish PDF pages, 2 annotators, 7 OCR systems, a Turkish-character metric | **arXiv only** (when checked) | 7 authors, academic + industry |
| KITAB-Bench ([arXiv](https://arxiv.org/abs/2502.14949v1)) | 8,809 Arabic OCR/document samples across 9 domains | **ACL 2025 Findings** ([Anthology](https://preview.aclanthology.org/watermark/2025.findings-acl.1135)) | MBZUAI, 10 authors |
| IndicDLP ([CVIT](https://cvit.iiit.ac.in/research/projects/cvit-projects/indicdlp)) | Indic layout dataset, 11 languages + English | **ICDAR 2025 oral**, Best Student Paper runner-up | **63 annotators** + reviewers |
| HinTel-AlignBench ([ACL Anthology](https://aclanthology.org/2026.alvr-main.26/)) | Hindi/Telugu VLM benchmark, 4,000 QA per language, 6 pages | **ALVR workshop @ ACL 2026** | — |

The pattern is clear. **Simple method, but not simple data.** Every paper that reached a good venue had real, native-sourced, human-verified data, a broad evaluation, and usually senior or industry co-authors. The "basic Korean" papers that look easy mostly sit on arXiv or at workshops. Being on arXiv is not the same as being "in a huge conference". I did not check Korean OCR papers in MDPI-style journals, so I can't comment on those.

**What reviewers expect in 2026.** The NeurIPS 2026 Evaluations & Datasets track (the renamed D&B track) holds submissions to main-track standards. It requires the data to be public **at submission time** on a persistent host such as Hugging Face or Kaggle, a mandatory **Croissant metadata file with Responsible-AI fields**, code for executable benchmarks, and an explicit statement of the claims and limitations of the evaluation. Inaccessible data "justifies the desk rejection of the paper" ([CFP](https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets)). In 2025, submissions commonly lacked licence information (11.9%), dataset descriptions and URLs ([NeurIPS blog](https://blog.neurips.cc/2025/12/05/neurips-datasets-benchmarks-track-from-art-to-science-in-ai-evaluations/)). From these rules and the papers above, I infer that the usual ways to get rejected are: a set too small with no insight beyond "models do worse on language X", LLM-made labels nobody verified, unclear redistribution rights, contamination (Wikisource pages are probably already in VLM training data), and no inter-annotator agreement.

**Is there an Indian-language gap?** Yes, but a narrow one. Scene text, layout and general VQA are covered (BSTD, IndicDLP, IndicVisionBench, HinTel-AlignBench). Krutrim's 2026 paper names what is still missing: dense printed documents, **forms and index pages**, rare scripts, handwriting and low-resolution scans. It also says there is **no public benchmark** for extracting key fields from government documents ([arXiv 2602.16430](https://arxiv.org/html/2602.16430v1)). IndicVisionBench's OCR track has only 876 Wikisource pages ([arXiv 2511.04727](https://arxiv.org/html/2511.04727)). Well-funded players (AI4Bharat, Krutrim, Sarvam) are active, so search again for 2026 releases before you commit.

**A realistic undergraduate version.** Pick 1–2 languages you read natively and one under-served document type, such as forms, old print or handwritten registers. Collect **200–500 pages** you have the rights to (your own photos, government or public-domain material). Annotate page-to-text, or key fields. Double-annotate about 20% to report agreement. Evaluate **8–15 systems**, mixing classic OCR (Tesseract, PaddleOCR) with small and large VLMs. Report the median plus a catastrophic-failure rate, because VLMs fall into repetition loops ([arXiv 2606.29213](https://arxiv.org/html/2606.29213)). Analyse errors by script phenomenon, such as conjuncts and matras. Release the data on Hugging Face with Croissant metadata and a licence. Expect several months of part-time work, mostly on annotation. Go up the venue ladder in order: **an ACL/CVPR/ICDAR workshop first (ALVR-style), then ICDAR main, ACL Findings or IJDAR, and NeurIPS E&D only with scale and a senior co-author.**

| Option | Effort | Realistic venue |
|---|---|---|
| 200–500 page Indic document set + 8–15 systems + error analysis | 3–6 months, part-time | Workshop → ICDAR / IJDAR |
| Same + Devanagari hallucination grid from §3 as the analysis section | +1–2 months | ICDAR / Findings, a stronger story |
| Thousands of items, many languages, annotator team | Lab-scale | NeurIPS E&D / main conference |

## Conclusion

The three ideas fit together better than they look. The SSL project asks *what a recognizer should ignore*. The hallucination project asks *what a VLM wrongly ignores* (the pixels, when its prior is strong). An Indic benchmark is most publishable when it carries exactly that kind of analysis rather than a leaderboard. So if you want a paper of your own beyond the thesis track, the strongest single move is to merge §3 and §4: a small, human-verified Devanagari document set whose headline result is *where and how detectably the prior overrides the pixels*. The cube study is the cleanest, most self-contained thing you can finish quickly, and its first figure already exists. Do it as a warm-up for writing a paper, not as the main bet.

---

# Part 7 — Raw research notes

## Notes: OCR hallucination cube and benchmarks / cube_idea.md

## Learned cube / permutation-puzzle solvers: training-data distribution, scramble-length labels, and a laptop-feasible project framing (as of Oct 12, 2026)

Builds on the earlier fact-check in `/home/claude/research_notes/Vision SSL ideas reality check/graph_cube_tabular.md`. That note found:
- DeepCubeA samples k uniformly in [1,30] for the cube and trains for 36 h on 2 Titan V GPUs plus 6 data-generation GPUs.
- Random walks on the 3x3x3 concentrate at depth 17–18 HTM.
- At mid lengths, walk length overstates true distance.

### Q1. What do EfficientCube, CayleyPy, Agostinelli's later work and 2024–2026 papers say about training-state distribution, scramble-length sampling, curricula and data scaling? Does any paper show "more data hurts" or a distribution-mismatch effect?

#### Takeaway
No paper I found shows that more random-walk data *hurts*.
- **EfficientCube** fits a power-law scaling law in which more data keeps helping.
- **CayleyPy** reports *stagnation*: 4B, 8B and 16B training states give essentially the same 3x3x3 solution lengths. It also says more random walks "does not always improve" the model, and that this is more pronounced on LRX graphs.
- **Hadar, Agostinelli & Shperberg (2025)** come closest to a distribution-mismatch result. They argue that the distribution of training states (random backward walks versus search-generated states) creates "heuristic depression" regions, and that search-based sampling better matches the states seen at deployment.

Every major system samples walk lengths uniformly or as all prefixes of a walk up to some K_max. None of them studies the shape of the length distribution as a variable. CayleyPy explicitly says it does not study K_max.

#### Cited Findings
**EfficientCube (Takano, TMLR 2023)**
- Training data: random scrambles of up to 26 moves (God's number in QTM) from the goal. Moves are uniform over the 12 QTM moves, and self-cancelling moves such as R after R' are excluded. The network predicts the *last move applied* (categorical cross-entropy), and the solver inverts predictions inside beam search. — [arXiv 2106.03157 PDF](https://arxiv.org/pdf/2106.03157v5)
- Main model: 2M steps × 26,000 scrambled moves per batch, about 2B "solutions". The paper says this is roughly 80% less data than DeepCubeA's ~10B. — [arXiv 2106.03157 PDF](https://arxiv.org/pdf/2106.03157v5)
- Scaling law: L̂(N,D) = E + A/N^α + B/D^β, with E=0.892, A=4.0, B=6.2, α=0.178, β=0.134, fitted on 36 models. It was fitted in HTM with a scramble length of 20.
  - The final model has ~119M parameters and was trained on ~144B states at C≈5.1×10¹⁹ FLOPs.
  - The authors note "we would benefit from increasing training data, but not model parameters", so they report no data saturation.
  - Source: [arXiv 2106.03157 PDF](https://arxiv.org/pdf/2106.03157v5)
- Venue: TMLR 2023. The code and notebooks (Rubik's Cube, 15-puzzle, 7×7 Lights Out) are in a Colab/Kaggle-ready repo under CC-BY-4.0. — [GitHub kyo-takano/efficientcube](https://github.com/kyo-takano/efficientcube)

**CayleyPy cube paper (Chervov et al., arXiv 2502.13266; listed as NeurIPS 2025 on mlanthology)**
- Training states come from **non-backtracking** random walks from the solved state, which forbid returning to the previous state. Each state is labeled with its step index k, and the network regresses k with MSE (the "diffusion distance").
  - K_max is 26 for 3×3×3, 45 for 4×4×4 and 65 for 5×5×5.
  - A fresh 1M-example dataset is generated each epoch.
  - The paper states it does not study the effect of K_max.
  - Sources: [arXiv 2502.13266](https://arxiv.org/html/2502.13266v1); venue listing at [mlanthology](https://mlanthology.org/neurips/2025/chervov2025neurips-machine)
- **Data scaling stagnates.** The paper reports "performance stagnation with respect to the train size". Average 3×3×3 solution lengths were 21.16, 21.12 and 21.19 for 4B, 8B and 16B training states; for 4×4×4 they were 55.4, 55.11 and 55.84. The authors conclude there is "no practical reason" to go beyond ~8B. — [arXiv 2502.13266](https://arxiv.org/html/2502.13266v1)
- Compute and results:
  - Model: a 10-layer ResMLP with ~4M parameters.
  - Training: 4 h 40 min on one A100-80GB, versus 86 h 25 min reported for EfficientCube.
  - 3×3×3 results on the DeepCubeA test set: 75.4% optimal at beam width 2^18 and 97.3% at 2^24. A 26-agent ensemble reaches 98.4% in the abstract and table, but the body text says 97.6%, so the paper is internally inconsistent.
  - Depth mattered more than parameter count.
  - Source: [arXiv 2502.13266](https://arxiv.org/html/2502.13266v1)
  - Code: [GitHub k1242/cayleypy-cube](https://github.com/k1242/cayleypy-cube)

**CayleyPy RL (arXiv 2502.18663)**
- **Walk generator matters more than volume.**
  - Simple random walks failed at every beam width when trained for a single epoch: "Without non-backtracking system cannot perform well on single epoch training."
  - An improved non-backtracking generator forbids roughly 32 steps of history, bans states visited anywhere in the batch, and bans their neighbors.
  - The rationale: on a tree, non-backtracking walk length equals true distance, so labels are less noisy.
  - Source: [arXiv 2502.18663v2](https://arxiv.org/html/2502.18663v2)
- **Explicit "more data does not always help".** The paper states: "enlarging the training set (generating more random walks) does not always improve the quality of the model". This was observed for cubes and is "even more prominent for LRX graphs". — [arXiv 2502.18663v2](https://arxiv.org/html/2502.18663v2)
- Diffusion distance is not a monotone function of true distance, even in the infinite-data limit. — [arXiv 2502.18663v2](https://arxiv.org/html/2502.18663v2)
- Bellman/DQN fine-tuning after a diffusion warm-up gives a consistent but "not so big" gain.
  - S₂₈ LRX median solution lengths (ideal ≈378): warm-up+DQN 30+200 → 402; diffusion-only 30+0 → 650; diffusion-only 100+0 → 516; pure DQN → 455.5.
  - Deep networks rarely beat a single-layer 128-neuron perceptron on LRX.
  - Single-epoch runs take 1–5 min on a P100.
  - Source: [arXiv 2502.18663v2](https://arxiv.org/html/2502.18663v2)

**Agostinelli and collaborators, later work**
- **"Beyond Single-Step Updates: RL of Heuristics with Limited-Horizon Search"** (Hadar, Agostinelli, Shperberg; arXiv 2511.10264; venue not stated on the page).
  - Domains: Rubik's Cube, STP-35 and 7×7 Lights Out.
  - The baseline SSBL samples states by random backward moves from the goal. LHBL instead runs a limited-horizon A*/GBFS search from each sampled state and trains on shortest-path-to-frontier labels.
  - Distribution-mismatch argument: heuristic-guided search over-represents states with low heuristic values, especially under GBFS, which can create **heuristic depression** regions. Search-based sampling "better resemble[s]" the states seen at deployment.
  - Results: LHBL is more sample-efficient. SSBL never reached 100% on STP and solved only 4.7–13.2% on Lights Out.
  - Budget: ~10B samples and 10–12 days for the cube. Code is promised on acceptance.
  - Source: [arXiv 2511.10264](https://arxiv.org/html/2511.10264)
- **DeepXube** (Agostinelli, Mar 2026) is an open-source package for learning heuristics: limited-horizon Bellman learning and hindsight experience replay, batch weighted A*, Q* and beam search, goals in ASP, CPU-parallel data generation. — [arXiv 2603.23873](https://arxiv.org/abs/2603.23873); [GitHub forestagostinelli/deepxube](https://github.com/forestagostinelli/deepxube)
- Also surfaced but **not fetched or verified**:
  - Agostinelli et al., "A* search without expansions: learning heuristic functions with deep Q-networks" (Q* search), [arXiv 2102.04518 via ResearchGate](https://www.researchgate.net/publication/349159622_A_Search_Without_Expansions_Learning_Heuristic_Functions_with_Deep_Q-Networks); revised version at [arXiv 2211.13316](https://arxiv.org/pdf/2211.13316) (v4 Feb 2025).
  - "Towards Learning Foundation Models for Heuristic Functions to Solve Pathfinding Problems", [arXiv 2406.02598](https://arxiv.org/html/2406.02598v1).

**Other 2024–2026 work**
- **GFlowNet shortest paths** (Morozov, Maksimov, Tiapkin, Samsonov; arXiv 2603.01786).
  - Instead of regressing walk length, the method trains a backward policy whose optimum assigns zero probability to every non-shortest path, so it targets exact shortest paths rather than diffusion distance.
  - Training is on-policy from the goal with N_max = 12 (2×2×2), 24 (3×3×3) and 50 (Swap).
  - 2×2×2: reaches the optimal mean of 10.64 QTM on the CayleyPy test set with a beam 16× smaller than CayleyPy's, and solves everything greedily (W=1).
  - 3×3×3: better than CayleyPy at beam widths ≤ 2^9.
  - Code: [GitHub GreatDrake/gfn-pathfinding](https://github.com/GreatDrake/gfn-pathfinding) (JAX).
  - Source: [arXiv 2603.01786](https://arxiv.org/abs/2603.01786)
- **"Learning Empirically Admissible Neural Heuristics"** (Sahay, June 2026).
  - Says MSE-trained DeepCubeA-style heuristics "regularly yield overestimations". It uses an underestimating Bellman operator, an asymmetric loss and a calibration offset computed on validation scrambles.
  - Reports up to 83% fewer node expansions on the 2×2 cube than analytical baselines, 19.9% on 3×3 Lights Out and 1.9% on the 8-puzzle.
  - No code is mentioned. It is a single-author preprint.
  - Source: [arXiv 2606.04860](https://arxiv.org/abs/2606.04860)
- **"Solving Rubik's Cube Without Tricky Sampling"** (Lin & Liang, Nov 2024 preprint). It is a policy-gradient method trained from fully scrambled states rather than near-solved sampling, and reports >99.4% on 2×2×2 without tree search. The sampling details were not on the abstract page. — [arXiv 2411.19583](https://arxiv.org/abs/2411.19583)
- **CayleyPy Growth** (arXiv 2509.19162, Sep 2025, v2 Apr 2026) is the third CayleyPy paper. It covers BFS growth and diameter conjectures and announces 10+ Kaggle path-finding benchmark datasets. The abstract does not discuss training data. — [arXiv 2509.19162](https://arxiv.org/abs/2509.19162)

#### Inferences
- The student's slogan "too much data is a bottleneck" is unsupported as stated.
  - The strongest data-volume evidence is EfficientCube's power law, which favours more data, and CayleyPy's flat 4B/8B/16B result, which shows saturation, not harm.
  - The defensible version is: **label quality and state distribution, not data volume, limit walk-supervised heuristics.**
  - The evidence for that version: CayleyPy's non-backtracking-vs-simple ablation, its non-monotonicity remark, its "more walks doesn't always help" remark, and Hadar et al.'s depression and mismatch argument.
- Two gaps stand out. Nobody has varied the *shape* of the training distribution over true distance at a fixed budget. Every paper uses uniform-k or all-prefixes up to K_max, and CayleyPy explicitly does not study K_max.

#### Gaps
- I did not read the full text of EfficientCube for per-length accuracy or any non-uniform length schedule.
- I did not read the full text of Q* search or the 2406.02598 foundation-model paper.
- I found no paper reporting a monotone *decrease* in solve quality with more walk data. The LRX "more prominent" remark in CayleyPy RL has no table I could see.
- I could not confirm the venue of 2511.10264.

### Q2. Is there work comparing random-walk-length labels with true distance on small puzzles where BFS is feasible?

#### Takeaway
Only partially. CayleyPy RL reports **Spearman correlations between learned diffusion-distance predictions and true distances** on small LRX/Sₙ graphs, using brute-force distances on about a million states. The correlation degrades as n grows: 0.955 → 0.883 for diffusion-only training from n=6 to n=10. I found no paper that, on the 2×2×2, 8-puzzle, Lights Out or TopSpin, systematically compares raw walk length or learned diffusion distance against BFS distance broken down *by true-distance bin*. I also found none that trains on BFS-exact labels versus walk labels at matched budget and measures the downstream effect on search.

#### Cited Findings
- CayleyPy RL, Table 1, Spearman correlation of model predictions vs true distance (A+B = A diffusion warm-up epochs + B DQN epochs):

  | n | 5+0 | 50+0 | 5+50 | 50+50 |
  |---|---|---|---|---|
  | 6 | 0.955 | 0.99 | 0.99 | 0.99 |
  | 8 | 0.954 | 0.969 | 0.98 | 0.982 |
  | 10 | 0.883 | 0.923 | 0.939 | 0.938 |

  Source: [arXiv 2502.18663v2](https://arxiv.org/html/2502.18663v2)
- On a tree, non-backtracking walk length equals distance. On graphs with cycles it is "closer" to distance and less variable, which is why it is used. — [arXiv 2502.18663v2](https://arxiv.org/html/2502.18663v2)
- The GFlowNet paper contrasts walk-length regression (CayleyPy) with exact-shortest-path targets. It does not compare them experimentally at the label level. — [arXiv 2603.01786](https://arxiv.org/abs/2603.01786)
- Exact 2×2×2 benchmarks already exist: a CayleyPy 100-cube test set with optimal mean 10.64 QTM. — [arXiv 2603.01786](https://arxiv.org/abs/2603.01786)
- The CayleyPy library provides BFS and growth functions, plus generators for Rubik's cubes, LRX, TopSpin, pancake and others, and beam search with pretrained predictors. It is MIT-licensed and installs with `pip install cayleypy`. — [GitHub cayleypy/cayleypy](https://github.com/cayleypy/cayleypy)
- Quantitative walk-vs-depth behaviour for the 3×3×3 (QTM): at N=18, depth 17 is more likely than 19, and the distribution is near stationary by N≈31–32. — [Towards Data Science blog](https://towardsdatascience.com/a-random-walk-on-the-rubiks-cube-684dd304bf3e/) (secondary source)
- An older experimental evaluation of deep heuristic learning on the cube exists. — [CEUR-WS Vol-1885](https://ceur-ws.org/Vol-1885/57.pdf) (not re-read here)

#### Inferences
- A "walk-length vs true-distance" label-noise characterization on the 2×2×2, 8-puzzle and Lights Out, broken down by true-distance bin and by walk type (simple vs non-backtracking vs CayleyPy's improved generator), appears **unpublished** as a standalone result. It would be cheap: P(true d | walk length k) is computable exactly from the BFS table plus walk simulation.
- The 2×2×2 facts below are background knowledge and were not verified by a fetched source in this session. They agree with the GFN paper's 10.64 QTM mean:
  - 3,674,160 states
  - God's number 11 HTM / 14 QTM
  - BFS table of ~3.7M bytes
- The 8-puzzle has 181,440 reachable states (background knowledge, unverified here).

#### Gaps
- I did not search exhaustively on Semantic Scholar or OpenReview for workshop papers on "walk length vs distance". A small study could exist undetected.
- TopSpin and Lights Out specific work on label noise was not found.

### Q3. A precise, falsifiable, laptop-feasible version of the idea

#### Takeaway
Reframe "too much data is a bottleneck" as follows: **"At a fixed sample budget, the *distribution over true distance* and the *label source* of training states, not their number, determine heuristic accuracy where search needs it, and therefore solve rate, optimality and nodes expanded."** Test it on the 2×2×2 cube (QTM), with the 8-puzzle and/or Lights Out 3×3–5×5 as replication domains, where every state's exact distance is known from BFS.

#### Cited Findings (anchors for the design)
- Baselines to reproduce:
  - Uniform-k scrambles in DeepCubeA style: [DeepCubeA PDF](https://deepcube.igb.uci.edu/static/files/SolvingTheRubiksCubeWithDeepReinforcementLearningAndSearch_Final.pdf)
  - Non-backtracking walk-length regression, CayleyPy style: [arXiv 2502.13266](https://arxiv.org/html/2502.13266v1)
  - Last-move classification, EfficientCube style: [arXiv 2106.03157](https://arxiv.org/pdf/2106.03157v5)
- CayleyPy runs single epochs in minutes on a P100 and uses small MLPs. The 2×2×2 GFN result shows greedy optimality is possible, so the domain is solvable with small models. — [arXiv 2502.18663v2](https://arxiv.org/html/2502.18663v2); [arXiv 2603.01786](https://arxiv.org/abs/2603.01786)
- Overestimation from MSE heuristics is a known issue, so admissibility-violation rate is a meaningful metric. — [arXiv 2606.04860](https://arxiv.org/abs/2606.04860)

#### Inferences (proposed design; my synthesis, not from a source)
**Setup**
- Build the full BFS table for the 2×2×2 (fix one corner; 3.67M states, QTM).
- Use a ResMLP or MLP with ~0.5–4M parameters. This is trivially within 8 GB.

**Hold the sample budget B fixed** (e.g. 10⁵, 10⁶, 10⁷; keep B below the state count so memorization does not trivialize the task).

**Factor 1: training-state distribution over true distance d**
- (a) uniform in walk length k∈[1,K], DeepCubeA style
- (b) uniform in true d
- (c) the natural distribution, i.e. uniform random states, which are mostly near the diameter
- (d) near-goal-heavy
- (e) far-heavy
- (f) a curriculum from small to large d

**Factor 2: label source**
- (i) raw simple-walk length
- (ii) non-backtracking walk length
- (iii) DeepCubeA-style Bellman/value-iteration targets
- (iv) exact BFS distance, as the oracle upper bound

**Metrics**
- MAE and signed bias of h per true-distance bin
- Spearman correlation
- Rate of admissibility violations
- Then, with A*, weighted A* and beam search at several widths on a fixed test set stratified by true distance: solve rate, optimality gap, and nodes expanded

**Falsifiable hypotheses**
- **H1:** walk-length labels (i)/(ii) are biased upward in the mid-range of d, and this bias is measurable from BFS alone, before any training.
- **H2:** at fixed B, distribution choice changes the optimality and nodes-expanded results by more than a 10× increase in B does. This is the real version of "data volume isn't the bottleneck".
- **H3:** with walk labels, increasing B beyond some point does not improve, or worsens, accuracy in specific d-bins, because the network converges to E[k | state] (diffusion distance), which is biased. With BFS labels it keeps improving. If more data never hurts under any condition, the strong claim is falsified, and the result becomes "saturation is due to label bias".
- **H4:** a mismatch between training distribution and the test d-distribution, for example training uniform-in-k but testing on random states, accounts for most of the degradation in search.

**Stretch goals**
- Repeat on the 8-puzzle (181,440 states) and on Lights Out (exact GF(2) solutions).
- Check one condition on the 3×3×3 using the CayleyPy pretrained pipeline as a sanity check, with no full retraining.

**Compute estimate (my inference)**
- BFS on the 2×2×2 runs in seconds to minutes in Python/numpy.
- Each training run of ≤10⁷ samples is minutes on a laptop GPU.
- The full factorial (6 distributions × 4 labels × 3 budgets × 3 seeds ≈ 216 runs) fits within days.

**Novelty risk**
- The closest prior work is CayleyPy RL's Spearman table on LRX and its non-backtracking ablation, plus Hadar et al.'s mismatch argument.
- The student must cite these and position the contribution as a controlled, exact-label decomposition on cube-family puzzles.

#### Gaps
- No source confirms that nobody has run exactly this factorial. Novelty is "not found", not proven.
- On the 2×2×2, a network that sees ~10⁷ samples could approach memorization of the 3.67M-state table. Budget choice needs a pilot.

### Q4. Open-source code to start from

#### Takeaway
There are four good starting points:
- **CayleyPy library** for BFS, puzzle generators and beam search (MIT)
- **cayleypy-cube** for the walk-regression training/search pipeline
- **EfficientCube** notebooks for last-move prediction (CC-BY-4.0)
- **DeepCubeA / DeepXube** for Bellman-trained heuristics with A*/Q* search

The **gfn-pathfinding** repo (JAX) is an exact-shortest-path alternative.

#### Cited Findings
- **CayleyPy**: BFS/growth, generators for Rubik's cubes, LRX, TopSpin and others, beam search with pretrained Kaggle-hosted predictors, MIT license, `pip install cayleypy`. — [GitHub cayleypy/cayleypy](https://github.com/cayleypy/cayleypy)
- **cayleypy-cube** (trainer.py, model.py, searcher.py). — [GitHub k1242/cayleypy-cube](https://github.com/k1242/cayleypy-cube)
- **EfficientCube**: notebooks for the cube, 15-puzzle and Lights Out, runnable on Colab/Kaggle, TMLR 2023. — [GitHub kyo-takano/efficientcube](https://github.com/kyo-takano/efficientcube)
- **DeepCubeA**. — [GitHub forestagostinelli/DeepCubeA](https://github.com/forestagostinelli/DeepCubeA)
- **DeepXube**. — [GitHub forestagostinelli/deepxube](https://github.com/forestagostinelli/deepxube); [arXiv 2603.23873](https://arxiv.org/abs/2603.23873)
- **GFlowNet pathfinding**. — [GitHub GreatDrake/gfn-pathfinding](https://github.com/GreatDrake/gfn-pathfinding)
- **Kaggle LRX challenges** named in CayleyPy RL: "LRX OEIS-A186783 brainstorm math conjecture", "LRX discover math and God's algorithm", "LRX-binary: in search of God's number". No URLs were given in the paper. The CayleyPy README lists Kaggle competitions for 4×4×4–7×7×7 cubes, Megaminx, pancake sorting and others. — [arXiv 2502.18663v2](https://arxiv.org/html/2502.18663v2); [GitHub cayleypy/cayleypy](https://github.com/cayleypy/cayleypy)

#### Inferences
- For the 2×2×2 study, the simplest stack is CayleyPy (or ~100 lines of numpy) for BFS and the move tables, a custom PyTorch MLP, and the search code from cayleypy-cube or DeepXube.

#### Gaps
- Direct URLs for the CayleyPy Kaggle competitions were not retrieved.
- Whether DeepXube ships a 2×2×2 domain or non-uniform sampling options was not verified.

## Notes: OCR hallucination cube and benchmarks / ocr_benchmarks_publishability.md

## Could an undergraduate publish an OCR benchmark paper? Recent OCR benchmarks and low-resource-language OCR papers (as of Oct 2026)

Research date: 2026-10-12. Each fact links to the page fetched or searched this session. Items marked [UNVERIFIED] come from search snippets or prior knowledge and were not confirmed against a primary page.

### Q1. What is the "pixel to structure" paper, and what does it contribute? (Plus related OCR and document-parsing benchmarks)

#### Takeaway
The likeliest match is "From Pixels to Structure: Lightweight Vision-Language Models for Document OCR and Structured JSON Extraction" (arXiv 2610.11818, posted 8 Oct 2026; published at ICDAR 2026, Springer LNCS). It is not a large general benchmark. It is an applied comparative study by a four-person academic team (FAU Erlangen group, inferred from the author names). It tests 8 open VLMs of 7B parameters or fewer on 3 university heritage collections, and covers zero-shot, few-shot and fine-tuned settings plus ablations. Its scope is achievable for a strong student working with a supervisor. What makes it publishable is the real, annotated institutional data and a careful experimental design, not novelty.

#### Cited Findings
- Title: "From Pixels to Structure: Lightweight Vision-Language Models for Document OCR and Structured JSON Extraction". Authors: Uddipan Basu Bir, Vincent Christlein, Andreas Maier, Mathias Zinnen. arXiv v1 posted 8 Oct 2026. Journal reference: "Document Analysis and Recognition – ICDAR 2026, LNCS vol. 16974, Springer", pp. 502–519. 17 pages, with code on GitHub. — [arXiv 2610.11818](https://arxiv.org/abs/2610.11818)
- Contribution: it compares 8 open-source lightweight VLMs (≤7B) on converting heritage document images into text and schema-compliant JSON. Data comes from 3 university heritage collections covering jewelry, prehistory and architecture.
  - Settings are zero-shot, few-shot and fine-tuned.
  - Ablations cover hyperparameter tuning, classical preprocessing (illumination flattening, denoising, CLAHE) and multi-stage training. The paper also compares per-dataset models with one multi-dataset model.
  - Metrics are CER, ANLS* and mAP-F1.
  - Motivation: privacy, cost and sustainability for archives.
  - Source: [arXiv 2610.11818](https://arxiv.org/abs/2610.11818)
- The abstract page does not state the dataset size or the annotation effort. — [arXiv 2610.11818](https://arxiv.org/abs/2610.11818)
- Comparator, OCRTurk (Turkish OCR benchmark, arXiv Feb 2026, no venue listed):
  - Team: 7 authors from METU, Politecnico di Torino and Roketsan Inc. (a defence company).
  - Data: only 180 PDF pages in 4 categories (academic, non-academic, theses, slides) at 3 difficulty levels, with 279 annotated items (92 equations, 130 tables, 57 figures).
  - Annotation: two annotators converted pages to Markdown, HTML and LaTeX, with ChatGPT/Gemini helping on formatting and every output checked by hand.
  - Evaluation: 7 OCR systems (DeepSeekOCR, Docling, PaddleOCR, HunyuanOCR, NanonetsOCR2, Nemotron, olmOCR2) with NED, TEDS, CDM and a Turkish character-sensitivity metric.
  - Source: [OCRTurk arXiv 2602.03693](https://arxiv.org/html/2602.03693v1)
- KITAB-Bench (Arabic OCR and document understanding): 8,809 samples across 9 domains and 36 sub-domains, including handwriting, tables, 21 chart types and PDF-to-Markdown. It evaluates GPT-4o, Gemini and Qwen against EasyOCR, PaddleOCR and Surya. Gemini-2.0-Flash scored about 65% on PDF-to-Markdown. The 10 authors include Salman Khan and Fahad Khan (MBZUAI). — [arXiv 2502.14949](https://arxiv.org/abs/2502.14949v1)
- KITAB-Bench was published in ACL 2025 Findings as paper 2025.findings-acl.1135. — [ACL Anthology](https://preview.aclanthology.org/watermark/2025.findings-acl.1135); [papers.cool](https://papers.cool/venue/2025.findings-acl.1135@ACL)
- [UNVERIFIED, prior knowledge, not fetched] The following are the large "industrial" benchmarks:
  - OmniDocBench (Shanghai AI Lab, CVPR 2025): about 1,000 pages over 9 document types.
  - OCRBench v2 (Liu et al.).
  - CC-OCR (Alibaba Qwen team).
  - olmOCR-bench (Allen AI).
  - Each has a large institutional team and large annotation budgets. The awesome-list [AWESOME-OCR-LLM](https://github.com/yuliang-liu/awesome-ocr-llm) indexes them.

#### Inferences
- "From Pixels to Structure" sits at ICDAR, the field's specialist conference. It is CORE-ranked but not at the level of CVPR, NeurIPS or ACL main. Its value is an evaluation on real archival data with schema-based extraction, done by an established document-analysis lab (Christlein and Maier are senior FAU researchers). The student is right that it is "basic" in method. But it rests on real annotated data from partner institutions, a 17-page systematic experimental design, and senior co-authors who know what ICDAR reviewers expect.
- OCRTurk shows the minimum viable size for a language-specific document-parsing benchmark: 180 pages, 2 annotators, open models only. That is well within an undergraduate's reach. Even so, the team had 7 people including industry and senior faculty, and it was still a preprint when checked.

#### Gaps
- The student may mean a different "pixels to structure" paper. I found no other exact title match. The affiliations for 2610.11818 were not on the abs page, so FAU is inferred from author names. I did not verify the dataset size.
- I did not re-fetch OmniDocBench, OCRBench v2, CC-OCR or olmOCR-bench details this session.

### Q2. Korean OCR and Korean document-understanding papers, 2024–2026: venues and what made them publishable

#### Takeaway
Recent Korean text-rich and OCR benchmarks split into three groups:
- Main-conference papers with substantial native data and many evaluated models, such as KRETA at EMNLP 2025 main.
- Workshop papers, such as KOFFVQA at a CVPR 2025 workshop.
- arXiv-only industry reports, such as KOCRBench from KL-Net and the VARCO-VISION technical reports.

The "very basic Korean OCR papers" the student has in mind are likely KOCRBench, which has only 250 questions but is an arXiv preprint and not at a major venue, or papers in MDPI-type journals. That impression mixes up venue tiers.

#### Cited Findings
- KRETA ("A Benchmark for Korean Reading and Reasoning in Text-rich VQA"), EMNLP 2025 main conference:
  - Team: 5 authors from Waddle, Seoul National University, Krafton, UNIST and SK Telecom.
  - Data: 2,577 samples (1,426 "System 1" recognition, 1,151 "System 2" reasoning) across 15 domains and 26 image types. Sources are native Korean images (government publications, posters, CSAT mock exams) plus the authors' own field photos.
  - Pipeline: VLM captioning, then LLM QA generation scored on 7 metrics, then hard-negative generation, then human review.
  - Evaluation: 4 closed and about 15 open VLMs.
  - Claimed gap: existing Korean VQA sets are translated, use non-Korean images, or have fewer than 650 samples.
  - Source: [ACL Anthology 2025.emnlp-main.1696](https://aclanthology.org/2025.emnlp-main.1696.pdf)
- KOCRBench (arXiv 2510.02543, Oct 2025, no venue listed):
  - Team: 2 authors at KL-Net, a Korean company.
  - Data: only 250 questions over 248 images (22 recognition, 70 scene VQA, 29 document VQA, 129 KIE). Partly repurposed from KVQA, mostly hand-annotated holdout data.
  - The paper's real centrepiece is KLOCR, a 55M-parameter bilingual OCR model trained on about 100M instances (mostly AIHub) for about 500 GPU-hours, with total development under 3,000 GPU-hours.
  - Source: [arXiv 2510.02543](https://arxiv.org/html/2510.02543v1)
- KOFFVQA (free-form Korean VQA benchmark) appeared at a CVPR 2025 workshop (BEAM), not the main conference. — [CVF open access](https://openaccess.thecvf.com/content/CVPR2025W/BEAM/papers/Kim_KOFFVQA_An_Objectively_Evaluated_Free-form_VQA_Benchmark_for_Large_Vision-Language_CVPRW_2025_paper.pdf)
- Korean VLMs with OCR evaluation, such as VARCO-VISION (NCSOFT) and VARCO-VISION-2.0, appear as arXiv technical reports. — [VARCO-VISION](https://arxiv.org/html/2411.19103v1); [VARCO-VISION-2.0](https://arxiv.org/html/2509.10105v2)
- Korean text-only benchmarks also reach Findings-tier venues, for example the Korean legal benchmark KBL at Findings of EMNLP 2024 ([ACL Anthology](https://aclanthology.org/2024.findings-emnlp.319/)) and a professional Korean benchmark suite at Findings of EMNLP 2025 ([ACL Anthology](https://aclanthology.org/2025.findings-emnlp.1038.pdf)).

#### Inferences
- KRETA, the clearest example of a Korean benchmark at a top venue, had several things a typical undergraduate project lacks:
  - Native-sourced images, including field photography.
  - A reusable semi-automated generation pipeline, which was itself a contribution.
  - A two-level reasoning taxonomy.
  - About 2.5K human-reviewed items.
  - A broad evaluation of about 19 models.
  - Collaborators across startups and big tech.
  - It was still a small team of 5 without a famous lab, so this level is reachable.
- "Very basic" Korean papers mostly sit in workshops, arXiv technical reports or lower-tier journals. Being on arXiv does not mean being published at a major venue.

#### Gaps
- I did not search IEEE Access, MDPI Sensors or Applied Sciences for Korean Hangul handwriting OCR papers, though such papers are commonly reported to exist [UNVERIFIED]. I also did not search for Upstage (DP-Bench / Document Parse) or NAVER (Donut/CORD, older) benchmark papers this session.

### Q3. Other low-resource-language OCR benchmarks and their venues

#### Takeaway
Language-specific OCR and VLM benchmarks get accepted at the following tiers:
- ACL Findings: KITAB-Bench (Arabic).
- ICDAR, including a best-student-paper runner-up: IndicDLP.
- Journals: Bharat Scene Text, in an IJDAR-like Springer journal (DOI 10.1007/s10032…).
- ICLR 2026: IndicVisionBench.
- ACL workshops: HinTel-AlignBench at ALVR 2026.

Nearly all came from established labs (MBZUAI, IIT Madras/IIIT Hyderabad/AI4Bharat, IIT Jodhpur, Krutrim) with paid annotator teams.

#### Cited Findings
- KITAB-Bench (Arabic), ACL 2025 Findings, MBZUAI-led, 8,809 samples. — [arXiv](https://arxiv.org/abs/2502.14949v1); [ACL Anthology](https://preview.aclanthology.org/watermark/2025.findings-acl.1135)
- IndicDLP (Indic document layout parsing), ICDAR 2025 oral and Best Student Paper Runner-Up:
  - Team: IIT Madras and IIIT Hyderabad (Mitesh Khapra, Ravi Kiran Sarvadevabhatla).
  - Coverage: 11 Indic languages plus English, 12 domains.
  - Annotation: 63 annotators, plus a reviewer and a "superchecker" for each language.
  - The dataset is hosted on Hugging Face under ai4bharat.
  - Sources: [CVIT project page](https://cvit.iiit.ac.in/research/projects/cvit-projects/indicdlp); [HF](https://huggingface.co/datasets/ai4bharat/IndicDLP); [arXiv 2512.20236](https://arxiv.org/abs/2512.20236v1)
- Bharat Scene Text Dataset (BSTD):
  - Data: over 100K words from more than 6,500 scene images in 11 Indian languages plus English.
  - Tasks: detection, script identification, cropped-word recognition and end-to-end recognition.
  - Team: 9 authors including Anand Mishra.
  - Venue: the DOI 10.1007/s10032-026-00583-9 is a Springer IJDAR-prefix DOI, so the journal is IJDAR [journal name inferred from the DOI prefix; not stated on the page].
  - Source: [arXiv 2511.23071](https://arxiv.org/abs/2511.23071v1)
- IndicVisionBench (Krutrim AI and OLA Electric, 9 authors):
  - Data: about 5K images and 37K+ QA pairs, English plus 10 Indic languages.
  - Tracks: VQA, multimodal MT, and OCR on 876 document images taken from Wikisource "Level-4" human-verified pages.
  - The paper says "existing OCR benchmarks are largely English-centric".
  - Source: [arXiv 2511.04727](https://arxiv.org/html/2511.04727)
  - Listed as ICLR 2026 by [mlanthology](https://mlanthology.org/iclr/2026/faraz2026iclr-indicvisionbench/) and [OpenReview](https://openreview.net/forum?id=LmJoLn04iL). The arXiv page shows no venue, and the track (main or workshop) was not confirmed.
- HinTel-AlignBench (Hindi and Telugu VLM benchmark, 4,000 QA pairs per language, semi-automated translation with human verification). It found average drops of 8.3 points (Hindi) and 5.5 points (Telugu) relative to English. Published at the ALVR workshop at ACL 2026, as a 6-page paper. — [ACL Anthology 2026.alvr-main.26](https://aclanthology.org/2026.alvr-main.26/)
- Others found but not examined in depth: IndicSTR12 (IIIT-H, 2023) ([CVIT](https://cvit.iiit.ac.in/research/projects/cvit-projects/indicstr)); the ICDAR 2025 Competition on Multi-lingual Roadside Scene Text Recognition ([ILOCR IIIT](https://ilocr.iiit.ac.in/icdar_2025_MLT-RSTR/)); HW-MLVQA, a multilingual handwritten document VQA benchmark ([arXiv 2507.15655](https://arxiv.org/html/2507.15655v1)); NE-OCR, covering 10 Northeast Indian languages ([ResearchGate](https://www.researchgate.net/publication/402902655_NE-OCR_Unified_Optical_Character_Recognition_for_10_Languages_of_Northeast_India)); and IIIT-H CVIT's "Adapting VLMs for Hindi OCR" (2025) ([PDF](https://cvit.iiit.ac.in/images/ConferencePapers/2025/adapting-Vision-Language-ocr.pdf)).

#### Inferences
- The venue ladder for this genre, roughly:
  - arXiv only.
  - Workshop (ALVR, CVPR workshops).
  - ICDAR, Findings, or journals such as IJDAR.
  - Main conferences and ICLR/NeurIPS E&D.
- Moving up the ladder tracks scale (thousands of samples), real human annotation by native speakers, task breadth, and a strong evaluation or analysis.

#### Gaps
- I did not cover Vietnamese or Persian OCR benchmarks this session.

### Q4. What reviewers expect of a benchmark paper in 2026; rejection reasons and cost

#### Takeaway
NeurIPS 2026 renamed the D&B track the "Evaluations & Datasets" track and moved it to double-blind by default. Submissions must meet these conditions:
- The dataset must be publicly accessible at submission time on a persistent host.
- A Croissant metadata file, including Responsible-AI fields, is required.
- Code is required for executable benchmark artifacts.
- The paper must state the claims, assumptions and limitations of its evaluation.
- An inaccessible dataset justifies desk rejection.

The track says its bar matches the main track.

#### Cited Findings
- NeurIPS 2026 E&D track rules:
  - Formerly D&B; it now treats "evaluation itself as a subject of study".
  - Submissions must state the evaluative role of the contribution: the claims it supports, its assumptions and its limitations.
  - Double-blind is the default, with single-blind available only when anonymisation is impossible.
  - Data must sit on Dataverse, Kaggle, Hugging Face or OpenML (preferred), be available at submission, and stay available long-term.
  - A Croissant file with core and RAI fields is mandatory.
  - Code is mandatory when the contribution is an executable artifact.
  - Inaccessible data or code "justifies the desk rejection of the paper".
  - Review stringency equals the main track.
  - 2026 dates: full paper deadline 6 May 2026, notification 24 Sep 2026.
  - Source: [NeurIPS 2026 E&D CFP](https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets)
- NeurIPS separately published RAI metadata requirements for the 2026 track. — [NeurIPS blog, May 2026](https://blog.neurips.cc/2026/05/04/responsible-ai-metadata-requirements-for-the-evaluations-and-datasets-track-neurips-2026/)
- Problems seen in 2025 submissions:
  - Missing license information (11.9%), dataset descriptions (4.9%) and URLs (3.5%).
  - Minimal adoption of RAI metadata.
  - Trouble hosting large datasets.
  - The track also says a dataset's impact depends on "enabling future research, surfacing underexplored problems, or challenging dominant evaluation paradigms".
  - Source: [NeurIPS blog, Dec 2025](https://blog.neurips.cc/2025/12/05/neurips-datasets-benchmarks-track-from-art-to-science-in-ai-evaluations/)
- Annotation-effort data points from the papers above:
  - OCRTurk: 2 annotators, 180 pages. [arXiv](https://arxiv.org/html/2602.03693v1)
  - KRETA: semi-automated pipeline with human reviewers, 2.5K items. [ACL](https://aclanthology.org/2025.emnlp-main.1696.pdf)
  - IndicDLP: 63 annotators plus a reviewer and superchecker per language. [CVIT](https://cvit.iiit.ac.in/research/projects/cvit-projects/indicdlp)
- Source licensing is handled in a few ways:
  - Using copyright-free and government material plus the authors' own photographs (KRETA).
  - Using Wikisource human-verified scans (IndicVisionBench OCR).
  - Using open repositories such as arXiv and DergiPark (OCRTurk).
  - Sources: [KRETA](https://aclanthology.org/2025.emnlp-main.1696.pdf); [IndicVisionBench](https://arxiv.org/html/2511.04727); [OCRTurk](https://arxiv.org/html/2602.03693v1)

#### Inferences
- Common reasons for rejection, inferred from the requirements and observed weaknesses rather than an official list:
  - Data is too small or too narrow, with no new insight beyond "models do worse on language X".
  - Labels are LLM-generated without human verification.
  - Licensing or redistribution rights are unclear.
  - The test set may be contaminated, for example by Wikisource or public pages already in VLM training data.
  - No human baseline and no inter-annotator agreement.
  - No maintenance or hosting plan.
  - Missing Croissant/RAI metadata.
- An undergraduate can meet these requirements, but they demand discipline and time, likely several months of part-time work. Hand-verifying Markdown, LaTeX and HTML is slow.

#### Gaps
- I found no official NeurIPS 2026 E&D acceptance rate or reviewer-rejection statistics. I found no hard figures on annotation hours or cost per page for OCR benchmarks.

### Q5. Is there a gap for an Indian-language or other low-resource-script OCR/VLM benchmark as of Oct 2026?

#### Takeaway
Indic scene text, layout and general VQA are already fairly well covered: BSTD, IndicSTR12, IndicDLP, IndicVisionBench and HinTel-AlignBench. Industry players such as Krutrim, Sarvam and AI4Bharat are active. The papers themselves name remaining gaps:
- Public benchmarks for end-to-end document parsing (page to Markdown, HTML and LaTeX, in the style of OmniDocBench and OCRTurk) for Indic scripts, especially on dense or non-book documents such as forms and index pages, rare scripts, handwriting and low-resolution scans.
- A public benchmark for government-document key-field extraction.

A narrowly scoped, carefully verified benchmark of this kind in one or two languages is a realistic ICDAR-workshop, ALVR/Findings or journal target for a student. A top main-conference acceptance is unlikely without senior collaborators and scale.

#### Cited Findings
- Krutrim's 2026 production-OCR paper:
  - Prior Indic OCR work leans toward scene text and benchmarks, with less work on printed document OCR under dense layouts.
  - Accuracy drops on rare scripts, forms and index pages, and on handwriting and noisy or low-resolution scans.
  - Its government-document KIE evaluation uses proprietary data, so "there is no public benchmark" for that task.
  - Its Chitrapathak labels came from Google Cloud OCR, which makes them noisy.
  - Source: [arXiv 2602.16430](https://arxiv.org/html/2602.16430v1)
- IndicVisionBench's OCR track has only 876 document images from Wikisource and states that OCR benchmarks are largely English-centric. — [arXiv 2511.04727](https://arxiv.org/html/2511.04727)
- OCRTurk's related work cites only IndicSTR12 for Indic OCR. That suggests no prominent Indic OmniDocBench-style parsing benchmark had reached that literature by Feb 2026. — [arXiv 2602.03693](https://arxiv.org/html/2602.03693v1)
- Industry is active:
  - Sarvam Vision offers a closed multilingual Indic document AI. [Sarvam blog](https://www.sarvam.ai/blogs/sarvam-vision)
  - Bodhan AI released Indic OCR models in Sept 2026. [Analytics Vidhya](https://www.analyticsvidhya.com/blog/2026/09/bodhan-ai-indic-models/)
  - A GitHub dataset claims 13.25M samples across 23 Indic languages (unreviewed). [GitHub IndicOCR](https://github.com/Faizaniqbal52/IndicOCR)

#### Inferences
- A gap still appears to exist for a public, human-verified Indic document-parsing benchmark with tables, equations, reading order and mixed script, rare scripts or under-served document types such as forms, old print and handwritten records. Two risks: competition from well-funded Indian labs, and the chance that a similar benchmark appeared in 2026 and was missed here.
- The student's reasoning ("those papers are basic, so I can do it") is half right:
  - The method in such papers is indeed simple: evaluating existing models.
  - Acceptance depends on real, licensed, human-verified data, systematic evaluation, error analysis, and a release that meets 2026 standards (hosting, Croissant, license, documentation).
  - It also helps to have an advisor with venue experience. Almost every accepted example above had senior or industry co-authors.
- A realistic path:
  1. Choose one or two languages they are native in and a document type absent from the list above.
  2. Annotate about 200–500 pages with verification and inter-annotator agreement.
  3. Evaluate about 8–15 OCR systems and VLMs.
  4. Target an ICDAR or ACL/CVPR workshop, or a journal, before aiming at NeurIPS E&D or ACL Findings.

#### Gaps
- I did not run a full search for every Indic document-VQA or parsing benchmark from 2026, so an OmniDocBench-style Indic benchmark may have appeared that I missed. Those to check include anything named "IndicDocBench", "Indic-OmniDoc" or similar, and the AI4Bharat 2026 releases.
- I did not confirm IndicVisionBench's ICLR 2026 track.

## Notes: OCR hallucination cube and benchmarks / ocr_hallucination.md

## OCR Hallucination in VLMs (as of Oct 2026): Benchmarks, Methods, Open Gaps, and a Laptop-Feasible Project Framing

Verification key: **VERIFIED** = abstract/HTML fetched this session; **SNIPPET** = search-result title/URL only; **UNVERIFIED** = background knowledge or inference, not checked. Builds on `/home/claude/research_notes/Vision SSL ideas reality check/ocr_text_landscape.md`. That file covers PAR, 2604.09364, 2606.28273, 2609.18823, GRC 2603.19790, and HIPE-OCRepair, and its findings are not repeated here.

### Q1. What OCR-hallucination benchmarks and datasets exist, and which are open?

#### Takeaway
At least five 2025–2026 benchmarks target OCR hallucination or prior reliance. They cover:
- **non-semantic scene text** (TextHalu-Bench, NeurIPS-track 2025, arXiv 2506.20168 / 2506.05551);
- **degraded KIE documents** with a refusal option (KIE-HVQA);
- **controlled word-level corruption**, including letter swaps, letter shuffles and zero-prior random strings (the DeepSeek-OCR study 2601.03714);
- **counterfactual glyph perturbation plus image-gain** on Ancient Greek (2605.27750);
- **synthetic multi-script rendering** (GlotOCR Bench, 158 scripts).

The axis of **lexical familiarity** (real word / misspelling / nonword / number / rare name) has been probed piecemeal. The study that comes closest to a cross with visual legibility is 2601.03714, which has three corruption types and three DeepSeek-OCR resolution modes. However, it is a behavioural study of one model family and has no fine-grained legibility sweep or internal analysis.

#### Cited Findings
**Hallucination-specific OCR benchmarks**
- **TextHalu-Bench** ("When Semantics Mislead Vision", arXiv 2506.05551). VERIFIED.
  - 1,740 samples of semantic vs non-semantic scene text (isolated numbers, incomplete words, rare/OOV tokens), drawn from ICDAR13/15/19, CCPD, MSRA-TD500, RoadText and MPSC. It has two subtasks, Spotting and Understanding.
  - F1 scores: GPT-4o 45.3, humans 96.8.
  - Code: github.com/shuyansy/MLLM-Semantic-Hallucination. It is not confirmed that the data are released there.
  - — [arXiv HTML](https://arxiv.org/html/2506.05551v2)
- **KIE-HVQA** ("Seeing is Believing? Mitigating OCR Hallucinations in MLLMs", NeurIPS 2025, arXiv 2506.20168). VERIFIED.
  - Billed as the "first benchmark" for OCR hallucination in degraded document understanding. It covers ID cards and invoices with simulated real-world degradations and tests whether models refuse when text is illegible.
  - Size and data link were not stated on the abstract page.
  - — [arXiv](https://arxiv.org/abs/2506.20168); [NeurIPS](https://papers.nips.cc/paper_files/paper/2025/hash/6b628a3d7cb8055eb6fd2dd48c586347-Abstract-Conference.html)
- **"HalluText: Towards Benchmarking and Mitigating OCR Hallucination for LVLMs"** (OpenReview). SNIPPET only, because the page was blocked by a verification wall. Content, venue and openness are unknown. — [OpenReview](https://openreview.net/forum?id=LRnt6foJ3q)
- **GlitchText Probing Dataset** (PAR, ACL 2026). Covered in the earlier notes. No public repo was found in this session's search. — [ACL](https://aclanthology.org/2026.acl-long.1065/)

**Controlled lexical-prior probes (closest to the "cube")**
- **"Visual Merit or Linguistic Crutch? A Close Look at DeepSeek-OCR"** (arXiv 2601.03714). VERIFIED.
  - **Sentence-level test:** on 112 Fox-benchmark English pages, key words were replaced with absurd but visually similar substitutes ("butterfly" → "breadflutter").
  - **Word-level test:** letters were swapped or shuffled in 5% or 10% of words, and zero-prior random strings (2–10 mixed-case letters) were also used.
  - **DeepSeek-OCR precision on random strings:** 19.84% (Tiny), 42.12% (Small) and 61.70% (Base). This means higher visual resolution, which is a legibility proxy, reduces prior reliance.
  - **Drop on random strings by model:** DeepSeek-OCR Tiny −68.16 pts, HunyuanOCR −59.79, Nougat −58.88, Qwen2.5-VL-7B −51.24. The pipeline OCR PaddleOCR-v5 lost only about 4.9 (to 89.53%).
  - The authors say data and scripts are released on GitHub, but the link was anonymised in the PDF.
  - — [arXiv PDF](https://arxiv.org/pdf/2601.03714)
- **"Reading or Guessing?"** on Ancient Greek (arXiv 2605.27750). VERIFIED.
  - **Data:** 90 real scans from 30 editions, plus rendered counterfactual stimuli in which the perturbed string is the ground truth. A grounded model should reproduce the implausible glyphs.
  - **Error taxonomy:** 8 categories, with a 19,901-form lexicon used to separate real-word from non-word substitutions.
  - **Token-level "image gain":** the log-probability of each token with the image vs without it.
  - **Models:** Tesseract, Kraken, LightOnOCR-1B, DeepSeek-OCR, olmOCR-2-7B, Qwen3-VL-2B/8B.
  - Stimuli, code and per-error labels are released. Compute was about 100 GPU-hours.
  - — [arXiv HTML](https://arxiv.org/html/2605.27750v1)
- **ReViCo** ("Vision Language Models Are Not (Yet) Spelling Correctors", arXiv 2509.17418). VERIFIED. Real images with naturally occurring misspellings in Chinese and English, used to test visual spelling *correction*, which is the inverse task. VLMs fall far short of humans. No data link appears on the abstract page. — [arXiv](https://arxiv.org/abs/2509.17418)

**Robustness and multi-script benchmarks (adjacent)**
- **GlotOCR Bench** (arXiv 2604.12978). VERIFIED.
  - **Design:** 158 scripts, rendered synthetically with Google Fonts, HarfBuzz and FreeType, each in a clean and a degraded variant. Scripts are grouped into High (Latin), Mid (9 scripts incl. Arabic, Cyrillic, Han) and Low (148) tiers.
  - **Results across 14 systems:** Latin above 75% Acc@5. Low-tier scripts reach at best 7.7%, and most models fall below 1%.
  - **Failure mode:** models emit fluent text in a familiar script or hallucinate look-alike-script characters, e.g. Gujarati → Devanagari and Thaana → Arabic.
  - **Availability:** data at HF `cis-lmu/glotocr-bench` (evaluation-only licence); renderer at github.com/cisnlp/glotocr-bench (Apache-2.0).
  - — [arXiv HTML](https://arxiv.org/html/2604.12978v1)
- **Devanagari stress test** ("Can OCR-VLMs Read Devanagari?", arXiv 2606.29213). VERIFIED.
  - **Data:** 100 FLORES Hindi sentences in 5 fonts, each in a clean version plus blur, noise and low-DPI variants (400 images), plus 300 real Sanskrit-OCR-Typed images.
  - **Systems:** 10, including Qwen2.5-VL-3B, Qwen3-VL-8B, olmOCR-7B and DeepSeek-OCR.
  - **Results:**
    - Clean text does not discriminate between systems (chrF++ 91–98 for all).
    - DeepSeek-OCR has repetition loops up to 71.6× the reference length.
    - VLM errors concentrate on conjuncts, matras and nukta.
    - English OCR strength does not predict Indic OCR strength (olmOCR-7B 40.5 vs Qwen3-VL-8B 75.2 chrF++ on real scans).
  - The authors recommend reporting "median together with catastrophic-rate".
  - Repo: github.com/Aditya-PS-05/devanagari-ocr-benchmark.
  - — [arXiv HTML](https://arxiv.org/html/2606.29213)
- **OCR-Robust** ("How Robust is OCR-Reasoning?", 2606.26041). VERIFIED via an aggregator page, not arXiv.
  - **Data:** 812 samples (OCR1.0: 482; OCR2.0: 330).
  - **Perturbations:** 5 (glass blur, colour shift, elastic, motion blur, snow) × 3 severities.
  - **Metrics:** RCR, WCR and CRI, across 18 systems.
  - **Finding:** clean accuracy does not predict robustness.
  - The page has internal inconsistencies, e.g. it mentions pixelate.
  - — [hyper.ai](https://hyper.ai/fr/papers/2606.26041)
- KazakhOCR, a synthetic low-resource benchmark (arXiv 2603.13238). SNIPPET. — [arXiv](https://arxiv.org/abs/2603.13238)
- CC-OCR (arXiv 2412.02210) and OCRBench (github Yuliang-Liu/MultimodalOCR) are general OCR benchmarks for large multimodal models, not hallucination-specific. SNIPPET. — [CC-OCR](https://arxiv.org/html/2412.02210v3); [OCRBench GitHub](https://github.com/yuliang-liu/multimodalocr)
- A general (non-OCR) prior-reliance benchmark with 540 images × 4 question phrasings has OCR as one category. Qwen3.5-9B drops from 69.3% to 42.0% on vision-grounded phrasing (arXiv 2606.10400). VERIFIED via alphaXiv. — [alphaXiv](https://www.alphaxiv.org/abs/2606.10400)

#### Inferences
- **Open and usable on a laptop now:** the GlotOCR renderer and data (eval only), the Devanagari benchmark, and the Ancient Greek stimuli and code. TextHalu-Bench and the DeepSeek-OCR corruption scripts are probably open (repo exists or is claimed). KIE-HVQA, HalluText and GlitchText could not be confirmed open.
- The existing evidence already establishes the behavioural fact that end-to-end VLM OCR "repairs" nonwords and perturbed glyphs toward plausible words. A project that only shows this behaviour would not be novel. Novelty must come from (a) the full factorial cross, (b) per-token internal signals that predict the error without ground truth, and/or (c) a non-Latin script.

#### Gaps
- Exact sizes, licences and download links for KIE-HVQA and HalluText could not be verified.
- No benchmark was found that explicitly crosses graded legibility (continuous blur/contrast/size) × lexical class (word / misspelling / nonword / number / rare name) × script. Absence in search results is not proof that none exists.

### Q2. What detection and mitigation methods exist for OCR hallucination specifically?

#### Takeaway
The methods fall into four families:
- **training-based abstention** (KIE-HVQA's SFT + GRPO with a refusal reward);
- **training-free layer- or attention-level fixes** (Grounded Layer Correction + ZoomText; PAR's RoPE perturbation + attention recycling; CALRD's transition-layer logit blending, which is not OCR-specific);
- **contrastive decoding** (VCD, M3ID);
- **external black-box abstention** (GRC).

The most directly reusable *detection* signal is the per-token **image gain** of 2605.27750. It shows that prior reliance is model-specific: low for olmOCR's lexical errors, high for Qwen3-VL even when wrong. A ground-truth-free detector therefore cannot assume that "wrong = low image reliance" holds universally.

#### Cited Findings
- **Grounded Layer Correction + ZoomText** (2506.05551). VERIFIED.
  - Layers with more attention on ground-truth text regions hallucinate less (strong negative Spearman correlation).
  - Training-free: picks the most text-grounded layer by argmax and fuses its hidden state into the final layer (w = 0.1).
  - TextHalu-Bench F1: Qwen2.5-VL 48.3 → 53.8; Mini-Monkey 46.5 → 50.6; LLaVA-NeXT +0.6 only.
  - — [arXiv HTML](https://arxiv.org/html/2506.05551v2)
- **KIE-HVQA method** (2506.20168). VERIFIED. SFT + GRPO with a reward for self-awareness of visual uncertainty and refusal on ambiguous inputs. A Qwen2.5-VL-7B model gains about 22% absolute "hallucination-free accuracy" over GPT-4o. — [arXiv](https://arxiv.org/abs/2506.20168)
- **CALRD** ("MLLMs Get It Right, Then Get It Wrong", arXiv 2606.17953). VERIFIED. **Not OCR**: it uses text-context vs image conflicts (Conflict-VQA, PhD-icc, POPE, CHAIR).
  - A per-layer "Modal Dominance Ratio" via logit lens shows the visual answer leads in middle layers and the text answer overrides late.
  - 85% of failures shift toward text, while 89% of correct conflict cases hold or shift toward vision.
  - Training-free fix: blend transition-layer logits into the final logits with λ = D_conf·(1−ρ). Overhead is about 19.8 vs 18.3 ms/token.
  - The abstract's "up to 9.4%" did not exactly match the visible tables (about 9.0).
  - — [arXiv HTML](https://arxiv.org/html/2606.17953)
- **Interventions on Ancient Greek OCR** (2605.27750). VERIFIED.
  - VCD had no significant effect.
  - M3ID (image-free contrastive) significantly improved Qwen3-VL but not olmOCR.
  - Script masking badly hurt Qwen3-VL-8B (median CER 0.07 → 0.69).
  - Length abstention only matched baseline.
  - Post-OCR LM correction gave the broadest gains (5 of 7 systems).
  - Image-gain medians: olmOCR lexical errors 0.17 vs perceptual 1.40; Qwen3-VL-8B lexical 1.97 vs perceptual 1.30.
  - — [arXiv HTML](https://arxiv.org/html/2605.27750v1)
- **Post-correction transfer:** a ByT5-small corrector trained on EasyOCR errors helped EasyOCR (+1.2–1.5 chrF++) but was neutral or harmful on VLM outputs, so error distributions are engine-specific (2606.29213). VERIFIED. — [arXiv HTML](https://arxiv.org/html/2606.29213)
- **PAR** (RoPE phase noise + Foveal Attention Recycling, about 12% lower CER) and **GRC** (cross-view geometric probes with abstention) are covered in the earlier notes. — [ACL](https://aclanthology.org/2026.acl-long.1065/); [arXiv](https://arxiv.org/abs/2603.19790)
- **General (non-OCR) training-free decoding baselines.** SNIPPET only: Decoding by Perturbation (2604.12424), CVPR 2025 attention-causal decoding, and VCD (CVPR 2024). — [2604.12424](https://arxiv.org/html/2604.12424); [CVPR25](https://openaccess.thecvf.com/content/CVPR2025/papers/Tang_Seeing_Far_and_Clearly_Mitigating_Hallucinations_in_MLLMs_with_Attention_CVPR_2025_paper.pdf); [VCD](https://openaccess.thecvf.com/content/CVPR2024/papers/Leng_Mitigating_Object_Hallucinations_in_Large_Vision-Language_Models_through_Visual_Contrastive_CVPR_2024_paper.pdf)

#### Inferences
- The student's "handoff layer" is now closely pre-empted for general conflicts by CALRD (late-layer textual override, located with logit lens) and by 2604.09364. For OCR it is partly pre-empted by Grounded Layer Correction, which does argmax-layer fusion. What remains less covered is **using the layer-wise trajectory as a ground-truth-free per-token error detector for OCR**. That means evaluating detection by AUROC / selective-risk curves rather than mitigation, and comparing against cheap baselines: token probability/entropy, image gain (image vs no-image log-prob), and GRC-style cross-view agreement.
- Because 2605.27750 finds image gain is model-specific, a strong contribution would be a test of **which signal (logit-lens crossover, image gain, entropy, attention to the text region) predicts errors in which lexical class and at which legibility level**. That is exactly where the friend's reframe (rare names, numbers, misspellings, unfamiliar scripts) bites.

#### Gaps
- No paper was found that reports AUROC for ground-truth-free *token-level* OCR-hallucination detection that compares internal signals across lexical classes. This absence is unconfirmed, because the searches were limited.
- PAR's and HalluText's mitigation details for small (≤4B) models were not checked.

### Q3. What is still open and laptop-feasible? Models, tooling, experiment design, metrics, and the non-Latin angle

#### Takeaway
A sharp, feasible framing is: **"When does the prior win? A legibility × lexical-familiarity × script cube for VLM OCR, and which ground-truth-free signals predict prior-driven errors."**
- Render controlled stimuli with an open pipeline (the GlotOCR renderer or PIL + HarfBuzz).
- Run 2–4B open VLMs, which can be hooked with the Spectra library (supports Qwen2.5-VL, Qwen3-VL, SmolVLM, LLaVA-1.5) or nnsight.
- Measure (i) the *repair rate* (output = a nearby real word instead of the rendered nonword) and (ii) detection AUROC of per-token signals.

This is distinct from DeepSeek-OCR-only behavioural work (2601.03714), from mitigation-focused work (PAR, GLC, CALRD), and from the Greek case study (one script, real scans). The Devanagari/Hindi or Korean axis adds a script where prior and visual confusions differ (conjuncts and matras; look-alike scripts).

#### Cited Findings
- **Tooling:** Spectra (ACL 2026 demo) is a mechanistic-interpretability library built on HF Transformers. It supports Qwen2.5-VL, Qwen3-VL, LLaVA-1.5 and SmolVLM, with activation patching and attention-pattern analysis; logit lens was not mentioned on the page. Repo: github.com/clemneo/vlm-spectra. VERIFIED. — [ACL Anthology](https://preview.aclanthology.org/ingest-acl/2026.acl-demo.78/)
- **Small models already used in OCR-prior studies:**
  - Qwen3-VL-2B (Ancient Greek study) — [2605.27750](https://arxiv.org/html/2605.27750v1)
  - Qwen2.5-VL-3B (Devanagari study) — [2606.29213](https://arxiv.org/html/2606.29213)
  - LightOnOCR-1B (Ancient Greek study) — [2605.27750](https://arxiv.org/html/2605.27750v1)
  - DeepSeek-OCR at multiple resolution modes — [2601.03714](https://arxiv.org/pdf/2601.03714)
- **Resolution as a legibility knob:** DeepSeek-OCR precision on random strings rises with mode, Tiny 19.84% → Base 61.70%. — [2601.03714](https://arxiv.org/pdf/2601.03714)
- **Repair toward known words and scripts:** VLM substitutions are fluent, in-vocabulary words (Greek) — [2605.27750](https://arxiv.org/html/2605.27750v1). Unfamiliar scripts are mapped onto look-alike familiar scripts — [GlotOCR](https://arxiv.org/html/2604.12978v1).
- **Devanagari-specific failure points:** conjuncts, matras, nukta, and ba/va and da/dha confusions. Clean synthetic Hindi does not discriminate between models (chrF++ 91–98), so degradation is needed. — [2606.29213](https://arxiv.org/html/2606.29213)
- **Metric advice:** report the median plus a catastrophic-rate, because of repetition loops of up to 71.6× length. — [2606.29213](https://arxiv.org/html/2606.29213)
- **Detection baseline to beat or compare:** the image-gain token score — [2605.27750](https://arxiv.org/html/2605.27750v1). For mechanisms, use the CALRD transition-layer / MDR trajectory — [2606.17953](https://arxiv.org/html/2606.17953). For layer–grounding correlation, use GLC — [2506.05551](https://arxiv.org/html/2506.05551v2).

#### Proposed experiment design (inference; not sourced as a whole)
1. **Stimuli: render about 5–20k word images.**
   - Factor A, lexical class:
     - frequent real word;
     - single-edit misspelling (the edit chosen so the nearest real word is unambiguous);
     - pronounceable nonword (e.g. Wuggy-style; tool UNVERIFIED);
     - random string;
     - digit strings and IDs;
     - rare proper names.
   - Factor B, legibility: about 6 graded levels of Gaussian blur / font size / contrast / JPEG quality, and optionally low-DPI as in 2606.29213.
   - Factor C, script: Latin vs one non-Latin script. Devanagari is suggested because it has an existing open benchmark plus conjunct structure; Korean Hangul is an alternative because its syllable blocks allow clean "nonword" blocks. Use the GlotOCR renderer for correct shaping.
   - Include word-in-sentence context vs isolated word as an optional factor, since PAR reports grounding declines with generation length.
2. **Models (all ≤4B):**
   - Qwen2.5-VL-3B and Qwen3-VL-2B/4B: general models, hookable via Spectra.
   - SmolVLM: hookable via Spectra.
   - One OCR specialist as a behavioural contrast: LightOnOCR-1B, Florence-2 or GOT-OCR2.
   - Optionally PaddleOCR or Tesseract as a "no-prior" control. 2601.03714 shows pipeline OCR is nearly prior-immune (−4.9 vs −51 to −68 pts).
3. **Behavioural metrics:**
   - exact match and CER per cell;
   - **repair rate**, the fraction of errors where the output is a dictionary word, or the specific source word for misspellings;
   - **legibility threshold**, the blur level at which 50% correct is reached, per lexical class. The gap between the word threshold and the nonword threshold quantifies prior strength.
   - catastrophic-rate.
4. **Ground-truth-free detection (core contribution).** Per output token, compute:
   - softmax probability and entropy;
   - image gain (log p with the image − log p with a blank image or no image);
   - logit-lens rank of the final token across layers, and the "crossover layer" where the correct-vs-output preference flips (CALRD MDR analogue);
   - attention mass on image tokens and the text region.

   Evaluate with AUROC / AUPRC for predicting a wrong token, and with risk–coverage curves (selective prediction). Stratify by lexical class × legibility. The hypothesis to test is that probability is overconfident on repaired misspellings while image-gain or crossover signals are not.
5. **Causal check (small):** on a subset, use activation patching (Spectra) from the clean high-legibility rendering into the blurred rendering. Alternatively, ablate the top "prior" heads, following the 2606.28273 recipe, and see whether repairs flip. This connects the original "handoff layer" idea without making it the whole project.

#### Feasibility on 8 GB (inference; UNVERIFIED)
- 2–4B VLMs in bf16 need roughly 4–9 GB for the weights alone. 4-bit (bitsandbytes) brings 3–4B to about 2.5–3.5 GB, but hooks on quantised linear layers can be awkward. 2B models in fp16 are the safest choice for patching and logit lens, and short single-word images keep the visual-token count small (Qwen dynamic resolution).
- Image-gain and logit lens need only forward passes and cached hidden states, so they fit easily. Activation patching on short sequences is also feasible. Full-page documents would not be.
- Compute reference: the Greek study used about 100 GPU-hours across 7 systems on full pages — [2605.27750](https://arxiv.org/html/2605.27750v1). Single-word stimuli should be far cheaper (inference).

#### Inferences
- **Recommended single-sentence framing:** "We map where the language prior overrides visual evidence in small VLM OCR across a legibility × lexical-familiarity × script cube, and test which ground-truth-free signals (confidence, image gain, logit-lens crossover) flag prior-driven misreads, especially for misspellings, numbers, rare names and Devanagari."
- **Risks:**
  - Reviewers may see the behavioural half as known (2601.03714, 2605.27750, TextHalu-Bench). The student must lead with the *detection-signal comparison by cell*.
  - CALRD and GLC limit claims of novelty for a "handoff layer". Cite them and position the layer analysis as a detector, not a new mechanism.

#### Gaps
- No VRAM measurements were found for Qwen3-VL-2B/4B, InternVL, Florence-2, GOT-OCR2 or olmOCR under hooks. olmOCR is 7B, so it likely needs 4-bit and is a poor fit for interpretability on 8 GB (UNVERIFIED).
- Spectra's support for InternVL, Florence-2 and GOT-OCR2 is not stated. TransformerLens VLM support was not checked.
- Korean and Arabic OCR-hallucination studies specific to 2026 were not found beyond GlotOCR's Mid-tier aggregate (Arabic included). The Korean angle is unverified.
- Whether a pronounceable-nonword generator is suitable for Hindi or Korean was not researched.

## Notes: Vision SSL ideas reality check / graph_cube_tabular.md

## Fact-check: small-world attention / small-world MARL / Rubik's cube sampling / tabular SSL (as of Oct 12, 2026)

### Q1. Do the cited papers exist and match their descriptions?

#### Takeaway
Every arXiv ID cited by the student and the friend resolves to a real paper, and most match their descriptions. Two need correcting. The 2605.00951 survey is about rewiring for over-squashing and over-smoothing; its abstract does not say "small-world". The ScienceDirect traffic paper exists (EAAI 2026), but its full text was not reachable here, so it is unconfirmed whether its small-world graph is the agents' communication topology or a model of the road network.

#### Cited Findings
- **arXiv 2512.09182**: "Understanding the Failure Modes of Transformers through the Lens of Graph Neural Networks", Hunjae Lee, Dec 9, 2025. It analyzes transformer (mainly decoder-only, causal-mask) failures as information-propagation bottlenecks using GNN theory, and unifies ad hoc fixes. It is about LLMs/causal masking, not ViTs or small-world masks. — [arXiv](https://arxiv.org/abs/2512.09182)
- **arXiv 2512.18094**: "Rethinking Multi-Agent Intelligence Through the Lens of Small-World Networks", Wang, Li, Huang, Dong, Dec 19, 2025. Its testbed is LLM multi-agent debate. Small-world connectivity gives similar accuracy/token cost to other structures but more stable consensus. It also proposes uncertainty-guided rewiring (long-range links between agents with divergent beliefs, using semantic entropy). The student's claim that it is "LLM debate, not RL" is **correct**. — [arXiv](https://arxiv.org/abs/2512.18094)
- **arXiv 2605.00951**: "Graph Rewiring in GNNs to Mitigate Over-Squashing and Over-Smoothing: A Survey", Attali, Pernelle, Buscaldi, Malliaros, May 1, 2026. It supports "GNN rewiring is saturated", but the abstract does not use the term "small-world". — [arXiv](https://arxiv.org/abs/2605.00951)
- **arXiv 2007.14062**: BigBird (Zaheer et al., 2020), a sparse attention mechanism with linear scaling, global tokens, and universal-approximation/Turing-completeness results. — [arXiv](https://arxiv.org/abs/2007.14062)
- **The BigBird body text explicitly motivates its design with Watts–Strogatz small-world graphs.** Quotes: "a class of random graphs, known as small world graphs, exhibit high clustering coefficient"; "A particular model introduced by Watts and Strogatz 1998 is of high relevance to us." Random attention gives short paths (expander/Erdős–Rényi argument) and the sliding window gives clustering/locality. — [ar5iv BigBird](https://ar5iv.labs.arxiv.org/html/2007.14062)
- **arXiv 2311.05988**: "Vision Big Bird: Random Sparsification for Full Attention", Zhang & Gong, Nov 10, 2023. It splits ViT heads into three groups: a CNN local branch, Random Sampling Windows (random sparse attention), and average-pooled global attention. It reports that positional encoding can be removed without harm. — [arXiv](https://arxiv.org/abs/2311.05988)
- **ScienceDirect S0952197626002009**: "Small-World Topology and Graph Attention Reinforcement Learning for dynamic traffic optimization", Engineering Applications of Artificial Intelligence (2026). Page metadata: published Jan 28, 2026, DOI 10.1016/j.engappai.2026.113919, authors include Zhibin Gao and Weijian Xu. The only description available says it uses a "novel small-world topology to efficiently model traffic patterns and interactions." — [SynapseSocial record](https://www.synapsesocial.com/papers/69a75c06c6e9836116a24609); title also indexed at [OUCI](https://ouci.dntb.gov.ua/works/9JQbOejE/). The ScienceDirect page itself blocked fetching (robots), and the OUCI record failed to load.
- **arXiv 2502.18663**: "CayleyPy RL: Pathfinding and Reinforcement Learning on Cayley Graphs", Chervov, Obozov, Soibelman, Lytkin, Kiselev and ~29 others. Submitted Feb 25, 2025; v3 May 15, 2026. It combines RL with a "diffusion distance" approach and benchmarks random-walk generators. — [arXiv](https://arxiv.org/abs/2502.18663)
- **arXiv 2501.18580**: "Node Classification and Search on the Rubik's Cube Graph with GNNs", Alessandro Barro, Jan 2025. It frames distance estimation as GNN node classification, uses the predicted classes as an A* heuristic, and compares against DeepCubeA. — [arXiv](https://arxiv.org/abs/2501.18580)
- **arXiv 2304.01429**: "Learning from data with structured missingness", Mitra, McGough, … Holmes, … Bianconi, … MacArthur, Apr 2023. A review/perspective that defines "structured missingness" and proposes grand challenges. — [arXiv](https://arxiv.org/abs/2304.01429)
- **arXiv 2608.24381**: "When Does Self-Supervised Pretraining Help Tabular Models? A Study of Label Scarcity and Missing Data", Sahand Mazrouei, Aug 25, 2026. Details under Q5. — [arXiv](https://arxiv.org/abs/2608.24381)

#### Inferences
- The student cited 2512.09182 as support for small-world ViT masks, which is a stretch: that paper covers causal-mask LLMs.
- The friend's BigBird critique is stronger than the friend stated: BigBird is literally built on the Watts–Strogatz argument.

#### Gaps
- Full text of the EAAI traffic paper (S0952197626002009) could not be fetched. It is unconfirmed whether "small-world topology" there is the MARL communication graph, a road-network model, or both.

### Q2. Is small-world / random-graph sparse attention in transformers/ViTs prior art? Is the sample-efficiency framing still open?

#### Takeaway
"Small-world attention masks" are not unoccupied. BigBird (2020) derives local+random+global attention explicitly from Watts–Strogatz. Vision Big Bird (2023) ports the same idea to ViTs. Exphormer (2023) uses expander graphs for sparse graph transformers, and 2026 work continues the random-routing line. What may still be open is narrower: a controlled study of Watts–Strogatz rewiring probability *p* as a **data-efficiency inductive bias** for ViTs trained from scratch on small data. Even that sits next to a crowded "inductive bias for data-efficient ViTs" literature (ConViT, graph-ViTs), and I found no paper that does exactly this.

#### Cited Findings
- BigBird attention = window (local clustering) + random (short paths, expander) + global tokens, motivated explicitly by Watts–Strogatz small-world graphs. — [ar5iv BigBird](https://ar5iv.labs.arxiv.org/html/2007.14062)
- Vision Big Bird applies local (CNN) + random-window + pooled-global heads to ViTs. — [arXiv 2311.05988](https://arxiv.org/abs/2311.05988)
- Exphormer (Shirzad et al., 2023) builds sparse graph transformers from "virtual global nodes and expander graphs", relying on spectral expansion and pseudorandomness for linear complexity. — [arXiv 2303.06147](https://arxiv.org/abs/2303.06147)
- "Stochastic Attention: Connectome-Inspired Randomized Routing for Expressive Linear-Time Attention" (Jin & Sui, Apr 2026) randomly permutes tokens before sliding-window attention. It is inspired by the fruit-fly connectome's short path lengths and gives global reach in logarithmically many layers. The abstract does not use the words "small-world" or "Watts–Strogatz", and it is evaluated on language models, not vision; it is framed around efficiency/expressivity, not sample efficiency. — [arXiv 2604.00754](https://arxiv.org/abs/2604.00754)
- HopFormer (Feb 2026) is a graph transformer with head-specific n-hop masked sparse attention. It reports that localized attention is more stable on graphs with strong small-world properties. Here small-world describes the input graph, not the attention mask. — [arXiv 2602.02268](https://arxiv.org/abs/2602.02268)
- Graph-related work on topological masking with graph random features also exists. — [arXiv 2410.03462](https://arxiv.org/html/2410.03462v2) (not fetched in detail)
- The data-efficient ViT inductive-bias framing is well populated, e.g. ConViT (soft convolutional biases, ICML 2021) — [PMLR](https://proceedings.mlr.press/v139/d-ascoli21a/d-ascoli21a.pdf). Another example is "Graph-based vision transformer with sparsity for training on small datasets from scratch" (Sci. Rep. 2025). It uses 8-neighbour grid adjacency plus similarity, explicitly for small datasets, but **no** small-world or random long-range edges. — [Nature Sci Rep](https://www.nature.com/articles/s41598-025-10408-0)
- My searches for "small-world" + vision transformer + data-efficiency returned no paper with that exact combination. — [search results incl. ConViT, IBiT, GvT](https://www.nature.com/articles/s41598-025-10408-0)

#### Inferences
- The student's "searched specifically … found nothing" is false for the mechanism, because BigBird and Vision Big Bird are canonical. It is plausibly true only for the precise framing: a rewiring-probability sweep as a sample-efficiency bias in small-data ViTs.
- A defensible reframing would cite BigBird and Vision Big Bird as the mechanism's origin. It would then pose the question "does the WS interpolation parameter p trade off locality bias vs. reach in a data-size-dependent way?" with baselines: local-only, BigBird-style, full attention, and ConViT.
- Feasibility: CIFAR-scale or Tiny-ImageNet ViTs with masked attention fit on 8 GB. Masks give no speedup without sparse kernels, which matches the student's "not speed" framing.

#### Gaps
- No exhaustive OpenReview/Semantic Scholar sweep was done. A 2025–2026 workshop paper on "small-world ViT" could exist undetected.
- Not verified: whether Vision Big Bird reports small-data or sample-efficiency results.

### Q3. Is small-world communication topology in MARL unclaimed?

#### Takeaway
"Unclaimed" is overstated. The EAAI 2026 traffic paper puts "small-world topology" and graph-attention RL in its title. Graph-structured and learned-sparsity communication in MARL is a mature area, and social-network-structure studies of emergent communication date back to 2020. A systematic comparison of WS-p sweeps for agent communication graphs in standard MARL benchmarks was not found, but the space is adjacent to heavy prior work.

#### Cited Findings
- The EAAI 2026 paper "Small-World Topology and Graph Attention Reinforcement Learning for dynamic traffic optimization" exists (DOI 10.1016/j.engappai.2026.113919). The exact role of the small-world graph could not be verified. — [SynapseSocial](https://www.synapsesocial.com/papers/69a75c06c6e9836116a24609)
- Dubova, Moskvichev & Goldstone (2020), "Reinforcement Communication Learning in Different Social Network Structures", studies how population network structure (global connectivity, agent degree) shapes emergent RL communication conventions. The abstract does not explicitly say whether small-world graphs were tested. — [arXiv 2007.09820](https://arxiv.org/abs/2007.09820)
- 2512.18094 applies small-world topology and rewiring to LLM agents, not RL. — [arXiv](https://arxiv.org/abs/2512.18094)
- Related graph-communication MARL work surfaced in search but was **not fetched/verified** here:
  - "Learning Multi-Agent Coordination through Connectivity-driven Communication" [arXiv 2002.05233](https://arxiv.org/pdf/2002.05233)
  - the 2026 survey "Communication Methods in Multi-Agent Reinforcement Learning" [arXiv 2601.12886](https://arxiv.org/pdf/2601.12886)
  - "Communication Learning in Multi-Agent Systems" [arXiv 2411.00382](https://arxiv.org/html/2411.00382v1)
- DGN (graph convolutional RL), TarMAC (targeted attention communication) and MAGIC (graph-attention communication) are well-known prior art on learned/graph communication structure. This comes from background knowledge and was not verified with fetched sources in this session.

#### Inferences
- A novelty claim would need to be narrower: for example, fixed WS-p communication graphs as a prior versus learned graphs (DGN/MAGIC) at scale N, with robustness to agent dropout. It must cite the EAAI traffic paper and the 2601.12886 survey.
- Single-GPU feasibility is reasonable for small benchmarks (MPE/predator-prey, SMAC-lite), which is a general judgment.

#### Gaps
- EAAI paper's full methodology.
- Whether 2601.12886 already reviews small-world topologies (not fetched).

### Q4. Rubik's cube: is the "random scrambles concentrate near the diameter" claim right? What is DeepCubeA's real compute? What are the alternatives?

#### Takeaway
The student's mechanism is half-right but misdescribes DeepCubeA. For long random walks, distance does concentrate: in half-turn metric ~97% of all states are at distance 17–18, and walks mix after ~30 moves. However, DeepCubeA does **not** use only long scrambles. It samples scramble length uniformly from 1 to K=30, so short-distance states are well represented. Mid-length scrambles are noisy because random-walk length is not equal to true distance, which is a different and subtler issue. The friend is right on compute. DeepCubeA trained for 36 h on 2 Titan V GPUs plus 6 GPUs for data generation, 1M iterations at batch 10,000, so "negligible compute" is wrong at DeepCubeA scale.

#### Cited Findings
- **DeepCubeA training distribution:** "ki is uniformly distributed between 1 and K"; for the cube "K was set to 30"; for the 15-puzzle, 24-puzzle and Lights Out, K = 500. — [DeepCubeA paper PDF (Agostinelli et al., Nature Machine Intelligence 2019)](https://deepcube.igb.uci.edu/static/files/SolvingTheRubiksCubeWithDeepReinforcementLearningAndSearch_Final.pdf)
- **DeepCubeA compute:** "Training was carried out for 1 million iterations on two NVIDIA Titan V GPUs, with six other GPUs used in parallel for data generation"; batch size 10,000; "Training was completed in 36h." — [DeepCubeA PDF](https://deepcube.igb.uci.edu/static/files/SolvingTheRubiksCubeWithDeepReinforcementLearningAndSearch_Final.pdf); same figures in [NVIDIA blog](https://developer.nvidia.com/blog/ai-solves-the-rubiks-cube-in-a-fraction-of-a-second/)
- **GitHub README:** pre-trained models used "1-4 GPUs and 20-30 CPUs", with training "often stopped and started again". The 15-puzzle example uses `--states_per_update 50000000 --max_itrs 1000000 --back_max 500`. The README gives no duration in days. — [GitHub DeepCubeA](https://github.com/forestagostinelli/DeepCubeA)
- **Distance distribution (HTM):** d=16 ≈2.5%, d=17 ≈28.3%, d=18 ≈68.9%, d=19 ≈3.5%, d=20 only ~490 million states (~1e-11). The page notes that the 16–20 rows are estimates and that its fractions don't sum exactly. — [cuberoot.me](https://www.cuberoot.me/math/group/distance); God's number = 20 (HTM) — [cube20.org](https://cube20.org/)
- **QTM:** diameter 26, random-state average ~22. — [cuberoot.me](https://www.cuberoot.me/math/group/distance)
- **Random-walk dynamics (QTM, 12 moves):**
  - In the mid range, ~9.34 of 12 moves increase distance and 2.66 decrease it.
  - Depth has the same parity as the walk length.
  - The walk gets "trapped" near depth class 21.
  - p(d|N) is close to stationary after N ≈ 31–32.
  - At N=18, depth 17 is more likely than depth 19, so walk length overestimates distance.
  - Source: [Towards Data Science, "Rubik's cubes and Markov chains"](https://towardsdatascience.com/a-random-walk-on-the-rubiks-cube-684dd304bf3e/), a blog post (secondary, but quantitative).
- **Prior work on training data for cube solvers:**
  - EfficientCube (Takano, "Self-Supervision is All You Need for Solving Rubik's Cube") trains on random scrambles from the goal state. It reports beating DeepCubeA on the Rubik's Cube, 15 Puzzle and 7×7 Lights Out "with significantly less training data", and studies scaling with model size and data volume. — [arXiv 2106.03157](https://arxiv.org/abs/2106.03157)
  - CayleyPy RL benchmarks random-walk generators and a diffusion-distance approach. — [arXiv 2502.18663](https://arxiv.org/abs/2502.18663)
  - The GNN node-classification heuristic paper is [arXiv 2501.18580](https://arxiv.org/abs/2501.18580).
  - "Learning Empirically Admissible Neural Heuristics for Combinatorial Search" (June 2026) calibrates learned heuristics with validation scrambles. — [arXiv 2606.04860](https://arxiv.org/abs/2606.04860)
  - Older work: "Deep Heuristic-learning in the Rubik's Cube Domain: an Experimental Evaluation" — [CEUR-WS](https://ceur-ws.org/Vol-1885/57.pdf).

#### Inferences
- "More data doesn't help because states concentrate at the diameter" does not describe DeepCubeA, which uses uniform k∈[1,30]. The real issues are (a) noisy labels/coverage for mid-range k, where walk length ≠ distance, and (b) whether uniform-in-k is the right mix. EfficientCube already studies data scaling, so the claim "more data doesn't help" contradicts its scaling study unless reframed. "Doesn't help" and "hurts" are indeed different claims, as the friend says.
- Exact distance sampling for the 3×3×3 is impractical at training scale. Optimal solvers exist, but labeling millions of states is costly. The friend is right here. Cheap exact-distance testbeds avoid this. Background knowledge, not fetched here:
  - 2×2×2 cube: 3,674,160 states, full BFS table, God's number 11 HTM / 14 QTM
  - 8-puzzle: 181,440 reachable states
  - Small Lights Out boards, with exact solutions via linear algebra over GF(2)
  - These make "sample by true distance vs. by walk length" a clean, cheap experiment on an 8 GB GPU.
- Compute: DeepCubeA-scale replication (36 h × 2 GPUs + 6 data GPUs, 10^10 training states) is not "negligible" on one laptop GPU. A 2×2×2 or 8-puzzle study would be.

#### Gaps
- Later Agostinelli work (e.g. Q* search, DeepCubeA2/curricula) was not fetched; whether it addresses training distribution is unverified.
- The 2×2×2/8-puzzle/Lights Out state counts come from background knowledge and were not verified with a fetched source in this session.
- The EfficientCube hardware/compute figures were not in the abstract.

### Q5. Tabular SSL idea: what does arXiv 2608.24381 actually find?

#### Takeaway
The Aug 2026 study finds that tabular SSL beats scratch on average but not significantly. SSL helps most on *clean* datasets and often **hurts** on datasets with high native missingness, contrary to the imputation-objective hypothesis. Robustness gains under injected MCAR/MNAR shift are positive on average but non-significant after correction. The pretext-task choice doesn't matter. This leaves room for a structured-missingness "shortcut" study, but this paper is the direct baseline it must engage.

#### Cited Findings
- At 10% labels, SSL reaches ~0.8954 AUC versus 0.9015 for Random Forest. SSL vs. scratch gains vary and are not significant (p = 0.626 at 5% and 10% labels). — [arXiv 2608.24381](https://arxiv.org/abs/2608.24381)
- The hypothesis that imputation-style objectives help natively missing data was not supported. SSL's gains are most reliable on clean datasets, and it often degrades performance under high inherent missingness. — [arXiv 2608.24381](https://arxiv.org/abs/2608.24381)
- Test-time missingness: MCAR gives +0.0245 AUC (positive on 11/14 tasks) and MNAR/structured shift gives +0.0418 AUC (8/14). Neither is significant after Holm–Bonferroni. — [arXiv 2608.24381](https://arxiv.org/abs/2608.24381)
- Their mask-and-recover objective shows no significant difference versus VIME, SCARF and SubTab under an identical encoder. — [arXiv 2608.24381](https://arxiv.org/abs/2608.24381)
- Structured missingness (missingness linked to the data) is framed as an unsolved grand challenge. — [arXiv 2304.01429](https://arxiv.org/abs/2304.01429)

#### Inferences
- The finding that SSL often hurts under high native missingness is consistent with a "missingness-pattern shortcut" hypothesis: masked-reconstruction encoders may learn the mask structure rather than the values. 2608.24381 does not appear (from its abstract) to test that mechanism directly, so a targeted study, such as controlled MNAR synthetic shortcuts or probing whether embeddings encode the missingness indicator, looks open and is laptop-feasible.
- It is a single-author arXiv preprint with 14 tasks. Its results are non-significant, so treat it as weak evidence.

#### Gaps
- The full paper was not read: dataset list, encoder, and whether missingness-indicator shortcuts are analyzed are all unverified.

## Notes: Vision SSL ideas reality check / ocr_text_landscape.md

## OCR / Text-Recognition Research Landscape (2024 – Oct 2026) and Fact-Check of Friend's Critique

Verification status key: **VERIFIED** = abstract/landing page fetched this session; **SNIPPET** = seen only as a search-result title/URL; **UNVERIFIED** = from background knowledge, not checked this session.

### Q1. Do the friend's citations exist and say what is claimed?

#### Takeaway
All 8 cited papers exist, and 6 of them broadly support the claim attached to them. Two claims overstate their source. (a) The COLING 2025 Dutch paper says seq2seq models "generally outperform" generative models. It never frames them as "small". (b) "Dual-Pathway Circuits" (2605.13156) is about **object hallucination**, not OCR. It supports the method (activation patching on VLM hallucination pathways) but not any OCR-specific claim. In idea 1, SeqCLR and CCD are real SSL text-recognition papers, but **neither studies invariance erasing diacritics or merged strokes**. They motivate the question without addressing it.

#### Cited Findings
**Idea 1 – Character-preserving SSL**
- arXiv 2012.10873 = "Sequence-to-Sequence Contrastive Learning for Text Recognition" (SeqCLR), Aberdam, Litman, Tsiper, Anschel, Slossberg, Mazor, Manmatha, Perona. VERIFIED. It splits feature maps into sub-word instances for the contrastive loss and proposes "augmentation heuristics". The abstract names no augmentations that hurt. — [arXiv](https://arxiv.org/abs/2012.10873). Published at CVPR 2021 — [CVF](https://openaccess.thecvf.com/content/CVPR2021/html/Aberdam_Sequence-to-Sequence_Contrastive_Learning_for_Text_Recognition_CVPR_2021_paper.html)
- The 2024 SSL-for-TR survey reports that in SeqCLR "aggressive horizontal croppings can lead to misalignment problems between positive and negative pairs". This is an alignment issue, not erasure of character distinctions. — [Survey HTML](https://arxiv.org/html/2407.19889v2)
- arXiv 2211.00288 = "Self-Supervised Character-to-Character Distillation for Text Recognition" (CCD), Guan et al., ICCV 2023. VERIFIED. It segments character regions via a self-supervised segmentation head plus DBSCAN, then distils character-level consistency between a regular view and a geometrically transformed view. It reports gains over DiG. — [arXiv](https://arxiv.org/abs/2211.00288); [CVF ICCV 2023](https://openaccess.thecvf.com/content/ICCV2023/html/Guan_Self-Supervised_Character-to-Character_Distillation_for_Text_Recognition_ICCV_2023_paper.html)
- CCD does **not** mention diacritics or analyse lost fine distinctions. It says only that glyph representations are "relatively invariant to slight structural changes, e.g., thicker or thinner", and it treats that as a benefit. — [arXiv](https://arxiv.org/abs/2211.00288)

**Idea 2 – Selective OCR correction**
- aclanthology 2025.coling-main.690 = "Evaluating Transformers for OCR Post-Correction in Early Modern Dutch Theatre", Debaene, Maladry, Lefever, Hoste. VERIFIED. The authors built a parallel corpus from EmDComF and fine-tuned 5 generative and 4 seq2seq models. "Sequence-to-sequence models generally outperform generative models," with less over- and under-generation, and mBART is best. **"Small" is the friend's framing.** The abstract gives no parameter counts. — [ACL Anthology](https://aclanthology.org/2025.coling-main.690/)
- arXiv 2603.19790 exists, but its **title is "Geometric Risk Control for Vision-Language Model OCR"** (v4, 30 Jul 2026), by Gong, Lu, Chen, Zuo, He, Fan. The friend's title, "From Plausibility to Verifiability: Risk-Controlled Generative OCR", was **not** found on the current landing page and may be an earlier version's title (UNVERIFIED). The paper describes a model-agnostic external controller, the Geometric Risk Controller (GRC). GRC applies geometric transformations as black-box probes and releases a transcription only when cross-view evidence supports a single candidate; otherwise it abstains. It has explicit control over coverage and query cost and reduces catastrophic errors on scene-text benchmarks with frozen VLMs. — [arXiv](https://arxiv.org/abs/2603.19790)
- Directly relevant extra: the ICDAR 2026 HIPE-OCRepair competition on LLM-assisted post-correction (EN/FR/DE, 17th–20th c.; 4 teams) reports that "Over-correction on low-noise inputs emerges as a recurring challenge" and calls for evaluation beyond CER reduction. — [arXiv 2607.08143](https://arxiv.org/abs/2607.08143)
- Other 2025 post-correction work (SNIPPET): "OCR Error Post-Correction with LLMs in Historical Documents: No Free Lunches" — [ACL Anthology](https://aclanthology.org/2025.resourceful-1.8/); "Post-OCR Correction of Historical German Periodicals using LLMs" — [ACL Anthology](https://aclanthology.org/2025.resourceful-1.26/); blog "Can LLMs Correct Historical OCR Without Rewriting History?" — [HF blog](https://huggingface.co/blog/emanuelaboros/can-llms-correct-historical-ocr-without-rewriting)

**Idea 3 – OCR-error budget in RAG**
- arXiv 2412.02592 = "OCR Hinders RAG: Evaluating the Cascading Impact of OCR on Retrieval-Augmented Generation" (OHRBench), Zhang et al. VERIFIED. It has 8,561 document images from 7 domains and 8,498 QA pairs. It defines Semantic Noise vs Formatting Noise, uses controlled perturbation, and finds "none [of current OCR solutions] is competent for constructing high-quality knowledge bases for RAG". — [arXiv](https://arxiv.org/abs/2412.02592)
- arXiv 2605.00911 = "When Good OCR Is Not Enough: Benchmarking OCR Robustness for Retrieval-Augmented Generation", Sun et al., 29 Apr 2026. VERIFIED. It covers 11 hard document types (including historical, watermarked, tables/formulas). Low character error rates do not guarantee RAG quality because structural or semantic errors break retrieval. The gap varies by category and persists across pipeline designs. — [arXiv](https://arxiv.org/abs/2605.00911)

**Idea 4 – OCR confidence fails on rare words / numbers**
- ACL 2026 long 1065 = "PAR: Training-Free Positional Perturbation and Attention Recycling for Faithful OCR", Yao, Liao, Zhang, Li, Zhao. VERIFIED. The claims are accurate. The abstract says models are "effectively 'reciting' the content rather than 'reading' the image" ("Linguistic Priors Hallucination"). It introduces a GlitchText Probing Dataset and finds visual grounding declines with generation length. Positional Perturbation injects phase noise into **RoPE**, and Foveal Attention Recycling redistributes attention back to visual regions. Reported result: about 12% lower CER. — [ACL Anthology](https://aclanthology.org/2026.acl-long.1065/)
- arXiv 2605.13156 = "Dual-Pathway Circuits of Object Hallucination in Vision-Language Models", Liu et al., 13 May 2026. VERIFIED. It uses activation patching across 5 VLMs to find a grounding pathway vs a hallucination pathway. Down-scaling the hallucination pathway cuts object hallucination by up to 76%. The circuit transfers to relational but not attribute hallucination, evaluated on POPE-adversarial and AMBER. **No OCR content.** — [arXiv](https://arxiv.org/abs/2605.13156)

#### Inferences
- The friend's bibliography is real and mostly accurately characterised. Two claims need correcting: drop "small" for the Dutch paper, and present Dual-Pathway as a method template from non-OCR work. The GRC title mismatch needs correcting before anyone cites it.
- For idea 1, the friend cites SeqCLR and CCD as motivation, but neither shows the erasure problem empirically. The empirical case is still to be made, which helps novelty but means the motivation has no direct prior evidence.

#### Gaps
- Could not confirm whether "From Plausibility to Verifiability: Risk-Controlled Generative OCR" was the v1 title of 2603.19790 (version history not fetched).
- Model sizes in the COLING Dutch paper not checked (full PDF not fetched).

### Q2. Closest prior work to the student's #1 ("Learning What to Ignore: Deriving Invariance for SSL Text Recognition")

#### Takeaway
SSL for text recognition is a mature, crowded area (CCD, DiG, MaskOCR, Text-DIAE, masked pretraining at 50M-line scale, and a 2025 IJCV critical survey). Physics-style degradation libraries (Augraphy) and learned augmentation for handwriting also exist. However, **no source found derives the invariance set from a model of the variation, or measures the match between trained invariance and the variation encountered at test time for text.** The survey itself says augmentation choice is ad hoc ("best fit the nature of the data"). The most important new paper is 2609.35473 (Sept 2026). It shows pixel-reconstruction SSL beats contrastive and JEPA for HTR, and that alignment with the high-pixel-variance subspace predicts CER. This **challenges the premise** that invariance-based (augmentation-driven) SSL is the right lever for HTR, so the student must engage with it directly.

#### Cited Findings
**Surveys / standards**
- "Self-Supervised Learning for Text Recognition: A Critical Survey", Penarrubia, Valero-Mas, Calvo-Zaragoza. arXiv July 2024, v2 June 2025, published in IJCV (DOI 10.1007/s11263-025-02487-3). VERIFIED. — [arXiv](https://arxiv.org/abs/2407.19889); [Springer](https://link.springer.com/article/10.1007/s11263-025-02487-3)
- The survey offers no systematic augmentation-selection procedure. It recommends choosing augmentations "that best fit the nature of the data" (citing CMT-Co), and the choices it reports are driven by properties of text such as asymmetry and sequential order. — [Survey HTML](https://arxiv.org/html/2407.19889v2)
- Augmentation findings it collects: Text-DIAE found "the degradation that provides the greatest benefit for TR is masking" (blur/noise help other tasks more). CCD benefits from hard geometric augmentation under distillation. Flip beats rotation for HTR. Mod-ST avoids flips and rotations because they "disrupt the sequential order of characters". ChaCo found positive-pair overlap should not be high. — [Survey HTML](https://arxiv.org/html/2407.19889v2)
- Directions it lists: move to harder benchmarks such as Union14M, standardise dataset protocols, and report training configurations explicitly. It also says some SSL subcategories are unexplored, but Section 6, which details them, was truncated in the fetch. — [Survey HTML](https://arxiv.org/html/2407.19889v2)

**Directly competing / closest papers**
- **"Handwritten Text Recognition Lives in the High-Pixel Variance Subspace"**, Garrido-Munoz & Calvo-Zaragoza, arXiv 2609.35473, 28 Sep 2026. VERIFIED. They compare 6 SSL methods from 3 families (pixel-grounded MIM, JEPA, contrastive) with matched encoder, data and evaluation, on 6 HTR benchmarks in 5 languages. Main findings:
  - Pixel-grounded SSL achieves the lowest CER on every benchmark and both frozen probes, and retains per-position character information.
  - It is the only family that benefits from pretraining on real handwriting, and it is more label-efficient.
  - Encoder alignment with the high-variance pixel subspace predicts CER across methods.
  - A frozen pixel-grounded encoder with an LLM decoder is competitive with fully fine-tuned supervised baselines.
  - Thesis: HTR's discriminative signal lies in high-variance pixel directions. — [arXiv](https://arxiv.org/abs/2609.35473)
- "Masked Self-Supervised Pre-Training for Text Recognition Transformers on Large-Scale Datasets", Kišš & Hradiš, March 2025. VERIFIED. Gradually increases masking probability, uses a loss on both masked and unmasked patches, pretrains on 50M unlabeled lines, and reports up to about 30% relative CER reduction. — [arXiv](https://arxiv.org/abs/2503.22513)
- Text-DIAE, "A Self-Supervised Degradation Invariant Autoencoder for Text" (AAAI 2023). SNIPPET. This is the closest prior work on *degradation invariance* specifically, although its degradations are hand-picked. — [AAAI](https://ojs.aaai.org/index.php/AAAI/article/download/25328/25100)
- "Learning Beyond Labels: Self-Supervised Handwritten Text Recognition" (CVIT/IIIT 2025). SNIPPET. — [PDF](https://cvit.iiit.ac.in/images/ConferencePapers/2025/Learning_Beyond_Labels__Semi_Supervised_Handwritten_Text_Recognition.pdf)
- DiG (ACM MM 2022), MaskOCR, SSM. UNVERIFIED this session. They are known STR SSL baselines, and CCD reports gains over DiG — [arXiv 2211.00288](https://arxiv.org/abs/2211.00288).

**Augmentation for text: hand-designed and learned**
- STRAug, Atienza, ICCV 2021 Workshop. SNIPPET. A library of STR-specific image transformations. — [CVF PDF](https://openaccess.thecvf.com/content/ICCV2021W/ILDAV/papers/Atienza_Data_Augmentation_for_Scene_Text_Recognition_ICCVW_2021_paper.pdf); [GitHub](https://github.com/roatienza/straug)
- "Fine-grained Automatic Augmentation for handwritten character recognition", Pattern Recognition, 2024. SNIPPET. Learned augmentation for handwriting already exists, but for supervised character recognition, not SSL invariance. — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0031320324008306)
- "An Effective Data Augmentation Method by Asking Questions about Scene Text Images" (arXiv 2603.03580, 2026). SNIPPET. — [arXiv](https://arxiv.org/html/2603.03580v1)

**Physics- or parametric degradation synthesis**
- Augraphy, a data-augmentation library for document images (arXiv 2208.14558). SNIPPET. It already ships many document degradations (ink, paper, and scan artefacts), so "physics-style degradation augmentations" are not novel in themselves. — [arXiv](https://arxiv.org/pdf/2208.14558)
- GL-PGENet (arXiv 2505.22021), a parameterized generation framework for document enhancement. SNIPPET. — [arXiv](https://arxiv.org/pdf/2505.22021)
- Bleed-through modelling and removal in medieval manuscripts, J. Imaging 2025. SNIPPET. Diffusion-based restoration of ancient Japanese manuscripts, Heritage Science 2025. SNIPPET. Both show active physical/forward modelling of degradation, but for restoration rather than SSL pretraining. — [MDPI/DOI](https://doi.org/10.3390/jimaging11050136); [Nature Heritage Sci](https://www.nature.com/articles/s40494-025-02214-8)

#### Inferences
- **Crowded:** generic SSL for STR/HTR (contrastive, distillation, MIM), masked pretraining at scale, document augmentation libraries, and LLM post-correction.
- **Still open (no counter-evidence found):** (i) *deriving* the invariance set from a generative or physical model of the nuisance variation instead of hand-picking it; (ii) measuring the match between trained invariance and encountered variation, in the style of Ericsson et al., for text, together with transfer to an unseen script or degradation.
- **Main risk:** 2609.35473 implies that augmentation-invariance objectives (contrastive/JEPA) lose to pixel reconstruction on HTR. The student's framing needs to (a) hold either for MIM, for example by deciding which degradations to apply to the MIM input versus the target, i.e. a "denoising-MIM" invariance, or (b) adopt 2609.35473's high-variance-subspace measure as a diagnostic for when derived invariance helps. That paper also supplies a natural "what governs the match" variable, namely alignment with the discriminative subspace.
- **Feasibility:** small ViT/CNN line recognisers at HTR scale (IAM, READ, and similar benchmarks) are trainable on 8 GB. Kišš & Hradiš's 50M-line pretraining is not reproducible on that budget, but small-scale controlled studies are what 2609.35473 itself does.

#### Gaps
- Ericsson et al. arXiv 2111.11398 ("Why do self-supervised models transfer? Investigating the impact of invariance on downstream tasks") was not fetched. Its title and content are UNVERIFIED. No text-domain replication of it was found.
- DocCreator, and diffusion-based degradation used specifically as SSL augmentation, were not found in searches. Absence is not proof.
- The survey's Section 6 (unexplored SSL categories) was not read because the fetch was truncated at 100k characters.
- No 2025–2026 paper on SSL with augmentations learned automatically for text (as opposed to supervised AutoAugment) was found.

### Q3. Novelty and feasibility of friend's ideas 1, 2, 3 and the "handoff layer" idea (as of Oct 2026)

#### Takeaway
- **Idea 1 (character-preserving SSL): moderately novel but partly pre-empted.** 2609.35473 already shows that per-position character information survives only in pixel-grounded SSL.
- **Idea 2 (selective correction): timely and feasible, but competitive.** HIPE-OCRepair flags over-correction and GRC does abstention for VLM OCR. "Leave rare correct text unchanged" as a calibrated selective-prediction problem is still a plausible angle.
- **Idea 3 (OCR-error budget for RAG): the benchmark space is crowded** (OHRBench, the 2605.00911 benchmark). Budget allocation is an untested twist, but it is a systems/NLP project and far from the student's SSL interest.
- **"Handoff layer": heavily occupied for general VLM conflicts, much less so for OCR specifically.** PAR already does mechanism-informed interventions for OCR "recitation".

#### Cited Findings
- Idea 1: 2609.35473 finds that pixel-grounded SSL "retained per-position character information that the other families recovered only through their readout layers". This is the core claim of character-preserving SSL, in a different framing. — [arXiv](https://arxiv.org/abs/2609.35473). Neither SeqCLR nor CCD studies diacritic erasure — [2012.10873](https://arxiv.org/abs/2012.10873), [2211.00288](https://arxiv.org/abs/2211.00288)
- Idea 2: HIPE-OCRepair 2026 names over-correction on low-noise inputs as a recurring challenge — [arXiv 2607.08143](https://arxiv.org/abs/2607.08143). GRC does risk-controlled abstention for VLM OCR — [arXiv 2603.19790](https://arxiv.org/abs/2603.19790). Seq2seq models beat generative models on Early Modern Dutch, with less overgeneration — [ACL](https://aclanthology.org/2025.coling-main.690/)
- Idea 3: OHRBench separates semantic from formatting noise — [arXiv 2412.02592](https://arxiv.org/abs/2412.02592). 2605.00911 shows CER does not predict RAG quality across 11 document types — [arXiv](https://arxiv.org/abs/2605.00911)
- Handoff layer, closest work:
  - "Arbitration Failure, Not Perceptual Blindness" (2604.09364, Apr 2026) tests 10 VLMs. Visual attributes are linearly decodable early (AUC > 0.86), the final-layer logit gap predicts grounding (ρ = 0.847), and the study uses a layer-wise logit lens with its MAC crossover analysis, activation patching and steering. Its conflict examples are not OCR. — [arXiv](https://arxiv.org/abs/2604.09364)
  - "Vision-Default, Prior-Override" (2606.28273, Jun 2026) finds that answering from priors depends on 2.5–4.8% of attention heads in the second half of the network. Ablating them flips 68–96% of prior answers to grounded ones. Method: activation patching. Not OCR. — [arXiv](https://arxiv.org/abs/2606.28273)
  - "Using OCR Heads to Verbalize Image Semantics" (Feucht, …, Bau; arXiv 2609.18823, 2026, under review) finds that OCR heads make up about 10% of attention heads across 4 VLMs (e.g., Qwen3-VL-8B), identified via a per-head logit lens and knockout. — [Project page](https://ocr.baulab.info/)
  - PAR (ACL 2026) covers the inference-time fix for OCR recitation — [ACL](https://aclanthology.org/2026.acl-long.1065/)
  - Also SNIPPET: "Same Attention, Different Truths: Put Logit-Lens over Visual Attention…" (CVPR 2026) — [CVF](https://openaccess.thecvf.com/content/CVPR2026/papers/Wang_Same_Attention_Different_Truths_Put_Logit-Lens_over_Visual_Attention_to_CVPR_2026_paper.pdf); "Diagnosing Visual Ignorance in VLMs" (2606.06890) — [arXiv](https://arxiv.org/html/2606.06890v1)

#### Inferences
- **Handoff layer for OCR:** the general mechanism (sparse prior-writing heads late in the network; failure at arbitration, not encoding) is already published. An OCR-specific version would combine 2604.09364/2606.28273-style analysis with PAR's GlitchText-style probes. That gives an incremental but feasible project on an 8 GB GPU with 2–3B VLMs (e.g., Qwen2-VL-2B; UNVERIFIED that it fits with patching overhead). Novelty would have to come from text-specific findings: rare words, numbers, diacritics, historical spellings.
- **Idea 2** fits the student's interests best among the friend's ideas, because it reuses the "what to leave unchanged" theme. A clean framing would be selective prediction/conformal abstention for post-correction, measured on rare-but-correct tokens (historical spellings, proper names). GRC and HIPE are the baselines to beat or differentiate from.
- **Idea 1** could be folded into the student's #1 as the evaluation axis. The question becomes which derived invariances destroy diacritic or stroke distinctions, measured with probes, building on 2609.35473's per-position analysis.
- **Idea 3** has low overlap with the student's SSL focus and sits in a space already holding two benchmarks.

#### Gaps
- No exhaustive search was done for 2026 papers on "selective/conservative post-OCR correction" beyond HIPE and GRC. A dedicated paper may exist.
- Not verified whether any 2026 paper already applies a layer-wise logit lens specifically to OCR transcription errors in VLMs. Searches surfaced only general-conflict papers plus OCR heads.
- Feasibility claims about 8 GB VRAM for VLM patching are inference, not sourced.

## Notes: Vision SSL ideas reality check / pipeline_and_datasets.md

## Pipeline and Datasets: "Learning What to Ignore" (derived invariances for SSL text recognition)

Scope note: about 19 tool calls. A zenodo.org fetch (CATMuS Medieval record) was refused by the proxy with HTTP 429, so CATMuS details below come only from search-result metadata. Items marked **[UNVERIFIED]** are from background knowledge and were not confirmed in this session. Check them before relying on them.

### Datasets by role (access, license, size, URL)

#### Takeaway
A beginner can get every role covered with freely downloadable data: Teklia's HF mirrors for IAM/RIMES-style clean lines, HTR-United plus CATMuS for degraded historical lines with transcriptions, CVIT/IIIT for Indic, Muharaf for historical Arabic, Augraphy/DIBCO for degradation, and PARSeq's LMDB bundle or Union14M for scene text. The main friction is licence and registration (IAM's original site, Union14M terms, Muharaf's 428 restricted pages) and the fact that many Indic sets are word-level rather than line-level.

#### Cited Findings
**(a) Clean labelled line-level handwriting/print**
- IAM lines on Hugging Face (Teklia/IAM-line): MIT licence as stated on the card. Splits: train 6.48k, validation 976, test 2.92k (about 10.4k lines). Stored as Parquet with JPEG images. No gating shown. Line image height is not stated on the card. — [HF Teklia/IAM-line](https://huggingface.co/datasets/Teklia/IAM-line)
  - Caveat: the original IAM database (fki.tic.heia-fr.ch) requires registration and is non-commercial. The MIT tag on the HF mirror may not reflect upstream terms, so cite the original IAM terms. **[UNVERIFIED re upstream terms]**
- Teklia also hosts other line-level HF mirrors (e.g., RIMES-2011-line, NorHand). The IAM card did not list them. **[UNVERIFIED; check https://huggingface.co/Teklia]**
- Bentham (ICFHR 2014), Washington, Saint Gall, Parzival (FKI/Uni Fribourg), READ 2016 and CVL are standard but were not verified this session. **[UNVERIFIED access details]**. The Bentham collection is used as the "historical handwritten" target in the closest prior SSL-for-HTR work (Kišš & Hradiš 2024). — [arXiv 2405.00420](https://arxiv.org/abs/2405.00420)

**(b) Genuinely degraded historical documents with transcriptions**
- HTR-United is "an ecosystem for sharing and finding ground truth for OCR/HTR." — [htr-united.github.io](https://htr-united.github.io/)
  - Each dataset is described by a YAML file with fields `language`, `script`, `script-type`, `time`, `hands`, `license`, `format`, `volume` and `transcription-guidelines`. The repo exposes `catalog.json` and `statistics.csv`. The repo itself is CC0-1.0; each dataset has its own licence (the example is CC-BY 4.0). A browsable catalogue is at htr-united.github.io/catalog.html, and the `htruc` tool does quality checks. — [GitHub HTR-United/htr-united](https://github.com/HTR-United/htr-united)
  - Practical use: download `catalog.json`, filter by `script` (e.g., `Latn`, `Arab`, `Hebr`) and `time`, then pull the datasets (mostly ALTO/PAGE XML plus images on GitHub or Zenodo).
- CATMuS Medieval: a large multilingual medieval manuscript HTR dataset, on Zenodo (latest record) and Hugging Face (`CATMuS/medieval`; a separate `CATMuS/medieval-segmentation` set exists for layout). Line counts and licence could not be fetched (429). From background knowledge it has about 160k+ lines, 10+ languages, 8th–16th c., CC-BY. **[UNVERIFIED numbers]** — [Zenodo CATMuS Medieval](https://zenodo.org/records/15030337/latest); [HF CATMuS/medieval-segmentation](https://huggingface.co/datasets/CATMuS/medieval-segmentation/tree/main/data); [BnF presentation PDF](https://afia.asso.fr/wp-content/uploads/2024/05/PINCHE_CATMuS_Medieval_3_05_2024_BnF.pdf)
- Esposalles, HKR, NorHand (Norwegian), Old Bailey and IMPACT were not verified this session. **[UNVERIFIED]**. A PyLaia NorHand recipe exists on GitHub. — [flaviodeoliveira/pylaia-norhand-htr](https://github.com/flaviodeoliveira/pylaia-norhand-htr); [Teklia Hugin-Munin project](https://teklia.com/research/projects/huginmunin/hugin-munin-project)

**(c) Low-resource / non-Latin scripts**
- IIIT-INDIC-HW-WORDS: 8 scripts (Bengali, Gujarati, Gurmukhi, Kannada, Odia, Malayalam, Tamil, Urdu), plus earlier Devanagari (IIIT-HW-Dev) and Telugu sets for 10 scripts in total. It has 872K handwritten word instances from 135 writers. It is **word-level, not line-level**. Each language is a direct-download zip with images, labels and vocabulary. The page mentions no registration and states no licence (contact the author). — [CVIT IIIT-INDIC-HW-WORDS](https://cvit.iiit.ac.in/research/projects/cvit-projects/iiit-indic-hw-words); [Indic HW data page](https://cvit.iiit.ac.in/research/projects/cvit-projects/indic-hw-data); also mirrored on India's AIKosh portal — [AIKosh](https://aikosh.indiaai.gov.in/home/datasets/details/iiit_indic_hw_words_11.html)
- PLATTER (2025) is a page-level Indic HTR system, a possible source of pointers to line- and page-level Indic data. — [arXiv 2502.06172](https://arxiv.org/pdf/2502.06172)
- DohaScript (2026) is a large-scale multi-writer dataset of continuous handwritten Hindi text. Access was not checked. — [HF papers 2602.18089](https://huggingface.co/papers/2602.18089.md)
- Muharaf (NeurIPS 2024 Datasets & Benchmarks): historical handwritten Arabic, 1,644 pages, **36,311 text lines** and 4,867 regions, early 19th to early 21st c. **1,216 images are public. 428 are proprietary and need the owner's permission.** The public licence and download URL sit in an appendix that was not captured. — [arXiv 2406.09630v2](https://arxiv.org/html/2406.09630v2); [NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2024/hash/6b8cb6b291045e217c3ff3f854f2fd0f-Abstract-Datasets_and_Benchmarks_Track.html)
- KHATT, BanglaWriting, Ge'ez/Amharic, Syriac, OCS, Pashto, Tibetan, AMADI_LontarSet and SleukRith were not verified this session. **[UNVERIFIED]**. HTR-United's `script` field is the fastest way to find Hebrew, Arabic, Greek and Cyrillic line-level sets with explicit licences. — [HTR-United repo](https://github.com/HTR-United/htr-united)

**(d) Degradation simulation / pairs**
- Augraphy 8.2.6 (latest on PyPI, released 31 Dec 2023), MIT licence, Python ≥3.8. Its augmentations include **InkBleed, BleedThrough**, BadPhotoCopy, BookBinding, Brightness, ColorPaper, DirtyDrum, DirtyRollers, Dithering, Faxify, Folding, Gamma, InkMottling, InkShifter, Jpeg, Letterpress, LightingGradient, LowInkPeriodicLines/RandomLines, LowLightNoise, NoiseTexturize, ShadowCast, SubtleNoise, WaterMark and others. The benchmark table also lists DepthSimulatedBlur, DirtyScreen and Stains. There is no explicit "fading" or "foxing" augmentation; approximate them with Brightness, LowInk* and ColorPaper or Stains. — [PyPI augraphy](https://pypi.org/project/augraphy/); [GitHub sparkfish/augraphy](https://github.com/sparkfish/augraphy/blob/dev/index.rst); [Augraphy paper arXiv 2208.14558](https://arxiv.org/abs/2208.14558v2)
- Maintenance flag: no PyPI release since Dec 2023, so treat Augraphy as stable but possibly unmaintained, and pin NumPy/OpenCV versions. — [PyPI augraphy](https://pypi.org/project/augraphy/)
- DIBCO/H-DIBCO, NoisyOffice, ocrodeg and DocCreator were not verified this session. **[UNVERIFIED]**

**(e) Scene text for "capture condition" transfer**
- The PARSeq repo links ready-made LMDB archives for MJSynth, SynthText, IIIT5k, SVT, SVTP, IC13, IC15, CUTE80, ArT, RCTW17, ReCTS, LSVT, MLT19, COCO-Text, Uber-Text, TextOCR and OpenVINO. This is the easiest beginner download. — [GitHub baudm/parseq](https://github.com/baudm/parseq)
- Union14M ("Revisiting Scene Text Recognition: A Data Perspective", ICCV 2023) has about 4M labelled and 10M unlabelled real images. The unlabelled split (Union14M-U) doubles as an SSL pool. The download is on the Mountchicken/Union14M GitHub. **[UNVERIFIED repo/terms]** — [arXiv 2307.08723](https://arxiv.org/pdf/2307.08723)

**(f) Unlabelled pools for SSL pretraining**
- CCD (ICCV 2023) follows DiG's data layout: Synth (MJ, ST), URD (unlabelled real data, from OCR-CC) and ARD (annotated real data). Data instructions point to the DiG repo. — [GitHub TongkunGuan/CCD](https://github.com/TongkunGuan/CCD)
- For documents, the cheapest pool is the labelled datasets above with labels thrown away (e.g., CATMuS and HTR-United lines). This mirrors Kišš & Hradiš 2024, who pretrain on target-domain historical lines (Bentham, plus a historical printed collection). — [arXiv 2405.00420](https://arxiv.org/abs/2405.00420)

#### Inferences
- Line-level handwriting for Indic scripts is scarce in freely licensed form. The word-level IIIT sets are usable for an "unseen script" probe if the recognizer works on word crops, and word crops are fine for a CTC model.
- HTR-United's `catalog.json` effectively turns the question "which degraded historical datasets exist" into a filter script. It is the single most useful resource for role (b) and partly (c).

#### Gaps
- Exact line counts and licence for CATMuS Medieval (Zenodo fetch refused).
- Muharaf public licence and download URL.
- Current availability and licences of KHATT, Bentham ICFHR2014, READ2016, Esposalles, HKR, DIBCO, SleukRith, AMADI_LontarSet and Union14M were not confirmed this session.

### Recommended starter datasets and held-out "unseen condition" split

#### Takeaway
Start with (1) IAM lines from HF (clean modern handwriting, MIT-tagged mirror, about 10k lines), (2) one degraded historical Latin-script set from CATMuS or HTR-United (real degradation), and (3) one cross-domain probe: a scene-text LMDB set from the PARSeq bundle for capture condition, or an IIIT Indic word set or the public part of Muharaf for unseen script. Hold out whole degradation families, media and scripts, not random lines.

#### Cited Findings
- IAM-line HF has fixed train/val/test splits (6.48k/976/2.92k) and downloads without gating. — [HF Teklia/IAM-line](https://huggingface.co/datasets/Teklia/IAM-line)
- Augraphy separates degradation types into individual classes (InkBleed, BleedThrough, LowInk*, Jpeg, ShadowCast, Folding, etc.), so whole families can be held out. — [PyPI augraphy](https://pypi.org/project/augraphy/)
- Kišš & Hradiš found target-domain SSL pretraining "very effective" but **not consistently better than transfer from closely related domains**, so a supervised related-domain baseline is mandatory. — [arXiv 2405.00420](https://arxiv.org/abs/2405.00420)

#### Inferences (proposed split design)
- **Pretraining pool:** unlabelled IAM-train plus unlabelled lines from a historical set (e.g., a CATMuS subset of 20–50k lines).
- **Invariance set A (derived from physics):** Augraphy InkBleed, BleedThrough, LowInk (fading), NoiseTexturize, blur, and Jpeg/ShadowCast as "capture". Parameter ranges are fitted to statistics measured on real historical lines (e.g., contrast histogram, stroke-width distribution, background texture power spectrum).
- **Invariance set B:** the standard hand-tuned text SSL augmentations (as in SeqCLR/CCD).
- **Held-out conditions, never seen in pretraining augmentations:**
  1. Degradation type: hold out one Augraphy family (e.g., BleedThrough) and evaluate on IAM-test with that family applied synthetically, *and* on real degraded lines.
  2. Medium: pretrain on handwriting only, then test print (historical printed lines from HTR-United) and scene text (IC13/IC15/IIIT5k LMDBs from PARSeq).
  3. Script: test on an Indic word set (e.g., IIIT Bengali) or public Muharaf lines with a new charset head.
  4. Capture: scanner (IAM) versus camera (scene text, or phone photos of IAM-style pages if available).
- **Label fractions:** 1%, 10% and 100% of IAM-train, i.e. about 65, 650 and 6.5k lines. Use three seeds at 1%, because variance there is high.

#### Gaps
- No public benchmark was found that pairs the same handwritten lines under scanner versus camera capture. This was not searched exhaustively.

### Code: SSL, HTR, degradation, SSL libraries (maintenance, fits 8 GB?)

#### Takeaway
The most beginner-relevant codebase is DCGM's **pero-pretraining**, the only one found that targets SSL on historical *document* lines. PARSeq (Apache-2.0, torch.hub weights) is the cleanest STR/HTR training framework. CCD has weights but assumes several RTX 3090s for pretraining and is academic-only. PyLaia (Teklia) is a maintained CRNN-CTC HTR baseline. Augraphy covers degradation.

#### Cited Findings
- **pero-pretraining (Kišš & Hradiš 2024):** includes masked-label-prediction variants (Feature Quantization, VQ-VAE, Post-Quantized AE) and joint-embedding variants (VICReg, NT-Xent). It also introduces "image shifting" to stop joint-embedding models collapsing onto positional encoding. Data: historical handwritten (Bentham) and printed lines. — [arXiv 2405.00420](https://arxiv.org/abs/2405.00420); code [github.com/DCGM/pero-pretraining](https://github.com/DCGM/pero-pretraining)
- **CCD (ICCV 2023):** ViT-Small and ViT-Base, with pretrained and fine-tuned weights on Google Drive. Tested on "3090 Ubuntu 16.04 Cuda 11". The README recommends "multiple 3090s" for pretraining, and its examples use 4 GPUs for pretraining, 2 for fine-tuning and 1 for testing. 2-clause BSD licence, but "only free for academic research purposes". Data layout is borrowed from DiG. — [GitHub TongkunGuan/CCD](https://github.com/TongkunGuan/CCD); [ICCV paper](https://openaccess.thecvf.com/content/ICCV2023/html/Guan_Self-Supervised_Character-to-Character_Distillation_for_Text_Recognition_ICCV_2023_paper.html)
- **DiG** ("Reading and Writing: Discriminative and Generative Modeling for SSL Text Recognition", ACM MM 2022) combines contrastive learning and masked image modelling. Code is at github.com/ayumiymk/DiG, referenced by the CCD README. — [arXiv 2207.00193](https://arxiv.org/pdf/2207.00193); [CCD README](https://github.com/TongkunGuan/CCD)
- Related STR SSL papers found: Symmetric Superimposition Modeling (2024) and Relational Contrastive Learning / RCL+MIM (2023/2024). — [arXiv 2405.05841](https://arxiv.org/pdf/2405.05841); [arXiv 2308.00508](https://arxiv.org/pdf/2308.00508); [arXiv 2411.11219](https://arxiv.org/pdf/2411.11219)
- **Critical survey (IJCV 2025):** SSL-for-text-recognition methods were often "developed independently," without comparison to prior results. The survey highlights inconsistencies and proposes standardisations, so it is required reading for experimental protocol. — [arXiv 2407.19889](https://arxiv.org/abs/2407.19889) (DOI 10.1007/s11263-025-02487-3)
- **PARSeq:** Apache-2.0. Last dated news is 2024-02-22 ("Updated for PyTorch 2.0 and Lightning 2.0"), with 49 open issues. The default model has 23.8M params (21.4M encoder). Models load with `torch.hub.load('baudm/parseq', 'parseq', pretrained=True)` (also `parseq_tiny`, `crnn`, `trba`, `vitstr`, `abinet`). Size is configurable via `model.img_size=[32,128]`. Python ≥3.9, PyTorch ≥2.0. An example batch size is 384. — [GitHub baudm/parseq](https://github.com/baudm/parseq)
- **PyLaia (Teklia):** documented at doc.teklia.com/pylaia and on PyPI, with a 2024 paper on adding n-gram language models to PyLaia. — [PyLaia docs](https://doc.teklia.com/pylaia/); [PyPI pylaia](https://pypi.org/project/pylaia/); [arXiv 2404.18722](https://arxiv.org/html/2404.18722v1)
- **Augraphy:** MIT, last release Dec 2023 (see above). — [PyPI](https://pypi.org/project/augraphy/)
- kraken, HTR-Flor, TrOCR fine-tuning, SeqCLR reimplementations, ocrodeg, DocCreator, lightly and solo-learn were not checked this session. **[UNVERIFIED maintenance status]**. From background knowledge, kraken (mittagessen/kraken) and lightly are actively maintained, and solo-learn is research code (CIFAR/ImageNet-oriented, needs adaptation to sequences). TrOCR-base (334M) is tight but feasible on 8 GB with fp16 and a small batch. **[UNVERIFIED]**

#### Inferences
- Do **not** start from CCD/DiG pretraining code on 8 GB. Their ViT-B and multi-3090 setups are built for millions of scene-text crops. Reuse their ideas, or fine-tune from their released weights.
- Recommended stack: a PARSeq-tiny or small CRNN/ResNet-BiLSTM-CTC backbone, a SimCLR/SeqCLR-style or VICReg sequence-level objective (pero-pretraining has VICReg/NT-Xent with the image-shifting fix), Augraphy in the data loader, and CER from `jiwer` or `torchmetrics`.
- Lightly provides the loss functions (NT-Xent, VICReg, BYOL) as drop-in modules. You only need the losses; frame-level pooling is custom.

#### Gaps
- Exact last-commit dates for CCD, pero-pretraining, PyLaia and kraken.
- Peak VRAM figures for any of these repos on 8 GB. None of the READMEs fetched state GPU memory.

### Step-by-step minimal pilot (2–4 weeks) and rough runtimes

#### Takeaway
The pilot is feasible on an RTX 4060 8 GB plus Kaggle with a small model (about 5–25M params) at line height 32–64 px. Pretraining runs of a few hours on about 10–50k lines are enough to compare a derived invariance set with a hand-tuned one at 1%, 10% and 100% labels. All runtimes below are inferred estimates, not measurements from sources.

#### Cited Findings
- Ericsson, Gouk & Hospedales (BMVC 2022) give the **invariance measures** (Appendix C.1):
  - Mahalanobis distance: l = ‖G f(x) − G f(t_φ(x))‖₂, where Σ⁻¹ = GGᵀ (Cholesky of the feature covariance). Lower means more invariant.
  - Whitened cosine: z = G(f̄ − f(x)), z_t = G(f̄ − f(t_φ(x))), l = cos(z, z_t). Closer to 1 means more invariant.
  - Both are averaged over images x ∈ D and transformation parameters φ ∈ Φ.
  - Findings: contrastive models learn the augmentation invariances, which transfer to related real changes. Different downstream tasks benefit from "polar opposite (in)variances". Fusing complementary-invariance features gives broad transfer.
  - [arXiv 2111.11398 (PDF v2)](https://arxiv.org/pdf/2111.11398v2); [BMVC 2022](https://bmvc2022.mpi-inf.mpg.de/509)
- Joint-embedding SSL on text lines can collapse onto positional encoding. Use image shifting (random horizontal offsets between views) to prevent it. — [arXiv 2405.00420](https://arxiv.org/abs/2405.00420)

#### Inferences (pilot plan; runtimes are my estimates)
1. **Week 1, data and baseline.**
   - Load IAM-line from HF. Resize to height 64, keep aspect ratio, pad width to about 1024 (or height 32 for a CRNN).
   - Build the charset from the training labels.
   - Train a supervised CRNN-CTC or PARSeq-tiny at 1%, 10% and 100%. Expect roughly 1–3 h for 100% IAM on the 4060 with AMP, batch about 32–64 at h=64.
   - Report CER and WER with `jiwer`.
2. **Week 1–2, degradation module.**
   - Wrap Augraphy classes as `T_derived`, parametrised by distributions fitted to real degraded lines: measure ink/background intensity, contrast, blur (variance of Laplacian) and noise σ on CATMuS/HTR-United lines, and set augmentation ranges to match those quantiles.
   - Define `T_hand`: SeqCLR-style crop, affine, colour jitter and blur.
   - Hold out one family (e.g., BleedThrough).
   - Pre-render augmented views offline if CPU is the bottleneck. Augraphy is CPU-heavy.
3. **Week 2–3, SSL pretraining.**
   - Use SeqCLR-style frame/window-level NT-Xent or VICReg (pero-pretraining code), with a ResNet-ish CNN (about 5–10M params) or ViT-tiny encoder.
   - Settings: height 64, batch 64–128 with AMP, 20–50k unlabelled lines, 50–100 epochs. That is about 4–12 GPU-hours per run, so offload runs to Kaggle T4s (30 h/week covers about 3–5 runs).
   - Runs: `T_hand`, `T_derived`, `T_derived` minus the held-out family, and no-SSL.
4. **Week 3, fine-tuning.** Attach a CTC head (or PARSeq decoder) and fine-tune at 1%, 10% and 100%. Run 3 seeds at 1%. Each run takes minutes to about 1 h.
5. **Week 3–4, evaluation.**
   - CER on IAM-test (clean), on IAM-test with the held-out degradation, on real degraded historical lines (with a new charset if needed), and on scene-text LMDBs (IC13/IIIT5k) as a capture shift.
   - Optionally test an unseen script: fine-tune on an IIIT Indic word set with a new charset head.
6. **Invariance measurement.**
   - Mean-pool encoder features per line.
   - Compute Ericsson's Mahalanobis and whitened-cosine scores per transformation family (including held-out ones) on about 1–2k lines.
   - Correlate per-family invariance with the CER drop under that family. This is the "trained invariance vs encountered variation" analysis.
   - It takes minutes on GPU. A covariance of dim 256–512 is trivial to invert, but regularise Σ with a small ridge.

#### Gaps
- No source gave measured runtimes or VRAM figures for SSL text-line pretraining on 8 GB consumer GPUs. All numbers above are estimates.

### Likely pitfalls

#### Takeaway
Most failures will come from data plumbing (charsets, normalization, splits, licences) and from evaluation inconsistency, not from the SSL method. Line-level datasets avoid segmentation entirely, so avoid page-level data in the pilot.

#### Cited Findings
- SSL-for-text-recognition papers often lack comparable protocols and contain inconsistencies, so state image size, charset, case sensitivity and test sets explicitly. — [arXiv 2407.19889](https://arxiv.org/abs/2407.19889)
- Joint-embedding collapse onto positional encoding is a known failure. — [arXiv 2405.00420](https://arxiv.org/abs/2405.00420)
- SSL may fail to beat simple transfer from a related labelled domain. Always include that baseline. — [arXiv 2405.00420](https://arxiv.org/abs/2405.00420)
- Datasets differ in transcription conventions. HTR-United records `transcription-guidelines` per dataset (e.g., abbreviations and diplomatic versus normalised transcriptions in medieval sets). — [HTR-United repo](https://github.com/HTR-United/htr-united)
- Indic IIIT data is word-level, so it is not directly comparable with line-level CER. — [CVIT](https://cvit.iiit.ac.in/research/projects/cvit-projects/iiit-indic-hw-words)
- Muharaf has mixed licensing: only 1,216 of 1,644 pages are public. — [arXiv 2406.09630](https://arxiv.org/html/2406.09630v2)
- CCD's code is academic-only and its weights were trained on scene text (ARD/STD), which mismatches handwriting. — [GitHub CCD](https://github.com/TongkunGuan/CCD)

#### Inferences
- **Charset:** a new script needs a new output head. Apply Unicode NFC/NFD normalization consistently, because combining marks in Indic and Arabic inflate CER if it is inconsistent. Report CER on grapheme clusters as well as code points for Indic.
- **RTL scripts:** Arabic labels must be in logical order, and CTC needs no reordering, but check that visualisations do not flip the order.
- **Label noise:** historical ground truth often expands or keeps abbreviations inconsistently. Normalise, or report CER both ways.
- **Leakage:** IAM writers overlap across non-standard splits. Use the official writer-independent split, and never pretrain on test lines, not even unlabelled ones.
- **Augraphy speed:** CPU-bound augmentation can starve the GPU, so pre-render or use multiple workers. Some effects (BleedThrough, BookBinding) assume page-sized images and may misbehave on 64-px lines. Apply them to page crops before line extraction, or tune their parameters.
- **"Derived" vs hand-tuned confound:** the derived set must not be secretly tuned on test conditions. Fit its statistics only on pretraining-pool data.

#### Gaps
- No source quantified the size of the CER changes caused by Unicode normalization or abbreviation conventions.

## Notes: Vision SSL ideas reality check / ssl_ideas_novelty.md

## Novelty fact-check: SSL vision research ideas (memo of Aug 2026, friend's critique of 11 Oct 2026), as of 12 Oct 2026

Scope note: I fetched arXiv abstract pages and one CVF PDF directly. I did not read most full papers, so claims about a paper's body are marked. OpenReview pages were blocked by a bot check.

### Q1. Friend's claims: do the cited papers exist and say what is claimed?

#### Takeaway
All of the friend's factual claims hold up. Joshi & Mirzasoleiman (ICML 2023) is real, selects examples by expected augmentation similarity, claims guarantees, and uses the same three datasets that idea 01 names. The Registers paper does say that artifact tokens sit in low-information background regions and are "repurposed for internal computations". The "not a group" point is mathematically correct. The H-from-segmentation point is a valid gap: the theorem needs a known positive-definite H, and Beyond Isotropy evaluates only classification.

#### Cited Findings
- **Joshi et al. exists.** Title: "Data-Efficient Contrastive Self-supervised Learning: Most Beneficial Examples for Supervised Learning Contribute the Least". Authors: Siddharth Joshi, Baharan Mirzasoleiman. Venue: ICML 2023 (PMLR v202). — [PMLR](https://proceedings.mlr.press/v202/joshi23b.html); [ICML poster](https://icml.cc/virtual/2023/poster/23865); [arXiv 2302.09195](https://arxiv.org/abs/2302.09195v1)
- Joshi et al. say the examples that help contrastive SSL most are those whose augmentations are, in expectation, most similar to the augmentations of other examples. They claim "rigorous guarantees" on the generalization of contrastive learning trained on these subsets. I did not read the form of the guarantees. — [PMLR](https://proceedings.mlr.press/v202/joshi23b.html)
- **Joshi et al. reports results on idea 01's exact datasets.** About 20% of CIFAR-100 and about 40% of STL-10 and Tiny-ImageNet can be removed without hurting downstream performance. Their subsets beat random subsets by more than 3%. They also claim to be the first work to quantify an example's value for SSL. — [PMLR](https://proceedings.mlr.press/v202/joshi23b.html)
- **Registers paper (arXiv 2309.16588).** The abstract says the high-norm artifact tokens appear "primarily in low-informative background areas of images" and are "repurposed for internal computations". The abstract does not itself say these tokens hold *global* information. — [arXiv 2309.16588](https://arxiv.org/abs/2309.16588)
- **Lappe & Giese, arXiv 2505.05892 (v2, Oct 2025)** make the global-information claim explicitly. Registers give the model a place to store global information. In large ViTs, "global information is dominated by information extracted from register tokens", which decouples local and global features. [CLS] has a similar effect in models without registers. An OpenReview forum exists, but I could not see the venue or decision because of a bot check. — [arXiv 2505.05892](https://arxiv.org/abs/2505.05892); [OpenReview](https://openreview.net/forum?id=KhavyzO9kK)
- **Jiang, Dravid, Efros, Gandelsman (arXiv 2506.08010, v5 Oct 2025).** A small set of neurons in CLIP and DINOv2 concentrates high-norm activations on outlier tokens. Moving those activations into an extra untrained token, with no training, works about as well as trained registers. — [arXiv 2506.08010](https://arxiv.org/abs/2506.08010)
- **Group-theoretic augmentation framework.** Chen, Dobriban & Lee (JMLR v21, 2020; NeurIPS 2020 oral) treat augmentation as averaging over the orbits of a *group* that keeps the data distribution *approximately* invariant. The abstract does not cover non-invertible transforms or semigroups. — [arXiv 1907.10905](https://arxiv.org/abs/1907.10905); [JMLR](https://jmlr.org/papers/v21/20-163.html); [NeurIPS 2020](https://neurips.cc/virtual/2020/oral/16993)
- **The non-group formalism already used in SSL theory is the augmentation graph.** HaoChen, Wei, Gaidon & Ma (2021): edges connect augmentations of the same input, ground-truth classes form connected subgraphs, and spectral contrastive loss gives provable linear-probe guarantees. — [arXiv 2106.04156](https://arxiv.org/abs/2106.04156)
- **Beyond Isotropy (arXiv 2605.20107, R. Jenkinson Alvarez, 19 May 2026).** The abstract states that the minimax / maximum-entropy covariance under a Hamiltonian energy budget is (c/d)·H⁻¹ *for a known downstream geometry*. When the geometry is unknown, no fixed covariance target is canonical. The paper proposes HamJEPA, a symplectic leapfrog predictor, and evaluates only kNN and linear probing on CIFAR-100 and ImageNet-100. It has no dense tasks. — [arXiv 2605.20107](https://arxiv.org/abs/2605.20107)

#### Inferences
- **Groups (my own math check).** Random-resized-crop, occlusion/cutout and ink loss are many-to-one maps, so they have no inverses. Crops compose (a crop of a crop is roughly a crop) and include the identity, so they form at best a monoid or semigroup, not a group. Hence "orbits" are not automatically equivalence classes: "x reaches y" is reflexive and transitive but not symmetric. Flips, 90° rotations, colour-channel permutations and invertible colour transforms can form groups. Many jitter operations do not, because of clipping.
- **Repair for idea 01.** Define the classes as connected components of the symmetrised augmentation graph, following HaoChen et al. The risk is that under strong crop and colour augmentation this graph may percolate into one giant component, which would make "number of equivalence classes" trivial. A soft quantity (spectral or effective-rank) is needed instead. This is my inference; I did not test it.
- **The friend's H point is correct in substance.** Segmentation masks give labels, not a covariance or Hessian. A positive-definite H would have to be built, for example as the Hessian or Fisher of a dense linear-probe loss with respect to features plus ridge regularisation. Such an H is probe- and task-dependent, PSD rather than PD without regularisation, and patch-level, not image-level. This is an inference, not from a source.

#### Gaps
- I did not read the theorem statements in Joshi et al. or Beyond Isotropy (full PDFs not fetched), so the exact assumptions (for example whether H must be positive definite) are unverified.
- I found no paper on "semigroup augmentation" specifically for SSL (one query). Absence is not proof.

### Q2. Idea 01: effective size of an unlabelled dataset = number of augmentation equivalence classes

#### Takeaway
The memo's "LOW novelty risk" is **not defensible**. Revised risk: **HIGH** for the pruning and prediction part, **MEDIUM** for the theory framing. Joshi et al. (ICML 2023) already does augmentation-similarity-based data pruning for contrastive SSL, with guarantees, on CIFAR-100, STL-10 and Tiny-ImageNet. HaoChen et al. already formalise data through augmentation-induced graph structure. 2025 work adds augmentation-aware bounds.

#### Cited Findings
- Joshi et al. prune 20–40% of CIFAR-100, STL-10 and Tiny-ImageNet by expected augmentation similarity, with guarantees. These are exactly idea 01's benchmark datasets. — [PMLR](https://proceedings.mlr.press/v202/joshi23b.html)
- The augmentation-graph formalism (HaoChen et al. 2021) links the connectivity of augmentations to downstream linear-probe accuracy. — [arXiv 2106.04156](https://arxiv.org/abs/2106.04156)
- Cui, Wen & Wang (arXiv 2505.22196, May 2025) give an augmentation-aware error bound for contrastive SSL: supervised risk ≤ unsupervised risk plus an explicit augmentation-induced trade-off term. They analyse specific augmentation types. The abstract does not say whether this is a sample-complexity result. — [arXiv 2505.22196](https://arxiv.org/abs/2505.22196)
- Other adjacent work showed up in search but I did not verify it:
  - "You Don't Need Data Augmentation in Self-Supervised Learning" — [arXiv 2406.09294](https://arxiv.org/html/2406.09294v1)
  - "A Theoretical Characterization of Optimal Data Augmentations" — [arXiv 2411.01767](https://arxiv.org/pdf/2411.01767)
  - SSL dataset distillation — [arXiv 2410.02116](https://arxiv.org/pdf/2410.02116)

#### Inferences
- What may still be open is a *training-free, pre-training predictor* of prunability that compares contrastive vs MAE vs JEPA. Joshi et al. is contrastive-only, and its abstract mentions no MAE or JEPA. This angle must be framed as an extension of Joshi et al., not as a first.
- The "stronger augmentation reduces effective data" claim must be stated in non-group terms (see Q1).
- A cross-objective (contrastive / MAE / JEPA) prunability comparison on CIFAR-100 and STL-10 is feasible on an 8 GB GPU with ResNet-18 or ViT-Tiny.

#### Gaps
- I did not search specifically for MAE/JEPA data-pruning papers from 2024–2026. A coreset paper for MAE may exist; this must be checked before claiming novelty.
- I did not verify the "green SSL" component.

### Q3. Idea 02: SSL weather robustness and augmentation coverage

#### Takeaway
The core mechanism, "robustness tracks how close the augmentation distribution is to the corruption distribution", is already established for supervised training by Mintun, Kirillov & Xie (NeurIPS 2021), using Minimal Sample Distance. For contrastive SSL, augmentation-induced invariances and transfer have been studied by Ericsson et al. (BMVC 2022) and Purushwalkam & Gupta (NeurIPS 2020). The SSL-specific, weather-specific version on frozen backbones with ACDC paired images looks less explored, but I did not exhaustively confirm it is open. Revised risk: **MEDIUM**, not LOW.

#### Cited Findings
- **Mintun, Kirillov & Xie** build a feature space for transforms and define Minimal Sample Distance between augmentations and corruptions. Closer similarity correlates strongly with corruption robustness. Augmentations generalise poorly to corruptions that are perceptually unlike ImageNet-C. — [arXiv 2102.11273](https://arxiv.org/abs/2102.11273); [NeurIPS 2021 PDF](https://proceedings.neurips.cc/paper_files/paper/2021/file/1d49780520898fe37f0cd6b41c5311bf-Paper.pdf)
- **Ericsson, Gouk & Hospedales.** Contrastive SSL models learn invariance to their augmentations, and this partly carries over to real pose and lighting changes. Different downstream tasks need opposing invariances. Fusing representations with complementary invariances helps. — [arXiv 2111.11398](https://arxiv.org/abs/2111.11398); [BMVC 2022](https://bmvc2022.mpi-inf.mpg.de/509)
- **Purushwalkam & Gupta**, "Demystifying Contrastive SSL: Invariances, Augmentations and Dataset Biases" (NeurIPS 2020). — [arXiv 2007.13916](https://arxiv.org/html/2007.13916); [NeurIPS PDF](https://proceedings.neurips.cc/paper/2020/file/22f791da07b0d8a2504c2537c560001c-Paper.pdf)
- **"What Should Not Be Contrastive in Contrastive Learning"** (augmentation-aware SSL). — [alphaXiv 2008.05659](https://www.alphaxiv.org/abs/2008.05659)
- **FastDINOv2** (Zhang, …, Balestriero; arXiv 2507.03779, v3 Jan 2026). A frequency curriculum plus Gaussian-noise patching keeps ImageNet-C robustness while cutting DINOv2 pre-training cost. Its abstract says "matching" robustness, which is weaker than the "Improves Robustness" title. — [arXiv 2507.03779](https://arxiv.org/abs/2507.03779)
- A NeurIPS 2025 paper titled "Emergence of Noise Robustness in Self-Supervised …" showed up in search. I did not read it. — [NeurIPS 2025 PDF](https://proceedings.neurips.cc/paper_files/paper/2025/file/c6a4fc50b10ec1add5086e2f527ff0d3-Paper-Conference.pdf)
- Adverse-weather work in 2026 is mostly supervised or domain-adaptation training recipes, for example:
  - "Bridging the Generalization Gap in Adverse Weather Segmentation: A Training Recipe Perspective" — [arXiv 2605.27962](https://arxiv.org/html/2605.27962)
  - "ICM: Intra-class Mixing for Domain Adaptation in Adverse Weather" — [arXiv 2609.27533](https://arxiv.org/html/2609.27533)
  - "Large Self-Supervised Models Bridge the Gap in Domain Adaptive Object Detection" — [arXiv 2503.23220](https://arxiv.org/html/2503.23220v1)
  - I did not read these.

#### Inferences
- A defensible contribution would be "Minimal Sample Distance for SSL augmentation pipelines on real weather (ACDC paired) rather than synthetic ImageNet-C", plus predicting frozen-backbone degradation. It must cite Mintun et al. as the direct predecessor.
- "Derive minimal augmentation set" overlaps with Mintun et al.'s conclusion that training on perceptually similar augmentations helps.

#### Gaps
- I did not find (or rule out) a 2024–2026 paper that measures SSL augmentation coverage against ACDC or Dark Zurich weather pairs. A targeted search ("ACDC DINOv2 frozen linear probe weather") is still needed.
- I did not read the NeurIPS 2025 noise-robustness SSL paper.

### Q4. Idea 03: emergent depth in DINOv3 features as occlusion / ordinal ordering

#### Takeaway
Depth probing of frozen SSL features is well established. El Banani et al. (CVPR 2024) found DINOv2 best on NYUv2 and NAVI using a dense DPT-like probe. In what I read I found no work that explicitly separates **ordinal (occlusion-order) vs metric** depth in DINOv2/v3 probes, so that sub-angle is plausibly open. Revised risk: **MEDIUM** ("probe DINO for depth" is taken; "is it ordinal rather than metric?" is not obviously taken).

#### Cited Findings
- **El Banani et al., "Probing the 3D Awareness of Visual Foundation Models"** (CVPR 2024). Frozen features from about ten backbones (DINO, DINOv2, iBOT, MAE, CLIP, SigLIP, StableDiffusion, SAM, MiDaS, DeiT III) are probed with a dense multiscale DPT-like probe on NYUv2 (scenes) and NAVI (objects).
  - Object depth uses a scale-invariant [0, 1] target, because metric training collapsed to predicting the mean.
  - DINOv2 performs best on depth.
  - The paper does not mention ordinal depth. Occlusion appears only in its correspondence experiments.
  - [CVF PDF](https://openaccess.thecvf.com/content/CVPR2024/papers/Banani_Probing_the_3D_Awareness_of_Visual_Foundation_Models_CVPR_2024_paper.pdf); [arXiv 2404.08636](https://arxiv.org/abs/2404.08636)
- **Sanghavi, "From Edges to Depth: Probing the Spatial Hierarchy in Vision Transformers"** (arXiv 2604.23452, Apr 2026). This uses layer-wise linear probes on a *supervised* ViT-B/16. Boundaries become decodable at layers 5–6 (AP 0.833) and depth peaks at layer 8 on NYUv2. Ablating the probe direction degrades depth by up to 165%. It covers no DINOv2/v3 and does not say whether depth is ordinal or metric. — [arXiv 2604.23452](https://arxiv.org/abs/2604.23452)
- DINOv3 (arXiv 2508.10104) itself reports depth results. I did not read the specifics. — [arXiv 2508.10104](https://arxiv.org/html/2508.10104v1)
- Other probing follow-ups appeared in search but were not read:
  - "Splat and Distill" — [arXiv 2602.06032](https://arxiv.org/html/2602.06032)
  - [arXiv 2411.19458](https://arxiv.org/pdf/2411.19458v1)

#### Inferences
- The El Banani probe3d code ([GitHub](https://github.com/mbanani/probe3d)) is a ready baseline. Adding an ordinal / pairwise-order probe (for example pairwise depth-order accuracy across occlusion boundaries) on NYUv2 and KITTI is a small, cheap delta that fits an 8 GB GPU with ViT-S/B frozen features.
- The novelty depends on showing ordinal ≫ metric *beyond* what scale-invariant losses already capture. El Banani already used scale-invariant targets for objects, so the comparison must be careful.

#### Gaps
- I did not check whether the "Probe3D" follow-ups (2025–2026) or DINOv3's paper already include relative/ordinal depth or occlusion-boundary probes. This is the key remaining novelty check.
- Two searches for "ordinal depth probe DINOv2" returned nothing directly relevant. This is not conclusive.

### Q5. Idea 04: JEPA anisotropy oracle for dense tasks (LeJEPA → Beyond Isotropy → dense)

#### Takeaway
The three anchor papers exist and say roughly what the memo claims:
- LeJEPA: isotropic Gaussian with SIGReg.
- Beyond Isotropy: (c/d)·H⁻¹ for a known H; classification-only experiments.
- SPHERE-JEPA: hyperspherical uniformity is optimal for kNN and kernel ridge regression.

I found no 2026 follow-up that applies an H-dependent covariance target to dense tasks. Revised risk: **LOW–MEDIUM**, but feasibility and well-posedness are the real risks (see the friend's H critique).

#### Cited Findings
- **LeJEPA** (arXiv 2511.08544): "Provable and Scalable Self-Supervised Learning Without the Heuristics". It uses SIGReg, an isotropic Gaussian target, and has code. — [arXiv 2511.08544](https://arxiv.org/abs/2511.08544); [GitHub](https://github.com/galilai-group/lejepa)
- **Beyond Isotropy** (arXiv 2605.20107, 19 May 2026, single author R. Jenkinson Alvarez). It gives the (c/d)·H⁻¹ optimum for known geometry, a "price of isotropy", and the result that no canonical fixed target exists when geometry is unknown. HamJEPA beats SIGReg on CIFAR-100 and ImageNet-100 (kNN@20, linear probe). It has no dense evaluation. — [arXiv 2605.20107](https://arxiv.org/abs/2605.20107)
- **SPHERE-JEPA** (arXiv 2605.26900, 26 May 2026; Nicollier, Dunitz, Pic, Musé, Meinhardt-Llopis, Facciolo).
  - Under a worst-case formulation, uniform distributions on manifolds are optimal for kNN, and the uniform sphere is optimal for kernel ridge regression with exponential dot-product and linear kernels.
  - It adapts LeJEPA's Cramér–Wold projections to hyperspherical uniformity.
  - It reports more than 6% gain in texture-retrieval mAP and +1.8% linear-probe accuracy on ImageNet-1K (ViT-B/14) over LeJEPA.
  - It has no dense tasks in the abstract.
  - [arXiv 2605.26900](https://arxiv.org/abs/2605.26900)
- A search for LeJEPA/SIGReg dense-prediction follow-ups in 2026 returned only LeJEPA itself and secondary summaries. — [search results incl. arXiv 2511.08544](https://arxiv.org/html/2511.08544v3)

#### Inferences
- The geometry question is now contested three ways (Gaussian vs H⁻¹-shaped vs spherical uniform). A dense-task study has a clear gap to fill, but it must engage both 2605 papers.
- Beyond Isotropy itself argues that structural bias belongs in the *cross-view coupling*, not the marginal covariance. A covariance "oracle" therefore partly contradicts the very paper it builds on, and the memo should address this.
- An H for dense tasks needs construction, for example a probe-Fisher. It will be patch-level and likely low-rank, so it needs regularisation to be PD.

#### Gaps
- I did not read the full proofs, so the exact conditions on H (PD vs PSD, how c is defined) are unverified.
- I found no evidence either way on peer-review status for the two May 2026 preprints.

### Q6. Idea 07: register / attention-sink tokens as a functional global-prior channel for low-texture regions

#### Takeaway
Most of the conceptual claim is already published:
- Registers paper: artifacts arise in low-information background patches and are repurposed for internal computation.
- Lappe & Giese 2025: registers carry global information and decouple local from global features.
- Jiang et al. 2025: neuron-level mechanism plus a training-free register.
- Varma et al., 2 Oct 2026: functional roles of registers vs high-norm patch tokens, with causal ablations.

Revised risk: **HIGH** for "registers hold global info"; **MEDIUM** only for the narrow claim that this channel *specifically helps dense predictions in low-texture regions*.

#### Cited Findings
- Registers paper: artifacts in "low-informative background areas", "repurposed for internal computations". — [arXiv 2309.16588](https://arxiv.org/abs/2309.16588)
- Lappe & Giese: global information is dominated by register-token information, and [CLS] behaves similarly without registers. — [arXiv 2505.05892](https://arxiv.org/abs/2505.05892)
- **Varma, Rufail, Khullar, Sharma, "Decoding the Functional Roles of Register and High-Norm Patch Tokens in Vision Transformers"** (arXiv 2610.03698, 2 Oct 2026, ten days before the critique).
  - Register features associate with high-level semantics.
  - High-norm outlier tokens associate with "lower-level structural, background, and texture-dominant patterns".
  - Disrupting register-derived features cuts representation cosine similarity by 48.17%, against 0.31% for outlier-derived features.
  - The abstract does not mention dense prediction, depth or priors.
  - [arXiv 2610.03698](https://arxiv.org/abs/2610.03698)
- Jiang et al.: training-free test-time registers via outlier neurons. — [arXiv 2506.08010](https://arxiv.org/abs/2506.08010)
- Su, "Vision Transformers Need Better Token Interaction" (arXiv 2605.23868, May 2026). It blames degraded dense patch features in long training on global semantic "diffusion" into patches, and fixes this with entmax-1.5 attention (VOC mIoU 42.80 → 48.78 on DINOv1 ViT-S/16). It does not mention registers. — [arXiv 2605.23868](https://arxiv.org/abs/2605.23868)

#### Inferences
- The friend's "weakens idea 07" claim is correct, and Varma et al. (Oct 2026) weakens it further. The memo (Aug 2026) could not have known about Varma et al.
- A remaining narrow test: ablate or patch the registers (or Jiang's test-time register) and measure per-region dense error (depth or segmentation) stratified by local texture or gradient energy. This would be a cheap, frozen-feature experiment if no paper has done it.

#### Gaps
- I did not read the full text of Varma et al. or Lappe & Giese. Either may already include texture-stratified dense analyses.
- I could not confirm the Lappe & Giese venue (OpenReview bot check).

### Q7. Overall revised verdicts (summary across ideas)

#### Takeaway
The memo's novelty ratings are too optimistic for ideas 01 and 07 and somewhat optimistic for 02. Ideas 03 (ordinal vs metric angle) and 04 (dense extension) still have open sub-angles, but each needs explicit positioning against named prior work.

#### Cited Findings
- Idea 01 → **HIGH** risk. Direct overlap with Joshi et al. — [PMLR](https://proceedings.mlr.press/v202/joshi23b.html); [HaoChen et al.](https://arxiv.org/abs/2106.04156)
- Idea 02 → **MEDIUM** risk. Mintun et al. and Ericsson et al. — [arXiv 2102.11273](https://arxiv.org/abs/2102.11273); [arXiv 2111.11398](https://arxiv.org/abs/2111.11398)
- Idea 03 → **MEDIUM** risk. Depth probing is taken; the ordinal angle was not seen. — [El Banani CVPR 2024](https://openaccess.thecvf.com/content/CVPR2024/papers/Banani_Probing_the_3D_Awareness_of_Visual_Foundation_Models_CVPR_2024_paper.pdf)
- Idea 04 → **LOW–MEDIUM** novelty risk, **HIGH** well-posedness and feasibility risk. — [arXiv 2605.20107](https://arxiv.org/abs/2605.20107); [arXiv 2605.26900](https://arxiv.org/abs/2605.26900)
- Idea 07 → **HIGH** risk for the general claim. — [arXiv 2505.05892](https://arxiv.org/abs/2505.05892); [arXiv 2610.03698](https://arxiv.org/abs/2610.03698)

#### Inferences
- For a single 8 GB GPU, ideas 03 and 07 (frozen-feature probing) are the most feasible. Idea 04 requires pre-training JEPAs and is the least feasible beyond CIFAR scale.

#### Gaps
- Searches were limited to about 25 tool calls. CVPR 2026, ICLR 2026 and NeurIPS 2026 proceedings were not systematically scanned.
- Very recent (Sep–Oct 2026) arXiv work beyond what search surfaced may exist.
