---
course: "Responsible Data Science: Privacy, Fairness and Documentation"
code: "DS-309"
version: "2027.1.0"
deck: "day2"
day: 2
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-309/slides/day2.html"
---

# Responsible Data Science: Privacy, Fairness and Documentation

## Day 2: Release with less risk

Generalisation, differential privacy, budgets and synthetic data

#### [day2#title] Release with less risk

*SDAIA Academy · Responsible Data Science: Privacy, Fairness and Documentation*

Day 2: Generalisation, differential privacy, budgets and synthetic data

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-309

#### [day2#agenda] Release with less risk

*Today*

- **Session 1 · Generalisation and suppression**: Generalise and suppress until every record hides among five, and measure what the analysis loses
- **Session 2 · Differential privacy for counts**: The promise of differential privacy, calibrated noise on counts, and the error a budget costs
- **Session 3 · Budgets and composition**: Sequential and parallel composition, bounded means, and one budget spread over several queries
- **Session 4 · Synthetic data and leakage**: A synthetic extract generated column by column, its utility, and the tests that show it copies people

#### [day2#review-day1] What did the linkage attack actually need?

*Review of Day 1*

**Question:** Yesterday three fields linked 99.2% of the register's applicants to their income and decision. Yahya asks what the attacker had to have. Which answer is right?

- A. The key that maps study codes back to applicants
- B. At least one direct identifier left in the release
- C. An outside file sharing birth date, gender and postcode with the release
- D. The applicants' incomes, to match them to the release

### Session 1: Generalisation and suppression

#### [day2#s1] Generalisation and suppression

*Session 1*

- Generalise quasi-identifiers along a hierarchy
- Suppress the records that stay below k
- Measure the utility cost on key statistics

#### [day2#hierarchies] Each quasi-identifier climbs its own hierarchy, one level at a time

*Generalisation*

| Level | birth | place |
| --- | --- | --- |
| 0 | birth date 1989-10-20 | postcode 10900 |
| 1 | birth year 1989 | district RYD-07 |
| 2 | five-year band 1985-1989 | region Riyadh |
| 3 | ten-year band 1980-1989 |  |

Every level up merges classes. The anonymisation guideline names this technique: specific values replaced by more general ones, such as ages in bands.

#### [day2#lattice-search] Search the lattice for the least general node that meets the target

*Lab 2.1, the reference run*

| Records below five | postcode | district | region |
| --- | --- | --- | --- |
| birth date | 60,000 | 60,000 | 59,870 |
| birth year | 41,404 | 8,576 | 1,744 |
| five-year band | 13,488 | 1,728 | 293 |
| ten-year band | 7,669 | 738 | 84 |

- Rule: suppress at most **1%** of records
- Least general node that meets it: **five-year band and region**
- 293 records left to suppress

#### [day2#suppression] Suppress the records still below five, and log how many

*The last step*

- **59,707** records kept
- **293** suppressed (0.49%)
- **k = 5** every record hides among five

> **What goes wrong.** The suppressed records are not random. They are the rare combinations: mostly non-Saudi applicants in small regions. The cost of the control lands on the smallest groups.

#### [day2#utility-cost] The three key statistics moved by at most 1%

*What the analysis lost*

| Statistic | Before | After | Change |
| --- | --- | --- | --- |
| Approval rate, women | 0.5056 | 0.5054 | -0.04% |
| Approval rate, men | 0.4266 | 0.4265 | -0.02% |
| Mean income, Northern Borders | 8,211 | 8,128 | -1.01% |
| Mean income, Riyadh | 8,313 | 8,313 | 0.00% |
| Mean household size, non-Saudi | 4.526 | 4.517 | -0.20% |

#### [day2#linkage-after] The same register now links nobody to a single record

*The attack, rerun*

**99.2% → 0** register applicants linked to exactly one record, before and after treatment

- **Identity disclosure.** Blocked for this outside file: every match now has at least five candidates.
- **Attribute disclosure.** Not blocked: a class of five that all declined still tells the attacker the decision.

#### [day2#k-limits] k protects the fields you chose against the attacks you imagined

*When k-anonymity is not enough*

- **Homogeneity.** Everyone in the class shares the sensitive value.
- **Background knowledge.** The attacker knows a field you did not treat as a quasi-identifier.
- **Repeated releases.** Two treated versions of the same table, intersected, shrink the classes.

> **Takeaway.** Treat row-level releases as personal data under an agreement, even at k of five. For published numbers, use a control with a guarantee: Session 2.

#### [day2#check-suppress] Suppress more, or generalise more?

*Checkpoint*

**Question:** At five-year band and district, 1,728 records (2.9%) are below five. Waad wants to keep the district. Malak can suppress those 1,728 or move to region and suppress 293. What should she weigh?

