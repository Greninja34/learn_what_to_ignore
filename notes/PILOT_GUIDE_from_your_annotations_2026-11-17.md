# The pilot explained, slide by slide, from your handwritten notes (17 Nov 2026)

Source: `DOC-20261116-WA0008_261117_003803.pdf` (33 slides, your red pen). Numbers come from
`results/pilot_summary.md`, `results/tables/*.md`, and the docstrings in `lwti/`. I checked the deck's numbers against them.
Where I am guessing what your handwriting says, I mark it **(guess)**.

---

## 0. What you are asking, in one paragraph

Your notes are three kinds of remark, mixed together:

1. **"I don't understand this"** (seeds, 5% labels, augmentation, background normalisation, hand-picked vs derived, the A2 graphs, why A3 failed, why "care" on A4, robustness, RQ3). Part 3 answers every one.
2. **"Is this honest / when did this happen?"** (Challenges slide, Objectives "done", Status column, "are we sure about E1-E4", "unseen script = we assume it works"). Part 4 answers these, and says plainly where the deck overclaims.
3. **"Redo the slide"** (jargon before explanation, too detailed, split into separate slides, add pictures, add Intro / OCR / SSL in simple words). Part 5 is a to-do list from these.

Your three red whiteboard slides (3, 4, 7) say: *Introduction* / *OCR | SSL* / *Simple words ○ ○ ○ ○*. I read that as: **"before any result, add an intro section that explains OCR, then SSL, in simple words, in four steps"**. Part 1 is a draft of that.

---

## 1. The whole project in simple words (the intro you asked for)

**OCR (text recognition).** A computer reads a photo of one line of handwriting and writes out the letters. Our model is a CRNN: a CNN looks at the image, a BiLSTM reads it left-to-right, CTC turns that into a string. Score = **CER** (character error rate): 20% means 1 character in 5 is wrong.

**The problem.** Old manuscripts are damaged (brown paper, faded ink, writing showing through from the back, stains, blur). Models trained on clean pages fail on them, and damaged pages are exactly where people have *not* typed up the correct text, so there are few labelled lines to train with.

**SSL (self-supervised learning).** Learn from lines with *no* text label. Example task: hide part of a line and make the network rebuild it. The network then "knows what lines look like" before it ever sees a label. After that you fine-tune with the few labelled lines.

**Our idea ("Learning What to Ignore").** SSL needs *some* damage fed in, so the model learns to see through it. People pick that damage by hand. We *measure* the damage on real manuscript lines (CATMuS), copy it onto clean lines (IAM), and use that "derived" damage instead of a guess. Then we ask: does it help, and can we predict from inside the model which damage will hurt?

**What the pilot actually did (one line each):**
1. Built clean data + a baseline recogniser (CRNN).
2. Checked damage hurts (A1) and that real damage is measurably different (A2).
3. Test 1: SSL pretraining with derived damage (A3, A4). **No gain.**
4. Test 2: use the same damage as plain training augmentation (E1). **Small gain on real lines.**
5. Checked if "how much the model's features ignore a damage" predicts "how much that damage raises error" (RQ3). **Yes in IAM, strongly.**

---

## 2. Glossary (every word that tripped you up)

