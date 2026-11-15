# Responsible Data Science: Privacy, Fairness and Documentation: labs

## Quick start

- Google Colab: open a notebook from the course page; its first cell clones this repository.
- Locally: clone the repository, then open the notebooks in `labs/` with Jupyter.

| Unit | Session | Notebook |
|---|---|---|
| Day 1 | Session 1 · Personal data in an analysis | [`D1_1_tag_each_applicant.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-309/blob/main/labs/D1_1_tag_each_applicant.ipynb) |
| Day 1 | Session 2 · Classification and permitted use | [`D1_2_assign_classification_levels.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-309/blob/main/labs/D1_2_assign_classification_levels.ipynb) |
| Day 1 | Session 3 · Linkage attacks | [`D1_3_re_identify_applicants.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-309/blob/main/labs/D1_3_re_identify_applicants.ipynb) |
| Day 1 | Session 4 · Measuring disclosure risk | [`D1_4_compute_unique_quasi.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-309/blob/main/labs/D1_4_compute_unique_quasi.ipynb) |
| Day 2 | Session 1 · Generalisation and suppression | [`D2_1_reach_k_least.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-309/blob/main/labs/D2_1_reach_k_least.ipynb) |
| Day 2 | Session 2 · Differential privacy for counts | [`D2_2_release_district_counts.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-309/blob/main/labs/D2_2_release_district_counts.ipynb) |
| Day 2 | Session 3 · Budgets and composition | [`D2_3_split_one_budget.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-309/blob/main/labs/D2_3_split_one_budget.ipynb) |
| Day 2 | Session 4 · Synthetic data and leakage | [`D2_4_generate_synthetic_extract.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-309/blob/main/labs/D2_4_generate_synthetic_extract.ipynb) |
| Day 3 | Session 1 · Disaggregating errors | [`D3_1_compute_error_rates.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-309/blob/main/labs/D3_1_compute_error_rates.ipynb) |
| Day 3 | Session 2 · Criteria that conflict | [`D3_2_show_two_fairness.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-309/blob/main/labs/D3_2_show_two_fairness.ipynb) |
| Day 3 | Session 3 · Bias across the lifecycle | [`D3_3_map_five_findings.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-309/blob/main/labs/D3_3_map_five_findings.ipynb) |
| Day 3 | Session 4 · Mitigation and its cost | [`D3_4_apply_reweighting_threshold.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-309/blob/main/labs/D3_4_apply_reweighting_threshold.ipynb) |
| Day 4 | Session 1 · Datasheets | [`D4_1_write_datasheet_de.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-309/blob/main/labs/D4_1_write_datasheet_de.ipynb) |
| Day 4 | Session 2 · Model cards | [`D4_2_write_model_card.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-309/blob/main/labs/D4_2_write_model_card.ipynb) |
| Day 4 | Session 3 · Impact assessment | [`D4_3_score_four_risks.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-309/blob/main/labs/D4_3_score_four_risks.ipynb) |
| Day 4 | Session 4 · Review by someone else | [`D4_4_rerun_one_result.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-309/blob/main/labs/D4_4_rerun_one_result.ipynb) |

The notebooks are generated from the percent-format sources in `labs/_src/` by `labs/_tools/py2nb.py` (`uv run python _tools/py2nb.py` from `labs/`), which also writes the solutions to `labs/solutions/`. Edit the sources, not the notebooks.
