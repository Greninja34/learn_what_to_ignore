# Weekly status reports

Edit this file, then run `python make_reports.py` (research2 env) to rebuild the PDF and the Word files.
Each week has exactly two rows per section; leave a row as `| 2 |  |  |  |` to keep it blank.

Project Title: Learning What to Ignore: Deriving Invariance for Self-Supervised Text Recognition
Batch No: 147
Guide: Dr. Chandrashekhar P Chavan

## Members

| Name | SRN |
|---|---|
| Arvind Kothamangala | PES2UG24CS628 |
| Atharv Sawarkar | PES2UG24CS670 |
| Vignesh Nunna | PES2UG24CS582 |
| Rohit Rajan | PES2UG25CS821 |

## Week 1: 2026-08-03 to 2026-08-09

### Activities Completed

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Team formed; Phase-I guidelines, deliverables and review schedule studied | 04.08.2026 | Team of four |
| 2 | Brainstormed candidate research areas | 07.08.2026 | SSL, OCR, segmentation, detection, depth, VLMs and others |

### In Progress

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Reading recent surveys for each candidate area | 09.08.2026 | Ongoing |
| 2 | Checking compute feasibility of each area | 09.08.2026 |  |

### Plan for Next Week

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Shortlist research areas by feasibility and interest | 14.08.2026 |  |
| 2 | Start survey of self-supervised learning (SSL) | 16.08.2026 |  |

## Week 2: 2026-08-10 to 2026-08-16

### Activities Completed

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Shortlisted vision SSL and OCR as focus areas | 12.08.2026 | Large-compute areas dropped |
| 2 | Studied early SSL ideas: Siamese networks, word2vec, BERT, context prediction | 15.08.2026 | Background for SSL family tree |

### In Progress

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Survey of contrastive and non-contrastive SSL (SimCLR, MoCo, BYOL, Barlow Twins, VICReg, DINO) | 16.08.2026 | Ongoing |
| 2 | Survey of OCR pipelines: detection, recognition, post-processing | 16.08.2026 | Ongoing |

### Plan for Next Week

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Study masked image modelling (MAE) and JEPA | 21.08.2026 |  |
| 2 | List open problems in vision SSL that fit our compute | 23.08.2026 |  |

## Week 3: 2026-08-17 to 2026-08-23

### Activities Completed

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Completed survey of contrastive and non-contrastive SSL | 18.08.2026 | SimCLR, MoCo, BYOL, Barlow Twins, VICReg, DINO |
| 2 | Studied masked image modelling (MAE) and JEPA | 21.08.2026 | Pixel vs feature-space prediction |

### In Progress

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Drafting memo of open problems in vision SSL | 23.08.2026 | First draft |
| 2 | Survey of text recognisers (CRNN + CTC, transformer decoders) | 23.08.2026 | Ongoing |

### Plan for Next Week

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Revise memo for a single 8 GB GPU budget | 28.08.2026 |  |
| 2 | Compile candidate paper ideas from all areas | 29.08.2026 |  |

## Week 4: 2026-08-24 to 2026-08-30

### Activities Completed

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Memo “Twelve Openings in Vision SSL” (rev. 2) completed | 27.08.2026 | Recalibrated for 8 GB GPU |
| 2 | Compiled list of candidate paper ideas | 29.08.2026 | Indic document OCR benchmark, VLM OCR hallucination, SSL for glyphs, others |

### In Progress

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Ranking ideas by novelty, feasibility and data availability | 30.08.2026 | Ongoing |
| 2 | Literature search for top-ranked ideas | 30.08.2026 | Ongoing |

### Plan for Next Week

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Narrow down to three candidate topics | 03.09.2026 |  |
| 2 | Read literature on SSL for text recognition | 06.09.2026 |  |

## Week 5: 2026-08-31 to 2026-09-06

### Activities Completed

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Narrowed to three topics: SSL for text recognition, VLM OCR hallucination, Indic OCR benchmark | 03.09.2026 | SSL for text recognition chosen as main topic |
| 2 | Read IJCV survey on SSL for text recognition (Penarrubia et al.) | 05.09.2026 | Augmentations still hand-picked: possible gap |