| Term | Plain meaning |
|---|---|
| **IAM** | Clean modern English handwriting. Our "clean" source. |
| **CATMuS** | Real medieval Latin/French manuscript lines. Our "real damage" target. Its test set is from *different manuscripts* than its training set. |
| **CER** | Wrong characters / total characters. Can exceed 100% (e.g. 102.1 appears in a table). Lower is better. |
| **Labels 5%, 10%, 1%** | We pretend only a fraction of the lines have transcriptions. 5% of CATMuS = 1,188 of 23,762 lines; 10% of IAM = 648 of 6,482; 1% = 65. This simulates "few labels", which is the whole motivation. 100% = fully supervised ceiling. |
| **Seed** | One repeat of the same experiment with different randomness (starting weights, which lines get picked, order of data). Different seeds give slightly different CER. The spread (about 0.5 points) is "luck", so a difference smaller than that means nothing. Hence 2-3 seeds. |
| **Scratch / no pretraining** | Train the CRNN from random start on the labelled lines only. The thing everything else must beat. |
| **Pretraining (ConvMAE)** | Before labels: take 30k unlabelled lines, add damage, hide 60% of 8-pixel strips, make the CNN rebuild the clean line (34 min). Copy that CNN into the CRNN, then train with labels. |
| **Masking only** | Same pretraining but no damage added. Tells us whether damage matters, or just the hide-and-rebuild trick. |
| **Hand-picked damage (recipe)** | The usual practice: every damage type, each applied with probability 0.5, strength uniform over a range we chose by eye. |
| **Derived damage (recipe)** | Fitted to CATMuS. For each damage type, measure a statistic (e.g. paper brightness). The share of CATMuS lines outside IAM's normal range = how often to apply it. Their position on the response curve = how strong. Result: paper-tone 84%, show-through 89%, stain 37%, fade 26%, noise 11%, blur 5%. Ink loss is **held out** (never trained on, used only as an "unseen damage" test). |
| **Augmentation** | Yes, your guess is right: **a transform applied to the training image while the label stays the same.** Here the transform is "add simulated damage", redrawn every epoch. The model must read the true text through it. No pretraining involved. |
| **Background normalisation (bgnorm)** | A plain image filter with no learning that flattens uneven paper/background before the model sees the line. It is a **control**: "could a simple clean-up give the same gain as our damage recipe?" Answer: 33.0% vs 31.6%, so no. |
| **Quartile / "darkest-paper quarter"** | Sort the CATMuS *test* lines by a measured statistic (within each manuscript), take the worst 25%. "Hard subset". Same lines for every model. |
| **KS D** | Gap between two distributions: 0 = same, 1 = totally separate. Used on the A2 graphs. |
| **Invariance** | Feed a line clean and then damaged. Compare the CNN's feature vectors with cosine similarity (1 = unchanged). 1 = the model "ignores" the damage. |
| **Spearman ρ** | Rank correlation. -1 = perfect "more of X, less of Y"; 0 = unrelated; +1 = both rise together. |
| **Held-out** | Kept out of training so it tests generalisation. |

---

## 3. Every number you flagged, explained

### Slide 23. Baselines ("clueless on the models... 5% of labels... what seeds??")
| Row | What it is | What it tells you |
|---|---|---|
| PaddleOCR, off the shelf | A big industrial OCR, used with no training | IAM 11.4%, **CATMuS 52.5%**. It collapses on medieval lines: the problem is real |
| CRNN 100% labels | Our small model, all labels | IAM 9.8%, CATMuS 20.0%. Beats the industrial OCR on IAM, so "good accuracy is achievable" |
| CRNN 10% IAM, 5% CATMuS, 1% IAM | Same model, few labels | Error rises as labels drop (9.8 → 19.9 → 43.3 on IAM). This is the low-label regime the project is about |

"Model" is the missing header word you wrote on the slide: the first column should say *which model*. The title ("accuracy is achievable and the gap is real") is a claim, not a label; you suggested "annotation style" which I read as an arrow-labelled chart **(guess)**.

**Stale numbers on this slide.** The deck says 19.6% (IAM 10%) and 33.6% (CATMuS 5%) as 2-seed means. After the third seed (16 Nov) `pilot_summary.md` Table 1 says **19.9% and 33.8% (3 seeds)**; IAM 1% is still 43.3% (2 seeds). Update the table and the footnote to "2-3 seeds".

