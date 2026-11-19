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
<div class="eyebrow" style="text-transform:none; margin-bottom:36px;">UE24CS320A · Project Phase 1 · Review 2</div>
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
0:15 · Say: Review 2: what the pilot week showed. Short answer: damage hurts and invariance predicts the error, but pretraining does not yet beat training from scratch at this scale.
-->

---

<!-- _class: dark -->

<div class="row" style="height:100%; align-items:center; gap:64px;">
<h1 style="flex:0 0 420px;">Agenda</h1>
<ol class="outline">
<li><span class="n">01</span><span class="s">Introduction, problem and scope</span></li>
<li><span class="n">02</span><span class="s">Suggestions from Review 1</span></li>
<li><span class="n">03</span><span class="s">Research gap and challenges</span></li>
<li><span class="n">04</span><span class="s">Objectives and literature survey</span></li>
<li><span class="n">05</span><span class="s">Timeline and effort</span></li>
<li><span class="n">06</span><span class="s">Pilot results</span></li>
<li><span class="n">07</span><span class="s">Conclusion and references</span></li>
</ol>
</div>

<!-- 0:10 · Say: Seven parts, in the order of the Review-2 template. The pilot results are the new material since Review 1. -->

---

# Why documents get damaged?

<div class="col" style="gap:8px;">
<div class="dmg"><div><h3>Clean line</h3><p class="meta">reference, no damage</p></div><img src="assets/damage/clean.png"></div>
<div class="dmg"><div><h3>Show- and bleed-through</h3><p class="meta">light or ink from the back of the page</p></div><img src="assets/damage/bleed_through.png"></div>
<div class="dmg"><div><h3>Fading</h3><p class="meta">ink thins; iron-gall ink corrodes</p></div><img src="assets/damage/fading.png"></div>
<div class="dmg"><div><h3>Foxing, stains</h3><p class="meta">fungi, oxidation, water</p></div><img src="assets/damage/foxing.png"></div>
<div class="dmg"><div><h3>Capture</h3><p class="meta">blur, sensor noise, compression</p></div><img src="assets/damage/capture.png"></div>
</div>
<div class="card white mt2" style="align-self:center; align-items:center; text-align:center; padding:14px 32px; gap:6px;">
<div class="mono" style="font-size:18.7px; font-weight:600; color:var(--ink);">front_seen ≈ front + α · blur<sub>σ</sub>(mirror(back))</div>
</div>

<!--
0:50 · Say: Five kinds of damage. Show-through and capture have clean physical models; fading is only partly modellable and stains only approximately. The formula reads: what you see = the front page + a faint (α), blurred (σ), mirrored copy of the back; we measure α and σ on real pages. It is what we actually do for show-through: it has a known physical form, and real pages tell us its strength. That is the "model + fit" step of our approach.
The strips are a synthetic illustration on a printed line; real damaged lines replace them once the data pipeline is in place.
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

# Abstract and scope

<div class="card" style="gap:16px; padding:26px 30px;">
<p style="font-size:19px; line-height:1.5; color:var(--ink);">Text recognisers fail on damaged documents, and damaged collections are where transcribed data is scarcest. Self-supervised learning (SSL) can learn from unlabelled lines by rebuilding a line from a corrupted copy, but the corruptions are hand-picked and re-tuned per collection.</p>
<p style="font-size:19px; line-height:1.5; color:var(--ink);"><b>Learning What to Ignore</b> measures damage on real historical lines, models the main damage types physically, fits their parameters to the measurements, and pretrains a masked autoencoder with the derived corruptions. We ask whether this beats plain masking and hand-picked corruptions with few labels, what transfers to unseen damage, media and scripts, and whether measured invariance predicts the error rise.</p>
<p style="font-size:19px; line-height:1.5; color:var(--ink);"><b>Scope:</b> single text lines already cut from the page; small models; 7 damage types; IAM (modern English) and CATMuS (medieval Latin and French) now, an unseen script in Phase 3. Page layout and large vision-language models are left out.</p>
</div>

