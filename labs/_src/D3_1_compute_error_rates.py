# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas>=2.2", "fairlearn>=0.13"]
# ///
# %% [markdown]
# # Lab 3.1 · Error rates with intervals
#
# Day 3 · Session 1 (Disaggregating errors) · 25 min.
#
# Internal audit asks whether Ahliya misses eligible applicants more often in some groups. You
# have 12,000 applications that Ahliya scored and that a full review then settled. You count the
# errors by gender, region and nationality, attach 95% intervals, slice one intersection, mark the
# cells too small to read, and write one sentence per finding.
#
# **Reference state.** `data/ahliya_scored_test.csv`. Nothing from another lab.
#
# **Tasks**
# - [ ] 1 · Confusion counts by group (6')
# - [ ] 2 · Rates with Wilson intervals (7')
# - [ ] 3 · One intersection (6')
# - [ ] 4 · Mark the cells too small to read (3')
# - [ ] 5 · One sentence per finding (3')
# - [ ] ✱ Stretch · Rebuild the table with Fairlearn's MetricFrame and compare

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

test = U.load("ahliya_scored_test.csv")
THRESHOLD = 0.5
test["pred"] = (test["score"] >= THRESHOLD).astype(int)
test["y"] = test["reviewed_eligible"]
MIN_POS = 30
print(len(test), "reviewed applications ·", int(test["y"].sum()), "eligible ·", int(test["pred"].sum()), "passed by Ahliya")

# %% [markdown]
# ## 1 · Confusion counts by group (6')
#
# For a support decision the two errors are not alike:
#
# | | eligible (review) | not eligible |
# |---|---|---|
# | **passed by Ahliya** | true positive | false positive: support to someone not eligible |
# | **declined by Ahliya** | **false negative: an eligible applicant denied** | true negative |
#
# ✏️ **Exercise** · Write `confusion(df, group)`: one row per value of `group` with `n`, `tp`, `fp`, `fn`, `tn`.

# %%
def confusion(df: pd.DataFrame, group: str) -> pd.DataFrame:
    # BEGIN SOLUTION
    g = df.assign(tp=(df["pred"] == 1) & (df["y"] == 1), fp=(df["pred"] == 1) & (df["y"] == 0),
                  fn=(df["pred"] == 0) & (df["y"] == 1), tn=(df["pred"] == 0) & (df["y"] == 0))
    out = g.groupby(group)[["tp", "fp", "fn", "tn"]].sum().astype(int)
    out.insert(0, "n", out.sum(axis=1))
    return out
    # END SOLUTION

# %%
GROUPS = ["gender", "nationality", "region"]
try:
    conf = {g: confusion(test, g) for g in GROUPS}
except NotImplementedError:
    conf = U.reference("lab31_confusion")
U.keep("lab31_confusion", conf)
print(conf["gender"])
U.check(all(int(c["n"].sum()) == len(test) for c in conf.values()), "every breakdown adds up to 12,000")

# %% [markdown]
# ## 2 · Rates with Wilson intervals (7')
#
# False negative rate (FNR) = fn / (tp + fn): the share of eligible applicants Ahliya declines.
# False positive rate (FPR) = fp / (fp + tn). Attach a 95% Wilson interval to each (`U.wilson`).
#
# ✏️ **Exercise** · Write `rates(c)` from a confusion table.

# %%
def rates(c: pd.DataFrame) -> pd.DataFrame:
    # BEGIN SOLUTION
    out = pd.DataFrame(index=c.index)
    out["eligible"] = c["tp"] + c["fn"]
    out["fnr"] = c["fn"] / out["eligible"]
    out[["fnr_lo", "fnr_hi"]] = [U.wilson(int(k), int(n)) for k, n in zip(c["fn"], out["eligible"])]
    neg = c["fp"] + c["tn"]
    out["fpr"] = c["fp"] / neg
    out[["fpr_lo", "fpr_hi"]] = [U.wilson(int(k), int(n)) for k, n in zip(c["fp"], neg)]
    return out.round(3)
    # END SOLUTION

