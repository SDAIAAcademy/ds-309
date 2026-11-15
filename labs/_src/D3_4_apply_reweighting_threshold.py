# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas>=2.2", "scikit-learn>=1.6"]
# ///
# %% [markdown]
# # Lab 3.4 · Reweighting and a threshold change
#
# Day 3 · Session 4 (Mitigation and its cost) · 25 min.
#
# The audit's largest gap is the false negative rate of non-Saudi women. You try two mitigations
# against the criterion chosen in Session 2 (equal false negative rates): reweighting the training
# data before the model is fitted, and a separate threshold per group after it. You measure each on
# reviewed applications it was not tuned on, then recommend one, with its cost.
#
# **Reference state.** `data/ahliya_train.csv.gz` and `data/ahliya_scored_test.csv`. Nothing from
# another lab: the model is refitted here from the supplied pipeline.
#
# **Tasks**
# - [ ] 1 · The baseline: accuracy and gaps (4')
# - [ ] 2 · Reweight the training data and retrain (8')
# - [ ] 3 · Group thresholds on the baseline model (7')
# - [ ] 4 · One comparison table and a recommendation (6')
# - [ ] ✱ Stretch · Repeat the threshold change for the intersection of Day 3 Session 1

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

train = U.load("ahliya_train.csv.gz")
test = U.load("ahliya_scored_test.csv")
for df in (train, test):
    df["group"] = df["gender"] + " | " + df["nationality"]
train["y"] = (train["officer_decision"] == "approved").astype(int)
test["y"] = test["reviewed_eligible"]
# tune on one half of the reviewed applications, report on the other half
rng = np.random.default_rng(U.SEED)
tune_mask = rng.random(len(test)) < 0.5
tune, evaluate = test[tune_mask].copy(), test[~tune_mask].copy()
print(len(train), "training rows ·", len(tune), "reviewed rows to tune ·", len(evaluate), "to report")

# %% [markdown]
# ## 1 · The baseline: accuracy and gaps (4')
#
# `report(df, scores, thresholds)` is supplied: accuracy against the review, FNR and selection
# rate by group, and the largest FNR gap between groups.

# %%
def report(df, scores, thresholds) -> dict:
    t = df["group"].map(thresholds) if isinstance(thresholds, dict) else thresholds
    p = scores >= t
    by = pd.DataFrame({g: {"fnr": float((~p[(df["group"] == g) & (df["y"] == 1)]).mean()),
                           "selection": float(p[df["group"] == g].mean())} for g in sorted(df["group"].unique())}).T
    return {"accuracy": round(float((p.astype(int) == df["y"]).mean()), 4),
            "fnr_gap": round(float(by["fnr"].max() - by["fnr"].min()), 4), "by_group": by.round(4)}

baseline = U.ahliya_model().fit(U.ahliya_frame(train, banded=True), train["y"])
s_base = pd.Series(baseline.predict_proba(U.ahliya_frame(evaluate))[:, 1], index=evaluate.index)
base = report(evaluate, s_base, 0.5)
print("accuracy", base["accuracy"], "· FNR gap", base["fnr_gap"])
print(base["by_group"])

# %% [markdown]
# ## 2 · Reweight the training data and retrain (8')
#
# Reweighting (Kamiran and Calders) gives each training row the weight
# `P(group) × P(label) / P(group, label)`: combinations that are rarer than independence would
# predict count more, so the model no longer learns that a group goes with a label.
#
# ✏️ **Exercise** · Write `weights(df)`.

# %%
def weights(df: pd.DataFrame) -> pd.Series:
    # BEGIN SOLUTION
    pg = df["group"].value_counts(normalize=True)
    py = df["y"].value_counts(normalize=True)
    pgy = df.groupby(["group", "y"]).size() / len(df)
    joint = pgy.reindex(pd.MultiIndex.from_arrays([df["group"], df["y"]])).to_numpy()
    return pd.Series(pg[df["group"]].to_numpy() * py[df["y"]].to_numpy() / joint, index=df.index)
    # END SOLUTION

# %%
try:
    w = weights(train)
except NotImplementedError:
    print("(safety net: the reference weights)")
    ref = U.reference("lab34_weights")
    w = (train["group"] + "|" + train["y"].astype(str)).map(ref)
U.keep("lab34_weights", {f"{g}|{y}": float(w[(train["group"] == g) & (train["y"] == y)].iloc[0])
                         for g in train["group"].unique() for y in (0, 1)})
reweighted = U.ahliya_model().fit(U.ahliya_frame(train, banded=True), train["y"],
                                  logisticregression__sample_weight=w.to_numpy())
