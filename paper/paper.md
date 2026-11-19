---
title: "Measured, Not Hand-Picked: Choosing the Damage a Handwriting Recogniser Should Learn to Ignore"
author:
  - Arvind Kothamangala
  - Atharv Sawarkar
  - Vignesh Nunna
  - Rohit Rajan
affiliation: "Team 147, Dept. of Computer Science and Engineering, PES University, Bengaluru"
guide: "Guide: Dr. Chandrashekhar P Chavan"
keywords: [handwritten text recognition, document degradation, data augmentation, self-supervised learning, invariance]
abstract: |
  Recognisers for handwritten text are usually trained to ignore damage chosen by hand: a list of blurs, noises and
  contrast changes whose strengths are guessed and re-tuned for each collection. We replace the guess with a
  measurement. Eight per-line statistics are measured on real medieval manuscript lines (CATMuS) and on clean
  modern handwriting (IAM); six simple forward models of damage are fitted to the difference by inverting a response
  curve per model, which yields how often each damage occurs and how strong it is. We use the resulting recipe in two
  ways with a 7.4M-parameter CRNN. As the corruption of a convolutional masked autoencoder, it does not help at our
  scale: no pretrained variant beats training from scratch by more than the seed spread. As plain training
  augmentation, it lowers the character error rate on real medieval test lines with 5% of the labels from 33.8% to
  31.6% (three seeds), where a hand-picked recipe gives 33.6% and background normalisation 33.0%. The gain is about
  equally large on the most damaged quarter of the test lines as on all lines, and on held-out synthetic ink loss the
  hand-picked recipe is the more robust one. Finally, a model's measured feature invariance to a damage type predicts
  how much that damage raises its error (Spearman $\rho \approx -0.9$), and the relation survives a control for
  pixel-level change (partial $\rho = -0.80$) in models not trained on the damage, but weakens to between $-0.12$ and
  $-0.39$ in augmented models. All decision rules were fixed before the runs; we report the failed ones as well.
---

# Introduction

Handwritten text recognition (HTR) reaches character error rates (CER) of a few per cent on clean benchmarks such as
IAM [@iam], but archives hold millions of pages whose ink has faded, whose parchment has darkened, whose verso text
shows through, or which carry stains. Accuracy drops on such pages, and these are also the collections for which
almost no transcribed lines exist. An off-the-shelf industrial recogniser that reaches 11.4% CER on IAM gets more than half of
the characters wrong (52.5%) on the medieval lines we use (Table \ref{tab:baselines}).

Whatever learning method is used to cope with the shortage of labels, the designer decides which variations the model
should become insensitive to. Self-supervised learning (SSL) does so through its pretext task: a denoising or masked
autoencoder learns to ignore the corruptions it is asked to undo, and a contrastive method learns to ignore the
augmentations that separate two views [@ericsson]. Supervised augmentation does the same in a more direct way. In
natural images, robustness to a corruption at test time depends on how similar the training augmentations are to it
[@mintun]. For text recognition, the choice is still made by hand. A critical survey of SSL for text recognition notes
that augmentations are tuned per dataset without a stated procedure [@survey]; Text-DIAE chooses its degradations and
their strengths by hand [@textdiae]; and the most recent large comparison of SSL objectives for handwriting, which
finds that pixel reconstruction clearly beats contrastive and joint-embedding objectives, uses "a fixed augmentation
pipeline" described only as "small", "mild" or "low" [@garrido].

This paper asks whether the damage a recogniser is trained to ignore can be *measured* on the target documents instead
of guessed, and what a recogniser gains from it. Fitting degradation models to real scans is not new: Kanungo, Baird
and colleagues estimated and validated the parameters of document degradation models against real page images in the
1990s [@kanungo94; @kanungo], and Baird's 2007 review lists the sound use of such synthetic data as an open problem
[@baird07]. That line of work targeted binary images and classical OCR. We revisit the idea for a deep line
recogniser, compare the fitted recipe with a hand-picked one on real damaged lines, and test whether the invariance
the recogniser acquires can be measured and predicts its errors.

Our contributions are:

- A simple, reproducible procedure that derives a damage recipe (which damage, how often, how strong) from eight
  per-line statistics of real lines by inverting the response curve of each of six forward models, with a seventh
  type, ink loss, held out for testing.
- A small, controlled comparison with pre-registered pass/fail rules on IAM and a Latin and French subset of CATMuS
  Medieval [@catmus]: the derived recipe gives no gain as the corruption of masked-autoencoder pretraining at our
  scale, but lowers CER on real medieval lines by 2.2 points when used as plain augmentation, where the hand-picked
  recipe (0.2 points) and background normalisation (0.8 points) do not come close.
