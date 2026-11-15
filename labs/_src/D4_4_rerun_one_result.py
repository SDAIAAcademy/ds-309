# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas>=2.2", "numpy>=1.26"]
# ///
# %% [markdown]
# # Lab 4.4 · Rerun a peer's result
#
# Day 4 · Session 4 (Review by someone else) · 25 min.
#
# A participant of an earlier cohort handed in a Lab 3.1 result: "Ahliya misses eligible men more
# often than eligible women". You rerun it from their code and the shared data, compare with the
# number they claimed, find the choices in the code that the write-up never mentions, measure how
# much each one moves the result, and record the gaps so that the author could fix them.
#
# **Reference state.** `data/peer/` (the peer's script, README and claimed result) and
# `data/ahliya_scored_test.csv`. Nothing from another lab.
#
# **Tasks**
# - [ ] 1 · Run the peer's code as given (5')
# - [ ] 2 · Compare with the claimed number (4')
# - [ ] 3 · Find the choices that move it (9')
# - [ ] 4 · Record the gaps (5')
# - [ ] 5 · State the corrected result (2')
# - [ ] ✱ Stretch · Swap notebooks with a neighbour and rerun one of their Day 2 or Day 3 results

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

import importlib.util
import numpy as np
import pandas as pd
import yusr as U

spec = importlib.util.spec_from_file_location("peer_lab31", "data/peer/peer_lab31.py")
peer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(peer)
claimed = U.json("peer/peer_results.json")
print(Path("data/peer/README.md").read_text(encoding="utf-8"))

# %% [markdown]
# ## 1 · Run the peer's code as given (5')
#
# Read `data/peer/peer_lab31.py` first, then run it exactly as handed in.

# %%
d = peer.load("data/ahliya_scored_test.csv")
rerun = peer.result(d)
print("rerun:", rerun)
print("interval, run 1:", peer.bootstrap_gap(d), "· run 2:", peer.bootstrap_gap(d))

# %% [markdown]
# ## 2 · Compare with the claimed number (4')

# %%
print("claimed:", {k: claimed[k] for k in ("fnr_women", "fnr_men", "gap")})
same = all(abs(rerun[k] - claimed[k]) < 0.001 for k in ("fnr_women", "fnr_men", "gap"))
U.check(same, "the code reproduces the claimed numbers")

# %% [markdown]
# It reproduces. That is not the end of the review: a result can be reproducible and still rest on
# choices the write-up hides. The two interval runs above already differ, because the bootstrap
# has no seed.
#
# ## 3 · Find the choices that move it (9')
#
# Compare the code with its README and with the course's Lab 3.1. You should find a threshold and
# a filter the README does not mention.
#
# ✏️ **Exercise** · Write `variants(path)`: the peer's `result()` under every combination of
# threshold (the peer's 0.45, Ahliya's documented 0.5) and missing incomes (dropped, kept). Return
# a DataFrame with columns `threshold`, `missing_income`, `rows`, `fnr_women`, `fnr_men`, `gap`.

# %%
def variants(path: str) -> pd.DataFrame:
    # BEGIN SOLUTION
    full = pd.read_csv(path)
    rows = []
    for t in (0.45, 0.5):
        for drop in (True, False):
            df = full[full["monthly_income_sar"].notna()].copy() if drop else full.copy()
            df["pred"] = (df["score"] >= t).astype(int)
            rows.append({"threshold": t, "missing_income": "dropped" if drop else "kept", "rows": len(df)} | peer.result(df))
    return pd.DataFrame(rows)
    # END SOLUTION

# %%
try:
    table = variants("data/ahliya_scored_test.csv")
except NotImplementedError:
    table = U.reference("lab44_variants")
U.keep("lab44_variants", table)
print(table.to_string(index=False))
full = pd.read_csv("data/ahliya_scored_test.csv")
missing = full[full["monthly_income_sar"].isna()]
print(f"\nrows dropped: {len(missing):,}; share of them women: {(missing['gender'] == 'F').mean():.0%} "
      f"(women in all rows: {(full['gender'] == 'F').mean():.0%})")

