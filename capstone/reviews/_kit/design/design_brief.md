# Design brief: "Learning What to Ignore" (capstone review deck)

This file is everything you need: the design direction, the constraints, and the full content of every slide. Assets are listed at the end; anything marked **[IMAGE]** is a frame I will fill myself.

---

## 1. The talk

- **What:** a 16:9 slide deck for a university capstone review (Phase 1, Review 1). Faculty panel, presented live.
- **Length:** 15 minutes of talk, then 5 minutes of questions. 20 content slides + 4 section dividers + title + thank-you, then 13 backup slides for the Q&A.
- **Topic:** self-supervised learning for handwritten text recognition, specifically **which kinds of document damage** (bleed-through, fading, stains, blur) a model should learn to ignore, with the damage modelled physically and fitted to real documents.
- **Tone:** a researcher explaining their thinking to a sharp but non-specialist audience. Clear, calm, a little personal (hand-written notes on diagrams), not corporate.

## 2. What I need back

A **design template I can rebuild in Marp** (Markdown slides + one CSS theme):

1. **Tokens:** exact colours (hex), font families and weights, a type scale (title, heading, body, caption, label sizes at 1280×720), spacing and corner radius.
2. **One layout per slide type** (section 5), each shown once with the real content from section 6.
3. **Diagram style:** how the hand-drawn diagrams look (stroke weight, roughness, arrowheads, fills), shown on the research loop and the hypothesis sketch.
4. Keep everything buildable in HTML/CSS + inline SVG: flat fills, simple shapes, no effects that need hand-placed artwork on every slide.

## 3. Design direction

### Colour: based on my website's palette

**Content slides are light; the title, the four section dividers and the closing slide are dark.** Both themes come from my site, and the accents keep exactly the same values in both.

| Token | Light (content slides) | Dark (title, dividers, closing) |
|---|---|---|
| Page | `#FFFFFF` | `#030305` |
| Card / raised surface | `#EBF0F4` | `#101318` |
| Headings / strong ink | `#12151B` | `#FFFFFF` |
| Body text | `#171B22` | `#E0E5EB` |
| Meta, captions | `#59606B` | `#9FA9B4` |
| Card edge | `#DFE6EB` | `#1B1E24` |
| Divider rule | `#B8BFC4` | `#35383E` |

**Four accents, each with one fixed meaning across the whole deck.** On my site, colour always means something; anything that isn't one of these four meanings stays neutral grey.

| Accent | Hex | Means in this deck |
|---|---|---|
| Purple | `#8D5ED0` | **Our method and contribution**: "this project", derived corruptions, the research questions |
| Blue | `#0078CD` | **Background and the landscape**: OCR, prior work, how things work today |
| Green | `#00893E` | **Data and feasibility**: datasets, "fits" verdicts, what we can do |
| Red | `#DB3837` | **Damage and risk**: degradation types, challenges, "wrong if" falsifiers |

- Tinted chips and soft fills mix the accent toward the background (about 14% fill and 54% edge on light, 22% fill and 42% edge on dark). Mix in OKLab, not OKLCH, so reds don't drift purple.
- Within these rules you are free to refine: shades, chart colours, how much accent each slide carries.

### Typography: serif-led, your choice

- **You pick the fonts.** I want a **serif-led** design: a serif for titles and headings at minimum; serif body text too if it reads well on a projector.
- Constraints: free Google Fonts; real bold and italic; clear numerals (the deck has stats like "49–71%"); comfortable at projector distance (body text no smaller than about 18 px at 1280×720).
- Don't use Nunito.
- Two fonts are fixed because they come from my website:
  - **Fira Code** (600) for labels: section kickers ("02 · PROBLEM"), badges ("H3", "RQ1"), stats, slide numbers.
  - **Virgil** (the Excalidraw hand-drawn font) for small handwritten annotations only.
- Candidates you might consider, none required: Fraunces, Source Serif 4, Newsreader, Literata, Spectral, Instrument Serif (display only).

### Hand-drawn touches

- **Excalidraw-style diagrams** for: the OCR pipeline highlight, the "Today vs This project" flow, the research loop, the research-question sketches and the H3 sign-flip sketch. Slightly rough strokes, hand-drawn arrows, flat fills.
- **Virgil annotations:** a few short handwritten notes with arrows, e.g. "this is us →" pointing at the recognition step, "the interesting one" next to H3, "not used!" next to latent prediction. At most one or two per slide, never for content the panel must read.
- Everything else (tables, cards, text) stays clean and typographic.

### Chrome