<!-- 0:50 · Say: One-paragraph version of the abstract on the panel's answer sheet. The scope is deliberately tight so that any difference we see comes from pretraining. -->

---

# Scope and feasibility

<div class="grid2">
<div class="card"><div class="kicker">What we will do</div><ul><li>Read single text lines already cut out of the page</li><li>Change only how the encoder is pretrained; keep models small</li><li>Model 3–5 damage types that physics can describe</li><li>Test on modern and historical handwriting, plus one unseen script</li></ul></div>
<div class="card dashed"><div class="kicker">What we leave out (for now)</div><ul><li>Finding text on the page (detection, layout): its errors would blur the comparison</li><li>Studying large vision-language models</li><li>Many languages at once</li></ul></div>
</div>

<div class="kicker mt2" style="margin-bottom:10px;">Can we do it?</div>
<div style="display:grid; grid-template-columns:repeat(5, 1fr); gap:12px;">
<div class="card white" style="padding:14px 16px; gap:6px;"><h3>Data</h3><span class="badge green" style="align-self:flex-start; font-size:11px; padding:0 7px; letter-spacing:.5px;">Fits</span><p class="small">Free, line-level datasets exist for every role.</p></div>
<div class="card white" style="padding:14px 16px; gap:6px;"><h3>Code</h3><span class="badge green" style="align-self:flex-start; font-size:11px; padding:0 7px; letter-spacing:.5px;">Fits</span><p class="small">We start from open code: pero-pretraining, PARSeq, Augraphy.</p></div>
<div class="card white" style="padding:14px 16px; gap:6px;"><h3>Compute</h3><span class="badge green" style="align-self:flex-start; font-size:11px; padding:0 7px; letter-spacing:.5px;">Fits</span><p class="small">Small models train on a laptop GPU and free Kaggle or Colab.</p></div>
<div class="card white" style="padding:14px 16px; gap:6px;"><h3>Novelty</h3><span class="badge" style="align-self:flex-start; font-size:11px; padding:0 7px; letter-spacing:.5px;">Medium risk</span><p class="small">No one fits damage to real pages for text SSL yet, but the field is busy.</p></div>
<div class="card white" style="padding:14px 16px; gap:6px;"><h3>Main risk</h3><span class="badge red" style="align-self:flex-start; font-size:11px; padding:0 7px; letter-spacing:.5px;">Real</span><p class="small">SSL may not beat supervised transfer, so we always run that baseline.</p></div>
</div>

<!--
0:50 · Say: We keep the scope tight: recognition of single lines, small models, a handful of damage types, so every difference we see comes from pretraining. Everything we need is free and open. The main risk is named, and the answer is to always run the baseline that could beat us.
Compute if asked: a laptop GPU plus Kaggle and Colab free tiers cover the core study; university GPUs or research credits only if we scale up.
-->

---

# Suggestions from Review 1

<style scoped>table td, table th { padding: 12px 16px !important; font-size: 17px; }</style>
<div class="t-neutral">

| Panel remark | How it is addressed now |
|---|---|
| Show that good accuracy can be achieved | A small CRNN trained for 50 min on a laptop GPU reaches **9.8%** character error rate on IAM; an off-the-shelf industrial OCR (PaddleOCR PP-OCRv6) gets 11.4% on the same lines |
| Make the base foundations strong | Fixed protocol (line height, charset, NFC, official splits); CATMuS polygon-fill artefact found and removed; scripted results table; 2 seeds; pass/fail rules written before the runs |
| (our own check) Is the problem real? | The same off-the-shelf OCR gets **52.5%** wrong on medieval CATMuS lines, and medium damage multiplies the baseline's error by up to 7.6 |

</div>

<!-- 0:50 · Say: Two remarks from Review 1. First, accuracy: the baseline is already competitive with an industrial system on clean handwriting, and the same system fails on medieval lines, which is the problem we study. Second, foundations: the checks listed here caught two bugs that would have invalidated results (CATMuS polygon fill; padding attention in the ViT). -->

---

# What is new, and what is not

