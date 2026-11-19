---
marp: true
theme: lwti
size: 16:9
paginate: false
header: '![PES](assets/pes_emblem.png)'
title: "Learning What to Ignore: Deriving Invariance for Self-Supervised Text Recognition"
description: "UE24CS320A Capstone Project Approval"

---

<!-- _class: dark -->

<div class="row" style="gap:64px; height:100%;">
<div class="col" style="flex:0 0 581px; justify-content:flex-start;">
<div class="col" style="gap:20px;">
<div class="eyebrow" style="text-transform:none; margin-bottom:36px;">UE24CS320A · End Semester Capstone Review</div>
<h1>Learning What to Ignore</h1>
<div class="sub">Deriving invariance for self-supervised text recognition</div>
</div>
<div style="margin-top:56px;">
<div class="field"><span class="kicker">Project ID</span><span class="v">147</span></div>
<div class="field"><span class="kicker">Project Guide</span><span class="v">Dr. Chandrashekar P Chavan</span></div>
<div class="field"><span class="kicker">Project Team</span><span class="v">Arvind Kothamangala · Atharv Sawarkar<br>Vignesh Nunna · Rohit Rajan</span></div>
</div>
</div>
<div class="col" style="flex:1 1 auto; margin-top:40px;">
<img class="photo grow" src="assets/img/damaged_manuscript_page.jpg" style="object-position:50% 62%;">
</div>
</div>

<!--
0:15 · Say: Phase 1 end-semester assessment: the formulation, the survey, the data, and what the pilot week showed. Short answer: damage hurts and invariance predicts the error; pretraining does not help at this scale, but the same derived damage used as training augmentation lowers the error on real medieval lines.
-->

---

<!-- _class: dark -->

<div class="col" style="height:100%; justify-content:center; gap:44px;">
<h1 style="margin:0;">Agenda</h1>
<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:34px 48px;">
<div style="border-top:1px solid #35383E; padding:16px 0 4px;"><div style="font-family:var(--mono); font-size:15px; color:#77ACE3;">01</div><div style="font-family:var(--serif); font-size:31px; color:#FFFFFF; line-height:1.15; margin-top:6px;">Introduction</div><div style="font-size:15.5px; color:#9FA9B4; margin-top:6px; min-height:20px;">Problem, scope, Review 1</div></div>
<div style="border-top:1px solid #35383E; padding:16px 0 4px;"><div style="font-family:var(--mono); font-size:15px; color:#77ACE3;">02</div><div style="font-family:var(--serif); font-size:31px; color:#FFFFFF; line-height:1.15; margin-top:6px;">Gap and challenges</div><div style="font-size:15.5px; color:#9FA9B4; margin-top:6px; min-height:20px;">What is missing, what is hard</div></div>
<div style="border-top:1px solid #35383E; padding:16px 0 4px;"><div style="font-family:var(--mono); font-size:15px; color:#77ACE3;">03</div><div style="font-family:var(--serif); font-size:31px; color:#FFFFFF; line-height:1.15; margin-top:6px;">Objectives and literature</div><div style="font-size:15.5px; color:#9FA9B4; margin-top:6px; min-height:20px;">What we will do, what exists</div></div>
<div style="border-top:1px solid #35383E; padding:16px 0 4px;"><div style="font-family:var(--mono); font-size:15px; color:#77ACE3;">04</div><div style="font-family:var(--serif); font-size:31px; color:#FFFFFF; line-height:1.15; margin-top:6px;">Dataset exploration</div><div style="font-size:15.5px; color:#9FA9B4; margin-top:6px; min-height:20px;">IAM, CATMuS and others</div></div>
<div style="border-top:1px solid #35383E; padding:16px 0 4px;"><div style="font-family:var(--mono); font-size:15px; color:#77ACE3;">05</div><div style="font-family:var(--serif); font-size:31px; color:#FFFFFF; line-height:1.15; margin-top:6px;">Pilot results</div><div style="font-size:15.5px; color:#9FA9B4; margin-top:6px; min-height:20px;">Approach and first runs</div></div>
<div style="border-top:1px solid #35383E; padding:16px 0 4px;"><div style="font-family:var(--mono); font-size:15px; color:#77ACE3;">06</div><div style="font-family:var(--serif); font-size:31px; color:#FFFFFF; line-height:1.15; margin-top:6px;">Conclusion and next steps</div><div style="font-size:15.5px; color:#9FA9B4; margin-top:6px; min-height:20px;">What we learned, plan, timeline</div></div>
<div style="border-top:1px solid #35383E; padding:16px 0 4px;"><div style="font-family:var(--mono); font-size:15px; color:#77ACE3;">07</div><div style="font-family:var(--serif); font-size:31px; color:#FFFFFF; line-height:1.15; margin-top:6px;">References</div><div style="font-size:15.5px; color:#9FA9B4; margin-top:6px; min-height:20px;"></div></div>
</div>
</div>
</div>

<!-- 0:10 · Say: Seven parts, in the order of the end-semester template. Review 1 is answered inside the introduction, the approach opens the pilot section, and the timeline closes the conclusion. Dataset exploration and the pilot results are the new material since Review 1. -->

---

<!-- _class: dark divider -->

<h1 style="text-align:center; width:100%; padding-left:0;">Introduction</h1>

---

<div style="position:absolute; inset:0;">
<svg viewBox="0 0 1280 720" width="1280" height="720" style="position:absolute; left:0; top:0;"><line x1="790" y1="-10" x2="490" y2="730" style="stroke:var(--accent-text);" stroke-width="3" stroke-linecap="round"/></svg>
<div style="position:absolute; left:90px; top:230px; width:420px;"><div style="font-family:var(--serif); font-size:120px; line-height:1; color:var(--ink);">OCR</div><div style="font-size:22px; color:var(--body); margin-top:18px; line-height:1.4;">Reading the letters of a text line from a photo</div></div>
<div style="position:absolute; left:790px; top:230px; width:420px;"><div style="font-family:var(--serif); font-size:120px; line-height:1; color:var(--ink);">SSL</div><div style="font-size:22px; color:var(--body); margin-top:18px; line-height:1.4;">Learning from lines that have no typed text</div></div>
</div>

<!-- 0:50 · Say: Two ideas carry this project. OCR, optical character recognition: a model reads the letters of a text line from a photo; we only read single lines that someone has already cut from the page, and the score is CER, the share of characters read wrongly. SSL, self-supervised learning: the model first practises on lines with no typed text, by hiding parts of a line and rebuilding them, and is then fine-tuned on the few labelled lines. Old manuscripts are where typed-out text is scarcest, which is why SSL matters here. -->

---

# Document Damages

<div class="col" style="gap:8px;">
<div class="dmg"><div><h3>Clean line</h3><p class="meta">reference, no damage</p></div><img src="assets/damage/clean.png"></div>
<div class="dmg"><div><h3>Show- and bleed-through</h3><p class="meta">light or ink from the back of the page</p></div><img src="assets/damage/bleed_through.png"></div>
<div class="dmg"><div><h3>Fading</h3><p class="meta">ink thins; iron-gall ink corrodes</p></div><img src="assets/damage/fading.png"></div>
<div class="dmg"><div><h3>Foxing, stains</h3><p class="meta">fungi, oxidation, water</p></div><img src="assets/damage/foxing.png"></div>
<div class="dmg"><div><h3>Capture</h3><p class="meta">blur, sensor noise, compression</p></div><img src="assets/damage/capture.png"></div>
</div>

<!--
0:40 · Say: Five kinds of damage that a recogniser meets on old pages: show-through from the back of the page, fading, stains, and capture problems such as blur and noise. Show-through and capture have clean physical models; fading is only partly modellable and stains only approximately. The strips are a synthetic illustration on a printed line; real damaged lines are shown on the dataset slides.
-->

---

# Problem statement

<div class="card" style="gap:18px; padding:28px 30px;">
<p style="font-size:20px; line-height:1.5; color:var(--ink);">Text recognisers fail on damaged documents (faded ink, bleed-through, stains, poor scans), and damaged lines are exactly where labelled training data is scarcest.</p>
<p style="font-size:20px; line-height:1.5; color:var(--ink);">SSL can learn from unlabelled lines, but it must be told which variations to ignore. Today that choice is a hand-picked list of corruptions, re-tuned for every new collection. For handwriting, reconstruction pretraining now beats contrastive methods, so the question becomes: which damage should a model learn to see through?</p>
<p style="font-size:20px; line-height:1.5; color:var(--ink); font-weight:700;">We derive that choice from the documents themselves: model the main damage types physically, fit them to real historical lines, pretrain with them, and test whether the learned invariance transfers to unseen damage, media and scripts, and whether it predicts where recognition fails.</p>
</div>

