# Capstone: the release pack for Sabeel Scholarship Fund

Sabeel Scholarship Fund (صندوق سبيل للمنح الدراسية) is a fictional fund that awards university
scholarships to secondary-school leavers. A screening model, **Tarjih**, scores every application
before an officer decides. Three requests arrive at once:

1. A university research group asks for an extract of the applications to study how school type
   and region relate to awards.
2. The fund's board wants to publish counts of awards by region and field of study.
3. Internal audit wants Tarjih audited before the next intake.

You prepare the release pack the fund's data protection officer needs before anything leaves the
fund. Everything is synthetic, generated with a fixed seed; no row describes a real person.

## The data

Run `uv run python capstone/make_sabeel.py` from `labs/` to write the files again; they are the same
on every run.

| File | What it holds |
|---|---|
| `data/sabeel_applicants.csv.gz` | 24,000 applications of 2024 to 2026, with direct identifiers, the school and city, grades, the aptitude score, household income and family size, and the officer's decision |
| `data/sabeel_public_honours.csv` | 2,500 award holders of 2025 as a university newsletter printed them: name, birth date, gender and school code |
| `data/sabeel_scored_test.csv` | 6,000 applications that Tarjih scored and that a full review settled (`reviewed_eligible`), without direct identifiers |
| `data/tarjih_validation.json` | The vendor's validation summary of Tarjih |

## What to hand in

A link to a **public GitHub repository** that holds:

- **The treated extract** for the research group, with its **release log**: risk before and after
  (unique records, k, a linkage test against the public list), the treatment, what was suppressed,
  and the change in at least three key statistics.
- **The public statistics**: award counts by region and field released under a stated privacy
  budget, with their expected error.
- **The fairness audit** of Tarjih: error rates by group and at least one intersection, with
  intervals and counts, the criterion you chose and why, the findings mapped to the bias types of
  the national AI Bias Reference Guide, one mitigation measured on held-out rows, and a
  recommendation.
- **The datasheet** of the extract and **the model card** of Tarjih.
- **The impact assessment**: each risk scored on the National AI Risk Management Framework's
  likelihood and impact scales, with treatment, residual risk, owner, and a human reviewer for
  every high risk.
- **A README** that reports the measured risk, utility and disparities and says how to rerun every
  number: the environment (a lock file), the seeds, and the order of the notebooks.

Commit as you go: the history is part of the evidence. A synthetic file for a hackathon is optional;
if you release one, include its leakage tests.

## The review

Ten minutes, questions included. The assessor picks a slice of the scored test set (a region, a
school type, a field, or two of them crossed) and you recompute one disparity live from your
repository, with its interval.

## Scoring

| Criterion | Weight |
|---|---|
| Privacy | 25% |
| Fairness audit | 25% |
| Documentation | 20% |
| Impact assessment | 20% |
| Reproducibility | 10% |

Reuse the week's notebooks: the methods carry over, the numbers do not. The Yusr reference results
do not apply to Sabeel.
