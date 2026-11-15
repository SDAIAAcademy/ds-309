---
course: "Responsible Data Science: Privacy, Fairness and Documentation"
code: "DS-309"
version: "2027.1.0"
scope: "course"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-309/"
---

# Responsible Data Science: Privacy, Fairness and Documentation

Measure and reduce re-identification risk, release counts under a privacy budget, test synthetic data for leakage, audit a screening model for subgroup errors, and document a release so that someone else can rerun it

Participants take the synthetic applicant data and eligibility-screening model of Yusr Housing Support Fund, a fictional public fund, through the checks a release needs: they measure re-identification risk and de-identify the table, publish differentially private counts under a budget, test a synthetic extract for leakage, audit subgroup errors against the bias types in SDAIA's AI Bias Reference Guide, and write the datasheet, model card and impact assessment a reviewer needs. Calibration and explanation are DS-305.

- **Audience:** Practitioners. Data scientists and analysts who have completed the level 200 set or can show equivalent work: an analysis they framed, carried out and explained to a stakeholder.
- **Prerequisites:** DS-204 Machine Learning for Tabular Data: Baselines and Validation; DS-207 Responsible Data Practice and Conduct in Analytical Work; Trains and evaluates a classifier in Python; Computes error rates and confidence intervals for proportions; Setup: a laptop CPU with uv, or Google Colab. No lab calls or downloads a model. See labs/README.md.
- **Case study:** Yusr Housing Support Fund: Yusr Housing Support Fund is a fictional public fund that screens applications for housing support with an eligibility screening model, Ahliya. A researcher asks for an extract, the fund wants to publish district counts and a synthetic extract, and internal audit wants the model audited: participants take 60,000 synthetic applicant records, a linkable public register and 12,000 scored and reviewed applications through every check a release needs. All data is synthetic, generated with a fixed seed, and planted with the problems the labs find.

## Outcomes

- LO1 (Awareness): Distinguish pseudonymisation, de-identification, aggregation, synthetic data and differential privacy by the guarantee and cost of each, given five described data releases
- LO2 (Applied): Measure re-identification risk from quasi-identifiers and reduce it while tracking analytic utility, given 60,000 synthetic applicant records and a linkable external file
- LO3 (Applied): Compute differentially private counts and means and state the accuracy cost of a privacy budget, given three candidate budgets
- LO4 (Applied): Test a synthetic extract for analytic utility and membership-inference leakage, given a generator trained on the applicant table
- LO5 (Performance): Audit a screening model for subgroup disparities, choose fairness criteria that fit the decision and evaluate two mitigations, given a scored test set with protected and intersectional attributes
- LO6 (Performance): Build the datasheet, model card and impact assessment a reviewer needs to judge and rerun a release, given the participant's capstone release

## Day 1: Find the personal data

Identifiers, classification, linkage and disclosure risk

#### [day1#title] Find the personal data

*SDAIA Academy · Responsible Data Science: Privacy, Fairness and Documentation*

Day 1: Identifiers, classification, linkage and disclosure risk

Data Science Track · 4 teaching days + capstone day · 4 sessions · 4 labs · DS-309

#### [day1#four-days-one-release] Four days take one release through every check it needs

*The course at a glance*

- **Day 1 · Find.** Identifiers, classification, linkage attacks, measured disclosure risk.
- **Day 2 · Reduce.** Generalisation, differential privacy, budgets, synthetic data and its leakage.
- **Day 3 · Audit.** Errors by group, criteria that conflict, bias types, two mitigations.
- **Day 4 · Document.** Datasheet, model card, impact assessment, a rerun by a peer.

> **Day 5 · Capstone.** A release pack for a second case, a scholarship allocation model, in a public repository, reviewed for ten minutes with one disparity recomputed live.

#### [day1#how-this-course-works] Every claim about risk or fairness ends in a measured number

*How this course works*

- **Measure, then decide.** Unique records, linkage success, error against budget, error rates with intervals. A control without a measurement is a hope.
- **Reference states.** Every lab starts from supplied files. Nothing depends on an earlier lab, and every exercise has a safety net.
- **Synthetic data only.** 60,000 invented applicants. Identifiers carry the marker `SYN`. No lab calls or downloads a model.

