# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas>=2.2", "numpy>=2.0", "scikit-learn>=1.6"]
# ///
"""Write the synthetic data of Yusr Housing Support Fund into labs/data/ (fixed seed, same files every run).

    cd labs
    uv run python prepare_data.py

Everything is invented. No row describes a real person. Identifiers carry the marker SYN so that
nobody mistakes them for real ones. The planted problems are listed in solutions/answer_key.md.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import roc_auc_score

SEED = 309
HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
N = 60_000
N_TEST = 12_000

REGIONS = [  # name, code, share, districts
    ("Riyadh", "RYD", 0.26, 8), ("Makkah", "MKH", 0.25, 8), ("Eastern", "EST", 0.15, 7),
    ("Madinah", "MDN", 0.07, 5), ("Qassim", "QSM", 0.05, 4), ("Asir", "ASR", 0.06, 5),
    ("Tabuk", "TBK", 0.03, 3), ("Hail", "HAL", 0.02, 3), ("Northern Borders", "NBR", 0.01, 3),
    ("Jazan", "JZN", 0.05, 4), ("Najran", "NJR", 0.02, 3), ("Al-Bahah", "BAH", 0.015, 3),
    ("Al-Jouf", "JOF", 0.015, 3),
]
FIRST_F = ["Amal", "Asma", "Dalal", "Fatimah", "Ghadah", "Hanan", "Hind", "Huda", "Jawaher", "Khadijah",
           "Latifah", "Lulu", "Maha", "Mashael", "Mona", "Nada", "Nouf", "Nourah", "Reem", "Sarah",
           "Shahad", "Wafa", "Zainab", "Abeer", "Areej", "Bodour", "Eman", "Hessah", "Maryam", "Rana"]
FIRST_M = ["Abdullah", "Ahmed", "Ali", "Bader", "Fahad", "Faisal", "Hamad", "Hassan", "Ibrahim", "Khalid",
           "Majed", "Mansour", "Mohammed", "Nasser", "Omar", "Saad", "Saleh", "Sami", "Sultan", "Turki",
           "Waleed", "Yousef", "Ziyad", "Adel", "Bandar", "Fawaz", "Hatem", "Jaber", "Mazen", "Nawaf"]
FAMILY = ["Al-Anazi", "Al-Asiri", "Al-Balawi", "Al-Dosari", "Al-Enezi", "Al-Faifi", "Al-Ghamdi", "Al-Hajri",
          "Al-Harbi", "Al-Jahdali", "Al-Juhani", "Al-Khaldi", "Al-Maliki", "Al-Mutairi", "Al-Nefaie",
          "Al-Omari", "Al-Qahtani", "Al-Rashidi", "Al-Saedi", "Al-Shammari", "Al-Shehri", "Al-Subaie",
          "Al-Tamimi", "Al-Zahrani", "Al-Yami", "Al-Hazmi", "Al-Sahli", "Al-Otaibi", "Al-Shahrani", "Al-Mansour"]


def districts():
    rows = []
    for name, code, share, nd in REGIONS:
        w = np.linspace(1.9, 0.35, nd)  # a few large districts and some small ones in every region
        w = w / w.sum()
        for i in range(nd):
            rows.append({"region": name, "district": f"{code}-{i + 1:02d}", "share": share * w[i]})
    d = pd.DataFrame(rows)
    d["share"] /= d["share"].sum()
    return d


def make_people(rng, n, dist, id_prefix="YH", start=1):
    di = rng.choice(len(dist), size=n, p=dist["share"].to_numpy())
    region = dist["region"].to_numpy()[di]
    district = dist["district"].to_numpy()[di]
    # postcodes: 8 to 14 per district, the first two digits fixed by the district
    pc_counts = 8 + (np.arange(len(dist)) * 7) % 7
    pc = np.array([10000 + (di_ * 150) + rng.integers(0, pc_counts[di_]) for di_ in di])
    gender = np.where(rng.random(n) < 0.34, "F", "M")
    nationality = np.where(rng.random(n) < np.where(gender == "F", 0.12, 0.05), "Non-Saudi", "Saudi")
    age = np.clip(np.round(rng.normal(41, 11, n)), 21, 75).astype(int)
    ref = np.datetime64("2026-07-01")
    birth = ref - (age * 365.25).astype("timedelta64[D]") - rng.integers(0, 365, n).astype("timedelta64[D]")
    marital = np.where(gender == "F",
                       rng.choice(["married", "divorced", "widowed", "single"], n, p=[0.38, 0.30, 0.20, 0.12]),
                       rng.choice(["married", "divorced", "widowed", "single"], n, p=[0.78, 0.08, 0.03, 0.11]))
    hh = np.clip(rng.poisson(np.where(marital == "single", 1.2, 3.8)) + 1, 1, 11)
    employment = rng.choice(["government", "private", "self-employed", "unemployed", "retired"], n,
                            p=[0.29, 0.29, 0.12, 0.16, 0.14])
    employment = np.where((age >= 60) & (rng.random(n) < 0.7), "retired", employment)
    base = {"government": 9800, "private": 8200, "self-employed": 7000, "unemployed": 2600, "retired": 5600}
    med = np.array([base[e] for e in employment]) * np.where(gender == "F", 0.78, 1.0)
    true_income = np.round(med * np.exp(rng.normal(0, 0.5, n)), -1)
    disability = np.where(rng.random(n) < 0.09, "yes", "no")
    social_security = np.where((true_income < 4000) & (rng.random(n) < 0.55), "yes", "no")
    tenure = rng.choice(["renting", "family_home", "other"], n, p=[0.62, 0.30, 0.08])
    rent = np.where(tenure == "renting", np.round(rng.normal(2100, 600, n).clip(700, 6000), -1), 0)
    firsts = np.where(gender == "F", rng.choice(FIRST_F, n), rng.choice(FIRST_M, n))
    father = rng.choice(FIRST_M, n)
    family = rng.choice(FAMILY, n)
    names = [f"{a} {b} {c}" for a, b, c in zip(firsts, father, family)]
    ids = [f"{id_prefix}-{i:06d}" for i in range(start, start + n)]
    nid = [f"SYN{rng.integers(1_000_000, 9_999_999)}" for _ in range(n)]
    mobile = [f"05-SYN-{rng.integers(100000, 999999)}" for _ in range(n)]
    email = [f"{a.lower()}.{c.lower().replace('al-', '')}{rng.integers(10, 999)}@example.org" for a, c in zip(firsts, family)]
    return pd.DataFrame({
        "applicant_id": ids, "national_id": nid, "full_name": names, "mobile": mobile, "email": email,
        "birth_date": pd.to_datetime(birth).strftime("%Y-%m-%d"), "gender": gender, "nationality": nationality,
        "marital_status": marital, "region": region, "district": district, "postcode": pc.astype(str),
        "household_size": hh, "employment": employment, "true_income": true_income,
        "disability_in_household": disability, "social_security": social_security, "tenure": tenure,
        "monthly_rent_sar": rent.astype(int),
    })


NOTES = [
    "Documents complete.", "Lease contract uploaded.", "Awaiting salary certificate.", "Visited branch office.",
    "Income statement checked.", "Requested review of household size.", "", "", "", "",
]


def add_notes(rng, df):
    notes = rng.choice(NOTES, len(df)).astype(object)
    hit = rng.random(len(df)) < 0.04
    for i in np.flatnonzero(hit):
        r = df.iloc[i]
        kind = rng.integers(0, 3)
        if kind == 0:
            notes[i] = f"Called back on {r['mobile']} about the lease."
        elif kind == 1:
            notes[i] = f"Spoke to {r['full_name'].split()[0]} at the branch; brother handles the file."
        else:
            notes[i] = f"Duplicate file found under {r['national_id']}."
    df["case_note"] = notes
    return int(hit.sum())


def decisions(rng, df):
    """The reviewed truth, the recorded income and the officers' historical decisions."""
    n = len(df)
    pc_true = df["true_income"] / df["household_size"]
    limit = np.where(df["disability_in_household"] == "yes", 2200, 1600)
    eligible = (pc_true < limit)
    flip = rng.random(n) < 0.05
    eligible = np.where(flip, ~eligible, eligible)
    df["reviewed_eligible"] = np.where(eligible, 1, 0)
    # measurement: self-employed income is recorded as turnover
    noise = rng.normal(1.0, 0.03, n)
    factor = np.where(df["employment"] == "self-employed", rng.uniform(1.5, 2.0, n), noise)
    recorded = np.round(df["true_income"] * factor, -1)
    female = df["gender"] == "F"
    p_miss = (0.02 + 0.06 * female + 0.03 * (df["employment"] == "self-employed")
              + 0.15 * (female & (df["nationality"] == "Non-Saudi")))
    recorded = np.where(rng.random(n) < p_miss, np.nan, recorded)
    df["monthly_income_sar"] = recorded
    days = rng.integers(0, (np.datetime64("2026-06-30") - np.datetime64("2023-01-01")).astype(int), n)
    df["application_date"] = (np.datetime64("2023-01-01") + days.astype("timedelta64[D]")).astype(str)
    # officers' decisions on the recorded income
    pc_rec = recorded / df["household_size"]
    approve = pc_rec < limit
    approve = np.where(np.isnan(pc_rec), rng.random(n) < 0.35, approve)
    old_rule = (df["application_date"] < "2024-07-01") & (df["tenure"] == "family_home")
    approve = np.where(old_rule & ~(pc_rec < 800), False, approve)  # historical: the pre-2024 rule
    qsm_bias = (df["region"] == "Qassim") & (df["gender"] == "F") & approve & (rng.random(n) < 0.35)
    approve = np.where(qsm_bias, False, approve)  # labelling: one office under-approved women-headed households
    officer_noise = rng.random(n) < 0.04
    approve = np.where(officer_noise, ~approve.astype(bool), approve)
    df["officer_decision"] = np.where(approve, "approved", "declined")
    df["office"] = df["region"] + " office"
    return int(old_rule.sum()), int(qsm_bias.sum())