- An analysis of what the gains do *not* show: the synthetic-damage gains are partly circular, the hand-picked recipe
  is more robust to held-out ink loss, and the CATMuS gain is not concentrated on the most damaged lines.
- Evidence that a model's measured feature invariance to a damage type predicts its CER rise (Spearman
  $\rho \approx -0.9$ across 21 damage settings), that this survives a pixel-space control in models not trained on
  the damage, and that it weakens sharply once the damage is part of training.

# Related work

**SSL for text recognition.** SeqCLR contrasts horizontal windows of two augmented views [@seqclr]; LoGo-HTR combines
local and global contrastive objectives and pretrains on millions of word images [@logo]. Kišš and Hradiš pretrain
recognisers on large unlabelled historical collections with masked feature prediction and find that target-domain
pretraining does not consistently beat supervised transfer from a related labelled dataset [@kiss]. Lacuna
reconstruction lowers CER from 60.4% to 23.7% with 30 labelled lines by pretraining on masked regions [@lacuna].
Garrido-Munoz and Calvo-Zaragoza compare six SSL objectives with one ViT-B-scale encoder on six handwriting benchmarks
[@garrido]. With a frozen encoder and full labels, MAE [@mae] reaches a mean CER of 5.5%, against 8.7% to 19.2% for
SimMIM, V-JEPA-2, SigLIP, I-JEPA and MoCo-v3, and MAE with 10% of the labels (8.8%) beats every joint-embedding and
contrastive method with all labels. They explain the gap by showing that the information that separates characters
lies in high-variance pixel directions, which reconstruction preserves. Text-MAE adapts a fully convolutional masked
autoencoder to handwritten lines [@textmae]; our ConvMAE follows the same idea on the recogniser's own CNN. None of
these works chooses its augmentations or corruptions from measurements of the data.

**Degradation-aware training and degradation models.** Text-DIAE pretrains a degradation-invariant autoencoder with
masking, blur and background-noise pretext tasks [@textdiae]; its degradations are hand-picked, and in its ablations
added noise did not help. Augraphy is a library of hand-designed document degradations [@augraphy], and PreP-OCR
restores degraded images with a model trained on hand-set synthetic damage before OCR [@prepocr]. Our show-through
model follows the recto-verso mixing model of Salerno and Tonazzini [@salerno]. The idea of *fitting* degradation
models to real documents goes back to Kanungo, Haralick, Baird and colleagues, who estimated the parameters of a
local degradation model from real scans [@kanungo94], turned the question "does this model match real scans?" into a
nonparametric permutation test [@kanungo], and used fitted models to produce synthetic training sets; Baird reviews
this line of work [@baird07]. Our fitting step is far cruder than theirs; what we add is the question of what a deep
recogniser learns from the fitted damage.

**Fitting corruption to data at the text level.** The ICDAR 2026 HIPE-OCRepair competition generates synthetic OCR
errors from character confusion matrices estimated on its data [@hipe], and a retrieval-augmented restoration method
for historical documents samples its corruption rate to match the real damage distribution [@hanja]. Both fit the
corruption of *text*, not of images, and neither trains a recogniser.

**Measuring invariance.** Ericsson et al. measure how invariant a pretrained representation is to each augmentation,
as the similarity of the features of an image and its transformed copy, and show that downstream tasks need
different invariances [@ericsson]. Mintun et al. show that robustness to a corruption depends on its perceptual
similarity to the training augmentations [@mintun]. We apply the first measurement to document damage and test the
link to error that the second suggests.

# Method

## Measuring damage on real lines

All lines are grey-scale, 64 px high, with dark ink on light paper. For each line we compute eight statistics on the
same normalised image that the models see, separating ink from paper with Otsu's threshold on a lightly smoothed copy
so that pixel noise is not counted as ink. Six statistics describe damage: *paper level* (median paper intensity /
255), *faint grey on paper* (share of paper pixels that are faintly grey, which reflects show-through), *background
unevenness* (standard deviation of the large-scale paper level), *ink–paper contrast* ((paper − ink level) / 255),
*sharpness* (Laplacian variance / contrast²) and *pixel noise* (robust standard deviation of the high-pass residual on
paper). Two describe scale and script rather than damage: *stroke width* (2 × ink area / ink perimeter) and *ink
fraction*. Only the damage statistics are used for fitting.

## Damage families

Each damage family $f$ is a forward model $D_f(x; p, \omega)$ with one physical parameter $p$ and random state
$\omega$, applied to a line $x$ with paper level $b$ (90th intensity percentile):

- *paper tone*: $x' = p\,x$ (darkened paper or parchment);
- *fading*: $x' = b - p\,(b - x)$, where $p$ is the ink–paper contrast kept;
- *blur*: Gaussian blur with $\sigma = p$ px;
- *noise*: additive Gaussian noise with standard deviation $255\,p$;
- *show-through*: a mirrored, randomly shifted and blurred copy $v$ of the line acts as the verso, and
  $x' = \min(x,\ b - p\max(0, b - v))$, where $p$ is the verso opacity [@salerno];
