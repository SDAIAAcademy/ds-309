# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas>=2.2", "scikit-learn>=1.6"]
# ///
# %% [markdown]
# # Lab 2.4 · Test a synthetic extract
#
# Day 2 · Session 4 (Synthetic data and leakage) · 25 min.
#
# The fund wants a realistic file for a hackathon. You generate a synthetic extract column by
# column with decision trees (the sequential method that synthpop made popular), at two settings
# of the trees. For each you measure utility (marginals, and a model trained on synthetic rows and
# tested on real ones) and leakage (exact copies, distance to the closest record, and a
# membership-inference test), then write the release recommendation.
#
# **Reference state.** `data/release_a_research_extract.csv.gz`. Nothing from another lab: the
# generator is supplied.
#
# **Tasks**
# - [ ] 1 · Fit the generator at two settings (6')
# - [ ] 2 · Utility: marginals and a model trained on synthetic rows (6')
# - [ ] 3 · Distance to the closest record (6')
# - [ ] 4 · Membership inference (4')
# - [ ] 5 · Release recommendation (3')
# - [ ] ✱ Stretch · Plant one rare combination and see whether the generator reproduces it

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
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.neighbors import NearestNeighbors
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
import yusr as U

N = U.pick(8000, 3000)
COLS = ["age", "gender", "nationality", "region", "household_size", "employment", "monthly_income_sar",
        "disability_in_household", "social_security", "officer_decision"]
NUMERIC = ["age", "household_size", "monthly_income_sar"]
raw = U.load("release_a_research_extract.csv.gz").dropna(subset=["monthly_income_sar"])
raw["age"] = 2026 - raw["birth_date"].str[:4].astype(int)
shuffled = raw[COLS].sample(frac=1, random_state=U.SEED).reset_index(drop=True)
train, holdout = shuffled.iloc[:N].reset_index(drop=True), shuffled.iloc[N:2 * N].reset_index(drop=True)
print(len(train), "training rows (members) ·", len(holdout), "holdout rows (non-members)")

# %% [markdown]
# ## 1 · Fit the generator at two settings (6')
#
# The generator, supplied: the first column is drawn from its observed values; each next column
# is drawn from a tree fitted on the columns before it. A synthetic row falls into a leaf of that
# tree, and the value is taken from a training row in the same leaf. `leaf` is the smallest number
# of training rows a leaf may hold.

# %%
def codes(df, ref):
    out = pd.DataFrame(index=df.index)
    for c in df.columns:
        out[c] = df[c] if c in NUMERIC else pd.Categorical(df[c], categories=sorted(ref[c].unique())).codes
    return out

