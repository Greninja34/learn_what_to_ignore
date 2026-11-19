# Self-checking the capstone report before Turnitin (Nov 2026)

**The main point:** only Turnitin can tell you what Turnitin will say. **No free detector has been shown to match Turnitin's AI score** ([aidetectors.io](https://www.aidetectors.io/blog/ai-detector-closest-to-turnitin)). Use free tools as rough signals and get a real Turnitin draft check through the college.

## 1. Getting a real Turnitin check

- **Turnitin Draft Coach** (add-in for Google Docs or **Word for the web**). It compares your draft against Turnitin's student-paper repository, journals and the web, and **does not add your draft to the repository** ([Turnitin](https://helpcenter.turnitin.com/hc/en-us/articles/27811948754445-Will-checking-my-document-in-Turnitin-Draft-Coach-save-it-to-a-repository)). It usually allows **3 similarity checks per document** ([Mohawk](https://atf.mohawkcollege.ca/hc/en-ca/articles/50384857570452-What-is-Turnitin-Draft-Coach)). It needs an institutional licence. **I found no source showing that Draft Coach gives an AI score** (unverified).
- **Library or guide check.** Indian libraries often run Turnitin, DrillBit or Urkund a limited number of times, for example MANUU allows at most 3 ([MANUU](https://manuu.edu.in/sites/default/files/Library/MANUU-SimilarityProcedure.pdf)), as part of the [UGC 2018 regulations](https://casrai.org/guides/ugc-india-anti-plagiarism-regulations-2018). iThenticate, usually for faculty, also shows an AI indicator ([guide](https://guides.ithenticate.com/hc/en-us/articles/27835303398541-AI-writing-detection-in-the-new-enhanced-Similarity-Report-view)).

### What to ask the librarian

1. "Do we have Draft Coach? Is it for Docs or Word online, and which account do I use?"
2. "Can you run a draft check that shows the **AI writing indicator** as well as similarity?"
3. "Can drafts be checked with **'no repository'**, so my final version doesn't match against them?"
4. "Does the 15% limit exclude the bibliography and quotes? Is AI counted separately from similarity?"
5. "How many checks am I allowed, and which software does the final check use?"

## 2. Tools

Free limits come mostly from third-party roundups. **Verify them on each vendor's site.**

| Tool | Free limit | What it checks | Stores text? | Agreement with Turnitin | Source |
|---|---|---|---|---|---|
| **Draft Coach** | ~3 checks per document | Similarity against web, journals and student papers | No | It *is* Turnitin (no AI score) | [Turnitin](https://helpcenter.turnitin.com/hc/en-us/articles/27811948754445-Will-checking-my-document-in-Turnitin-Draft-Coach-save-it-to-a-repository) |
| **Pangram** | ~2,000 words/day | AI | Unverified | Not measured directly. Best in independent studies: about 0 FPR on medium and long text, and closest to ground truth. One UMD test found 2.7% FPR | [Jabarian & Imas 2025](https://www.nber.org/papers/w34223); [Springer 2026](https://link.springer.com/article/10.1007/s40979-026-00226-w) |
| **GPTZero** | ~10,000 words/month | AI | Unverified | FPR ≤1% on long text, ~2.4% on short text. Underestimated AI content in the Springer study. Blogs call it the "closest" to Turnitin (unverified) | [Booth Review](https://www.chicagobooth.edu/review/2025/december/do-ai-detectors-work-well-enough-trust) |
| **QuillBot** | 1,200 words × 6 scans/day | AI | Unverified | No independent data | [roundup](https://plagiarismcheckerplus.com/guides/best-free-ai-detectors) |
| **Copyleaks** | ~25,000 characters/scan | AI | Unverified | Underestimated AI content in the Springer study | [fast.io](https://fast.io/resources/free-ai-detector-tools-2026/) |
| Scribbr AI | Reports conflict | AI | Unverified | Claims that it uses Turnitin's model are unverified | [fast.io](https://fast.io/resources/scribbr-ai-detector-review-2026/) |
| ZeroGPT, Sapling | 15,000 / 2,000 characters | AI | Unverified | No good data and many reports of false flags. **Avoid** | [stack-junkie](https://stack-junkie.com/blog/zerogpt-vs-gptzero-free-ai-detector-comparison) |
| Originality.ai, Winston | No free plan found | AI + plagiarism | – | Originality.ai: low FPR but more missed AI text | [Booth Review](https://www.chicagobooth.edu/review/2025/december/do-ai-detectors-work-well-enough-trust) |
| **Scribbr plagiarism** | Free preview, full report paid | Web + publications (Turnitin-powered), **no student papers** | Not added to a database, and you can delete it | Close to Turnitin, minus student-paper matches | [Scribbr](https://help.scribbr.com/hc/en-us/articles/39232872423319-How-does-the-Scribbr-Plagiarism-Check-work) |
| Grammarly, Quetext, DupliChecker | Small free checks | **Web only** | Vendors say no (not audited) | Miss journals and student papers | [Grammarly](https://www.grammarly.com/plagiarism-checker) |

**Privacy:** a stored Turnitin draft (for example a library check sent to the repository) can make your final version match against it. Ask for "no repository", and avoid unknown free checkers.

**What students and faculty say online** (Reddit blocked my fetches, so this comes from secondary sources and is **unverified**):
- r/Professors reportedly prefers Pangram and distrusts Turnitin's AI score while trusting its similarity check ([roundup](https://gptone.me/best-ai-detector-reddit)).
- Reviews of GPTZero and ZeroGPT report many false flags on human writing ([Trustpilot](https://uk.trustpilot.com/review/gptzero.me)).
- Some universities disabled Turnitin's AI detector ([Vanderbilt](https://www.vanderbilt.edu/brightspace/2023/08/16/guidance-on-ai-detection-and-why-were-disabling-turnitins-ai-detector/)).

"Humanizer" and paraphrase-to-evade tools exist. Using them on AI-written text is misconduct, and they are not covered here.

## 3. False positives

- **Non-native writers.** Older detectors flagged **61% of human TOEFL essays** ([Liang et al. 2023](https://arxiv.org/abs/2304.02819)). Newer tools claim far lower rates (vendor claims).
- **Formulaic text.** Turnitin says repetitive style, lists, outlines, tables and code can trigger flags. It analyses only prose, with a **minimum of 300 words** ([Turnitin](https://help.turnitin.com/ai-writing-detection.htm)).
- **Low scores.** Scores below 20% are shown as "*%" because that range is unreliable ([Turnitin](https://www.turnitin.com/blog/ai-writing-detection-update-from-turnitins-chief-product-officer)).
- **Short text.** All tools are unreliable under about 50 words.

**What helps when the writing is genuinely yours:**
- Keep version history, notes and dated drafts.
- Write specifics (your numbers, decisions, failures) instead of generic definitions and template phrases.
- Cite properly and ask for the bibliography to be excluded.
- Avoid whole-paragraph AI "rewrite" features. This is my inference, not tested by a study.
- Disclose any permitted AI use.

## 4. Workflow

1. Write in Google Docs or Word online so you keep version history.
2. Check each chapter in Pangram and cross-check in GPTZero. Revise a section only if **both** flag it, and don't chase 0%.
3. Check similarity with Draft Coach (1 of your 3 checks), or with Scribbr's preview if you don't have Draft Coach.
4. About 1–2 weeks before the deadline, ask for a library Turnitin draft check with the AI indicator and **no repository**.
5. Fix the issues, run a final Draft Coach check, and keep screenshots of the reports and your version history.