<!--
0:50 · Say: Read the bold sentence. Then stress the clarification: nobody is labelling data here; the hand-picked part is the recipe of corruptions.
-->

---

# In simple words

<div class="grid4">
<div class="card"><div class="kicker">1 · The reader</div><h3>A model reads a photo of one line of text</h3><p class="small">This is text recognition (OCR): picture in, letters out.</p></div>
<div class="card"><div class="kicker">2 · The problem</div><h3>Old pages are faded, stained and see-through</h3><p class="small">The model makes more mistakes, and typed-out text for such pages is the hardest to get.</p></div>
<div class="card"><div class="kicker">3 · The practice</div><h3>It practises on lines with no typed text</h3><p class="small">That is SSL: hide part of a line and guess it back. The practice lines are damaged on purpose, so it learns to see through damage.</p></div>
<div class="card accent"><div class="kicker accent">4 · Our question</div><h3>Which damage should it practise on?</h3><p class="small">Today people guess. We measure real old pages and copy their damage.</p></div>
</div>

<div class="card white mt2" style="gap:10px; padding:16px 22px;">
<div class="kicker">Example: the same words, three looks</div>
<div class="row" style="gap:16px; align-items:center;">
<div style="flex:1 1 0;"><img src="assets/damage/clean.png" style="width:100%; border-radius:6px;"><p class="small meta" style="margin:4px 0 0;">Clean</p></div>
<div style="flex:1 1 0;"><img src="assets/damage/fading.png" style="width:100%; border-radius:6px;"><p class="small meta" style="margin:4px 0 0;">Faded ink</p></div>
<div style="flex:1 1 0;"><img src="assets/damage/foxing.png" style="width:100%; border-radius:6px;"><p class="small meta" style="margin:4px 0 0;">Stained paper</p></div>
</div>
<p style="font-size:17px; line-height:1.45; margin:0;">A reader that only practised on the first line struggles with the other two. We want one that reads all three, so we practise it on damage that looks like the real thing.</p>
</div>

<!-- 0:40 · Say: The whole project in four sentences. A model reads one line of text from a photo. Old pages are damaged, so it makes more mistakes, and typed-out text for them is scarce. SSL lets the model practise on lines that need no typed text; we damage those practice lines on purpose. Everyone today guesses which damage to use; we measure real old pages and copy what we see. -->

---

# Scope: one sharp question, with room to grow

<div class="grid3">
<div class="card accent"><div class="kicker accent">Our focus now (Phase 1)</div>
<ul>
<li>Which damage should a recogniser learn to see through?</li>
<li>Single text lines, small models, 7 damage types</li>
<li>2 real datasets, both Latin script</li>
</ul></div>
<div class="card"><div class="kicker">Where it grows (Phase 2–3)</div>
<ul>
<li>A script the model has never seen, as a harder test</li>
<li>2 datasets in the same script with different damage</li>
</ul></div>
<div class="card"><div class="kicker">Other work, not our focus at the moment</div>
<ul>
<li>Finding text and layout on the page</li>
<li>Large vision-language models</li>
<li>Many languages at once</li>
</ul></div>
</div>

<p style="margin-top:24px;">Currently, we claim results for the Latin script only. A new script needs its own character set (its list of letters) and its own recogniser (model), so script transfer is tested, not assumed. It may become a goal further down the line.</p>

<!-- 0:40 · Say: Phase 1 is the pilot, and it is deliberately sharp: one question, single lines, small models, seven damage types, two datasets. Both datasets use the Latin alphabet, so our claims stop there. Finding text on the page and large vision-language models are good work, but they are different questions, and keeping them out stops their errors mixing into our comparison. A new script is a later test, not something we assume will work. -->

---

# Suggestions from Review 1

<div class="row" style="gap:28px; align-items:flex-start;">
<div class="col" style="flex:1 1 auto; gap:16px;">
<div class="card" style="gap:6px; padding:16px 22px;"><div class="kicker">Panel remark</div><h3>Can good accuracy be achieved?</h3></div>
<div class="card accent" style="gap:6px; padding:16px 22px;"><div class="kicker accent">Our answer</div><p style="font-size:17px; line-height:1.45; margin:0;">Yes, on the dataset: a small model trained in under an hour reaches <b>9.8% CER</b> on IAM, better than a commercial OCR (PaddleOCR PP-OCRv6, 11.4%). Where labels are few, the error rises quickly, and that is the gap we target. In the literature, SSL reaches parity with supervised training rather than a clear win, so we always keep a supervised baseline beside it.</p></div>
<div class="card" style="gap:6px; padding:16px 22px; margin-top:8px;"><div class="kicker">Panel remark</div><h3>Are the foundations strong?</h3></div>
<div class="card accent" style="gap:6px; padding:16px 22px;"><div class="kicker accent">Our answer</div><p style="font-size:17px; line-height:1.45; margin:0;">Yes. We read the key papers and checked what is new and what is not. The use cases are real: archives and libraries hold damaged manuscripts with few typed-out lines. Every run uses the same settings, and pass/fail rules were written down before the results.</p></div>
</div>
<div class="col" style="flex:0 0 400px; gap:8px;">
<img src="assets/img/ssl_vs_supervised.png" style="width:400px; border-radius:8px; border:1px solid var(--rule);">
</div>
</div>

<!-- 0:40 · Say: Review 1 gave two remarks. On accuracy: yes, a small model trained in under an hour on a laptop beats an off-the-shelf commercial OCR on clean handwriting, 9.8% against 11.4%. But we do not oversell SSL: in the literature it reaches parity with supervised training at best, and in our pilot pretraining did not beat training from scratch. On foundations: we have read the key papers, checked novelty, and the use cases exist; the checks also caught a data bug (a black fill around CATMuS lines) that would have spoiled the results. -->

---

<!-- _class: dark divider -->

<h1 style="text-align:center; width:100%; padding-left:0;">Gap and challenges</h1>

---

# Research gap

<style scoped>table td, table th { padding: 9px 12px !important; font-size: 15px; }</style>
<div class="t-neutral">

| What earlier work did | The gap | What we add |
|---|---|---|
| SSL for text recognition<br><span class="meta">SeqCLR, Lacuna Reconstruction, LoGo-HTR</span> | The corruptions a model learns to ignore are picked by hand and re-tuned for each collection | Work out **what the model should ignore** by measuring real damage |
| Fitting damage models to real scans<br><span class="meta">Kanungo, Haralick, Baird et al. 2000; Baird 2007</span> | Built for classic OCR on binary pages; never linked to what a deep recogniser learns to ignore | Link **recipe → what the model learns to ignore → how well it reads damaged lines**, tested on real lines |
| Damage-style augmentation in text SSL<br><span class="meta">Text-DIAE</span> | Damage types and strengths are hand-picked; no test on damage, media or scripts held out | Test with **whole damage types, media and scripts held out** |
| Synthetic document damage<br><span class="meta">Augraphy, PreP-OCR, recto–verso models</span> | Which damage, and how strong, is left to the user; nobody checks if it matters for the model | Check whether **what the model ignores predicts the error** for each damage type |

</div>

<div class="band white mt"><p>Fitting damage to scans is old. Deciding what a recogniser should ignore, and checking that it does, is the new part.</p></div>

<!--
0:50 · Say: (“Not found” is not “proven absent”: the literature search continues.) Left: what already exists and we reuse. Middle: the gap, in one sentence each. Right: what we add. PreP-OCR is the closest on damage, but it sets damage levels by hand and uses them to restore images, not to train a recogniser. Fitting degradation to real scans is not our novelty (Kanungo, Haralick, Baird); using the measurements to decide what a deep recogniser should ignore, and testing the chain on real damaged lines, is. The last row is a prediction, H3, that the pilot has not confirmed; Phase 2 tests it.
-->

---

# Challenges and how we (plan to) handle them

<style scoped>table td, table th { padding: 12px 14px !important; font-size: 16px; }</style>
<div class="t-red">