def synthesise(real: pd.DataFrame, leaf: int, n: int, seed: int = U.SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    syn = pd.DataFrame({COLS[0]: rng.choice(real[COLS[0]].to_numpy(), n)})
    for i, col in enumerate(COLS[1:], start=1):
        prev = COLS[:i]
        Tree = DecisionTreeRegressor if col in NUMERIC else DecisionTreeClassifier
        tree = Tree(min_samples_leaf=leaf, random_state=seed).fit(codes(real[prev], real), codes(real[[col]], real)[col])
        real_leaf = tree.apply(codes(real[prev], real))
        donors = pd.Series(real[col].to_numpy()).groupby(real_leaf).apply(lambda s: s.to_numpy())
        syn_leaf = tree.apply(codes(syn[prev], real))
        syn[col] = [rng.choice(donors[l]) for l in syn_leaf]
    return syn

SETTINGS = {"leaf=1": 1, "leaf=200": 200}
synth = {name: synthesise(train, leaf, len(train)) for name, leaf in SETTINGS.items()}
print(synth["leaf=200"].head())

# %% [markdown]
# ## 2 · Utility: marginals and a model trained on synthetic rows (6')
#
# Two measures. **Marginal distance**: for each categorical column, the total variation distance
# between real and synthetic shares (0 is identical, 1 is disjoint), averaged. **Train on
# synthetic, test on real**: a model that predicts the officer's decision, trained on synthetic
# rows and scored on the real holdout, against the same model trained on real rows.
#
# ✏️ **Exercise** · Write `utility(syn)`, returning `tvd` and `auc_tstr`.

# %%
CATS = [c for c in COLS if c not in NUMERIC]

def design(df):
    x = pd.get_dummies(df[[c for c in COLS if c != "officer_decision"]], columns=[c for c in CATS if c != "officer_decision"])
    x["monthly_income_sar"] = np.log1p(x["monthly_income_sar"])
    return x

def tstr_auc(fit_on: pd.DataFrame) -> float:
    xa, xh = design(fit_on).align(design(holdout), join="outer", axis=1, fill_value=0)
    model = LogisticRegression(max_iter=2000).fit(xa.astype(float), fit_on["officer_decision"] == "approved")
    return float(roc_auc_score(holdout["officer_decision"] == "approved", model.predict_proba(xh.astype(float))[:, 1]))

def utility(syn: pd.DataFrame) -> dict:
    # BEGIN SOLUTION
    tvd = np.mean([0.5 * (train[c].value_counts(normalize=True)
                          .subtract(syn[c].value_counts(normalize=True), fill_value=0).abs().sum()) for c in CATS])
    return {"tvd": round(float(tvd), 4), "auc_tstr": round(tstr_auc(syn), 4)}
    # END SOLUTION

# %%
try:
    util = {name: utility(s) for name, s in synth.items()}
except NotImplementedError:
    util = U.reference("lab24_utility")
U.keep("lab24_utility", util)
auc_real = round(tstr_auc(train), 4)
print("trained on real rows: AUC", auc_real)
print(pd.DataFrame(util).T)

# %% [markdown]
# ## 3 · Distance to the closest record (6')
#
# For every synthetic row, find the closest training row and the closest holdout row (numeric
# columns scaled, categorical columns one-hot). A generator that has not memorised its training
# rows is about as close to unseen rows as to the rows it learnt from.
#
# ✏️ **Exercise** · Write `leakage(syn)`: the share of synthetic rows that are exact copies of a
# training row, the same share against the holdout (the baseline), and the share of synthetic rows
# closer to the training set than to the holdout.

# %%
def embed(df):
    x = pd.get_dummies(df[COLS], columns=CATS).astype(float)
    for c in NUMERIC:
        x[c] = (x[c] - train[c].mean()) / train[c].std()
    return x

def nearest(a: pd.DataFrame, b: pd.DataFrame) -> np.ndarray:
    xa, xb = embed(a).align(embed(b), join="outer", axis=1, fill_value=0)
    return NearestNeighbors(n_neighbors=1).fit(xb.to_numpy()).kneighbors(xa.to_numpy())[0][:, 0]

def leakage(syn: pd.DataFrame) -> dict:
    # BEGIN SOLUTION
    d_train, d_hold = nearest(syn, train), nearest(syn, holdout)
    return {"copies_train": round(float((d_train == 0).mean()), 4), "copies_holdout": round(float((d_hold == 0).mean()), 4),
            "closer_to_train": round(float((d_train < d_hold).mean()), 4)}
    # END SOLUTION

# %%
try:
    leak = {name: leakage(s) for name, s in synth.items()}
except NotImplementedError:
    leak = U.reference("lab24_leakage")
U.keep("lab24_leakage", leak)
print(pd.DataFrame(leak).T)
U.check(leak["leaf=1"]["copies_train"] > 5 * max(leak["leaf=1"]["copies_holdout"], 0.001),
        "with leaves of one row the generator copies its training rows")

# %% [markdown]
# ## 4 · Membership inference (4')
#
# The attacker holds a real record and asks: was this person in the training data? A simple
# attack scores each real record by how close the nearest synthetic row is. If members score
# higher than non-members, membership leaks. AUC 0.5 is a coin toss.

# %%
def mia_auc(syn: pd.DataFrame) -> float:
    d_mem, d_non = nearest(train, syn), nearest(holdout, syn)
    y = np.r_[np.ones(len(d_mem)), np.zeros(len(d_non))]
    return round(float(roc_auc_score(y, -np.r_[d_mem, d_non])), 4)

mia = {name: mia_auc(s) for name, s in synth.items()}
print("membership-inference AUC:", mia)
U.keep("lab24_mia", mia)
U.check(mia["leaf=1"] > mia["leaf=200"], "the over-fitted generator leaks membership more")

# %% [markdown]
# ## 5 · Release recommendation (3')
#
# The fund's release rule for synthetic files: copies no more than twice the holdout baseline (with a floor of 0.1%),
# membership-inference AUC below 0.55, and a train-on-synthetic AUC within 0.05 of the real one.

# %%
report = pd.DataFrame({name: {**util[name], **leak[name], "mia_auc": mia[name]} for name in synth}).T
report["release"] = ((report["copies_train"] <= 2 * report["copies_holdout"].clip(lower=0.001))
                     & (report["mia_auc"] < 0.55) & (report["auc_tstr"] >= auc_real - 0.05))
print(report)
report.to_csv(U.out("lab24") / "utility_leakage_report.csv")
U.keep("lab24_report", report)
U.check(bool(report.loc["leaf=200", "release"]) and not bool(report.loc["leaf=1", "release"]),
        "only the generator with leaves of two hundred passes the release rule")

# %% [markdown]
# ## ✱ Stretch · A rare combination
#
# Add five training rows for a 74-year-old non-Saudi applicant in Al-Bahah with a household of
# eleven, regenerate at both settings, and count how often that combination appears.

# %% [markdown]
# ## Check yourself
#
# 1. The leaf=1 file has the best utility. Why is that a warning and not good news?
# 2. Why compare copies of training rows with copies of holdout rows instead of with zero?
# 3. Does passing these tests make the synthetic file differentially private?
#
# <details><summary>Answers</summary>
#
# 1. It is good because it copies: a copy has perfect utility and no privacy.
# 2. Coarse data repeats naturally; only copies beyond what unseen rows show are leakage.
# 3. No. These are empirical tests against one attack. A guarantee needs a generator trained with differential privacy.
# </details>
#
# **Carry forward.** `artifacts/lab24/utility_leakage_report.csv` is the LO4 evidence.
