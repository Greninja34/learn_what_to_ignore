# Keep the SSL question, run two side bets

Your #1 project has a final, defensible problem statement: **derive the corruptions that a masked or denoising autoencoder learns to see through by fitting them to measured statistics of real historical lines, then test which of them transfer to unseen degradations, media, scripts and capture conditions, and whether invariance scores predict the CER cost.** That wording takes on board the September 2026 result that pixel-reconstruction pretraining beats contrastive and JEPA methods on all six HTR benchmarks tested ([arXiv 2609.35473](https://arxiv.org/abs/2609.35473)). It also keeps your original voice. Both side ideas are doable on your laptop, but only in their sharper forms. The Rubik's-cube idea is not "too much data hurts", because nobody has shown that. It is about **which distances the training states come from and how they are labelled, at a fixed budget**, and I confirmed in 36 seconds on a CPU that walk-length labels are badly biased on the 2×2×2 cube. The OCR-hallucination idea cannot simply re-show that VLMs "fix" nonwords into real words, because several 2026 papers already did that. Its open part is **which ground-truth-free signal flags those misreads, broken down by legibility and word type.** On benchmarks, you are half right. The method in those papers really is basic. But the ones at good venues won on real, licensed, human-checked data, broad evaluation and senior co-authors, and the "very basic Korean" ones are mostly arXiv preprints or workshop papers. A careful Indian-language document benchmark is a realistic target for a workshop, for ICDAR or for IJDAR. It is not a realistic target for CVPR.

## 1. The final problem statement

**Title:** Learning What to Ignore: Deriving Invariance for Self-Supervised Text Recognition

**Statement (≈130 words, your voice):**

> Self-supervised learning requires choosing which input variations a representation should discard, yet this choice is made by hand and retuned for every new domain. We ask whether it can be derived instead. For handwriting, reconstruction pretraining now beats contrastive and joint-embedding methods, so the choice moves from an augmentation list to the corruptions a masked or denoising autoencoder must see through. Text and document images are an ideal testbed: the variation to be discarded — degradation, medium, script, capture conditions — is severe, highly structured, and often physically modellable, while labels are scarcest where it is worst. We fit corruption ranges to measured statistics of real historical lines, then investigate which sources of derived invariance transfer to conditions unseen during pretraining, and what governs the match between trained invariance and encountered variation.

**Research questions.**
**RQ1.** Does a masked or denoising autoencoder whose input corruptions are *fitted to real line statistics* beat (a) plain masked autoencoding and (b) the same model with hand-picked, SeqCLR-style corruptions, at 1%, 10% and 100% of the labels?
**RQ2.** Which sources of derived invariance transfer when you hold out a whole degradation family, a medium (print or scene text), a script, or a capture condition?
**RQ3.** What governs the match? Specifically, do per-family invariance scores and overlap with the character-carrying pixel subspace predict how much CER rises under each held-out family?

| # | Falsifiable hypothesis | What would falsify it |
|---|---|---|
| H1 | Derived corruptions lower CER on real historical lines at 1% labels compared with both plain MAE and hand-picked MAE | The gap is within seed spread (3 seeds), or hand-picked corruptions match it |
| H2 | Transfer shrinks as conditions move away from what was fitted: held-out degradation > medium > script | Script transfer equals or beats degradation transfer |
| H3 | Invariance helps when a degradation lies **outside** the high-variance, character-carrying pixel directions, and hurts when it overlaps them (ink loss, merged strokes, diacritics). This shows up as a sign flip in the correlation between invariance score and CER increase across the two groups | One monotone relationship holds across all families, or there is no correlation |
| H4 (control) | VICReg trained on the same derived set loses to derived-corruption MAE, which reproduces 2609.35473 at small scale | VICReg matches or wins. That would mean the reframing itself needs rethinking |