FEATURES_NUM = ["log_income", "income_missing", "per_capita", "household_size", "age", "monthly_rent_sar"]
FEATURES_CAT = ["tenure", "employment", "region", "marital_status", "disability_in_household", "social_security"]


def model_frame(df):
    x = df.copy()
    inc = x["monthly_income_sar"]
    x["income_missing"] = inc.isna().astype(int)
    fill = inc.fillna(7000)
    x["log_income"] = np.log1p(fill)
    x["per_capita"] = fill / x["household_size"]
    x["age"] = 2026 - pd.to_datetime(x["birth_date"]).dt.year
    return x[FEATURES_NUM + FEATURES_CAT]


def ahliya():
    pre = ColumnTransformer([("num", StandardScaler(), FEATURES_NUM),
                             ("cat", OneHotEncoder(handle_unknown="ignore"), FEATURES_CAT)])
    return make_pipeline(pre, LogisticRegression(max_iter=2000, C=1.0))


def write_csv(df, name):
    if name.endswith(".gz"):
        import gzip
        raw = df.to_csv(index=False, lineterminator="\n").encode("utf-8")
        with open(DATA / name, "wb") as fh, gzip.GzipFile(filename="", mode="wb", fileobj=fh, mtime=0) as gz:
            gz.write(raw)  # a fixed header: the same bytes on every run
    else:
        df.to_csv(DATA / name, index=False, lineterminator="\n")


