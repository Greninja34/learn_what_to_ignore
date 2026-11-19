# Front matter (pages 1 to 5)

You make pages 1 to 4 yourself in Word from the department template
(`capstone/format/report_template/`). Below is what goes on each page, then the
full abstract for page 5. Pages 6 onwards are in `report.md`.

---

## Page 1: Title page (template: "Page 1-2.docx", first page)

- Line 1: **Dissertation on**
- Title: **"Learning What to Ignore: Deriving Invariance for Self-Supervised Text Recognition"**
- Submitted in partial fulfillment of the requirements for **Bachelor of Technology in Computer Science & Engineering**
- Course: **UE24CS320A – Capstone Project Phase - 1**
- Submitted by (name + SRN, one row each):
  - Arvind Kothamangala, PES2UG24CS628
  - Atharv Sawarkar, PES2UG24CS670
  - Vignesh Nunna, PES2UG24CS582
  - Rohit Rajan, PES2UG25CS821
- Under the guidance of: **Dr. Chandrashekar P Chavan**, Associate Professor, PES University
- **Aug–Dec 2026**
- Department of Computer Science and Engineering, Faculty of Engineering, PES University (keep the template's address block and logo)

## Page 2: Certificate (template: "Page 1-2.docx", second page)

- Dissertation title: **'Learning What to Ignore: Deriving Invariance for Self-Supervised Text Recognition'**
- The same four names with SRNs (as on page 1)
- Guide signature block: **Dr. Chandrashekar P Chavan**, Associate Professor; Chairperson block: **Dr. Sandesh B J**
- Leave the External Viva table empty.
- **Fix two typos in the template text:** it says "(UE23CS320A)" and "Aug 2025 – Dec. 2026". Use **UE24CS320A** and **Aug – Dec 2026**.

## Page 3: Declaration (template: "Page 3-8.docx", page 1)

- Project title in quotes: "Learning What to Ignore: Deriving Invariance for Self-Supervised Text Recognition"
- Guide: Dr. Chandrashekar P Chavan, Associate Professor
- Semester: Aug – Dec 2026
- Table: SRN | Name | Signature, one row per member:
  - PES2UG24CS628 | Arvind Kothamangala
  - PES2UG24CS670 | Atharv Sawarkar
  - PES2UG24CS582 | Vignesh Nunna
  - PES2UG25CS821 | Rohit Rajan

## Page 4: Acknowledgement (template: "Page 3-8.docx", page 2)

- Keep the template wording. Put **Dr. Chandrashekar P Chavan** as the guide and pick "his/her" correctly.
- Optional extra line (only if true): thank the Review 1 and Review 3 panels for their comments on accuracy, use case and target users.
- Since there are four of you, change "I" to "We" throughout.

---

## Page 5: Abstract

Handwritten text recognition (HTR) turns a photograph of a line of handwriting
into typed text. Modern recognisers read clean modern handwriting well, but
their error rises sharply on historical documents with faded ink, darkened
paper, bleed-through and stains. These damaged collections are also the ones
with the fewest typed-out transcriptions to train on. Self-supervised learning
(SSL) can use unlabelled lines instead, but every SSL method must be told which
variations to ignore, and in current practice this list of corruptions is
chosen by hand and re-tuned for each collection.

This project proposes to derive that choice from the documents themselves. We
measure simple damage statistics (paper brightness, show-through, background
unevenness, ink contrast, sharpness, noise) on real manuscript lines, compare
them with clean lines, and turn the difference into a recipe that sets how
often and how strongly each of seven synthetic damage types is applied. The
recipe is then used for masked-autoencoder pretraining and as training
augmentation, and we measure how much each trained model ignores each damage
type.

A one-week pilot on IAM (modern English handwriting) and CATMuS Medieval
(Latin and French manuscripts) tested four assumptions written down before the
runs. Synthetic damage raised the error of a clean-trained recogniser by up to
7.6 times at medium strength. Real manuscripts differed from clean lines mainly
in paper tone and show-through. Pretraining on 30,244 unlabelled lines did not
beat training from scratch. Used as augmentation, however, the derived damage
lowered the character error rate on unseen medieval manuscripts from 33.8% to
31.6% (mean of three seeds), while hand-picked damage and a background clean-up
filter did not. Phase 2 will test consistency training, one bounded
pretraining retry, and transfer to new damage and scripts.

**Keywords:** handwritten text recognition, self-supervised learning, document
degradation, data augmentation, invariance, historical manuscripts.

---

## Pages 6 to 8: Table of contents, list of tables, list of figures

Do not type these by hand. In Word: apply Heading 1/2/3 styles to the chapter
and section titles, add captions with Insert Caption (Figure/Table, numbered by
chapter, e.g. "Table 2.1"), then use References → Table of Contents and
References → Insert Table of Figures (once for Figures, once for Tables).