- A. Which small groups the 1,728 are, and whether Waad's question needs the district
- B. Always the option with fewer suppressed records
- C. Always suppression, since it leaves every kept record exact
- D. Whichever option gives the higher k

#### [day2#lab-2-1] Reach k of five

Lab 2.1 · 25 min

Reach k of at least five and measure the change in three key statistics.

[D2_1_reach_k_least.ipynb](https://sdaiaacademy.github.io/ds-309/labs/D2_1_reach_k_least.ipynb)

- [ ] Three key statistics before treatment (5 min)
- [ ] Generalise birth date and postcode step by step (8 min)
- [ ] Suppress what is still below five (4 min)
- [ ] The three statistics after treatment (5 min)
- [ ] Rerun the linkage (3 min)
- [ ] ✱ Stretch: Find a second treatment that keeps the district, and compare its cost

### Session 2: Differential privacy for counts

#### [day2#s2] Differential privacy for counts

*Session 2*

- State what the differential privacy promise covers and what it does not
- Add calibrated noise to counts with a library
- Measure the error that a budget costs

#### [day2#dp-promise] The output barely depends on whether any one person is in the data

*Differential privacy*

- Two datasets that differ by **one applicant**
- A randomised release gives almost the same **distribution of outputs** on both
- **Epsilon** bounds "almost": smaller epsilon, closer distributions, more privacy
- It holds whatever the attacker knows, including every other record

- **What it does not promise.** That nothing about the population is learnt. A count shows that a district has many approvals; that is the point of publishing it.

#### [day2#sensitivity] Noise is scaled to the most one person can change the answer

*How much noise*

1. **1 · Sensitivity** adding one applicant changes one district count by 1
2. **2 · Scale** sensitivity divided by epsilon
3. **3 · Noise** drawn from a Laplace distribution with that scale

- **epsilon 1.** scale 1: typical error about one applicant
- **epsilon 0.5.** scale 2
- **epsilon 0.1.** scale 10: typical error about ten

#### [day2#opendp-code] The library builds the measurement and tells you what it spends

*Lab 2.2 in five lines*

```python
# file: python
import opendp.prelude as dp
dp.enable_features("contrib")
domain = dp.vector_domain(dp.atom_domain(T=int), size=59)
meas = dp.m.make_laplace(domain, dp.l1_distance(T=int), scale=1 / eps)
released = meas(counts)          # 59 noisy counts
meas.map(d_in=1)                 # the epsilon spent when one person changes
```

> **Check the claim with the library.** `map` computes the privacy loss from the domain, the distance and the scale. Never trust an epsilon typed in a report.

#### [day2#error-by-budget] Ten times less budget costs about ten times more error

*Lab 2.2, the reference run*

| epsilon | Mean absolute error | 95th percentile | Relative error, ten smallest districts |
| --- | --- | --- | --- |
| 0.1 | 9.98 | 30 | 16.0% |
| 0.5 | 1.92 | 6 | 3.1% |
| 1.0 | 0.85 | 3 | 1.5% |

59 districts, 27,189 approved applicants, smallest district 36. 300 repeated releases per budget.

#### [day2#recommend-budget] Choose the smallest budget that meets the accuracy the use needs

*From a curve to a decision*

- The use: a dashboard that compares districts
- The rule agreed with Bashayer: typical error under **5%** in the smallest districts
- 0.1 fails (16%), **0.5 meets it (3.1%)**, 1.0 meets it with margin
- Recommendation: **epsilon 0.5 per release**

- **The budget is per release.** A monthly refresh at 0.5 spends 6 a year. Session 3 is about that.

#### [day2#post-processing] Anything computed from a released value spends no more budget

*After the noise*

- **Clamp.** Negative counts set to zero.
- **Round.** Whole numbers for a dashboard.
- **Aggregate.** Regional totals summed from district counts.

> **What goes wrong.** Recomputing from the true data "to fix" a strange noisy value is not post-processing. It spends budget, usually without anyone noticing.

#### [day2#check-epsilon] What does a smaller epsilon buy?

*Checkpoint*

**Question:** Malak releases the 59 district counts at epsilon 0.1 instead of 0.5. Bashayer asks what changed. Which statement is right?

- A. The large districts now carry most of the error
- B. The counts are now private, where before they were not
- C. The noise is 59 times larger, one share per district
- D. Each count's noise is about five times larger, and the guarantee is stronger

#### [day2#lab-2-2] District counts at three budgets

Lab 2.2 · 25 min

Release district counts at three budgets and plot the error.

[D2_2_release_district_counts.ipynb](https://sdaiaacademy.github.io/ds-309/labs/D2_2_release_district_counts.ipynb)

- [ ] True counts of approved applicants by district (4 min)
- [ ] One noisy release with the library (6 min)
- [ ] Repeat at three budgets (7 min)
- [ ] Plot the error against the budget (5 min)
- [ ] Recommend a budget (3 min)
- [ ] ✱ Stretch: Post-process the counts (no negatives, whole numbers) and check that the error does not grow

### Session 3: Budgets and composition

#### [day2#s3] Budgets and composition

*Session 3*

- Add up privacy loss under sequential and parallel composition
- Release a bounded mean with a library
- Allocate one budget across queries by need

#### [day2#composition] Epsilons add up over the same people, not over different people

*Spending a budget*

- **Sequential composition.** Two releases about the same applicants: the epsilons add. Mean income at 0.3 and household size at 0.2 spend 0.5.
- **Parallel composition.** Releases about disjoint people: the largest epsilon counts once. 13 region counts at 0.1 spend 0.1, not 1.3.

#### [day2#four-queries] Four queries share it, and each has its own sensitivity

*Yahya's approved budget: epsilon 1 for the year*

| Query | Released | One applicant changes it by |
| --- | --- | --- |
| Q1 | applicants per region, 13 counts | 1 in one count |
| Q2 | mean income, clamped to 0 to 30,000 riyals | sum by 30,000; count by 1 |
| Q3 | approved per district, 59 counts | 1 in one count |
| Q4 | mean household size, clamped to 1 to 12 | sum by 12; count by 1 |

A mean is a noisy sum over a noisy count, each with half the query's epsilon.

#### [day2#equal-split] An equal split wastes budget on the queries that do not need it

*Lab 2.3, the reference run*

| Item | Value |
| --- | --- |
| Q3 district counts | 2.05% |
| Q1 region counts | 0.24% |
| Q2 mean income | 0.05% |
| Q4 mean household | 0.04% |

Mean relative error with epsilon 0.25 each.

#### [day2#split-by-need] Give each query budget in proportion to its error at epsilon 1

*Allocate by need*

| Query | Equal: epsilon | Equal: error | By need: epsilon | By need: error |
| --- | --- | --- | --- | --- |
| Q1 | 0.25 | 0.24% | 0.099 | 0.61% |
| Q2 | 0.25 | 0.05% | 0.025 | 0.57% |
| Q3 | 0.25 | 2.05% | 0.857 | 0.54% |
| Q4 | 0.25 | 0.04% | 0.019 | 0.53% |

> **Takeaway.** The worst error falls from 2.05% to 0.61% for the same total budget.

#### [day2#ledger] Let the library keep the ledger, and check it adds up to the budget

*Accounting*

```python
# file: Lab 2.3 output
{'Q1': 0.099426, 'Q2': 0.024857,
 'Q3': 0.856597, 'Q4': 0.01912}  total 1.0
```

- Each value is `map` of the measurement, not a typed number
- Q2 and Q4 each sum two measurements: the sum and the count
- The ledger goes into the release log, with the date and the approver

#### [day2#monthly-cost] Monthly releases from one yearly budget make every release noisier

*The cost of repetition*

**0.61% → 7.2%** worst mean relative error, one yearly release against twelve monthly releases from the same budget

- **The decision is Bashayer's.** Fresher numbers or more accurate numbers. The budget makes the trade visible instead of hiding it in suppression rules.

#### [day2#check-parallel] How much did the region counts spend?

*Checkpoint*

**Question:** Malak releases applicants per region, 13 counts, each with noise of scale 10 (epsilon 0.1 for a count). Every applicant is in exactly one region. What has the release spent?

- A. 1.3, the sum over the 13 regions
- B. 0.1, because the regions hold disjoint applicants
- C. About 0.008, a thirteenth of 0.1
- D. Nothing, since counts are aggregates

#### [day2#lab-2-3] Split one budget over four queries

Lab 2.3 · 25 min

Split one budget across four queries and justify the allocation.

[D2_3_split_one_budget.ipynb](https://sdaiaacademy.github.io/ds-309/labs/D2_3_split_one_budget.ipynb)

- [ ] The four queries and their sensitivities (5 min)
- [ ] An equal split and its errors (6 min)
- [ ] A split by need (7 min)
- [ ] Check that the ledger adds up to the budget (4 min)
- [ ] Justify the allocation (3 min)
- [ ] ✱ Stretch: Work out what the same budget buys when the four queries are asked every month

### Session 4: Synthetic data and leakage

#### [day2#s4] Synthetic data and leakage

*Session 4*

- Generate a synthetic extract by sequential modelling
- Measure its utility against the real table
- Test it for record copying and membership inference

#### [day2#synthetic-idea] A synthetic extract keeps the patterns and replaces the people

*A different kind of release*

- Fit a model of the table, then **sample new rows** from it
- Useful where the analyst needs rows: a hackathon, teaching, testing a pipeline
- No row is a real person, **if** the model did not memorise them
- That "if" is tested, every time, before release

- **No guarantee by default.** An ordinary generator gives no formal privacy guarantee. A generator trained with differential privacy does, at a cost in utility.

#### [day2#sequential-cart] Each column is drawn from a tree fitted on the columns before it

*How the lab's generator works*

1. **1 · age** drawn from observed ages
2. **2 · gender** tree on age
3. **3 · ...** tree on all earlier columns
4. **4 · decision** value taken from a training row in the same leaf

> **What goes wrong.** If a leaf may hold a single training row, the "donor" is always that row: the synthetic row becomes a copy of a real person.

#### [day2#utility-measures] Measure utility on the shares and on a model trained on synthetic rows

*Is the file useful?*

- **Marginal distance.** Total variation distance between real and synthetic shares of each categorical column, averaged. 0 is identical.
- **Train synthetic, test real.** A model predicting the officer's decision, trained on synthetic rows and scored on real rows it never saw. Compare with the same model trained on real rows: AUC 0.936.

#### [day2#leakage-measures] Compare distances to the training rows with distances to unseen rows

*Does the file leak?*

- **Exact copies.** Synthetic rows identical to a training row, against the same share for holdout rows.
- **Distance to closest record.** Share of synthetic rows closer to the training set than to the holdout. 50% means no preference.
- **Membership inference.** Score each real record by its nearest synthetic row. AUC 0.5 means the attacker cannot tell members.

#### [day2#synthetic-results] The most useful file is the one that copies people

*Lab 2.4, the reference run*

| Setting | Marginal distance | AUC, synthetic-trained | Copies of training rows | Copies of holdout rows | Membership AUC |
| --- | --- | --- | --- | --- | --- |
| leaf = 1 | 0.006 | 0.935 | 92.8% | 0.08% | 0.819 |
| leaf = 200 | 0.006 | 0.933 | 0.10% | 0.05% | 0.511 |

> **Utility alone would pick the wrong file.** Both look equally useful; one of them is 93% real people.

#### [day2#release-recommendation] Release the leaf = 200 file for the hackathon, under stated limits

*The recommendation*

- **Passes**: copies near baseline, membership AUC 0.511, utility within 0.003 AUC
- **Limits**: for prototypes, not for statistics about small groups
- **Not a guarantee**: one attack was tested; the report says so
- **Rejected**: leaf = 1, which copies 92.8% of rows

- **LO4 evidence.** The utility and leakage report that Lab 2.4 saves, with this recommendation and its limits.

#### [day2#check-synthetic] Which result should block the release?

*Checkpoint*

**Question:** A vendor's synthetic file matches the real one on utility. No row is an exact copy, and 31% of its rows are closer to the training data than to a holdout. What do you conclude?

- A. Nothing blocks it on these tests: no copies, and no preference for training rows
- B. It leaks: 31% of rows sit next to training records
- C. It is too accurate to be private, so it must be copying
- D. It is differentially private, since no row is copied

#### [day2#lab-2-4] Test a synthetic extract

Lab 2.4 · 25 min

Generate a synthetic extract and test it with distance-to-closest-record and membership-inference checks.

[D2_4_generate_synthetic_extract.ipynb](https://sdaiaacademy.github.io/ds-309/labs/D2_4_generate_synthetic_extract.ipynb)

- [ ] Fit the generator at two settings (6 min)
- [ ] Utility: marginals and a model trained on synthetic rows (6 min)
- [ ] Distance to the closest record (6 min)
- [ ] Membership inference (4 min)
- [ ] Release recommendation (3 min)
- [ ] ✱ Stretch: Plant one rare combination and see whether the generator reproduces it

#### [day2#wrap-up] Every control has a guarantee, a cost and a test

*Day 2 · Three things to keep*

- **k-anonymity.** k of five on the chosen fields; 293 records suppressed, mostly from small groups; no guarantee beyond those fields.
- **Differential privacy.** A guarantee whatever the attacker knows; error near one over epsilon; a budget that adds up.
- **Synthetic data.** Rows without people only if tested: copies, distance and membership against a holdout.

#### [day2#next] Audit for fairness

*Tomorrow · Day 3*

- Ahliya's errors by gender, region and nationality, with intervals, and one intersection
- Two fairness criteria that cannot both hold, and how to choose
- Five findings mapped to the national bias guide, then two mitigations and their cost
- Before tomorrow: recall how a Wilson interval for a proportion is computed (DS-204)