| Challenge | Why it matters | How we handle it |
|---|---|---|
| Self-supervised pretraining may not beat plain supervised training (a known risk: Kišš & Hradiš 2024) | Then SSL would not pay off, and the whole idea loses its first use | Always run that baseline; the invariance analysis is a result either way |
| “You only learned your own simulator” | A model that only saw our synthetic damage may not read real damage | Always also test on real damaged lines, tagged by damage type |
| Some damage has no clean physical model | Fading and stains cannot be written as exact formulas | Model what physics allows (show-through, capture); label the rest as approximate |

</div>

<!--
0:40 · Say: The template asks for challenges. These are the three that could sink the project, why each one matters, and what we do about it. The first one is the main bet: we always run a plain supervised baseline, so that the work still stands if SSL does not help.
-->

---

<!-- _class: dark divider -->

<h1 style="text-align:center; width:100%; padding-left:0;">Objectives and literature</h1>

---

# Objectives

<div class = 'card'>
<ol style="margin:12px 0 0; padding-left:1.3em; font-size:23px; line-height:1.4; display:flex; flex-direction:column; gap:14px;">
<li>Reproducible line-recognition pipeline and strong supervised baselines</li>
<li>Per-line damage-measurement tool; how real historical lines differ from clean ones</li>
<li>Physical damage models whose frequency and strength are <b>derived</b> from the measurements</li>
<li>Masked-autoencoder pretraining with derived damage vs none, plain masking, hand-picked damage and a VICReg control</li>
<li>Transfer to a held-out damage type, a new medium and an unseen script</li>
<li>Per-damage invariance of every model vs the rise in error</li>
</ol>
</div>

<!-- 0:50 · Say: Six objectives, each with a deliverable. The first three have first versions in Phase 1 (pipeline and baselines, measurement tool, recipe v0); the rest are Phase 2 and 3. The pilot gave a first answer to objective 4 and a preview of objective 6. -->

---

# Research questions (hypotheses)

<style scoped>table td, table th { padding: 10px 13px !important; font-size: 15px; }</style>
<div class="t-neutral">

| | Question and claim, in plain words | We are wrong if… |
|---|---|---|
| **RQ1 (H1)** | Does damage derived from real pages beat plain masking and hand-picked damage when few labels exist?<br><br>**Claim:** it lowers the error on real historical lines. | the gap is within the seed spread, or hand-picked damage matches it |
| **RQ2 (H2)** | What transfers?<br><br>**Claim:** the benefit shrinks as we move away from what was fitted: unseen damage, then a new medium, then a new script. | script transfer equals or beats damage transfer |
| **RQ3 (H3)** | Does the model's invariance to a damage predict how much it raises the error?<br><br>**Claim:** ignoring paper-only damage helps; ignoring damage on the strokes does not (a “sign flip”). | one single relationship holds for all damage types, or there is none |

</div>

<!--
0:50 · Say: Three research questions, each with a claim and a statement of what would prove us wrong. RQ1 is the main comparison; the pilot answers it for augmentation, not for pretraining. RQ2 is planned for Phase 2 and 3. RQ3 has a first answer: invariance predicts the error. But the sign flip in H3 is not seen in the pilot; the proper test needs models trained to be invariant (E2).
-->

---

<!-- _class: dense -->

# Literature survey (1/2): SSL for text recognition

<style scoped>table td, table th { padding: 8px 11px !important; font-size: 13.5px; line-height:1.35; }</style>
<div class="t-neutral">

| Paper: title, authors, venue | Methodology | Result | Limitation for us |
|---|---|---|---|
| *Self-Supervised Learning for Text Recognition: A Critical Survey*<br>Penarrubia, Valero-Mas & Calvo-Zaragoza, IJCV 2025 | Surveys SSL methods for text recognition and how they are evaluated | No standard evaluation protocol; augmentations must suit text data | Maps the field but gives no way to choose the augmentations |
| *Self-supervised Pre-training of Text Recognizers*<br>Kišš & Hradiš, ICDAR 2024 | Masked pretraining on unlabelled historical lines, then fine-tuning; code is public | Gains from pretraining in some settings, compared against supervised transfer | Not always better than supervised transfer; damage not studied. Our starting code |
| *Lacuna Reconstruction: Self-Supervised Pre-Training for Low-Resource Historical Document Transcription*<br>Vogler et al., NAACL Findings 2022 | Masked-region pretraining with distractors on unlabelled lines | With 30 labelled lines, CER falls from 60.4% to 23.7% | Corruptions are not matched to real damage |
| *Learning Beyond Labels: Self-Supervised Handwritten Text Recognition (LoGo-HTR)*<br>Mitra, Mondal & Jawahar, WACV 2026 | Local–global contrastive pretraining on about 10M unlabelled word images, then fine-tuning | Gains when labels are scarce | Contrastive family; no damage study |
| *Text-DIAE: A Self-Supervised Degradation Invariant Autoencoder for Text Recognition and Document Enhancement*<br>Souibgui et al., AAAI 2023 | Autoencoder pretrained to undo masking, blur and noise | Degradation-invariant features for recognition and enhancement | Degradations and their strengths are hand-picked |

</div>

<!-- 1:00 · Say: Five papers on self-supervised pretraining for text. Penarrubia is the survey: it shows there is no standard evaluation protocol and that augmentations must suit text, with no procedure for choosing them. Kišš and Hradiš is why supervised transfer is a mandatory baseline, and our starting code. Lacuna shows SSL works with very few labels on historical lines. LoGo-HTR is the contrastive family. Text-DIAE is the closest on degradation invariance, but its degradations are hand-picked. The common limitation: the damage choices are made by hand. -->

---

<!-- _class: dense -->

# Literature survey (2/2): damage, invariance and robustness

<style scoped>table td, table th { padding: 8px 11px !important; font-size: 13.5px; line-height:1.35; }</style>
<div class="t-neutral">

| Paper: title, authors, venue | Methodology | Result | Limitation for us |
|---|---|---|---|
| *PreP-OCR: A Complete Pipeline for Document Image Restoration and Enhanced OCR Accuracy*<br>Guan et al., ACL 2025 | Restoration model trained on synthetic damage, OCR, then a language model corrects the text | Character error 63.9–70.3% lower than OCR on raw pages | Damage levels set by hand; restores images, does not train a recogniser |
| *A Statistical, Nonparametric Methodology for Document Degradation Model Validation*<br>Kanungo, Haralick, Baird, Stuetzle & Madigan, TPAMI 2000 | Fit and validate degradation models against real scans | Synthetic pages statistically close to real ones | Built for classic OCR on binary pages; not what a deep model ignores |
| *Augraphy: A Data Augmentation Library for Document Images*<br>Groleau et al., arXiv 2022 | Library of ink, paper and lighting damage effects | Realistic synthetic document damage | Which damage, and how strong, is left to the user |
| *Why Do Self-Supervised Models Transfer? On the Impact of Invariance on Downstream Tasks*<br>Ericsson, Gouk & Hospedales, BMVC 2022 | Measures how invariant a model is to each augmentation | Different tasks need different invariances | Natural images only; not text. We reuse the measure |
| *On Interaction Between Augmentations and Corruptions in Natural Corruption Robustness*<br>Mintun, Kirillov & Xie, NeurIPS 2021 | Measures how similar training augmentations are to test corruptions | Similarity predicts robustness | Supervised, natural images; corruptions are not derived from data |

</div>

<!-- 0:50 · Say: Five papers on damage, invariance and robustness. PreP-OCR restores damaged pages, with hand-set damage. Kanungo, Haralick and Baird fitted degradation models to real scans in the 1990s; we reuse that idea, and the new part is what a deep recogniser learns from it. Augraphy simulates damage but leaves the choice to the user. Ericsson gives the invariance measure we use; Mintun shows that robustness depends on how well training corruptions match the test ones, which is the reason to derive them from real pages. -->

---

<!-- _class: dark divider -->

<h1 style="text-align:center; width:100%; padding-left:0;">Dataset exploration</h1>

---

# Dataset exploration

<style scoped>table td, table th { padding: 9px 12px !important; font-size: 14.5px; }</style>
<div class="t-green">

| Dataset | Script | Size | Role | Status |
|---|---|---|---|---|
| IAM-line<br><span class="meta">Teklia on Hugging Face; research use</span> | Latin (modern English) | 6,482 train / 976 val / 2,915 test lines, 657 writers | Baseline, clean test, base for synthetic damage | Processed |
| CATMuS Medieval<br><span class="meta">Hugging Face, CC BY 4.0</span> | Latin (medieval Latin, French, others) | 194,808 lines in full | Real damage: measuring, pretraining, testing | Subset processed |
| IIIT-INDIC-HW-WORDS<br><span class="meta">CVIT, IIIT Hyderabad</span> | 8 Indian scripts | 872,000 words (word images, not lines) | Optional script test | Planned |
| Muharaf<br><span class="meta">NeurIPS 2024 Datasets track</span> | Arabic | 36,311 manuscript lines in total; 1,216 of 1,644 pages public | Unseen-script test (stretch) | Planned|


