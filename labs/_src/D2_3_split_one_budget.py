# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas>=2.2", "opendp>=0.16"]
# ///
# %% [markdown]
# # Lab 2.3 · Split one budget over four queries
#
# Day 2 · Session 3 (Budgets and composition) · 25 min.
#
# Yahya has approved a total privacy budget of epsilon = 1 for this year's public statistics from
# the applicant table. Four queries share it. You work out each query's sensitivity, measure the
# errors of an equal split, design a split by need, check with the library that the ledger adds up
# to the budget, and write the justification Yahya will sign.
#
# **Reference state.** `data/applicants.csv.gz`. Nothing from another lab.
#
# **Tasks**
# - [ ] 1 · The four queries and their sensitivities (5')
# - [ ] 2 · An equal split and its errors (6')
# - [ ] 3 · A split by need (7')
# - [ ] 4 · Check that the ledger adds up to the budget (4')
# - [ ] 5 · Justify the allocation (3')
# - [ ] ✱ Stretch · Work out what the same budget buys when the four queries are asked every month

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
import opendp.prelude as dp
import yusr as U

dp.enable_features("contrib")
TOTAL = 1.0
RUNS = U.pick(300, 60)
apps = U.load("applicants.csv.gz")

# %% [markdown]
# ## 1 · The four queries and their sensitivities (5')
#
# | Query | Released | One applicant changes it by at most |
# |---|---|---|
# | Q1 | applicants per region (13 counts) | 1 in one count: the regions are disjoint |
# | Q2 | mean monthly income, clamped to 0 to 30,000 riyals | a sum by 30,000 and a count by 1 |
# | Q3 | approved applicants per district (59 counts) | 1 in one count |
# | Q4 | mean household size, clamped to 1 to 12 | a sum by 12 and a count by 1 |
#
# A mean is released as a noisy sum over a noisy count, each with half the query's budget.
# **Clamping** is what makes the sum's sensitivity finite: without bounds, one applicant with an
# enormous income could move the sum by any amount.

# %%
q1 = [int(v) for v in apps.groupby("region").size()]
q3 = [int(v) for v in apps[apps["officer_decision"] == "approved"].groupby("district").size()]
inc = apps["monthly_income_sar"].dropna().astype(float).tolist()
hh = apps["household_size"].astype(float).tolist()
TRUE = {"Q1": np.array(q1), "Q2": float(np.clip(inc, 0, 30000).mean()), "Q3": np.array(q3), "Q4": float(np.clip(hh, 1, 12).mean())}
print({k: (v if np.isscalar(v) else f"{len(v)} counts") for k, v in TRUE.items()})

# %% [markdown]
# ## 2 · An equal split and its errors (6')
#
# The measurements are built for you. Read `release`, then write the exercise below it.

# %%
def counts_meas(n, eps):
    return dp.m.make_laplace(dp.vector_domain(dp.atom_domain(T=int), size=n), dp.l1_distance(T=int), scale=1.0 / eps)

SUM2, N2 = float(np.clip(inc, 0, 30000).sum()), len(inc)
SUM4, N4 = float(np.clip(hh, 1, 12).sum()), len(hh)

def mean_meas(hi, eps):
    """Noise for a clamped sum (one applicant moves it by at most `hi`) and for a count (by at most 1)."""
    s = dp.m.make_laplace(dp.atom_domain(T=float, nan=False), dp.absolute_distance(T=float), scale=hi / (eps / 2))
    c = dp.m.make_laplace(dp.atom_domain(T=int), dp.absolute_distance(T=int), scale=1.0 / (eps / 2))
    return s, c

def release(split: dict) -> dict:
    """One release of the four queries under `split`; returns values and the epsilon each measurement spends."""
    m1, m3 = counts_meas(len(q1), split["Q1"]), counts_meas(len(q3), split["Q3"])
    s2, c2 = mean_meas(30000.0, split["Q2"])
    s4, c4 = mean_meas(12.0, split["Q4"])
    values = {"Q1": np.array(m1(q1)), "Q2": s2(SUM2) / max(c2(N2), 1), "Q3": np.array(m3(q3)), "Q4": s4(SUM4) / max(c4(N4), 1)}
    spent = {"Q1": m1.map(1), "Q2": s2.map(30000.0) + c2.map(1), "Q3": m3.map(1), "Q4": s4.map(12.0) + c4.map(1)}
    return {"values": values, "spent": spent}