### Slide 24. A1 passes: damage hurts
- Take the model trained on *clean* IAM (9.8% CER), apply each of 7 synthetic damages to the test lines at 3 strengths, measure CER again.
- The chart shows only **medium** strength (your "others??" question). Low/high are in the table: e.g. tone 10.8 / 33.1 / **99.4%**; ink loss 44.5 / 75.1 / 87.7%. If you want them on the slide, show all three as a small grid.
- Pass rule written before the runs: at least 2 of 7 families must double the error at medium. Four did (ink loss ×7.6, noise ×4.9, tone ×3.4, blur ×3.1). Fade, stain, show-through only ×1.2-1.4 and are grey.
- The right-hand box is the *real-lines* version: on CATMuS, the most faded quarter is 1.35-1.47× worse than the least faded. Other statistics (paper level, noise, unevenness) show no clear effect.
- Your fix ("state A1 first, then conclusion; centre the chart") is purely layout: put the assumption sentence "A1: damage hurts a clean-trained model" above the chart.

### Slide 25. A2 fails (the graphs "and all math used")
- Each small plot = one measured statistic on every line. Grey outline = IAM, green fill = CATMuS. If the two shapes barely overlap the statistic separates the datasets.
- **KS D** measures that: the biggest vertical gap between the two cumulative curves. Rule fixed in advance: at least **3** damage statistics with D ≥ 0.5.
- Results: paper level **0.82**, faint grey (show-through) **0.84** reach it; background unevenness 0.42, contrast 0.26, sharpness 0.11, noise 0.16 do not. That is 2 of 3 needed, so **A2 FAIL**.
- Stroke width (0.73) and ink fraction (0.94) differ a lot, but that is scale/script (CATMuS strokes are thicker at 64 px height), not damage, so they do not count.
- **Your note, as I now read it (zoomed in):** *"need to understand these graphs properly, all the math used here, and help me get it from the [graph]... values don't match table"*. Two parts: (1) explain the graphs and the maths; (2) the numbers you can read off the graphs do not obviously match the table. See the next section. Short answer to (2): **there is no data error.** I recomputed all eight medians and KS values from `results/stats/iam_train.csv` and `catmus_train.csv` (3,000 random lines each) and every one matches the slide and `pilot_summary.md` exactly. The graphs just never print the medians, and a KS value cannot be read off a histogram by eye.
- Reading it simply: **real manuscripts differ from clean IAM mainly by darker paper and more show-through, not by blur or noise.** Honest caveat for reviewers: IAM-vs-CATMuS also differs in pen, script and scan resolution, so some of this gap is not damage. `derive.py` says so itself ("v0 limitation").

### The 8 graphs of slide 25, one by one (you counted 8, I only explained 6; here are all of them)

Each graph = one number measured on **every line** (`lwti/damage/measure.py`). Bars = how many lines have that value. Grey outline = IAM, green fill = CATMuS.

| # | Graph | What is measured | Reads as | IAM median | CATMuS median | KS D | Counts as damage? | Damage family it feeds |
|---|---|---|---|---|---|---|---|---|
| 1 | Paper level | brightness of the background (median of the non-ink pixels, 0-1) | lower = darker paper | 0.980 | 0.804 | **0.82** | yes | tone |
| 2 | Faint grey on paper | share of paper pixels (away from strokes) that are faintly grey | higher = more show-through | 0.0018 | 0.0767 | **0.84** | yes | show-through |
| 3 | Background unevenness | spread of the smoothed paper level, strokes painted out | higher = stains, uneven light | 0.0054 | 0.0094 | 0.42 | yes, not separated | stain |
| 4 | Ink-paper contrast | (paper − ink)/255 from an Otsu split | lower = faded ink | 0.478 | 0.408 | 0.26 | yes, not separated | fade |
| 5 | Sharpness | variance of the Laplacian / contrast² | lower = blurred | 1.084 | 0.939 | 0.11 | yes, not separated | blur |
| 6 | Pixel noise | robust spread of the high-pass residual on paper pixels | higher = noisier | 0.0000 | 0.0058 | 0.16 | yes, not separated | noise |
| 7 | Stroke width | 2 × ink area / ink perimeter, in px | thicker strokes | 3.33 | 4.81 | 0.73 | **no, scale/script** | none |
| 8 | Ink fraction | share of pixels that are ink | more ink | 0.119 | 0.260 | 0.94 | **no, scale/script** | ink loss |

