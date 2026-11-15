"""My Lab 3.1 result: Ahliya misses eligible men more often than eligible women.

A participant's notebook from an earlier cohort, exported as a script. Kept as it was handed in.
"""
import numpy as np
import pandas as pd

THRESH = 0.45


def load(path="data/ahliya_scored_test.csv"):
    df = pd.read_csv(path)
    df = df[df["monthly_income_sar"].notna()]
    df["pred"] = (df["score"] >= THRESH).astype(int)
    return df


def fnr(df):
    eligible = df[df["reviewed_eligible"] == 1]
    return float((eligible["pred"] == 0).mean())


def result(df):
    w, m = df[df["gender"] == "F"], df[df["gender"] == "M"]
    return {"fnr_women": round(fnr(w), 3), "fnr_men": round(fnr(m), 3), "gap": round(fnr(w) - fnr(m), 3)}


def bootstrap_gap(df, runs=200):
    gaps = []
    for _ in range(runs):
        s = df.sample(frac=1, replace=True)
        gaps.append(result(s)["gap"])
    return np.percentile(gaps, [2.5, 97.5]).round(3).tolist()


if __name__ == "__main__":
    d = load()
    print(result(d), bootstrap_gap(d))
