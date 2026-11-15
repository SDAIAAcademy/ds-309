---
course: "Responsible Data Science: Privacy, Fairness and Documentation"
code: "DS-309"
version: "2027.1.0"
deck: "day4"
day: 4
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-309/slides/day4.html"
---

# Responsible Data Science: Privacy, Fairness and Documentation

## Day 4: Document and assess

Datasheets, model cards, impact assessment and review by a peer

#### [day4#title] Document and assess

*SDAIA Academy · Responsible Data Science: Privacy, Fairness and Documentation*

Day 4: Datasheets, model cards, impact assessment and review by a peer

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-309

#### [day4#agenda] Document and assess

*Today*

- **Session 1 · Datasheets**: What a datasheet of a de-identified release must answer, filled from the release log
- **Session 2 · Model cards**: A model card with intended use, disaggregated results and the fairness criterion it was held to
- **Session 3 · Impact assessment**: Risks scored on the national framework: likelihood, impact, level, treatment, residual risk and a reviewer
- **Session 4 · Review by someone else**: A colleague's result rerun from their notebook and data, and the documentation gaps that changed it

#### [day4#review-day3] Gender alone shows no gap. Is Ahliya fair?

*Review of Day 3*

**Question:** Anmar reports that eligible women and men are missed at 22.7% and 22.8%. He proposes to close the audit.

- A. Not shown: the intersection of gender and nationality must be checked too
- B. Yes: equal false negative rates by gender meet equal opportunity
- C. No: the selection rates by gender must also be equal
- D. Not until every region by gender by nationality cell is estimated

### Session 1: Datasheets

#### [day4#s1] Datasheets

*Session 1*

- List what a datasheet of a de-identified release must answer
- Fill each answer from a log, not from memory
- Test a datasheet for completeness

#### [day4#why-document] A file without its documentation invites the wrong use

*What a recipient cannot see*

- Waad receives 59,707 rows: she cannot see the **293 suppressed** records
- She cannot see that income is **as recorded**, overstated for the self-employed
- She cannot see that the officer decision is **historical**, not a reviewed outcome

- **The datasheet answers.** Why the data exist, what is in them, how they were made and treated, what risk remains, and what they must not be used for.

#### [day4#datasheet-sections] Seven sections, two of them for de-identified data

*The sections*

- **Motivation.** Who asked, for what purpose, who approved.
- **Composition.** Records, fields released and removed.
- **Collection.** The source and what its fields really record.
- **De-identification.** Risk before, treatment, risk after, utility.
- **Residual risk.** What the treatment does not cover.
- **Uses · Maintenance.** Two sections: allowed and forbidden uses; contact and code.

#### [day4#from-the-log] Fill the datasheet from the release log, never from memory

*Where the numbers come from*

| Release log entry | Value |
| --- | --- |
| Unique on birth date, gender and postcode, before | 59,458 |
| Linkage success, before | 99.2% |
| Suppressed (rule: at most 1%) | 293 |
| k after treatment · links claimed | 5 · 0 |
| Largest change: mean income, Northern Borders | -1.01% |

#### [day4#k-needs-context] "k = 5" means little without what it was measured on

*One number is not a guarantee*

- The **quasi-identifiers**: birth band, gender, nationality, region
- The **suppression**: 293 records, and who they were
- What k does **not** cover: a class that shares one income or one disability value

- **Residual risks in the log.** Attribute disclosure in classes with one value; outside files holding other fields; suppression falling on non-Saudi applicants in small regions.

> **What goes wrong.** A datasheet that says "anonymised" and stops there. The extract is still personal data and stays Restricted.

#### [day4#cannot-rerun] Name what a reader still cannot rerun, and why

*The honest last section*

- **The treatment.** The source stays inside the fund. Acceptable: the code and seed 309 are named.
- **The linkage test.** Needs the register and the truth key, which the fund keeps for audit.
- **The study codes.** Only the data protection officer holds the mapping, by design.

#### [day4#check-datasheet] What must the residual risk section say?

*Checkpoint*

