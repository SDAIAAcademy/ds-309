# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas>=2.2", "numpy>=2.0", "scikit-learn>=1.6"]
# ///
"""Write the synthetic data of the capstone case, Sabeel Scholarship Fund, into labs/capstone/data/.

    cd labs
    uv run python capstone/make_sabeel.py

Fixed seed, same files every run. Everything is invented; identifiers carry the marker SYN. The
problems planted in the data are listed for trainers in solutions/answer_key.md, not here.
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

SEED = 3090
HERE = Path(__file__).resolve().parent
OUT = HERE / "data"
N = 24_000
N_TEST = 6_000

REGIONS = [("Riyadh", 0.25, 9), ("Makkah", 0.24, 9), ("Eastern", 0.15, 7), ("Madinah", 0.07, 5),
           ("Qassim", 0.05, 4), ("Asir", 0.06, 5), ("Tabuk", 0.03, 3), ("Hail", 0.025, 3),
           ("Northern Borders", 0.012, 2), ("Jazan", 0.05, 4), ("Najran", 0.02, 3), ("Al-Bahah", 0.015, 2),
           ("Al-Jouf", 0.018, 3)]
REMOTE = {"Northern Borders", "Jazan", "Najran", "Al-Bahah", "Al-Jouf"}
FIELDS = ["engineering", "medicine and health", "computing", "business", "education", "sciences", "humanities"]
FIRST_F = ["Amal", "Asma", "Dana", "Ghala", "Hala", "Hind", "Joud", "Lama", "Leen", "Maha", "Nouf", "Rahaf",
           "Reema", "Renad", "Sarah", "Shahad", "Taif", "Wasan", "Yara", "Lujain"]
FIRST_M = ["Abdulrahman", "Ahmed", "Ali", "Bassam", "Fahad", "Faris", "Hamza", "Hussam", "Khalid", "Majed",
           "Mohammed", "Nawaf", "Omar", "Rakan", "Saud", "Talal", "Turki", "Yazeed", "Ziyad", "Mishari"]
FAMILY = ["Al-Anazi", "Al-Asiri", "Al-Balawi", "Al-Dosari", "Al-Faifi", "Al-Ghamdi", "Al-Harbi", "Al-Juhani",
          "Al-Maliki", "Al-Mutairi", "Al-Omari", "Al-Qahtani", "Al-Rashidi", "Al-Shammari", "Al-Shehri",
          "Al-Subaie", "Al-Tamimi", "Al-Zahrani", "Al-Yami", "Al-Hazmi"]


def write(df: pd.DataFrame, name: str) -> None:
    path = OUT / name
    if name.endswith(".gz"):
        with open(path, "wb") as fh, gzip.GzipFile(filename="", mode="wb", fileobj=fh, mtime=0) as gz:
            gz.write(df.to_csv(index=False, lineterminator="\n").encode("utf-8"))
    else:
        path.write_text(df.to_csv(index=False, lineterminator="\n"), encoding="utf-8", newline="\n")


def main() -> None:
    rng = np.random.default_rng(SEED)
    OUT.mkdir(exist_ok=True)
    reg = pd.DataFrame(REGIONS, columns=["region", "share", "cities"])
    reg["share"] /= reg["share"].sum()
    ri = rng.choice(len(reg), N, p=reg["share"].to_numpy())
    region = reg["region"].to_numpy()[ri]
    city = np.array([f"{r[:3].upper()}-C{rng.integers(1, c + 1):02d}" for r, c in zip(region, reg["cities"].to_numpy()[ri])])
    gender = np.where(rng.random(N) < 0.52, "F", "M")
    nationality = np.where(rng.random(N) < 0.07, "Non-Saudi", "Saudi")
    birth = (np.datetime64("2008-09-01") - rng.integers(0, 3 * 365, N).astype("timedelta64[D]"))
    remote = np.isin(region, list(REMOTE))
    school_type = np.where(rng.random(N) < np.where(remote, 0.08, 0.27), "private", "public")
    school = np.array([f"{c}-S{rng.integers(1, 7)}" for c in city])
    income = np.round(np.clip(rng.lognormal(np.log(np.where(school_type == "private", 19000, 9500)), 0.55), 2500, 90000), -1)
    family = np.clip(rng.poisson(4.5, N) + 1, 2, 13)
    disability = np.where(rng.random(N) < 0.035, "yes", "no")
    merit = rng.normal(0, 1, N)  # what the review judges; never released
    gpa = np.clip(np.round(88 + 6 * merit + rng.normal(0, 2.5, N) + np.where(school_type == "private", 4.0, 0.0), 1), 60, 100)
    aptitude = np.clip(np.round(74 + 8 * merit + rng.normal(0, 4, N)), 40, 100)
    p_missing = np.where(remote, 0.22, 0.04) * np.where(gender == "F", 1.6, 1.0)
    aptitude = np.where(rng.random(N) < p_missing, np.nan, aptitude)
    field = rng.choice(FIELDS, N, p=[0.2, 0.18, 0.16, 0.16, 0.1, 0.1, 0.1])
    year = rng.choice([2024, 2025, 2026], N, p=[0.3, 0.33, 0.37])
    need = income / family
    reviewed = ((merit > -0.15) & (need < 5200)) | ((merit > 0.9) & (need < 9000))
    # officers: favoured high grades and full files, and in one region declined women in engineering
    s_off = 0.9 * (gpa - 88) / 6 + 0.5 * np.nan_to_num((aptitude - 74) / 8, nan=-1.4) - 0.00012 * (need - 4000)
    officer = s_off + rng.normal(0, 0.6, N) > 0.1
    officer &= ~((region == "Eastern") & (gender == "F") & (field == "engineering") & (rng.random(N) < 0.4))
    sid = np.arange(1, N + 1)
    first = np.where(gender == "F", rng.choice(FIRST_F, N), rng.choice(FIRST_M, N))
    df = pd.DataFrame({
        "student_id": [f"SB-{i:06d}" for i in sid],
        "national_id": [f"SYN{rng.integers(10**8, 10**9)}" for _ in sid],
        "name": [f"{f} {rng.choice(FIRST_M)} {rng.choice(FAMILY)}" for f in first],
        "mobile": [f"05SYN{rng.integers(10**5, 10**6)}" for _ in sid],
        "birth_date": pd.to_datetime(birth).strftime("%Y-%m-%d"),
        "gender": gender, "nationality": nationality, "region": region, "city": city, "school": school,
        "school_type": school_type, "gpa": gpa, "aptitude_score": aptitude, "household_income_sar": income,
        "family_size": family, "disability": disability, "field_of_study": field, "application_year": year,
        "officer_decision": np.where(officer, "awarded", "declined"), "reviewed_eligible": reviewed.astype(int),
    })
    # the screening model, Tarjih: trained on the officers' decisions, missing aptitude filled with 0
    X = df[["gpa", "aptitude_score", "household_income_sar", "family_size", "school_type", "field_of_study", "region"]].copy()
    X["aptitude_score"] = X["aptitude_score"].fillna(0)
    pre = ColumnTransformer([("n", StandardScaler(), ["gpa", "aptitude_score", "household_income_sar", "family_size"]),
                             ("c", OneHotEncoder(handle_unknown="ignore"), ["school_type", "field_of_study", "region"])])
    idx = rng.permutation(N)
    tr, te = idx[N_TEST:], idx[:N_TEST]
    model = make_pipeline(pre, LogisticRegression(max_iter=2000)).fit(X.iloc[tr], officer[tr].astype(int))
    df["score"] = np.round(model.predict_proba(X)[:, 1], 4)
    applicants = df.drop(columns=["reviewed_eligible", "score"])
    write(applicants, "sabeel_applicants.csv.gz")
    scored = df.iloc[np.sort(te)].drop(columns=["national_id", "name", "mobile", "birth_date", "school", "city"])
    write(scored, "sabeel_scored_test.csv")
    # a public list of last year's award holders, as a university newsletter might print it
    pub = df[(df["application_year"] == 2025) & officer].sample(2500, random_state=SEED)
    write(pub[["name", "birth_date", "gender", "school"]].rename(columns={"school": "school_code"}), "sabeel_public_honours.csv")
    (OUT / "tarjih_validation.json").write_text(json.dumps({
        "model": "Tarjih 2.0", "threshold": 0.5, "trained_on": "officer decisions, 2024 to 2026",
        "accuracy_vs_officers": round(float(((df["score"].iloc[te] >= 0.5) == officer[te]).mean()), 3),
        "note": "missing aptitude scores are filled with 0 before scoring",
    }, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(applicants):,} applicants · {len(scored):,} scored and reviewed · {len(pub):,} on the public list")


if __name__ == "__main__":
    main()
