# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas>=2.2", "numpy>=2.0", "scikit-learn>=1.6", "matplotlib>=3.8", "opendp>=0.16", "fairlearn>=0.13"]
# ///
# %% [markdown]
# # Setup check
#
# Run this once before Day 1, on your laptop or in Google Colab. It imports every library the labs
# use, reads one data file, and prints what is missing. No lab calls or downloads a model.

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

# %%
import importlib

missing = []
for name in ["pandas", "numpy", "sklearn", "matplotlib", "opendp", "fairlearn"]:
    try:
        mod = importlib.import_module(name)
        print(f"{name:12} {getattr(mod, '__version__', '?')}")
    except ImportError:
        missing.append(name)
print("Python", sys.version.split()[0])

# %%
import yusr as U

applicants = U.load("applicants.csv.gz")
print(f"{len(applicants):,} applicant records read")
missing += [] if len(applicants) == 60_000 else ["the data files (run: uv run python prepare_data.py)"]
U.check(not missing, "ready for Day 1" if not missing else "missing: " + ", ".join(missing))