Why 8 graphs but 7 damage families: six damage families each have their own statistic (rows 1-6), ink loss uses row 8, and stroke width (row 7) has no family. Rows 7-8 differ hugely because CATMuS strokes are thick and dense at 64 px height, which is about pen, script and scan scale, so the pre-set rule does not count them.

**How to read a histogram and get the numbers yourself.**
1. *Median* = the value where half the lines are below. In graph 1 the grey IAM outline is a narrow spike near 0.98 (every IAM page is white), while the green CATMuS bars spread from 0.6 to 1.0 with the middle at 0.80.
2. *KS D* (Kolmogorov-Smirnov, the "math used"). Sort each dataset's values. For any cut-off x, let F_IAM(x) = share of IAM lines with value ≤ x and F_CAT(x) = the same for CATMuS. Then **D = max over x of |F_IAM(x) − F_CAT(x)|**. D = 0 means the two datasets are indistinguishable, 1 means you can separate them perfectly with one cut-off. Paper level D = 0.82 means: there is a cut-off where 82 percentage points more CATMuS lines than IAM lines lie below it. Shapes that barely overlap (graphs 1, 2, 8) give D near 1; shapes that overlap (graph 5) give D near 0.
3. *The rule*: at least 3 of the damage statistics (rows 1-6) need D ≥ 0.5. Rows 1 and 2 reach it, so 2 of 3 and A2 fails.

Two honesty notes for A2:
- The slide says "rule fixed in advance". `lwti/eval/fig_stats.py` says the criterion was *"fixed before computing D, after seeing medians"*. That is weaker. Say "fixed before computing the KS values", or the panel may ask.
- The green spike at 1.0 in graphs 1 and 4 is 160 of 3,000 CATMuS lines (5.3%) that are pure black-and-white (already binarised). They are included in A2 but excluded from the real-line quartile analysis (`hard_subset.py`).

### Slide 26. A3 fails, A4 passes (the "how hand-pick / how derive / why care for A4")
- Setup (Test 1): pretrain the CNN 34 min on unlabelled lines with each recipe, then fine-tune with few labels. Columns: no pretraining, masking only, + hand-picked damage, + derived damage.
- **A3 = "pretraining beats scratch".** CATMuS 5%: 33.6 / 33.3 / 35.0 / 33.4. Nothing beats scratch by more than the ~0.5-pt seed spread. **FAIL.**
- **A4 = "derived beats hand-picked".** Derived ≤ hand-picked in 3 of 3 settings. **PASS...**
- **...read with care**, because derived is *not better than doing nothing*: derived ≈ masking only ≈ scratch. The only reason derived "wins" is that hand-picked damage **hurts** (35.0 vs 33.3). So the correct reading is "bad damage hurts, derived damage does no harm", not "derived damage helps". That is what the amber box has to explain.
- **Why it failed (this needs its own slide, as you said).** These are our hypotheses, not proven: (1) only 30k lines for 34 min, while papers that gain use millions; (2) it was judged on *clean* CER, but the idea is about damaged lines; (3) fine-tuning ran long at full learning rate and may have washed out the pretrained start; (4) rebuilding 8-px gaps teaches texture that normal training learns in minutes anyway. Matches Kišš & Hradiš 2024: pretraining isn't always better than supervised.
- Fix the table: its "no pretraining" column is the old 2-seed mean (33.6 / 19.6); the updated 3-seed means are 33.8 / 19.9 (the A3 verdict does not change).
- "Mean of 2 seeds": the header says two runs were averaged. It is circled because 2 is thin.