</div>

<div class="grid2 mt2">
<div class="card" style="gap:6px;"><div class="kicker">The CATMuS subset we use</div><p class="small">Latin + French, 11 projects: 23,762 training, 1,243 validation and 4,022 test lines. Every line: grey-scale, 64 px high, Unicode NFC text; character sets from the training splits only (79 symbols for IAM, 195 for CATMuS).</p></div>
<div class="card red" style="gap:6px;"><div class="kicker">Why script matters</div><p class="small">A new script needs a new character set and a new recogniser, so Latin results do not carry over automatically. Script transfer is a Phase 3 test, not an assumption.</p></div>
</div>

<!-- 0:50 · Say: Source, script, size and role, as the template asks. IAM and CATMuS are both Latin script and are downloaded and processed. The two other-script datasets are planned for Phase 3: Muharaf has real damaged Arabic lines but only the public part (1,216 of 1,644 pages); IIIT-INDIC is word images with no stated licence, so access must be confirmed with the authors. CATMuS is 22.5 GB in full, so we took the two languages that are large in both train and test. IAM uses the official writer-independent split. -->

---

<div style="display:flex; justify-content:center; align-items:center; height:100%;">
<img src="assets/img/pilot/samples_iam_catmus.png" style="height:600px; border-radius:8px; border:1px solid var(--rule);">
</div>

<!-- 0:45 · Say: Top two lines are IAM, the rest CATMuS with their transcriptions. The black polygon fill would have been read as ink by every measurement; our first damage numbers were wrong because of it, and the pipeline now removes it. -->

---

<!-- _class: dark divider -->

<h1 style="text-align:center; width:100%; padding-left:0;">Pilot results</h1>

---

# Proposed approach

<img src="assets/img/approach_diagram.jpg" style="width:1152px; display:block; margin:0 auto; border-radius:8px; border:1px solid var(--rule);">

<!--
0:50 · Say: The loop is unchanged; what changed after the pilot is step 3. Pretraining did not pay off at our scale, while the same derived damage used as plain augmentation did. So Phase 2 climbs a ladder from the cheapest use of the damage to the most expensive: E1 augmentation (done), E2 consistency training on unlabelled lines (CRNN + CTC, clean vs corrupted view), E3 one bounded attempt to rescue SSL pretraining (protocol fixes, a 10 times larger unlabelled pool on Kaggle, a public pretrained encoder) with a fixed stop date, and E4 a same-script dataset pair with different damage. Fallback side project if E2–E4 stall: hallucination of vision-language OCR under controlled damage.
Fixed from the start: the research questions and hypotheses, held-out tests on real damaged lines, strong baselines including supervised transfer, and the reporting protocol (image height, charset).
Decided by evidence, loop by loop: which damage types to model, backbone and model size, masking ratio and corruption strength, label budgets and test conditions.
-->

---

# Pilot run: what we did

<div class="grid3">
<div class="card"><div class="kicker">Data</div><ul><li><b>IAM</b>: clean modern handwriting. 6,482 training, 976 validation and 2,915 test lines</li><li><b>CATMuS</b> (Latin + French): real manuscripts from 11 projects. 23,762 training, 1,243 validation and 4,022 test lines</li><li>The CATMuS test lines come from manuscripts the model never saw in training</li></ul></div>
<div class="card accent"><div class="kicker accent">What we compared</div><ul><li><b>Baseline</b>: train on the few labelled lines only, from a random start</li><li><b>Test 1, pretraining</b>: before training, the model practises rebuilding hidden parts of unlabelled lines. Three versions: no damage, hand-picked damage, derived damage</li><li><b>Test 2, augmentation</b> (no pretraining): damage added to the labelled training lines. Same three versions, plus a simple clean-up filter as a control</li></ul></div>
<div class="card"><div class="kicker">Model</div><ul><li><b>CRNN</b>: a CNN, then a BiLSTM, then CTC. It reads a text line from left to right (7.4M parameters)</li><li><b>ConvMAE</b> is the pretraining: a masked autoencoder on the CRNN's own CNN</li><li>Same settings for every run, so differences come from the training images only</li></ul><img src="assets/img/crnn-arch.jpg" style="width:100%; border-radius:8px; border:1px solid var(--rule); margin-top:auto;"></div>
</div>

<p class="small meta" style="margin-top:14px;">* We first tried a larger transformer model (ViT). It memorised (learned by heart) the few labelled lines, with 60–75% CER (share of characters read wrongly), and was set aside.</p>

<!-- 0:40 · Say: Three things here. Data: IAM is clean modern handwriting, CATMuS is real medieval manuscripts whose test lines come from manuscripts the model never saw in training; there are train, validation and test splits for both. What we compared: from scratch, three kinds of pretraining, and augmentation tested separately. The model is the same CRNN in every run; ConvMAE is only the pretraining procedure, a masked autoencoder that trains the CRNN's own CNN, so every difference comes from the CNN's starting weights or the training images. "A few labels" means only 1%, 5% or 10% of the training lines keep their text. Footnote: a ViT was tried first and memorised the few labels. -->

---

# Baselines: how well does a small model read?

<style scoped>table td, table th { padding: 10px 14px !important; font-size: 16.5px; }</style>
<div class="t-neutral">

| Model | IAM | CATMuS |
|---|---|---|
| PaddleOCR PP-OCRv6, off the shelf | 11.4% | 52.5% |
| CRNN, all labels | **9.8%** (6,482 lines) | **20.0%** (23,762 lines) |
| CRNN, few labels | 19.9% (10% = 648 lines) | 33.8% (5% = 1,188 lines) |
| CRNN, very few labels | 43.3% (1% = 65 lines) | not run |

</div>
<p class="small meta" style="margin-top:14px;">x% labels = only that share of the training lines keep their typed text; the rest are treated as unlabelled. The few-label settings give each dataset roughly a thousand labelled lines. Repeats: 3 for the few-label rows, 2 for 1%, 1 for all labels.</p>

<p class="small meta" style="margin-top:12px;">CATMuS test = manuscripts not seen in training.</p>

<!-- 0:50 · Say: Read down the IAM column: our small model trained on all labels gets 9.8%, the ready-made industrial OCR 11.4%. Fewer labels make the error climb fast: 19.9% with 10% of the IAM labels, 43.3% with 1%. The CATMuS column shows the same pattern at 5% of labels, 33.8%. Off the shelf means the ready-made OCR, used without any training by us. A seed is one repeat of a run with different randomness; results from different seeds differ by up to about 0.5 points, so smaller differences could be luck. "5% labels" means only 5% of the training lines keep their typed text, which copies the real situation of few labels. The recogniser is the same CRNN in every row; only the amount of labelled data changes. -->

---

# Four assumptions, tested one by one

<div class="grid2">
<div class="card"><div class="kicker accent">A1</div><h3>Damage hurts a model trained on clean lines.</h3><p class="small">Rule, written before the runs: at least 2 of 7 damage types at least double the error at medium strength.</p><div style="margin-top:auto;"><span class="badge green">PASS</span></div></div>
<div class="card"><div class="kicker">A2</div><h3>Real damaged pages differ measurably from clean ones.</h3><p class="small">Rule: at least 3 damage statistics with a KS distance of 0.5 or more. KS distance: 0 = the same, 1 = totally separate (explained on the A2 slides).</p><div style="margin-top:auto;"><span class="badge red">FAIL: only 2</span></div></div>
<div class="card"><div class="kicker">A3</div><h3>Pretraining beats training from scratch.</h3><p class="small">Rule: a pretrained model beats scratch by more than the seed spread (about 0.5 points).</p><div style="margin-top:auto;"><span class="badge red">FAIL</span></div></div>
<div class="card"><div class="kicker">A4</div><h3>Derived damage beats hand-picked damage.</h3><p class="small">Rule: derived is at most as bad as hand-picked in the pretraining comparison.</p><div style="margin-top:auto;"><span class="badge green">PASS</span></div></div>
</div>

