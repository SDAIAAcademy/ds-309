# %% [markdown]
# # Lab 2.2 · Release district counts at three budgets and plot the error
#
# Day 2 · Session 2 (Differential privacy for counts) · 25 min.
#
# REPLACE: what participants build in this lab, in two or three lines.
#
# **Tasks**
# - [ ] REPLACE: the tasks, each with its minutes; they add up to 25
# - [ ] ✱ Stretch · REPLACE: an extension for those who finish early

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ds-309.git"
    if not Path("/content/ds-309").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ds-309"], check=True)
    os.chdir("/content/ds-309/labs")
else:
    while not Path("_tools").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

# %% [markdown]
# ## 1 · REPLACE: the first task
#
# REPLACE: what to do and why, in two sentences.

# %%
# ✏️ Exercise
def first_task():
    # BEGIN SOLUTION
    return "the reference result"
    # END SOLUTION

# %%
# Check, with a safety net: the cells below still run when the exercise is not done yet
try:
    result = first_task()
except NotImplementedError:
    result = "the reference result"
print(result)
