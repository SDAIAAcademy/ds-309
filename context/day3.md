---
course: "Responsible Data Science: Privacy, Fairness and Documentation"
code: "DS-309"
version: "2027.1.0"
deck: "day3"
day: 3
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-309/slides/day3.html"
---

# Responsible Data Science: Privacy, Fairness and Documentation

## Day 3: Audit for fairness

Disaggregated errors, conflicting criteria, bias types and mitigation

#### [day3#title] Audit for fairness

*SDAIA Academy · Responsible Data Science: Privacy, Fairness and Documentation*

Day 3: Disaggregated errors, conflicting criteria, bias types and mitigation

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-309

#### [day3#agenda] Audit for fairness

*Today*

- **Session 1 · Disaggregating errors**: Error rates by group and by intersection, with intervals that say how much a small group can tell
- **Session 2 · Criteria that conflict**: Demographic parity, equal opportunity and predictive parity, why they conflict, and how to choose
- **Session 3 · Bias across the lifecycle**: Where in the lifecycle a bias enters, its name in the national guide, and the check that tells two apart
- **Session 4 · Mitigation and its cost**: Reweighting before training, group thresholds after it, and what each costs in accuracy and disparity

#### [day3#review-day2] A monthly dashboard at epsilon 0.5: what is spent in a year?

*Review of Day 2*

**Question:** Bashayer approves the district counts at epsilon 0.5 and asks for them every month. Yahya asks what the fund will have spent after a year.

- A. 0.5, because each month is a separate table
- B. 6, because the same applicants are counted twelve times
- C. 0.5, because later months are post-processing
- D. About 0.04, a twelfth of 0.5

### Session 1: Disaggregating errors

#### [day3#s1] Disaggregating errors

*Session 1*

- Compute false negative and false positive rates by group with intervals
- Slice by an intersection of two attributes
- Report a small group without overclaiming

#### [day3#two-errors] For a support decision, the two errors do different harm

*What an audit counts*

- **False negative.** An eligible applicant declined by Ahliya. The harm the fund exists to prevent. **FNR** = missed eligible / all eligible.
- **False positive.** Support passed to someone not eligible. A cost to the fund, caught later by an officer. **FPR** = wrongly passed / all not eligible.

In the reference data: 12,000 reviewed applications, 6,341 eligible, 5,280 passed by Ahliya at a threshold of 0.5.

#### [day3#recap-intervals] Every rate gets an interval, and small groups get wide ones

*Recap from DS-204 and DS-207*

- A rate from 2,413 eligible women is precise
- A rate from 4 eligible applicants is a guess
- The **Wilson interval** stays inside 0 to 1 and behaves for small counts
- Report the count beside every rate

- **Same 50% rate.** From 200 eligible: 43% to 57%. From 4 eligible: 15% to 85%.

#### [day3#by-gender] By gender alone, Ahliya misses eligible women and men at the same rate

*Lab 3.1, the reference run*

| Group | Eligible | FNR | 95% interval | FPR |
| --- | --- | --- | --- | --- |
| Women | 2,413 | 22.7% | 21.0 to 24.4 | 9.6% |
| Men | 3,928 | 22.8% | 21.6 to 24.2 | 5.6% |
| Non-Saudi | 511 | 28.6% | 24.8 to 32.6 | 6.5% |
| Saudi | 5,830 | 22.3% | 21.2 to 23.4 | 6.8% |

#### [day3#intersection] Non-Saudi women are missed most, and gender alone hides it

*Slice by two attributes at once*

| Item | Value |
| --- | --- |
| Women, non-Saudi | 29.8% |
| Men, non-Saudi | 26.9% |
| Men, Saudi | 22.6% |
| Women, Saudi | 21.7% |

False negative rate. Non-Saudi women: 295 eligible, interval 24.9% to 35.3%.

#### [day3#small-cells] Each extra attribute splits the data until the rates mean nothing

*How far to slice*

**23 of 52** region by gender by nationality cells with fewer than 30 eligible applicants

- **Al-Jouf, non-Saudi women.** 4 eligible, 3 missed: FNR 75%, interval 30% to 95%. Report "too few to estimate (4)", not 75%.

> **What goes wrong.** Fifty-two cells, one of them extreme by chance, and a headline about Al-Jouf. Many comparisons produce false alarms; small cells produce loud ones.

#### [day3#finding-sentence] One sentence: the group, the rate, the interval, the comparison, the limit

*Reporting a finding*

Prompt for Audit report, finding 1:

```text
Ahliya declines 30% of eligible non-Saudi women (95% interval 25% to 35%) against 22% of all other eligible applicants; gender alone shows no gap, so the margins understate it.
```