- *stain*: $x' = x\,(1 - p\,\phi^2)$ with $\phi \in [0,1]$ a smooth random field;
- *ink loss*: inside random blobs covering a fraction $p$ of the line, pixels are set to $\max(x, b)$.

Blur, fading and ink loss overlap the character-carrying pixels; tone, noise, show-through and stains mostly change
the paper. Ink loss is held out of every recipe and used only as unseen test damage. For robustness tests each family
has three fixed severity levels (Table \ref{tab:recipe}), chosen to span "barely visible" to "hard to read" before any
error rate was computed.

## Deriving a recipe by response-curve inversion

Let $S$ be clean source lines (IAM train) and $T$ target lines (3,000 CATMuS train lines), and let $s_f$ be the
statistic that family $f$ mainly moves, with $d_f = \pm 1$ its damage direction. On 300 source lines we apply $D_f$ at
a grid of values of $p$ and record the response curve

$$ m_f(p) = \operatorname{median}_{x \in S}\, s_f\big(D_f(x; p)\big), $$

which is monotone. A target line $y$ counts as damaged by $f$ if $s_f(y)$ lies beyond the clean source range in the
damage direction, $d_f\, s_f(y) > d_f\, q_f$, where $q_f$ is the 5th or 95th percentile of $s_f$ on $S$. The recipe
for $f$ is then a frequency and a strength distribution:

$$ \pi_f = \frac{|T_f|}{|T|}, \qquad p_y = m_f^{-1}\big(s_f(y)\big) \ \text{ for } y \in T_f, $$

with $m_f^{-1}$ obtained by linear interpolation and clipped to the grid. During training, each family is applied
independently with probability $\pi_f$, in the physical order tone, stain, show-through, fading, blur, noise, with a
strength drawn by inverse-CDF sampling from 21 stored quantiles of $\{p_y\}$. The derived recipe (Table
\ref{tab:recipe}) is dominated by paper-side damage: tone on 84% and show-through on 89% of the lines, blur on only 5%.
This first version has a known weakness: a difference in a statistic between two datasets also reflects script, pen
and scan resolution, not only damage.

**Hand-picked recipe.** As the usual practice, every family is applied with probability 0.5 and a strength drawn
uniformly over its three severity levels. Fig. \ref{fig:recipes} shows both recipes on one IAM line.

