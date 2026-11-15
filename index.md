---
course: "Responsible Data Science: Privacy, Fairness and Documentation"
code: "DS-309"
version: "2027.1.0"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-309/index.html"
---

# Responsible Data Science: Privacy, Fairness and Documentation

علم البيانات المسؤول: الخصوصية والإنصاف والتوثيق

Data Science Track · 4 teaching days + capstone day · 26 hours · Level 300

Measure and reduce re-identification risk, release counts under a privacy budget, test synthetic data for leakage, audit a screening model for subgroup errors, and document a release so that someone else can rerun it

Participants take the synthetic applicant data and eligibility-screening model of Yusr Housing Support Fund, a fictional public fund, through the checks a release needs: they measure re-identification risk and de-identify the table, publish differentially private counts under a budget, test a synthetic extract for leakage, audit subgroup errors against the bias types in SDAIA's AI Bias Reference Guide, and write the datasheet, model card and impact assessment a reviewer needs. Calibration and explanation are DS-305.

**Who it is for:** Practitioners. Data scientists and analysts who have completed the level 200 set or can show equivalent work: an analysis they framed, carried out and explained to a stakeholder.

**Format:** Intensive: 4 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

## The case study

**Yusr Housing Support Fund.** Yusr Housing Support Fund is a fictional public fund that screens applications for housing support with an eligibility screening model, Ahliya. A researcher asks for an extract, the fund wants to publish district counts and a synthetic extract, and internal audit wants the model audited: participants take 60,000 synthetic applicant records, a linkable public register and 12,000 scored and reviewed applications through every check a release needs. All data is synthetic, generated with a fixed seed, and planted with the problems the labs find.

## The course

### Day 1: Find the personal data

Slides: https://sdaiaacademy.github.io/ds-309/slides/day1.md