- **Logo:** the PES University **emblem only** (`assets/pes_emblem.png`, the compass circle, no text), small, top-right on every slide. On dark slides give it a light circular backing. Do not use the university's colours anywhere else.
- **No footers:** no section markers at the bottom, no university name, no repeating bottom text. A tiny slide number in a corner is optional; leave it out if it looks like a footer.
- Titles sit in the same place on every content slide.

### Avoid

- PES brand colours (navy and orange) beyond the emblem itself.
- Decorative stripes, underline bars under titles, gradient backgrounds.
- Fake document images. All real images are mine to add.
- Any GPU model, run times or calendar dates on slides.

## 4. Assets

| File | What | Use |
|---|---|---|
| `assets/pes_emblem.png` | PES emblem only (132×132 px, small; scale down, not up) | Every slide, top-right |
| `assets/ocr_pipeline_ppocr.png` | PP-OCR system diagram, from *Dive into OCR* (PaddlePaddle, 2022) | Slide "How OCR works" |
| `assets/ocr_recognition_framework.png` | Four-stage recognition framework, same book | Slide "Inside recognition" |
| `assets/ocr_ctc_vs_attention.png` | CTC vs attention recognisers, same book | Backup slide |
| **[IMAGE]** frames | Real damaged manuscript lines, Welch Labs video screenshots, application photos, my planning notes, a Gantt chart | Design a clear empty frame with room for a one-line credit underneath |

Book figures and video screenshots always carry a small credit line ("Figure: *Dive into OCR*, ch. 5", "Screenshot: Welch Labs").

## 5. Slide types needed

| Type | Used for |
|---|---|
| Title (dark) | Title, subtitle, blank fields for Project ID / Guide / Team, a large **[IMAGE]** frame |
| Section divider (dark) | Big number, section name, 3–5 topic chips |
| Figure + explanation | Book figure across the top, three cards or a table + callout below |
| Diagram + labels | The "cake" diagram (three layers with labels) |
| Timeline grid | 8 history cards in a 4×2 grid, colour-coded by family, plus 3 **[IMAGE]** frames |
| Card row with images | 4–5 cards, each with a small **[IMAGE]** frame, title, one line, a status badge |
| Statement + comparison | A quote card, then two flows: "Today" (neutral) vs "This project" (purple) |
| Two columns | Practical vs Scientific |
| Three cards with sketches | Research questions, each with a small hand-drawn chart |
| Cards + feature sketch | Hypotheses: three small cards + one large card with the sign-flip sketch |
| 2×2 grid + band | Background reasons + "the gap" |
| Table + callout | Prior work table with a dark "our contribution" card |
| Loop diagram | 5-step research loop with a return arrow, plus "fixed vs open" cards |
| Three lists | Experiments: compare / test / data |
| Verdict panel | Scope in/out + feasibility rows with status badges |
| Phase columns + frame | Deliverables per phase + a Gantt **[IMAGE]** frame |
| Closing (dark) | "Thank you", questions, list of backup slides |
| Backup table | Dense tables (up to 8 rows × 4 columns) with a small "BACKUP" tag by the title |
| References | Two slides, small type, numbered |

## 6. Slide-by-slide content

Timings are the speaker's plan (total ≈ 14:50). **Visual:** lines are layout notes, not slide text.

### Main deck

**1 · Title** (dark, 0:15)
- Kicker: UE24CS320A · Capstone Project Phase 1 · Review 1
- Title: **Learning What to Ignore**
- Subtitle: Deriving invariance for self-supervised text recognition
- Fields (left blank): Project ID · Project Guide · Project Team
- **[IMAGE]** a real damaged manuscript line or page (CATMuS Medieval, credited)

**2 · Divider 01: The landscape** (dark, 0:05)
- "Three ideas the rest of the talk builds on"
- Chips: How OCR works · Self-supervised learning · Why documents get damaged

**3 · How OCR works: the general pipeline** (0:45)
- Figure: `ocr_pipeline_ppocr.png`. Caption: "The PP-OCR system: image → text detection → box rectification → text recognition → output. Figure from *Dive into OCR* (PaddlePaddle, 2022), ch. 6."
- Step 1 · Detection: Find where the text is. Regression-based (CTPN, EAST) or segmentation-based (PSENet, DBNet) methods.
- Step 2 · Rectify and orient: Crop each box, straighten it with a perspective fix, turn it the right way up with a direction classifier.
- Step 3 · Recognition **[purple, "this project"]**: Turn each cropped line into characters. The book's verdict: "recognition is more challenging than detection".
- Visual: Virgil note "this is us →" pointing at Step 3.