**Question:** Malak's draft says: "k = 5 was reached, so the extract is anonymous and no risk remains." Yahya sends it back.

- A. That k should be raised to 10 before release
- B. That the sharing agreement makes residual risk irrelevant
- C. That 99.2% of applicants can still be linked
- D. The risks k does not cover, and that the extract is still personal data

#### [day4#lab-4-1] The datasheet of the release

Lab 4.1 · 25 min

Write the datasheet for the de-identified release.

[D4_1_write_datasheet_de.ipynb](https://sdaiaacademy.github.io/ds-309/labs/D4_1_write_datasheet_de.ipynb)

- [ ] Read the release log (4 min)
- [ ] Fill the composition and collection sections (7 min)
- [ ] Fill the de-identification and residual risk sections (7 min)
- [ ] Run the completeness check (5 min)
- [ ] Name what a reader still cannot rerun (2 min)
- [ ] ✱ Stretch: Add the distribution terms for the researcher: licence, retention and destruction

### Session 2: Model cards

#### [day4#s2] Model cards

*Session 2*

- Write the intended and out-of-scope uses of a model
- Report disaggregated results with intervals
- State the fairness criterion and what it costs

#### [day4#card-sections] A model card tells a reviewer what the model is for and where it fails

*Mitchell and colleagues, 2019*

- **Model details** and **intended use**
- **Metrics**: which, against what outcome
- **Quantitative analyses**: results by group, with intervals
- **Fairness**: the criterion, the mitigation, its cost
- **Out-of-scope uses** and **caveats**

- **Ahliya today.** No card: only a validation report the audit could not reproduce.

#### [day4#which-accuracy] Report accuracy against what really happened, not against officers

*Metrics against the right outcome*

- **88.1%** validation report: agreement with officers in Riyadh and Makkah
- **84.8%** the card: against the reviewed outcome of 12,000 applications

> **What goes wrong.** Copying the vendor's number into the card. It measured agreement with biased labels, in two regions.

#### [day4#results-table] The results table includes the intersection, with counts and intervals

*Quantitative analyses*

| Group | Eligible | FNR | 95% interval |
| --- | --- | --- | --- |
| Women · Men | 2,413 · 3,928 | 22.7% · 22.8% | overlap |
| Women, non-Saudi | 295 | 29.8% | 24.9 to 35.3 |
| Qassim | 282 | 31.6% | 26.4 to 37.2 |
| Men, non-Saudi | 216 | 26.9% | 21.4 to 33.1 |

#### [day4#card-fairness] State the criterion, the gap, the mitigation, and what it costs

*The fairness section*

Prompt for Model card, Fairness:

```text
Held to equal opportunity: equal false negative rates, because the harmful error is declining an eligible applicant. Largest group gap 12.9 points; group thresholds reduce it to 10.0 at the same accuracy, using gender and nationality, which needs approval. The lasting fix is verified income.
```

#### [day4#out-of-scope] Out-of-scope uses are the ones someone will try

*Limits*

- Declining an application **without an officer's review**
- Scoring applications for **another programme**
- Ranking applicants against each other for a **fixed budget**

- **Caveats.** Trained on historical decisions. Measurement bias in self-employed income, historical bias on family homes, labelling bias in one office, a feedback loop through auto-declines.

#### [day4#check-card] A card that passes every section check

*Checkpoint*

**Question:** Anmar's card has all seven sections. Its results table shows gender and region, each with intervals. Wiam rejects it.

- A. The card omits the validation report's 88.1%
- B. It does not estimate every region by gender cell
- C. It hides the largest gap, which is in gender by nationality
- D. The gap is not closed, so the card cannot be filed

#### [day4#lab-4-2] The model card of Ahliya

Lab 4.2 · 25 min

Write a model card with disaggregated results and intended use.

[D4_2_write_model_card.ipynb](https://sdaiaacademy.github.io/ds-309/labs/D4_2_write_model_card.ipynb)

- [ ] Model details and intended use (5 min)
- [ ] The disaggregated results table (8 min)
- [ ] Fairness criterion, mitigation and cost (5 min)
- [ ] Limits and out-of-scope uses (4 min)
- [ ] Run the card check (3 min)
- [ ] ✱ Stretch: Write a one-paragraph summary of the card for applicants

### Session 3: Impact assessment

#### [day4#s3] Impact assessment

*Session 3*

- Score a risk's likelihood and impact on the national framework's scales
- Choose a treatment and score the residual risk
- Name a human reviewer for every high risk

#### [day4#risk-cycle] Identify, assess, treat, monitor: and assess again after treatment

*National AI Risk Management Framework*

1. **1 · Identify** the risk, who is affected, the evidence
2. **2 · Assess** likelihood × impact, a level and a band
3. **3 · Treat** avoid, mitigate, transfer or accept
4. **4 · Monitor** the residual risk, its owner, its reviewer

#### [day4#risk-scales] Two scores from 1 to 4, and their product is the level

*The scales*

| Score | Likelihood | Impact |
| --- | --- | --- |
| 1 | Rare | Low: limited, contained quickly |
| 2 | Unlikely | Medium: tangible, contained in reasonable time |
| 3 | Likely | High: substantial, needs an organisational response |
| 4 | Almost certain | Catastrophic: severe, wide, possibly irreversible |

Bands: 1 to 2 low · 3 to 6 medium · 8 to 12 high · 16 catastrophic.

#### [day4#argue-from-evidence] Argue every score from a measured number

*A score needs a reason*

- **R2 · wrongful declines.** Likelihood 4: it is happening now, 30% of eligible non-Saudi women declined. Impact 3: support delayed or lost. **Level 12, high.**
- **R4 · the synthetic file.** Likelihood 2: only a regeneration with another setting copies rows. Impact 3: leaf one copied 92.8%. **Level 6, medium.**

> **What goes wrong.** Scores by feeling, then adjusted until the table looks balanced. The register check in Lab 4.3 rejects a reason with no number in it.

#### [day4#treat-residual] A treatment usually lowers the likelihood, not the impact

*Treat and score again*

| Risk | Level | Treatment | Residual |
| --- | --- | --- | --- |
| R1 re-identification | 9 high | k of five, agreement, destruction | 3 |
| R2 wrongful declines | 12 high | officer review, verified income | 6 |
| R3 dashboard budget | 6 | yearly ledger, margins shown | 4 |
| R4 synthetic file | 6 | leakage tests as a release gate | 3 |

#### [day4#human-reviewer] Every risk has an owner; every high risk also has a human reviewer

*Who signs*

- **Owner**: runs the treatment and reports on it
- **Reviewer**: independent of the owner, signs the residual risk
- At Yusr: R1 and R2 go to **Wiam Al-Mutairi**, internal audit

- **Accepting a high risk.** Not a data scientist's decision. The register check rejects "accept" on a high band.

#### [day4#check-likelihood] How likely is a harm that is already happening?

*Checkpoint*

**Question:** Malak scores R2's likelihood as 2, "unlikely", because officers can overturn Ahliya. The audit measured 1,444 of 6,341 eligible applicants declined by the screen.

- A. 2 is right, since officers review every decision
- B. 4: the harm is measured now, without an effective control
- C. 3, so that the level does not reach the catastrophic band
- D. 1, because the gender gap is only 0.1 points

#### [day4#lab-4-3] Score four risks

Lab 4.3 · 25 min

Score four risks on the national framework's likelihood and impact matrix and propose treatments.

[D4_3_score_four_risks.ipynb](https://sdaiaacademy.github.io/ds-309/labs/D4_3_score_four_risks.ipynb)

- [ ] Read the four risks and their evidence (4 min)
- [ ] Score likelihood and impact (7 min)
- [ ] Treat and score again (7 min)
- [ ] Name owners and reviewers (3 min)
- [ ] Run the register check (4 min)
- [ ] ✱ Stretch: Add a fifth risk from your own audit and score it

### Session 4: Review by someone else

#### [day4#s4] Review by someone else

*Session 4*

- Rerun a colleague's result from their notebook and data
- Find the undocumented choices that change a number
- Record documentation gaps that a reviewer can act on

#### [day4#rerun-evidence] A result counts when someone else can rerun it and get the same number

*Reproducibility as evidence*

- The **code** and the **data**, as used
- A **pinned environment**: uv.lock in this course
- Every **seed**, every threshold, every filter
- A **log** of the run that was reported

- **The capstone.** The assessor picks a slice and you recompute one disparity live, from your repository.

#### [day4#peer-claim] "Ahliya misses eligible men more often than eligible women"

*Lab 4.4, the peer's result*

**15.7% · 18.6%** claimed FNR, women · men; gap -2.9 points

- **The README says.** "I used Ahliya's threshold and the scored test set. The interval is a bootstrap."

The code reproduces the claim exactly. Day 3 found 22.7% and 22.8%.

#### [day4#choices-move] Two undocumented choices; one of them flips the sign

*What the README does not say*

| Threshold | Missing income | Rows | Gap, women minus men |
| --- | --- | --- | --- |
| 0.45 (peer) | dropped (peer) | 11,367 | -2.9 pts |
| 0.45 | kept | 12,000 | +0.6 pts |
| 0.5 | dropped | 11,367 | -3.7 pts |
| 0.5 (deployed) | kept | 12,000 | -0.2 pts |

#### [day4#useful-gap] A useful gap says where, by how much, and what to write

*Recording a gap*

- **Where.** load(), the notna() filter.
- **Effect.** Gap -2.9 with the filter, +0.6 without it.
- **Fix.** Keep the rows, or state the filter and who it removes.

> **What goes wrong.** "Results not reproducible." True, and of no use to the author.

#### [day4#corrected] On all rows at 0.5, no gender gap: the claim does not hold

*The corrected result*

Prompt for Review, corrected result:

```text
On all 12,000 reviewed applications at Ahliya's threshold of 0.5, the false negative rate is 0.227 for women and 0.228 for men (gap -0.002, 95% bootstrap interval -0.020 to +0.018, seed 309).
```

#### [day4#check-review] Which gap explains the different number?

*Checkpoint*

**Question:** A peer reports an FNR gap of -2.9 points; your rerun on all rows at 0.5 gives -0.2. The bootstrap is unseeded, the threshold is 0.45, and 633 rows with missing income are dropped.

- A. The dropped rows: removing them alone takes the gap from +0.6 to -2.9
- B. The unseeded bootstrap, because each run differs
- C. The threshold of 0.45, because it differs from the documented 0.5
- D. A different pandas version on the peer's machine

#### [day4#lab-4-4] Rerun a peer's result

Lab 4.4 · 25 min

Rerun one result from a peer's day 2 or day 3 notebook and record the documentation gaps.

[D4_4_rerun_one_result.ipynb](https://sdaiaacademy.github.io/ds-309/labs/D4_4_rerun_one_result.ipynb)

- [ ] Run the peer's code as given (5 min)
- [ ] Compare with the claimed number (4 min)
- [ ] Find the choices that move it (9 min)
- [ ] Record the gaps (5 min)
- [ ] State the corrected result (2 min)
- [ ] ✱ Stretch: Swap notebooks with a neighbour and rerun one of their Day 2 or Day 3 results

#### [day4#wrap-up] Write from the log, score from the evidence, rerun before you believe

*Day 4 · Three things to keep*

- **From the log.** Datasheet and card numbers trace to the approved run, with their limits stated.
- **From the evidence.** Likelihood and impact argued from measured numbers; a reviewer for every high risk.
- **Rerun.** A filter nobody documented flipped a peer's conclusion.

#### [day4#next] The release pack for the Sabeel Scholarship Fund

*Next · Capstone*

- A treated extract with its release log
- A fairness audit with intervals, a datasheet, a model card and an impact assessment
- A public repository whose README says how to rerun every number
- Ten minutes: the assessor picks a slice and you recompute one disparity live
