# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 1.2 · Classify three extracts
#
# Day 1 · Session 2 (Classification and permitted use) · 25 min.
#
# Three extracts sit on the fund's analysis server: the full applicant table, the pseudonymised
# research extract prepared for Waad Al-Shehri, and a table of approved applicants per district and nationality for
# the annual report. You profile each one, assign its classification level from the impact of a
# disclosure, decide which may leave the fund and on what conditions, and finish with the decision
# table of five releases that LO1 asks for.
#
# **Reference state.** `data/applicants.csv.gz` and `data/release_a_research_extract.csv.gz`.
# Nothing from another lab.
#
# **Tasks**
# - [ ] 1 · Read the three extracts (3')
# - [ ] 2 · Score the impact and the level of each (7')
# - [ ] 3 · Decide which may leave the fund, and on what conditions (7')
# - [ ] 4 · Five releases, five controls: the decision table (8')
# - [ ] ✱ Stretch · Rewrite the researcher's request so that it asks for the minimum necessary

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ds-309.git"
    if not Path("/content/ds-309").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ds-309"], check=True)
    os.chdir("/content/ds-309/labs")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True)
else:
    while not Path("yusr.py").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

import pandas as pd
import yusr as U

DIRECT = {"applicant_id", "national_id", "full_name", "mobile", "email", "case_note"}
QUASI = {"birth_date", "gender", "nationality", "marital_status", "region", "district", "postcode",
         "household_size", "employment", "application_date", "office"}

# %% [markdown]
# ## 1 · Read the three extracts (3')

# %%
e1 = U.load("applicants.csv.gz")
e2 = U.load("release_a_research_extract.csv.gz")
e3 = (e1[e1["officer_decision"] == "approved"].groupby(["region", "district", "nationality"]).size()
      .rename("approved").reset_index())
EXTRACTS = {"E1 applicant table": e1, "E2 research extract": e2, "E3 district counts": e3}
for name, df in EXTRACTS.items():
    print(f"{name}: {df.shape[0]:,} rows, columns: {', '.join(df.columns[:8])}{' ...' if df.shape[1] > 8 else ''}")
print("smallest district count in E3:", int(e3["approved"].min()))

# %% [markdown]
# ## 2 · Score the impact and the level of each (7')
#
# The Data Classification Policy sets the level by the impact of an unauthorised disclosure:
# **Top Secret** (high), **Secret** (medium), **Restricted** (low) and **Public** (none). It lists
# personally identifiable information, such as names and identification numbers, among its
# examples of Restricted data, and splits Restricted by scale: **A** a whole sector, **B** several
# entities or a group of individuals, **C** one entity or one individual.
#
# ✏️ **Exercise** · Write `profile(df)` (what the extract holds) and `level(p)` (the level from
# the profile). Treat an extract as personal data when it holds a direct identifier, or at least
# three quasi-identifiers at row level. An aggregate table is `Public` only when no count is below
# 10; otherwise it waits for the disclosure check of Day 2 and stays `Restricted - C`.

# %%
def profile(df: pd.DataFrame) -> dict:
    # BEGIN SOLUTION
    cols = set(df.columns)
    row_level = "approved" not in cols
    return {"direct": sorted(cols & DIRECT), "quasi": sorted(cols & QUASI), "row_level": row_level,
            "people": int(len(df)) if row_level else int(df["approved"].sum()),
            "min_cell": None if row_level else int(df["approved"].min())}
    # END SOLUTION


def level(p: dict) -> str:
    # BEGIN SOLUTION
    personal = bool(p["direct"]) or (p["row_level"] and len(p["quasi"]) >= 3)
    if personal:
        return "Restricted - B" if p["people"] > 1 else "Restricted - C"
    if p["min_cell"] is not None and p["min_cell"] < 10:
        return "Restricted - C"
    return "Public"
    # END SOLUTION

# %%
try:
    levels = {name: level(profile(df)) for name, df in EXTRACTS.items()}
except NotImplementedError:
    levels = U.reference("lab12_levels")
U.keep("lab12_levels", levels)
print(pd.Series(levels))
U.check(levels["E1 applicant table"].startswith("Restricted"), "the applicant table is Restricted")
U.check(levels["E2 research extract"].startswith("Restricted"),
        "the pseudonymised extract is still personal data, so still Restricted")

# %% [markdown]
# **Look at** E2. It has no name and no national identifier. The anonymisation guideline is
# explicit that pseudonymised data is still personal data: the code can be reversed by whoever
# holds the key, and the quasi-identifiers that are left can be linked (Session 3).

# %% [markdown]
# ## 3 · Decide which may leave the fund, and on what conditions (7')
#
# The General Rules for Secondary Use of Data ask for a legitimate purpose that serves the public
# interest or research and is not for profit, data confined to the minimum necessary for that
# purpose, a request to the entity that holds the data and, for a researcher, a request through
# her institution with its written approval.
#
# ✏️ **Exercise** · Write `leave()`: for each extract, `(may_leave, [conditions])`.

