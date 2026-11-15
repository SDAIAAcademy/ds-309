<!-- academy:title -->
# Responsible Data Science: Privacy, Fairness and Documentation

علم البيانات المسؤول: الخصوصية والإنصاف والتوثيق

Data Science Track · SDAIA Academy · DS-309 · Level 300

REPLACE: one line under the title: what participants can do after the course

Participants take the synthetic applicant data and eligibility-screening model of Yusr Housing Support Fund, a fictional public fund, through the checks a release needs: they measure re-identification risk and de-identify the table, publish differentially private counts under a budget, test a synthetic extract for leakage, audit subgroup errors against the bias types in SDAIA's AI Bias Reference Guide, and write the datasheet, model card and impact assessment a reviewer needs. Calibration and explanation are DS-305.

**Format:** Intensive: 4 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

**Course page:** https://sdaiaacademy.github.io/ds-309/
<!-- /academy:title -->

## Outcomes

| | Outcomes | Level | Evidence |
|---|---|---|---|
| LO1 | Distinguish pseudonymisation, de-identification, aggregation, synthetic data and differential privacy by the guarantee and cost of each, given five described data releases | Awareness | a decision table naming the fitting control and the residual risk for each |
| LO2 | Measure re-identification risk from quasi-identifiers and reduce it while tracking analytic utility, given 60,000 synthetic applicant records and a linkable external file | Applied | unique records, linkage success and three key statistics before and after treatment |
| LO3 | Compute differentially private counts and means and state the accuracy cost of a privacy budget, given three candidate budgets | Applied | error-against-budget curves and a recommended setting |
| LO4 | Test a synthetic extract for analytic utility and membership-inference leakage, given a generator trained on the applicant table | Applied | a utility and leakage report with a release recommendation |
| LO5 | Audit a screening model for subgroup disparities, choose fairness criteria that fit the decision and evaluate two mitigations, given a scored test set with protected and intersectional attributes | Performance | an audit report with disaggregated error rates, intervals and a recommendation |
| LO6 | Build the datasheet, model card and impact assessment a reviewer needs to judge and rerun a release, given the participant's capstone release | Performance | a pack that a peer reruns and challenges, with a likelihood and impact score for each risk |

<!-- academy:units -->
## Units