# %% [markdown]
# **Look at** who the filter drops. Missing income is more common for women (Day 3 found it), and
# applicants without an income are often eligible and declined by the screen, so dropping them
# removes many of the women the model misses. The sign of the gap comes from the filter.
#
# ## 4 · Record the gaps (5')
#
# A gap is useful when the author can act on it: what is undocumented, where in the code, what it
# changes, and what to write.

# %%
def lookup(t, m, col):
    return float(table[(table["threshold"] == t) & (table["missing_income"] == m)][col].iloc[0])

gaps = pd.DataFrame([
    {"gap": "Rows with missing income are dropped", "where": "load(), the notna() filter",
     "effect": f"gap {lookup(0.45, 'dropped', 'gap'):+.3f} with the filter, {lookup(0.45, 'kept', 'gap'):+.3f} without it",
     "fix": "keep them, or state the filter and report how many rows and which groups it removes"},
    {"gap": "Threshold 0.45, not Ahliya's documented 0.5", "where": "THRESH",
     "effect": f"gap {lookup(0.45, 'kept', 'gap'):+.3f} at 0.45, {lookup(0.5, 'kept', 'gap'):+.3f} at 0.5 (all rows)",
     "fix": "use the deployed threshold, or say why another one answers the question"},
    {"gap": "The bootstrap has no seed", "where": "bootstrap_gap()",
     "effect": "the interval changes on every run",
     "fix": "seed it and record the seed and the number of resamples"},
    {"gap": "No versions recorded", "where": "README",
     "effect": "a later pandas or data version could change the rows silently",
     "fix": "record the data file's date or hash and the library versions"},
])
print(gaps.to_string(index=False))
U.check(len(gaps) >= 3 and gaps["effect"].str.contains(r"\d").sum() >= 2,
        "at least three gaps, and the ones that move the number say by how much")
gaps.to_csv(U.out("lab44") / "review_gaps.csv", index=False)

# %% [markdown]
# ## 5 · State the corrected result (2')
#
# On all reviewed applications at the deployed threshold, with a seeded interval.

# %%
d_all = full.copy()
d_all["pred"] = (d_all["score"] >= 0.5).astype(int)
corrected = peer.result(d_all)
rng = np.random.default_rng(U.SEED)
boot = []
for _ in range(200):
    s = d_all.iloc[rng.integers(0, len(d_all), len(d_all))]
    boot.append(peer.result(s)["gap"])
lo, hi = np.percentile(boot, [2.5, 97.5])
statement = (f"On all {len(d_all):,} reviewed applications at Ahliya's threshold of 0.5, the false negative rate is "
             f"{corrected['fnr_women']:.3f} for women and {corrected['fnr_men']:.3f} for men (gap {corrected['gap']:+.3f}, "
             f"95% bootstrap interval {lo:+.3f} to {hi:+.3f}, seed {U.SEED}). The claim that Ahliya misses men more often "
             "does not hold; the gap the audit found is between nationality and gender combined, not gender alone.")
print(statement)
U.check(lo < 0 < hi, "the corrected interval includes zero: no gender gap at the margin")

# %% [markdown]
# ## ✱ Stretch · Swap with a neighbour
#
# Give your Day 2 or Day 3 notebook to a neighbour with only its README. Rerun one of theirs.
# Record the gaps in the same four columns and hand them back.

# %% [markdown]
# ## Check yourself
#
# 1. The code reproduced the claimed numbers. Why was the review not finished there?
# 2. Which single choice flipped the sign of the gap, and why does it fall on women?
# 3. What makes a documentation gap useful to its author?
#
# <details><summary>Answers</summary>
#
# 1. Reproducing shows the code gives the number; it does not show the number answers the question. Undocumented choices did.
# 2. Dropping rows with missing income: more women have no income recorded, and those applicants are often eligible and missed.
# 3. It says where the choice is, how much it moves the result, and what to write or change.
# </details>
#
# **Carry forward.** `artifacts/lab44/review_gaps.csv` is the review record of the LO6 pack; the
# capstone asks a peer to do the same to your release.