**4 · Inside recognition: four stages** (0:55)
- Figure: `ocr_recognition_framework.png` (rectify → visual features → sequence → predict). Caption: "The general text-recognition framework. Figure from *Dive into OCR*, ch. 5."
- Table:

| Family | Examples | Idea |
|---|---|---|
| CTC | CRNN, Rosetta | Fast; no character-level alignment needed |
| Attention (seq2seq) | RARE, SAR | More accurate; weaker on very long or short text |
| Transformer | SRN, NRTR, ABINet | Global context instead of LSTMs |
| Rectification | RARE, ASTER | Straighten curved text first |

- Callout **[purple]**: "Where this project plugs in: self-supervised pretraining trains the feature extractor (Feat.) and sequence model (Seq.) on unlabelled lines. Only the small prediction head is then fine-tuned with a few labelled ones."

**5 · Self-supervised learning: the cake** (0:50)
- Left: "Labels are expensive: every training line needs a human transcription. Self-supervised learning (SSL) makes the training signal from the data itself, the way GPT learns by predicting the next word."
- Mini flow: Many unlabelled lines → Pretrain → Few labels → Fine-tune
- **[IMAGE]** Welch Labs, "Yann LeCun's Billion Dollar Bet": the "Intelligence is a cake" slide (4:17)
- Right, the cake diagram (three stacked layers, labels beside each):
  - Cherry · Reinforcement learning: **a few bits** per sample (a reward)
  - Icing · Supervised learning: **10–10,000 bits** per sample (a label)
  - Cake · Self-supervised learning: **millions of bits** per sample, because the model predicts parts of the data itself
  - Small: "After Yann LeCun's NIPS 2016 keynote"
- Visual: draw the cake in the hand-drawn style.

**6 · Self-supervised learning: a short history** (0:50)
- Eight cards, colour-coded by family:
  - 1993 · Siamese networks: two copies of one network compare inputs (Bell Labs) *[joint-embedding]*
  - 2013 / 2018 · word2vec, BERT: predict a word's neighbours; fill in masked words *[text]*
  - 2015–16 · Pretext tasks: context prediction, jigsaw puzzles, colourisation *[joint-embedding]*
  - 2020 · SimCLR, MoCo: contrastive, pull two damaged views together *[joint-embedding]*
  - 2021 · BYOL, Barlow Twins, VICReg, DINO: no negatives needed; avoid "collapse" *[joint-embedding]*
  - 2021–22 · MAE: hide 75% of an image, rebuild the pixels *[reconstruction, highlighted]*
  - 2023 · I-JEPA: predict features, not pixels (world-model family) *[latent prediction]*
  - 2021 → 2026 · SSL for text: SeqCLR (2021) … pixel reconstruction wins for handwriting (2026) *[text, highlighted]*
- Three **[IMAGE]** frames: Welch Labs: Siamese networks (15:16) · representation collapse (17:53) · Barlow Twins (19:54)
- Legend: **Reconstruction**: our method · **Joint-embedding**: control only (VICReg) · **Latent prediction**: not used · Text-specific
- Visual: Virgil note "not used!" near I-JEPA.

**7 · Why documents get damaged** (0:50)
- Five cards, each with a small **[IMAGE]** real example and a badge **[red]**:
  - Show-through: light passes through thin paper · *Modellable*
  - Bleed-through: ink soaks through the page · *Partly*
  - Fading: ink thins; iron-gall ink corrodes · *Partly*
  - Foxing, stains: fungi, oxidation, water · *Approximate*
  - Capture: blur, sensor noise, compression · *Modellable*
- Formula band: **front_seen ≈ front + α · blur_σ(mirror(back))**. "A physical model of show-through. α and σ differ from manuscript to manuscript, and those are the numbers we measure on real pages."

**8 · Divider 02: The problem** (dark, 0:05)
- Chips: Problem statement · Why it matters · Research questions · Hypotheses

**9 · Problem statement** (1:00)
- Quote: "Self-supervised learning must choose which variations a representation should discard, and today that choice, the **corruption recipe**, is made by hand for every new domain. **We derive it instead:** model the main damage types physically, fit their parameters to real historical lines, and test which derived invariances transfer to unseen conditions, and what governs the match."
- Flow, **Today** (neutral grey): A researcher's guess ("blur 0.5–2 px, mask 75%") → Pretrain (on unlabelled lines) → Hope it transfers (retune for each new collection)
- Flow, **This project** (purple): Measure real damage (on real historical lines) → Model + fit (physical form, fitted strength) → Pretrain (corrupt, then rebuild) → Test + explain (unseen damage; measure the match)
- Callout: "'Chosen by hand' ≠ annotation. Pretraining uses no labels; only the corruption recipe is hand-chosen today. The full statement is in backup."

