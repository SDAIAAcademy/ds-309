# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas>=2.2", "numpy>=2.0"]
# ///
# %% [markdown]
# # Lab 3.2 · Two criteria in conflict
#
# Day 3 · Session 2 (Criteria that conflict) · 25 min.
#
# Three fairness criteria each sound reasonable: pass women and men at the same rate (demographic
# parity), miss eligible women and men at the same rate (equal opportunity), and be right equally
# often when passing them (predictive parity). Eligible women are more common than eligible men in
# the reviewed data, so the criteria cannot all hold at once. You measure the three gaps, force
# one criterion, watch the others move, and choose the criterion that fits the decision.
#
# **Reference state.** `data/ahliya_scored_test.csv`. Nothing from another lab.
#
# **Tasks**
# - [ ] 1 · Three gaps at the current threshold (6')
# - [ ] 2 · Equalise selection rates and watch the other gaps (8')
# - [ ] 3 · Equalise false negative rates instead (6')
# - [ ] 4 · Choose and justify (5')
# - [ ] ✱ Stretch · Find the thresholds that equalise predictive parity and read the other gaps

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

import numpy as np
import pandas as pd
import yusr as U

test = U.load("ahliya_scored_test.csv")
test["y"] = test["reviewed_eligible"]
print((test.groupby("gender")["y"].mean()).round(3).rename("base rate (eligible share)"))

# %% [markdown]
# ## 1 · Three gaps at the current threshold (6')
#
# | Criterion | Equal across groups | Gap reported |
# |---|---|---|
# | Demographic parity | selection rate: share passed | women minus men |
# | Equal opportunity | false negative rate among the eligible | women minus men |
# | Predictive parity | precision: share of the passed who are eligible | women minus men |
#
# ✏️ **Exercise** · Write `metrics(df, thresholds)`: per gender, the selection rate, the FNR and
# the precision when group `g` is passed at `score >= thresholds[g]`; and the three gaps.

# %%
def metrics(df: pd.DataFrame, thresholds: dict) -> dict:
    # BEGIN SOLUTION
    rows = {}
    for g, d in df.groupby("gender"):
        p = d["score"] >= thresholds[g]
        rows[g] = {"selection": float(p.mean()), "fnr": float((~p[d["y"] == 1]).mean()),
                   "precision": float(d.loc[p, "y"].mean())}
    t = pd.DataFrame(rows).T.round(4)
    gaps = (t.loc["F"] - t.loc["M"]).round(4).to_dict()
    return {"table": t, "gaps": gaps}
    # END SOLUTION

# %%
SAME = {"F": 0.5, "M": 0.5}
try:
    base = metrics(test, SAME)
except NotImplementedError:
    base = U.reference("lab32_base")
U.keep("lab32_base", base)
print(base["table"])
print("gaps (women minus men):", base["gaps"])
U.check(abs(base["gaps"]["fnr"]) < 0.01, "at one threshold, equal opportunity holds almost exactly")
U.check(base["gaps"]["selection"] > 0.05, "and demographic parity does not")

# %% [markdown]
# ## 2 · Equalise selection rates and watch the other gaps (8')
#
# Pick a threshold per gender so that both are passed at the overall rate of the current
# threshold.
#
# ✏️ **Exercise** · Write `thresholds_for_selection(df, rate)`: for each gender, the score above
# which a share `rate` of that gender lies.

# %%
def thresholds_for_selection(df: pd.DataFrame, rate: float) -> dict:
    # BEGIN SOLUTION
    return {g: float(np.quantile(d["score"], 1 - rate)) for g, d in df.groupby("gender")}
    # END SOLUTION

# %%
overall_rate = float((test["score"] >= 0.5).mean())
try:
    t_dp = thresholds_for_selection(test, overall_rate)
except NotImplementedError:
    t_dp = U.reference("lab32_t_dp")
U.keep("lab32_t_dp", t_dp)
try:
    dp_result = metrics(test, t_dp)
except NotImplementedError:
    dp_result = U.reference("lab32_dp")
U.keep("lab32_dp", dp_result)
print("thresholds:", {k: round(v, 3) for k, v in t_dp.items()})
print(dp_result["table"])
print("gaps:", dp_result["gaps"])
U.check(abs(dp_result["gaps"]["selection"]) < 0.01, "selection rates are now equal")
U.check(dp_result["gaps"]["fnr"] > 0.05, "and eligible women are now missed more often than eligible men")

# %% [markdown]
# **Look at** the FNR gap. To pass women at men's rate, Ahliya must decline eligible women it
# would have passed: their need is higher, so equal selection means unequal misses.

# %% [markdown]
# ## 3 · Equalise false negative rates instead (6')
#
# Set each gender's threshold so that its FNR equals a target: the overall FNR at 0.5.

# %%
def thresholds_for_fnr(df: pd.DataFrame, fnr: float) -> dict:
    return {g: float(np.quantile(d.loc[d["y"] == 1, "score"], fnr)) for g, d in df.groupby("gender")}

overall_fnr = float((test.loc[test["y"] == 1, "score"] < 0.5).mean())
t_eo = thresholds_for_fnr(test, overall_fnr)
try:
    eo_result = metrics(test, t_eo)
except NotImplementedError:
    eo_result = U.reference("lab32_eo")
U.keep("lab32_eo", eo_result)
print("thresholds:", {k: round(v, 3) for k, v in t_eo.items()})
print(eo_result["table"])
print("gaps:", eo_result["gaps"])

# %% [markdown]
# ## 4 · Choose and justify (5')
#
# The AI Ethics Principles ask that the fairness metric be chosen from the effect of the decision
# and the harm of correct and incorrect predictions. Write which criterion Ahliya should be held
# to, why, and what it costs.

# %%
choice = {
    "criterion": "equal opportunity (equal false negative rates among eligible applicants)",
    "why": "the harmful error is declining an eligible applicant; groups differ in need, so equal selection would deny eligible women",
    "cost": f"selection rates stay unequal by {100 * eo_result['gaps']['selection']:+.1f} points because need differs",
}
print(pd.Series(choice))
U.out("lab32").joinpath("criteria.csv").write_text(
    pd.concat({"same threshold": base["table"], "equal selection": dp_result["table"], "equal FNR": eo_result["table"]})
    .to_csv(), encoding="utf-8")

# %% [markdown]
# ## ✱ Stretch · Predictive parity
#
# Search per-gender thresholds that make the precision equal. Which other gap opens?

# %% [markdown]
# ## Check yourself
#
# 1. Why can demographic parity and equal opportunity not both hold here?
# 2. A colleague says "the model does not use gender, so it is fair". What do the numbers say?
# 3. When would demographic parity be the right criterion?
#
# <details><summary>Answers</summary>
#
# 1. The base rates differ: 60% of women and 49% of men are eligible. Equal misses imply unequal selection, and the reverse.
# 2. Gender is absent, yet selection differs by 9 points and, at equal selection, misses would differ: fairness is measured on outcomes, not inputs.
# 3. When the true need is believed equal across groups and the measured difference comes from biased labels, or when the decision allocates a fixed opportunity that should be shared.
# </details>
#
# **Carry forward.** The criterion you chose is the one Lab 3.4 mitigates towards and the model card of Lab 4.2 states.
