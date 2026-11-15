# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas>=2.2", "opendp>=0.16", "matplotlib>=3.9"]
# ///
# %% [markdown]
# # Lab 2.2 · District counts at three budgets
#
# Day 2 · Session 2 (Differential privacy for counts) · 25 min.
#
# Bashayer wants the number of approved applicants in each of the 59 districts on a public
# dashboard. You release the counts with differential privacy using the OpenDP library, at three
# candidate budgets (epsilon 0.1, 0.5 and 1), repeat each release many times to see the error, plot
# error against budget, and recommend one.
#
# **Reference state.** `data/applicants.csv.gz`. Nothing from another lab.
#
# **Tasks**
# - [ ] 1 · True counts of approved applicants by district (4')
# - [ ] 2 · One noisy release with the library (6')
# - [ ] 3 · Repeat at three budgets (7')
# - [ ] 4 · Plot the error against the budget (5')
# - [ ] 5 · Recommend a budget (3')
# - [ ] ✱ Stretch · Post-process the counts (no negatives, whole numbers) and check that the error does not grow

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
plt = U.plt()
BUDGETS = [0.1, 0.5, 1.0]
RUNS = U.pick(300, 60)

# %% [markdown]
# ## 1 · True counts of approved applicants by district (4')
#
# Each applicant is in one district and is counted at most once. Adding or removing one
# applicant changes one count by one: the **sensitivity** of the whole vector is 1.

# %%
apps = U.load("applicants.csv.gz")
true = (apps[apps["officer_decision"] == "approved"].groupby("district").size()
        .reindex(sorted(apps["district"].unique()), fill_value=0))
counts = [int(v) for v in true]
print(len(counts), "districts · smallest", min(counts), "· largest", max(counts), "· total", sum(counts))

# %% [markdown]
# ## 2 · One noisy release with the library (6')
#
# OpenDP builds a **measurement** from a domain, a distance and a noise scale. For integer counts
# `make_laplace` adds discrete Laplace noise. The scale is sensitivity divided by epsilon, and
# `map(d_in=1)` reports the epsilon the measurement really spends when one person changes.
#
# ✏️ **Exercise** · Write `measurement(eps)`.

# %%
DOMAIN = dp.vector_domain(dp.atom_domain(T=int), size=len(counts))
METRIC = dp.l1_distance(T=int)

def measurement(eps: float):
    # BEGIN SOLUTION
    return dp.m.make_laplace(DOMAIN, METRIC, scale=1.0 / eps)
    # END SOLUTION

# %%
try:
    m = measurement(1.0)
    spent = m.map(d_in=1)
    one = m(counts)
except NotImplementedError:
    print("(safety net: a measurement built by the reference)")
    m = dp.m.make_laplace(DOMAIN, METRIC, scale=1.0)
    spent, one = m.map(d_in=1), m(counts)
print("epsilon spent:", spent)
print(pd.DataFrame({"true": counts[:6], "released": one[:6]}, index=true.index[:6]))
U.check(abs(spent - 1.0) < 1e-6, "the measurement spends exactly the budget it was given")

# %% [markdown]
# ## 3 · Repeat at three budgets (7')
#
# One release shows one draw of the noise. To see the error a budget costs, release many times
# and summarise. (A real dashboard releases once: every release spends the budget again.)
#
# ✏️ **Exercise** · Write `error_table(budgets, runs)`: for each budget, the mean absolute error
# over all districts, the 95th percentile absolute error, and the mean relative error in the ten
# smallest districts.

# %%
SMALL = np.argsort(counts)[:10]

def error_table(budgets, runs) -> pd.DataFrame:
    # BEGIN SOLUTION
    rows = []
    c = np.array(counts)
    for eps in budgets:
        meas = measurement(eps)
        err = np.array([np.array(meas(counts)) - c for _ in range(runs)])
        rows.append({"epsilon": eps, "mae": float(np.abs(err).mean()), "p95_abs": float(np.percentile(np.abs(err), 95)),
                     "small_rel_err": float((np.abs(err[:, SMALL]) / c[SMALL]).mean())})
    return pd.DataFrame(rows).round(4)
    # END SOLUTION

# %%
try:
    errors = error_table(BUDGETS, RUNS)
except NotImplementedError:
    errors = U.reference("lab22_errors")
U.keep("lab22_errors", errors)
print(errors.to_string(index=False))
U.check(errors["mae"].is_monotonic_decreasing, "a larger budget gives a smaller error")
U.check(abs(errors.loc[errors["epsilon"] == 0.1, "mae"].iloc[0] - 10) < 1.5,
        "at epsilon 0.1 the typical error is about 1 / epsilon = 10 applicants")

# %% [markdown]
# ## 4 · Plot the error against the budget (5')
#
# Add a curve over a finer grid: the mean absolute error of discrete Laplace noise is close to
# one over epsilon for these budgets.

# %%
grid = np.round(np.linspace(0.05, 2.0, 40), 3)
try:
    curve = error_table(list(grid), max(RUNS // 10, 10))
except NotImplementedError:
    curve = pd.DataFrame({"epsilon": grid, "mae": 1 / grid, "small_rel_err": (1 / grid) / np.array(counts)[SMALL].mean()})
fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
ax[0].plot(curve["epsilon"], curve["mae"], color="#0f766e")
ax[0].scatter(errors["epsilon"], errors["mae"], color="#c2410c", zorder=3)
ax[0].set(xlabel="epsilon", ylabel="mean absolute error (applicants)", title="All districts")
ax[1].plot(curve["epsilon"], 100 * curve["small_rel_err"], color="#0f766e")
ax[1].scatter(errors["epsilon"], 100 * errors["small_rel_err"], color="#c2410c", zorder=3)
ax[1].set(xlabel="epsilon", ylabel="relative error (%)", title="Ten smallest districts")
fig.tight_layout()
fig.savefig(U.out("lab22") / "error_vs_budget.png", dpi=120)
U.show()

# %% [markdown]
# ## 5 · Recommend a budget (3')
#
# The dashboard's rule of thumb, agreed with Bashayer: in the ten smallest districts the typical
# error must stay under 5%. Pick the smallest budget of the three that meets it.

# %%
meets = errors[errors["small_rel_err"] < 0.05]
recommended = float(meets["epsilon"].min()) if len(meets) else None
print("recommended epsilon per release:", recommended)
U.keep("lab22_recommended", recommended)

# %% [markdown]
# ## ✱ Stretch · Post-processing
#
# Clamp negative counts to zero. Post-processing never spends budget. Does it change the error?

# %%
try:
    noisy = np.array(measurement(0.1)(counts))
except NotImplementedError:
    noisy = np.array(counts)
print("negatives before clamping:", int((noisy < 0).sum()), "· after:", int((np.maximum(noisy, 0) < 0).sum()))

# %% [markdown]
# ## Check yourself
#
# 1. What does epsilon bound?
# 2. Why is the sensitivity of the whole vector 1 and not 59?
# 3. The dashboard is refreshed every month at the recommended epsilon. What is spent in a year?
#
# <details><summary>Answers</summary>
#
# 1. How much any one applicant's presence or absence can change the probability of any released output.
# 2. Each applicant is in exactly one district, so adding one changes one count by one.
# 3. Twelve times the monthly epsilon, by sequential composition (Session 3).
# </details>
#
# **Carry forward.** `artifacts/lab22/error_vs_budget.png` is the LO3 error-against-budget evidence.