<div class="t-neutral" style="font-size:17.3px;">

| Not new: we build on it | New: not found in prior work (Oct 2026) |
|---|---|
| SSL for text recognition<br><span class="meta">SeqCLR, Lacuna Reconstruction, LoGo-HTR</span> | Corruptions **fitted to measured statistics** of real damaged lines, through physical damage models |
| Damage-style augmentation in text SSL<br><span class="meta">Text-DIAE</span> | Tests with **whole damage types, media and scripts held out**, on real lines tagged by damage |
| Synthetic document damage<br><span class="meta">Augraphy, PreP-OCR, recto–verso models</span> | Checking whether **measured invariance predicts the error** for each damage type |
| Fitting simulators to real data, in other fields<br><span class="meta">sim-to-real robotics, learned augmentation</span> | The predicted **sign flip**: invariance helps for background damage, hurts for stroke damage |

</div>


<!--
0:45 · Say: (“Not found” is not “proven absent”: the literature search continues through Phase I.) Left column: what already exists and we reuse. Right column: the four things we have not found anywhere. PreP-OCR is the closest on damage, but it sets damage levels by hand and uses them to restore images, not to pretrain a recogniser.
-->

---

# Challenges and how we handle them

<style scoped>table td, table th { padding: 11px 14px !important; font-size: 16px; }</style>

<div class="t-red">

| Challenge | How we handle it |
|---|---|
| SSL may not beat supervised transfer | Always run that baseline; the invariance analysis is a result either way |
| “You only learned your own simulator” | Always also test on real damaged lines, tagged by damage type |
| Some damage has no clean physical model | Model what physics allows (show-through, capture); label the rest as approximate |
| Leaking test data into the fitted damage | Fit damage only on pretraining data; official writer-independent splits |
| Other groups work in this area | Move fast: a workshop paper first, then the full version |

</div>

<!--
0:40 · Say: The template asks for possible shortcomings. These are the five that could sink the project, and what we do about each.
More if asked: few damage families give few points to correlate (we compute invariance per family × severity level); protocols differ across papers (we fix image height, charset and Unicode normalisation on day one).
-->

---

# Objectives

<div class="card" style="gap:10px; padding:22px 28px;">
<ol style="margin:0; padding-left:1.3em; font-size:18px; line-height:1.45; display:flex; flex-direction:column; gap:7px;">
<li>Reproducible line-recognition pipeline and strong supervised baselines <span class="meta">(done)</span></li>
<li>Per-line damage-measurement tool; how real historical lines differ from clean ones <span class="meta">(done)</span></li>
<li>Physical damage models whose frequency and strength are <b>derived</b> from the measurements <span class="meta">(first version done)</span></li>
<li>Masked-autoencoder pretraining with derived damage vs none, plain masking, hand-picked damage and a VICReg control <span class="meta">(RQ1; pilot done, VICReg in Phase 2)</span></li>
<li>Transfer to a held-out damage type, a new medium and an unseen script <span class="meta">(RQ2)</span></li>
<li>Per-damage invariance of every model vs the rise in error <span class="meta">(RQ3; preview done)</span></li>
<li>Release code, fitted damage settings and real lines tagged by damage type</li>
</ol>
</div>

<!-- 0:50 · Say: Seven objectives, the first three finished in Phase 1, the rest are Phase 2 and 3. -->

---

<!-- _class: dense -->

# Literature survey: closest work

<style scoped>table td, table th { padding: 8px 12px !important; font-size: 13.5px; }</style>
<div class="t-neutral">

| Paper | Method | Result | Limitation for us |
|---|---|---|---|
| Garrido-Munoz & Calvo-Zaragoza, NeurIPS 2026 | Six SSL methods, one ViT-B, six HTR sets | MAE best: 5.5% CER (frozen) | Hand-picked augmentation; no damage study |
| Kišš & Hradiš, ICDAR 2024 | Masked pretraining on unlabelled historical lines | Gains; public code | Not always better than supervised transfer |
| Vogler et al. (Lacuna), NAACL Findings 2022 | Masked-region pretraining | CER 60.4% → 23.7% with 30 labels | Not about matching real damage |
| Souibgui et al. (Text-DIAE), AAAI 2023 | Masking, blur and noise pretext tasks | Degradation-invariant features | Degradations hand-picked |
| Ericsson et al., BMVC 2022 | Per-augmentation invariance measure | Tasks need different invariances | Natural images only |
| Guan et al. (PreP-OCR), 2025 | Restoration on synthetic damage, then OCR | Better OCR after restoration | Hand-set damage; not pretraining |

