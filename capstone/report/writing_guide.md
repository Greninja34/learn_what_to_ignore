# How to write the Phase-1 report in your own words

The college checks the report with Turnitin: a similarity score plus an AI-writing indicator, with a limit of 15% that includes AI content. The draft in `report.md` was written with Claude, so its prose must not be submitted as it is. The reliable way to pass is to write the text yourselves from the facts. This guide shows how to do that quickly.

## 1. Work from the skeleton, not the draft

1. Open `key_points.md`. It lists the claims, numbers and citations for each chapter as bullets, with no prose.
2. Close `report.md`. Writing next to the draft pulls you into its sentences, and that is what the checker sees.
3. Write each section from the bullets, as if you were explaining it to a classmate. Keep it rough and fix it later.
4. Only then open the draft to check that no fact or number is missing. Copy numbers, tables and references, never sentences.

Split the chapters by owner, using the effort plan in the report: Arvind writes data and baselines, Atharv the damage chapter, Vignesh the SSL and results chapters, and Rohit evaluation and the plan. One person then reads everything for consistency.

## 2. What makes text read as your own

- **Say what you did and why.** Write things like "We first tried a small ViT; it memorised the 648 labelled lines, so we switched to the CRNN's own CNN." Only you know these decisions, and they are the most original part of the report.
- **Use plain, uneven sentences.** Real writing mixes short and long sentences and sometimes repeats a word. Uniform, polished paragraphs are what AI detectors pick up.
- **Be specific.** Write "33.8% to 31.6% CER on CATMuS, 3 seeds", not "a notable improvement".
- **Explain each figure in one or two sentences**: what it shows, then what it means for the research question.
- **Paraphrase from understanding.** Read the paper's point, close it, and write the point down. Swapping words for synonyms keeps the source's sentence structure, and both the similarity and AI checks catch it.
- **Quote exactly, in quotation marks, with the citation,** when the wording matters (for example the research-gap definition). Keep direct quotes rare.
- **Cite every claim that isn't yours** (IEEE style, as in the reference list).

## 3. Checking before you submit

- **Use the college's own check.** The report goes to the librarian with the guide in CC. Ask the librarian or the guide for a draft Turnitin run before the final submission; many institutions allow one. That is the only check that predicts the real result.
- **Free AI detectors do not predict Turnitin.** Tools such as GPTZero or ZeroGPT often disagree with Turnitin and with each other, so tuning the text until one of them says "human" proves nothing.
- **Don't use AI "humanizer" or paraphrasing tools.** Running AI text through a rewriter is still submitting AI text, and colleges treat it as misconduct if found. Turnitin also reports AI-paraphrased text separately (check the current Turnitin documentation). It is the riskiest option and saves the least time.
- **Ask what the check excludes.** Many setups leave out the reference list, quoted text and small matches. Ask the librarian how it is configured; it changes how much the tables and references count.

## 4. Order of work (about a day for four people)

1. Each owner writes their chapters from `key_points.md`: 2–3 hours.
2. Swap chapters and read each other's for clarity and missing facts: 1 hour.
3. Paste the text into `report.md` (keep the tables, figures and reference list) and rebuild with `python capstone/report/build_pandoc.py`.
4. Get the draft Turnitin check, fix any flagged passages by rewriting them yourselves, then submit.