<!-- 0:50 · Say: Four claims, each with a rule we wrote down before the runs. A1 passes: damage hurts. A2 fails: real damage differs in only two of the measures we set as the test. A3 fails: pretraining does not beat training from scratch by more than the seed spread. A4 passes: derived damage is never worse than hand-picked. The thresholds were fixed before we computed the results; for A2 we fixed them before computing the KS values, after seeing the medians. Say this plainly if asked. -->


---

# The damage we add: low, medium, high

<img src="assets/img/pilot/fig_damage_levels.png" style="width:1152px; display:block; margin:0 auto; border-radius:8px; border:1px solid var(--rule);">

<p class="small" style="margin-top:12px;">The same IAM line with each of the 7 damage types added by computer at three fixed strengths. The levels were chosen by eye, before any results, to run from “barely visible” to “hard to read”.</p>

<!-- 0:40 · Say: This is what low, medium and high mean in the next tables. Same clean line, seven damage types, three strengths each. Paper tone darkens the page, fade thins the ink, blur softens the edges, noise adds speckle, show-through adds ghost writing from the back of the page, stain adds dark patches, and ink loss removes parts of the strokes. The three levels are fixed by hand before looking at any results. -->

---

# A1 passes: damage hurts

<div class="card accent" style="padding:10px 18px; margin-bottom:12px;"><p style="font-size:16px; margin:0;"><b>Assumption A1:</b> damage hurts a model trained on clean lines. <b>Rule:</b> at least 2 of 7 damage types double the error at <b>medium</b> strength (the middle level, fixed before the runs).</p></div>

<div class="row" style="gap:28px; align-items:flex-start;">
<img src="assets/img/pilot/fig_robustness.png" style="width:560px; flex:0 0 auto; border-radius:8px; border:1px solid var(--rule);">
<div class="col" style="flex:1 1 auto; gap:10px;">
<style scoped>table td, table th { padding: 6px 10px !important; font-size: 14.5px; }</style>
<div class="t-neutral">

| Test CER (%), clean: 9.8 | Low | Medium | High |
|---|---|---|---|
| Ink loss | 44.5 | **75.1** (×7.6) | 87.7 |
| Noise | 12.3 | **48.6** (×4.9) | 99.3 |
| Paper tone | 10.8 | **33.1** (×3.4) | 99.4 |
| Blur | 12.7 | **30.2** (×3.1) | 70.6 |
| Stain | 10.1 | 13.6 (×1.4) | 31.4 |
| Fade | 10.1 | 13.0 (×1.3) | 34.1 |
| Show-through | 10.0 | 12.2 (×1.2) | 21.5 |

</div>
<p class="small meta" style="margin:0;">CRNN trained on all IAM labels, tested on clean IAM lines with damage added by computer.</p>
</div>
</div>

<div class="band accent mt"><p style="font-size:17px; margin:0;"><b>PASS.</b> Four of the seven damage types more than double the error at medium strength (we needed two). The stronger the damage, the worse it gets. On real CATMuS lines, the faintest-ink quarter is 1.35–1.47× worse than the strongest-ink quarter.</p></div>

<!-- 0:45 · Say: Chart and table are the same numbers: a model trained on all IAM labels, tested on clean IAM lines with one damage added at low, medium and high strength. At medium strength, four of seven damage types at least double the error (bold): ink loss, noise, paper tone and blur. We needed two, so A1 passes. Strength matters too: paper tone goes from 10.8% to 99.4%. This is one model on one dataset; we have not run the same test on CATMuS with synthetic damage. On real CATMuS lines, the faintest-ink quarter is about 1.4 times worse than the strongest-ink quarter. The sharpness results on real lines point the other way; we think stroke width is the cause, so we claim nothing from them. -->

---

# A2 fails: only 2 of the 6 damage measures clearly differ

<div class="card" style="padding:10px 18px; margin-bottom:12px;"><p style="font-size:16px; margin:0;"><b>Assumption A2:</b> real damaged pages differ measurably from clean ones. <b>Rule:</b> at least 3 damage statistics with KS distance ≥ 0.5.</p></div>

<img src="assets/img/pilot/fig1_stats_iam_vs_catmus.png" style="width:880px; display:block; margin:0 auto; border-radius:8px; border:1px solid var(--rule);">

<p class="small" style="margin-top:10px; font-size:15px; line-height:1.4;">Each graph compares one measure on clean IAM lines (grey outline) and real CATMuS lines (green): the further apart the two shapes, the bigger the difference (KS D). <b>Paper level (D 0.82)</b> and <b>faint grey, i.e. show-through (D 0.84)</b> are clearly apart: real pages are darker and more see-through. Background unevenness, ink contrast, sharpness and noise overlap, so no clear difference. Only 2 reach 0.5 and we needed 3: A2 <b>fails</b>. Stroke width and ink fraction also differ, but that is scale, not damage.</p>

<!-- 0:40 · Say: Each small graph is one measure taken on every line, for clean IAM handwriting and for real CATMuS manuscripts. Only paper level and faint grey on the paper pass our 0.5 bar, so by our own rule A2 fails. The rule was fixed before we computed the KS values, after seeing the medians. The next slide explains how to read the graphs. -->

---

<style scoped>table td, table th { padding: 8px 10px !important; font-size: 14.5px; }</style>
<div class="row" style="gap:28px; align-items:flex-start;">
<div style="flex:0 0 58%;">
<div class="t-neutral">

| Statistic | What it measures | IAM median | CATMuS median | KS D |
|---|---|---|---|---|
| Paper level | brightness of the paper (low = darker) | 0.980 | 0.804 | **0.82** |
| Faint grey on paper | share of paper that is faintly grey (high = show-through) | 0.0018 | 0.0767 | **0.84** |
| Background unevenness | patchy paper (stains, uneven light) | 0.0054 | 0.0094 | 0.42 |
| Ink–paper contrast | dark ink vs paper (low = faded) | 0.478 | 0.408 | 0.26 |
| Sharpness | edge sharpness (low = blurred) | 1.084 | 0.939 | 0.11 |
| Pixel noise | speckle on the paper | 0.0000 | 0.0058 | 0.16 |
| Stroke width (scale) | pen width in pixels | 3.33 | 4.81 | 0.73 |
| Ink fraction (scale) | share of pixels that are ink | 0.119 | 0.260 | 0.94 |

</div>
</div>
<div class="col" style="flex:1 1 auto; gap:12px;">
<div class="card" style="gap:6px; padding:14px 18px;"><div class="kicker">Each graph</div><p class="small" style="margin:0;">One number measured on every line. Bars = how many lines have that value. Grey outline = IAM, green fill = CATMuS. Median = the middle value.</p></div>
<div class="card" style="gap:6px; padding:14px 18px;"><div class="kicker">KS distance D</div><p class="small" style="margin:0;">Sort the values of both datasets; D is the largest gap between the two running shares ("share of lines at or below x"). 0 = the same, 1 = totally separate.</p></div>
<div class="card accent" style="gap:6px; padding:14px 18px;"><div class="kicker accent">The rule</div><p class="small" style="margin:0;">Counts only damage statistics (the first six rows). Two reach D ≥ 0.5; three are needed. Rows 7–8 differ because CATMuS strokes are thicker and denser at the same line height: scale, not damage.</p></div>
<div class="card" style="gap:6px; padding:14px 18px;"><div class="kicker">Why 6, not 7</div><p class="small" style="margin:0;">Each damage type is tracked by one measure. The 7th type, ink loss, is held out for testing, and its measure (ink fraction) mixes in pen size, so it is not counted.</p></div>
</div>
</div>

<!-- 0:50 · Say: The table lists the eight measures. The first six are damage measures; the last two are scale, meaning how thick the pen is and how much of the line is ink. A KS distance D tells you how separate two sets of values are, from 0 for identical to 1 for totally apart. Two damage measures reach 0.5, and our rule needs three, so A2 fails. We used 3,000 random lines per dataset, and the values match the stats files. About 5% of CATMuS lines are already pure black and white, which causes the spike at 1.0 in two graphs. -->

---

# Two ways to choose the damage