### In Progress

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Reading text-recognition SSL papers (SeqCLR, Kišš & Hradiš, Lacuna Reconstruction) | 06.09.2026 | Ongoing |
| 2 | Identifying public handwriting text-line datasets | 06.09.2026 | IAM, CATMuS |

### Plan for Next Week

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Finish reading SSL-for-text papers | 11.09.2026 |  |
| 2 | Study document degradation and damage simulation | 13.09.2026 |  |

## Week 6: 2026-09-07 to 2026-09-13

### Activities Completed

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Read SeqCLR, Kišš & Hradiš (ICDAR 2024), Lacuna Reconstruction, LoGo-HTR | 10.09.2026 | Masked reconstruction works well for text |
| 2 | Studied IAM and CATMuS datasets: splits, licences, line format | 12.09.2026 | IAM lines for baseline |

### In Progress

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Study of document damage: Text-DIAE, Augraphy, recto-verso bleed-through | 13.09.2026 | Ongoing |
| 2 | Drafting problem statement on degradation and SSL | 13.09.2026 | Draft |

### Plan for Next Week

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Read invariance literature (Ericsson et al., Mintun et al.) | 18.09.2026 |  |
| 2 | Refine problem statement | 20.09.2026 |  |

## Week 7: 2026-09-14 to 2026-09-20

### Activities Completed

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Studied Text-DIAE, Augraphy and PreP-OCR (damage simulation and removal) | 16.09.2026 | Damage levels set by hand in all |
| 2 | Read Ericsson et al. (BMVC 2022) and Mintun et al. (NeurIPS 2021) | 19.09.2026 | What a model ignores decides what it is good at |

### In Progress

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Problem statement: fit pretraining corruptions to real degraded lines | 20.09.2026 | Draft |
| 2 | Looking at Indic scripts and manuscripts for transfer tests | 20.09.2026 | Ongoing |

### Plan for Next Week

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Write research questions and hypotheses | 25.09.2026 |  |
| 2 | Plan supervised baseline and evaluation metric | 27.09.2026 |  |

## Week 8: 2026-09-21 to 2026-09-27

### Activities Completed

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Drafted research questions (RQ1–RQ3) and hypotheses | 24.09.2026 |  |
| 2 | Planned supervised CNN + BiLSTM + CTC baseline; CER as metric | 26.09.2026 | 1%, 10%, 100% label budgets |

### In Progress

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Study of side topics: VLM OCR hallucination, Indic OCR benchmarks | 27.09.2026 | Backup options |
| 2 | Tracking new arXiv work on SSL for handwriting recognition | 27.09.2026 | Ongoing |

### Plan for Next Week

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Read newly released work on SSL for HTR | 02.10.2026 |  |
| 2 | Compare MAE and contrastive pretraining for our plan | 04.10.2026 |  |

## Week 9: 2026-09-28 to 2026-10-04

### Activities Completed

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Studied arXiv 2609.35473 (28.09.2026): pixel reconstruction beats contrastive and JEPA for HTR | 30.09.2026 | Supports MAE-style pretraining |
| 2 | Reframed plan around masked reconstruction (MAE) pretraining | 03.10.2026 | VICReg kept as control |

### In Progress

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Survey of VLM OCR hallucination benchmarks and Indic OCR datasets | 04.10.2026 | Side topics |
| 2 | Updating problem statement after reframe | 04.10.2026 | Ongoing |

### Plan for Next Week

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Novelty check of the reframed idea | 10.10.2026 |  |
| 2 | Get external feedback on shortlisted ideas | 11.10.2026 |  |

## Week 10: 2026-10-05 to 2026-10-11

### Activities Completed

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Novelty check of candidate ideas against 2024–26 literature | 10.10.2026 | Fitting damage to real pages for text SSL: not found |
| 2 | Reviewed and fact-checked external critique of our ideas | 11.10.2026 |  |

### In Progress

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Finalising topic, title and problem statement | 11.10.2026 | Ongoing |
| 2 | Studying Review-1 PPT template and requirements | 11.10.2026 |  |

### Plan for Next Week

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Finalise title, problem statement and research questions | 12.10.2026 |  |
| 2 | Prepare and present Review-1 | 15.10.2026 |  |

## Week 11: 2026-10-12 to 2026-10-18

