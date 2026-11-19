# Damage types and the statistics that track them

From the code: `STAT` and `DIRECTION` in `lwti/damage/derive.py`, the statistics in `lwti/damage/measure.py`, the damage functions in `lwti/damage/families.py`.

| # | Damage type (what we add) | How we simulate it | Statistic that tracks it | How the statistic is measured | Damage pushes it… |
|---|---|---|---|---|---|
| 1 | **Paper tone** | Darken the paper (scale its brightness down) | **Paper level** | Median brightness of the paper pixels ÷ 255 | **down** (darker paper) |
| 2 | **Show-through** | Add a mirrored, shifted, blurred, faint copy of the line, as if the back page shows through | **Faint grey on paper** | Share of paper pixels that are slightly grey | **up** |
| 3 | **Stain** | Add smooth dark patches | **Background unevenness** | Spread of the large-scale paper brightness | **up** |
| 4 | **Fade** | Make the ink lighter, closer to the paper | **Ink–paper contrast** | (paper level − ink level) ÷ 255 | **down** |
| 5 | **Blur** | Gaussian blur (out of focus) | **Sharpness** | Edge strength (Laplacian variance) ÷ contrast² | **down** |
| 6 | **Noise** | Add random speckle (sensor noise) | **Pixel noise** | Spread of the fine-detail residual on the paper | **up** |
| 7 | **Ink loss** (held out) | Erase random bits of the strokes | **Ink fraction** | Share of pixels that are ink | **down** |
| – | *(no damage)* | – | **Stroke width** | 2 × ink area ÷ ink outline length (pen width in px) | – |

## How to read it

- **One statistic per damage type.** For each pair we checked that adding more of the damage moves its statistic steadily in the direction shown.
- **The direction matters for the derive step.** A CATMuS line counts as "damaged by tone" only if its paper is *darker* than 95% of clean IAM lines. It counts as "damaged by noise" only if it is *noisier* than 95% of them.
- **Ink and paper are split first,** with Otsu's threshold on a slightly smoothed copy of the line, so noise is not counted as ink. Only real pixels are used: the old CATMuS black polygon fill is masked out.
- **Stroke width and ink fraction are the "scale" pair.** They differ between the datasets because of pen and script, not damage. Ink fraction is in principle ink loss's statistic, but ink loss is held out, so it is never used to derive anything.

## What is chosen and what is derived

- **Chosen by us:** the 7 damage types, the 8 statistics, the pairing of damage type to statistic, the low/medium/high levels, the hand-picked ranges, and holding out ink loss.
- **Derived from the data (6 trained types):**
  - **how often** each damage is applied: the share of CATMuS lines outside the clean IAM 5–95% band;
  - **how strong** it is: their statistic values, converted back into strengths with each damage's strength curve.