s_rw = pd.Series(reweighted.predict_proba(U.ahliya_frame(evaluate))[:, 1], index=evaluate.index)
rw = report(evaluate, s_rw, 0.5)
print("accuracy", rw["accuracy"], "· FNR gap", rw["fnr_gap"])
U.check(abs(float(w.mean()) - 1) < 0.01, "the weights average 1, so the training set keeps its size")

# %% [markdown]
# ## 3 · Group thresholds on the baseline model (7')
#
# On the tuning half, find for each group the threshold at which its FNR equals the baseline's
# overall FNR. Then report on the other half.
#
# ✏️ **Exercise** · Write `group_thresholds(df, scores, target_fnr)`.

# %%
def group_thresholds(df: pd.DataFrame, scores: pd.Series, target_fnr: float) -> dict:
    # BEGIN SOLUTION
    return {g: float(np.quantile(scores[(df["group"] == g) & (df["y"] == 1)], target_fnr))
            for g in sorted(df["group"].unique())}
    # END SOLUTION

# %%
s_tune = pd.Series(baseline.predict_proba(U.ahliya_frame(tune))[:, 1], index=tune.index)
target = float((s_tune[tune["y"] == 1] < 0.5).mean())
try:
    thr = group_thresholds(tune, s_tune, target)
except NotImplementedError:
    thr = U.reference("lab34_thresholds")
U.keep("lab34_thresholds", thr)
print("target FNR", round(target, 3), "· thresholds", {k: round(v, 3) for k, v in thr.items()})
th = report(evaluate, s_base, thr)
print("accuracy", th["accuracy"], "· FNR gap", th["fnr_gap"])
U.check(th["fnr_gap"] < base["fnr_gap"], "the group thresholds narrow the FNR gap on applications they were not tuned on")

# %% [markdown]
# ## 4 · One comparison table and a recommendation (6')

# %%
comparison = pd.DataFrame({
    "baseline": {"accuracy": base["accuracy"], "fnr_gap": base["fnr_gap"],
                 "fnr non-Saudi women": base["by_group"].loc["F | Non-Saudi", "fnr"]},
    "reweighting": {"accuracy": rw["accuracy"], "fnr_gap": rw["fnr_gap"],
                    "fnr non-Saudi women": rw["by_group"].loc["F | Non-Saudi", "fnr"]},
    "group thresholds": {"accuracy": th["accuracy"], "fnr_gap": th["fnr_gap"],
                         "fnr non-Saudi women": th["by_group"].loc["F | Non-Saudi", "fnr"]},
}).T
print(comparison)
comparison.to_csv(U.out("lab34") / "mitigation_comparison.csv")
U.keep("lab34_comparison", comparison)

# %% [markdown]
# Write the recommendation for Bashayer in three sentences: which mitigation, what it costs in
# accuracy and in other groups' rates, and what must be fixed at the source. A threshold that
# depends on gender and nationality uses protected attributes at decision time: say who must
# approve that, and why the root cause (Lab 3.3) is the lasting fix.

# %%
recommendation = (
    f"Apply group thresholds as an interim measure: the FNR gap falls from {base['fnr_gap']:.1%} to {th['fnr_gap']:.1%} "
    f"with accuracy {th['accuracy']:.1%} (baseline {base['accuracy']:.1%}); non-Saudi women are still missed at "
    f"{th['by_group'].loc['F | Non-Saudi', 'fnr']:.1%}, because their threshold rests on few eligible applicants. "
    f"Reweighting moved the gap only to "
    f"{rw['fnr_gap']:.1%}, because the gap comes from missing and mis-recorded income, not from the label balance. "
    "Using gender and nationality in the threshold needs the data protection officer's and legal approval, and the lasting "
    "fix is to verify incomes before scoring.")
print(recommendation)

# %% [markdown]
# ## ✱ Stretch · Another slice
#
# Repeat the threshold change with `group` defined as region (or self-employed against the rest).
# How many thresholds would the fund have to maintain, and how many of them rest on fewer than 30
# eligible applicants?

# %% [markdown]
# ## Check yourself
#
# 1. Why tune the thresholds on one half and report on the other?
# 2. Why did reweighting barely help here?
# 3. What does a group threshold cost besides accuracy?
#
# <details><summary>Answers</summary>
#
# 1. Thresholds tuned and measured on the same rows overstate how well the gap closes.
# 2. The gap comes from features (missing and mis-recorded income), not from the balance of labels by group.
# 3. Explicit use of protected attributes at decision time, which needs legal approval and must be explained to applicants.
# </details>
#
# **Carry forward.** `artifacts/lab34/mitigation_comparison.csv` and the recommendation complete the audit report (LO5).
