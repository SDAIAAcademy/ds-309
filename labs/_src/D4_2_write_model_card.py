# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 4.2 · The model card of Ahliya
#
# Day 4 · Session 2 (Model cards) · 25 min.
#
# Ahliya has no model card: only a validation report that the audit could not reproduce. You
# write the card a reviewer needs: what the model is and is for, what it must not be used for,
# its results broken down by group with intervals, the fairness criterion it is held to, the
# mitigation and its cost, and its limits. A check tests the card before it is filed.
#
# **Reference state.** `data/ahliya_scored_test.csv`, `data/ahliya_validation_report.json` and
# the Day 3 reference results in `data/reference/`. Nothing from another lab.
#
# **Tasks**
# - [ ] 1 · Model details and intended use (5')
# - [ ] 2 · The disaggregated results table (8')
# - [ ] 3 · Fairness criterion, mitigation and cost (5')
# - [ ] 4 · Limits and out-of-scope uses (4')
# - [ ] 5 · Run the card check (3')
# - [ ] ✱ Stretch · Write a one-paragraph summary of the card for applicants

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
test["pred"] = (test["score"] >= 0.5).astype(int)
test["gender_x_nationality"] = test["gender"] + ", " + test["nationality"]
validation = U.json("ahliya_validation_report.json")
mitigation = U.saved("lab34_comparison")
MIN_POS = 30

# %% [markdown]
# ## 1 · Model details and intended use (5')
#
# The sections follow Mitchell and colleagues' "Model Cards for Model Reporting".

# %%
card = {
    "Model details": (f"Ahliya {validation['version']}, a logistic regression on 12 application features, owned by the "
                      "eligibility and support directorate; built by Anmar Al-Ghamdi. Threshold 0.5."),
    "Intended use": ("Ranks housing support applications for an officer's review. Every decision is an officer's; "
                     "a score below the threshold must not decline an application without review."),
}

# %% [markdown]
# ## 2 · The disaggregated results table (8')
#
# ✏️ **Exercise** · Write `results_table(df, groups)`: one row per group value with `eligible`,
# `fnr`, its interval (`fnr_lo`, `fnr_hi`), `fpr`, and a column `note` that says "too few to
# estimate" when there are fewer than 30 eligible applicants (and the rate is then left empty).

# %%
def results_table(df: pd.DataFrame, groups: list) -> pd.DataFrame:
    # BEGIN SOLUTION
    rows = []
    for g in groups:
        for v, d in df.groupby(g):
            pos, neg = d[d["reviewed_eligible"] == 1], d[d["reviewed_eligible"] == 0]
            fn, n = int((pos["pred"] == 0).sum()), len(pos)
            lo, hi = U.wilson(fn, n)
            small = n < MIN_POS
            rows.append({"attribute": g, "group": v, "eligible": n,
                         "fnr": None if small else round(fn / n, 3), "fnr_lo": None if small else round(lo, 3),
                         "fnr_hi": None if small else round(hi, 3),
                         "fpr": round(float((neg["pred"] == 1).mean()), 3) if len(neg) else None,
                         "note": "too few to estimate" if small else ""})
    return pd.DataFrame(rows)
    # END SOLUTION

# %%
GROUPS = ["gender", "nationality", "gender_x_nationality", "region"]
try:
    results = results_table(test, GROUPS)
except NotImplementedError:
    results = U.reference("lab42_results")
U.keep("lab42_results", results)
print(results.to_string(index=False))
overall_acc = float((test["pred"] == test["reviewed_eligible"]).mean())
card["Metrics"] = ("False negative rate (eligible applicants declined) and false positive rate, by group, with 95% Wilson "
                   f"intervals, against the reviewed outcome of 12,000 applications. Accuracy against that outcome: {overall_acc:.1%}. "
                   f"The validation report's {validation['accuracy']:.1%} was measured against officers' decisions in two regions "
                   "and is not used here.")
card["Quantitative analyses"] = U.md_table(results)

