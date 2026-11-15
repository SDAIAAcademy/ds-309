# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
# %% [markdown]
# # Lab 4.1 · The datasheet of the release
#
# Day 4 · Session 1 (Datasheets) · 25 min.
#
# The k-anonymous research extract of Day 2 is ready to go to Waad Al-Shehri. Before it leaves,
# it needs a datasheet: what is in it, how it was made, what was done to protect the applicants,
# what risk remains, and what it must not be used for. You fill it from the release log, never
# from memory, run a completeness check that also traces every number back to the log, and name
# what a reader still cannot rerun.
#
# **Reference state.** `data/release_log.json` (the log of the Day 2 release). Nothing from
# another lab; if you kept your own Lab 2.1 numbers, you may put them in a copy of the log.
#
# **Tasks**
# - [ ] 1 · Read the release log (4')
# - [ ] 2 · Fill the composition and collection sections (7')
# - [ ] 3 · Fill the de-identification and residual risk sections (7')
# - [ ] 4 · Run the completeness check (5')
# - [ ] 5 · Name what a reader still cannot rerun (2')
# - [ ] ✱ Stretch · Add the distribution terms for the researcher: licence, retention and destruction

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

import json
import re
import yusr as U

log = U.json("release_log.json")

# %% [markdown]
# ## 1 · Read the release log (4')
#
# The log was written while the release was made: every decision, number and approver.

# %%
print(json.dumps(log, indent=1)[:1500])

# %% [markdown]
# ## 2 · Fill the composition and collection sections (7')
#
# The datasheet has the sections of Gebru and colleagues' "Datasheets for Datasets", plus two a
# de-identified release needs: **De-identification** and **Residual risk**.
#
# ✏️ **Exercise** · Write `motivation_composition_collection(log)`: a dict with the sections
# `Motivation`, `Composition` and `Collection`, each a short paragraph built from the log.

# %%
def motivation_composition_collection(log: dict) -> dict:
    # BEGIN SOLUTION
    return {
        "Motivation": f"Released for {log['requested_by']}. Purpose: {log['purpose']}. Approved by {log['approved_by']}.",
        "Composition": (f"{log['risk_after']['records']:,} records, one per application. Fields: "
                        f"{', '.join(log['fields_released'])}. No direct identifier is included. "
                        f"Removed: {', '.join(log['fields_removed'])}."),
        "Collection": (f"Drawn from the {log['source']}. The officer decision is the historical decision, not a reviewed "
                       "outcome, and income is as recorded, which overstates self-employed income."),
    }
    # END SOLUTION

# %% [markdown]
# ## 3 · Fill the de-identification and residual risk sections (7')
#
# ✏️ **Exercise** · Write `protection(log)`: the sections `De-identification`, `Residual risk`,
# `Uses` and `Maintenance`. State every number with its meaning, and only numbers from the log.

# %%
def protection(log: dict) -> dict:
    # BEGIN SOLUTION
    b, a, t = log["risk_before"], log["risk_after"], log["treatment"]
    return {
        "De-identification": (f"Before treatment {b['unique']:,} records were unique on {b['measured_on']}, "
                              f"and a linkage test re-identified {b['linkage_success']:.1%} of applicants in a public register. "
                              f"Birth was generalised to a {t['birth']} and place to the {t['place']}; {t['suppressed']} records "
                              f"were suppressed ({t['suppression_rule']}). After treatment k = {a['k']} and the linkage test "
                              f"claimed {a['linkage_claimed']} links. The largest change in a key statistic was "
                              f"{log['utility']['largest_change_pct']}% ({log['utility']['largest_change_statistic']})."),
        "Residual risk": ("The extract is still personal data and stays Restricted. Remaining risks: "
                          + "; ".join(log["residual_risks"]) + "."),
        "Uses": "For the stated research question only. Not for decisions about individuals, and not for linking with other files.",
        "Maintenance": f"Release of {log['date']}; reproducible from {log['code']}. Questions to the data protection officer.",
    }
    # END SOLUTION

# %%
try:
    sections = motivation_composition_collection(log) | protection(log)
except NotImplementedError:
    sections = U.reference("lab41_sections")
U.keep("lab41_sections", sections)
datasheet = "# Datasheet: " + log["release"] + "\n\n" + "\n\n".join(f"## {k}\n\n{v}" for k, v in sections.items()) + "\n"
print(datasheet)

# %% [markdown]
# ## 4 · Run the completeness check (5')
#
# Three rules: every required section is there and says something; nothing is left as a gap
# marker; and every number in the De-identification section can be found in the log.

# %%
REQUIRED = ["Motivation", "Composition", "Collection", "De-identification", "Residual risk", "Uses", "Maintenance"]

def log_numbers(obj) -> set:
    found = set()
    if isinstance(obj, dict):
        for v in obj.values():
            found |= log_numbers(v)
    elif isinstance(obj, list):
        for v in obj:
            found |= log_numbers(v)
    elif isinstance(obj, bool):
        pass
    elif isinstance(obj, (int, float)):
        found |= {round(float(obj), 4), round(float(obj) * 100, 1)}
    elif isinstance(obj, str):
        found |= {round(float(x), 4) for x in re.findall(r"\d+(?:\.\d+)?", obj)}
    return found

def check_datasheet(sections: dict, log: dict) -> list:
    problems = [f"missing or empty: {s}" for s in REQUIRED if len(sections.get(s, "").split()) < 5]
    problems += [f"gap marker in {s}" for s, v in sections.items() if re.search(r"\?\?\?|to be completed|\bTBD\b", v)]
    known = log_numbers(log)
    for raw in re.findall(r"-?\d[\d,]*(?:\.\d+)?", sections.get("De-identification", "")):
        n = round(float(raw.replace(",", "")), 4)
        if n not in known and abs(n) not in known:
            problems.append(f"number not in the log: {raw}")
    return problems

problems = check_datasheet(sections, log)
print(problems or "complete, and every number traces to the log")
U.check(not problems, "the datasheet is complete and traceable")
(U.out("lab41") / "DATASHEET.md").write_text(datasheet, encoding="utf-8")

# %% [markdown]
# **Look at** what the check catches: change one number in your De-identification text (type
# 290 suppressed records) and run the check again.

# %% [markdown]
# ## 5 · Name what a reader still cannot rerun (2')
#
# A reviewer who receives the extract and this datasheet: what can they not reproduce, and why
# is that acceptable or not?

# %%
cannot_rerun = [
    "the treatment from the source table, which stays inside the fund (acceptable: the code and seed are named)",
    "the linkage test, which needs the register and the truth key (the fund keeps both for audit)",
    "the study code mapping, which only the data protection officer holds (by design)",
]
print("\n".join("- " + c for c in cannot_rerun))

# %% [markdown]
# ## ✱ Stretch · Distribution terms
#
# Add a `Distribution` section from `log["agreement"]`, and say who may receive the extract and
# what happens at the end of the retention period.

# %% [markdown]
# ## Check yourself
#
# 1. Why must a de-identified extract still have a datasheet?
# 2. The datasheet says "k = 5". What must stand next to it?
# 3. Why fill the datasheet from the log rather than from your notebook's last run?
#
# <details><summary>Answers</summary>
#
# 1. It is still personal data, and the recipient needs to know what was done, what remains and what it must not be used for.
# 2. The quasi-identifiers it was measured on, the suppression count, and the residual risk k does not cover.
# 3. The log records the run that was approved and released; a later run may differ.
# </details>
#
# **Carry forward.** `artifacts/lab41/DATASHEET.md` is the first document of the LO6 pack.