# %%
try:
    table = {g: rates(conf[g]) for g in GROUPS}
except NotImplementedError:
    table = U.reference("lab31_rates")
U.keep("lab31_rates", table)
for g in GROUPS:
    print(table[g], "\n")
U.check(table["gender"].loc["F", "fnr_lo"] < table["gender"].loc["M", "fnr"] < table["gender"].loc["F", "fnr_hi"],
        "women's and men's false negative rates are within each other's intervals")

# %% [markdown]
# **Look at** the regions. Which region has the highest FNR, and does its interval overlap the
# others'? Qassim stands out; hold that thought for Session 3.

# %% [markdown]
# ## 3 · One intersection (6')
#
# Gender alone looks even, and nationality shows a gap. Slice by both at once.

# %%
test["gender_x_nationality"] = test["gender"] + " | " + test["nationality"]
try:
    inter = rates(confusion(test, "gender_x_nationality"))
except NotImplementedError:
    inter = U.reference("lab31_intersection")
U.keep("lab31_intersection", inter)
print(inter)
U.check(inter["fnr"].idxmax() == "F | Non-Saudi", "non-Saudi women have the highest false negative rate")

# %% [markdown]
# ## 4 · Mark the cells too small to read (3')
#
# A rate from fewer than 30 eligible applicants is reported as "too few to estimate", with its
# count, never as a percentage. Slice region by gender by nationality and count the cells.

# %%
test["cell"] = test["region"] + " | " + test["gender"] + " | " + test["nationality"]
try:
    cells = rates(confusion(test, "cell"))
except NotImplementedError:
    cells = U.reference("lab31_cells")
small = cells[cells["eligible"] < MIN_POS]
print(len(cells), "cells ·", len(small), "with fewer than", MIN_POS, "eligible applicants")
print(small[["eligible", "fnr", "fnr_lo", "fnr_hi"]].head(8))
U.keep("lab31_cells", cells)

# %% [markdown]
# ## 5 · One sentence per finding (3')
#
# One sentence each: the group, the rate with its interval, the comparison, and what you do not
# claim. Example for the intersection:

# %%
r = inter.loc["F | Non-Saudi"]
rest = test[test["gender_x_nationality"] != "F | Non-Saudi"]
rest_fnr = ((rest["pred"] == 0) & (rest["y"] == 1)).sum() / (rest["y"] == 1).sum()
sentence = (f"Ahliya declines {r['fnr']:.0%} of eligible non-Saudi women (95% interval {r['fnr_lo']:.0%} to {r['fnr_hi']:.0%}) "
            f"against {rest_fnr:.0%} of all other eligible applicants; gender alone shows no gap, so the margins understate it.")
print(sentence)
table_all = pd.concat({g: table[g] for g in GROUPS} | {"gender_x_nationality": inter})
table_all.to_csv(U.out("lab31") / "error_rates.csv")

# %% [markdown]
# ## ✱ Stretch · Fairlearn's MetricFrame

# %%
from fairlearn.metrics import MetricFrame, false_negative_rate, false_positive_rate
mf = MetricFrame(metrics={"fnr": false_negative_rate, "fpr": false_positive_rate}, y_true=test["y"], y_pred=test["pred"],
                 sensitive_features=test[["gender", "nationality"]])
print(mf.by_group.round(3))
print("largest FNR difference between groups:", round(float(mf.difference()["fnr"]), 3))

# %% [markdown]
# ## Check yourself
#
# 1. Women and men have nearly equal FNR. Why can non-Saudi women still be declined more often?
# 2. A cell has 12 eligible applicants and an FNR of 50%. What do you write?
# 3. Why is the FNR the error to look at first for this decision?
#
# <details><summary>Answers</summary>
#
# 1. The marginal rates average over subgroups: a gap in a small intersection can vanish in both margins.
# 2. "Too few eligible applicants to estimate (12)", with the interval if you show anything at all.
# 3. A false negative denies support to an eligible applicant: the harm the fund exists to prevent.
# </details>
#
# **Carry forward.** `artifacts/lab31/error_rates.csv` is the core of the audit report (LO5).