# %% [markdown]
# ✏️ **Exercise** · Write `rel_errors(split, runs)`: release `runs` times and return, per query,
# the mean relative error (for Q1 and Q3 averaged over their counts).

# %%
def rel_errors(split: dict, runs: int) -> dict:
    # BEGIN SOLUTION
    acc = {q: [] for q in TRUE}
    for _ in range(runs):
        v = release(split)["values"]
        for q in TRUE:
            acc[q].append(float(np.mean(np.abs(v[q] - TRUE[q]) / np.abs(TRUE[q]))))
    return {q: round(float(np.mean(a)), 5) for q, a in acc.items()}
    # END SOLUTION

# %%
EQUAL = {q: TOTAL / 4 for q in TRUE}
try:
    equal_err = rel_errors(EQUAL, RUNS)
except NotImplementedError:
    equal_err = U.reference("lab23_equal")
U.keep("lab23_equal", equal_err)
print("equal split, mean relative error:", equal_err)

# %% [markdown]
# **Look at** the spread. One query's error is hundreds of times another's under the same
# epsilon: the large means barely notice the noise, the small district counts do.

# %% [markdown]
# ## 3 · A split by need (7')
#
# A query's relative error falls as one over its epsilon. So give each query a share of the budget
# proportional to its error at epsilon = 1: that equalises the relative errors.
#
# ✏️ **Exercise** · Write `by_need(base)`, where `base` is the error of each query at epsilon 1.

# %%
def by_need(base: dict) -> dict:
    # BEGIN SOLUTION
    total = sum(base.values())
    return {q: TOTAL * e / total for q, e in base.items()}
    # END SOLUTION

# %%
try:
    base = rel_errors({q: 1.0 for q in TRUE}, RUNS)
    NEED = by_need(base)
    need_err = rel_errors(NEED, RUNS)
except NotImplementedError:
    ref = U.reference("lab23_need")
    NEED, need_err = ref["split"], ref["errors"]
U.keep("lab23_need", {"split": NEED, "errors": need_err})
table = pd.DataFrame({"equal eps": EQUAL, "equal err": equal_err, "need eps": NEED, "need err": need_err}).round(4)
print(table)
U.check(max(need_err.values()) < max(equal_err.values()), "the worst query is better off under the split by need")

# %% [markdown]
# ## 4 · Check that the ledger adds up to the budget (4')
#
# The library, not your arithmetic, says what each measurement spends. Sequential composition:
# the four queries touch the same people, so their epsilons add. Parallel composition: the 13
# region counts touch disjoint people, so Q1 spends its epsilon once, not 13 times.

# %%
ledger = release(NEED)["spent"]
print({q: round(v, 6) for q, v in ledger.items()}, "total", round(sum(ledger.values()), 6))
U.keep("lab23_ledger", ledger)
U.check(abs(sum(ledger.values()) - TOTAL) < 1e-6, "the four queries spend the budget of 1 and no more")

# %% [markdown]
# ## 5 · Justify the allocation (3')
#
# Write two sentences for Yahya: which query gets most of the budget and why, and what the
# largest relative error is under your split.

# %%
justification = (f"Q3 receives {NEED['Q3']:.2f} of the budget because its 59 small counts are the most sensitive "
                 f"to noise; under this split every query's mean relative error is at most {max(need_err.values()):.2%}.")
print(justification)

# %% [markdown]
# ## ✱ Stretch · Monthly
#
# If the four queries are released every month under the same yearly budget, each release gets
# a twelfth. By how much does the worst error grow?

# %%
monthly = {q: e / 12 for q, e in NEED.items()}
try:
    print("worst error per monthly release:", max(rel_errors(monthly, max(RUNS // 4, 10)).values()))
except NotImplementedError:
    print("write rel_errors first")

# %% [markdown]
# ## Check yourself
#
# 1. Why does Q1 cost its epsilon once although it releases 13 numbers?
# 2. Why must income be clamped before it is summed?
# 3. A colleague releases Q3 again next week "with the same epsilon". What has the fund spent?
#
# <details><summary>Answers</summary>
#
# 1. Parallel composition: each applicant is in one region, so each person affects one count.
# 2. Without bounds the sum's sensitivity is unbounded, and no finite noise covers it.
# 3. The Q3 epsilon twice: sequential composition adds the two releases.
# </details>
#
# **Carry forward.** The split, the ledger and the justification go into the release log of Day 4.