> **AI policy.** AI off for the supervised check and for Lab 1.1. In the other labs an assistant may explain a method or an error, but it does not produce the audit. In the capstone anything goes, and you defend it live.

#### [day1#yusr-case] Yusr Housing Support Fund and its screening model, Ahliya

*One case all week*

A fictional public fund that screens applications for housing support. Its model, **Ahliya** (أهلية), scores each application before an officer decides.

- **A researcher's request.** Waad Al-Shehri, a university researcher, asks for row-level data on household size, income and approval.
- **Two publications.** District counts for a public dashboard, and a synthetic extract for a hackathon.
- **An audit.** Internal audit asks whether Ahliya misses eligible applicants more often in some groups.

#### [day1#setup-check] Open the labs in Colab, or run them locally with uv

*Lab environment*

1. **Colab:** open a notebook from the course page. Its first cell clones the repository and installs two libraries.
2. **Locally:** the commands on the right. A laptop processor is enough; the slowest lab runs in about a minute.
3. Exercises raise an error until you fill them in. The cell after each one supplies a reference result, so the rest of the notebook still runs.

```bash
# file: terminal (local option)
git clone https://github.com/SDAIAAcademy/ds-309
cd ds-309/labs
uv sync
uv run jupyter lab
```

#### [day1#agenda] Find the personal data

*Today*

- **Session 1 · Personal data in an analysis**: Which applicant fields identify a person directly, which do it in combination, and which are sensitive
- **Session 2 · Classification and permitted use**: The national classification levels, the secondary use rules, and five release controls by guarantee and cost
- **Session 3 · Linkage attacks**: How a release with no names is joined to an outside file, and what a link discloses
- **Session 4 · Measuring disclosure risk**: Equivalence classes, uniqueness and k, and why k alone misses what a group reveals

### Session 1: Personal data in an analysis

#### [day1#s1] Personal data in an analysis

*Session 1*

- Tell direct identifiers, quasi-identifiers and sensitive attributes apart in a real table
- Find identifiers hiding in free-text fields
- Decide keep, drop or transform for each field against a stated purpose

#### [day1#pdpl-recap] The law asks for a purpose first, then only the data that purpose needs

*Recap from DS-207*

- **Purpose.** Data collected to decide support is used for that, or for a compatible purpose under the rules.
- **Minimisation.** Each field that leaves has a reason tied to the purpose. "Might be useful" is not one.
- **Secondary use.** Research use has its own rules: legitimate purpose, minimum necessary, an approved request.

> **This course goes further.** DS-207 decided whether a request is lawful. Here you measure how identifying the data still is after you cut it, and you reduce that risk with numbers to show for it.

#### [day1#three-kinds-of-field] Direct identifiers, quasi-identifiers and sensitive attributes

*Not every field identifies the same way*

| Kind | What it does | In the Yusr table |
| --- | --- | --- |
| **Direct identifier** | Points at one person by itself | national identifier, name, mobile, e-mail, the fund's applicant number |
| **Quasi-identifier** | Points at one person in combination, and someone outside could know it | birth date, gender, postcode, district, nationality, household size |
| **Sensitive attribute** | What an attacker wants to learn | income, social security, disability in the household, the fund's decision |
| **Free text** | Can hold any of the above | the officers' case notes |

#### [day1#quasi-test] Ask who outside the fund could already know the value

*How to tell a quasi-identifier*

- A **neighbour** knows the postcode and roughly the household size
- An **employer** knows the sector and the birth date
- A **public list** may hold name, birth date, gender and postcode together
- If an outsider can know it, an outsider can **join on it**

- **Three ordinary fields.** In 1990 United States census data, 87% of people were likely unique on five-digit ZIP code, gender and date of birth.

#### [day1#notes-hold-identifiers] Case notes hold identifiers that no column was meant to

*The field everyone forgets*

Prompt for case_note:

```text
Called back on 05-SYN-418203 about the lease.
```

Prompt for case_note:

```text
Spoke to Hind at the branch; brother handles the file.
```

Prompt for case_note:

```text
Duplicate file found under SYN5520147.
```

**2,470** of 60,000 notes hold a mobile, a national identifier or a first name (Lab 1.1)

