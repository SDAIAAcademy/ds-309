# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 3.3 · Five findings, five types
#
# Day 3 · Session 3 (Bias across the lifecycle) · 25 min.
#
# The audit has five findings. A finding is not yet a diagnosis: two bias types can produce the
# same gap and need different fixes. For each finding you run the check that tells the candidate
# types apart, then name the type from SDAIA's AI Bias Reference Guide and the stage of the AI
# system lifecycle (as the AI Ethics Principles name the stages) where it entered.
#
# **Reference state.** `data/audit_findings.json` and the files each finding names. Nothing from
# another lab.
#
# **Tasks**
# - [ ] 1 · Read the five findings (3')
# - [ ] 2 · Run the evidence check for each (12')
# - [ ] 3 · Map each to a type and a stage (6')
# - [ ] 4 · Check the mapping (4')
# - [ ] ✱ Stretch · Write the sixth finding you would look for next, and its check

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

findings = U.json("audit_findings.json")
for k, f in findings.items():
    print(k, "·", f["finding"])

TYPES = ["Historical Bias", "Measurement Bias", "Labeling Bias", "Evaluation Bias", "Feedback Loop Bias",
         "Sampling Bias", "Aggregation Bias", "Sample Size Bias"]
STAGES = ["Plan and Design", "Prepare Input Data", "Build and Validate", "Deploy and Monitor"]

# %% [markdown]
# ## 1 · Read the five findings (3')
#
# Names in `TYPES` are entries of the national guide; three of them are distractors here. The
# stages are the four of the AI Ethics Principles' lifecycle.

# %% [markdown]
# ## 2 · Run the evidence check for each (12')
#
# Each check is a few lines. Write them in order; each returns the numbers that decide the type.
#
# ✏️ **Exercise F1** · Self-employed: is their *recorded* income wrong, or are they treated
# differently at the same income? Return the median ratio of recorded to verified income, by
# employment.

# %%
audit = U.load("income_audit.csv")
train = U.load("ahliya_train.csv.gz")
test = U.load("ahliya_scored_test.csv")
report = U.json("ahliya_validation_report.json")
deploy = U.load("ahliya_deployment_log.csv")

def check_f1() -> dict:
    # BEGIN SOLUTION
    a = audit.dropna(subset=["monthly_income_sar"])
    return (a["monthly_income_sar"] / a["verified_income_sar"]).groupby(a["employment"]).median().round(3).to_dict()
    # END SOLUTION

# %% [markdown]
# ✏️ **Exercise F2** · Family home: return the officers' approval rate by tenure, before and after
# 1 July 2024 (`application_date < "2024-07-01"`).

# %%
def check_f2() -> pd.DataFrame:
    # BEGIN SOLUTION
    t = train.assign(period=lambda d: (d["application_date"] < "2024-07-01").map({True: "before", False: "after"}),
                     approved=lambda d: d["officer_decision"] == "approved")
    return t.pivot_table(index="tenure", columns="period", values="approved", aggfunc="mean").round(3)
    # END SOLUTION

# %% [markdown]
# ✏️ **Exercise F3** · Qassim: among applications the review found eligible, return the share the
# *officers* declined, for women and men, in the Qassim office and in all other offices.

# %%
def check_f3() -> pd.DataFrame:
    # BEGIN SOLUTION
    e = test[test["reviewed_eligible"] == 1].assign(
        office_group=lambda d: (d["office"] == "Qassim office").map({True: "Qassim", False: "other offices"}),
        declined=lambda d: d["officer_decision"] == "declined")
    return e.pivot_table(index="gender", columns="office_group", values="declined", aggfunc="mean").round(3)
    # END SOLUTION

# %% [markdown]
# ✏️ **Exercise F4** · Validation: return Ahliya's accuracy against the reviewed outcome, at the
# report's threshold, in the report's two regions and in the other eleven.

# %%
def check_f4() -> dict:
    # BEGIN SOLUTION
    ok = (test["score"] >= report["threshold"]).astype(int) == test["reviewed_eligible"]
    urban = test["region"].isin(["Riyadh", "Makkah"])
    return {"reported": report["accuracy"], "reviewed, Riyadh and Makkah": round(float(ok[urban].mean()), 3),
            "reviewed, other regions": round(float(ok[~urban].mean()), 3)}
    # END SOLUTION

