---
marp: true
theme: lwti
size: 16:9
paginate: false
header: '![PES](assets/pes_emblem.png)'
title: "Learning What to Ignore: Deriving Invariance for Self-Supervised Text Recognition"
description: "UE24CS320A Capstone Project Approval"
---

<!-- _header: '' -->
<!-- _backgroundColor: '#ffffff' -->

<img src="assets/img/guide_approval.png" style="position:absolute; left:80px; top:103px; width:1120px; height:513px; border:1px solid #D9DCE1; border-radius:8px; box-shadow:0 4px 18px rgba(0,0,0,.08);">
<img src="assets/img/guide_approval_details.png" style="position:absolute; left:560px; top:208px; width:600px; height:233px; border:1px solid #C9CDD3; border-radius:8px; box-shadow:0 8px 28px rgba(0,0,0,.18);">

<!--
Guide's approval: Dr. Chavan approved this presentation by email on 14 October 2026.
-->

---

<!-- _class: dark -->

<div class="row" style="gap:64px; height:100%;">
<div class="col" style="flex:0 0 581px; justify-content:flex-start;">
<div class="col" style="gap:20px;">
<div class="eyebrow" style="text-transform:none; margin-bottom:36px;">UE24CS320A · Capstone Project Approval</div>
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
0:15 · Say: We want a text recogniser that learns from unlabelled pages which kinds of damage to ignore, with that choice derived from real documents instead of hand-picked.
Image: a damaged medieval manuscript page (British Museum collection; add the exact source).
-->

---

<!-- _class: dark -->

<div class="row" style="height:100%; align-items:center; gap:64px;">
<h1 style="flex:0 0 420px;">Outline</h1>
<ol class="outline">
<li><span class="n">01</span><span class="s">Landscape</span></li>
<li><span class="n">02</span><span class="s">Problem</span></li>
<li><span class="n">03</span><span class="s">Background</span></li>
<li><span class="n">04</span><span class="s">Approach</span></li>
<li><span class="n">05</span><span class="s">Deliverables</span></li>
</ol>
</div>

<!-- 0:10 · Say: Five parts: how OCR and self-supervised learning work today, the problem, the work it builds on, our approach, and what we will deliver. -->

---

<!-- _class: dark divider -->

# Landscape

<!-- 0:05 -->

---

# How OCR works (the general pipeline)

<div class="cv" style="width:1152px; height:130px;">
<img class="sk" src="assets/sketch/ocr_pipeline_general.svg">
<div class="ov" style="left:2px; width:88px; top:52px;"><div class="b">Image</div></div>
<div class="ov" style="left:1062px; width:88px; top:52px;"><div class="b">Text</div></div>
<div class="ov box" style="left:128px; width:152px; top:6px; height:118px; justify-content:center; padding:0 14px; box-sizing:border-box;"><div class="k">Stage 1</div><div class="h">Acquisition &amp; pre-processing</div></div>
<div class="ov box" style="left:314px; width:152px; top:6px; height:118px; justify-content:center; padding:0 14px; box-sizing:border-box;"><div class="k">Stage 2</div><div class="h">Layout analysis</div></div>
<div class="ov box" style="left:500px; width:152px; top:6px; height:118px; justify-content:center; padding:0 14px; box-sizing:border-box;"><div class="k">Stage 3</div><div class="h">Text detection</div></div>
<div class="ov box" style="left:686px; width:152px; top:6px; height:118px; justify-content:center; padding:0 14px; box-sizing:border-box;"><div class="k p">Stage 4</div><div class="h">Text recognition</div></div>
<div class="ov box" style="left:872px; width:152px; top:6px; height:118px; justify-content:center; padding:0 14px; box-sizing:border-box;"><div class="k">Stage 5</div><div class="h">Post-processing</div></div>
</div>

