# Learning What to Ignore: Project Starter Pack

Oct 12, 2026 · @MN

**The project in one paragraph.** You pretrain a small text-line encoder on unlabelled line images with a reconstruction objective (mask or corrupt the input, rebuild the clean line). The corruptions it must see through are *derived* — their ranges fitted to measured statistics of real degraded lines — instead of hand-picked. Then you fine-tune a recogniser with few labels, test it on conditions held out from pretraining (a degradation type, a medium, a script, a capture condition), and measure whether "how invariant the model is to X" predicts "how much its error rate rises under X".

The data question has a short answer: **you do not need to build a dataset.** Clean labelled lines, real degraded historical lines and other-script sets already exist free; the "synthetic" part is your own degradation code, which *is* the research contribution, not a separate data project (Part 3).

Read Part 1 over a week, Parts 2–3 once, and come back with questions on Part 4.

## Part 1 — Learn the field

Your existing [One-Week Crash Course](https://claude.ai/code/artifact/747a7731-e76c-4f0d-bae4-597504465231) covers transformers, SSL, invariance, image physics, degradation and OCR day by day. Below is the trimmed path for *this* project, in order, with what to take from each.

| # | Resource | Type | What to take from it |
| --- | --- | --- | --- |
| 1 | [3Blue1Brown: Attention, step by step](https://www.3blue1brown.com/lessons/attention) | Video, 30 min | How a transformer mixes tokens |
| 2 | [Hugging Face CV Course](https://huggingface.co/learn/computer-vision-course) — CNN and ViT units | Course, 3 h | Encoders you'll use |
| 3 | [Lilian Weng: Self-Supervised Representation Learning](https://lilianweng.github.io/posts/2019-11-10-self-supervised/) | Blog, 1 h | The map of SSL families |
| 4 | [NYU DL Week 10: SSL in vision (Ishan Misra)](https://atcold.github.io/NYU-DLSP21/en/week10/10/) | Lecture, 2 h | Why augmentations decide what is learned |
| 5 | [MAE: Masked Autoencoders](https://arxiv.org/abs/2111.06377) | Paper, figures + intro | The reconstruction objective your project now uses |
| 6 | [UvA Tutorial 17: SimCLR](https://uvadlc-notebooks.readthedocs.io/en/latest/tutorial_notebooks/tutorial17/SimCLR.html) | Notebook, 1.5 h | Hands-on: augmentations are a few lines of code |
| 7 | [3Blue1Brown: Groups and the monster](https://www.3blue1brown.com/lessons/groups-and-monsters) + [GDL Lecture 3, Geometric Priors](https://youtu.be/qEjWMhRlXgY) | Video + lecture, 1.5 h | Vocabulary: invariance, action, orbit |
| 8 | [FPCV: Image Formation](https://fpcv.cs.columbia.edu/) and Image Processing modules | Video series, 3 h | Blur, noise, frequency — the language of degradation |
| 9 | [Salerno & Tonazzini: recto–verso model](https://ercim-news.ercim.eu/en95/special/highly-degraded-recto-verso-document-image-processing-and-understanding) | Short article | What a physical degradation model looks like |
| 10 | [Distill: Sequence Modeling with CTC](https://distill.pub/2017/ctc/) | Interactive blog, 1 h | How a line becomes characters |
| 11 | [Scheidl: Build an HTR system](https://harald-scheidl.medium.com/build-a-handwritten-text-recognition-system-using-tensorflow-2326a3487cd5) | Blog + code, 1 h | The whole HTR pipeline end to end |
| 12 | [Self-Supervised Learning for Text Recognition: A Critical Survey (IJCV)](https://arxiv.org/abs/2407.19889) | Survey, 2 h | The whole sub-field on one map |
| 13 | [Kiss & Hradis 2024: SSL pretraining on historical lines](https://arxiv.org/abs/2405.00420) | Paper, 1 h | Closest prior work, with code |
| 14 | [HTR Lives in the High-Pixel Variance Subspace (Sep 2026)](https://arxiv.org/abs/2609.35473) | Paper, 1 h | Why reconstruction beats contrastive for handwriting |
| 15 | [Ericsson et al.: Why do SSL models transfer?](https://arxiv.org/abs/2111.11398) | Paper, 1 h | How to measure invariance |

Items 1–11 are "understand the field". Items 12–15 are "understand your exact problem" — read them last and slowly. If you only have a weekend: 3, 5, 10, 12, 14.

## Part 2 — Scope, feasibility, use cases, background

### Background: why this problem exists

- **SSL learns what its corruptions or augmentations tell it to ignore.** Pick the wrong set and the model throws away what the task needs, or keeps what it should drop. [Ericsson et al.](https://arxiv.org/abs/2111.11398) showed different downstream tasks want opposite invariances.
- **For text, this choice is made by hand.** The IJCV survey of SSL for text recognition says augmentations are picked to "best fit the nature of the data" and gives no procedure ([survey](https://arxiv.org/abs/2407.19889)). [Text-DIAE (AAAI 2023)](https://ojs.aaai.org/index.php/AAAI/article/download/25328/25100) trains a degradation-invariant autoencoder for text, but with hand-picked degradations.
- **The method choice shifted in Sep 2026.** Pixel reconstruction beat contrastive and JEPA pretraining on six handwriting benchmarks, and kept per-character position information the others lose ([2609.35473](https://arxiv.org/abs/2609.35473)). So your "what to ignore" lives in the input corruptions of a reconstruction model.
- **The closest analysis outside text:** [Mintun et al.](https://arxiv.org/abs/2102.11273) showed that how similar an augmentation is to a corruption predicts robustness — for natural images, supervised. Nobody has done this for text with derived corruptions.

### Use cases

- **Archives and libraries:** a new collection (different ink, paper, scanner) without hand-retuning a pipeline.
- **Low-resource scripts:** labels are scarce, so most learning has to come from unlabelled pages.
- **Damaged records:** faded or bled-through registers, letters, government files.
- **Camera capture:** phone photos of documents instead of flatbed scans.

### Scope

| In scope | Out of scope (for now) |
| --- | --- |
| Line-level images (already cut into lines) | Page layout and line segmentation |
| One small encoder (5–25M parameters) | Large VLMs, foundation-model scale |
| 3–5 degradation families with forward models | Every possible damage type |
| Clean handwriting + one real degraded set + one held-out medium or script | Many languages at once |
| CER at 1%, 10%, 100% labels + invariance scores | Language models, post-correction |

### Feasibility

| Factor | Verdict | Why |
| --- | --- | --- |
| Compute | Fits | Small encoder at line height 32–64 px; pretraining runs estimated at 4–12 GPU-hours, so use Kaggle for the long ones. Estimates, not measured. |
| Data | Fits | Free, line-level sets exist for every role (Part 3) |
| Code | Fits | [pero-pretraining](https://github.com/DCGM/pero-pretraining) for SSL on historical lines, [PARSeq](https://github.com/baudm/parseq) for recognisers, [Augraphy](https://github.com/sparkfish/augraphy) for degradations |
| Novelty | Medium risk | Derivation + match measurement for text looks open as of Oct 2026; SSL-for-text itself is crowded |
| Main risk | Real | SSL may not beat plain supervised transfer from a related labelled set ([Kiss & Hradis](https://arxiv.org/abs/2405.00420) saw this), so that baseline is mandatory |

### Literature to keep open

| Paper | Role |
| --- | --- |
| [SSL for Text Recognition: A Critical Survey (IJCV 2025)](https://arxiv.org/abs/2407.19889) | Map of the sub-field and its protocol problems |
| [Handwritten Text Recognition: A Survey (2025)](https://arxiv.org/abs/2502.08417) | HTR methods and datasets |
| [Deep Learning for Historical Document Analysis — A Survey](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8321201/) | Historical documents specifically |
| [Kiss & Hradis 2024](https://arxiv.org/abs/2405.00420) | Closest prior work + code |
| [HTR Lives in the High-Pixel Variance Subspace](https://arxiv.org/abs/2609.35473) | Why reconstruction; possible match measure |
| [Text-DIAE](https://ojs.aaai.org/index.php/AAAI/article/download/25328/25100) | Hand-picked-degradation baseline you improve on |
| [SeqCLR](https://arxiv.org/abs/2012.10873), [DiG](https://arxiv.org/abs/2207.00193), [CCD](https://arxiv.org/abs/2211.00288) | Standard SSL-for-text methods |
| [Ericsson et al.](https://arxiv.org/abs/2111.11398), [Mintun et al.](https://arxiv.org/abs/2102.11273) | How to measure invariance and match |
| [Augraphy paper](https://arxiv.org/abs/2208.14558) | The degradation library you build on |

## Part 3 — Datasets: your main concern, answered

**Short answer: data is about one week of plumbing, not a separate project.** Everything you need already exists, free and line-level. The "synthetic" part is your degradation code applied to real lines, and that code *is* your contribution.

### Your three options, judged

| Option | Use it for | Don't use it for | Verdict |
| --- | --- | --- | --- |
| **Official research datasets** (Hugging Face, HTR-United, Zenodo) | Training, pretraining, all reported results | — | Main source. Clear licences, standard splits reviewers recognise |
| **Kaggle / Google Dataset Search** | Finding things, quick experiments | Reported results | Many Kaggle HTR sets are re-uploads of IAM and others with unclear licences and non-standard splits. Trace each back to its official source before it goes in a paper |
| **Synthetic** | (a) your derived corruptions on real lines; (b) rendering fonts for a new script if no real data exists | Your only test set | If you test only on your own simulator, a reviewer will say you learned your simulator. You must also test on **real** degraded lines |

### What to download, by role

| Role | Dataset | Size | Access |
| --- | --- | --- | --- |
| Clean labelled handwriting | [IAM-line (Teklia, Hugging Face)](https://huggingface.co/datasets/Teklia/IAM-line) | \~10.4k lines: 6.48k train / 976 val / 2.92k test | Free, no sign-up. Also cite the [original IAM terms](https://fki.tic.heia-fr.ch/databases/iam-handwriting-database) (research only) |
| Real degraded historical lines | [CATMuS Medieval (Hugging Face)](https://huggingface.co/datasets/CATMuS/medieval) | \~195k lines: 153k train / 19.4k val / 22.6k test, multilingual medieval manuscripts | CC-BY-4.0, not gated |
| More historical sets, filterable by script and period | [HTR-United catalogue](https://htr-united.github.io/) (`catalog.json`) | Dozens of sets, each with its own licence | Free; per-dataset licence |
| More line-level HTR | [Teklia on Hugging Face](https://huggingface.co/Teklia): NorHand (Norwegian), POPP, Himanis, Belfort | Varies | Check each card |
| Unseen script (Indic) | [IIIT-INDIC-HW-WORDS](https://cvit.iiit.ac.in/research/projects/cvit-projects/iiit-indic-hw-words) | 872k words, 10 scripts | Direct zips, word-level, no stated licence: ask the authors |
| Unseen script (Arabic) | [Muharaf](https://arxiv.org/abs/2406.09630) (NeurIPS 2024 D&B) | 36,311 lines; 1,216 of 1,644 pages public | Public part only |
| Unseen capture (camera) | Scene-text LMDB bundles linked from [PARSeq](https://github.com/baudm/parseq) | IIIT5k, IC13, IC15 and more | Free |
| Degradation code | [Augraphy](https://github.com/sparkfish/augraphy) | InkBleed, BleedThrough, LowInk, NoiseTexturize, Jpeg, ShadowCast and more; no fading/foxing class | MIT, last release Dec 2023 |

**Start with three:** IAM-line (clean), CATMuS Medieval (real degradation), one held-out probe (PARSeq scene text, or an IIIT Indic script).

### The one real data task

To answer "which invariances transfer", you need a **real** test set where each line is tagged with the degradation it shows (bleed-through, fading, stains, blur). Nobody ships this. Plan to tag a few hundred CATMuS or HTR-United test lines by degradation type yourself. That's labelling the *damage*, not transcribing the text: a few evenings, and a small contribution in its own right.

### Pitfalls

- **Charsets:** a new script needs a new output layer; normalise Unicode consistently (NFC), or Indic and Arabic error rates inflate.
- **Transcription rules differ:** medieval sets expand or keep abbreviations differently. Read each set's guidelines and report CER both ways if needed.
- **Leakage:** use IAM's official writer-independent split, and never pretrain on test lines, even unlabelled.
- **Fitting "derived" ranges:** fit degradation statistics only on pretraining data, never on test conditions.
- **Augraphy on lines:** some effects (BleedThrough, BookBinding) expect full pages; apply them to page crops or tune them, and pre-render if the CPU slows training.

## Part 4 — Rough implementation sketch

&#91;embedded content: project pipeline · fit, pretrain, fine-tune, measure\]

The top row is the "derive" step, the middle row is pretraining, and the bottom two rows are the experiment. Everything below is a sketch to react to, not a spec; runtimes are estimates, not measurements.

| Stage | What you build | Tools | Rough cost |
| --- | --- | --- | --- |
| 0. Baseline | Supervised recogniser on IAM at 1%, 10%, 100% labels; CER with `jiwer` | [PARSeq](https://github.com/baudm/parseq) (tiny) or a small CNN + BiLSTM + CTC | 1–3 h per full run |
| 1. Measure | Per-line statistics on real degraded lines: ink/background contrast, blur (variance of Laplacian), noise level, stroke width, bleed intensity | NumPy, OpenCV | Minutes |
| 2. Derive | Turn each statistic into a parameter range for one damage family (e.g. Augraphy BleedThrough strength drawn from the measured distribution). Keep one family out entirely | [Augraphy](https://github.com/sparkfish/augraphy) + your own forward models (show-through, fading) | Your main coding work |
| 3. Pretrain | Encoder sees the corrupted line (plus masking), decoder rebuilds the clean line. Runs: plain MAE, hand-picked corruptions, derived corruptions | [pero-pretraining](https://github.com/DCGM/pero-pretraining) as a starting point; line height 32–64 px; 5–25M parameters | 4–12 GPU-h each; long ones on Kaggle |
| 4. Fine-tune | Add a CTC head, fine-tune at 1%, 10%, 100%; 3 seeds at 1% | Same code as stage 0 | Minutes to 1 h |
| 5. Test | CER on clean IAM, IAM with the held-out damage, real degraded lines (tagged by damage type), scene text or an unseen script | PARSeq LMDB bundles, IIIT Indic, Muharaf | Minutes |
| 6. Measure the match | Ericsson-style invariance score per damage family and severity: distance between features of a line and its damaged copy. Correlate with the CER rise under that family | Mean-pooled encoder features, whitened distance | Minutes |

**Order to build it in:** stage 0 first, end to end, before anything clever. Then 3 with plain MAE (no derived corruptions), so you know the reconstruction setup works. Only then 1–2, and finally 5–6. The comparisons that make the paper are: derived vs hand-picked vs plain MAE vs supervised transfer, on held-out conditions.

## Sources

Dataset sizes and licences were checked on the linked pages in October 2026 (IAM-line, CATMuS Medieval, Teklia, HTR-United, IIIT-INDIC-HW-WORDS, Muharaf, Augraphy, PARSeq, pero-pretraining). Not yet checked: Union14M terms, KHATT, Bentham, READ 2016. The September 2026 reconstruction result ([2609.35473](https://arxiv.org/abs/2609.35473)) was read at abstract level only — read the full paper before building on its subspace measure. Compute times are estimates. Background reports from this conversation: *Vision SSL ideas reality check* and *OCR hallucination cube and benchmarks*.