**10 · What's the point of doing this?** (0:50)
- Top quote: Not "another OCR model", but an answer to: **what should a text recogniser learn to ignore, and can we measure that before deployment?**
- Column **Practical**: "Read a new damaged collection with a small model and very few transcribed lines."
  - Archives meet new ink, paper, damage and scanners with every collection
  - Labels are scarcest exactly where damage is worst
  - Gives a **recipe**: physics-based damage models, fitted to real documents
- Column **Scientific**: "Turn a hand-tuned choice into a measured, testable one."
  - Every SSL method decides what to ignore; for text there is no procedure
  - Explains when ignoring damage helps and when it erases the letters
  - Gives a **test set** of real lines tagged by damage, and an **analysis tool**

**11 · Research questions** (0:50)
- RQ1 · Does it help? Do physics-derived, data-fitted corruptions beat plain masking and hand-chosen corruptions? *Sketch: three bars (Plain, Hand-chosen, Derived) for error with few labels; a "?" over Derived.*
- RQ2 · What transfers? Which invariances survive when a damage type, medium, script or capture condition is held out? *Sketch: three falling bars (Damage, Medium, Script); arrow "held out: farther from what we fitted →".*
- RQ3 · What governs the match? Does measured invariance predict how much the error rises under each damage type? *Sketch: scatter of invariance score vs error rise, dashed trend line, "?".*
- Note: "Sketches show what each question measures; they are not results."

**12 · Falsifiable hypotheses** (0:55)
- H1 · Derived beats both baselines: lower error on real historical lines at the smallest label budget. **Wrong if:** the gap is within seed noise.
- H2 · Transfer shrinks with distance: new damage > new medium > new script. **Wrong if:** scripts transfer best.
- H4 · Control: VICReg trained on the same damage loses to our reconstruction model. **Wrong if:** VICReg matches or wins.
- H3 · The sign flip (large card): invariance should **help** for damage that leaves the strokes alone, and **hurt** for damage to the strokes themselves. *Sketch, two mini-charts: "Background damage (bleed-through, stains, blur)": more invariance → smaller error rise (line falls). "Stroke damage (ink loss, merged strokes, diacritics)": more invariance → larger error rise (line rises).* **Wrong if:** one trend holds for all damage types, or there is no trend at all.
- Visual: "Wrong if" lines in red; Virgil note "the interesting one" by H3.

**13 · Divider 03: Background** (dark, 0:05)
- Chips: Why this problem · Why pixels matter for text · What exists, and the gap

**14 · Background: why this problem** (0:50)
1. SSL learns what its corruptions tell it to ignore. Pick the wrong set and the model throws away what the task needs. Different tasks want opposite invariances (Ericsson et al., 2022).
2. For text, the recipe is chosen by hand. Augmentations are chosen to "best fit the nature of the data" (IJCV survey, 2025); finding them "can be challenging, often requiring substantial effort and expertise" (Baloun et al., 2025).
3. The method shifted in Sept 2026. Pixel reconstruction beat contrastive and JEPA pretraining on six handwriting benchmarks (arXiv 2609.35473).
4. The closest analysis is outside text. Augmentation–corruption similarity predicts robustness, but only for natural images (Mintun et al., 2021).
- Band: **The gap:** nobody has derived the corruption recipe from physical models fitted to real damaged documents, or measured whether trained invariance matches the damage met at test time, for text.

**15 · Why pixels matter for text** (0:50)
- Left, "The argument against pixels": LeCun's case for JEPA: predicting raw pixels wastes effort on unpredictable detail (blurry generated video), so models should predict in feature space instead. **[IMAGE]** Welch Labs: "Blurry images in generative video" (8:00), "Why the output is blurry" (11:16)
- Right, "Why text is different" **[purple]**: in handwriting the "detail" **is** the signal: one dot or stroke decides the letter. The signal lives in high-variance pixel directions, and only pixel reconstruction kept per-character position (2026). **[IMAGE]** close-up of a handwritten word where one dot or stroke changes the letter
- Band: So we use **pixel reconstruction**, and the open question becomes **which damage it should learn to see through.**

**16 · What exists, and the gap** (1:00)

