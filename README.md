<!-- academy:title -->
# Responsible Data Science: Privacy, Fairness and Documentation

علم البيانات المسؤول: الخصوصية والإنصاف والتوثيق

Data Science Track · SDAIA Academy · DS-309 · Level 300

Measure and reduce re-identification risk, release counts under a privacy budget, test synthetic data for leakage, audit a screening model for subgroup errors, and document a release so that someone else can rerun it

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
| Capstone | Capstone: the release pack |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**Yusr Housing Support Fund** (صندوق يُسر لدعم السكن) is a fictional public fund that screens applications for housing support with an eligibility screening model, **Ahliya**. A university researcher asks for an extract, the board wants district counts and a synthetic file for a hackathon, and internal audit wants the model audited. All data is synthetic and generated with a fixed seed by `labs/prepare_data.py`: 60,000 applications with identifiers, free-text notes and decisions; a public register that shares three fields with them; and 12,000 applications that Ahliya scored and a full review settled.

Problems are planted in the data and each is found by a named lab: identifiers typed into case notes, quasi-identifiers that make almost every applicant unique, tiny district counts, self-employed income recorded too high, an old family-home rule in the officers' decisions, one office declining eligible women, income missing most often for non-Saudi women, a validation on the wrong labels, and auto-declines that never get a label. The trainer's key is `labs/solutions/answer_key.md`.

The people: Bashayer Al-Otaibi (director of eligibility and support, who owns the decisions), Yahya Al-Qahtani (data protection officer), Anmar Al-Ghamdi (who built Ahliya), Waad Al-Shehri (the researcher), Wiam Al-Mutairi (internal audit, the human reviewer of high risks) and Malak Al-Harbi (the data scientist, the role participants play).

## How the course is organised

- **One release, followed from request to review.** Day 1 finds the personal data and measures the risk; Day 2 treats it three ways (k-anonymity, differential privacy, synthetic data) and measures what each costs; Day 3 audits Ahliya by group; Day 4 writes the datasheet, model card and impact assessment, and reruns a peer's result.
- **Every lab starts from a supplied reference state**: the data files and, in `labs/data/reference/`, the results earlier labs would have produced. No lab depends on a participant's earlier run, and every exercise has a safety net.
- **Pre-work and follow-up.** Before Day 1: run `labs/00_setup_check.ipynb` and revise error rates and confidence intervals for proportions from DS-204. After the course: take one release or model at your workplace through the impact assessment and send the scored register, never the data.
- **AI policy.** AI off for the supervised check and for Lab 1.1. In the other labs an assistant may explain methods and errors without producing the audit. In the capstone any use of AI is allowed and defended live.
- **Responsible use.** All data is synthetic. Privacy, classification, secondary use, bias, transparency and accountability each have their own lab, and the impact assessment names a human reviewer for every risk scored high.
- **No model is called over an API and none is downloaded.** Every lab runs on a laptop CPU or in Google Colab.

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | Tag the applicant fields (AI-off) | [`D1_1_tag_each_applicant.ipynb`](labs/D1_1_tag_each_applicant.ipynb) |
| 1.2 | Day 1 · Session 2 | Classify three extracts | [`D1_2_assign_classification_levels.ipynb`](labs/D1_2_assign_classification_levels.ipynb) |
| 1.3 | Day 1 · Session 3 | Link the release to the register | [`D1_3_re_identify_applicants.ipynb`](labs/D1_3_re_identify_applicants.ipynb) |
| 1.4 | Day 1 · Session 4 | Uniqueness and k for three releases | [`D1_4_compute_unique_quasi.ipynb`](labs/D1_4_compute_unique_quasi.ipynb) |
| 2.1 | Day 2 · Session 1 | Reach k of five | [`D2_1_reach_k_least.ipynb`](labs/D2_1_reach_k_least.ipynb) |
| 2.2 | Day 2 · Session 2 | District counts at three budgets | [`D2_2_release_district_counts.ipynb`](labs/D2_2_release_district_counts.ipynb) |
| 2.3 | Day 2 · Session 3 | Split one budget over four queries | [`D2_3_split_one_budget.ipynb`](labs/D2_3_split_one_budget.ipynb) |
| 2.4 | Day 2 · Session 4 | Test a synthetic extract | [`D2_4_generate_synthetic_extract.ipynb`](labs/D2_4_generate_synthetic_extract.ipynb) |
| 3.1 | Day 3 · Session 1 | Error rates with intervals | [`D3_1_compute_error_rates.ipynb`](labs/D3_1_compute_error_rates.ipynb) |
| 3.2 | Day 3 · Session 2 | Two criteria in conflict | [`D3_2_show_two_fairness.ipynb`](labs/D3_2_show_two_fairness.ipynb) |
| 3.3 | Day 3 · Session 3 | Five findings, five types | [`D3_3_map_five_findings.ipynb`](labs/D3_3_map_five_findings.ipynb) |
| 3.4 | Day 3 · Session 4 | Reweighting and a threshold change | [`D3_4_apply_reweighting_threshold.ipynb`](labs/D3_4_apply_reweighting_threshold.ipynb) |
| 4.1 | Day 4 · Session 1 | The datasheet of the release | [`D4_1_write_datasheet_de.ipynb`](labs/D4_1_write_datasheet_de.ipynb) |
| 4.2 | Day 4 · Session 2 | The model card of Ahliya | [`D4_2_write_model_card.ipynb`](labs/D4_2_write_model_card.ipynb) |
| 4.3 | Day 4 · Session 3 | Score four risks | [`D4_3_score_four_risks.ipynb`](labs/D4_3_score_four_risks.ipynb) |
| 4.4 | Day 4 · Session 4 | Rerun a peer's result | [`D4_4_rerun_one_result.ipynb`](labs/D4_4_rerun_one_result.ipynb) |
<!-- /academy:labs -->