<style scoped>.stg { display: grid; grid-template-columns: 112px repeat(5, 182px); column-gap: 4px; margin-top: 22px; } .stg img { width: 182px; height: 217px; object-fit: contain; background: #FFFFFF; border: 1px solid var(--edge); border-radius: 6px; display: block; }</style>

<div class="stg"><div></div><img src="assets/img/ocr_stages/1_preprocess.png"><img src="assets/img/ocr_stages/2_layout.png"><img src="assets/img/ocr_stages/3_detection.png"><img src="assets/img/ocr_stages/4_recognition.png"><img src="assets/img/ocr_stages/5_postprocess.png"></div>

<!--
0:50 · Say: Every OCR system does these five jobs. Scan and clean the image, find the layout, detect where the text is, recognise it, then fix likely mistakes with a dictionary or language model. Classic systems fight damage in stage 1, by cleaning the image first. We work only on stage 4, recognition, and teach it to see through damage instead; the other stages stay fixed so their errors never enter our comparison.
The images are one receipt run through PaddleOCR 3.7 on our laptop GPU: (1) a simulated phone photo of it, straightened by the document preprocessor (orientation + UVDoc unwarping); (2) layout blocks from PP-DocLayout; (3) line boxes from PP-OCRv6 detection; (4) line crops read by PP-OCRv6 recognition; (5) the text turned into fields with simple rules, plus a check that subtotal + tax = total. Stage 5's rules are ours; PaddleOCR stops at the text. Script: deck/tools/ocr_stage_images.py.
Sources: Chacko & Dhanya (IJAIA 2014); Dive into OCR (PaddlePaddle, 2022). Modern systems merge some stages: VLMs read whole pages end to end.
-->

---
# Inside text recognition: four stages

<style scoped>.alg { font-size: 16px; line-height: 24px; color: var(--ink); white-space: nowrap; } .alg.h { font-weight: 700; }</style>

<div class="cv" style="width:1152px; height:340px;">
<img class="sk" src="assets/sketch/recognition_stages.svg">
<div class="ov box" style="left:2px; width:240px; top:4px; height:140px; justify-content:center; padding:0 18px; box-sizing:border-box;"><div class="k">Stage 1</div><div class="h">Transformation</div><div class="t">Straighten curved or slanted text.</div></div>
<div class="ov box" style="left:306px; width:240px; top:4px; height:140px; justify-content:center; padding:0 18px; box-sizing:border-box;"><div class="k">Stage 2</div><div class="h">Feature extraction</div><div class="t">Turn the image into visual features.</div></div>
<div class="ov box" style="left:610px; width:240px; top:4px; height:140px; justify-content:center; padding:0 18px; box-sizing:border-box;"><div class="k">Stage 3</div><div class="h">Sequence modelling</div><div class="t">Add context along the line.</div></div>
<div class="ov box" style="left:914px; width:240px; top:4px; height:140px; justify-content:center; padding:0 18px; box-sizing:border-box;"><div class="k">Stage 4</div><div class="h">Prediction</div><div class="t">Turn features into characters.</div></div>
<div class="ov" style="left:66px; top:178px;"><div class="alg">TPS (thin-plate spline)</div></div>
<div class="ov" style="left:66px; top:220px;"><div class="alg">STN (spatial transformer)</div></div>
<div class="ov" style="left:370px; top:178px;"><div class="alg">VGG</div></div>
<div class="ov" style="left:370px; top:220px;"><div class="alg">ResNet</div></div>
<div class="ov" style="left:370px; top:262px;"><div class="alg">ViT</div></div>
<div class="ov" style="left:674px; top:178px;"><div class="alg">BiLSTM</div></div>
<div class="ov" style="left:674px; top:220px;"><div class="alg">Transformer</div></div>
<div class="ov" style="left:962px; top:178px;"><div class="alg h">CTC</div></div>
<div class="ov" style="left:974px; top:220px;"><div class="alg">CRNN</div></div>
<div class="ov" style="left:974px; top:262px;"><div class="alg">Rosetta</div></div>
<div class="ov" style="left:1070px; top:178px;"><div class="alg h">Attention</div></div>
<div class="ov" style="left:1082px; top:220px;"><div class="alg">RARE</div></div>
<div class="ov" style="left:1082px; top:262px;"><div class="alg">SAR</div></div>
<div class="ov" style="left:1082px; top:304px;"><div class="alg">PARSeq</div></div>
</div>

<style scoped>.arch { display: grid; grid-template-columns: repeat(4, 240px); column-gap: 64px; margin-top: 10px; } .arch > div { height: 200px; display: flex; flex-direction: column; gap: 8px; } .arch img { flex: 1 1 0; min-height: 0; width: 100%; object-fit: contain; background: #FFFFFF; border: 1px solid var(--edge); border-radius: 6px; padding: 6px; box-sizing: border-box; display: block; }</style>

<div class="arch">
<div><img src="assets/img/stn-arch.png"></div>
<div><img src="assets/img/vit.png"></div>
<div><img src="assets/img/bilstm.png"></div>
<div><img src="assets/img/crnn-arch.jpg"><img src="assets/img/parseq-arch.png"></div>
</div>

<!--
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
-->

---
# Self-supervised learning

<style scoped>
.step { display: grid; grid-template-columns: 34px 1fr; column-gap: 12px; row-gap: 6px; align-items: center; }
.step .num { width: 30px; height: 30px; border-radius: 50%; background: var(--accent-fill); border: 2px solid var(--accent-edge); color: var(--accent-text); font-family: var(--mono); font-weight: 600; font-size: 14px; display: flex; align-items: center; justify-content: center; }
.step img { grid-column: 2; width: 100%; height: 50px; object-fit: cover; object-position: left center; border-radius: 6px; border: 1px solid var(--edge); display: block; }
</style>

<div class="row" style="gap:40px; align-items:center;">
<div class="col" style="flex:0 0 640px; gap:18px;">
<p style="font-size:20px; line-height:1.45; color:var(--ink);"><b>Self-supervised learning (SSL)</b> lets a model learn from data nobody has labelled. Hide part of each input and train the model to predict it; the original input is the answer, so no human labelling is needed.</p>
<div class="step"><span class="num">1</span><p><b>Hide.</b> Mask out most of a text line (MAE hides about 75% of the image patches).</p><img src="assets/img/ssl_masked_line.png"></div>
<div class="step"><span class="num">2</span><p><b>Rebuild.</b> An encoder reads what is left and a small decoder redraws the missing patches; the difference from the original line is the training signal.</p><img src="assets/damage/clean.png"></div>
<div class="step"><span class="num">3</span><p><b>Reuse.</b> Drop the decoder, keep the encoder, and fine-tune it on a few hundred labelled lines to make it read.</p></div>
<p class="meta"><b>Why it works:</b> to fill in a missing stroke, the model has to learn what letters, ink and paper look like, which is exactly what a recogniser needs. The same idea trains GPT (predict the next word) and BERT (fill in hidden words).</p>
</div>
<img class="photo" src="assets/img/welch_cake_7-29.jpg" style="flex:1 1 auto; min-width:0;">
</div>

<!--
1:00 · Say: Labels are expensive: every training line needs a person to type it out. SSL makes the labels from the data itself. Hide most of a line, have the model redraw it, and check against the original. To do that, it has to learn what letters and strokes look like. Then a few labelled lines are enough to teach it to read.
LeCun's cake: most of what a model learns comes from the data itself (the cake), a little from labels (the icing), a tiny bit from rewards (the cherry). That's why SSL matters where labels are scarce, like damaged historical documents.
Image: screenshot from Welch Labs, "Yann LeCun's Billion Dollar Bet" (7:29); the cake is from LeCun's NIPS 2016 keynote.
-->

---
<div class="col" style="align-items:center;">
<img class="photo" src="assets/img/welch_ssl_timeline_1-51.jpg" style="width:1040px; height:585px;">
</div>

<!--
0:45 · Say: The family tree of self-supervised learning. Siamese networks (1993) → contrastive methods (SimCLR, MoCo) → non-contrastive (BYOL, Barlow Twins, VICReg) → latent prediction (JEPA). Point to "Pixel Level Generative Models" (top middle): MAE sits on this branch because it rebuilds the input pixels themselves; that is our family. Point to VicReg (bottom row): VICReg is our control. A September 2026 paper showed that for handwriting, rebuilding pixels beats contrastive and JEPA, which is why we chose this branch.
Image: screenshot from Welch Labs, "Yann LeCun's Billion Dollar Bet" (1:51).
-->

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

<!-- _class: dark divider -->

# Problem

<!-- 0:05 -->

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

# Today vs this project

<div class="cv" style="width:1152px; height:350px; margin-top:24px;">
<img class="sk" src="assets/sketch/today_vs_project.svg">
<div class="ov" style="left:0; width:160px; top:64px;"><div class="k">Today</div></div>
<div class="ov" style="left:0; width:160px; top:264px;"><div class="k p">This project</div></div>
<div class="ov box" style="left:176px; width:216px; top:10px; height:130px; justify-content:center; padding:0 16px; box-sizing:border-box;"><div class="bt">Pick corruptions</div><div class="bi">by hand and trial: “blur 0.5–2 px, mask 75%”</div></div>
<div class="ov box" style="left:428px; width:216px; top:10px; height:130px; justify-content:center; padding:0 16px; box-sizing:border-box;"><div class="bt">Pretrain</div><div class="bi">on unlabelled lines</div></div>
<div class="ov box" style="left:680px; width:216px; top:10px; height:130px; justify-content:center; padding:0 16px; box-sizing:border-box;"><div class="bt">Fine-tune</div><div class="bi">on a few labelled lines</div></div>
<div class="ov box" style="left:932px; width:216px; top:10px; height:130px; justify-content:center; padding:0 16px; box-sizing:border-box;"><div class="bt">Hope it transfers</div><div class="bi">if not, re-tune for the next collection</div></div>
<div class="ov box" style="left:176px; width:216px; top:210px; height:130px; justify-content:center; padding:0 16px; box-sizing:border-box;"><div class="bt">Measure</div><div class="bi">the damage on real historical lines</div></div>
<div class="ov box" style="left:428px; width:216px; top:210px; height:130px; justify-content:center; padding:0 16px; box-sizing:border-box;"><div class="bt">Model + fit</div><div class="bi">physical damage models, fitted to those measurements</div></div>
<div class="ov box" style="left:680px; width:216px; top:210px; height:130px; justify-content:center; padding:0 16px; box-sizing:border-box;"><div class="bt">Pretrain</div><div class="bi">rebuild clean lines from damaged ones</div></div>
<div class="ov box" style="left:932px; width:216px; top:210px; height:130px; justify-content:center; padding:0 16px; box-sizing:border-box;"><div class="bt">Test + explain</div><div class="bi">on unseen damage; does invariance predict the error?</div></div>
</div>

<!--
0:50 · Say: Today the corruption recipe is a guess, and we hope it transfers. Here it is measured on real pages, modelled, fitted, and then tested on damage the model never saw.
Images you could show while presenting: a real line with bleed-through next to its fitted synthetic version; a screenshot of a typical hand-chosen augmentation list from a paper's appendix.
-->

---

# Research questions

<div class="grid3">
<div class="card white-accent" style="gap:10px;">
<div class="hd" style="align-items:baseline;"><span class="badge accent">RQ1</span><h3 style="font-size:22px;">Does it help?</h3></div>
<p>Do physics-derived, data-fitted corruptions beat plain masking and hand-chosen corruptions?</p>
<div class="grow"></div>
<div class="cv" style="width:330px; height:240px;"><img class="sk" src="assets/sketch/rq1.svg">
<div class="ov" style="left:46px; width:270px; top:2px;"><div class="ax">error with few labels</div></div>
<div class="ov" style="left:258px; width:24px; top:62px;"><div class="q">?</div></div>
<div class="ov" style="left:48px; width:88px; top:178px;"><div class="lb">Plain</div></div>
<div class="ov" style="left:126px; width:108px; top:178px;"><div class="lb">Hand-chosen</div></div>
<div class="ov" style="left:224px; width:88px; top:178px;"><div class="lb p">Derived</div></div>
</div>
</div>
<div class="card white-accent" style="gap:10px;">
<div class="hd" style="align-items:baseline;"><span class="badge accent">RQ2</span><h3 style="font-size:22px;">What transfers?</h3></div>
<p>Which invariances survive when a damage type, medium, script or capture condition is held out?</p>
<div class="grow"></div>
<div class="cv" style="width:330px; height:240px;"><img class="sk" src="assets/sketch/rq2.svg">
<div class="ov" style="left:46px; width:270px; top:2px;"><div class="ax">how much transfers</div></div>
<div class="ov" style="left:48px; width:88px; top:178px;"><div class="lb">Damage</div></div>
<div class="ov" style="left:136px; width:88px; top:178px;"><div class="lb">Medium</div></div>
<div class="ov" style="left:224px; width:88px; top:178px;"><div class="lb">Script</div></div>
<div class="ov" style="left:44px; width:280px; top:214px;"><div class="ax">held out: farther from what we fitted</div></div>
</div>
</div>
<div class="card white-accent" style="gap:10px;">
<div class="hd" style="align-items:baseline;"><span class="badge accent">RQ3</span><h3 style="font-size:22px;">What governs the match?</h3></div>
<p>Does measured invariance predict how much the error rises under each damage type?</p>
<div class="grow"></div>
<div class="cv" style="width:330px; height:240px;"><img class="sk" src="assets/sketch/rq3.svg">
<div class="ov" style="left:46px; width:200px; top:2px;"><div class="ax">error rise</div></div>
<div class="ov" style="left:296px; width:24px; top:14px;"><div class="q">?</div></div>
<div class="ov" style="left:120px; width:200px; top:178px;"><div class="ax" style="text-align:right;">invariance score →</div></div>
</div>
</div>
</div>

<!--
0:50 · Say: Three questions: does it help, what transfers, and can we predict the cost of a damage type before we see it. RQ3 is what makes this more than a leaderboard result. The sketches show what each question measures; they are not results.
-->

---

# Falsifiable hypotheses

<div class="row" style="gap:16px; flex:0 1 auto; height:520px;">
<div class="col" style="flex:0 0 467px; gap:12px;">
<div class="card grow" style="gap:6px; padding:16px 18px;"><div class="hd"><span class="badge accent">H1</span><h3 style="font-size:18.7px;">Derived corruptions win</h3></div><p>With few labels, they beat plain masking and hand-chosen corruptions on real historical lines.</p><p><span class="wrong">Wrong if:</span> the gap is within seed-to-seed spread.</p></div>
<div class="card grow" style="gap:6px; padding:16px 18px;"><div class="hd"><span class="badge accent">H2</span><h3 style="font-size:18.7px;">Closer conditions transfer better</h3></div><p>Gains shrink as tests move away from what we fitted: new damage type, then medium, then script.</p><p><span class="wrong">Wrong if:</span> new scripts transfer as well as new damage.</p></div>
<div class="card grow" style="gap:6px; padding:16px 18px;"><div class="hd"><span class="badge accent">H4</span><h3 style="font-size:18.7px;">Control: reconstruction beats VICReg</h3></div><p>VICReg trained on the same damage does worse than our model.</p><p><span class="wrong">Wrong if:</span> VICReg matches or beats it.</p></div>
</div>
<div class="card white-accent" style="gap:10px;">
<div class="hd"><span class="badge accent">H3</span><h3 style="font-size:24px;">The sign flip</h3></div>
<p>Learning to ignore damage should <span class="p">help</span> when the damage sits on the background, and <span class="wrong">hurt</span> when it changes the strokes themselves.</p>
<div class="grow"></div>
<div class="row" style="gap:12px; justify-content:space-between;">
<div class="cv" style="width:305px; height:227px; flex:none;"><img class="sk" src="assets/sketch/h3_help.svg">
<div class="ov" style="left:0; width:305px; top:0;"><div style="font-size:18.7px; font-weight:600; color:var(--ink);">Background damage</div></div>
<div class="ov" style="left:0; width:305px; top:27px;"><div class="ax">(bleed-through, stains, blur)</div></div>
<div class="ov" style="left:28px; width:133px; top:57px;"><div class="ax">error rise</div></div>
<div class="ov" style="left:193px; width:80px; top:99px;"><div style="font-size:18.7px; font-weight:600; color:var(--accent-text);">help</div></div>
<div class="ov" style="left:133px; width:160px; top:200px;"><div class="ax" style="text-align:right;">more invariance →</div></div>
</div>
<div class="cv" style="width:305px; height:227px; flex:none;"><img class="sk" src="assets/sketch/h3_hurt.svg">
<div class="ov" style="left:0; width:305px; top:0;"><div style="font-size:18.7px; font-weight:600; color:var(--ink);">Stroke damage</div></div>
<div class="ov" style="left:0; width:305px; top:27px;"><div class="ax">(ink loss, merged strokes, lost diacritics)</div></div>
<div class="ov" style="left:28px; width:133px; top:57px;"><div class="ax">error rise</div></div>
<div class="ov" style="left:193px; width:80px; top:141px;"><div style="font-size:18.7px; font-weight:600; color:var(--red-text);">hurt</div></div>
<div class="ov" style="left:133px; width:160px; top:200px;"><div class="ax" style="text-align:right;">more invariance →</div></div>
</div>
</div>
<div class="grow"></div>
<p><span class="wrong">Wrong if:</span> every damage type shows the same trend, or none shows a trend.</p>
</div>
</div>

<img class="float" src="assets/sketch/h3_arrow.svg" style="left:824px; top:150px; width:133px; height:33px;">
<div class="float hand" style="left:964px; top:153px; width:227px; transform:rotate(-3deg);">the interesting one</div>

<!--
Full wording if asked:
| H1 | Derived corruptions lower CER on real historical lines at the smallest label budget, compared with both plain MAE and hand-chosen corruptions | The gap is within seed spread, or hand-chosen corruptions match it |
| H2 | Transfer shrinks as conditions move away from what was fitted: held-out damage > medium > script | Script transfer equals or beats damage transfer |
| H3 | Invariance helps when a damage type leaves the character-carrying pixels alone, and hurts when it overlaps them (ink loss, merged strokes, diacritics): a sign flip between the two groups | One monotone relationship across all families, or no correlation |
| H4 (control) | A joint-embedding model (VICReg) trained on the same derived damage loses to derived-corruption MAE, reproducing arXiv 2609.35473 at small scale | VICReg matches or wins, so the reconstruction choice needs rethinking |

0:55 · Say: Each hypothesis says in advance what would prove us wrong. H3 is the interesting one: the same invariance should help for background damage and hurt when the damage hits the letters.
-->

---

<!-- _class: dark divider -->

# Background

<!-- 0:05 -->

---
# How the field got here

<div class="tl">
<div class="col"><div class="y">2021</div><div class="dot"></div>
<div class="box"><div class="nm">SeqCLR</div><div class="vn">CVPR</div><div class="ln">First contrastive SSL for text recognition.</div></div>
<div class="box"><div class="nm">Mintun et al.</div><div class="vn">NeurIPS</div><div class="ln">Augmentations that resemble the test damage give robustness (natural images).</div></div>
</div>
<div class="col"><div class="y">2022</div><div class="dot"></div>
<div class="box"><div class="nm">Lacuna Reconstruction</div><div class="vn">NAACL Findings</div><div class="ln">Masked SSL on historical lines: 30 labels, CER 60.4 → 23.7.</div></div>
<div class="box"><div class="nm">Ericsson et al.</div><div class="vn">BMVC</div><div class="ln">Different tasks need different invariances.</div></div>
</div>
<div class="col"><div class="y">2023</div><div class="dot"></div>
<div class="box"><div class="nm">Text-DIAE</div><div class="vn">AAAI</div><div class="ln">Learns to undo degradations, but they are hand-chosen.</div></div>
</div>
<div class="col"><div class="y">2024</div><div class="dot"></div>
<div class="box"><div class="nm">Kišš &amp; Hradiš</div><div class="vn">ICDAR</div><div class="ln">SSL on historical lines is not always better than supervised transfer.</div></div>
</div>
<div class="col"><div class="y">2025</div><div class="dot"></div>
<div class="box"><div class="nm">Penarrubia et al.</div><div class="vn">IJCV survey</div><div class="ln">Augmentations are still chosen by hand.</div></div>
<div class="box"><div class="nm">PreP-OCR</div><div class="vn">arXiv</div><div class="ln">Restore the page, then OCR; damage levels set by hand.</div></div>
</div>
<div class="col"><div class="y">2026</div><div class="dot"></div>
<div class="box"><div class="nm">LoGo-HTR</div><div class="vn">WACV</div><div class="ln">Contrastive SSL on 10M handwritten words; no damage modelling.</div></div>
<div class="box"><div class="nm">Garrido-Munoz &amp; Calvo-Zaragoza</div><div class="vn">arXiv · Sept</div><div class="ln">Rebuilding pixels beats contrastive and JEPA for HTR.</div></div>
</div>
</div>

<!--
1:00 · Say: SSL for text grew from contrastive methods to masked reconstruction, and in Sept 2026 pixel reconstruction was shown to win for handwriting; but the corruptions are still hand-picked (the survey). Document damage is simulated or removed before OCR (PreP-OCR), never fitted to real pages for pretraining. Mintun and Ericsson show that what a model ignores decides what it is good at, but only on natural images. Nobody has joined these for text: that is our gap.
Also relevant: Baloun et al. (IJDAR 2025) compare augmentations by trial for page segmentation; Augraphy (2022) simulates document damage.
-->

---
# Key papers at a glance

<div class="thumbs">
<div class="thumb"><img src="assets/img/papers/lacuna.png"><div><div class="yr">2022</div><div class="nm">Lacuna Reconstruction</div><div class="vn">NAACL Findings</div><p>Masked SSL works on historical lines: 30 labelled lines take error from 60% to 24%.</p></div></div>
<div class="thumb"><img src="assets/img/papers/ericsson.png"><div><div class="yr">2022</div><div class="nm">Ericsson et al.</div><div class="vn">BMVC</div><p>How to measure what a model ignores; our tool for RQ3.</p></div></div>
<div class="thumb"><img src="assets/img/papers/textdiae.png"><div><div class="yr">2023</div><div class="nm">Text-DIAE</div><div class="vn">AAAI</div><p>SSL that undoes degradations, but the degradations are hand-chosen.</p></div></div>
<div class="thumb"><img src="assets/img/papers/kiss.png"><div><div class="yr">2024</div><div class="nm">Kišš &amp; Hradiš</div><div class="vn">ICDAR</div><p>SSL on historical lines with public code (our starting point) and an honest supervised baseline.</p></div></div>
<div class="thumb"><img src="assets/img/papers/prepocr.png"><div><div class="yr">2025</div><div class="nm">PreP-OCR</div><div class="vn">arXiv</div><p>Models document damage to restore pages before OCR; damage levels set by hand.</p></div></div>
<div class="thumb"><img src="assets/img/papers/garrido.png"><div><div class="yr">2026</div><div class="nm">Garrido-Munoz &amp; Calvo-Zaragoza</div><div class="vn">arXiv</div><p>Rebuilding pixels beats contrastive and JEPA for handwriting: why we use reconstruction.</p></div></div>
</div>

<!--
0:45 · Say: The six papers this project stands on. Lacuna shows SSL works on historical lines; Ericsson gives us the way to measure invariance; Text-DIAE and PreP-OCR model damage, but by hand; Kišš & Hradiš give us code and the baseline to beat; Garrido-Munoz tells us to rebuild pixels. None of them fits the damage to real pages.
-->

---
<!-- _class: dense -->

# Why pixels matter for text

<div class="grid2">
<div class="card"><div class="kicker">The argument against pixels</div><p>LeCun’s case for JEPA: predicting raw pixels wastes effort on unpredictable detail (blurry generated video), so models should predict in feature space instead.</p><img class="photo" src="assets/img/welch_blurry_11-20.jpg" style="height:190px;"></div>
<div class="card accent"><div class="kicker accent">Why text is different</div><p>In handwriting the “detail” <b>is</b> the signal: one dot or stroke decides the letter. The signal lives in high-variance pixel directions, and only pixel reconstruction kept per-character position (Garrido-Munoz &amp; Calvo-Zaragoza, 2026).</p><img class="photo" src="assets/img/manuscript_handwriting.jpg" style="height:190px; object-position:50% 20%;"></div>
</div>
<div class="band accent mt"><p>So we use <b>pixel reconstruction</b>, and the open question becomes <b>which damage it should learn to see through.</b></p></div>

<!--
0:45 · Say: LeCun argues that predicting pixels wastes effort on detail that doesn't matter, which is why JEPA predicts features instead. For text that argument flips: the tiny detail, a dot or a stroke, is exactly what decides the letter. The September 2026 HTR paper confirms it: pixel reconstruction keeps per-character information that contrastive and JEPA-style models lose. So we rebuild pixels, and the real question is which damage the model should learn to see through.
Image: Welch Labs, "Yann LeCun's $1B Bet Against LLMs [Part 1]" (11:20).
-->

---

<!-- _class: dense -->

# Other related work

| Work | What it does | What it leaves open |
|---|---|---|
| SeqCLR, DiG, CCD (2021–23) | Contrastive, masked and distillation SSL for text | Augmentation choice ad hoc; heavy compute |
| LoGo-HTR (Mitra, Mondal & Jawahar), WACV 2026 | Contrastive + decorrelation SSL for handwriting; 10M unlabelled word images | No damage modelling; contrastive, which 2609.35473 finds weaker for HTR |
| Baloun et al., IJDAR 2025 | Barlow Twins SSL for historical page segmentation; compares augmentations by trial | Segmentation, not recognition; augmentations still hand-chosen |
| Penarrubia et al., IJCV 2025 (survey) | Map of SSL for text recognition | No augmentation-selection procedure; inconsistent protocols |
| Mintun et al., NeurIPS 2021 | Augmentation–corruption similarity predicts robustness | Natural images, supervised |
| Augraphy (2022), DocCreator | Simulators of document damage | Not fitted to real statistics, not studied for SSL |
| Salerno & Tonazzini (recto–verso models) | Physical models of show-through and bleed-through | Used for restoration, not for pretraining |

<!--
If asked whether damaged historical text is solved: on four sets of Islamicate manuscripts, Google Cloud OCR had 49–71% character error rate; pretraining on unlabelled lines plus only 30 labelled lines brought it to 15–46% (Vogler et al., 2022).
-->

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

<!-- _class: dark divider -->

# Approach

<!-- 0:05 -->

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
# Experiments and data

<div class="grid3">
<div class="card"><div class="kicker">Models we train</div><p class="small meta">Same encoder and fine-tuning for all; only the pretraining changes.</p><ol style="margin:0; padding-left:1.3em;"><li>No pretraining (supervised only)</li><li>Masking only (plain MAE)</li><li>Masking + hand-picked damage</li><li><span class="p">Masking + derived damage (ours)</span></li><li>VICReg + derived damage (control)</li></ol><div class="rule small"><b>Reference points:</b> transfer from a related labelled set; an off-the-shelf OCR or VLM.</div></div>
<div class="card"><div class="kicker">How we test them</div><ul><li>Fine-tune with 1%, 10% and 100% of the labels</li><li>Clean handwriting, then with one damage type held out</li><li>Real damaged lines, tagged by damage type</li><li>An unseen script, and camera-captured text</li></ul><div class="rule small"><b>We measure:</b> character error rate (CER), how much each model ignores each damage type, and how the two relate.</div></div>
<div class="card green"><div class="kicker green">Data, and what it is for</div><ul><li><b>IAM</b> (≈10k lines, modern English handwriting): supervised baseline and the clean test</li><li><b>CATMuS Medieval</b> (≈195k real historical lines): pretraining, fitting the damage models, damaged test</li><li><b>HTR-United</b> (catalogue of historical sets): extra damage types and media</li><li><b>IIIT-Indic</b> (872k words, 10 Indian scripts) and <b>Muharaf</b> (36k Arabic lines): unseen-script test</li><li><b>Scene text</b> (IIIT5k, IC13, IC15): camera-capture test</li></ul></div>
</div>

<!--
0:50 · Say: Five models that differ only in pretraining, so any difference comes from what each was trained to ignore. We test with few and many labels, on clean, held-out and real damaged lines, and on scripts and capture conditions we never fitted. The one new data task is tagging a few hundred real lines by type of damage (not transcribing them). The OCR/VLM reference answers "why not just use a big model?" with numbers on the same lines.
Tools: pero-pretraining and PARSeq (code), Augraphy plus our own physics-based damage models, PyTorch. All datasets are free for research; the Indic and Arabic sets need an author request for the full version.
-->

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

# Applications and use cases

<div class="grid4" style="flex:1 1 auto; min-height:0;">
<div class="card"><img class="photo grow" style="min-height:0;" src="assets/img/bodleian_library.jpg"><h3 style="font-size:20px;">Archives and libraries</h3><p style="font-size:14px; min-height:120px;">Libraries scan faster than anyone can transcribe. Pretrain on a collection’s own pages, then a few hundred transcribed lines are enough to start reading it.</p></div>
<div class="card"><img class="photo grow" style="min-height:0; object-position:50% 30%;" src="assets/img/indic_manuscript_devanagari.jpg"><h3 style="font-size:20px;">Low-resource scripts</h3><p style="font-size:14px; min-height:120px;">Many Indian scripts have plenty of scanned pages but few labelled lines. Learning mostly from the unlabelled pages is how they scale.</p></div>
<div class="card"><img class="photo grow" style="min-height:0; object-position:50% 25%;" src="assets/img/handwritten_page.jpg"><h3 style="font-size:20px;">Forms and exam scripts</h3><p style="font-size:14px; min-height:120px;">Handwritten forms and answer sheets vary in ink, paper and scanner, and few are transcribed. Pretraining on the scans themselves means a few labels suffice.</p></div>
<div class="card"><img class="photo grow" style="min-height:0;" src="assets/img/blurred_photo.jpg"><h3 style="font-size:20px;">Camera capture</h3><p style="font-size:14px; min-height:120px;">Phone photos of documents bring blur, shadows and uneven light. The same measure-and-fit recipe applies to capture damage.</p></div>
</div>

<!--
0:45 · Say: Anywhere text is damaged or unusual and labels are scarce: damaged documents are where OCR fails and labels are rarest, so deriving the corruptions from the documents themselves lets a small model learn a new collection from its unlabelled pages.
Why it matters beyond archives: for research, every SSL method decides what to ignore, and for text that choice is made by trial; we turn it into a procedure and test when ignoring damage helps and when it erases the letters. What we leave behind: fitted damage models, real lines tagged by damage type, and a tool that measures what a trained model ignores. Beyond OCR, the recipe (measure the nuisance, model it, fit it, check the match) could serve any field where damage is physically modellable.
Photo credits: Duke Humfrey's Library, Bodleian (David Iliffe, Wikimedia Commons); Devanagari manuscript on paper (Wikimedia Commons); handwritten page and blurred photo: add sources.
-->

---

<!-- _class: dark divider -->

# Deliverables

<!-- 0:05 -->

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

<!-- _class: dense -->

# References (1/2)

<div class="refs">
<div><span>1</span><span>Garrido-Munoz &amp; Calvo-Zaragoza. <a href="https://arxiv.org/abs/2609.35473"><i>Handwritten Text Recognition Lives in the High-Pixel Variance Subspace.</i></a> arXiv:2609.35473, 2026.</span></div>
<div><span>2</span><span>Penarrubia, Valero-Mas &amp; Calvo-Zaragoza. <a href="https://arxiv.org/abs/2407.19889"><i>Self-Supervised Learning for Text Recognition: A Critical Survey.</i></a> IJCV, 2025.</span></div>
<div><span>3</span><span>Kišš &amp; Hradiš. <a href="https://arxiv.org/abs/2405.00420"><i>Self-supervised Pre-training of Text Recognizers.</i></a> ICDAR, 2024.</span></div>
<div><span>4</span><span>Vogler, Allen, Miller &amp; Berg-Kirkpatrick. <a href="https://arxiv.org/abs/2112.08692"><i>Lacuna Reconstruction: Self-Supervised Pre-Training for Low-Resource Historical Document Transcription.</i></a> Findings of NAACL, 2022.</span></div>
<div><span>5</span><span>Mitra, Mondal &amp; Jawahar. <a href="https://openaccess.thecvf.com/content/WACV2026/html/Mitra_Learning_Beyond_Labels_Self-Supervised_Handwritten_Text_Recognition_WACV_2026_paper.html"><i>Learning Beyond Labels: Self-Supervised Handwritten Text Recognition (LoGo-HTR).</i></a> WACV, 2026.</span></div>
<div><span>6</span><span>Baloun, Prantl, Lenc, Martínek &amp; Král. <a href="https://doi.org/10.1007/s10032-025-00538-6"><i>On Self-Supervision in Historical Handwritten Document Segmentation.</i></a> IJDAR, 2025.</span></div>
<div><span>7</span><span>Souibgui et al. <a href="https://arxiv.org/abs/2203.04814"><i>Text-DIAE: A Self-Supervised Degradation Invariant Autoencoder for Text Recognition and Document Enhancement.</i></a> AAAI, 2023.</span></div>
<div><span>8</span><span>Ericsson, Gouk &amp; Hospedales. <a href="https://arxiv.org/abs/2111.11398"><i>Why Do Self-Supervised Models Transfer? Investigating the Impact of Invariance on Downstream Tasks.</i></a> BMVC, 2022.</span></div>
<div><span>9</span><span>Mintun, Kirillov &amp; Xie. <a href="https://arxiv.org/abs/2102.11273"><i>On Interaction Between Augmentations and Corruptions in Natural Corruption Robustness.</i></a> NeurIPS, 2021.</span></div>
<div><span>10</span><span>Aberdam et al. <a href="https://arxiv.org/abs/2012.10873"><i>Sequence-to-Sequence Contrastive Learning for Text Recognition (SeqCLR).</i></a> CVPR, 2021.</span></div>
<div><span>11</span><span>Groleau et al. <a href="https://arxiv.org/abs/2208.14558"><i>Augraphy: A Data Augmentation Library for Document Images.</i></a> arXiv:2208.14558.</span></div>
<div><span>12</span><span>Salerno &amp; Tonazzini. <a href="https://explore.cnr.it/resource/item/82858"><i>Highly Degraded Recto-Verso Document Image Processing and Understanding.</i></a> ERCIM News 95, 2013.</span></div>
<div><span>13</span><span>Clérice et al. <a href="https://doi.org/10.1007/978-3-031-70543-4_11"><i>CATMuS Medieval: a multilingual large-scale cross-century dataset in Latin script for HTR.</i></a> ICDAR, 2024.</span></div>
<div><span>14</span><span>Marti &amp; Bunke. <a href="https://doi.org/10.1007/s100320200071"><i>The IAM-database: an English sentence database for offline handwriting recognition.</i></a> IJDAR, 2002.</span></div>
<div><span>15</span><span>Li, Liu, Guo, Yin et al. <a href="https://github.com/PaddlePaddle/PaddleOCR"><i>Dive into OCR.</i></a> PaddlePaddle, 2022.</span></div>
<div><span>16</span><span>Chacko &amp; Dhanya. <a href="https://arxiv.org/abs/1402.2188"><i>Handwritten Character Recognition in Malayalam Scripts: A Review.</i></a> IJAIA 5(1), 2014.</span></div>
</div>

---

<!-- _class: dense -->

# References (2/2)

<div class="refs">
<div><span>17</span><span>Guan et al. <a href="https://arxiv.org/abs/2505.20429"><i>PreP-OCR: A Complete Pipeline for Document Image Restoration and Enhanced OCR Accuracy.</i></a> arXiv:2505.20429, 2025.</span></div>
<div><span>18</span><span>Bromley, Guyon, LeCun, Säckinger &amp; Shah. <a href="https://proceedings.neurips.cc/paper/1993/hash/288cc0ff022877bd3df94bc9360b9c5d-Abstract.html"><i>Signature Verification using a “Siamese” Time Delay Neural Network.</i></a> NIPS, 1993.</span></div>
<div><span>19</span><span>Mikolov et al. <a href="https://arxiv.org/abs/1301.3781"><i>Efficient Estimation of Word Representations in Vector Space (word2vec).</i></a> 2013.</span></div>
<div><span>20</span><span>Devlin et al. <a href="https://arxiv.org/abs/1810.04805"><i>BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.</i></a> NAACL, 2019.</span></div>
<div><span>21</span><span>Doersch, Gupta &amp; Efros. <a href="https://arxiv.org/abs/1505.05192"><i>Unsupervised Visual Representation Learning by Context Prediction.</i></a> ICCV, 2015.</span></div>
<div><span>22</span><span>Chen et al. <a href="https://arxiv.org/abs/2002.05709"><i>A Simple Framework for Contrastive Learning of Visual Representations (SimCLR).</i></a> ICML, 2020.</span></div>
<div><span>23</span><span>He et al. <a href="https://arxiv.org/abs/1911.05722"><i>Momentum Contrast for Unsupervised Visual Representation Learning (MoCo).</i></a> CVPR, 2020.</span></div>
<div><span>24</span><span>Grill et al. <a href="https://arxiv.org/abs/2006.07733"><i>Bootstrap Your Own Latent (BYOL).</i></a> NeurIPS, 2020.</span></div>
<div><span>25</span><span>Zbontar et al. <a href="https://arxiv.org/abs/2103.03230"><i>Barlow Twins: Self-Supervised Learning via Redundancy Reduction.</i></a> ICML, 2021.</span></div>
<div><span>26</span><span>Bardes, Ponce &amp; LeCun. <a href="https://arxiv.org/abs/2105.04906"><i>VICReg: Variance-Invariance-Covariance Regularization for Self-Supervised Learning.</i></a> ICLR, 2022.</span></div>
<div><span>27</span><span>Caron et al. <a href="https://arxiv.org/abs/2104.14294"><i>Emerging Properties in Self-Supervised Vision Transformers (DINO).</i></a> ICCV, 2021.</span></div>
<div><span>28</span><span>He et al. <a href="https://arxiv.org/abs/2111.06377"><i>Masked Autoencoders Are Scalable Vision Learners (MAE).</i></a> CVPR, 2022.</span></div>
<div><span>29</span><span>Assran et al. <a href="https://arxiv.org/abs/2301.08243"><i>Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture (I-JEPA).</i></a> CVPR, 2023.</span></div>
<div><span>30</span><span>LeCun. <a href="https://nips.cc/Conferences/2016"><i>Predictive Learning</i></a> (the “cake” slide). NIPS 2016 keynote.</span></div>
<div><span>31</span><span>VLM OCR hallucination evidence: <a href="https://arxiv.org/abs/2601.03714">arXiv:2601.03714</a> (DeepSeek-OCR on random strings); <a href="https://arxiv.org/abs/2506.05551">TextHalu-Bench, arXiv:2506.05551</a>.</span></div>
<div><span>32</span><span>Video: Welch Labs. <a href="https://www.youtube.com/@WelchLabsVideo"><i>Yann LeCun’s Billion Dollar Bet</i></a> (Part 1), YouTube.</span></div>
<div><span>33</span><span>Jaderberg et al. <a href="https://arxiv.org/abs/1506.02025"><i>Spatial Transformer Networks.</i></a> NeurIPS, 2015.</span></div>
<div><span>34</span><span>Dosovitskiy et al. <a href="https://arxiv.org/abs/2010.11929"><i>An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale (ViT).</i></a> ICLR, 2021.</span></div>
<div><span>35</span><span>Shi, Bai &amp; Yao. <a href="https://arxiv.org/abs/1507.05717"><i>An End-to-End Trainable Neural Network for Image-based Sequence Recognition (CRNN).</i></a> TPAMI, 2017.</span></div>
<div><span>36</span><span>Bautista &amp; Atienza. <a href="https://arxiv.org/abs/2207.06966"><i>Scene Text Recognition with Permuted Autoregressive Sequence Models (PARSeq).</i></a> ECCV, 2022.</span></div>
</div>

---

<!-- _class: dark -->

<div class="col" style="height:100%; justify-content:center;">
<div class="col" style="gap:16px;">
<h1 style="font-size:96px;">Thank you</h1>
</div>
</div>