# %% [markdown]
# ✏️ **Exercise F5** · Retraining: return the share of applications with a reviewed label, by route.

# %%
def check_f5() -> dict:
    # BEGIN SOLUTION
    return (deploy["label_available"] == "yes").groupby(deploy["route"]).mean().round(3).to_dict()
    # END SOLUTION

# %%
evidence = {}
for name, fn in [("F1", check_f1), ("F2", check_f2), ("F3", check_f3), ("F4", check_f4), ("F5", check_f5)]:
    try:
        evidence[name] = fn()
    except NotImplementedError:
        evidence[name] = U.reference(f"lab33_{name}")
    U.keep(f"lab33_{name}", evidence[name])
    print(f"--- {name}\n{evidence[name]}\n")
U.check(evidence["F1"]["self-employed"] > 1.3 and abs(evidence["F1"]["government"] - 1) < 0.05,
        "F1: only self-employed income is recorded too high")
auto_share = float((deploy["route"] == "auto-declined").mean())
print(f"auto-declined share of applications: {auto_share:.1%}")

# %% [markdown]
# ## 3 · Map each to a type and a stage (6')
#
# Use the evidence, not the finding's wording. Two tests:
#
# - **Historical or labelling?** Historical: the labels followed a rule or a world that has
#   changed. Labelling: the labels were wrong when they were made.
# - **Measurement or labelling?** Measurement: a feature is recorded wrongly. Labelling: the
#   outcome is.
#
# ✏️ **Exercise** · Fill `mapping()`: finding → `(type, stage)`.

# %%
def mapping() -> dict:
    # BEGIN SOLUTION
    return {
        "F1": ("Measurement Bias", "Prepare Input Data"),
        "F2": ("Historical Bias", "Prepare Input Data"),
        "F3": ("Labeling Bias", "Prepare Input Data"),
        "F4": ("Evaluation Bias", "Build and Validate"),
        "F5": ("Feedback Loop Bias", "Deploy and Monitor"),
    }
    # END SOLUTION

# %% [markdown]
# ## 4 · Check the mapping (4')

# %%
try:
    mine = mapping()
except NotImplementedError:
    mine = {k: tuple(v) for k, v in U.reference("lab33_mapping").items()}
U.keep("lab33_mapping", mine)
U.check(all(t in TYPES and s in STAGES for t, s in mine.values()), "every type is from the guide and every stage from the lifecycle")
key_types = {"F1": "Measurement Bias", "F2": "Historical Bias", "F3": "Labeling Bias", "F4": "Evaluation Bias",
             "F5": "Feedback Loop Bias"}
wrong = {k: (mine[k][0], v) for k, v in key_types.items() if mine[k][0] != v}
print("disagreements with the key (yours, key):", wrong or "none")
U.check(not wrong, "each finding carries the type its evidence supports")
pd.DataFrame([(k, findings[k]["finding"], t, s) for k, (t, s) in mine.items()],
             columns=["finding", "text", "type", "stage"]).to_csv(U.out("lab33") / "findings_mapped.csv", index=False)

# %% [markdown]
# ## ✱ Stretch · The sixth finding
#
# Write the finding you would look for next (for example sampling or coverage of non-Saudi
# applicants in small regions) and the check that would confirm it.

# %% [markdown]
# ## Check yourself
#
# 1. F3's gap shows in Ahliya's errors. Why is its type about the officers?
# 2. What would you change first for F1, and would reweighting help?
# 3. Why does F5 not show in today's error rates at all?
#
# <details><summary>Answers</summary>
#
# 1. Ahliya learnt from the officers' decisions; in Qassim those decisions declined eligible women the review later accepted.
# 2. Record net income for the self-employed (or verify it). Reweighting cannot fix a wrong feature.
# 3. It is about the future: auto-declined applications never get a reviewed label, so retraining cannot see its own misses.
# </details>
#
# **Carry forward.** `artifacts/lab33/findings_mapped.csv` goes into the audit report and the model card.
