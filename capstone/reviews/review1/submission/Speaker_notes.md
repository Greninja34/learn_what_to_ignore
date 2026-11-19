# Speaker notes: Learning What to Ignore (Team 147)

## Slide 1: Guide's approval

Screenshot of Dr. Chavan's email approving this presentation (14 October 2026).

## Slide 2: UE24CS320A · Capstone Project Approval

0:15 · Say: We want a text recogniser that learns from unlabelled pages which kinds of damage to ignore, with that choice derived from real documents instead of hand-picked.
Image: a damaged medieval manuscript page (British Museum collection; add the exact source).

## Slide 3: Outline

0:10 · Say: Five parts: how OCR and self-supervised learning work today, the problem, the work it builds on, our approach, and what we will deliver.

## Slide 4: Landscape

0:05

## Slide 5: How OCR works (the general pipeline)

0:50 · Say: Every OCR system does these five jobs. Scan and clean the image, find the layout, detect where the text is, recognise it, then fix likely mistakes with a dictionary or language model. Classic systems fight damage in stage 1, by cleaning the image first. We work only on stage 4, recognition, and teach it to see through damage instead; the other stages stay fixed so their errors never enter our comparison.
The images are one receipt run through PaddleOCR 3.7 on our laptop GPU: (1) a simulated phone photo of it, straightened by the document preprocessor (orientation + UVDoc unwarping); (2) layout blocks from PP-DocLayout; (3) line boxes from PP-OCRv6 detection; (4) line crops read by PP-OCRv6 recognition; (5) the text turned into fields with simple rules, plus a check that subtotal + tax = total. Stage 5's rules are ours; PaddleOCR stops at the text. Script: deck/tools/ocr_stage_images.py.
Sources: Chacko & Dhanya (IJAIA 2014); Dive into OCR (PaddlePaddle, 2022). Modern systems merge some stages: VLMs read whole pages end to end.

## Slide 6: Inside text recognition: four stages

1:00 · Say: Inside the recogniser there are four stages, and every known method is a choice at each one.
CTC vs attention, if asked: CTC predicts one label per image column and needs no character alignment; it is fast and good for regular, long lines, but uses little context. Attention decoders predict one character at a time while looking back at the image; more accurate, weaker on very long or very short text.
What we use in this project:
- Stage 1, transformation: none. Our inputs are already-cropped, mostly straight text lines.
- Stage 2, features: a small ViT encoder (ViT-Tiny/Small). This is what self-supervised (MAE) pretraining trains. The supervised baseline uses a small CNN.
- Stage 3, sequence: BiLSTM in the CRNN baseline; the transformer decoder in PARSeq-tiny.
- Stage 4, prediction: CTC for the baseline (CNN + BiLSTM + CTC); attention (PARSeq) for the main model.
Only the encoder's pretraining changes between our models; stages 3 and 4 are fine-tuned with the few labels.
Figures: Spatial Transformer (Jaderberg et al., 2015); ViT (Dosovitskiy et al., 2021); a bidirectional LSTM (add the source); CRNN with a CTC layer (Shi et al., 2017); PARSeq (Bautista & Atienza, 2022).
Sources: Dive into OCR (PaddlePaddle, 2022), ch. 3 and 5.

## Slide 7: Self-supervised learning

1:00 · Say: Labels are expensive: every training line needs a person to type it out. SSL makes the labels from the data itself. Hide most of a line, have the model redraw it, and check against the original. To do that, it has to learn what letters and strokes look like. Then a few labelled lines are enough to teach it to read.
LeCun's cake: most of what a model learns comes from the data itself (the cake), a little from labels (the icing), a tiny bit from rewards (the cherry). That's why SSL matters where labels are scarce, like damaged historical documents.
Image: screenshot from Welch Labs, "Yann LeCun's Billion Dollar Bet" (7:29); the cake is from LeCun's NIPS 2016 keynote.

## Slide 8: 

0:45 · Say: The family tree of self-supervised learning. Siamese networks (1993) → contrastive methods (SimCLR, MoCo) → non-contrastive (BYOL, Barlow Twins, VICReg) → latent prediction (JEPA). Point to "Pixel Level Generative Models" (top middle): MAE sits on this branch because it rebuilds the input pixels themselves; that is our family. Point to VicReg (bottom row): VICReg is our control. A September 2026 paper showed that for handwriting, rebuilding pixels beats contrastive and JEPA, which is why we chose this branch.
Image: screenshot from Welch Labs, "Yann LeCun's Billion Dollar Bet" (1:51).

