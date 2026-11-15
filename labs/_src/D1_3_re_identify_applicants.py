# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 1.3 · Link the release to the register
#
# Day 1 · Session 3 (Linkage attacks) · 25 min.
#
# The research extract (release A) has no names. A volunteers register published online has names,
# birth dates, genders and postcodes for 9,000 people, some of whom applied to the fund. You play
# the attacker: join the two files, keep the links that point at exactly one record, score them
# against a truth key the attacker would not have, and count what the links disclose.
#
# **Reference state.** `data/release_a_research_extract.csv.gz`, `data/public_register.csv` and,
# for scoring only, `data/reference/linkage_truth.csv`. Nothing from another lab.
#
# **Tasks**
# - [ ] 1 · Load the release and the register (3')
# - [ ] 2 · Join on birth date, gender and postcode (7')
# - [ ] 3 · Keep unique matches and score them against the truth key (7')
# - [ ] 4 · What the links reveal (5')
# - [ ] 5 · Try a coarser join (3')
# - [ ] ✱ Stretch · Link on the district in place of the postcode and compare the success

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
# ## 1 · Load the release and the register (3')

# %%
release = U.load("release_a_research_extract.csv.gz")
register = U.load("public_register.csv")
truth = U.load("reference/linkage_truth.csv").fillna("")
print(len(release), "release rows ·", len(register), "register rows ·",
      int((truth["pseudo_id"] != "").sum()), "register people who are applicants (the attacker does not know this)")
print(register.head(3))

# %% [markdown]
# ## 2 · Join on birth date, gender and postcode (7')
#
# ✏️ **Exercise** · Write `link(release, register, on)`: for every register row, the release rows
# that share its values on `on`. Return one row per register record with the columns
# `register_id`, `matches` (how many release rows match) and `pseudo_id` (the matched code when
# there is exactly one match, otherwise empty).

# %%
def link(release: pd.DataFrame, register: pd.DataFrame, on: list) -> pd.DataFrame:
    # BEGIN SOLUTION
    sizes = release.groupby(on).size().rename("matches").reset_index()
    first = release.groupby(on)["pseudo_id"].first().rename("candidate").reset_index()
    j = register[["register_id"] + on].merge(sizes, on=on, how="left").merge(first, on=on, how="left")
    j["matches"] = j["matches"].fillna(0).astype(int)
    j["pseudo_id"] = j["candidate"].where(j["matches"] == 1, "").fillna("")
    return j[["register_id", "matches", "pseudo_id"]]
    # END SOLUTION

# %%
QI = ["birth_date", "gender", "postcode"]
try:
    links = link(release, register, QI)
except NotImplementedError:
    links = U.reference("lab13_links")
U.keep("lab13_links", links)
print(links["matches"].value_counts().sort_index().head(6))
U.check(len(links) == len(register), "one row per register record")

# %% [markdown]
# ## 3 · Keep unique matches and score them (7')
#
# **Linkage success** is the share of the register's applicants that are correctly re-identified.
# **Precision** is the share of claimed links that are right: a non-applicant who happens to share
# a unique combination is a false link, and it harms them too.
#
# ✏️ **Exercise** · Write `score(links, truth)` returning `claimed`, `correct`, `success` and `precision`.

# %%
def score(links: pd.DataFrame, truth: pd.DataFrame) -> dict:
    # BEGIN SOLUTION
    m = links.merge(truth.rename(columns={"pseudo_id": "true_id"}), on="register_id")
    claimed = m["pseudo_id"] != ""
    correct = claimed & (m["pseudo_id"] == m["true_id"])
    applicants = int((m["true_id"] != "").sum())
    return {"claimed": int(claimed.sum()), "correct": int(correct.sum()),
            "success": round(float(correct.sum() / applicants), 4),
            "precision": round(float(correct.sum() / max(claimed.sum(), 1)), 4)}
    # END SOLUTION

# %%
try:
    result = score(links, truth)
except NotImplementedError:
    result = U.reference("lab13_score")
U.keep("lab13_score", result)
print(result)
U.check(result["success"] > 0.9, "more than nine applicants in ten are re-identified by three ordinary fields")

# %% [markdown]
# ## 4 · What the links reveal (5')
#
# A link is not the harm. The harm is what the release says about the named person.

# %%
named = links[links["pseudo_id"] != ""].merge(release, on="pseudo_id").merge(register[["register_id", "full_name"]], on="register_id")
learned = {
    "named people": len(named),
    "on social security": int((named["social_security"] == "yes").sum()),
    "disability in household": int((named["disability_in_household"] == "yes").sum()),
    "declined by the fund": int((named["officer_decision"] == "declined").sum()),
}
print(learned)
print(named[["full_name", "monthly_income_sar", "social_security", "officer_decision"]].head(3))

# %% [markdown]
# ## 5 · Try a coarser join (3')
#
# Replace the birth date by the birth year. The release does not hold a birth year column, so
# derive it on both sides first.

# %%
for df in (release, register):
    df["birth_year"] = df["birth_date"].str[:4]
try:
    coarse = score(link(release, register, ["birth_year", "gender", "postcode"]), truth)
except NotImplementedError:
    coarse = U.reference("lab13_coarse")
U.keep("lab13_coarse", coarse)
print("birth year in place of the date:", coarse)
U.check(coarse["success"] < result["success"], "a coarser join links fewer people")

# %% [markdown]
# ## ✱ Stretch · District in place of postcode
#
# Run `link` on `["birth_date", "gender", "district"]` and score it. Which field does more of the
# identifying here, the date or the postcode?

# %% [markdown]
# ## Check yourself
#
# 1. The release has no names. Why did linking work?
# 2. A claimed link is wrong. Who is harmed?
# 3. Which single change to the release cut the links most in your runs?
#
# <details><summary>Answers</summary>
#
# 1. Birth date, gender and postcode together are unique for almost every applicant, and the register holds all three with names.
# 2. The person in the register, who is now wrongly believed to be on social security or declined.
# 3. Coarsening the birth date to a year: compare the two success rates you printed.
# </details>
#
# **Carry forward.** Lab 1.4 measures this risk without an outside file; Lab 2.1 reruns this attack on the treated release.