def main():
    rng = np.random.default_rng(SEED)
    DATA.mkdir(exist_ok=True)
    (DATA / "reference").mkdir(exist_ok=True)
    dist = districts()
    df = make_people(rng, N, dist)
    n_notes = add_notes(rng, df)
    n_old, n_qsm = decisions(rng, df)

    # the applicant table, as the fund holds it (the true income stays in the generator)
    cols = ["applicant_id", "national_id", "full_name", "mobile", "email", "birth_date", "gender", "nationality",
            "marital_status", "region", "district", "postcode", "household_size", "employment",
            "monthly_income_sar", "disability_in_household", "social_security", "tenure", "monthly_rent_sar",
            "application_date", "office", "officer_decision", "case_note"]
    applicants = df[cols]
    write_csv(applicants, "applicants.csv.gz")

    # pseudonyms for the research extract (a keyed code, the key held by the data protection officer)
    order = rng.permutation(N)
    df["pseudo_id"] = ""
    df.loc[df.index[order], "pseudo_id"] = [f"R{i:05d}" for i in range(N)]
    release_a = df[["pseudo_id", "birth_date", "gender", "nationality", "postcode", "district", "region",
                    "household_size", "employment", "monthly_income_sar", "disability_in_household",
                    "social_security", "officer_decision"]].sort_values("pseudo_id")
    write_csv(release_a, "release_a_research_extract.csv.gz")

    # a public register that overlaps 3,000 applicants (a synthetic volunteers register published online)
    overlap = rng.choice(N, 3000, replace=False)
    others = make_people(rng, 6000, dist, id_prefix="VX", start=1)
    reg_app = df.iloc[overlap][["full_name", "birth_date", "gender", "postcode", "pseudo_id"]].copy()
    reg_oth = others[["full_name", "birth_date", "gender", "postcode"]].copy()
    reg_oth["pseudo_id"] = ""
    register = pd.concat([reg_app, reg_oth]).sample(frac=1, random_state=SEED).reset_index(drop=True)
    register.insert(0, "register_id", [f"VR-{i:05d}" for i in range(len(register))])
    write_csv(register[["register_id", "full_name", "birth_date", "gender", "postcode"]], "public_register.csv")
    write_csv(register[["register_id", "pseudo_id"]], "reference/linkage_truth.csv")

    # Day 3: Ahliya, trained on the officers' decisions, scored on 12,000 reviewed applications
    test_idx = rng.choice(N, N_TEST, replace=False)
    is_test = np.zeros(N, bool)
    is_test[test_idx] = True
    train = df[~is_test].copy()
    test = df[is_test].copy()
    model = ahliya()
    y_train = (train["officer_decision"] == "approved").astype(int)
    model.fit(model_frame(train), y_train)
    test["score"] = np.round(model.predict_proba(model_frame(test))[:, 1], 4)
    train_cols = ["applicant_id", "birth_date", "gender", "nationality", "marital_status", "region", "district",
                  "household_size", "employment", "monthly_income_sar", "disability_in_household",
                  "social_security", "tenure", "monthly_rent_sar", "application_date", "officer_decision"]
    write_csv(train[train_cols], "ahliya_train.csv.gz")
    test["age_band"] = pd.cut(2026 - pd.to_datetime(test["birth_date"]).dt.year, [0, 30, 40, 50, 60, 120],
                              labels=["21-30", "31-40", "41-50", "51-60", "61+"], right=True).astype(str)
    test_cols = ["applicant_id", "gender", "nationality", "region", "age_band", "marital_status", "employment",
                 "tenure", "household_size", "monthly_income_sar", "disability_in_household", "social_security",
                 "application_date", "office", "officer_decision", "reviewed_eligible", "score", "monthly_rent_sar"]
    write_csv(test[test_cols], "ahliya_scored_test.csv")

    # the modelling lead's validation report: officers' decisions, two urban regions only
    urban = test["region"].isin(["Riyadh", "Makkah"])
    y_off = (test["officer_decision"] == "approved").astype(int)
    pred = (test["score"] >= 0.5).astype(int)
    report = {
        "model": "Ahliya", "version": "1.3", "author": "Anmar Al-Ghamdi",
        "validation_set": "applications of 2025 and 2026 from Riyadh and Makkah, labelled by officers' decisions",
        "rows": int(urban.sum()),
        "accuracy": round(float((pred[urban] == y_off[urban]).mean()), 3),
        "auc": round(float(roc_auc_score(y_off[urban], test.loc[urban, "score"])), 3),
        "threshold": 0.5,
    }
    (DATA / "ahliya_validation_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")

    # deployment log: Ahliya auto-declines low scores; only applications passed to an officer get a reviewed label
    dep = make_people(rng, 9000, dist, id_prefix="YD", start=1)
    decisions(rng, dep)
    dep["score"] = np.round(model.predict_proba(model_frame(dep))[:, 1], 4)
    dep["route"] = np.where(dep["score"] < 0.2, "auto-declined", "officer review")
    dep["label_available"] = np.where(dep["route"] == "officer review", "yes", "no")
    dep["score_band"] = pd.cut(dep["score"], [0, 0.2, 0.4, 0.6, 0.8, 1.0001], right=False,
                               labels=["0.0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"]).astype(str)
    write_csv(dep[["applicant_id", "gender", "employment", "tenure", "score", "score_band", "route",
                   "label_available"]], "ahliya_deployment_log.csv")

    # Day 4.4: the peer's notebook result
    peer = test[test["monthly_income_sar"].notna()]
    pp = peer["score"] >= 0.45
    def fnr(d, p):
        pos = d["reviewed_eligible"] == 1
        return float((~p[pos]).mean())
    f_w = fnr(peer[peer["gender"] == "F"], pp[peer["gender"] == "F"])
    f_m = fnr(peer[peer["gender"] == "M"], pp[peer["gender"] == "M"])
    claims = {"author": "a participant of an earlier cohort", "claim": "Ahliya misses eligible men more often than eligible women",
              "fnr_women": round(f_w, 3), "fnr_men": round(f_m, 3), "gap": round(f_w - f_m, 3),
              "interval": "bootstrap, 200 resamples", "data": "data/ahliya_scored_test.csv"}
    (DATA / "peer").mkdir(exist_ok=True)
    (DATA / "peer" / "peer_results.json").write_text(json.dumps(claims, indent=2) + "\n", encoding="utf-8", newline="\n")

    # Day 3.3: an income audit of 600 reviewed applications (verified income against recorded income)
    audit_rng = np.random.default_rng(SEED + 1)
    audit = test.iloc[audit_rng.choice(len(test), 600, replace=False)]
    audit = audit.assign(verified_income_sar=audit["true_income"])
    write_csv(audit[["applicant_id", "employment", "monthly_income_sar", "verified_income_sar"]], "income_audit.csv")

    # facts for the trainer's answer key
    facts = {
        "applicants": N, "notes_with_identifiers": n_notes, "old_rule_rows": n_old, "qassim_flips": n_qsm,
        "test_rows": N_TEST, "train_rows": int((~is_test).sum()), "register_rows": len(register),
        "register_applicants": 3000, "validation_report": report,
        "test_base_rate": round(float(test["reviewed_eligible"].mean()), 3),
        "test_auc_vs_reviewed": round(float(roc_auc_score(test["reviewed_eligible"], test["score"])), 3),
    }
    (DATA / "reference" / "generator_facts.json").write_text(json.dumps(facts, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(facts, indent=2))


if __name__ == "__main__":
    main()