| Unit | Title | Sessions | Slides |
|---|---|---|---|
| Day 1 | Find the personal data | Personal data in an analysis; Classification and permitted use; Linkage attacks; Measuring disclosure risk | [`slides/day1.html`](slides/day1.html) |
| Day 2 | Release with less risk | Generalisation and suppression; Differential privacy for counts; Budgets and composition; Synthetic data and leakage | [`slides/day2.html`](slides/day2.html) |
| Day 3 | Audit for fairness | Disaggregating errors; Criteria that conflict; Bias across the lifecycle; Mitigation and its cost | [`slides/day3.html`](slides/day3.html) |
| Day 4 | Document and assess | Datasheets; Model cards; Impact assessment; Review by someone else | [`slides/day4.html`](slides/day4.html) |
| Capstone | Capstone project presentations |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**REPLACE: the name of the fictional organisation every lab works on.** REPLACE: two sentences on the case study and its synthetic data

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | Tag each applicant field by identifiability and decide what to drop (AI-off) | [`D1_1_tag_each_applicant.ipynb`](labs/D1_1_tag_each_applicant.ipynb) |
| 1.2 | Day 1 · Session 2 | Assign classification levels to three extracts and decide which may leave the fund | [`D1_2_assign_classification_levels.ipynb`](labs/D1_2_assign_classification_levels.ipynb) |
| 1.3 | Day 1 · Session 3 | Re-identify applicants by linking a release to a synthetic public register | [`D1_3_re_identify_applicants.ipynb`](labs/D1_3_re_identify_applicants.ipynb) |
| 1.4 | Day 1 · Session 4 | Compute unique quasi-identifier combinations and k for three candidate releases | [`D1_4_compute_unique_quasi.ipynb`](labs/D1_4_compute_unique_quasi.ipynb) |
| 2.1 | Day 2 · Session 1 | Reach k of at least five and measure the change in three key statistics | [`D2_1_reach_k_least.ipynb`](labs/D2_1_reach_k_least.ipynb) |
| 2.2 | Day 2 · Session 2 | Release district counts at three budgets and plot the error | [`D2_2_release_district_counts.ipynb`](labs/D2_2_release_district_counts.ipynb) |
| 2.3 | Day 2 · Session 3 | Split one budget across four queries and justify the allocation | [`D2_3_split_one_budget.ipynb`](labs/D2_3_split_one_budget.ipynb) |
| 2.4 | Day 2 · Session 4 | Generate a synthetic extract and test it with distance-to-closest-record and membership-inference checks | [`D2_4_generate_synthetic_extract.ipynb`](labs/D2_4_generate_synthetic_extract.ipynb) |
| 3.1 | Day 3 · Session 1 | Compute error rates by gender, region and nationality with intervals | [`D3_1_compute_error_rates.ipynb`](labs/D3_1_compute_error_rates.ipynb) |
| 3.2 | Day 3 · Session 2 | Show two fairness criteria conflicting on the test set and choose one | [`D3_2_show_two_fairness.ipynb`](labs/D3_2_show_two_fairness.ipynb) |
| 3.3 | Day 3 · Session 3 | Map five findings to bias types in the national guide | [`D3_3_map_five_findings.ipynb`](labs/D3_3_map_five_findings.ipynb) |
| 3.4 | Day 3 · Session 4 | Apply reweighting and a threshold change and compare accuracy and disparity | [`D3_4_apply_reweighting_threshold.ipynb`](labs/D3_4_apply_reweighting_threshold.ipynb) |
| 4.1 | Day 4 · Session 1 | Write the datasheet for the de-identified release | [`D4_1_write_datasheet_de.ipynb`](labs/D4_1_write_datasheet_de.ipynb) |
| 4.2 | Day 4 · Session 2 | Write a model card with disaggregated results and intended use | [`D4_2_write_model_card.ipynb`](labs/D4_2_write_model_card.ipynb) |
| 4.3 | Day 4 · Session 3 | Score four risks on the national framework's likelihood and impact matrix and propose treatments | [`D4_3_score_four_risks.ipynb`](labs/D4_3_score_four_risks.ipynb) |
| 4.4 | Day 4 · Session 4 | Rerun one result from a peer's day 2 or day 3 notebook and record the documentation gaps | [`D4_4_rerun_one_result.ipynb`](labs/D4_4_rerun_one_result.ipynb) |
<!-- /academy:labs -->

## Capstone

A release pack for a second synthetic case (a scholarship allocation model): treated extract, fairness audit, datasheet, model card and impact assessment, in a public repository whose README reports measured risk, utility and disparities, defended in a ten-minute review

**Submission:** REPLACE: what participants submit and how: a public repository link, or a shared folder for a course without code

## Prerequisites

- DS-204 Machine Learning for Tabular Data: Baselines and Validation
- DS-207 Responsible Data Practice and Conduct in Analytical Work
- Trains and evaluates a classifier in Python
- Computes error rates and confidence intervals for proportions

<!-- academy:tools -->
## Tools

Each line is a capability; the examples are interchangeable.

- **De-identification and disclosure risk:** ARX, sdcMicro
- **Differential privacy library:** OpenDP, diffprivlib
- **Synthetic tabular data:** Synthetic Data Vault, synthpop
- **Fairness metrics and mitigation:** Fairlearn, AIF360, Aequitas
- **Notebooks with pinned environments:** Jupyter or marimo with uv, R with Quarto and renv
<!-- /academy:tools -->

<!-- academy:sources -->
## Sources

- REPLACE: every source the course cites, with its address, in course.json under "sources"; this list is written from there
<!-- /academy:sources -->

### National references

- Personal Data Protection Law and its implementing regulations: REPLACE: the address of the official text
- PDPL guideline on destruction, anonymisation and pseudonymisation of personal data: REPLACE: the address of the official text
- NDMO Data Classification Policy: REPLACE: the address of the official text
- General Rules for Secondary Use of Data: REPLACE: the address of the official text
- SDAIA AI Ethics Principles and their fairness tools annex: REPLACE: the address of the official text
- SDAIA AI Bias Reference Guide: REPLACE: the address of the official text
- National AI Risk Management Framework: REPLACE: the address of the official text
