# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 1.1 · Tag the applicant fields (AI-off)
#
# Day 1 · Session 1 (Personal data in an analysis) · 25 min.
#
# Yusr Housing Support Fund holds 60,000 applications in one table. Waad Al-Shehri, a university
# researcher, wants to study how household size and income relate to approval in each region. You
# tag every field by how it identifies a person, find the identifiers hiding in the case notes, and
# decide field by field what may go into her extract. **AI off**: this lab is done without an
# assistant, as the supervised check will be.
#
# **Reference state.** `data/applicants.csv.gz`. Nothing from another lab.
#
# **Tasks**
# - [ ] 1 · Load the table and list its fields (3')
# - [ ] 2 · Tag each field by identifiability (8')
# - [ ] 3 · Find identifiers in the case notes (6')
# - [ ] 4 · Keep, drop or transform, with a reason (6')
# - [ ] 5 · Count what the purpose still needs (2')
# - [ ] ✱ Stretch · Hash the national identifier and decide whether the hash is still personal data

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

import re
import pandas as pd
import yusr as U

# %% [markdown]
# ## 1 · Load the table and list its fields (3')
#
# Look at three rows and at the list of columns. Every value is synthetic: identifiers carry the
# marker `SYN`, and e-mail addresses end in `example.org`.

# %%
apps = U.load("applicants.csv.gz")
print(len(apps), "applications,", apps.shape[1], "fields")
print(apps.head(3).T)

# %% [markdown]
# ## 2 · Tag each field by identifiability (8')
#
# Four tags, and a fifth for text:
#
# | Tag | Meaning | Test |
# |---|---|---|
# | `direct` | identifies one person by itself | could you phone or find the person with this field alone? |
# | `quasi` | identifies in combination, and someone outside could know it | would a neighbour, an employer or a public list hold it? |
# | `sensitive` | what an attacker wants to learn about a person | would disclosure harm the person or expose their finances, health or support? |
# | `other` | none of these | |
# | `free_text` | free text, which can hold any of the above | |
#
# ✏️ **Exercise** · Complete `make_tags()`: one tag for every field.

# %%
def make_tags() -> dict:
    # BEGIN SOLUTION
    return {
    "applicant_id": "direct", "national_id": "direct", "full_name": "direct", "mobile": "direct", "email": "direct",
    "birth_date": "quasi", "gender": "quasi", "nationality": "quasi", "marital_status": "quasi", "region": "quasi",
    "district": "quasi", "postcode": "quasi", "household_size": "quasi", "employment": "quasi",
    "monthly_income_sar": "sensitive", "disability_in_household": "sensitive", "social_security": "sensitive",
    "tenure": "other", "monthly_rent_sar": "other", "application_date": "quasi", "office": "quasi",
    "officer_decision": "sensitive", "case_note": "free_text",
    }
    # END SOLUTION

# %%
# Check, with a safety net: the cells below still run when the exercise is not done yet
try:
    tags = make_tags()
except NotImplementedError:
    tags = U.reference("lab11_tags")
U.keep("lab11_tags", tags)
U.check(set(tags) == set(apps.columns), "every field has a tag")
key_direct = {"applicant_id", "national_id", "full_name", "mobile", "email"}
U.check({f for f, t in tags.items() if t == "direct"} == key_direct, "the five direct identifiers are tagged direct")
print(pd.Series(tags).value_counts())

# %% [markdown]
# **Look at** `applicant_id`. It is the fund's own number, not a name. Why is it a direct
# identifier inside the fund? Because anyone with the fund's systems can look the person up with
# it alone. Outside the fund it is a key to the person's whole file.

# %% [markdown]
# ## 3 · Find identifiers in the case notes (6')
#
# Officers type notes. Some contain a mobile number, a national identifier or a first name.
#
# ✏️ **Exercise** · Write `identifiers_in(note)`: return the set of kinds found (`"mobile"`,
# `"national_id"`, `"name"`). Mobiles look like `05-SYN-123456`, national identifiers like
# `SYN1234567`. For names, use the first names that appear in `full_name`.

# %%
FIRST_NAMES = set(apps["full_name"].str.split().str[0])

def identifiers_in(note) -> set:
    # BEGIN SOLUTION
    found = set()
    if not isinstance(note, str) or not note:
        return found
    if re.search(r"05-SYN-\d{6}", note):
        found.add("mobile")
    if re.search(r"\bSYN\d{7}\b", note):
        found.add("national_id")
    if any(w.strip(".,;") in FIRST_NAMES for w in note.split()):
        found.add("name")
    return found
    # END SOLUTION