**Why this is new, and what you must cite.** **Text-DIAE** already trains a degradation-invariant autoencoder for text, but with hand-picked degradations, and it found masking the most useful one ([AAAI 2023](https://ojs.aaai.org/index.php/AAAI/article/download/25328/25100); summarised in the [IJCV survey](https://arxiv.org/html/2407.19889v2)). Mintun et al. link augmentation–corruption similarity to robustness, but only on natural images ([arXiv 2102.11273](https://arxiv.org/abs/2102.11273)). Ericsson et al. supply the invariance measures (Mahalanobis distance and whitened cosine between clean and transformed features), but not for text ([arXiv 2111.11398](https://arxiv.org/pdf/2111.11398v2)). The IJCV survey itself says augmentations are chosen to "best fit the nature of the data" and offers no procedure for choosing them ([survey](https://arxiv.org/html/2407.19889v2)). Your contribution is the *derivation* step plus the *match measurement* for text. One caution: I have only seen the abstract of 2609.35473, so read its exact definition of the high-variance-subspace measure before you build H3 on it. Also, a handful of degradation families gives very few points to correlate, so compute the scores per family × severity level.

## 2. The cube idea: label bias is a 36-second fact, so the paper is what follows from it

**Taken vs open**

| Already done | Still open |
|---|---|
| Uniform scramble length k ∈ [1,30] (DeepCubeA) ([PDF](https://deepcube.igb.uci.edu/static/files/SolvingTheRubiksCubeWithDeepReinforcementLearningAndSearch_Final.pdf)) | The **shape** of the training distribution over *true* distance as a variable at fixed budget. Every paper uses uniform k or all prefixes up to K_max, and CayleyPy says it does not study K_max ([arXiv 2502.13266](https://arxiv.org/html/2502.13266v1)) |
| Data scaling: EfficientCube's power law keeps rewarding more data ([arXiv 2106.03157](https://arxiv.org/pdf/2106.03157v5)). CayleyPy is flat at 4B/8B/16B states (21.16/21.12/21.19 moves) ([arXiv 2502.13266](https://arxiv.org/html/2502.13266v1)) | A factorial of label source × distribution, with an exact BFS oracle, on a puzzle where every distance is known |
| "More random walks does not always improve the model". Non-backtracking walks are essential. Spearman correlation vs true distance on small permutation (LRX) graphs ([arXiv 2502.18663](https://arxiv.org/html/2502.18663v2)) | Per-distance-bin bias and its effect on search (nodes expanded, optimality) |
| Train/deploy state mismatch causes "heuristic depression" ([arXiv 2511.10264](https://arxiv.org/html/2511.10264)). Exact-shortest-path GFlowNets ([arXiv 2603.01786](https://arxiv.org/abs/2603.01786)). Overestimating heuristics ([arXiv 2606.04860](https://arxiv.org/abs/2606.04860)) | Whether more walk-labelled data ever *hurts* specific distance bins (nobody shows harm, only saturation) |

**Sharp framing.** *At a fixed sample budget, the distribution of training states over true distance and the source of their labels, not their number, determine heuristic accuracy where search needs it.* This is what "too much data is a bottleneck" was reaching for, stated so it can be tested.

**I ran the pilot.** The script below builds the full 2×2×2 table (**3,674,160 states, God's number 14 in the quarter-turn metric**, matching the known values) and asks what true distance a random walk of length k actually reaches. For simple walks, k = 10 lands at a mean true distance of **6.44**, and 91% of those states are closer than 10. Even with non-backtracking walks (CayleyPy's choice), k = 10 gives a mean of **8.63**, and **52%** are mislabelled as too far. Beyond k ≈ 14, labels keep rising while true distance flattens near 10.5. So H1 from the notes ("walk labels are biased upward in the middle range") is true, and checking it takes no training at all. That makes it **Figure 1, not the paper**. The paper is H2–H4. **H2:** at fixed budget, changing the distribution moves optimality and nodes expanded more than a 10× increase in budget does. **H3:** with walk labels, more data stalls or hurts in specific distance bins, while with BFS labels it keeps improving. **H4:** a mismatch between the training and test distance distributions explains most of the search failures.

**Minimal experiment.** Hold the budget fixed at B ∈ {10⁵, 10⁶} samples, below the 3.67M states so the model cannot just memorise the table. Cross 4 distributions (uniform in k, uniform in true d, uniform random states, near-goal-heavy) with 3 label sources (simple walk, non-backtracking walk, BFS-exact). Use 3 seeds and a small MLP on one-hot stickers. Run A* and beam search on a test set stratified by true distance. Report MAE per distance bin, the admissibility-violation rate, solve rate, optimality gap and nodes expanded.

```python
# cube2.py — tested: 3,674,160 states, God's number 14 QTM, ~36 s and ~670 MB RAM on CPU
import numpy as np
from collections import deque
stickers = [(p, n) for p in np.array(np.meshgrid([-1,1],[-1,1],[-1,1])).T.reshape(-1,3)
            for n in np.eye(3, dtype=int) * p[:, None] if n.any()]
stickers = [(tuple(p), tuple(n)) for p, n in stickers]; idx = {s: i for i, s in enumerate(stickers)}
def move_perm(axis):                      # quarter turn of the +1 layer; corner (-1,-1,-1) stays fixed
    R = np.eye(3, dtype=int); a, b = [i for i in range(3) if i != axis]
    R[[a, a, b, b], [a, b, a, b]] = [0, -1, 1, 0]; perm = np.arange(24)
    for i, (p, n) in enumerate(stickers):
        if p[axis] == 1: perm[idx[(tuple(R @ p), tuple(R @ n))]] = i
    return perm
MOVES = [m for p in map(move_perm, range(3)) for m in (p, p[p[p]])]   # R R' U U' F F'
INV = [1, 0, 3, 2, 5, 4]
SOLVED = np.array([2 * [x != 0 for x in n].index(True) + (sum(n) > 0) for _, n in stickers], np.int8)
def bfs():
    dist = {SOLVED.tobytes(): 0}; q = deque([SOLVED])
    while q:
        s = q.popleft(); d = dist[s.tobytes()]
        for m in MOVES:
            t = s[m]
            if t.tobytes() not in dist: dist[t.tobytes()] = d + 1; q.append(t)
    return dist
def walk_table(dist, K=20, n=20000, nonback=True, seed=0):   # out[k, d] = walks of length k ending at true d
    rng = np.random.default_rng(seed); out = np.zeros((K + 1, 15), int)
    for _ in range(n):
        s, last = SOLVED, None
        for k in range(1, K + 1):
            last = rng.choice([m for m in range(6) if not (nonback and last is not None and m == INV[last])])
            s = s[MOVES[last]]; out[k, dist[s.tobytes()]] += 1
    return out
```

From there, the training loop is ordinary PyTorch. Bucket the BFS keys by distance to sample "uniform in true d", feed the 24 stickers as a 144-dim one-hot vector, regress the label, then plug the network into A*. Starting points for search code are [CayleyPy](https://github.com/cayleypy/cayleypy) (MIT, `pip install cayleypy`), [cayleypy-cube](https://github.com/k1242/cayleypy-cube) and [DeepXube](https://github.com/forestagostinelli/deepxube).

**8 GB note.** No problem at all. BFS runs on the CPU (measured above), and a sub-4M-parameter MLP trains in minutes per run. CayleyPy's single-epoch runs take 1–5 minutes on a P100 ([arXiv 2502.18663](https://arxiv.org/html/2502.18663v2)). By my estimate, the full factorial of about 100–200 runs takes days, not weeks. The only real risk is novelty: no paper I found runs this factorial, but that is "not found", not proven.

## 3. VLM OCR hallucination: the behaviour is known, the detector is open

**Taken vs open**

| Already done | Still open |
|---|---|
| VLM OCR "repairs" toward real words. On random strings, DeepSeek-OCR precision is 19.84% / 42.12% / 61.70% (Tiny/Small/Base). VLMs drop 51–68 points while PaddleOCR drops only ~4.9 ([arXiv 2601.03714](https://arxiv.org/pdf/2601.03714)) | A full **legibility × word-type × script** grid on small open VLMs |
| TextHalu-Bench: 1,740 items; GPT-4o F1 45.3 vs humans 96.8 ([arXiv 2506.05551](https://arxiv.org/html/2506.05551v2)). KIE-HVQA refusal benchmark (NeurIPS 2025) ([arXiv 2506.20168](https://arxiv.org/abs/2506.20168)) | **Ground-truth-free, token-level error detection** scored by AUROC and risk–coverage, compared *across cells*. I found no paper doing this |
| Per-token "image gain" on Ancient Greek, which turns out to be model-specific: olmOCR lexical errors 0.17 vs perceptual 1.40, Qwen3-VL-8B 1.97 vs 1.30 ([arXiv 2605.27750](https://arxiv.org/html/2605.27750v1)) | Whether confidence is overconfident on repaired misspellings while image gain is not, and where that flips |
| Mitigation: PAR ([ACL 2026](https://aclanthology.org/2026.acl-long.1065/)), grounded-layer fusion ([2506.05551](https://arxiv.org/html/2506.05551v2)), late-layer text override CALRD ([2606.17953](https://arxiv.org/html/2606.17953)), cross-view abstention GRC ([2603.19790](https://arxiv.org/abs/2603.19790)) | A non-Latin script: Devanagari errors cluster on conjuncts, matras and nukta ([arXiv 2606.29213](https://arxiv.org/html/2606.29213)), and unfamiliar scripts get swapped for look-alike scripts ([GlotOCR](https://arxiv.org/html/2604.12978v1)) |

**Sharp framing.** *When does the prior win? We map where the language prior overrides visual evidence in small VLMs across a legibility × lexical-familiarity × script grid, and test which ground-truth-free signals (confidence, image gain, logit-lens crossover) flag prior-driven misreads.* Lead with the detector comparison. Your "handoff layer" becomes one of the signals, not the headline, because CALRD and grounded-layer fusion already claim the mechanism.

**Minimal experiment.** Use 4 word types (frequent word, one-swap misspelling, random string, digit string) × 6 blur levels × about 200 items, with Latin first and Devanagari second (render it with a Noto font and correct shaping, or with the GlotOCR renderer). For each output, record exact match, the **repair rate** (wrong *and* a dictionary word), the blur level at which 50% of items are still correct for each word type, and the AUROC of minimum token log-prob vs minimum image gain for predicting an error. Add PaddleOCR or Tesseract as the "no-prior" control. The script below covers the whole loop. I tested the rendering and stimulus parts, but the model part is **untested** here because I had no GPU.

```python
# pip install "transformers>=4.57" accelerate pillow wordfreq pandas scikit-learn
import random, string, torch
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from wordfreq import top_n_list
LEX = top_n_list("en", 50000); LEXSET = set(LEX); rng = random.Random(0)
def make_items(n):
    words = [w for w in LEX[500:5000] if w.isalpha() and 5 <= len(w) <= 9]; items = []
    for w in rng.sample(words, n):
        items.append(("word", w))
        for _ in range(20):                                  # one interior letter swap that is NOT a word
            i = rng.randrange(1, len(w) - 2); m = w[:i] + w[i+1] + w[i] + w[i+2:]
            if m != w and m not in LEXSET: items.append(("misspelling", m)); break
        items.append(("random", "".join(rng.choices(string.ascii_lowercase, k=len(w)))))
        items.append(("digits", "".join(rng.choices(string.digits, k=len(w)))))
    return items
def render(text, blur, size=40):                             # use a Noto TTF for Devanagari
    font = ImageFont.load_default(size=size); w = int(font.getlength(text)) + 40
    img = Image.new("RGB", (max(w, 160), size + 40), "white")
    ImageDraw.Draw(img).text((20, 20), text, fill="black", font=font)
    return img.filter(ImageFilter.GaussianBlur(blur)) if blur else img
PROMPT = "Transcribe the text in the image exactly, letter by letter. Output only the text."
def load(mid="Qwen/Qwen3-VL-2B-Instruct"):
    from transformers import AutoProcessor, AutoModelForImageTextToText
    return (AutoProcessor.from_pretrained(mid),
            AutoModelForImageTextToText.from_pretrained(mid, torch_dtype=torch.bfloat16, device_map="cuda").eval())
def _inp(proc, img):
    msgs = [{"role": "user", "content": [{"type": "image", "image": img}, {"type": "text", "text": PROMPT}]}]
    return proc.apply_chat_template(msgs, tokenize=True, add_generation_prompt=True, return_dict=True, return_tensors="pt")
@torch.no_grad()
def read(proc, model, img):
    x = _inp(proc, img).to(model.device); out = model.generate(**x, max_new_tokens=24, do_sample=False)
    return proc.batch_decode(out[:, x["input_ids"].shape[1]:], skip_special_tokens=True)[0].strip()
@torch.no_grad()
def token_logprobs(proc, model, img, target):                 # teacher-forced log p(target | image, prompt)
    x = _inp(proc, img); t = proc.tokenizer(target, add_special_tokens=False, return_tensors="pt")["input_ids"]
    x["input_ids"] = torch.cat([x["input_ids"], t], 1)
    x["attention_mask"] = torch.cat([x["attention_mask"], torch.ones_like(t)], 1); x = x.to(model.device)
    lp = model(**x).logits[0, -t.shape[1] - 1:-1].float().log_softmax(-1)
    return lp.gather(-1, t[0].to(model.device)[:, None])[:, 0].cpu()
def image_gain(proc, model, img, text):                       # real image vs blank image of the same size
    return token_logprobs(proc, model, img, text) - token_logprobs(proc, model, Image.new("RGB", img.size, "white"), text)
if __name__ == "__main__":
    import pandas as pd; from sklearn.metrics import roc_auc_score
    proc, model = load(); rows = []
    for cls, text in make_items(50):
        for blur in range(6):
            img = render(text, blur); out = read(proc, model, img) or " "
            rows.append(dict(cls=cls, blur=blur, text=text, out=out, correct=out == text,
                             repaired=out != text and out.lower() in LEXSET,
                             min_logp=token_logprobs(proc, model, img, out).min().item(),
                             min_gain=image_gain(proc, model, img, out).min().item()))
    df = pd.DataFrame(rows); df.to_csv("cube_results.csv", index=False)
    print(df.groupby(["cls", "blur"])[["correct", "repaired"]].mean().unstack())
    for cls, g in df.groupby("cls"):
        if g.correct.nunique() == 2:
            print(cls, {s: round(roc_auc_score(~g.correct, -g[s]), 3) for s in ["min_logp", "min_gain"]})
```

**8 GB note.** These are my estimates, not measurements. A 2B model in bf16 needs roughly 4–5 GB for its weights, and single-word images keep the visual-token count small, so Qwen3-VL-2B (used in the Greek study) fits, as does SmolVLM. A 3–4B model in bf16 is borderline. 4-bit quantisation fits, but it makes logit-lens and patching hooks awkward. Stay at 2B for the internal-signal work. The Greek study used about 100 GPU-hours, but on full pages ([arXiv 2605.27750](https://arxiv.org/html/2605.27750v1)). The single-word grid above is far cheaper. For hooks, Spectra supports Qwen2.5-VL, Qwen3-VL, SmolVLM and LLaVA-1.5 ([ACL 2026 demo](https://preview.aclanthology.org/ingest-acl/2026.acl-demo.78/)).

## 4. "Even I can do a benchmark paper": half right, and here is the other half

**The papers you're probably thinking of**

| Paper | What it actually contributed | Where it appeared | Team / data |
|---|---|---|---|
| **From Pixels to Structure** ([arXiv 2610.11818](https://arxiv.org/abs/2610.11818)) | Not a big benchmark. A careful comparison of 8 open VLMs (≤7B) on 3 university heritage collections: zero-shot, few-shot and fine-tuned, with ablations on preprocessing and multi-stage training. Metrics: CER, ANLS* and mAP-F1 | **ICDAR 2026**, Springer LNCS (17 pp.) | 4 authors, including senior document-analysis researchers (Christlein, Maier). Annotated real institutional data |
| KRETA ([EMNLP 2025](https://aclanthology.org/2025.emnlp-main.1696.pdf)) | 2,577 Korean text-rich VQA items from native images (including the authors' own photos), a reusable generation-plus-review pipeline, about 19 models evaluated | **EMNLP 2025 main** | 5 authors across startups, a university and big tech |
| KOCRBench ([arXiv 2510.02543](https://arxiv.org/html/2510.02543v1)) | Only 250 questions. The real contribution is a 55M-parameter OCR model trained for about 500 GPU-hours | **arXiv only** | 2 authors at a company |
| KOFFVQA ([CVF](https://openaccess.thecvf.com/content/CVPR2025W/BEAM/papers/Kim_KOFFVQA_An_Objectively_Evaluated_Free-form_VQA_Benchmark_for_Large_Vision-Language_CVPRW_2025_paper.pdf)) | Free-form Korean VQA benchmark | **CVPR 2025 workshop**, not the main conference | — |
| OCRTurk ([arXiv 2602.03693](https://arxiv.org/html/2602.03693v1)) | 180 Turkish PDF pages, 2 annotators, 7 OCR systems, a Turkish-character metric | **arXiv only** (when checked) | 7 authors, academic + industry |
| KITAB-Bench ([arXiv](https://arxiv.org/abs/2502.14949v1)) | 8,809 Arabic OCR/document samples across 9 domains | **ACL 2025 Findings** ([Anthology](https://preview.aclanthology.org/watermark/2025.findings-acl.1135)) | MBZUAI, 10 authors |
| IndicDLP ([CVIT](https://cvit.iiit.ac.in/research/projects/cvit-projects/indicdlp)) | Indic layout dataset, 11 languages + English | **ICDAR 2025 oral**, Best Student Paper runner-up | **63 annotators** + reviewers |
| HinTel-AlignBench ([ACL Anthology](https://aclanthology.org/2026.alvr-main.26/)) | Hindi/Telugu VLM benchmark, 4,000 QA per language, 6 pages | **ALVR workshop @ ACL 2026** | — |

The pattern is clear. **Simple method, but not simple data.** Every paper that reached a good venue had real, native-sourced, human-verified data, a broad evaluation, and usually senior or industry co-authors. The "basic Korean" papers that look easy mostly sit on arXiv or at workshops. Being on arXiv is not the same as being "in a huge conference". I did not check Korean OCR papers in MDPI-style journals, so I can't comment on those.

**What reviewers expect in 2026.** The NeurIPS 2026 Evaluations & Datasets track (the renamed D&B track) holds submissions to main-track standards. It requires the data to be public **at submission time** on a persistent host such as Hugging Face or Kaggle, a mandatory **Croissant metadata file with Responsible-AI fields**, code for executable benchmarks, and an explicit statement of the claims and limitations of the evaluation. Inaccessible data "justifies the desk rejection of the paper" ([CFP](https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets)). In 2025, submissions commonly lacked licence information (11.9%), dataset descriptions and URLs ([NeurIPS blog](https://blog.neurips.cc/2025/12/05/neurips-datasets-benchmarks-track-from-art-to-science-in-ai-evaluations/)). From these rules and the papers above, I infer that the usual ways to get rejected are: a set too small with no insight beyond "models do worse on language X", LLM-made labels nobody verified, unclear redistribution rights, contamination (Wikisource pages are probably already in VLM training data), and no inter-annotator agreement.

**Is there an Indian-language gap?** Yes, but a narrow one. Scene text, layout and general VQA are covered (BSTD, IndicDLP, IndicVisionBench, HinTel-AlignBench). Krutrim's 2026 paper names what is still missing: dense printed documents, **forms and index pages**, rare scripts, handwriting and low-resolution scans. It also says there is **no public benchmark** for extracting key fields from government documents ([arXiv 2602.16430](https://arxiv.org/html/2602.16430v1)). IndicVisionBench's OCR track has only 876 Wikisource pages ([arXiv 2511.04727](https://arxiv.org/html/2511.04727)). Well-funded players (AI4Bharat, Krutrim, Sarvam) are active, so search again for 2026 releases before you commit.

**A realistic undergraduate version.** Pick 1–2 languages you read natively and one under-served document type, such as forms, old print or handwritten registers. Collect **200–500 pages** you have the rights to (your own photos, government or public-domain material). Annotate page-to-text, or key fields. Double-annotate about 20% to report agreement. Evaluate **8–15 systems**, mixing classic OCR (Tesseract, PaddleOCR) with small and large VLMs. Report the median plus a catastrophic-failure rate, because VLMs fall into repetition loops ([arXiv 2606.29213](https://arxiv.org/html/2606.29213)). Analyse errors by script phenomenon, such as conjuncts and matras. Release the data on Hugging Face with Croissant metadata and a licence. Expect several months of part-time work, mostly on annotation. Go up the venue ladder in order: **an ACL/CVPR/ICDAR workshop first (ALVR-style), then ICDAR main, ACL Findings or IJDAR, and NeurIPS E&D only with scale and a senior co-author.**

| Option | Effort | Realistic venue |
|---|---|---|
| 200–500 page Indic document set + 8–15 systems + error analysis | 3–6 months, part-time | Workshop → ICDAR / IJDAR |
| Same + Devanagari hallucination grid from §3 as the analysis section | +1–2 months | ICDAR / Findings, a stronger story |
| Thousands of items, many languages, annotator team | Lab-scale | NeurIPS E&D / main conference |

## Conclusion

The three ideas fit together better than they look. The SSL project asks *what a recognizer should ignore*. The hallucination project asks *what a VLM wrongly ignores* (the pixels, when its prior is strong). An Indic benchmark is most publishable when it carries exactly that kind of analysis rather than a leaderboard. So if you want a paper of your own beyond the thesis track, the strongest single move is to merge §3 and §4: a small, human-verified Devanagari document set whose headline result is *where and how detectably the prior overrides the pixels*. The cube study is the cleanest, most self-contained thing you can finish quickly, and its first figure already exists. Do it as a warm-up for writing a paper, not as the main bet.