| Prior work | What it leaves open |
|---|---|
| Lacuna Reconstruction (NAACL Findings 2022) | Corruptions not studied |
| Text-DIAE (AAAI 2023) | Degradations hand-chosen |
| Kišš & Hradiš (ICDAR 2024) | Not always better than supervised transfer |
| LoGo-HTR (WACV 2026) | No damage modelling; contrastive |
| Garrido-Munoz & Calvo-Zaragoza (2026) | Which corruptions to see through |
| Ericsson 2022 · Mintun 2021 | Invariance studied on natural images only |
| Augraphy · recto–verso models | Simulators, not fitted, not used for SSL |

- Card **[dark, purple accent]** "Our contribution": corruptions derived from physical models fitted to real damaged documents, tested on held-out damage, media and scripts, with a test of whether trained invariance predicts the error.
- Card "What is not new": SSL for text, degradation augmentation, damage simulators. We build on them; the full comparison is in backup.

**17 · Divider 04: Approach and plan** (dark, 0:05)
- Chips: Research loop · Experiments and data · Scope and feasibility · Applications · Deliverables

**18 · Approach: an iterative research loop** (0:50)
- Loop: ① Measure (contrast, blur, noise, stroke width, bleed on real lines) → ② Model (physical form + fitted parameters) → ③ Pretrain (corrupt the input, rebuild the clean line) → ④ Evaluate (on held-out damage, media, scripts) → ⑤ Analyse (does invariance predict the error?) → return arrow: "refine the damage models and repeat"
- Card "Fixed from the start": the research questions and hypotheses · held-out tests on real damaged lines · strong baselines, incl. supervised transfer · reporting protocol (image height, charset)
- Card "Decided by evidence, loop by loop": which damage types to model, and how · backbone and model size · masking ratio and corruption strength · label budgets and test conditions
- Visual: the loop is the showcase hand-drawn diagram.

**19 · Experiments and data** (0:50)
- What we compare: supervised only · plain masked reconstruction · + hand-chosen corruptions · **+ derived corruptions** · VICReg on derived (control) · supervised transfer · off-the-shelf OCR / VLM (reference)
- Where we test: clean modern handwriting · same, with a held-out damage type · real damaged lines, tagged by damage · scene text (camera capture) · an unseen script (Indic / Arabic). Metrics: character error rate, invariance scores, their correlation.
- Data we use **[green]**: IAM (clean handwriting, ≈10k lines) · CATMuS Medieval (≈195k real historical lines) · HTR-United (more historical sets) · IIIT-Indic / Muharaf (unseen scripts) · scene-text sets (camera capture)
- Callout: "Same backbone and fine-tuning for every model: only what the model was trained to ignore changes. The one new data task: tag a few hundred real lines by type of damage (not their text)."

**20 · Scope and feasibility** (0:50)
- In scope: recognition of cropped text lines · small encoders; pretraining is what we change · 3–5 damage types with physical models · modern + historical lines, one unseen script or medium
- Out of scope (for now): detection / line segmentation (keeps reading errors clean; a follow-up) · large VLMs as the object of study · many languages at once
- Feasibility rows (badge colour in brackets):
  - Data · Fits [green] · free, line-level datasets for every role
  - Code · Fits [green] · open code: pero-pretraining, PARSeq, Augraphy
  - Compute · Fits [green] · small models; free tiers first, paid GPUs only to scale up
  - Novelty · Medium risk [amber or neutral] · the gap looks open; SSL for text is crowded
  - Main risk · Real [red] · SSL may not beat supervised transfer, so that baseline is mandatory

**21 · Applications and use cases** (0:35)
- Four cards, each with an **[IMAGE]**: Archives and libraries (read a new collection without mass labelling) · Low-resource scripts (learn mostly from unlabelled pages) · Damaged records (faded or bled-through registers, letters, files) · Camera capture (phone photos: blur, shadows, uneven light)
- Band: **Beyond OCR:** measure the nuisance, model it, fit it, check the match: the same recipe could serve any field where damage is physically modellable.

