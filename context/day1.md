---
course: "Responsible Data Science: Privacy, Fairness and Documentation"
code: "DS-309"
version: "2027.1.0"
deck: "day1"
day: 1
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-309/slides/day1.html"
---

# Responsible Data Science: Privacy, Fairness and Documentation

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