### Slide 27. "Same damage as augmentation helps on real lines" (Test 2, the best result)
- Setup: no pretraining. Just train the CRNN from scratch on the 5% labelled CATMuS lines, but each epoch add damage to each training image. Four arms: none, hand-picked recipe, derived recipe, bgnorm control.
- **"How can adding damage help?"** With only 1,188 labelled lines the model has seen few paper tones and contrast levels. Adding fitted damage shows it many more versions of the same lines, so it generalises better to unseen manuscripts.
- Rows = what we test on. *All test lines* is the headline; the three "quarter" rows are the most damaged 25% by paper darkness, show-through and low contrast; IAM 10% is the clean check.
- **What the numbers mean.** 33.8% → **31.6%** = 2.2 fewer wrong characters per 100, mean of 3 seeds, seed range about ±0.5-0.7. The gain is bigger than the noise, so it's real. On the hard quarters: 35.6→33.0 (-2.6), 35.7→32.9 (-2.8), 39.4→37.0 (-2.4). Bold = best in the row.
- Hand-picked is nearly no gain on CATMuS (33.6) but the best on IAM (18.8 vs 18.9, essentially tied).
- **Pass/fail rules (B1-B5)** were written on 16 Nov *before* the runs finished: B1 big gain on synthetic damage; B2 derived beats hand-picked; B3 beats bgnorm; B4 no clean-accuracy cost; B5 helps the hard real lines. B1, B3, B4, B5 pass.
- **Flag: B2 "pending" looks like it will fail.** The rule compares the IAM synthetic-damage CER: derived 19.4% vs hand-picked 18.9%. Derived is *not* lower. (On real CATMuS lines derived is clearly better, 31.6 vs 33.6, but that is a different measure from the one the rule uses.) Run `python -m lwti.eval.summary` and decide whether to say "B2 fails on IAM, holds on CATMuS" rather than "pending". Do not leave it ambiguous in front of the panel.

### Slide 28. "What this does and does not show" (make it a list; understand each)
- **A. Synthetic gain is partly circular.** IAM medium damage: 37.9% → 19.4% looks huge, but we tested on the *same damage types* the model trained on. It is like practising the exact exam questions. The fair test is ink loss, which no recipe used: error ratio ×3.82 → ×3.59 (derived), ×3.27 (hand-picked). Small gain.
- **B. Helps, but not "damage-specific".** If derived damage were targeting damage, the hardest quarters should gain more than average. They gain 2.4-2.8, the average gains 2.2. About the same. So we say "helps on CATMuS", not "helps where damage is worst".
- **C. Winner depends on the data.** Hand-picked wins on IAM (clean data, synthetic damage); derived wins on CATMuS (damage real and large). Fits our idea but it is one dataset pair.
- **D. Small evidence.** 3 seeds, one dataset pair, one recogniser.

### Slide 29. "The recipe leaves a trace in robustness"
- **Robustness** = how much accuracy survives when test lines are damaged. These are the *pretrained* IAM-10% models, test CER under damage, seed 0 / seed 1 (shown separately because seeds disagree a lot).
- Paper-tone medium: derived 32.1 / 26.4 vs scratch 39.9 / 39.4. Blur high: hand-picked 64 vs 79-80. Ink loss (never trained on): nothing helps.
- **"Trace"** = each recipe makes the model a bit more resistant to the damage it saw: derived to paper tone, hand-picked to blur.
- Be careful: only 2 seeds and they swing wildly (masking only, paper tone: 32.5 vs 59.2). Treat it as a hint, not a result.