<div class="row" style="gap:24px; align-items:flex-start;">
<img src="assets/img/pilot/fig_corruptions_handpicked_vs_derived.png" style="height:500px; flex:0 0 auto; border-radius:8px; border:1px solid var(--rule);">
<div class="col" style="gap:12px; flex:1 1 auto;">
<div class="card" style="gap:6px; padding:14px 18px;"><div class="kicker">Hand-picked (the usual practice)</div><p style="font-size:15.5px; line-height:1.4; margin:0;">No measuring. Each of the six damage types hits half of the lines (a 50% chance), at a strength drawn evenly from a range we chose by eye.</p></div>
<div class="card accent" style="gap:6px; padding:14px 18px;"><div class="kicker accent">Derived (our recipe v0): from real lines</div>
<ol style="margin:0; padding-left:1.2em; font-size:15.5px; line-height:1.4; display:flex; flex-direction:column; gap:4px;">
<li><b>Strength scale:</b> add the damage to clean IAM lines at many strengths and measure one number (e.g. paper brightness) each time.</li>
<li><b>Which lines are damaged:</b> a CATMuS line counts as damaged if its number lies beyond what clean IAM lines show (outside the 5–95% band). Its strength is read off the scale.</li>
<li><b>Frequency and strength:</b> the share of damaged CATMuS lines sets how often to apply the damage; their strengths set how strong.</li>
</ol>
<p style="font-size:15.5px; line-height:1.4; margin:0;"><b>Result:</b> paper tone 84% of lines, show-through 89%, stain 37%, fade 26%, noise 11%, blur 5%.</p></div>
<p class="small meta" style="margin:0;">Ink loss is held out of every recipe: it is our “unseen damage” test.</p>
</div>
</div>

<!-- 0:45 · Say: The top strips are real CATMuS lines. Below them, the same clean IAM line is shown four times with hand-picked damage, then four times with damage derived from the measurements, which looks like grey paper and faint ghost strokes. Hand-picked is how it is usually done: every damage type with a 50% chance and a strength from a range chosen by eye (lwti/damage/derive.py, handpicked). Derived is three steps: build a strength scale for each damage by damaging clean IAM lines and measuring one statistic; call a CATMuS line damaged if its statistic lies beyond the 5-95% band of clean lines and read its strength off the scale; then the share of damaged lines is the probability and their strengths are the strength distribution. Show-through is ink from the back of the page seen through the paper. Version 0 has a limit: a gap between IAM and CATMuS numbers also includes script, pen and scan differences, not only damage. Phase 2 replaces this with a separate physical fit for each damage type. -->

---

# Pretraining: hide parts of a line, rebuild it clean

<img src="assets/img/pilot/fig_pretrain_mask_rebuild.png" style="width:1152px; display:block; margin:0 auto;">

<div class="card mt2" style="padding:16px 22px;"><p style="font-size:16.5px; line-height:1.45; margin:0;"><b>Pretraining</b> = before using any labels, the CNN learns to rebuild lines with 60% of the 8-pixel strips hidden (damage added first; it must rebuild the clean line). 30,244 unlabelled lines (CATMuS + IAM training lines, text thrown away), 34 minutes. Then the whole CRNN is trained on the few labelled lines.</p></div>

<!-- 0:40 · Say: This is the pretraining task, with real outputs from our derived-damage run. Row 1 is the input with damage, row 2 is what the model actually sees with 60% of the strips hidden, row 3 is what it draws back, row 4 is the clean target it is scored against. Left a real CATMuS line with noise added, right an IAM line. The rebuild is blurry where whole letters were hidden: it learns texture and stroke shape well, but not which letter is which, which may be one reason pretraining did not help the reader. -->

---

# Does pretraining help? (A3, A4)

<style scoped>table td, table th { padding: 10px 14px !important; font-size: 16.5px; }</style>
<div class="col" style="gap:26px;">

<div class="t-neutral">

| Test CER, mean of 2–3 seeds | No pretraining (scratch) | Masking only | + hand-picked damage | + derived damage |
|---|---|---|---|---|
| CATMuS, 5% labels | 33.8% | 33.3% | 35.0% | 33.4% |
| IAM, 10% labels | 19.9% | 20.4% | 21.0% | 20.5% |
| IAM, 1% labels | 43.3% | 43.8% | 44.7% | 43.9% |

</div>

<div class="grid2" style="gap:22px;">
<div class="card red" style="gap:8px; padding:16px 22px;"><div class="kicker">A3, pretraining beats scratch: FAIL</div><p style="font-size:16.5px; line-height:1.45; margin:0;">No pretrained version beats starting from scratch by more than the seed spread (about 0.5 points).</p></div>
<div class="card green" style="gap:8px; padding:16px 22px;"><div class="kicker green">A4, derived beats hand-picked: PASS</div><p style="font-size:16.5px; line-height:1.45; margin:0;">Derived is at most as bad as hand-picked in 3 of 3 settings, but not better than doing nothing. It “wins” only because hand-picked damage hurts (35.0% vs 33.3%).</p></div>
</div>

<p class="small meta" style="margin:0;">CER = share of characters read wrong (lower is better). Masking only = the rebuild task with no added damage. 5% labels = 5% of training lines keep their text.</p>

</div>

<!-- 0:50 · Say: Same CRNN (the small reader model: a CNN that looks at the line, then a recurrent layer that reads the letters) with the same fine-tuning. Only the CNN's starting weights differ, and scratch means no pretraining at all. The main point is the first two columns: nothing pretrained beats scratch by more than the noise between seeds. A seed is one repeat of a run with a different random start. -->

---

# Why pretraining did not help here

<p style="font-size:17px; line-height:1.45;" class="meta">Our explanations; not yet tested.</p>

<div class="grid3">
<div class="card" style="gap:8px;"><div class="kicker">Too little data</div><p style="font-size:18px; line-height:1.45; margin:0;">We pretrained on 30k lines for 34 minutes. Lacuna Reconstruction used 750k lines to cut the error from 60.4% to 23.7%.</p></div>
<div class="card" style="gap:8px;"><div class="kicker">Start washed out</div><p style="font-size:18px; line-height:1.45; margin:0;">Fine-tuning ran long at full step size (learning rate), which may have erased the pretrained start.</p></div>
<div class="card" style="gap:8px;"><div class="kicker">Easy task</div><p style="font-size:18px; line-height:1.45; margin:0;">Rebuilding small gaps teaches texture, which normal training learns within minutes anyway.</p></div>
</div>

<div class="card white mt" style="gap:8px; padding:16px 22px;"><div class="kicker">What Kišš & Hradiš (ICDAR 2024) found</div>
<p style="font-size:17px; line-height:1.45; margin:0;">They pretrained text recognisers on unlabelled historical lines (handwritten Bentham papers and old printed books) with masked and contrastive methods, then fine-tuned with different amounts of labels. Pretraining clearly beat training from scratch. But a model first trained with labels on a <b>related</b> dataset (transfer learning) was about as good or better. So SSL is not a free win, and it needs a lot of unlabelled data. Our pilot did not even beat scratch, which points to our small scale. Phase 2 gives pretraining one bounded retry (E3) with a fixed stop date.</p></div>

<!-- 0:40 · Say: These three are our guesses for why pretraining did not help, and none is tested yet, so read them as the next checks. Scale: Lacuna Reconstruction pretrained on 750k lines, we used 30k. The other two are about how fine-tuning treats the pretrained weights and how easy the rebuild task is. Kišš and Hradiš: target-domain pretraining beats scratch, but struggles to beat transfer from a closely related labelled dataset; this is why supervised transfer is a mandatory baseline for us. -->

---

# Use the damage as augmentation

<div class="row" style="gap:28px; align-items:flex-start;">
<img src="assets/img/pilot/expl_aug.jpg" style="height:500px; flex:0 0 auto; border-radius:8px; border:1px solid var(--rule);">
<div class="col" style="gap:12px; flex:1 1 auto;">
<div class="card" style="padding:16px 20px;"><p style="font-size:17px; line-height:1.45; margin:0;"><b>The idea:</b> show the model the same labelled line many times, each time with different fake damage, but always with the same correct text. To get the answer right, it has to learn to look past the damage.</p><p style="font-size:17px; line-height:1.45; margin:6px 0 0;"><b>Augmentation</b> = change the training image, keep its label. The damage is drawn afresh on every pass over the data. No pretraining and no extra lines are needed. The picture, top to bottom: 4 real training lines as they are; with hand-picked damage (2 random draws each); with derived damage (2 draws each); after the clean-up filter.</p></div>
<div class="card" style="gap:4px; padding:14px 20px;"><div class="kicker">No augmentation</div><p style="font-size:17px; line-height:1.45; margin:0;">The plain model, trained on the lines as they are.</p></div>
<div class="card" style="gap:4px; padding:14px 20px;"><div class="kicker">+ hand-picked damage</div><p style="font-size:17px; line-height:1.45; margin:0;">The usual guess, with damage types chosen by hand.</p></div>
<div class="card accent" style="gap:4px; padding:14px 20px;"><div class="kicker accent">+ derived damage</div><p style="font-size:17px; line-height:1.45; margin:0;">Our recipe, measured on real lines.</p></div>
<div class="card" style="gap:4px; padding:14px 20px;"><div class="kicker">Background normalisation</div><p style="font-size:17px; line-height:1.45; margin:0;">A control: a plain filter flattens the paper tone before the model sees the line. No learning. It asks: could a simple clean-up do the same?</p></div>
<p class="small meta" style="margin:0;">For these results, validation and test lines are never damaged; only training lines are.</p>
</div>
</div>