</div>

<!-- 1:00 · Say: Six of the ten papers in the report. The common limitation is the last column: damage and augmentation choices are made by hand, never fitted to real pages. Garrido-Munoz is why we use pixel reconstruction; Kišš & Hradiš is why supervised transfer is a mandatory baseline, and why our own pilot result (no gain yet) is not a surprise. -->

---

# Proposed approach

<div class="cv" style="width:1152px; height:240px; margin-top:16px;">
<img class="sk" src="assets/sketch/loop.svg">
<div class="ov" style="left:16px; width:32px; top:26px;"><div class="k p" style="text-align:center;">1</div></div>
<div class="ov" style="left:56px; width:133px; top:23px;"><div class="h">Measure</div></div>
<div class="ov" style="left:17px; width:171px; top:64px;"><div class="t" style="font-size:18.7px;">contrast, blur, noise, stroke width, bleed on real lines</div></div>
<div class="ov" style="left:253px; width:32px; top:26px;"><div class="k p" style="text-align:center;">2</div></div>
<div class="ov" style="left:293px; width:133px; top:23px;"><div class="h">Model</div></div>
<div class="ov" style="left:255px; width:171px; top:64px;"><div class="t" style="font-size:18.7px;">physical form + fitted parameters</div></div>
<div class="ov" style="left:491px; width:32px; top:26px;"><div class="k p" style="text-align:center;">3</div></div>
<div class="ov" style="left:531px; width:133px; top:23px;"><div class="h">Pretrain</div></div>
<div class="ov" style="left:492px; width:171px; top:64px;"><div class="t" style="font-size:18.7px;">corrupt the input, rebuild the clean line</div></div>
<div class="ov" style="left:728px; width:32px; top:26px;"><div class="k p" style="text-align:center;">4</div></div>
<div class="ov" style="left:768px; width:133px; top:23px;"><div class="h">Evaluate</div></div>
<div class="ov" style="left:729px; width:171px; top:64px;"><div class="t" style="font-size:18.7px;">on held-out damage, media, scripts</div></div>
<div class="ov" style="left:965px; width:32px; top:26px;"><div class="k p" style="text-align:center;">5</div></div>
<div class="ov" style="left:1005px; width:133px; top:23px;"><div class="h">Analyse</div></div>
<div class="ov" style="left:967px; width:171px; top:64px;"><div class="t" style="font-size:18.7px;">does invariance predict the error?</div></div>
<div class="ov" style="left:376px; width:400px; top:187px;"><div style="font-size:18.7px; font-style:italic; color:var(--accent-text); text-align:center;">refine the damage models and repeat</div></div>
</div>

<!--
0:50 · Say: The first loop is deliberately simple: a supervised baseline, then plain masked reconstruction. Each loop adds one thing, chosen by what the last loop showed.
Fixed from the start: the research questions and hypotheses, held-out tests on real damaged lines, strong baselines including supervised transfer, and the reporting protocol (image height, charset).
Decided by evidence, loop by loop: which damage types to model, backbone and model size, masking ratio and corruption strength, label budgets and test conditions.
-->

---

# Expected deliverables

<style scoped>
.drow { display: grid; grid-template-columns: 220px 1fr 270px; gap: 28px; align-items: start; background: var(--card); border: 1px solid var(--edge); border-radius: 12px; padding: 20px 24px; }
.drow h3 { margin-top: 4px; }
.drow ul { display: grid; grid-template-columns: 1fr 1fr; column-gap: 28px; row-gap: 6px; font-size: 16px; margin: 0; }
.drow li { margin: 0; }
.drow .ms { border-left: 3px solid var(--accent); padding-left: 14px; display: flex; flex-direction: column; gap: 4px; }
.drow .ms p { font-size: 15px; color: var(--ink); line-height: 1.4; }
</style>