## Capstone

A release pack for a second synthetic case (a scholarship allocation model): treated extract, fairness audit, datasheet, model card and impact assessment, in a public repository whose README reports measured risk, utility and disparities, defended in a ten-minute review

**Submission:** A link to a public GitHub repository holding the release pack for the Sabeel Scholarship Fund case: the treated extract with its release log, the fairness audit with disaggregated error rates and intervals, the datasheet, the model card and the impact assessment, with a README that reports the measured risk, utility and disparities and how to rerun them. The commit history is part of the evidence.

The case brief and its synthetic data are in [`labs/capstone/`](labs/capstone/README.md): **Sabeel Scholarship Fund** (صندوق سبيل للمنح الدراسية) and its screening model **Tarjih**, with 24,000 applications, a public list of award holders and 6,000 scored and reviewed applications. The review is ten minutes, questions included: the assessor picks a slice of the scored applications and the participant recomputes one disparity live from the repository.

| Criterion | Weight |
|---|---|
| Privacy | 25 |
| Fairness audit | 25 |
| Documentation | 20 |
| Impact assessment | 20 |
| Reproducibility | 10 |

## Prerequisites

- DS-204 Machine Learning for Tabular Data: Baselines and Validation
- DS-207 Responsible Data Practice and Conduct in Analytical Work
- Trains and evaluates a classifier in Python
- Computes error rates and confidence intervals for proportions
- Setup: a laptop CPU with uv, or Google Colab. No lab calls or downloads a model. See [`labs/README.md`](labs/README.md).

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

### National references