## Slide 9: Why documents get damaged?

0:50 · Say: Five kinds of damage. Show-through and capture have clean physical models; fading is only partly modellable and stains only approximately. The formula reads: what you see = the front page + a faint (α), blurred (σ), mirrored copy of the back; we measure α and σ on real pages. It is what we actually do for show-through: it has a known physical form, and real pages tell us its strength. That is the "model + fit" step of our approach.
The strips are a synthetic illustration on a printed line; real damaged lines replace them once the data pipeline is in place.

## Slide 10: Problem

0:05

## Slide 11: Problem statement

0:50 · Say: Read the bold sentence. Then stress the clarification: nobody is labelling data here; the hand-picked part is the recipe of corruptions.

## Slide 12: Today vs this project

0:50 · Say: Today the corruption recipe is a guess, and we hope it transfers. Here it is measured on real pages, modelled, fitted, and then tested on damage the model never saw.
Images you could show while presenting: a real line with bleed-through next to its fitted synthetic version; a screenshot of a typical hand-chosen augmentation list from a paper's appendix.

## Slide 13: Research questions

0:50 · Say: Three questions: does it help, what transfers, and can we predict the cost of a damage type before we see it. RQ3 is what makes this more than a leaderboard result. The sketches show what each question measures; they are not results.

## Slide 14: Falsifiable hypotheses

Full wording if asked:
| H1 | Derived corruptions lower CER on real historical lines at the smallest label budget, compared with both plain MAE and hand-chosen corruptions | The gap is within seed spread, or hand-chosen corruptions match it |
| H2 | Transfer shrinks as conditions move away from what was fitted: held-out damage > medium > script | Script transfer equals or beats damage transfer |
| H3 | Invariance helps when a damage type leaves the character-carrying pixels alone, and hurts when it overlaps them (ink loss, merged strokes, diacritics): a sign flip between the two groups | One monotone relationship across all families, or no correlation |
| H4 (control) | A joint-embedding model (VICReg) trained on the same derived damage loses to derived-corruption MAE, reproducing arXiv 2609.35473 at small scale | VICReg matches or wins, so the reconstruction choice needs rethinking |

0:55 · Say: Each hypothesis says in advance what would prove us wrong. H3 is the interesting one: the same invariance should help for background damage and hurt when the damage hits the letters.

## Slide 15: Background

0:05

## Slide 16: How the field got here

1:00 · Say: SSL for text grew from contrastive methods to masked reconstruction, and in Sept 2026 pixel reconstruction was shown to win for handwriting; but the corruptions are still hand-picked (the survey). Document damage is simulated or removed before OCR (PreP-OCR), never fitted to real pages for pretraining. Mintun and Ericsson show that what a model ignores decides what it is good at, but only on natural images. Nobody has joined these for text: that is our gap.
Also relevant: Baloun et al. (IJDAR 2025) compare augmentations by trial for page segmentation; Augraphy (2022) simulates document damage.

## Slide 17: Key papers at a glance

0:45 · Say: The six papers this project stands on. Lacuna shows SSL works on historical lines; Ericsson gives us the way to measure invariance; Text-DIAE and PreP-OCR model damage, but by hand; Kišš & Hradiš give us code and the baseline to beat; Garrido-Munoz tells us to rebuild pixels. None of them fits the damage to real pages.

## Slide 18: Why pixels matter for text

0:45 · Say: LeCun argues that predicting pixels wastes effort on detail that doesn't matter, which is why JEPA predicts features instead. For text that argument flips: the tiny detail, a dot or a stroke, is exactly what decides the letter. The September 2026 HTR paper confirms it: pixel reconstruction keeps per-character information that contrastive and JEPA-style models lose. So we rebuild pixels, and the real question is which damage the model should learn to see through.
Image: Welch Labs, "Yann LeCun's $1B Bet Against LLMs [Part 1]" (11:20).

## Slide 19: Other related work