<!-- 0:40 · Say: The picture shows four CATMuS training lines in four versions: the clean line first, then hand-picked damage, derived damage and background normalisation. Damage only changes the training images; the text label stays the same, and nothing is pretrained. The control asks whether flattening the paper tone alone gives the same gain. -->

---

# Derived damage helps on real lines

<style scoped>table td, table th { padding: 11px 16px !important; font-size: 18px; }</style>
<div class="col" style="gap:22px;">
<div class="t-neutral">

| Test CER, mean of 3 seeds | No augmentation | + hand-picked damage | + derived damage | Background normalisation |
|---|---|---|---|---|
| CATMuS 5%, all test lines | 33.8% | 33.6% | **31.6%** | 33.0% |
| CATMuS 5%, darkest-paper quarter | 35.6% | 34.7% | **33.0%** | 35.0% |
| CATMuS 5%, most show-through quarter | 35.7% | 35.1% | **32.9%** | 34.7% |
| CATMuS 5%, lowest-contrast quarter | 39.4% | 38.1% | **37.0%** | 38.2% |
| IAM 10%, clean test lines | 19.9% | **18.8%** | 18.9% | 19.8% |

</div>

<div class="grid3" style="gap:16px;">
<div class="card accent" style="gap:6px; padding:12px 16px;"><div class="kicker accent">Real lines</div><p style="font-size:15.5px; line-height:1.4; margin:0;">33.8% → 31.6% on CATMuS: 2.2 fewer wrong characters per 100, about 3 times the seed spread. Hand-picked damage barely moves it.</p></div>
<div class="card" style="gap:6px; padding:12px 16px;"><div class="kicker">Not just a clean-up</div><p style="font-size:15.5px; line-height:1.4; margin:0;">Flattening the paper tone with a filter gives only 33.0%. The model gains by learning from damage, not by having it removed.</p></div>
<div class="card" style="gap:6px; padding:12px 16px;"><div class="kicker">Clean IAM: a tie</div><p style="font-size:15.5px; line-height:1.4; margin:0;">18.8% vs 18.9% is within noise. The recipe copies CATMuS damage, which clean IAM lines do not have.</p></div>
</div>

<p class="small meta" style="margin:0;">CER = share of characters read wrong (lower is better). A “quarter” = the 25% most damaged test lines by that measurement. The gain on the damaged quarters (2.4–2.8 points) is similar to the gain on all lines.</p>
</div>

<!--
0:50 · Say: Read the bold numbers, which are the best value in each row. On real CATMuS test lines, derived damage takes the error from 33.8% to 31.6%, and it also wins on the three hardest quarters. On clean IAM lines hand-picked is best, which is the one place our recipe does not win.
If asked, what the numbers mean: 2.2 fewer wrong characters per 100 is more than the seed spread (about ±0.5-0.7), so it is not luck. A "quarter" is the 25% most damaged test lines by that measurement, within each manuscript project. Seed = one repeat run with a different random start.
If asked, the rules fixed before the runs: four of the five (B1, B3, B4, B5) are met. B2 (derived beats hand-picked) is checked on IAM synthetic damage: 19.4% vs 18.9%, so it is not met there; on real CATMuS lines derived is better, 31.6% vs 33.6%.
If asked, the limits of this pilot result: (a) the big synthetic IAM gain (37.9% to 19.4% under medium damage) is partly circular, because it is measured on the damage types we trained on; the fair check is held-out ink loss, where the error ratio goes from x3.82 to x3.59 with derived and x3.27 with hand-picked, so only a small real gain on unseen damage. (b) On CATMuS the gain on the hardest quarters is 2.4-2.8 points, about the gain on all lines (2.2), so we say "helps on CATMuS", not "targets damage"; E4, a second dataset pair, separates the two. (c) The winner depends on the data: hand-picked wins on IAM, derived on CATMuS. (d) 3 seeds, one dataset pair, one model: a pilot result, not a final one.
-->

---

# How we measure invariance (our current choice)

<div class="col" style="gap:20px;">
<p style="font-size:20px; line-height:1.5; color:var(--ink); margin:0;"><b>Invariance</b> = how much the model ignores a damage. <b>1</b> = the damage changed nothing inside the model.</p>

<div class="grid4">
<div class="card" style="gap:8px; padding:16px 18px;"><div class="kicker">Step 1</div><h3>Run the lines</h3><p style="font-size:16px; line-height:1.45; margin:0;">Take 500 IAM test lines. Run each one through the model's image-reading part (its CNN): once clean, once with one synthetic damage added.</p></div>
<div class="card" style="gap:8px; padding:16px 18px;"><div class="kicker">Step 2</div><h3>Read the features</h3><p style="font-size:16px; line-height:1.45; margin:0;">The CNN gives 384 numbers for each slice of the line. Average them along the line: one list of 384 numbers per line. Standardise each number (mean 0, spread 1, from the clean lines).</p></div>
<div class="card" style="gap:8px; padding:16px 18px;"><div class="kicker">Step 3</div><h3>Compare</h3><p style="font-size:16px; line-height:1.45; margin:0;">Compare clean and damaged with cosine similarity: how alike two lists of numbers point (1 = identical). Average over the lines. This is <b>invariance</b>.</p></div>
<div class="card" style="gap:8px; padding:16px 18px;"><div class="kicker">Step 4</div><h3>Measure the error rise</h3><p style="font-size:16px; line-height:1.45; margin:0;">CER = share of characters read wrong (lower is better). <b>CER rise</b> = damaged CER ÷ clean CER. Each damage type at each strength gives one pair (invariance, CER rise): 7 types × 3 strengths = 21 pairs. RQ3 asks whether the first predicts the second.</p></div>
</div>

<div class="card white" style="align-self:center; align-items:center; text-align:center; padding:18px 32px; gap:8px;">
<div class="kicker">The measure</div>
<div class="mono" style="font-size:18.7px; font-weight:600; color:var(--ink);">invariance = mean over lines of cos( z(clean line), z(damaged line) )</div>
<p style="font-size:16px; margin:0;">z = the standardised features · cos = cosine similarity</p>
</div>
</div>

<!-- 1:00 · Say: Invariance means how much the model ignores a damage. We take 500 test lines, run each one clean and with one damage added, then compare the model's internal numbers; a score of 1 means the damage changed nothing inside the model. Each damage type and strength gives one pair of numbers, invariance and error rise: 7 types × 3 strengths = 21 pairs. This is our current choice of measure, not the only possible one. The measure follows the style of Ericsson et al. (BMVC 2022), which was made for natural images, applied here to text recognition. -->

---

<!-- _class: dark divider -->

<h1 style="text-align:center; width:100%; padding-left:0;">Conclusion and next steps</h1>

---

# Conclusion

<div class="col" style="gap:18px;">
<div class="grid2">
<div class="card white" style="gap:8px;"><div class="kicker">What we built in Phase 1</div>
<ul style="margin:0; padding-left:1.1em; font-size:16px; line-height:1.45; display:flex; flex-direction:column; gap:6px;">
<li>Clean data pipeline for IAM (modern English handwriting) and CATMuS (medieval Latin and French manuscripts)</li>
<li>Baseline error: CER 9.8% on IAM, 20.0% on CATMuS</li>
<li>Damage-measurement tool and 7 damage models (formulas for 7 kinds of damage)</li>
<li>Derived recipe v0: a first set of damage settings, derived from measurements on real lines</li>
<li>Pilot: pretraining and augmentation, each run repeated</li>
</ul>
</div>
<div class="card accent" style="gap:8px;"><div class="kicker accent">What the pilot says</div>
<p style="font-size:16px; line-height:1.45; margin:0;">A1–A4 are pass/fail checks written down before the runs.</p>
<ul style="margin:0; padding-left:1.1em; font-size:16px; line-height:1.45; display:flex; flex-direction:column; gap:6px;">
<li><b>A1 pass:</b> damage hurts</li>
<li><b>A2 fail:</b> real damage differs mainly in paper tone and show-through (ink seen through from the other side)</li>
<li><b>A3 fail:</b> pretraining (learning from unlabelled lines first) does not help at 30k lines / 34 min</li>
<li><b>A4 pass:</b> derived damage is never worse than hand-picked damage</li>
<li><b>E1, damage as augmentation</b> (labelled lines shown with fake damage, same text): CATMuS error 33.8% → 31.6%, also on the hardest real lines</li>
</ul>
</div>
</div>
</div>