Table: Damage families, the statistic each one moves, the fixed severity levels (low / medium / high) used for
testing, and the two training recipes. Ink loss is held out of both recipes. {#tab:recipe}

| Family | Parameter $p$ | Statistic | Overlaps ink | Severity levels | Derived: share of lines | Derived: median $p$ | Hand-picked |
|:--|:--|:--|:--|:--|--:|--:|:--|
| Paper tone | brightness kept | paper level | no | 0.9 / 0.8 / 0.65 | 84% | 0.80 | 50%, $p \sim U$[levels] |
| Show-through | verso opacity | faint grey | no | 0.15 / 0.30 / 0.50 | 89% | 0.40 | 50%, $p \sim U$[levels] |
| Stain | darkening depth | unevenness | no | 0.15 / 0.30 / 0.50 | 37% | 0.08 | 50%, $p \sim U$[levels] |
| Fading | contrast kept | contrast | yes | 0.6 / 0.35 / 0.2 | 26% | 0.52 | 50%, $p \sim U$[levels] |
| Noise | $\sigma$ / 255 | pixel noise | no | 0.04 / 0.10 / 0.18 | 11% | 0.014 | 50%, $p \sim U$[levels] |
| Blur | $\sigma$ (px) | sharpness | yes | 0.8 / 1.5 / 2.5 | 5% | 1.1 | 50%, $p \sim U$[levels] |
| Ink loss | area removed | ink fraction | yes | 0.15 / 0.35 / 0.55 | held out | -- | held out |

![What the models are trained to ignore: three real CATMuS lines (top), and one clean IAM line under four draws of the
hand-picked recipe and four of the derived recipe.](results/figures/fig_corruptions_handpicked_vs_derived.png){#fig:recipes width=0.92\linewidth}

## Recogniser and pretraining

**CRNN.** The recogniser is a CRNN [@crnn]: seven $3\times3$ convolution blocks with batch normalisation and ReLU
(64 to 384 channels) reduce the 64-px line to a sequence of 384-dimensional feature columns, one per 4 px of width;
a two-layer bidirectional LSTM (256 units per direction, dropout 0.25) and a linear layer produce per-column character
probabilities trained with CTC [@ctc] and decoded greedily. It has 7.4M parameters.

**ConvMAE pretraining.** Our pretraining applies a masked, denoising autoencoder to the CRNN's own CNN, since a first
6.5M-parameter ViT encoder memorised the few labelled lines (test CER 60–75%, against 20–43% for the CRNN; a frozen
encoder probe reached 75%). The input is a 512-px crop, optionally corrupted by a recipe, in which random 8-px vertical
strips are blanked with ratio 0.6. A light decoder (two 1-D convolutions with kernel 5 and a $1\times1$ projection)
predicts the *clean* pixels $c_t$ of every $64\times4$ column from the encoder features:

$$ \mathcal{L} = \frac{1}{|M|}\sum_{t \in M} \lVert \hat c_t - c_t \rVert^2
   + \lambda \frac{1}{|V|}\sum_{t \in V} \lVert \hat c_t - c_t \rVert^2, $$

where $M$ and $V$ are the masked and visible columns and $\lambda = 0.25$. Three variants differ only in the input
corruption: none (masking only), hand-picked, and derived. Each is pretrained for 12,000 steps (batch 64, AdamW, learning
rate $3\cdot10^{-4}$, weight decay 0.05, about 34 minutes) on 30,244 unlabelled lines from the CATMuS and IAM
training splits; no validation or test line is used. The pretrained CNN then initialises the CRNN, which is fine-tuned
with exactly the baseline settings.

## Damage as augmentation and a preprocessing control

In the augmentation arms the scratch CRNN is trained with every training line corrupted by the hand-picked or derived
recipe, redrawn each epoch; validation and test lines are not touched. As a cheap control for the paper-side damage,
the *background normalisation* arm divides every train, validation and test line by a background estimate (grey-scale
closing with a $21\times21$ square followed by a median blur) and stretches the result to the full grey range.

## Invariance score and pixel control

For a trained model $g$ with pooled CNN features (mean over valid columns, standardised with the mean and standard
deviation of the clean set), the invariance to damage family $f$ at level $\ell$ is

$$ I_{f,\ell} = \frac{1}{N}\sum_{i=1}^{N} \cos\!\big(g(x_i),\ g(D_f(x_i; p_\ell))\big), $$

on $N = 500$ IAM test lines, following Ericsson et al. [@ericsson]; $I = 1$ means the damage is ignored. We correlate
$I_{f,\ell}$ with the CER ratio $r_{f,\ell} = \mathrm{CER}_{f,\ell} / \mathrm{CER}_{\text{clean}}$ over the 21
settings (7 families × 3 levels) with Spearman's $\rho$. Both quantities could simply follow how much the damage changes
the pixels, so the *pixel control* computes the same cosine similarity directly on the input pixels (ink = 1) and
reports the partial Spearman correlation of $I$ and $r$ after rank-regressing both on the pixel similarity ($p$ from a
$t$-test with $n-3$ degrees of freedom).

# Experimental setup

**Data.** IAM-line [@iam] has 6,482 training, 976 validation and 2,915 test lines from 657 writers, with the official
writer-independent split. From CATMuS Medieval [@catmus] we use the Latin and French lines, the two languages that are
large in both the training and the test split: 25,005 training lines from 11 projects (5% kept for validation, which
leaves 23,762) and 4,022 test lines (3,003 Latin, 1,019 French) from manuscripts not seen in training (Fig.
\ref{fig:samples}). Lines are resized to 64 px height and transcriptions normalised to Unicode NFC; character sets are
built from training lines only (79 for IAM, 195 for CATMuS, which keeps medieval abbreviation marks). We found that 99%
of CATMuS line images have the area outside the line polygon painted pure black, about 15% of the image on average.
This frame is read as ink by every measurement, so we fill border-connected black pixels with the local paper tone,
store a mask of real pixels, and measure only real pixels at least 3 px from the former polygon edge.

![Sample lines from IAM (top two) and the CATMuS Latin and French subset (bottom three), after removal of the
polygon fill.](results/figures/samples_iam_catmus.png){#fig:samples width=\linewidth}

**Training.** All recognisers use AdamW (learning rate $3\cdot10^{-4}$, weight decay 0.01), batch 16, linear warm-up
over the first 10% of steps (at most 1,000) and cosine decay, gradient clipping at 5 and bf16 mixed precision. The
step budget is 3,000 for IAM 1% labels (65 lines), 8,000 for IAM 10% (648) and CATMuS 5% (1,188), 20,000 for IAM 100%
and 30,000 for CATMuS 100%. Validation CER is computed every 500 steps, training stops after 8 evaluations without
improvement, and the best validation checkpoint is scored on the test split. All training ran on one 8 GB laptop
GPU; a full-label IAM model takes 50 minutes. The augmentation comparison uses three seeds per arm; the pretraining
comparison two.

**Metrics and subsets.** CER is the edit distance between output and reference divided by the reference length.
Synthetic robustness is measured on the IAM test set with each family at each severity level, with damage seeded per
line so that every model sees the same images. For real damage, CATMuS test lines are split into quartiles of a
measured statistic *within each manuscript project*, so that project difficulty does not masquerade as damage;
pre-binarised lines are excluded. The *hard subsets* are the most damaged quartiles by paper level (darkest),
faint grey (most show-through) and contrast (lowest), 1,007 lines each.

**Pre-registered rules.** Before the pilot we fixed four assumptions: A1, damage hurts (CER at least doubles for at
least two families at medium severity); A2, real and clean lines differ (at least three damage statistics with
two-sample Kolmogorov–Smirnov $D \ge 0.5$); A3, pretraining helps (a pretrained variant beats scratch by more than the
seed spread in at least one setting); A4, derived $\le$ hand-picked (indicative). Before any augmentation run had
finished we added B1–B5 for the 10%-IAM / 5%-CATMuS setting. The *damage measure* is the mean CER over the six recipe
families at medium strength on IAM; the seed spread is half the max–min range over seeds. B1: derived augmentation
lowers the damage measure versus scratch by at least 2 points and by more than the seed spread. B2: derived beats
hand-picked on the damage measure. B3: derived beats background normalisation on it. B4: derived costs at most 1 point
of clean CER on both datasets. B5: derived beats scratch by more than the seed spread on at least two of the three
CATMuS hard subsets.

Table: Supervised CRNN baselines and an off-the-shelf reference (test CER; mean and range over seeds). {#tab:baselines}

| Data | Labels | Lines | Seeds | CER | Range |
|:--|:--|--:|--:|--:|:--|
| IAM | 1% | 65 | 2 | 43.3% | 43.1–43.6 |
| IAM | 10% | 648 | 3 | 19.9% | 19.4–20.7 |
| IAM | 100% | 6,482 | 1 | 9.8% | -- |
| CATMuS | 5% | 1,188 | 3 | 33.8% | 33.4–34.1 |
| CATMuS | 100% | 23,762 | 1 | 20.0% | -- |
| IAM | PaddleOCR [@paddle] | -- | -- | 11.4% | -- |
| CATMuS | PaddleOCR [@paddle] | -- | -- | 52.5% | -- |

# Results

Table \ref{tab:baselines} gives the supervised baselines. With all labels the CRNN reaches 9.8% CER on IAM and 20.0%
on CATMuS; the off-the-shelf PaddleOCR PP-OCRv6 recogniser, used without adaptation, reaches 11.4% on IAM but 52.5%
on the medieval lines. With few labels the error rises quickly (19.9% with 648 IAM lines, 43.3% with 65).

## Damage hurts (A1: pass)

At medium severity, four of the seven families at least double the CER of the full-label IAM model (Table
\ref{tab:a1}): ink loss multiplies it by 7.64, noise by 4.95, tone by 3.37 and blur by 3.07, while show-through, fading
and stains raise it by at most 1.4 times. On real CATMuS test lines, in each of nine trained models, the
lowest-contrast quartile has 1.33–1.47 times the CER of the highest-contrast quartile, whereas quartiles of paper level,
noise and background unevenness differ by factors of 0.93–1.08 and the faint-grey quartiles by 1.11–1.13. Sharpness
moves the other way (0.74–0.76); we suspect a confound with stroke width and line density and draw no conclusion
from it.

Table: CER of the full-label IAM CRNN under synthetic damage (clean: 9.8%). {#tab:a1}

| Family | Low | Medium | High | Medium / clean |
|:--|--:|--:|--:|--:|
| Tone | 10.8% | 33.1% | 99.4% | ×3.37 |
| Fading | 10.1% | 13.0% | 34.1% | ×1.32 |
| Blur | 12.7% | 30.2% | 70.6% | ×3.07 |
| Noise | 12.3% | 48.6% | 99.3% | ×4.95 |
| Show-through | 10.0% | 12.2% | 21.5% | ×1.24 |
| Stain | 10.1% | 13.6% | 31.4% | ×1.39 |
| Ink loss | 44.5% | 75.1% | 87.7% | ×7.64 |

## Real damage differs, but less than planned (A2: fail)

Table \ref{tab:a2} compares the statistics of 3,000 IAM and 3,000 CATMuS training lines. Two damage statistics
separate the datasets strongly: the medieval paper is much darker ($D = 0.82$) and far more of it is faintly grey
($D = 0.84$), consistent with parchment texture and show-through. Background unevenness differs moderately ($D =
0.42$); contrast, sharpness and noise hardly differ. Our rule required three damage statistics with $D \ge 0.5$, so A2
narrowly fails. The result still shapes the recipe: real medieval damage is concentrated on the paper side, not in the
blur and noise that hand-picked recipes emphasise. Stroke width and ink fraction also separate the datasets strongly,
but they reflect the denser script and tighter cropping of the manuscripts and are not used for fitting.

Table: Per-line statistics, IAM vs CATMuS training lines (medians and two-sample KS $D$). {#tab:a2}

| Statistic | Kind | IAM | CATMuS | KS $D$ |
|:--|:--|--:|--:|--:|
| Paper level | damage | 0.980 | 0.804 | **0.82** |
| Faint grey on paper | damage | 0.002 | 0.077 | **0.84** |
| Background unevenness | damage | 0.005 | 0.009 | 0.42 |
| Ink–paper contrast | damage | 0.478 | 0.408 | 0.26 |
| Sharpness | damage | 1.084 | 0.939 | 0.11 |
| Pixel noise | damage | 0.000 | 0.006 | 0.16 |
| Stroke width (px) | script | 3.33 | 4.81 | 0.73 |
| Ink fraction | script | 0.119 | 0.260 | 0.94 |

## Reconstruction pretraining does not help at this scale (A3: fail)

No ConvMAE variant beats the scratch CRNN by more than the seed spread (Table \ref{tab:pretrain}). With 5% of the
CATMuS labels, masking alone and derived corruption match scratch (33.3% and 33.4% against 33.8%), and on IAM all
pretrained variants are slightly worse than scratch. Derived corruption is at least as good as hand-picked corruption
in all three settings, so A4 passes, but derived is indistinguishable from plain masking. The honest reading is that
hand-picked corruption hurts pretraining a little and derived corruption does no harm, not that derived corruption
helps. This matches the caution of Kišš and Hradiš that target-domain pretraining does not always beat supervised
training [@kiss]; with 30,244 unlabelled lines and 34 minutes of pretraining, our scale is a likely cause.

The recipe does leave a trace in what the fine-tuned models resist (IAM, 10% labels, two seeds). Models pretrained with
hand-picked corruption, which blurs half of its inputs, have 64.1% and 63.6% CER under high blur, against 79.2% and
79.6% for scratch; models pretrained with derived corruption, which darkens the paper of 84% of its inputs, have
32.1% and 26.4% under medium tone, against 39.9% and 39.4%. No recipe helps on held-out ink loss.

Table: Test CER of the CRNN with and without ConvMAE pretraining of its CNN (mean ± half the seed range; $n$ seeds). {#tab:pretrain}

| Setting | Scratch | Masking | + hand-picked | + derived |
|:--|--:|--:|--:|--:|
| CATMuS 5% | 33.8±0.4 (3) | 33.3±0.3 (2) | 35.0±0.2 (2) | 33.4±0.7 (2) |
| IAM 1% | 43.3±0.2 (2) | 43.8±0.2 (2) | 44.7±0.5 (2) | 43.9±0.5 (2) |
| IAM 10% | 19.9±0.6 (3) | 20.4±0.3 (2) | 21.0±0.4 (2) | 20.5±0.1 (2) |

## Derived damage as augmentation

Used as plain augmentation of the scratch CRNN, the same recipe gives the clearest gain of the study (Table
\ref{tab:e1}, Fig. \ref{fig:hard}). With 5% of the CATMuS labels, derived augmentation lowers the CER on real medieval
test lines from 33.8% to 31.6%, with seed spreads of at most ±0.5 points; hand-picked augmentation gives 33.6% and
background normalisation 33.0%. The gain holds on each of the three hard subsets, by 2.6 points on the darkest-paper
quartile, 2.8 on the most-show-through quartile and 2.4 on the lowest-contrast quartile (B5: pass, 3 of 3). With 10%
of the IAM labels both recipes lower the clean CER by about one point (19.9% to 18.8–18.9%), so the recipe costs
nothing on clean lines (B4: pass).

Table: Damage as training augmentation of the scratch CRNN: clean test CER, and CATMuS 5% CER on the most damaged
quartile of real test lines by each statistic (mean ± half the seed range, three seeds). {#tab:e1}

| Training | IAM 10%, clean | CATMuS 5%, all lines | Q4 darkest paper | Q4 most show-through | Q4 lowest contrast |
|:--|--:|--:|--:|--:|--:|
| No augmentation | 19.9 ± 0.6 | 33.8 ± 0.4 | 35.6 ± 0.4 | 35.7 ± 0.4 | 39.4 ± 0.4 |
| Hand-picked damage | **18.8** ± 0.3 | 33.6 ± 0.4 | 34.7 ± 0.3 | 35.1 ± 0.3 | 38.1 ± 0.2 |
| Derived damage | 18.9 ± 0.2 | **31.6** ± 0.5 | **33.0** ± 0.7 | **32.9** ± 0.6 | **37.0** ± 0.3 |
| Background normalisation | 19.8 ± 0.6 | 33.0 ± 0.2 | 35.0 ± 0.0 | 34.7 ± 0.3 | 38.2 ± 0.3 |

![CATMuS 5% test CER of the three treatments on all lines and on the most damaged quartile by each measured statistic
(dot: mean of three seeds; bar: seed range). The no-augmentation reference is 33.8%, 35.6%, 35.7% and 39.4%.](results/figures/fig_e1_hard_subset.png){#fig:hard width=0.78\textwidth}

On IAM with synthetic damage (Table \ref{tab:synth}), derived augmentation lowers the medium-strength damage measure
from 37.9% to 19.4% (B1: pass) and background normalisation only to 32.3% (B3: pass). The hand-picked recipe,
however, is slightly better still (18.9%), and at high strength clearly so (20.1% against 24.1%). The automated summary
lists B2 as pending; on these numbers we do not claim it. The fair test is ink loss, held out of both recipes: the
ratio of damaged to clean CER at medium strength falls from 3.82 without augmentation to 3.59 with derived and 3.27
with hand-picked augmentation, and background normalisation does not help at all (3.83).

Table: IAM 10% CER under synthetic damage. "6 fam." is the mean over the six recipe families; ink loss is held out of
both recipes; "ratio" is damaged / clean CER (mean ± half the seed range, three seeds). {#tab:synth}

| Training | Med.: 6 fam. | ratio | Med.: ink loss | ratio | High: 6 fam. | ratio | High: ink loss | ratio |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| No augmentation | 37.9 ± 2.8 | 1.90 | 76.1 ± 1.6 | 3.82 | 65.3 ± 0.2 | 3.28 | 94.3 ± 5.5 | 4.73 |
| Hand-picked damage | **18.9** ± 0.3 | **1.00** | **61.5** ± 0.8 | **3.27** | **20.1** ± 0.3 | **1.07** | **77.5** ± 1.5 | **4.12** |
| Derived damage | 19.4 ± 0.1 | 1.03 | 67.6 ± 0.7 | 3.59 | 24.1 ± 0.2 | 1.28 | 83.0 ± 1.7 | 4.40 |
| Background normalisation | 32.3 ± 2.2 | 1.63 | 75.8 ± 3.5 | 3.83 | 45.6 ± 3.9 | 2.30 | 92.6 ± 7.4 | 4.68 |

## Invariance predicts the error rise

For the full-label IAM model, the Spearman correlation between invariance and CER ratio over the 21 damage settings
is $-0.92$ ($p < 0.001$; Fig. \ref{fig:inv}). Across the nine pilot models (scratch and ConvMAE-pretrained, none
trained with damage augmentation) it lies between $-0.81$ and $-0.94$ and holds within the families that overlap the
characters and within the paper-only families. It is not just a matter of stronger damage moving both quantities: with
the severity level held fixed, the correlation across the seven families averages $-0.81$, $-0.88$ and $-0.88$ at the
low, medium and high level. It also holds *across models*: among the eight IAM 10% models (four pretraining variants
× two seeds), the model that is more invariant to a given damage setting tends to be hurt less by it, with a negative
correlation in all 21 settings (mean $-0.69$).

![Invariance of the full-label IAM CRNN to each of the 21 damage settings against the CER rise it causes (log
scale). Blue: families that overlap the characters; grey: paper-only families.](results/figures/fig_invariance_vs_cer.png){#fig:inv width=\linewidth}

Pixel change alone does not order the damage by harm. Averaged over the 19 models, high-strength stains lower the
pixel similarity to 0.80 but raise CER only 1.5 times, while high-strength blur lowers it to 0.83 and raises CER 3.3
times; the feature invariance separates the two (0.70 against 0.15). After rank-regressing out the pixel similarity, the partial correlation in the
nine pilot models stays between $-0.56$ and $-0.87$ (mean $-0.80$, $p \le 0.01$ in each), and is $-0.76$ in a third
scratch seed added later (Table \ref{tab:pix}).

The relation weakens once damage is part of training. In the six augmented models the raw correlation drops to
between $-0.17$ and $-0.43$ and the partial correlation to between $-0.12$ and $-0.39$, none significant: these models
are nearly invariant to the six trained families, which leaves little variation to correlate. In the three
background-normalised models, invariance and pixel similarity are almost the same quantity ($\rho = 0.98$–$0.99$),
and the partial correlation ranges from $-0.51$ to $+0.01$. Over all 19 models the mean partial correlation is
$-0.53$. The finding therefore holds clearly only for models not trained on the damage.

Table: Spearman $\rho$ between invariance and CER ratio over 21 damage settings, by group of models: raw feature
$\rho$, $\rho$ for pixel similarity, and partial $\rho$ of features given pixels (range and mean; "sig." counts
partial $p < 0.05$). Means are computed from the per-run values. {#tab:pix}

| Models | $n$ | Feature $\rho$ | Pixel $\rho$ | Partial $\rho$ | Sig. |
|:--|--:|:--|:--|:--|--:|
| Pilot (no aug.) | 9 | $-0.94$…$-0.81$ ($-0.90$) | $-0.80$…$-0.63$ ($-0.73$) | $-0.87$…$-0.56$ ($-0.80$) | 9 |
| Scratch, seed 3 | 1 | $-0.91$ | $-0.82$ | $-0.76$ | 1 |
| Augmented | 6 | $-0.43$…$-0.17$ ($-0.30$) | $-0.35$…$-0.22$ ($-0.26$) | $-0.39$…$-0.12$ ($-0.25$) | 0 |
| Bg. normalised | 3 | $-0.98$…$-0.95$ ($-0.97$) | $-0.98$…$-0.97$ ($-0.97$) | $-0.51$…$+0.01$ ($-0.22$) | 1 |
| All | 19 | ($-0.72$) | ($-0.62$) | ($-0.53$) | 11 |

# Discussion and limitations

**What the synthetic gains do and do not show.** The drop from 37.9% to 19.4% under synthetic damage is partly
circular: the augmented models were trained on the same six families they are tested on, so the result mostly
measures whether the simulator was learned. Ink loss, held out of both recipes, is the fair synthetic test, and there
the hand-picked recipe is the more robust one (ratio 3.27 against 3.59). A plausible reason is that the hand-picked
recipe blurs and fades half of its lines, and blur and fading are the other two families that touch the strokes,
whereas the derived recipe applies them to 5% and 26% of the lines.

**Where derived damage wins.** Derived augmentation is better on CATMuS, where the damage is real and large, and
hand-picked augmentation is slightly better on IAM, including under synthetic damage. This is the pattern one would
expect if the derived recipe helps by matching the target's damage, but our data cannot separate that explanation
from others. In particular, the CATMuS gain on the hard quartiles (2.4–2.8 points) is about the same as on all lines
(2.2 points). We can therefore say that derived augmentation helps on CATMuS, not that its benefit is specific to the
most damaged lines.

**Confounds and scale.** We fit on one dataset pair in which damage is confounded with script: CATMuS differs from
IAM in language, script, pen and cropping as well as in damage, and the A2 analysis shows that the two strongest
non-damage differences (ink fraction and stroke width) are larger than most damage differences. Some of what the
derived recipe "fits" may thus be script density seen through the paper-level statistics. All results come from one
small recogniser, three seeds at most (two for pretraining), label budgets of 1–10%, and pretraining runs of about
half an hour; the pretraining result says nothing about larger encoders or larger unlabelled pools. The invariance
analysis uses synthetic damage on IAM only. Finally, our fitting step inverts one median response curve per family
and treats families independently; it is far simpler than the statistical estimation and validation of Kanungo et
al. [@kanungo], and we did not validate the fitted damage against real lines with a two-sample test.

**Two pipeline lessons.** Two problems would have silently invalidated results: the black polygon fill of CATMuS
images corrupted the first damage measurements, and our ViT encoder at first attended to the padding of short lines,
so that a line could be read differently depending on its batch neighbours. Both are now checked automatically.

# Conclusion and future work

We derived a damage recipe for handwriting recognition from measured statistics of real medieval lines instead of
choosing it by hand. At our scale the recipe did not make masked-autoencoder pretraining useful, but as plain
augmentation it lowered CER on real medieval lines from 33.8% to 31.6% with 5% of the labels, where a hand-picked
recipe and background normalisation did not. A model's measured invariance to a damage type predicted how much that
damage raised its error, beyond what the pixel change explains, in models not trained on the damage; in augmented
models the link largely disappears. The held-out ink-loss test favours the hand-picked recipe, and the CATMuS gain is
not concentrated on the most damaged lines, so the benefit of measuring rather than guessing remains to be shown to be
damage-specific.

Three next steps follow. First, consistency training on unlabelled lines: train the CRNN with CTC to give the same
output for a clean and a derived-damaged view of the same unlabelled line, the cheapest way to use unlabelled data with
the recipe. Second, one bounded attempt to rescue reconstruction pretraining, with a ten times larger unlabelled pool
and a public pretrained encoder, stopped at a fixed decision date. Third, a cleaner dataset pair with the same script
and different damage, which would show whether the derived recipe follows the damage of the target rather than its
script.

# References {-}

::: {#refs}
:::