> **What goes wrong.** A pipeline drops the identifier columns and keeps the note "for context". The extract now carries names and numbers in free text.

#### [day1#minimise-field-by-field] Decide each field against the question: keep, drop or transform

*Minimisation in practice*

| Field | Decision | Reason, for the question "household size, income and approval by region" |
| --- | --- | --- |
| birth date | transform | an age band answers the question |
| postcode, district | drop | region is the unit of the question |
| income | transform | bands of 1,000 riyals |
| applicant number | transform | a study code; the key stays with the data protection officer |
| case note | drop | free text holds identifiers |

In the reference solution 8 of 23 fields leave, kept or transformed.

#### [day1#pseudonym-still-personal] A pseudonymised extract is still personal data

*A code is not anonymity*

- **Pseudonymisation** replaces identifiers with codes; the key is kept apart
- Whoever holds the key can reverse it; the quasi-identifiers stay
- SDAIA's anonymisation guideline treats pseudonymised data as personal data and its protection as weaker than anonymisation
- **Anonymised** data must be irreversible, with the re-identification risk assessed

- **A hash is a code too.** Anyone with a list of national identifiers recomputes the same hashes and finds the rows (Lab 1.1 stretch).

#### [day1#check-hashed-id] Is the hashed extract still personal data?

*Checkpoint*

**Question:** Malak replaces each national identifier with its SHA-256 hash and removes names. Birth date, gender and postcode stay. Waad says the extract is now anonymous. What do you answer?

- A. Yes: a hash cannot be reversed, so nobody can find the person
- B. No: the hash is a pseudonym and the quasi-identifiers still single people out
- C. Yes, as long as it stays on the university's servers
- D. No, but only because names were in the original table

#### [day1#lab-1-1] Tag the applicant fields (AI-off)

Lab 1.1 · 25 min

Tag each applicant field by identifiability and decide what to drop (AI-off).