<div class="col" style="gap:14px;">
<div class="drow"><div><div class="kicker">Phase I</div><div class="meta small">Sep–Dec 2026</div><h3>Foundations</h3></div><ul><li>Literature survey, final formulation</li><li>Data pipeline</li><li>Supervised baseline</li><li>Damage-measurement tool</li><li>First pretraining loop</li></ul><div class="ms"><div class="kicker accent">Milestone</div><p>The first pretraining loop runs end to end.</p></div></div>
<div class="drow"><div><div class="kicker">Phase II</div><div class="meta small">Jan–May 2027</div><h3>Damage models and main runs</h3></div><ul><li>Physical damage models, fitted</li><li>Real lines tagged by damage</li><li>All pretraining runs + control</li><li>Held-out evaluation (RQ1, RQ2)</li></ul><div class="ms"><div class="kicker accent">Milestone</div><p>RQ1 and RQ2 answered on held-out tests.</p></div></div>
<div class="drow"><div><div class="kicker">Phase III</div><div class="meta small">Jun–Dec 2027</div><h3>Analysis and release</h3></div><ul><li>Invariance–error analysis (RQ3)</li><li>Script and medium transfer</li><li>Ablations and seeds</li><li>Paper, code and data release</li></ul><div class="ms"><div class="kicker accent">Milestone</div><p>H3 tested; code, fitted parameters and tagged lines public.</p></div></div>
</div>

<!--
0:50 · Say: Phase I ends with a working baseline and the measurement tool. Phase II delivers the core comparison. Phase III delivers the explanation and the paper (ICDAR workshop first, then the main track or IJDAR).
Success criteria if asked: H1 holds by more than the seed spread; H3's correlation flips sign; a negative H1 still yields the analysis as a finding.
-->

---

<!-- _header: '' -->

![bg](assets/img/gantt.png)

<!--
0:45 · Say: September 2026 to December 2027. Phase I builds the baseline and the measurement tool; Phase II builds and fits the damage models and runs the main comparison; Phase III explains it and writes it up. Months are indicative. Source: gantt.md (edit there, then ./build.sh).
-->

---

# Effort plan (tentative)

<div class="t-neutral">

| Member | Owns | Main tasks | Phases |
|---|---|---|---|
| Arvind Kothamangala | Data and baselines | Data loaders, charset and splits, supervised baseline, CER tooling | I–II |
| Atharv Sawarkar | Damage modelling | Damage-measurement tool, physical damage models, parameter fitting, tagging real lines | I–II |
| Vignesh Nunna | SSL pretraining | Plain, hand-chosen and derived pretraining; VICReg control | I–III |
| Rohit Rajan | Evaluation and analysis | Fine-tuning, held-out tests, invariance scores, transfer experiments | II–III |
| Everyone | Writing and release | Weekly and phase reports, paper, code and data release | I–III |

</div>


<!--
0:30 · Say: Tentative split: each of us owns one workstream end to end (about a quarter of the work each), and writing is shared. The template asks for effort by individuals: this is it, and the Gantt chart shows when each task happens.
-->

---

# Pilot week: what we ran

<div class="grid3">
<div class="card"><div class="kicker">Data</div><ul><li><b>IAM</b>: 6.5k train lines, clean handwriting</li><li><b>CATMuS</b> Latin + French: 23.8k train / 4.0k test real lines, 11 manuscript projects</li><li>CATMuS polygon fill removed (it faked a pre-binarised look)</li></ul></div>
<div class="card"><div class="kicker">Models</div><ul><li><b>CRNN</b> (CNN + BiLSTM + CTC), 7.4M parameters, same settings for every run</li><li><b>ConvMAE</b> pretrains the CRNN's own CNN (34 min, 12k steps), then fine-tune</li><li>Small ViT tried first: memorised the few labels (60–75% CER), set aside</li></ul></div>
<div class="card accent"><div class="kicker accent">Four assumptions, tested</div><ul><li><b>A1</b> damage hurts a clean-trained model</li><li><b>A2</b> real damage differs measurably</li><li><b>A3</b> pretraining beats scratch</li><li><b>A4</b> derived beats hand-picked</li></ul><p class="small meta">Pass/fail rules fixed before the runs.</p></div>
</div>

