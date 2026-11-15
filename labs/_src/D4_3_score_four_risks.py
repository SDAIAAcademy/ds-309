# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas>=2.2"]
# ///
# %% [markdown]
# # Lab 4.3 · Score four risks
#
# Day 4 · Session 3 (Impact assessment) · 25 min.
#
# The release pack needs an impact assessment. Four risks came out of the week's work. You score
# each on the National AI Risk Management Framework's scales (likelihood 1 to 4, impact 1 to 4,
# level = likelihood × impact), argue each score from the measured evidence, choose a treatment,
# score the residual risk, and name an owner, plus a human reviewer for every risk scored high.
# A register check then tests the assessment.
#
# **Reference state.** `data/risks.json`. Nothing from another lab.
#
# **Tasks**
# - [ ] 1 · Read the four risks and their evidence (4')
# - [ ] 2 · Score likelihood and impact (7')
# - [ ] 3 · Treat and score again (7')
# - [ ] 4 · Name owners and reviewers (3')
# - [ ] 5 · Run the register check (4')
# - [ ] ✱ Stretch · Add a fifth risk from your own audit and score it

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

risks = U.json("risks.json")
for k, r in risks.items():
    print(f"{k} · {r['risk']}\n     evidence: {r['evidence']}\n     affected: {r['affected']}\n")

# %% [markdown]
# ## 1 · Read the four risks and their evidence (4')
#
# The framework's scales, in short:
#
# | Score | Likelihood | Impact |
# |---|---|---|
# | 1 | rare | low: limited, contained quickly |
# | 2 | unlikely | medium: tangible, contained in a reasonable time |
# | 3 | likely | high: substantial, needs a clear organisational response |
# | 4 | almost certain | catastrophic: very severe, wide, possibly irreversible |
#
# Level = likelihood × impact. Bands: 1 to 2 low, 3 to 6 medium, 8 to 12 high, 16 catastrophic.
# Treatments: avoid, mitigate, transfer, accept. Likelihood is argued from exposure, the controls
# in place, how easily the harm happens, and precedents.

# %%
LIKELIHOOD = {1: "rare", 2: "unlikely", 3: "likely", 4: "almost certain"}
IMPACT = {1: "low", 2: "medium", 3: "high", 4: "catastrophic"}
TREATMENTS = {"avoid", "mitigate", "transfer", "accept"}

def band(level: int) -> str:
    return "low" if level <= 2 else "medium" if level <= 6 else "high" if level <= 12 else "catastrophic"

# %% [markdown]
# ## 2 · Score likelihood and impact (7') and 3 · Treat and score again (7')
#
# ✏️ **Exercise** · Write `assess()`: for each risk, `likelihood`, `impact`, `why` (one sentence
# from the evidence), `treatment`, `control` (what is done), `residual_likelihood`,
# `residual_impact`.

# %%
def assess() -> dict:
    # BEGIN SOLUTION
    return {
        "R1": {"likelihood": 3, "impact": 3, "why": "Public lists share birth date, gender and postcode, and the untreated extract linked 99.2% of the register's applicants.",
               "treatment": "mitigate", "control": "k of five with region and five-year bands, a sharing agreement banning linkage, destruction after 24 months",
               "residual_likelihood": 1, "residual_impact": 3},
        "R2": {"likelihood": 4, "impact": 3, "why": "Measured now: 30% of eligible non-Saudi women and 65% of eligible self-employed applicants are declined by the screen.",
               "treatment": "mitigate", "control": "officer review of every decline, verified net income for the self-employed, group thresholds if approved",
               "residual_likelihood": 2, "residual_impact": 3},
        "R3": {"likelihood": 3, "impact": 2, "why": "Monthly refreshes are already requested and small districts carry a 3.1% error at epsilon 0.5.",
               "treatment": "mitigate", "control": "a yearly budget ledger signed by the data protection officer, and error margins printed on the dashboard",
               "residual_likelihood": 2, "residual_impact": 2},
        "R4": {"likelihood": 2, "impact": 3, "why": "Only a regeneration with a different setting copies rows, and the leaf-one setting copied 92.8% of them.",
               "treatment": "mitigate", "control": "the leakage tests of Lab 2.4 as a release gate for every regeneration",
               "residual_likelihood": 1, "residual_impact": 3},
    }
    # END SOLUTION