<!-- 0:45 · Say: Phase 1 is complete. Pretraining did not help at this scale, but the same derived damage used as plain augmentation did, on real medieval lines. We do not yet claim it targets damage specifically. Phase 2 climbs from E2 to E3 to E4. -->

---

# Next steps (Phase 2 plan, tentative and subject to change)

<div class="col" style="gap:18px;">
<div class="grid4">
<div class="card" style="gap:8px; padding:16px 18px;"><div class="kicker">planned</div><h3>E2 · Consistency</h3><p style="font-size:16px; line-height:1.45; margin:0;">Unlabelled lines (no transcription). The model should give the same reading for a clean and a damaged view. This is also the real test of H3, our sign-flip prediction.</p></div>
<div class="card" style="gap:8px; padding:16px 18px;"><div class="kicker">planned</div><h3>E3 · One bounded SSL retry</h3><p style="font-size:16px; line-height:1.45; margin:0;">SSL = learning from unlabelled lines first. One more try: 10× more unlabelled lines, a public pretrained encoder, and a fixed stop date, whatever the result.</p></div>
<div class="card" style="gap:8px; padding:16px 18px;"><div class="kicker">planned</div><h3>E4 · New damage</h3><p style="font-size:16px; line-height:1.45; margin:0;">A same-script dataset pair with different damage, to separate damage from script (the writing system).</p></div>
<div class="card" style="gap:8px; padding:16px 18px;"><div class="kicker">planned</div><h3>Phase 3 · Script transfer</h3><p style="font-size:16px; line-height:1.45; margin:0;">One unseen script as a stretch test, e.g. an Indic script (IIIT-INDIC) or Arabic manuscripts (Muharaf). Access and licence to be confirmed.</p></div>
</div>
<div class="band white"><p style="font-size:18px; line-height:1.45; margin:0;"><b>Also next:</b> fitted (physical) damage models v1, tagged real lines, invariance on CATMuS, more seeds. The plan is to be confirmed with our guide after this assessment.</p></div>
</div>

<!-- 0:45 · Say: Phase 2 is four planned steps, each with a fixed scope. E2 uses unlabelled lines and is also the real test of the H3 sign flip. E3 is one bounded attempt to rescue SSL with a fixed stop date, so it cannot drag on. E4 separates damage from script, and Phase 3 tests an unseen script as a stretch goal; access and licence for Muharaf are still to be confirmed. -->

---

<!-- _header: '' -->

![bg](assets/img/gantt.png)

<!--
0:45 · Say: September 2026 to December 2027. Phase I builds the baseline and the measurement tool and runs the pilot (pretraining, E1 augmentation); Phase II fits the damage models and runs E2 consistency, E3 the bounded SSL rescue and E4 the new dataset pair; Phase III explains it and writes it up. Months are indicative. Source: gantt.md (edit there, then ./build.sh).
-->

---

<!-- _class: dark divider -->

<h1 style="text-align:center; width:100%; padding-left:0;">References</h1>

---

<!-- _class: dense -->

# References

<div class="refs">
<div><span>1</span><span>Garrido-Munoz &amp; Calvo-Zaragoza. <a href="https://arxiv.org/abs/2609.35473"><i>Handwritten Text Recognition Lives in the High-Pixel Variance Subspace.</i></a> arXiv:2609.35473, 2026.</span></div>
<div><span>2</span><span>Penarrubia, Valero-Mas &amp; Calvo-Zaragoza. <a href="https://arxiv.org/abs/2407.19889"><i>Self-Supervised Learning for Text Recognition: A Critical Survey.</i></a> IJCV, 2025.</span></div>
<div><span>3</span><span>Kišš &amp; Hradiš. <a href="https://arxiv.org/abs/2405.00420"><i>Self-supervised Pre-training of Text Recognizers.</i></a> ICDAR, 2024.</span></div>
<div><span>4</span><span>Vogler et al. <a href="https://arxiv.org/abs/2112.08692"><i>Lacuna Reconstruction: Self-Supervised Pre-Training for Low-Resource Historical Document Transcription.</i></a> Findings of NAACL, 2022.</span></div>
<div><span>5</span><span>Souibgui et al. <a href="https://arxiv.org/abs/2203.04814"><i>Text-DIAE: A Self-Supervised Degradation Invariant Autoencoder for Text Recognition and Document Enhancement.</i></a> AAAI, 2023.</span></div>
<div><span>6</span><span>Ericsson, Gouk &amp; Hospedales. <a href="https://arxiv.org/abs/2111.11398"><i>Why Do Self-Supervised Models Transfer? On the Impact of Invariance on Downstream Tasks.</i></a> BMVC, 2022.</span></div>
<div><span>7</span><span>Mintun, Kirillov &amp; Xie. <a href="https://arxiv.org/abs/2102.11273"><i>On Interaction Between Augmentations and Corruptions in Natural Corruption Robustness.</i></a> NeurIPS, 2021.</span></div>
<div><span>8</span><span>Mitra, Mondal &amp; Jawahar. <a href="https://openaccess.thecvf.com/content/WACV2026/html/Mitra_Learning_Beyond_Labels_Self-Supervised_Handwritten_Text_Recognition_WACV_2026_paper.html"><i>Learning Beyond Labels: Self-Supervised Handwritten Text Recognition (LoGo-HTR).</i></a> WACV, 2026.</span></div>
<div><span>9</span><span>Guan et al. <a href="https://arxiv.org/abs/2505.20429"><i>PreP-OCR: A Complete Pipeline for Document Image Restoration and Enhanced OCR Accuracy.</i></a> ACL, 2025.</span></div>
<div><span>10</span><span>He et al. <a href="https://arxiv.org/abs/2111.06377"><i>Masked Autoencoders Are Scalable Vision Learners.</i></a> CVPR, 2022.</span></div>
<div><span>11</span><span>Shi, Bai &amp; Yao. <a href="https://arxiv.org/abs/1507.05717"><i>An End-to-End Trainable Neural Network for Image-based Sequence Recognition (CRNN).</i></a> TPAMI, 2017.</span></div>
<div><span>12</span><span>Clérice et al. <a href="https://doi.org/10.1007/978-3-031-70543-4_11"><i>CATMuS Medieval: a multilingual large-scale cross-century dataset in Latin script for HTR.</i></a> ICDAR, 2024.</span></div>
<div><span>13</span><span>Marti &amp; Bunke. <a href="https://doi.org/10.1007/s100320200071"><i>The IAM-database: an English sentence database for offline handwriting recognition.</i></a> IJDAR, 2002.</span></div>
<div><span>14</span><span>Li et al. <a href="https://github.com/PaddlePaddle/PaddleOCR"><i>PaddleOCR (PP-OCRv6).</i></a> PaddlePaddle.</span></div>
<div><span>15</span><span>Groleau et al. <a href="https://arxiv.org/abs/2208.14558"><i>Augraphy: A Data Augmentation Library for Document Images.</i></a> arXiv:2208.14558, 2022.</span></div>
<div><span>16</span><span>Kanungo, Haralick, Baird, Stuetzle &amp; Madigan. <a href="https://doi.org/10.1109/34.888707"><i>A Statistical, Nonparametric Methodology for Document Degradation Model Validation.</i></a> TPAMI, 2000.</span></div>
<div><span>17</span><span>Baird. <a href="https://doi.org/10.1007/978-1-84628-726-8_12"><i>The State of the Art of Document Image Degradation Modelling.</i></a> In <i>Digital Document Processing</i>, Springer, 2007.</span></div>
</div>

---

<!-- _class: dark -->

<div class="col" style="height:100%; justify-content:center;">
<div class="col" style="gap:16px;">
<h1 style="font-size:96px;">Thank you</h1>
</div>
</div>