- [Personal Data Protection Law (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/PersonalDataProtectionLaw.pdf)
- [Implementing Regulation of the Personal Data Protection Law (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf)
- [Personal Data Destruction, Anonymization and Pseudonymisation Guideline, version 1.0 (SDAIA, August 2024)](https://sdaia.gov.sa/Documents/PersonalDataDestructionAnonymizationAndEncryptionGuideline.pdf)
- [Data Classification Policy (National Data Management Office, SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/DataClassificationPolicy.pdf)
- [General Rules for Secondary Use of Data (SDAIA)](https://sdaia.gov.sa/Documents/GeneralRulesForSecondaryUseOfData_EN.pdf)
- [AI Ethics Principles, with Annexure A (AI ethics tools) and Annexure B (tools by lifecycle stage) (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/ai-principles.pdf)
- [AI Bias Reference Guide, first edition (SDAIA, May 2026)](https://sdaia.gov.sa/en/MediaCenter/KnowledgeCenter/ResearchLibrary/EN-AI-BIAS.pdf)
- [National AI Risk Management Framework, full text in Arabic (SDAIA, April 2026)](https://sdaia.gov.sa/ar/MediaCenter/KnowledgeCenter/ResearchLibrary/ExecutiveSummaryAr.pdf)
- [National AI Risk Management Framework, English executive summary (SDAIA, April 2026)](https://sdaia.gov.sa/en/MediaCenter/KnowledgeCenter/ResearchLibrary/ExecutiveSummaryEn.pdf)

### Methods

- [Sweeney, Simple Demographics Often Identify People Uniquely (Carnegie Mellon University, 2000)](https://dataprivacylab.org/projects/identifiability/paper1.pdf)
- [Dwork and Roth, The Algorithmic Foundations of Differential Privacy](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf)
- [Nowok, Raab and Dibben, synthpop: Bespoke Creation of Synthetic Data in R (Journal of Statistical Software, 2016)](https://www.jstatsoft.org/article/view/v074i11)
- [Kleinberg, Mullainathan and Raghavan, Inherent Trade-Offs in the Fair Determination of Risk Scores](https://arxiv.org/abs/1609.05807)
- [Kamiran and Calders, Data preprocessing techniques for classification without discrimination (Knowledge and Information Systems, 2012)](https://link.springer.com/article/10.1007/s10115-011-0463-8)
- [Hardt, Price and Srebro, Equality of Opportunity in Supervised Learning](https://arxiv.org/abs/1610.02413)
- [Gebru and others, Datasheets for Datasets](https://arxiv.org/abs/1803.09010)
- [Mitchell and others, Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993)

### Tools

- [OpenDP library documentation](https://docs.opendp.org/)
- [Fairlearn documentation](https://fairlearn.org/)
- [ARX data anonymization tool](https://arx.deidentifier.org/)
- [sdcMicro on CRAN](https://cran.r-project.org/package=sdcMicro)
- [synthpop on CRAN](https://cran.r-project.org/package=synthpop)
- [Synthetic Data Vault documentation](https://docs.sdv.dev/sdv)
- [AI Fairness 360](https://github.com/Trusted-AI/AIF360)
- [Aequitas](https://github.com/dssg/aequitas)
- [uv documentation](https://docs.astral.sh/uv/)
<!-- /academy:sources -->

### National references

- Personal Data Protection Law: https://sdaia.gov.sa/en/SDAIA/about/Documents/PersonalDataProtectionLaw.pdf, and its implementing regulation: https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf
- Personal Data Destruction, Anonymization and Pseudonymisation Guideline: https://sdaia.gov.sa/Documents/PersonalDataDestructionAnonymizationAndEncryptionGuideline.pdf
- NDMO Data Classification Policy: https://sdaia.gov.sa/en/SDAIA/about/Documents/DataClassificationPolicy.pdf
- General Rules for Secondary Use of Data: https://sdaia.gov.sa/Documents/GeneralRulesForSecondaryUseOfData_EN.pdf
- SDAIA AI Ethics Principles and their annexes of tools: https://sdaia.gov.sa/en/SDAIA/about/Documents/ai-principles.pdf
- SDAIA AI Bias Reference Guide: https://sdaia.gov.sa/en/MediaCenter/KnowledgeCenter/ResearchLibrary/EN-AI-BIAS.pdf
- National AI Risk Management Framework: https://sdaia.gov.sa/ar/MediaCenter/KnowledgeCenter/ResearchLibrary/ExecutiveSummaryAr.pdf (full text, Arabic), with an English executive summary: https://sdaia.gov.sa/en/MediaCenter/KnowledgeCenter/ResearchLibrary/ExecutiveSummaryEn.pdf