### Slide 30. RQ3 (your "counter-intuitive, cannot comprehend")
Your sentence, *"the less the encoder ignores a damage, the more that damage raises error"*, **is exactly what the slide says**, not the opposite. The confusion is the minus sign:
- x-axis = invariance (1 = encoder ignores the damage). y-axis = how much CER multiplies (log scale).
- Dots go from top-left (low invariance, error ×10) to bottom-right (high invariance, error ×1). That is a **negative** correlation, ρ = -0.92. "Negative" here means "good": more invariance, less damage to accuracy.
- How each dot is made: pick a damage type and strength (7 types × 3 strengths = 21 dots). Run 500 test lines clean and damaged through the CNN, average the features over each line, compare with cosine similarity → x. Divide damaged CER by clean CER → y.
- **Why it might be too easy, and why the checks exist.** Heavy damage changes pixels more, which would both lower invariance and raise error. So the claim could be trivial. Three checks: (1) hold strength fixed: ρ ≈ -0.81 / -0.88 / -0.88 at low / medium / high; (2) compare 8 models at the same damage: negative in 21 of 21 (mean -0.69); (3) subtract pixel-space change: partial ρ ≈ -0.80 in all nine pilot models.
- **"Only IAM, where is the rest?"** Right: only IAM, only synthetic damage. The slide's last line says so. CATMuS invariance has not been computed.
- **Two things the slide does not say loudly enough:**
  (a) In models trained with damage augmentation ρ is only -0.2 to -0.4, because they barely react to damage they trained on. So the relationship is strongest for models that were *not* trained for it.
  (b) **The H3 "sign flip" is not supported by the pilot.** Full explanation in the next section.

### What is the "sign flip" (H3)? Start to finish

*Sign* = whether invariance is good (negative correlation with error rise) or bad (positive). H3 says the sign depends on **which part of the image the damage touches**.

- **Paper-only damage** (tone, noise, show-through, stain; the strokes are intact). The model can ignore it for free, so invariance should help: more invariance, less error. Sign: **negative**.
- **Stroke-overlapping damage** (fade, blur, ink loss; the strokes themselves are altered). To become invariant to blur, the model must stop using fine stroke detail, and that is the same detail that separates *e* from *c* on clean lines. Invariance is bought with accuracy. H3 predicts it **does not help, and may hurt**. Sign: **zero or positive**.
- Analogy: noise-cancelling headphones help when the unwanted sound is a fan hum, but hurt when the unwanted sound is in the same pitch range as the voice you want to hear.
- "Flip" = the relationship changes sign between the two groups. The report's falsifier (Table 2.1) is: *"one monotone relationship across all families, or no correlation"*.

**What the pilot shows.** In the 9 normal models: overlap group ρ = −0.80 to −0.95, paper-only ρ = −0.78 to −0.94. Both strongly negative: one monotone relationship. By our own falsifier, **no flip was seen**. A second hint against it: hand-picked pretraining includes blur (an overlapping damage) and made models *more* robust to blur (64% vs 79-80% CER at high strength), so inducing invariance to an overlapping damage helped there (2 seeds, indicative only).

**Why this is still not a fair verdict on H3:**
1. H3 is a claim about *making* a model invariant (by training). The pilot only measures the invariance models happen to have. The proper test is E2 (consistency training toward invariance on an overlapping damage), which has not been run.
2. Overlapping damage destroys information, which lowers invariance and raises error at the same time, so a negative ρ is almost guaranteed there whatever H3 says.
3. In the augmented models, overlap-group ρ is about 0 (−0.08 to +0.13, p > 0.5), and the paper-only ρ is about −0.2. That is too noisy to call either way.

**What to put on the slides.** Slide 11 lists the flip as something *new that we found*. It is a **prediction we have not confirmed**. Honest wording: "H3 predicts a sign flip; the first, observational pilot check shows none; E2 is the real test."

### Scripts: IAM and CATMuS are Latin, Arabic and Indic are not. Is that a problem?

**Yes, it is a real problem, and your instinct is right.** Reasoning:

1. **What gets transferred is the recipe, not the model.** A recogniser trained on Latin cannot read Arabic: its output layer is built from the training charset (79 symbols for IAM, 195 for CATMuS). For a new script we must train a *fresh* recogniser with a new charset, with and without our damage augmentation, and compare. So "unseen script" really asks: does damage fitted on Latin lines still help on Arabic lines?
2. **Why it can work in principle.** Paper tone, show-through, blur and noise are physical and script-independent.
3. **Why it can fail, or be hard to interpret:**
   - Our recipe v0 was derived from the IAM-vs-CATMuS difference, and that difference already mixes in pen, script and scan scale (`derive.py` says so). Part of what we call "damage" is not damage.
   - Damage hits scripts differently. Arabic has connected strokes and dots; Indic scripts have thin headline strokes and vowel marks. The same blur can destroy them sooner, so a bad result may mean "this script is fragile", not "the recipe failed".
   - **The datasets do not fit our own protocol.** IIIT-INDIC-HW-WORDS is **word** images (our scope is single *lines* at 64 px), is modern handwriting with little real damage, and has *no stated licence* (starter pack: "ask the authors"). Muharaf has real damaged *lines* but is right-to-left, and only 1,216 of 1,644 pages are public.
   - Neither dataset is downloaded: `~/data/lwti` holds only IAM and CATMuS. That is the likely meaning of your "not confirmed" on the Status column: availability and licences for Phase 3 are not confirmed.
4. **Why you were right to say "we are assuming it works".** The deck shows scripts as part of the headline claim (RQ2) although nothing has been tested outside Latin. It is a hypothesis for Phase 3 (H2: script transfer should shrink most, and is falsified if it equals or beats damage transfer).

**My recommendation** (your decision):
- Keep **all main results (RQ1, RQ3) on IAM + CATMuS** and say plainly: "Latin script". 
- Treat the **same-script, new-damage pair (E4)** as the clean test of the *damage* claim, because it holds the script fixed. It answers exactly your worry.
- Make script transfer **one stretch test**, Muharaf (Arabic lines, real damage), and mark IIIT-INDIC as optional or drop it (words, no licence, undamaged).
- On the dataset slide: add a column "script" and mark Phase-3 rows "planned, access not yet confirmed".

---

## 4. The honesty questions

**Slide 12, "is this supervised learning or what?" / "when did we encounter these?"**
- *Supervised transfer* = train a model on a large labelled dataset, then reuse/fine-tune it on yours. Plain supervised learning, no SSL involved. "SSL may not beat supervised transfer" means: the fancy method may lose to the boring one.
- When encountered: row 1 **did happen** (A3 fail). Row 2 appeared as the circularity finding (slide 28 A). Row 3: ink loss held out, derived v0 matches statistics, not a physical fit. Row 4 is handled by design (official splits). Row 5 comes from the literature sweep. The slide is a mix of "happened" and "anticipated"; label each one, or retitle the slide "Risks and mitigations".

**Slide 13, Objectives: "done?? when done?"** From the weekly report (Week 15, 09.11.2026): the data pipeline, CRNN baselines and damage-measurement tool were built on **9 Nov 2026** (IAM CER 9.8%, PaddleOCR 11.4% IAM / 52.5% CATMuS). So objectives 1 and 2 were finished on **9 Nov**, with the pretraining chain on 9-10 Nov, E1 and RQ3 controls 10-16 Nov. Put the date next to "done". Note that your own weekly-report weeks 12-14 were reconstructed, not dictated; verify them.
**Slide 13, "what is this and why"**: objectives are the checklist the panel marks us against (the ESA marks research gap, objectives and feasibility). Each one maps to a deliverable. Say so in one sentence on the slide.

**Slide 16, "not confirmed" on Status.** The two Phase-3 datasets are only *planned*: nothing in `~/data/lwti/raw` or `lwti/data/` loads them, IIIT-INDIC has no stated licence and Muharaf only has a public part. IAM and the CATMuS subset really are processed (`prepare_iam.py`, `prepare_catmus.py`). Change the Status column to "processed / planned, access to be confirmed".

**Slide 16, "if unseen then we are not training on it, meaning we assume our approach works".** Yes, and that's the point of a transfer test: the claim is *"derived damage fitted on one source also helps on a script it never saw"*. It is a hypothesis to be tested in Phase 3, not an assumption. The slide should say "test whether it transfers", never "it works".