# %%
try:
    hits = apps["case_note"].map(identifiers_in)
    n_hits = int((hits.map(len) > 0).sum())
    kinds = pd.Series([k for s in hits for k in s]).value_counts().to_dict()
except NotImplementedError:
    ref = U.reference("lab11_notes")
    n_hits, kinds = ref["n_hits"], ref["kinds"]
U.keep("lab11_notes", {"n_hits": n_hits, "kinds": kinds})
print(n_hits, "notes hold an identifier:", kinds)
U.check(n_hits == U.json("reference/generator_facts.json")["notes_with_identifiers"],
        "every planted identifier in the notes is found, and nothing else")

# %% [markdown]
# ## 4 · Keep, drop or transform, with a reason (6')
#
# The purpose: *how household size and income relate to approval, by region*. For each field
# decide `keep`, `drop` or `transform` (say into what), and give the reason in a few words.
#
# ✏️ **Exercise** · Complete `make_decisions()`: `field: (decision, reason)` for every field.

# %%
def make_decisions() -> dict:
    # BEGIN SOLUTION
    return {
    "applicant_id": ("transform", "replace with a study code; the key stays with the data protection officer"),
    "national_id": ("drop", "not needed for the purpose"), "full_name": ("drop", "not needed for the purpose"),
    "mobile": ("drop", "not needed for the purpose"), "email": ("drop", "not needed for the purpose"),
    "birth_date": ("transform", "age band is enough for the purpose"), "gender": ("keep", "needed to read approval by group"),
    "nationality": ("drop", "not part of the question"), "marital_status": ("drop", "not part of the question"),
    "region": ("keep", "the question is by region"), "district": ("drop", "region is the unit of the question"),
    "postcode": ("drop", "region is the unit of the question"), "household_size": ("keep", "named in the question"),
    "employment": ("drop", "not part of the question"), "monthly_income_sar": ("transform", "income band of 1,000 riyals"),
    "disability_in_household": ("drop", "not part of the question"), "social_security": ("drop", "not part of the question"),
    "tenure": ("drop", "not part of the question"), "monthly_rent_sar": ("drop", "not part of the question"),
    "application_date": ("transform", "year of application only"), "office": ("drop", "region already says it"),
    "officer_decision": ("keep", "the outcome of the question"), "case_note": ("drop", "free text holds identifiers"),
    }
    # END SOLUTION

# %%
try:
    decisions = make_decisions()
except NotImplementedError:
    decisions = {k: tuple(v) for k, v in U.reference("lab11_decisions").items()}
U.keep("lab11_decisions", decisions)
U.check(set(decisions) == set(apps.columns), "every field has a decision")
U.check(all(decisions[f][0] != "keep" for f, t in tags.items() if t in ("direct", "free_text")),
        "no direct identifier and no free text is kept as it is")
U.check(all(len(str(r).split()) >= 3 for _, r in decisions.values()), "every decision has a reason of a few words")

# %% [markdown]
# ## 5 · Count what the purpose still needs (2')

# %%
leaving = [f for f, (d, _) in decisions.items() if d != "drop"]
print(len(leaving), "of", apps.shape[1], "fields leave the fund, kept or transformed:", leaving)

# %% [markdown]
# ## ✱ Stretch · A hashed national identifier
#
# Replace `national_id` by its SHA-256 hash. Can someone who holds a list of national identifiers
# find a person in the hashed extract? Try it with five identifiers from the table.

# %%
import hashlib
h = apps["national_id"].head(5).map(lambda s: hashlib.sha256(s.encode()).hexdigest()[:16])
print(pd.DataFrame({"national_id": apps["national_id"].head(5), "hash": h}))
# Anyone with the list recomputes the same hashes: the hash is a pseudonym, and the extract is still personal data.

# %% [markdown]
# ## Check yourself
#
# 1. Why is `postcode` a quasi-identifier and not a direct one?
# 2. A note says "Spoke to Hind at the branch". Which tag does the whole field get, and why?
# 3. Waad asks for the exact birth date "to compute age precisely". What do you answer?
#
# <details><summary>Answers</summary>
#
# 1. A postcode alone covers many people; with a birth date and a gender it points at one.
# 2. `free_text`: any note may hold identifiers, so the field is treated as identifying and dropped or redacted as a whole.
# 3. An age band meets the purpose; the exact date adds re-identification risk and nothing the question needs.
# </details>
#
# **Carry forward.** Session 2 classifies the extract these decisions describe.