### Activities Completed

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Finalised title and problem statement; prepared Review-1 presentation | 14.10.2026 | Approved by guide on 14.10.2026 |
| 2 | Review-1 presentation delivered | 15.10.2026 | Phase-I Review-1 |

### In Progress

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Incorporating Review-1 feedback into the plan | 18.10.2026 | Ongoing |
| 2 | Setting up GPU environment (PyTorch, PaddleOCR) | 18.10.2026 | Ongoing |

### Plan for Next Week

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Update title and problem statement in shared spreadsheet; submit Review-1 Google Form | 24.10.2026 | Deadline 26.10.2026 |
| 2 | Start data pipeline for IAM text lines | 25.10.2026 |  |

## Week 12: 2026-10-19 to 2026-10-25

### Activities Completed

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Incorporated Review-1 feedback (show achievable accuracy; strengthen the base) into the plan | 21.10.2026 | Baselines and a comparison with an off-the-shelf OCR planned |
| 2 | Set up GPU environment; tested PaddleOCR on sample lines | 23.10.2026 | PyTorch and PaddleOCR working |

### In Progress

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Updating title and problem statement in the shared spreadsheet | 25.10.2026 | Review-1 form due 26.10.2026 |
| 2 | Preparing the Review-1 submission deck and weekly reports | 25.10.2026 | Ongoing |

### Plan for Next Week

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Submit the Review-1 Google Form, spreadsheet entry and PPT | 26.10.2026 |  |
| 2 | Study the Phase-1 report format and the next review templates | 30.10.2026 |  |

## Week 13: 2026-10-26 to 2026-11-01

### Activities Completed

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Submitted the Review-1 Google Form, spreadsheet entry and PPT with the guide's approval mail | 26.10.2026 | Deadline met |
| 2 | Studied the Phase-1 report guidelines and the Review-2 and end-semester templates | 30.10.2026 | Report 20–25 pages |

### In Progress

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Planning a one-week pilot to test the main assumptions before the end-semester review | 01.11.2026 | Pass/fail rules to be written first |
| 2 | Drafting the Phase-1 report structure | 01.11.2026 | Ongoing |

### Plan for Next Week

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Finalise the pilot plan and its pass/fail criteria | 04.11.2026 |  |
| 2 | Update the literature survey with 2026 work | 07.11.2026 |  |

## Week 14: 2026-11-02 to 2026-11-08

### Activities Completed

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Received the Phase-1 ESA schedule (13–20 Nov); noted ESA marking areas and report rules | 04.11.2026 | Plagiarism limit 15% including AI content |
| 2 | Wrote the pilot plan with four testable assumptions (A1–A4) and fixed pass/fail rules | 07.11.2026 | Fixed before any result |

### In Progress

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Updating the literature survey (2026 sweep) | 08.11.2026 | Ongoing |
| 2 | Downloading IAM and CATMuS Medieval (Latin and French) | 08.11.2026 | Ongoing |

### Plan for Next Week

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Build the data pipeline and supervised baselines | 10.11.2026 |  |
| 2 | Measure damage on real lines; run pretraining comparison | 11.11.2026 |  |

## Week 15: 2026-11-09 to 2026-11-15

### Activities Completed

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Built data pipeline (removed CATMuS polygon fill), CRNN baselines and damage-measurement tool | 09.11.2026 | IAM CER 9.8%; PaddleOCR 11.4% IAM, 52.5% CATMuS |
| 2 | Ran pretraining comparison and robustness and invariance analysis; verdicts A1 pass, A2 fail, A3 fail, A4 pass | 10.11.2026 | Invariance vs error rise: Spearman -0.9 |

### In Progress

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Writing the Phase-1 report and the Review-2 deck | 10.11.2026 | Final by 12.11.2026 |
| 2 | Testing fixes for the weak pretraining result (freeze-then-unfreeze, lower rate) | 10.11.2026 | If time allows |

### Plan for Next Week

| # | Tasks | Date | Remarks |
|---|---|---|---|
| 1 | Review-2 (ISA-2) with the guide; take feedback | 13.11.2026 |  |
| 2 | Prepare for the Phase-1 end-semester assessment | 17.11.2026 | ESA slot to be confirmed |