**Slide 18, "are we sure about E1-E4?"** E1 is done. E2 (consistency training), E3 (one bounded SSL rescue with a stop date), E4 (same-script new-damage pair) are **plans**, not results, and the slide's "E1 · DONE" tag already shows that. After 17 Nov the direction itself is undecided (handoff: rescue SSL vs reframe), so label E2-E4 "planned, subject to the post-ESA decision".

**Slide 21, "I am doing everything, kind pointless".** Noted. This is a team-allocation issue, not a slide fix. Decide with the guide whether the slide should show planned or actual ownership.

---

## 5. Slide-by-slide to-do from your pen (so nothing is lost)

| # | Your note | What to do |
|---|---|---|
| 1 | "align" | Align title-slide text or block to the left margin |
| 2 | "align centre", ticks, 02 struck, 07 boxed | Centre the number column; drop or reorder Suggestions from Review 1; emphasise Pilot results |
| 3,4,7 | Introduction / OCR \| SSL / Simple words | Add a 3-slide intro: OCR, SSL, "what we do" (draft in Part 1) |
| 5 | Formula crossed out | Delete the `front_seen = ...` line |
| 8 | "why? problem statement enough?" + scope box → next slide | Drop the abstract slide or merge; move *Scope* to the next slide |
| 9 | "redo this lol!!" | Redesign Scope and feasibility |
| 10 | jargon, too detailed, make separate slide | Plain words first; one slide for panel remarks, one for "is the problem real?" |
| 11 | "isn't this just lit. survey? improve header; need to understand!!" | Rename (e.g. "How we differ from earlier work"); explain each row |
| 12 | "when did we encounter these" | See Part 4 |
| 13 | "what is this and why" | Explain why objectives are there, add done dates or remove "done" |
| 14 | "remove too new ig" | Row 1 is the NeurIPS 2026 paper; remove or justify |
| 14 | "not same papers as review 1 ppt" | Make the survey consistent with Review 1 |
| 16 | "separate it", "not confirm" | Move the CATMuS-subset row elsewhere; verify statuses |
| 17 | "points direct" | Turn "Found while exploring" into plain bullets |
| 18 | "I will draw this" | You draw the pipeline |
| 19 | "RQ, H and all in old ppt, add them here" | Add RQ1-3 and H1-3 to this slide (full text is in `capstone/report/report.md`, lines 60-73) |
| 21 | "pointless" | Part 4 |
| 22 (Pilot) | "run week", "pictures", "is this needed", "explain", "graphics", "separate slide" | Retitle "Pilot run"; add images; explain "polygon fill" (the black area outside each CATMuS line, removed so the model does not see a fake pre-binarised look); move A1-A4 to its own slide |
| 23 | Model header, seeds, label % | Part 3 |
| 24, 25 | State A1/A2 first | Put the assumption sentence above each chart |
| 26 | Show A3 separately, why failed, why care for A4 | Part 3 |
| 27 | how, wth bgnorm, aug, numbers | Part 3 |
| 28 | make a list, understand | Part 3 |
| 29 | explain robustness | Part 3 |
| 30 | only IAM, counter-intuitive | Part 3 |
| 31 | "add future plans", "enough, make simple" | Add a plan strip; trim "Phase 1 delivered" |

---

## 6. Still your call

1. Whether to keep the sign flip as a "novelty" on slide 11 (my advice: reword it as an untested prediction).
2. Whether the script claim stays in the headline or moves to "Phase 3 stretch" (my advice: move it).
3. Slide 23 "make like annotation no?": I read it as "make the title a label, not a claim" (e.g. "Baselines"), with the claim as a callout. Tell me if you meant something else.
4. Slide 16 "separate it": I read it as moving the "CATMuS subset used" row out of the dataset table into its own line or the pipeline slide.