<!-- 0:50 · Say: A one-week go/no-go. Pass/fail rules were written down before the results, so failures are reported as failures. -->

---

# Baselines: accuracy is achievable, and the gap is real

<style scoped>table td, table th { padding: 10px 14px !important; font-size: 17px; }</style>
<div class="t-neutral">

| Test CER (lower is better) | IAM | CATMuS |
|---|---|---|
| PaddleOCR PP-OCRv6, off the shelf | 11.4% | **52.5%** |
| CRNN, 100% of labels | **9.8%** | 20.0% |
| CRNN, 10% of IAM labels (648 lines) | 19.6% | – |
| CRNN, 5% of CATMuS labels (1,188 lines) | – | 33.6% |
| CRNN, 1% of IAM labels (65 lines) | 43.3% | – |

</div>

<p class="small meta" style="margin-top:14px;">Mean of 2 seeds for low-label rows; seeds differ by at most 0.5 points. CATMuS test = manuscripts not seen in training.</p>

<!-- 0:45 · Say: Left to right: a small model trained in under an hour beats an industrial OCR on clean handwriting, and the industrial OCR gets more than half the characters wrong on medieval lines. With few labels the baseline degrades fast, which is the regime where SSL should help. -->

---

# A1 passes: damage hurts

<div class="row" style="gap:28px; align-items:center;">
<img src="assets/img/pilot/fig_robustness.png" style="width:700px; border-radius:8px; border:1px solid var(--rule);">
<div class="col" style="gap:14px;">
<div class="card accent" style="gap:6px;"><div class="kicker accent">Verdict</div><p>Four of seven damage types at least double the error at medium strength (need 2). <b>PASS</b></p></div>
<div class="card" style="gap:6px;"><p class="small">On real CATMuS lines, the most faded quartile is <b>1.35–1.47×</b> worse than the least faded. Paper level, noise and unevenness: no clear effect.</p></div>
</div>
</div>

<!-- 0:45 · Say: Synthetic damage on clean IAM test lines, full-label CRNN. Ink loss, noise, tone and blur break it; show-through, fading and stains barely do. On real lines, low contrast is the damage that tracks the error. Sharpness goes the opposite way; we think it is confounded with stroke width and do not claim anything from it. -->

---

# A2 fails: real damage differs, but only in tone and show-through

<img src="assets/img/pilot/fig1_stats_iam_vs_catmus.png" style="width:1152px; border-radius:8px; border:1px solid var(--rule);">

<p class="small" style="margin-top:10px;">Rule fixed in advance: at least 3 of the damage statistics with KS distance ≥ 0.5. Only <b>paper level (0.82)</b> and <b>faint grey (0.84)</b> reach it, so A2 <b>fails</b>. Stroke width and ink fraction differ too, but that is scale, not damage.</p>

<!-- 0:45 · Say: Distributions of eight per-line statistics, clean IAM outline vs real CATMuS fill. The real manuscripts are darker and show more show-through; contrast, sharpness and noise overlap with clean handwriting. By our own rule this is a fail, and the derived recipe reflects it: tone 84% and show-through 89% of lines, noise 11%, blur 5%. -->

---

# A3 fails, A4 passes: pretraining does not help yet

<style scoped>table td, table th { padding: 10px 14px !important; font-size: 16.5px; }</style>
<div class="t-neutral">