# %% [markdown]
# ## 3 · Fairness criterion, mitigation and cost (5')

# %%
base, thr = mitigation.loc["baseline"], mitigation.loc["group thresholds"]
card["Fairness"] = (
    "Held to equal opportunity: equal false negative rates across groups, because the harmful error is declining an "
    f"eligible applicant. Largest gap between gender and nationality groups: {base['fnr_gap']:.1%}. "
    f"Group thresholds reduce it to {thr['fnr_gap']:.1%} at the same accuracy; they use gender and nationality and need "
    "approval. Reweighting did not help. The lasting fix is verified income.")

# %% [markdown]
# ## 4 · Limits and out-of-scope uses (4')
#
# ✏️ **Exercise** · Write `limits()`: a dict with `Out-of-scope uses` (a list of at least two) and
# `Caveats` (a paragraph naming the bias types found on Day 3).

# %%
def limits() -> dict:
    # BEGIN SOLUTION
    return {
        "Out-of-scope uses": ["declining an application without an officer's review",
                              "scoring applications for any other support programme",
                              "ranking applicants against each other for a fixed budget"],
        "Caveats": ("Trained on officers' historical decisions, not reviewed outcomes. Known biases: measurement bias in "
                    "self-employed income, historical bias against family-home applicants, labelling bias in one office, "
                    "evaluation bias in the original validation, and a feedback loop through auto-declines. Rates for "
                    "groups with fewer than 30 eligible applicants are not estimated."),
    }
    # END SOLUTION

# %%
try:
    lim = limits()
except NotImplementedError:
    lim = U.reference("lab42_limits")
U.keep("lab42_limits", lim)
card["Out-of-scope uses"] = "\n".join("- " + u for u in lim["Out-of-scope uses"])
card["Caveats"] = lim["Caveats"]

# %% [markdown]
# ## 5 · Run the card check (3')

# %%
REQUIRED = ["Model details", "Intended use", "Metrics", "Quantitative analyses", "Fairness", "Out-of-scope uses", "Caveats"]

def check_card(card: dict, results: pd.DataFrame) -> list:
    problems = [f"missing: {s}" for s in REQUIRED if len(str(card.get(s, "")).split()) < 5]
    if not (results["attribute"] == "gender_x_nationality").any():
        problems.append("no intersectional rows")
    shown = results[results["note"] == ""]
    if shown[["fnr_lo", "fnr_hi"]].isna().any().any():
        problems.append("a reported rate without an interval")
    if results[(results["eligible"] < MIN_POS) & results["fnr"].notna()].shape[0]:
        problems.append("a rate reported for a group below the minimum")
    if len(lim["Out-of-scope uses"]) < 2:
        problems.append("fewer than two out-of-scope uses")
    return problems

problems = check_card(card, results)
print(problems or "the card passes")
U.check(not problems, "the model card is complete")
text = "# Model card: Ahliya\n\n" + "\n\n".join(f"## {k}\n\n{v}" for k, v in card.items()) + "\n"
(U.out("lab42") / "MODEL_CARD.md").write_text(text, encoding="utf-8")
print(text[:1200])

# %% [markdown]
# ## ✱ Stretch · For applicants
#
# Write one paragraph, in plain words, that an applicant could read: what the score is used for,
# that an officer decides, and how to ask for a review.

# %% [markdown]
# ## Check yourself
#
# 1. Why does the card report accuracy against the reviewed outcome and not the validation report's figure?
# 2. Why does the table include gender by nationality when gender alone shows no gap?
# 3. Which out-of-scope use matters most given the feedback-loop finding?
#
# <details><summary>Answers</summary>
#
# 1. The report measured agreement with officers in two regions; the reviewed outcome measures being right.
# 2. The largest gap is in that intersection and would be hidden by the margins.
# 3. Declining without review: it creates the auto-declines that never get a label.
# </details>
#
# **Carry forward.** `artifacts/lab42/MODEL_CARD.md` is the second document of the LO6 pack.