- **Rate and interval.** Never a bare percentage.
- **Against whom.** The comparison group is named.
- **What is not claimed.** No cause yet: that is Session 3.

#### [day3#calibration-pointer] Calibration by group and explanations are DS-305

*What this audit does not cover*

- Today: errors at the decision threshold, by group
- Not today: whether a score of 0.7 means the same chance for every group (calibration)
- Not today: why a particular applicant was scored low (explanation)

- **Next course.** DS-305 Uncertainty, Interpretability and Model Validation takes both further.

#### [day3#check-interval] What can the audit say about Hail?

*Checkpoint*

**Question:** Hail has an FNR of 18.2% from 110 eligible applicants, interval 12.1% to 26.4%. The FNR over all 6,341 eligible applicants is 22.8%. Wiam asks whether Ahliya treats Hail's applicants better.

- A. Yes: 18.2% is lower than 22.8%, so Hail is treated better
- B. Nothing at all, since 110 applicants is too few to compute a rate
- C. No difference is shown: the interval includes the overall rate
- D. No: small regions are always disadvantaged by the model

#### [day3#lab-3-1] Error rates with intervals

Lab 3.1 · 25 min

Compute error rates by gender, region and nationality with intervals.

[D3_1_compute_error_rates.ipynb](https://sdaiaacademy.github.io/ds-309/labs/D3_1_compute_error_rates.ipynb)

- [ ] Confusion counts by group (6 min)
- [ ] Rates with Wilson intervals (7 min)
- [ ] One intersection (6 min)
- [ ] Mark the cells too small to read (3 min)
- [ ] One sentence per finding (3 min)
- [ ] ✱ Stretch: Rebuild the table with Fairlearn's MetricFrame and compare

### Session 2: Criteria that conflict

#### [day3#s2] Criteria that conflict

*Session 2*

- Compute demographic parity, equal opportunity and predictive parity gaps
- Show why they cannot all hold when base rates differ
- Choose a criterion from the harm of each kind of error

#### [day3#three-criteria] Four criteria, each reasonable, each equalising something different

*What "fair" can mean*

| Criterion | Equal across groups | Plain words |
| --- | --- | --- |
| **Demographic parity** | selection rate | pass the same share of each group |
| **Equal opportunity** | false negative rate | miss eligible people equally often |
| **Equalised odds** | false negative and false positive rates | both errors equal |
| **Predictive parity** | precision | a pass is equally reliable for each group |

#### [day3#base-rates-differ] Eligibility is more common among women applicants than among men

*The fact that forces a choice*

| Item | Value |
| --- | --- |
| Women | 59.7% |
| Men | 49.3% |

- Share eligible after full review (Lab 3.2)
- Women applicants are more often heads of lower-income households in this data
- When base rates differ, a model that is not perfect cannot satisfy all criteria at once

#### [day3#at-one-threshold] At one threshold, misses are equal and selection is not

*Lab 3.2, the reference run*

| Threshold 0.5 for all | Selection | FNR | Precision |
| --- | --- | --- | --- |
| Women | 50.1% | 22.7% | 92.3% |
| Men | 40.9% | 22.8% | 93.0% |
| Gap | +9.1 pts | -0.2 pts | -0.8 pts |

Equal opportunity holds almost exactly; demographic parity does not.

#### [day3#force-parity] Equal selection makes Ahliya miss eligible women far more often

*Force demographic parity*

| Equal selection (thresholds 0.620 and 0.432) | Selection | FNR | Precision |
| --- | --- | --- | --- |
| Women | 44.0% | 30.9% | 93.8% |
| Men | 44.0% | 18.5% | 91.4% |
| Gap | 0 | +12.4 pts | +2.4 pts |

> **The trade.** One gap closes, another opens. Here the gap that opens is in the harmful error.

#### [day3#choose-by-harm] Choose the criterion from the decision and the harm of each error

*How to choose*

- SDAIA's AI Ethics Principles ask that fairness metrics be chosen at design time from the kind of decision and the harm and benefit of correct and incorrect predictions
- Ahliya allocates **support by need**; the harmful error is the **missed eligible applicant**
- So: **equal opportunity**, with the selection gap explained by need

- **When parity fits.** When need is believed equal and the labels are suspect, or when a fixed opportunity is shared out.

#### [day3#check-criterion] Which criterion for a support decision?

*Checkpoint*

**Question:** Ahliya decides who is passed to an officer for housing support. Eligible applicants are more common among women. Bashayer asks which fairness criterion the fund should commit to.

- A. Equal false negative rates: miss eligible applicants equally in each group
- B. Equal selection rates: pass the same share of women and men
- C. All three criteria at once, to be safe
- D. None: Ahliya does not use gender, so it is fair

#### [day3#lab-3-2] Two criteria in conflict

Lab 3.2 · 25 min

Show two fairness criteria conflicting on the test set and choose one.

[D3_2_show_two_fairness.ipynb](https://sdaiaacademy.github.io/ds-309/labs/D3_2_show_two_fairness.ipynb)

- [ ] Three gaps at the current threshold (6 min)
- [ ] Equalise selection rates and watch the other gaps (8 min)
- [ ] Equalise false negative rates instead (6 min)
- [ ] Choose and justify (5 min)
- [ ] ✱ Stretch: Find the thresholds that equalise predictive parity and read the other gaps

### Session 3: Bias across the lifecycle

#### [day3#s3] Bias across the lifecycle

*Session 3*

- Place a finding in a stage of the AI system lifecycle
- Name its bias type from the national bias guide
- Run the check that separates two neighbouring types

#### [day3#lifecycle] The AI Ethics Principles name four stages, and bias can enter at each

*Where bias enters*

1. **1 · Plan and Design** purpose, target, the fairness metric and its threshold
2. **2 · Prepare Input Data** collection, recording, labels
3. **3 · Build and Validate** features, model choice, evaluation
4. **4 · Deploy and Monitor** use, feedback, retraining

#### [day3#bias-guide] SDAIA's AI Bias Reference Guide defines more than a hundred bias types

*The national vocabulary*

| Type | In the guide's terms |
| --- | --- |
| **Historical Bias** | training data carries past circumstances that no longer hold |
| **Measurement Bias** | values systematically over- or under-recorded |
| **Labeling Bias** | labels shaped by the people who assigned them |
| **Evaluation Bias** | evaluation data or metrics that do not reflect real use |
| **Feedback Loop Bias** | the system's outputs become its future inputs |

#### [day3#same-gap-two-causes] The same gap can have two causes that need opposite fixes

*Why the type matters*

- **Measurement or labelling?** Measurement: a feature is recorded wrongly (fix the recording). Labelling: the outcome used for training is wrong (fix the labels).
- **Historical or labelling?** Historical: labels followed a rule that has since changed (retrain on the current rule). Labelling: labels were wrong when made (relabel or review).

#### [day3#evidence-f1-f3] Three findings, three checks, three different types

*Lab 3.3, the reference run*

| Finding | Check | Result | Type |
| --- | --- | --- | --- |
| Self-employed: FNR 65% | recorded against verified income | median ratio 1.73; others 1.00 | Measurement |
| Family home: FNR 36% against 17% for renters | officers' approvals before and after the July 2024 rule change | 22% before, 49% after; renters 49% throughout | Historical |
| Qassim: highest FNR | officers' declines of eligible applicants, by office and gender | women 43% in Qassim, 23% elsewhere; men equal | Labelling |

#### [day3#evidence-f4-f5] Two findings sit outside the data: in validation and in deployment

*Lab 3.3, the reference run*

- **Evaluation Bias · Build and Validate.** The validation report claimed accuracy 0.881 on officers' decisions in Riyadh and Makkah. Against the reviewed outcome: 0.845 there, 0.850 elsewhere.
- **Feedback Loop Bias · Deploy and Monitor.** 37.4% of applications are auto-declined and never reviewed, so they never get a label. Retraining cannot see its own misses; 62.8% of self-employed applicants are auto-declined.

#### [day3#check-bias-type] Measurement or labelling?

*Checkpoint*

**Question:** Self-employed applicants are missed by Ahliya far more often. An income audit shows their recorded income is 1.73 times the verified income; for employees it is 1.00. Which type fits, and what is the first fix?

- A. Labeling Bias: retrain on corrected decisions
- B. Sampling Bias: reweight the self-employed in training
- C. Historical Bias: retrain on recent applications only
- D. Measurement Bias: record net income for the self-employed

#### [day3#lab-3-3] Five findings, five types

Lab 3.3 · 25 min

Map five findings to bias types in the national guide.

[D3_3_map_five_findings.ipynb](https://sdaiaacademy.github.io/ds-309/labs/D3_3_map_five_findings.ipynb)

- [ ] Read the five findings (3 min)
- [ ] Run the evidence check for each (12 min)
- [ ] Map each to a type and a stage (6 min)
- [ ] Check the mapping (4 min)
- [ ] ✱ Stretch: Write the sixth finding you would look for next, and its check

### Session 4: Mitigation and its cost

#### [day3#s4] Mitigation and its cost

*Session 4*

- Apply reweighting before training
- Apply group thresholds after training
- Compare accuracy and disparity, and recommend

#### [day3#three-points] You can act before training, during it, or after it

*Mitigation*

- **Before: pre-processing.** Change the training data: **reweighting**, resampling, relabelling, fixing a feature.
- **During: in-processing.** A constraint in the fitting, such as Fairlearn's reductions. Named here, not practised.
- **After: post-processing.** Change the decision rule: **a threshold per group**.

#### [day3#reweighting] Reweighting makes group and label independent in the training data

*Pre-processing*

```python
# file: python
pg  = df["group"].value_counts(normalize=True)
py  = df["y"].value_counts(normalize=True)
pgy = df.groupby(["group", "y"]).size() / len(df)
idx = pd.MultiIndex.from_arrays([df["group"], df["y"]])
w   = (pg[df["group"]].to_numpy() * py[df["y"]].to_numpy()
       / pgy.reindex(idx).to_numpy())
model.fit(X, y, logisticregression__sample_weight=w)
```

- Rare combinations, such as approved non-Saudi women, weigh more
- The weights average 1
- It can only fix what the **labels' balance** causes

#### [day3#group-thresholds] A threshold per group, tuned on one half and reported on the other

*Post-processing*

- Target: each group's FNR equal to the overall 22.5%
- Tuned thresholds: non-Saudi women 0.468, Saudi women 0.511, non-Saudi men 0.470, Saudi men 0.499
- Reported on reviewed applications not used to tune

- **A legal question, not only a technical one.** The rule now uses gender and nationality at the moment of decision. The data protection officer and legal counsel decide whether that is allowed and how it is explained.

#### [day3#mitigation-results] Thresholds narrow the gap a little; reweighting barely moves it

*Lab 3.4, the reference run*

| Reported on 6,050 reviewed applications | Accuracy | Largest FNR gap | FNR, non-Saudi women |
| --- | --- | --- | --- |
| Baseline | 84.5% | 12.9 pts | 34.9% |
| Reweighting | 84.5% | 12.6 pts | 34.9% |
| Group thresholds | 84.5% | 10.0 pts | 32.2% |

> **Accuracy did not fall.** The cost here is not accuracy: it is a rule that uses protected attributes, and a gap that remains.

#### [day3#recommendation] Fix the source, use thresholds only as an interim, and say what remains

*The audit's recommendation*

1. **1 · Source** verify or impute income properly; net income for the self-employed
2. **2 · Interim** group thresholds, if legally approved, with officer review of declines
3. **3 · Monitor** review a sample of auto-declines, so retraining sees its misses

#### [day3#check-mitigation] Which mitigation would you recommend?

*Checkpoint*

**Question:** Reweighting moved the FNR gap from 12.9 to 12.6 points. Group thresholds moved it to 10.0, at the same accuracy. The gap comes mostly from missing and mis-recorded income. What do you recommend to Bashayer?

- A. Group thresholds as the permanent fix, since accuracy did not fall
- B. Fix income recording first; thresholds only as an approved interim measure
- C. Reweighting, because pre-processing is always preferable
- D. Neither, since the gap is not closed completely

#### [day3#lab-3-4] Reweighting and a threshold change

Lab 3.4 · 25 min

Apply reweighting and a threshold change and compare accuracy and disparity.

[D3_4_apply_reweighting_threshold.ipynb](https://sdaiaacademy.github.io/ds-309/labs/D3_4_apply_reweighting_threshold.ipynb)

- [ ] The baseline: accuracy and gaps (4 min)
- [ ] Reweight the training data and retrain (8 min)
- [ ] Group thresholds on the baseline model (7 min)
- [ ] One comparison table and a recommendation (6 min)
- [ ] ✱ Stretch: Repeat the threshold change for the intersection of Day 3 Session 1

#### [day3#wrap-up] Disaggregate, choose the criterion by the harm, diagnose before mitigating

*Day 3 · Three things to keep*

- **Disaggregate.** Gender alone showed no gap; non-Saudi women are missed at 30%. Intervals and counts beside every rate.
- **Choose.** Different base rates make criteria conflict. For support by need: equal false negative rates.
- **Diagnose.** Five findings, five types. Reweighting failed where the cause was a feature.

#### [day3#next] Document and assess

*Tomorrow · Day 4*

- The datasheet of the de-identified release, filled from its log
- The model card of Ahliya with disaggregated results
- Four risks scored on the national framework's likelihood and impact matrix
- A peer's result rerun, and the gaps that changed the number