- **Session 1: Personal data in an analysis**
  - Tell direct identifiers, quasi-identifiers and sensitive attributes apart in a real table
  - Find identifiers hiding in free-text fields
  - Decide keep, drop or transform for each field against a stated purpose
  - [Lab 1.1: Tag the applicant fields (AI-off) (25 min)](https://sdaiaacademy.github.io/ds-309/labs/D1_1_tag_each_applicant.ipynb)
- **Session 2: Classification and permitted use**
  - Assign a national classification level to an extract from its impact
  - State when an extract may leave the fund under the secondary use rules
  - Match five release controls to their guarantee and their cost
  - [Lab 1.2: Classify three extracts (25 min)](https://sdaiaacademy.github.io/ds-309/labs/D1_2_assign_classification_levels.ipynb)
- **Session 3: Linkage attacks**
  - Explain how a linkage attack joins a release to an outside file
  - Run a linkage on quasi-identifiers and measure its success
  - Name what a successful link discloses
  - [Lab 1.3: Link the release to the register (25 min)](https://sdaiaacademy.github.io/ds-309/labs/D1_3_re_identify_applicants.ipynb)
- **Session 4: Measuring disclosure risk**
  - Compute equivalence classes, uniqueness and k for a release
  - Compare candidate releases by record-level risk
  - Explain why k alone misses attribute disclosure
  - [Lab 1.4: Uniqueness and k for three releases (25 min)](https://sdaiaacademy.github.io/ds-309/labs/D1_4_compute_unique_quasi.ipynb)

### Day 2: Release with less risk

Slides: https://sdaiaacademy.github.io/ds-309/slides/day2.md

- **Session 1: Generalisation and suppression**
  - Generalise quasi-identifiers along a hierarchy
  - Suppress the records that stay below k
  - Measure the utility cost on key statistics
  - [Lab 2.1: Reach k of five (25 min)](https://sdaiaacademy.github.io/ds-309/labs/D2_1_reach_k_least.ipynb)
- **Session 2: Differential privacy for counts**
  - State what the differential privacy promise covers and what it does not
  - Add calibrated noise to counts with a library
  - Measure the error that a budget costs
  - [Lab 2.2: District counts at three budgets (25 min)](https://sdaiaacademy.github.io/ds-309/labs/D2_2_release_district_counts.ipynb)
- **Session 3: Budgets and composition**
  - Add up privacy loss under sequential and parallel composition
  - Release a bounded mean with a library
  - Allocate one budget across queries by need
  - [Lab 2.3: Split one budget over four queries (25 min)](https://sdaiaacademy.github.io/ds-309/labs/D2_3_split_one_budget.ipynb)
- **Session 4: Synthetic data and leakage**
  - Generate a synthetic extract by sequential modelling
  - Measure its utility against the real table
  - Test it for record copying and membership inference
  - [Lab 2.4: Test a synthetic extract (25 min)](https://sdaiaacademy.github.io/ds-309/labs/D2_4_generate_synthetic_extract.ipynb)

### Day 3: Audit for fairness

Slides: https://sdaiaacademy.github.io/ds-309/slides/day3.md

- **Session 1: Disaggregating errors**
  - Compute false negative and false positive rates by group with intervals
  - Slice by an intersection of two attributes
  - Report a small group without overclaiming
  - [Lab 3.1: Error rates with intervals (25 min)](https://sdaiaacademy.github.io/ds-309/labs/D3_1_compute_error_rates.ipynb)
- **Session 2: Criteria that conflict**
  - Compute demographic parity, equal opportunity and predictive parity gaps
  - Show why they cannot all hold when base rates differ
  - Choose a criterion from the harm of each kind of error
  - [Lab 3.2: Two criteria in conflict (25 min)](https://sdaiaacademy.github.io/ds-309/labs/D3_2_show_two_fairness.ipynb)
- **Session 3: Bias across the lifecycle**
  - Place a finding in a stage of the AI system lifecycle
  - Name its bias type from the national bias guide
  - Run the check that separates two neighbouring types
  - [Lab 3.3: Five findings, five types (25 min)](https://sdaiaacademy.github.io/ds-309/labs/D3_3_map_five_findings.ipynb)
- **Session 4: Mitigation and its cost**
  - Apply reweighting before training
  - Apply group thresholds after training
  - Compare accuracy and disparity, and recommend
  - [Lab 3.4: Reweighting and a threshold change (25 min)](https://sdaiaacademy.github.io/ds-309/labs/D3_4_apply_reweighting_threshold.ipynb)

### Day 4: Document and assess

Slides: https://sdaiaacademy.github.io/ds-309/slides/day4.md

- **Session 1: Datasheets**
  - List what a datasheet of a de-identified release must answer
  - Fill each answer from a log, not from memory
  - Test a datasheet for completeness
  - [Lab 4.1: The datasheet of the release (25 min)](https://sdaiaacademy.github.io/ds-309/labs/D4_1_write_datasheet_de.ipynb)
- **Session 2: Model cards**
  - Write the intended and out-of-scope uses of a model
  - Report disaggregated results with intervals
  - State the fairness criterion and what it costs
  - [Lab 4.2: The model card of Ahliya (25 min)](https://sdaiaacademy.github.io/ds-309/labs/D4_2_write_model_card.ipynb)
- **Session 3: Impact assessment**
  - Score a risk's likelihood and impact on the national framework's scales
  - Choose a treatment and score the residual risk
  - Name a human reviewer for every high risk
  - [Lab 4.3: Score four risks (25 min)](https://sdaiaacademy.github.io/ds-309/labs/D4_3_score_four_risks.ipynb)
- **Session 4: Review by someone else**
  - Rerun a colleague's result from their notebook and data
  - Find the undocumented choices that change a number
  - Record documentation gaps that a reviewer can act on
  - [Lab 4.4: Rerun a peer's result (25 min)](https://sdaiaacademy.github.io/ds-309/labs/D4_4_rerun_one_result.ipynb)

### Capstone: Capstone: the release pack

Slides: https://sdaiaacademy.github.io/ds-309/slides/capstone.md

## Capstone

A release pack for a second synthetic case (a scholarship allocation model): treated extract, fairness audit, datasheet, model card and impact assessment, in a public repository whose README reports measured risk, utility and disparities, defended in a ten-minute review

**What you submit:** A link to a public GitHub repository holding the release pack for the Sabeel Scholarship Fund case: the treated extract with its release log, the fairness audit with disaggregated error rates and intervals, the datasheet, the model card and the impact assessment, with a README that reports the measured risk, utility and disparities and how to rerun them. The commit history is part of the evidence. Then a ten-minute review in which the assessor picks a slice and the participant recomputes one disparity live.

**Rubric:**

- Privacy: 25%
- Fairness audit: 25%
- Documentation: 20%
- Impact assessment: 20%
- Reproducibility: 10%

## Outcomes

- **LO1** Distinguish pseudonymisation, de-identification, aggregation, synthetic data and differential privacy by the guarantee and cost of each, given five described data releases (Awareness) Evidence: a decision table naming the fitting control and the residual risk for each
- **LO2** Measure re-identification risk from quasi-identifiers and reduce it while tracking analytic utility, given 60,000 synthetic applicant records and a linkable external file (Applied) Evidence: unique records, linkage success and three key statistics before and after treatment
- **LO3** Compute differentially private counts and means and state the accuracy cost of a privacy budget, given three candidate budgets (Applied) Evidence: error-against-budget curves and a recommended setting
- **LO4** Test a synthetic extract for analytic utility and membership-inference leakage, given a generator trained on the applicant table (Applied) Evidence: a utility and leakage report with a release recommendation
- **LO5** Audit a screening model for subgroup disparities, choose fairness criteria that fit the decision and evaluate two mitigations, given a scored test set with protected and intersectional attributes (Performance) Evidence: an audit report with disaggregated error rates, intervals and a recommendation
- **LO6** Build the datasheet, model card and impact assessment a reviewer needs to judge and rerun a release, given the participant's capstone release (Performance) Evidence: a pack that a peer reruns and challenges, with a likelihood and impact score for each risk

## Tools

- **De-identification and disclosure risk:** ARX, sdcMicro
- **Differential privacy library:** OpenDP, diffprivlib
- **Synthetic tabular data:** Synthetic Data Vault, synthpop
- **Fairness metrics and mitigation:** Fairlearn, AIF360, Aequitas
- **Notebooks with pinned environments:** Jupyter or marimo with uv, R with Quarto and renv

## Prerequisites

- DS-204 Machine Learning for Tabular Data: Baselines and Validation
- DS-207 Responsible Data Practice and Conduct in Analytical Work
- Trains and evaluates a classifier in Python
- Computes error rates and confidence intervals for proportions
- Setup: a laptop CPU with uv, or Google Colab. No lab calls or downloads a model. See labs/README.md.

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

---

SDAIA Academy · Data Science Track · Responsible Data Science: Privacy, Fairness and Documentation

Course version 2027.1.0 · engine 1.0.0 · built 2026-11-15 · commit 8cfd447