If asked whether damaged historical text is solved: on four sets of Islamicate manuscripts, Google Cloud OCR had 49–71% character error rate; pretraining on unlabelled lines plus only 30 labelled lines brought it to 15–46% (Vogler et al., 2022).

## Slide 20: What is new, and what is not

0:45 · Say: (“Not found” is not “proven absent”: the literature search continues through Phase I.) Left column: what already exists and we reuse. Right column: the four things we have not found anywhere. PreP-OCR is the closest on damage, but it sets damage levels by hand and uses them to restore images, not to pretrain a recogniser.

## Slide 21: Approach

0:05

## Slide 22: Proposed approach

0:50 · Say: The first loop is deliberately simple: a supervised baseline, then plain masked reconstruction. Each loop adds one thing, chosen by what the last loop showed.
Fixed from the start: the research questions and hypotheses, held-out tests on real damaged lines, strong baselines including supervised transfer, and the reporting protocol (image height, charset).
Decided by evidence, loop by loop: which damage types to model, backbone and model size, masking ratio and corruption strength, label budgets and test conditions.

## Slide 23: Experiments and data

0:50 · Say: Five models that differ only in pretraining, so any difference comes from what each was trained to ignore. We test with few and many labels, on clean, held-out and real damaged lines, and on scripts and capture conditions we never fitted. The one new data task is tagging a few hundred real lines by type of damage (not transcribing them). The OCR/VLM reference answers "why not just use a big model?" with numbers on the same lines.
Tools: pero-pretraining and PARSeq (code), Augraphy plus our own physics-based damage models, PyTorch. All datasets are free for research; the Indic and Arabic sets need an author request for the full version.

## Slide 24: Scope and feasibility

0:50 · Say: We keep the scope tight: recognition of single lines, small models, a handful of damage types, so every difference we see comes from pretraining. Everything we need is free and open. The main risk is named, and the answer is to always run the baseline that could beat us.
Compute if asked: a laptop GPU plus Kaggle and Colab free tiers cover the core study; university GPUs or research credits only if we scale up.

## Slide 25: Challenges and how we handle them

0:40 · Say: The template asks for possible shortcomings. These are the five that could sink the project, and what we do about each.
More if asked: few damage families give few points to correlate (we compute invariance per family × severity level); protocols differ across papers (we fix image height, charset and Unicode normalisation on day one).

## Slide 26: Applications and use cases

0:45 · Say: Anywhere text is damaged or unusual and labels are scarce: damaged documents are where OCR fails and labels are rarest, so deriving the corruptions from the documents themselves lets a small model learn a new collection from its unlabelled pages.
Why it matters beyond archives: for research, every SSL method decides what to ignore, and for text that choice is made by trial; we turn it into a procedure and test when ignoring damage helps and when it erases the letters. What we leave behind: fitted damage models, real lines tagged by damage type, and a tool that measures what a trained model ignores. Beyond OCR, the recipe (measure the nuisance, model it, fit it, check the match) could serve any field where damage is physically modellable.
Photo credits: Duke Humfrey's Library, Bodleian (David Iliffe, Wikimedia Commons); Devanagari manuscript on paper (Wikimedia Commons); handwritten page and blurred photo: add sources.

## Slide 27: Deliverables

0:05

## Slide 28: Expected deliverables

0:50 · Say: Phase I ends with a working baseline and the measurement tool. Phase II delivers the core comparison. Phase III delivers the explanation and the paper (ICDAR workshop first, then the main track or IJDAR).
Success criteria if asked: H1 holds by more than the seed spread; H3's correlation flips sign; a negative H1 still yields the analysis as a finding.

## Slide 29: Timeline

0:45 · Say: September 2026 to December 2027. Phase I builds the baseline and the measurement tool; Phase II builds and fits the damage models and runs the main comparison; Phase III explains it and writes it up. Months are indicative. Source: gantt.md (edit there, then ./build.sh).

## Slide 30: Effort plan (tentative)

0:30 · Say: Tentative split: each of us owns one workstream end to end (about a quarter of the work each), and writing is shared. The template asks for effort by individuals: this is it, and the Gantt chart shows when each task happens.

## Slide 31: References (1/2)

(no notes)

## Slide 32: References (2/2)

(no notes)

## Slide 33: Thank you

(no notes)
