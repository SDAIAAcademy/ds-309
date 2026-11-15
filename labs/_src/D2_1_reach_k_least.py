# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 2.1 · Reach k of five
#
# Day 2 · Session 1 (Generalisation and suppression) · 25 min.
#
# You treat release A, the research extract that Lab 1.3 re-identified, until every record hides
# among at least five on its quasi-identifiers. You climb two hierarchies (birth date and place),
# suppress the few records that are still exposed, and measure what Waad's analysis loses on three
# key statistics. Then you rerun the linkage attack on the treated release.
#
# **Reference state.** `data/release_a_research_extract.csv.gz` and `data/public_register.csv`.
# Nothing from another lab: the linkage function is supplied.
#
# **Tasks**
# - [ ] 1 · Three key statistics before treatment (5')
# - [ ] 2 · Generalise birth date and postcode step by step (8')
# - [ ] 3 · Suppress what is still below five (4')
# - [ ] 4 · The three statistics after treatment (5')
# - [ ] 5 · Rerun the linkage (3')
# - [ ] ✱ Stretch · Find a second treatment that keeps the district, and compare its cost

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

import itertools
import pandas as pd
import yusr as U

release = U.load("release_a_research_extract.csv.gz")
register = U.load("public_register.csv")
truth = U.load("reference/linkage_truth.csv").fillna("")
REGION_OF = dict(zip(release["postcode"], release["region"])) | dict(zip(release["district"], release["region"]))
DISTRICT_OF = dict(zip(release["postcode"], release["district"]))
K = 5
print(len(release), "records; target k =", K)

# %% [markdown]
# ## 1 · Three key statistics before treatment (5')
#
# Waad's question needs these three. They are the utility you must protect.
#
# | Statistic | Computed as |
# |---|---|
# | S1 | approval rate by gender |
# | S2 | mean monthly income by region |
# | S3 | mean household size by nationality |

# %%
def key_stats(df: pd.DataFrame) -> dict:
    return {
        "S1": (df["officer_decision"] == "approved").groupby(df["gender"]).mean().round(4).to_dict(),
        "S2": df.groupby("region")["monthly_income_sar"].mean().round(0).to_dict(),
        "S3": df.groupby("nationality")["household_size"].mean().round(3).to_dict(),
    }

before = key_stats(release)
print(before["S1"], before["S3"])

# %% [markdown]
# ## 2 · Generalise birth date and postcode step by step (8')
#
# Two hierarchies:
#
# | Level | birth | place |
# |---|---|---|
# | 0 | birth date | postcode |
# | 1 | birth year | district |
# | 2 | five-year band | region |
# | 3 | ten-year band | |
#
# ✏️ **Exercise** · Write `generalise(df, b, p)`: a copy of `df` with two new columns, `birth` at
# level `b` and `place` at level `p`. Bands start at 1950 (1950-1954, 1955-1959 ...).