# %%
def leave() -> dict:
    # BEGIN SOLUTION
    return {
        "E1 applicant table": (False, ["stays inside the fund; used only for the purpose it was collected for"]),
        "E2 research extract": (True, ["a sharing request through the researcher's university, with its written approval",
                                       "a stated research purpose that is not for profit",
                                       "only the minimum necessary fields (Lab 1.1 decisions)",
                                       "disclosure risk reduced and measured first (Day 2)",
                                       "a sharing agreement with retention and destruction terms"]),
        "E3 district counts": (True, ["published only after the counts below 10 are treated (Day 2)"]),
    }
    # END SOLUTION

# %%
try:
    decisions = leave()
except NotImplementedError:
    decisions = {k: tuple(v) for k, v in U.reference("lab12_leave").items()}
U.keep("lab12_leave", decisions)
for k, (ok, cond) in decisions.items():
    print(f"{k}: {'may leave' if ok else 'stays'}", *[f"\n   - {c}" for c in cond])
U.check(decisions["E1 applicant table"][0] is False, "the full table does not leave the fund")
U.check(decisions["E2 research extract"][0] and len(decisions["E2 research extract"][1]) >= 3,
        "the research extract leaves only under at least three conditions")
U.check(any("minimum" in c for c in decisions["E2 research extract"][1]), "minimum necessary is one of them")

# %% [markdown]
# ## 4 · Five releases, five controls: the decision table (8')
#
# Five controls, each with a different guarantee and cost: **pseudonymisation**,
# **de-identification** (generalise and suppress to a k), **aggregation**, **synthetic data** and
# **differential privacy**. Match each release to the control that fits, and name the risk that
# remains after it.
#
# ✏️ **Exercise** · Complete `table()`: release → `(control, residual risk)`.

# %%
RELEASES = {
    "R1": "Fund analysts link applications across three years and must follow the same applicant",
    "R2": "Row-level records for an approved university study of household size and approval",
    "R3": "Approved applicants per region, once a year, in the annual report",
    "R4": "A realistic file for a hackathon that builds prototype dashboards",
    "R5": "Applicants per district, updated every month on a public dashboard",
}
CONTROLS = ["pseudonymisation", "de-identification", "aggregation", "synthetic data", "differential privacy"]

def table() -> dict:
    # BEGIN SOLUTION
    return {
        "R1": ("pseudonymisation", "still personal data: the key reverses it and the quasi-identifiers still link"),
        "R2": ("de-identification", "attribute disclosure in uniform groups and outside knowledge; utility lost"),
        "R3": ("aggregation", "small cells and differencing between tables"),
        "R4": ("synthetic data", "a generator that copies records or lets membership be inferred"),
        "R5": ("differential privacy", "noise in small districts, and a budget spent again every month"),
    }
    # END SOLUTION

# %%
try:
    decision_table = table()
except NotImplementedError:
    decision_table = {k: tuple(v) for k, v in U.reference("lab12_table").items()}
U.keep("lab12_table", decision_table)
print(pd.DataFrame([(k, RELEASES[k], c, r) for k, (c, r) in decision_table.items()],
                   columns=["release", "described", "control", "residual risk"]).to_string(index=False))
key = {"R1": "pseudonymisation", "R2": "de-identification", "R3": "aggregation", "R4": "synthetic data",
       "R5": "differential privacy"}
U.check(all(decision_table[k][0] == v for k, v in key.items()), "each release has the control that fits it")
U.check(all(len(r.split()) >= 4 for _, r in decision_table.values()), "each row names its residual risk")
U.out("lab12").joinpath("decision_table.csv").write_text(
    pd.DataFrame([(k, c, r) for k, (c, r) in decision_table.items()], columns=["release", "control", "residual"])
    .to_csv(index=False), encoding="utf-8")

# %% [markdown]
# ## ✱ Stretch · The minimum necessary
#
# Waad's request asks for "the applicant table without names". Rewrite it in three lines: the
# question, the fields with their form (from Lab 1.1), and what she will not receive.

# %% [markdown]
# ## Check yourself
#
# 1. Why does removing names not make E2 Public?
# 2. Which control lets the fund follow one applicant over years, and why is that data still personal?
# 3. R5 is refreshed monthly. What happens to its privacy loss over a year?
#
# <details><summary>Answers</summary>
#
# 1. Its rows still describe individuals who can be singled out by quasi-identifiers; the policy's level follows the impact of disclosure, which is unchanged.
# 2. Pseudonymisation: the same code for the same person. The key exists and the quasi-identifiers remain, so it is personal data.
# 3. It adds up: twelve releases spend twelve times the monthly budget (Day 2, Session 3).
# </details>
#
# **Carry forward.** `artifacts/lab12/decision_table.csv` is the LO1 evidence for your portfolio.
