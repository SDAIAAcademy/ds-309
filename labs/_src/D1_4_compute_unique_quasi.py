# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 1.4 · Uniqueness and k for three releases
#
# Day 1 · Session 4 (Measuring disclosure risk) · 25 min.
#
# Lab 1.3 needed an outside file to show the risk. Here you measure it from the release alone:
# for three candidate releases you compute the equivalence classes on their quasi-identifiers,
# the unique records, the release's k, the records in classes smaller than five, and the average
# re-identification risk. Then you pick the release that Day 2 will treat.
#
# **Reference state.** `data/release_a_research_extract.csv.gz`. Nothing from another lab.
#
# **Tasks**
# - [ ] 1 · Build the three candidate releases (5')
# - [ ] 2 · Equivalence class sizes (6')
# - [ ] 3 · Unique records, k and records below five (7')
# - [ ] 4 · Average re-identification risk (4')
# - [ ] 5 · Pick the release to treat (3')
# - [ ] ✱ Stretch · Measure the l-diversity of social security status in release B

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

# %% [markdown]
# ## 1 · Build the three candidate releases (5')
#
# | Release | Quasi-identifiers |
# |---|---|
# | A | birth date, gender, postcode |
# | B | birth year, gender, district, nationality |
# | C | ten-year age band, gender, region, nationality |

# %%
base = U.load("release_a_research_extract.csv.gz")
base["birth_year"] = base["birth_date"].str[:4].astype(int)
base["age_band"] = pd.cut(2026 - base["birth_year"], [0, 30, 40, 50, 60, 200],
                          labels=["21-30", "31-40", "41-50", "51-60", "61+"]).astype(str)
QI = {
    "A": ["birth_date", "gender", "postcode"],
    "B": ["birth_year", "gender", "district", "nationality"],
    "C": ["age_band", "gender", "region", "nationality"],
}
print({k: len(base.groupby(v).size()) for k, v in QI.items()}, "distinct combinations")

# %% [markdown]
# ## 2 · Equivalence class sizes (6')
#
# An **equivalence class** is the set of records that share the same values on every
# quasi-identifier. Its size is how many people a record hides among.
#
# ✏️ **Exercise** · Write `class_sizes(df, quasi)`: a Series, one value per record, the size of
# its class. (`U.classes` does the same; write it yourself first.)

# %%
def class_sizes(df: pd.DataFrame, quasi: list) -> pd.Series:
    # BEGIN SOLUTION
    return df.groupby(quasi)[quasi[0]].transform("size")
    # END SOLUTION

# %%
try:
    sizes = {k: class_sizes(base, q) for k, q in QI.items()}
except NotImplementedError:
    print("(safety net: using U.classes)")
    sizes = {k: U.classes(base, q) for k, q in QI.items()}
U.check(all(len(s) == len(base) for s in sizes.values()), "one class size per record")
U.check(sizes["A"].equals(U.classes(base, QI["A"])), "the class sizes agree with the helper")

# %% [markdown]
# ## 3 · Unique records, k and records below five (7')
#
# ✏️ **Exercise** · Write `risk_table(sizes)`: one row per release with `unique` (records alone
# in their class), `k` (the smallest class), `below_5` (records in classes smaller than five) and
# `below_5_share`.

# %%
def risk_table(sizes: dict) -> pd.DataFrame:
    # BEGIN SOLUTION
    rows = []
    for k, s in sizes.items():
        rows.append({"release": k, "unique": int((s == 1).sum()), "k": int(s.min()),
                     "below_5": int((s < 5).sum()), "below_5_share": round(float((s < 5).mean()), 4)})
    return pd.DataFrame(rows).set_index("release")
    # END SOLUTION

# %%
try:
    risk = risk_table(sizes)
except NotImplementedError:
    risk = U.reference("lab14_risk")
U.keep("lab14_risk", risk)
print(risk)
U.check(int(risk.loc["A", "unique"]) > 0.95 * len(base), "almost every record of A is unique")
U.check(int(risk.loc["C", "k"]) < 5, "even the coarsest release still has classes below five")

# %% [markdown]
# ## 4 · Average re-identification risk (4')
#
# If an attacker knows someone is in the release and knows their quasi-identifiers, the chance of
# picking the right record is one over the size of its class. The mean over records is the
# average risk; the maximum is the risk of the most exposed person.

# %%
risk["avg_risk"] = [round(float((1 / s).mean()), 4) for s in sizes.values()]
risk["max_risk"] = [round(float((1 / s).max()), 4) for s in sizes.values()]
print(risk[["avg_risk", "max_risk"]])
U.keep("lab14_risk_full", risk)

# %% [markdown]
# **Look at** C. Its average risk is tiny, but its maximum is still 1: some people are alone in
# their class. Which ones? Print them.

# %%
alone_c = base[sizes["C"] == 1][QI["C"]]
print(alone_c)

# %% [markdown]
# ## 5 · Pick the release to treat (3')
#
# Waad's question needs household size, income and approval by region. C answers it with the
# least risk, but it is still not at k of five. Write in one line which release you would treat on
# Day 2 and what has to change.

# %%
choice = "A, generalised along its hierarchy until it looks like C, then the few classes below five suppressed"
print(choice)

# %% [markdown]
# ## ✱ Stretch · l-diversity in release B
#
# A class of five in which every record says `social_security = yes` discloses that attribute to
# anyone who finds the class. Count B's classes of size five or more that have only one value of
# `social_security`.

# %%
big = base[sizes["B"] >= 5]
uniform = big.groupby(QI["B"])["social_security"].nunique()
print(int((uniform == 1).sum()), "of", len(uniform), "classes of size five or more have a single social security value")

# %% [markdown]
# ## Check yourself
#
# 1. Release B's k is 1. Does that mean every record in B is unique?
# 2. Two releases have the same k. How else can you tell which is safer?
# 3. Why is k not enough when the sensitive attribute is the same for the whole class?
#
# <details><summary>Answers</summary>
#
# 1. No: k is the smallest class. Read `unique` and `below_5` for how many people are exposed.
# 2. The share of records below five, and the average risk.
# 3. The attacker learns the attribute without picking the record: that is attribute disclosure.
# </details>
#
# **Carry forward.** Lab 2.1 starts again from release A and treats it to k of at least five.