**22 · Deliverables and timeline** (0:45)
- Phase I: literature survey, final formulation · data pipeline · supervised baseline · damage-measurement tool · first pretraining loop
- Phase II: physical damage models, fitted · real lines tagged by damage · all pretraining runs + control · held-out evaluation (RQ1, RQ2)
- Phase III: invariance–error analysis (RQ3) · script and medium transfer · ablations and seeds · paper (ICDAR workshop → main track / IJDAR), code and data release
- **[IMAGE]** Gantt chart (I'll make it): phases I–III, dates from the department calendar. Critical path: the damage models in Phase II.

**23 · Thank you** (dark)
- Kicker: Learning What to Ignore
- "Thank you" · "Questions and suggestions are welcome"
- Small: Backup: full problem statement · recognition algorithms · how this problem was found · hypotheses in full · related work · what is new and what is not · datasets · compute options · challenges · effort plan · references

### Backup slides (small "BACKUP" tag next to each title)

**B1 · Problem statement (full text)**
> Self-supervised learning requires choosing which input variations a representation should discard, yet this choice is made by hand and retuned for every new domain. **We ask whether it can be derived instead.**
> For handwriting, reconstruction pretraining now beats contrastive and joint-embedding methods, so the choice moves from an augmentation list to the corruptions a masked or denoising autoencoder must see through. Text images are an ideal testbed: the variation to discard (degradation, medium, script, capture) is severe, structured and often physically modellable, while labels are scarcest where it is worst.
> **We model the main damage types physically, fit their parameters to measured statistics of real historical lines, then investigate which derived invariances transfer to unseen conditions, and what governs the match between trained invariance and encountered variation.**

**B2 · Recognition algorithms: CTC vs attention**: figure `ocr_ctc_vs_attention.png`. Caption: "Left: CRNN with a CTC transcription layer. Right: an attention-based sequence-to-sequence decoder. Figure from *Dive into OCR* (PaddlePaddle, 2022), ch. 3."

**B3 · How this problem was found**: six-step timeline:
1. Explore (Aug 2026): mapped 13 interests against the literature
2. Pick: physics-derived augmentation for damaged manuscripts
3. Get critiqued (Oct 2026): peer review; claims too strong, maths tightened
4. Reality-check: a Sept 2026 paper showed pixel reconstruction wins for handwriting
5. Reframe: physics-derived corruptions for a reconstruction model
6. Keep checking (ongoing): new related work folded in, claims kept honest

Below it, three **[IMAGE]** frames: my planning memo (13 directions) · the peer critique · literature notes / the Sept 2026 paper.

**B4 · Hypotheses in full**

| # | Hypothesis | What would falsify it |
|---|---|---|
| H1 | Derived corruptions lower CER on real historical lines at the smallest label budget, compared with both plain MAE and hand-chosen corruptions | The gap is within seed spread, or hand-chosen corruptions match it |
| H2 | Transfer shrinks as conditions move away from what was fitted: held-out damage > medium > script | Script transfer equals or beats damage transfer |
| H3 | Invariance helps when a damage type leaves the character-carrying pixels alone, and hurts when it overlaps them (ink loss, merged strokes, diacritics): a sign flip between the two groups | One monotone relationship across all families, or no correlation |
| H4 (control) | A joint-embedding model (VICReg) trained on the same derived damage loses to derived-corruption MAE, reproducing arXiv 2609.35473 at small scale | VICReg matches or wins, so the reconstruction choice needs rethinking |

**B5 · Related work (1/2): SSL for text and documents**

| Work | What it does | What it leaves open |
|---|---|---|
| Vogler et al., NAACL Findings 2022 (Lacuna Reconstruction) | Masked-region SSL on historical lines; with 30 labelled lines, CER 60.4 → 23.7 on one manuscript set | Corruptions not studied; invariance claimed, not measured |
| Kišš & Hradiš, ICDAR 2024 | SSL pretraining on historical lines (masked and VICReg); code public | Not consistently better than transfer from a related labelled domain |
| Text-DIAE, AAAI 2023 | Degradation-invariant autoencoder for text | Degradations hand-chosen |
| SeqCLR, DiG, CCD (2021–23) | Contrastive, masked and distillation SSL for text | Augmentation choice ad hoc; heavy compute |
| LoGo-HTR (Mitra, Mondal & Jawahar), WACV 2026 | Contrastive + decorrelation SSL for handwriting; 10M unlabelled word images | No damage modelling; contrastive, which 2609.35473 finds weaker for HTR |
| Garrido-Munoz & Calvo-Zaragoza, 2026 | Pixel reconstruction beats contrastive / JEPA on 6 HTR benchmarks | Which corruptions to train it to see through |
| Baloun et al., IJDAR 2025 | Barlow Twins SSL for historical page segmentation; compares augmentations by trial | Segmentation, not recognition; augmentations still hand-chosen |

**B6 · Related work (2/2): augmentation, invariance, damage**

| Work | What it does | What it leaves open |
|---|---|---|
| Ericsson et al., BMVC 2022 | Measures invariance; different tasks want opposite invariances | Natural images only |
| Mintun et al., NeurIPS 2021 | Augmentation–corruption similarity predicts robustness | Natural images, supervised |
| Augraphy (2022), DocCreator | Simulators of document damage | Not fitted to real statistics, not studied for SSL |
| Salerno & Tonazzini (recto–verso models) | Physical models of show-through and bleed-through | Used for restoration, not for pretraining |
| IJCV survey, 2025 | Map of SSL for text recognition | No augmentation-selection procedure; inconsistent protocols |

Note under the table: "Evidence that reading damaged historical text is unsolved: on four sets of Islamicate manuscripts, Google Cloud OCR had 49–71% character error rate; pretraining on unlabelled lines plus only 30 labelled lines brought it to 15–46% (Vogler et al., 2022)."

**B7 · What is new, and what is not**

| Not new (we build on it) | New (not found in prior work, as of Oct 2026) |
|---|---|
| SSL for text recognition (SeqCLR 2021 onwards; Lacuna Reconstruction 2022; LoGo-HTR 2026) | Corruption ranges for text SSL **fitted to measured statistics** of real damaged lines, through physics-based damage models |
| Degradation-style augmentation in text SSL (Text-DIAE 2023) | Evaluation with **whole damage families, media and scripts held out**, on real lines tagged by damage type |
| Document damage simulators and physical models (Augraphy, recto–verso models) | Testing whether **measured invariance predicts the error cost** of each damage type |
| Fitting simulators to real data in other fields (sim-to-real robotics, learned augmentation) | The predicted **sign flip**: invariance that helps for background damage but erases letters for ink damage |

Small: "'Not found' is not 'proven absent': the literature search continues through Phase I."

**B8 · Datasets and tools**

| Role | Dataset / tool | Size | Licence / access |
|---|---|---|---|
| Clean labelled handwriting | IAM-line (Teklia, Hugging Face) | ≈10.4k lines | Free; cite IAM terms (research use) |
| Real damaged historical lines | CATMuS Medieval (Hugging Face) | ≈195k lines, multilingual | CC-BY-4.0 |
| More historical sets | HTR-United catalogue | Dozens; filter by script / period | Per-dataset licence |
| Unseen script | IIIT-INDIC-HW-WORDS; Muharaf (Arabic) | 872k words, 10 scripts; 36,311 lines | Ask authors; public part only |
| Unseen capture | Scene-text test sets via PARSeq (IIIT5k, IC13, IC15) | Standard benchmarks | Free |
| Damage models | Own physics-based models + Augraphy | Show-through, bleed, fading, stains, capture | MIT (Augraphy) |
| SSL / HTR code | pero-pretraining, PARSeq, PyTorch | Small encoders | BSD-2 / Apache-2.0 |

**B9 · Compute options**

| Option | Cost | Use |
|---|---|---|
| Personal GPU, Kaggle notebooks, Google Colab free tier | **Free** | Development, debugging, small runs |
| University / department GPUs | **Free**, if available | Longer pretraining runs |
| Research credit programmes (cloud credits, TPU Research Cloud) | **Free**, on approval | Scaling up, if approved |
| Colab Pro / Pro+ | **Paid** | Longer sessions, better GPUs |
| Cloud GPU rental (AWS, GCP, Azure, RunPod, Lambda, vast.ai) | **Paid**, per hour | Only if we scale beyond small models |
| IndiaAI subsidised compute | **Paid, subsidised** (check eligibility) | Scaling up |

Note: "The core study is designed around small models, so the free options cover it; paid options are only for scaling up."

**B10 · Challenges and mitigations**

| Challenge | Mitigation |
|---|---|
| SSL may not beat supervised transfer | Mandatory supervised-transfer baseline; the invariance analysis is publishable even as a negative result |
| "You only learned your own simulator" | Always also test on real damaged lines, tagged by damage type |
| Few damage families = few points to correlate | Compute invariance per family × severity level |
| Leakage into the fitted parameters | Fit statistics on pretraining data only; official writer-independent splits |
| Some damage has no clean physical model | Use physical models where they exist (show-through, capture); clearly label approximate ones |
| "Why not just use a big VLM?" | VLM reference point on the same damaged lines |
| Active groups work in this exact area | Move fast; workshop paper first, then the full version |
| Inconsistent protocols across papers | Fix image height, charset and Unicode normalisation on day one |

**B11 · Effort plan, success criteria, publication**

| Workstream | Tasks | Phase | Effort | Owner |
|---|---|---|---|---|
| Data and baselines | Loaders, charset, splits, supervised baseline, CER tooling | I | ≈20% | |
| Damage modelling | Measure real damage, physical models, parameter fitting, tag real lines | I–II | ≈25% | |
| SSL pretraining | Plain, hand-chosen and derived pretraining; VICReg control | II | ≈25% | |
| Evaluation and analysis | Fine-tuning, held-out tests, invariance scores, correlation, transfer | II–III | ≈20% | |
| Writing and release | Weekly reports, phase reports, paper, code and data release | I–III | ≈10% | |

- Success criteria: H1, derived beats both baselines by more than seed spread · H3, the invariance–error correlation flips sign · a negative H1 still yields the analysis as a finding
- Publication and release: ICDAR workshop first, then ICDAR main track or IJDAR · release code, fitted damage parameters, tagged lines

**B12 · References (1/2)**
1. Garrido-Munoz & Calvo-Zaragoza. *Handwritten Text Recognition Lives in the High-Pixel Variance Subspace.* arXiv:2609.35473, 2026.
2. Penarrubia, Valero-Mas & Calvo-Zaragoza. *Self-Supervised Learning for Text Recognition: A Critical Survey.* IJCV, 2025.
3. Kišš & Hradiš. *Self-supervised Pre-training of Text Recognizers.* ICDAR, 2024.
4. Vogler, Allen, Miller & Berg-Kirkpatrick. *Lacuna Reconstruction: Self-Supervised Pre-Training for Low-Resource Historical Document Transcription.* Findings of NAACL, 2022.
5. Mitra, Mondal & Jawahar. *Learning Beyond Labels: Self-Supervised Handwritten Text Recognition (LoGo-HTR).* WACV, 2026.
6. Baloun, Prantl, Lenc, Martínek & Král. *On Self-Supervision in Historical Handwritten Document Segmentation.* IJDAR, 2025.
7. Souibgui et al. *Text-DIAE: A Self-Supervised Degradation Invariant Autoencoder for Text Recognition and Document Enhancement.* AAAI, 2023.
8. Ericsson, Gouk & Hospedales. *Why Do Self-Supervised Models Transfer? Investigating the Impact of Invariance on Downstream Tasks.* BMVC, 2022.
9. Mintun, Kirillov & Xie. *On Interaction Between Augmentations and Corruptions in Natural Corruption Robustness.* NeurIPS, 2021.
10. Aberdam et al. *Sequence-to-Sequence Contrastive Learning for Text Recognition (SeqCLR).* CVPR, 2021.
11. Groleau et al. *Augraphy: A Data Augmentation Library for Document Images.* arXiv:2208.14558.
12. Salerno & Tonazzini. *Highly Degraded Recto-Verso Document Image Processing and Understanding.* ERCIM News 95, 2013.
13. Clérice et al. *CATMuS Medieval: a multilingual large-scale cross-century dataset in Latin script for HTR.* ICDAR, 2024.
14. Marti & Bunke. *The IAM-database: an English sentence database for offline handwriting recognition.* IJDAR, 2002.
15. Li, Liu, Guo, Yin et al. *Dive into OCR.* PaddlePaddle, 2022.

**B13 · References (2/2)**
16. Bromley, Guyon, LeCun, Säckinger & Shah. *Signature Verification using a "Siamese" Time Delay Neural Network.* NIPS, 1993.
17. Mikolov et al. *Efficient Estimation of Word Representations in Vector Space (word2vec).* 2013.
18. Devlin et al. *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.* NAACL, 2019.
19. Doersch, Gupta & Efros. *Unsupervised Visual Representation Learning by Context Prediction.* ICCV, 2015.
20. Chen et al. *A Simple Framework for Contrastive Learning of Visual Representations (SimCLR).* ICML, 2020.
21. He et al. *Momentum Contrast for Unsupervised Visual Representation Learning (MoCo).* CVPR, 2020.
22. Grill et al. *Bootstrap Your Own Latent (BYOL).* NeurIPS, 2020.
23. Zbontar et al. *Barlow Twins: Self-Supervised Learning via Redundancy Reduction.* ICML, 2021.
24. Bardes, Ponce & LeCun. *VICReg: Variance-Invariance-Covariance Regularization for Self-Supervised Learning.* ICLR, 2022.
25. Caron et al. *Emerging Properties in Self-Supervised Vision Transformers (DINO).* ICCV, 2021.
26. He et al. *Masked Autoencoders Are Scalable Vision Learners (MAE).* CVPR, 2022.
27. Assran et al. *Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture (I-JEPA).* CVPR, 2023.
28. LeCun. *Predictive Learning* (the "cake" slide). NIPS 2016 keynote.
29. VLM OCR hallucination evidence: arXiv:2601.03714 (DeepSeek-OCR on random strings); TextHalu-Bench, arXiv:2506.05551.
30. Video: Welch Labs. *Yann LeCun's Billion Dollar Bet* (Part 1), YouTube, 2025.