[D1_1_tag_each_applicant.ipynb](https://sdaiaacademy.github.io/ds-309/labs/D1_1_tag_each_applicant.ipynb)

- [ ] Load the table and list its fields (3 min)
- [ ] Tag each field by identifiability (8 min)
- [ ] Find identifiers in the case notes (6 min)
- [ ] Keep, drop or transform, with a reason (6 min)
- [ ] Count what the purpose still needs (2 min)
- [ ] ✱ Stretch: Hash the national identifier and decide whether the hash is still personal data

### Session 2: Classification and permitted use

#### [day1#s2] Classification and permitted use

*Session 2*

- Assign a national classification level to an extract from its impact
- State when an extract may leave the fund under the secondary use rules
- Match five release controls to their guarantee and their cost

#### [day1#four-levels] The level follows the impact of an unauthorised disclosure

*The national classification*

| Level | Impact | Typical content |
| --- | --- | --- |
| **Top Secret** | high | exceptionally serious, irreparable harm to national interests |
| **Secret** | medium | serious harm to national interests or major losses |
| **Restricted** | low | limited harm; the policy's examples include personally identifiable information such as names and identification numbers |
| **Public** | none | none of the impacts above |

Restricted splits by scale: **A** a whole sector, **B** several entities or a group of individuals, **C** one entity or one individual.

#### [day1#three-extracts] Three extracts, three levels, three answers to "may it leave?"

*On the fund's analysis server*

- **E1 · Applicant table.** 60,000 rows, 23 fields, names and identifiers. **Restricted B.** Stays inside the fund.
- **E2 · Research extract.** No names, a study code, birth date and postcode kept. **Restricted B.** Leaves only under conditions.
- **E3 · Counts.** Approved by district and nationality: 118 cells, the smallest is 2. **Restricted C** until treated.

#### [day1#secondary-use-conditions] A research extract leaves under conditions, not because names are gone

*When E2 may leave*

1. **1 · Request** through the researcher's university, with its written approval
2. **2 · Purpose** research or public interest, not profit
3. **3 · Minimum** only the fields the purpose needs
4. **4 · Measured** disclosure risk reduced, then shared under an agreement

#### [day1#five-controls] Five controls, each with a different guarantee and a different cost

*The controls a release can use*

| Control | What it guarantees | What it costs |
| --- | --- | --- |
| **Pseudonymisation** | nothing outside the key holder; still personal data | almost nothing |
| **De-identification** | each record hides among at least k on the chosen fields | detail, and rows suppressed |
| **Aggregation** | no row-level data | no row-level analysis; small cells still leak |
| **Synthetic data** | no real row, if the generator does not copy | weaker relationships; must be tested |
| **Differential privacy** | a bound on what any one person changes | noise, and a budget that runs out |

#### [day1#match-control] The use decides the control, and the control decides the risk left

*Fit the control to the release*

- Follow one applicant over years inside the fund: **pseudonymisation**
- Row-level records for an approved study: **de-identification**
- Once-a-year regional counts: **aggregation**
- A realistic file for a hackathon: **synthetic data**
- Monthly district counts on a public dashboard: **differential privacy**

- **Residual risk is part of the answer.** The monthly dashboard spends its budget twelve times a year. The hackathon file is only as safe as the generator's leakage test.

#### [day1#check-control] Which control fits the monthly dashboard?

*Checkpoint*

**Question:** Bashayer wants applicants per district on a public dashboard, refreshed every month. Some districts have fewer than ten applicants a month. Which control fits best?

- A. Pseudonymise the applicant numbers before counting
- B. Suppress every count below ten each month
- C. Publish a synthetic extract instead of counts
- D. Add calibrated noise under a stated yearly privacy budget

#### [day1#lab-1-2] Classify three extracts

Lab 1.2 · 25 min

Assign classification levels to three extracts and decide which may leave the fund.

[D1_2_assign_classification_levels.ipynb](https://sdaiaacademy.github.io/ds-309/labs/D1_2_assign_classification_levels.ipynb)

- [ ] Read the three extracts (3 min)
- [ ] Score the impact and the level of each (7 min)
- [ ] Decide which may leave the fund, and on what conditions (7 min)
- [ ] Five releases, five controls: the decision table (8 min)
- [ ] ✱ Stretch: Rewrite the researcher's request so that it asks for the minimum necessary

### Session 3: Linkage attacks

#### [day1#s3] Linkage attacks

*Session 3*

- Explain how a linkage attack joins a release to an outside file
- Run a linkage on quasi-identifiers and measure its success
- Name what a successful link discloses

#### [day1#linkage-attack] A linkage attack joins the release to a file that has names

*How a release without names is re-identified*

1. **1 · Release** study code, birth date, gender, postcode, income, decision
2. **2 · Outside file** name, birth date, gender, postcode
3. **3 · Join** on the shared fields
4. **4 · Unique match** a name attached to an income and a decision

> **In the lab.** A synthetic volunteers register published online: 9,000 people, 3,000 of whom applied to the fund.

#### [day1#linkage-result] Three ordinary fields re-identify 99% of the register's applicants

*Lab 1.3, the reference run*

- **3,042** register rows with exactly one match
- **99.2%** of the 3,000 applicants correctly named
- **97.8%** of claimed links are right

> **The 66 wrong links harm people too.** Someone who never applied is now believed to be on social security, or declined.

#### [day1#what-links-reveal] What the 3,042 named records disclose

*A link is the door, not the harm*

| Item | Value |
| --- | --- |
| Declined by the fund | 1,662 |
| On social security | 420 |
| Disability in household | 267 |

Plus the exact monthly income of every named person.

#### [day1#coarser-join] Coarsening one field cuts the links from 99% to 17%

*The lever that matters most*

| Join on | Claimed | Correct | Success | Precision |
| --- | --- | --- | --- | --- |
| birth date, gender, postcode | 3,042 | 2,976 | 99.2% | 97.8% |
| birth year, gender, postcode | 1,595 | 506 | 16.9% | 31.7% |

> **Takeaway.** Not zero, and two in three claimed links are now wrong: the attacker can no longer tell which ones to trust. Day 2 finishes the job with a hierarchy and a k.

#### [day1#background-knowledge] Assume the attacker knows someone who applied

*Who the attacker is*

- **Prosecutor.** Knows a specific person is in the release and looks for their row.
- **Journalist.** Has an outside file and links whoever links; does not know who applied.
- **Insider.** A relative or colleague who knows exact values: birth date, household size, sector.

#### [day1#check-which-field] Which change stops most of the links?

*Checkpoint*

**Question:** Release A links 99% of the register's applicants on birth date, gender and postcode. Waad needs household size and approval by region. Which single change cuts the links most while keeping her question answerable?

- A. Replace the birth date with an age band
- B. Remove gender
- C. Replace the study code with a new random code
- D. Round income to the nearest 1,000 riyals

#### [day1#lab-1-3] Link the release to the register

Lab 1.3 · 25 min

Re-identify applicants by linking a release to a synthetic public register.

[D1_3_re_identify_applicants.ipynb](https://sdaiaacademy.github.io/ds-309/labs/D1_3_re_identify_applicants.ipynb)

- [ ] Load the release and the register (3 min)
- [ ] Join on birth date, gender and postcode (7 min)
- [ ] Keep unique matches and score them against the truth key (7 min)
- [ ] What the links reveal (5 min)
- [ ] Try a coarser join (3 min)
- [ ] ✱ Stretch: Link on the district in place of the postcode and compare the success

### Session 4: Measuring disclosure risk

#### [day1#s4] Measuring disclosure risk

*Session 4*

- Compute equivalence classes, uniqueness and k for a release
- Compare candidate releases by record-level risk
- Explain why k alone misses attribute disclosure

#### [day1#equivalence-class] An equivalence class is everyone who looks the same on the quasi-identifiers

*Risk without an outside file*

| age band | gender | region | nationality | class size |
| --- | --- | --- | --- | --- |
| 31-40 | F | Riyadh | Saudi | 1,410 |
| 41-50 | M | Tabuk | Saudi | 409 |
| 51-60 | F | Al-Jouf | Non-Saudi | 1 |

- The **class size** is how many people a record hides among
- A class of 1 is a **unique** record
- The release's **k** is its smallest class

#### [day1#three-releases-risk] The same 60,000 people, three very different risks

*Lab 1.4, the reference run*

| Release | Quasi-identifiers | Unique | Below 5 | Average risk |
| --- | --- | --- | --- | --- |
| A | birth date, gender, postcode | 59,458 | 100% | 0.996 |
| B | birth year, gender, district, nationality | 2,152 | 14.3% | 0.129 |
| C | age band, gender, region, nationality | 7 | 0.1% | 0.004 |

All three have k = 1.

#### [day1#k-is-a-floor] k is a floor for the most exposed person, not an average

*What k tells you*

- **k = 5**: every record hides among at least five
- One unique record makes k = 1 for the whole release
- Report k with the **share below the target** and the **average risk**
- The fund's target in this course: **k of at least 5**

- **Average risk.** The mean of one over the class size: the chance that a prosecutor picks the right record. Release C: 0.004. Its maximum is still 1.

#### [day1#attribute-disclosure] A class of five that all share one value discloses it to anyone who finds the class

*When k is met and the harm happens anyway*

- **Homogeneity.** In release B, 661 of 3,241 classes of five or more have a single social security value (Lab 1.4 stretch).
- **l-diversity.** Ask every class to hold at least l different values of the sensitive attribute. A partial fix: two values can still be "yes" and "almost yes".

#### [day1#tools-for-risk] Write it in pandas to see the mechanism, then use a tool for the release

*Tools for disclosure risk*

```python
# file: python
sizes = df.groupby(qi)[qi[0]].transform("size")
unique   = (sizes == 1).sum()
k        = sizes.min()
below_5  = (sizes < 5).mean()
avg_risk = (1 / sizes).mean()
```

- **ARX.** A desktop and Java tool: hierarchies, k, l, t, risk models and utility.
- **sdcMicro.** An R package for statistical disclosure control with risk and utility measures.

#### [day1#check-k] Which release is safer?

*Checkpoint*

**Question:** Release B and release C both have k = 1. B has 2,152 unique records and C has 7. Yahya asks whether they are equally risky. What do you tell him?

- A. Yes: both have k = 1, so both expose someone
- B. B is safer because its birth year and district are more precise
- C. C is far safer, but neither meets k of five until the small classes are treated
- D. C is safe to release as it is, since seven records is negligible

#### [day1#lab-1-4] Uniqueness and k for three releases

Lab 1.4 · 25 min

Compute unique quasi-identifier combinations and k for three candidate releases.

[D1_4_compute_unique_quasi.ipynb](https://sdaiaacademy.github.io/ds-309/labs/D1_4_compute_unique_quasi.ipynb)

- [ ] Build the three candidate releases (5 min)
- [ ] Equivalence class sizes (6 min)
- [ ] Unique records, k and records below five (7 min)
- [ ] Average re-identification risk (4 min)
- [ ] Pick the release to treat (3 min)
- [ ] ✱ Stretch: Measure the l-diversity of social security status in release B

#### [day1#wrap-up] Find the personal data, then measure how identifying it still is

*Day 1 · Three things to keep*

- **Fields are not equal.** Direct identifiers, quasi-identifiers, sensitive attributes and free text each need a different decision.
- **No names is not anonymous.** Three ordinary fields linked 99% of the register's applicants to their income and decision.
- **Report risk with numbers.** Unique records, k, the share below five and the average risk, together.

#### [day1#next] Release with less risk

*Tomorrow · Day 2*

- Treat release A to k of at least five and measure what the analysis loses
- Publish district counts with differential privacy, at three budgets
- Split one budget over four queries, then test a synthetic extract for leakage
- Before tomorrow: rerun Lab 1.4 if it did not finish; Lab 2.1 starts from the supplied release

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

## Capstone: Capstone: the release pack

Ten-minute reviews of the Sabeel Scholarship Fund release pack, with one disparity recomputed live

#### [capstone#title] Capstone: the release pack

*SDAIA Academy · Responsible Data Science: Privacy, Fairness and Documentation*

Capstone: Ten-minute reviews of the Sabeel Scholarship Fund release pack, with one disparity recomputed live

Data Science Track · 4 teaching days + capstone day · 10 min talk and demo · DS-309

#### [capstone#agenda] How the presentations run

*Capstone*

- **Expectations and final prep**: the rubric, a last rehearsal, then the first presentations
- **Presentations**: ten minutes each, with one disparity recomputed live and questions inside the ten minutes
- **Review and closing**: peer feedback, the trainer's review, what next

#### [capstone#rubric] The rubric

*How presentations are scored*

| Item | Value |
| --- | --- |
| Privacy | 25% |
| Fairness audit | 25% |
| Documentation | 20% |
| Impact assessment | 20% |
| Reproducibility | 10% |

> **How the course is assessed.** This rubric is 60% of the mark, the live recomputation 20% and the supervised AI-off check 20%. To pass: 70% overall and at least 60% on the rubric.

#### [capstone#format] Ten minutes each, questions and the live recomputation included

*Format of the review*

- **1 · The release · 3 min.** Risk before and after, the treatment, the budget, what remains.
- **2 · The audit · 3 min.** The largest gap with its interval, its cause, the mitigation and its cost.
- **3 · Live · 4 min.** The assessor picks a slice; you recompute one disparity from your repository, then questions.

> **Peer feedback.** After each review, everyone writes one strength, one question and one suggestion.

#### [capstone#running-order] Who presents when

*Running order*

| # | Presenter | Project |
| --- | --- | --- |
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |
| 5 |  |  |
| 6 |  |  |
| 7 |  |  |
| 8 |  |  |

#### [capstone#final-prep] Final prep · 20 minutes

*Before the first presentation*

Rehearse once, record a backup, try the demo on this screen.

#### [capstone#now-presenting] Talk and demo

*Now presenting*

#### [capstone#review] What the presentations showed

*Trainer review*

- **Strongest patterns.** What several packs got right: linkage tests, intervals, logs.
- **Common gaps.** What most would fix next. Usual ones: an audit that stopped at gender, a residual risk lowered by its impact.
- **One surprise.** A finding nobody expected, and what explained it.

#### [capstone#what-next] Keep going

*After the course*

- **The follow-up task:** take one release or model at your workplace through the impact assessment and send the scored register, not the data.
- **Your repository stays yours:** keep it rerunning from a clean copy and add the mitigation you named today.
- **At work:** keep a release log from the next extract on; a datasheet is only as good as its log.
- **Next Academy course:** DS-305 Uncertainty, Interpretability and Model Validation, for calibration and explanation.

#### [capstone#thanks] Thank you

*SDAIA Academy*

Responsible Data Science: Privacy, Fairness and Documentation