# %%
try:
    scores = assess()
except NotImplementedError:
    scores = U.reference("lab43_scores")
U.keep("lab43_scores", scores)

# %% [markdown]
# ## 4 · Name owners and reviewers (3')
#
# Every risk has an owner. Every risk whose level is high or catastrophic before treatment also
# names a human reviewer who signs the residual risk; at Yusr that is Wiam Al-Mutairi of internal
# audit.

# %%
OWNERS = {"R1": "Yahya Al-Qahtani, data protection officer", "R2": "Bashayer Al-Otaibi, director of eligibility and support",
          "R3": "Yahya Al-Qahtani, data protection officer", "R4": "Malak Al-Harbi, data scientist"}
register = []
for k, s in scores.items():
    lvl, res = s["likelihood"] * s["impact"], s["residual_likelihood"] * s["residual_impact"]
    register.append({"risk": k, "L": s["likelihood"], "I": s["impact"], "level": lvl, "band": band(lvl),
                     "treatment": s["treatment"], "residual": res, "residual_band": band(res), "owner": OWNERS[k],
                     "reviewer": "Wiam Al-Mutairi, internal audit" if lvl >= 8 else "", "why": s["why"], "control": s["control"]})
register = pd.DataFrame(register)
print(register[["risk", "L", "I", "level", "band", "treatment", "residual", "residual_band", "reviewer"]].to_string(index=False))

# %% [markdown]
# ## 5 · Run the register check (4')

# %%
def check_register(reg: pd.DataFrame) -> list:
    p = []
    for _, r in reg.iterrows():
        if not (1 <= r["L"] <= 4 and 1 <= r["I"] <= 4):
            p.append(f"{r['risk']}: a score outside 1 to 4")
        if r["band"] != band(r["L"] * r["I"]):
            p.append(f"{r['risk']}: band does not match the level")
        if r["treatment"] not in TREATMENTS:
            p.append(f"{r['risk']}: unknown treatment")
        if r["residual"] > r["level"]:
            p.append(f"{r['risk']}: residual above the initial level")
        if r["level"] >= 8 and not r["reviewer"]:
            p.append(f"{r['risk']}: high risk without a human reviewer")
        if r["treatment"] == "accept" and r["band"] in ("high", "catastrophic"):
            p.append(f"{r['risk']}: a high risk accepted without treatment")
        if len(str(r["why"]).split()) < 8 or not any(ch.isdigit() for ch in str(r["why"])):
            p.append(f"{r['risk']}: the score is not argued from a measured number")
    return p

problems = check_register(register)
print(problems or "the register passes")
U.check(not problems, "every risk is scored, treated, owned and argued from evidence")
register.to_csv(U.out("lab43") / "risk_register.csv", index=False)

# %% [markdown]
# **Look at** R2. Its residual is still medium: the treatment lowers the likelihood, not the
# impact, because a wrongly declined applicant is harmed the same way. Say so in the assessment
# rather than lowering the impact to make the table look better.

# %% [markdown]
# ## ✱ Stretch · A fifth risk
#
# Add the feedback loop of Lab 3.3 (auto-declined applications never reviewed) as R5, score it,
# and rerun the check.

# %% [markdown]
# ## Check yourself
#
# 1. Why is R2's likelihood 4 and not 3?
# 2. Which risks need a named human reviewer, and why those?
# 3. A colleague lowers R2's impact to 2 after adding officer review. What do you say?
#
# <details><summary>Answers</summary>
#
# 1. The harm is happening now and was measured: it is almost certain without effective controls.
# 2. R1 and R2, whose levels (9 and 12) are in the high band; the course entry and the framework's escalation both call for a human decision there.
# 3. Review lowers the chance that a wrong score becomes a wrong decision (likelihood); for the applicant who is still wrongly declined, the harm is unchanged.
# </details>
#
# **Carry forward.** `artifacts/lab43/risk_register.csv` is the impact assessment of the LO6 pack.