# %%
def generalise(df: pd.DataFrame, b: int, p: int) -> pd.DataFrame:
    # BEGIN SOLUTION
    out = df.copy()
    year = out["birth_date"].str[:4].astype(int)
    if b == 0:
        out["birth"] = out["birth_date"]
    elif b == 1:
        out["birth"] = year.astype(str)
    else:
        width = 5 if b == 2 else 10
        lo = 1950 + ((year - 1950) // width) * width
        out["birth"] = lo.astype(str) + "-" + (lo + width - 1).astype(str)
    out["place"] = out[["postcode", "district", "region"][p]]
    return out
    # END SOLUTION

# %% [markdown]
# Now search the lattice: every pair of levels, scored by the share of records in classes below
# five. A tool like ARX searches the same lattice with a utility measure.

# %%
QI = ["birth", "gender", "nationality", "place"]
rows = []
try:
    for b, p in itertools.product(range(4), range(3)):
        s = U.classes(generalise(release, b, p), QI)
        rows.append({"birth": b, "place": p, "below_5": int((s < K).sum()), "share": round(float((s < K).mean()), 4)})
    lattice = pd.DataFrame(rows)
except NotImplementedError:
    lattice = U.reference("lab21_lattice")
U.keep("lab21_lattice", lattice)
print(lattice.pivot(index="birth", columns="place", values="below_5"))

# %% [markdown]
# Choose the least general node where at most 1% of records would have to be suppressed.

# %%
ok = lattice[lattice["share"] <= 0.01].copy()
ok["generality"] = ok["birth"] + ok["place"]
best = ok.sort_values(["generality", "share"]).iloc[0]
B, P = int(best["birth"]), int(best["place"])
print("chosen node: birth level", B, "place level", P, "·", int(best["below_5"]), "records to suppress")

# %% [markdown]
# ## 3 · Suppress what is still below five (4')
#
# ✏️ **Exercise** · Write `treat(df, b, p)`: generalise, drop the records whose class is below
# five, and keep only the columns the study needs (no birth date, postcode or district).

# %%
KEEP = ["pseudo_id", "birth", "gender", "nationality", "place", "household_size", "employment",
        "monthly_income_sar", "disability_in_household", "social_security", "officer_decision"]

def treat(df: pd.DataFrame, b: int, p: int) -> pd.DataFrame:
    # BEGIN SOLUTION
    g = generalise(df, b, p)
    s = U.classes(g, QI)
    return g[s >= K][KEEP].reset_index(drop=True)
    # END SOLUTION

# %%
try:
    treated = treat(release, B, P)
except NotImplementedError:
    print("(safety net: the reference treatment, built with the helper)")
    g = U.generalise(release, B, P)
    treated = g[U.classes(g, QI) >= K][KEEP].reset_index(drop=True)
k_after = int(U.classes(treated, QI).min())
suppressed = len(release) - len(treated)
print(len(treated), "records kept ·", suppressed, "suppressed · k =", k_after)
U.check(k_after >= K, "every record hides among at least five")
U.check(suppressed <= 0.01 * len(release), "at most 1% of records suppressed")
U.keep("lab21_summary", {"birth_level": B, "place_level": P, "kept": len(treated), "suppressed": suppressed, "k": k_after})

# %% [markdown]
# ## 4 · The three statistics after treatment (5')
#
# The treated release has `place` in place of the region. Map it back to the region (postcode and
# district maps are public knowledge) and recompute the statistics.

# %%
t = treated.copy()
t["region"] = t["place"].map(lambda v: REGION_OF.get(v, v))
after = key_stats(t)
change = pd.DataFrame({
    "statistic": ["S1 approval, women", "S1 approval, men", "S2 income, Northern Borders", "S2 income, Riyadh",
                  "S3 household, Non-Saudi", "S3 household, Saudi"],
    "before": [before["S1"]["F"], before["S1"]["M"], before["S2"]["Northern Borders"], before["S2"]["Riyadh"],
               before["S3"]["Non-Saudi"], before["S3"]["Saudi"]],
    "after": [after["S1"]["F"], after["S1"]["M"], after["S2"]["Northern Borders"], after["S2"]["Riyadh"],
              after["S3"]["Non-Saudi"], after["S3"]["Saudi"]],
})
change["change_%"] = ((change["after"] / change["before"] - 1) * 100).round(2)
print(change.to_string(index=False))
worst = float(change["change_%"].abs().max())
U.keep("lab21_change", change)
U.check(worst < 5, "no key statistic moved by 5% or more")

# %% [markdown]
# **Look at** which statistic moved most. Suppression removes the rarest records, and rare records
# are mostly non-Saudi applicants in small regions: the cost lands on the smallest groups.

# %% [markdown]
# ## 5 · Rerun the linkage (3')
#
# The attacker generalises the register the same way and joins again.

# %%
def link_success(rel, reg, on):
    sizes = rel.groupby(on).size().rename("matches").reset_index()
    first = rel.groupby(on)["pseudo_id"].first().rename("cand").reset_index()
    j = reg.merge(sizes, on=on, how="left").merge(first, on=on, how="left").merge(truth, on="register_id")
    hit = (j["matches"] == 1) & (j["cand"] == j["pseudo_id"])
    return int((j["matches"] == 1).sum()), int(hit.sum())

try:
    gen = generalise
    gen(release.head(1), B, P)
except NotImplementedError:
    gen = U.generalise
reg = gen(register.assign(postcode=register["postcode"], district=register["postcode"].map(DISTRICT_OF),
                                 region=register["postcode"].map(REGION_OF), nationality=""), B, P)
claimed, correct = link_success(treated.assign(nationality=""), reg, ["birth", "gender", "place"])
print("claimed links:", claimed, "· correct:", correct, "of 3,000 applicants in the register")
U.keep("lab21_linkage", {"claimed": claimed, "correct": correct})
U.check(claimed == 0, "no register record matches a single treated record")

# %% [markdown]
# ## ✱ Stretch · Keep the district
#
# Keep `place` at level 1 (district) and coarsen the birth to the ten-year band. How many records
# must be suppressed now, and which key statistic moves most?

# %%
alt = lattice[(lattice["place"] == 1) & (lattice["birth"] == 3)]
print(alt)

# %% [markdown]
# ## Check yourself
#
# 1. Why search the lattice from the least general node upwards?
# 2. Suppression removed under 1% of records. Why can it still matter?
# 3. The linkage now finds no unique match. Is the release anonymous?
#
# <details><summary>Answers</summary>
#
# 1. Every step up the hierarchy costs detail; the lowest node that meets the target keeps the most.
# 2. The suppressed records are not random: they are the rare combinations, so small groups lose most.
# 3. Not by that alone: classes of five can still share a sensitive value (Lab 1.4 stretch), and another outside file could hold other fields.
# </details>
#
# **Carry forward.** The node, the suppression count and the statistics are the release log that the datasheet of Lab 4.1 is filled from (a reference log is supplied there).