| Test CER, mean of 2 seeds | No pretraining | Masking only | + hand-picked damage | + derived damage |
|---|---|---|---|---|
| CATMuS, 5% labels | 33.6% | 33.3% | 35.0% | 33.4% |
| IAM, 10% labels | 19.6% | 20.4% | 21.0% | 20.5% |
| IAM, 1% labels | 43.3% | 43.8% | 44.7% | 43.9% |

</div>

<div class="grid2 mt2">
<div class="card red" style="gap:6px;"><div class="kicker">A3: FAIL</div><p class="small">No pretrained variant beats scratch by more than the seed spread (about 0.5 points).</p></div>
<div class="card green" style="gap:6px;"><div class="kicker green">A4: PASS, but read with care</div><p class="small">Derived ≤ hand-picked in 3 of 3 settings, yet derived ≈ masking only: hand-picked damage <b>hurts</b>, derived damage does <b>no harm</b>.</p></div>
</div>

<!-- 0:50 · Say: Same CRNN, same fine-tuning, only the CNN's initialisation differs. Pretraining here is 30k lines and 34 minutes, far smaller than the published work, and Kišš and Hradiš also report that target-domain SSL does not always beat plain supervised training. This is the main risk, stated honestly. Planned fixes: longer and larger pretraining, freeze-then-unfreeze, lower fine-tune rate, a 30-label budget. -->

---

# RQ3 preview: invariance predicts the error rise

<div class="row" style="gap:28px; align-items:center;">
<img src="assets/img/pilot/fig_invariance_vs_cer.png" style="width:640px; border-radius:8px; border:1px solid var(--rule);">
<div class="col" style="gap:14px;">
<div class="card accent" style="gap:6px;"><div class="kicker accent">Strongest pilot result</div><p>Spearman ρ between measured invariance and CER rise is <b>−0.92</b> (21 damage settings) and between <b>−0.78 and −0.95</b> in all nine trained models.</p></div>
<div class="card" style="gap:6px;"><p class="small">It holds inside the "damage overlaps characters" and "paper only" groups separately. So far: one dataset, synthetic damage only.</p></div>
</div>
</div>

<!-- 0:45 · Say: Invariance is the cosine similarity of the encoder's features for a clean line and its damaged copy. The less the encoder ignores a damage, the more that damage raises the error. This is the first evidence for RQ3 and it does not depend on pretraining helping. Caveat: the H3 sign flip (invariance helps for paper damage, hurts for stroke damage) cannot be tested until we have models trained to be invariant. -->

---

# Conclusion

<div class="grid2">
<div class="card white" style="gap:8px;"><div class="kicker">Phase 1 delivered</div><ul class="small"><li>Literature survey and formulation, re-checked in Nov 2026</li><li>Clean data pipeline for IAM and CATMuS</li><li>Supervised baselines: 9.8% IAM, 20.0% CATMuS</li><li>Damage-measurement tool, 7 damage models, derived recipe v0</li><li>First pretraining loop, end to end</li></ul></div>
<div class="card accent" style="gap:8px;"><div class="kicker accent">What the pilot says</div><ul class="small"><li><b>A1 pass:</b> damage hurts; <b>A2 fail:</b> real damage differs mainly in tone and show-through</li><li><b>A3 fail:</b> no gain from pretraining yet at 30k lines / 34 min</li><li><b>A4 pass:</b> hand-picked damage hurts, derived does no harm</li><li><b>RQ3:</b> invariance predicts error rise, ρ ≈ −0.9</li></ul></div>
</div>
<div class="band white mt"><p><b>Phase 2:</b> larger and longer pretraining with freeze-then-unfreeze, fitted physical damage models, tagged real test lines, held-out evaluation and VICReg control.</p></div>

<!-- 0:40 · Say: Phase 1 is complete. The pilot gives one positive and strong result (invariance predicts error), supports the motivation, and tells us honestly that pretraining at small scale does not yet pay off. -->

---

<!-- _class: dense -->

# References

<div class="refs">
<div><span>1</span><span>Garrido-Munoz &amp; Calvo-Zaragoza. <a href="https://arxiv.org/abs/2609.35473"><i>Handwritten Text Recognition Lives in the High-Pixel Variance Subspace.</i></a> arXiv:2609.35473, 2026.</span></div>
<div><span>2</span><span>Penarrubia, Valero-Mas &amp; Calvo-Zaragoza. <a href="https://arxiv.org/abs/2407.19889"><i>Self-Supervised Learning for Text Recognition: A Critical Survey.</i></a> IJCV, 2025.</span></div>
<div><span>3</span><span>Kišš &amp; Hradiš. <a href="https://arxiv.org/abs/2405.00420"><i>Self-supervised Pre-training of Text Recognizers.</i></a> ICDAR, 2024.</span></div>
<div><span>4</span><span>Vogler et al. <a href="https://arxiv.org/abs/2112.08692"><i>Lacuna Reconstruction: Self-Supervised Pre-Training for Low-Resource Historical Document Transcription.</i></a> Findings of NAACL, 2022.</span></div>
<div><span>5</span><span>Souibgui et al. <a href="https://arxiv.org/abs/2203.04814"><i>Text-DIAE: A Self-Supervised Degradation Invariant Autoencoder for Text Recognition and Document Enhancement.</i></a> AAAI, 2023.</span></div>
<div><span>6</span><span>Ericsson, Gouk &amp; Hospedales. <a href="https://arxiv.org/abs/2111.11398"><i>Why Do Self-Supervised Models Transfer? Investigating the Impact of Invariance on Downstream Tasks.</i></a> BMVC, 2022.</span></div>
<div><span>7</span><span>Mintun, Kirillov &amp; Xie. <a href="https://arxiv.org/abs/2102.11273"><i>On Interaction Between Augmentations and Corruptions in Natural Corruption Robustness.</i></a> NeurIPS, 2021.</span></div>
<div><span>8</span><span>Mitra, Mondal &amp; Jawahar. <a href="https://openaccess.thecvf.com/content/WACV2026/html/Mitra_Learning_Beyond_Labels_Self-Supervised_Handwritten_Text_Recognition_WACV_2026_paper.html"><i>Learning Beyond Labels: Self-Supervised Handwritten Text Recognition (LoGo-HTR).</i></a> WACV, 2026.</span></div>
<div><span>9</span><span>Guan et al. <a href="https://arxiv.org/abs/2505.20429"><i>PreP-OCR: A Complete Pipeline for Document Image Restoration and Enhanced OCR Accuracy.</i></a> arXiv:2505.20429, 2025.</span></div>
<div><span>10</span><span>He et al. <a href="https://arxiv.org/abs/2111.06377"><i>Masked Autoencoders Are Scalable Vision Learners.</i></a> CVPR, 2022.</span></div>
<div><span>11</span><span>Shi, Bai &amp; Yao. <a href="https://arxiv.org/abs/1507.05717"><i>An End-to-End Trainable Neural Network for Image-based Sequence Recognition (CRNN).</i></a> TPAMI, 2017.</span></div>
<div><span>12</span><span>Clérice et al. <a href="https://doi.org/10.1007/978-3-031-70543-4_11"><i>CATMuS Medieval: a multilingual large-scale cross-century dataset in Latin script for HTR.</i></a> ICDAR, 2024.</span></div>
<div><span>13</span><span>Marti &amp; Bunke. <a href="https://doi.org/10.1007/s100320200071"><i>The IAM-database: an English sentence database for offline handwriting recognition.</i></a> IJDAR, 2002.</span></div>
<div><span>14</span><span>Li et al. <a href="https://github.com/PaddlePaddle/PaddleOCR"><i>PaddleOCR (PP-OCRv6).</i></a> PaddlePaddle.</span></div>
<div><span>15</span><span>Groleau et al. <a href="https://arxiv.org/abs/2208.14558"><i>Augraphy: A Data Augmentation Library for Document Images.</i></a> arXiv:2208.14558, 2022.</span></div>
</div>

---

<!-- _class: dark -->

<div class="col" style="height:100%; justify-content:center;">
<div class="col" style="gap:16px;">
<h1 style="font-size:96px;">Thank you</h1>
</div>
</div>
