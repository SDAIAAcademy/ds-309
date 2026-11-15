"""Shared helpers for the DS-309 labs (Yusr Housing Support Fund, synthetic data).

    import yusr as U

U.DATA            the data folder (labs/data)
U.QUICK           True when YUSR_QUICK=1: fewer repetitions and smaller samples
U.pick(a, b)      a normally, b in quick mode
U.load(name)      a CSV (or .csv.gz) of labs/data as a pandas DataFrame
U.json(name)      a JSON file of labs/data
U.reference(n)    the reference result of an exercise, for the safety-net cells
U.keep(n, value)  writes a reference result (only when YUSR_WRITE_REF=1, for the course team)
U.check(ok, m)    prints a tick, or raises AssertionError with the message
U.wilson(k, n)    the 95% Wilson interval of k / n, as (low, high)
U.classes(df, q)  the size of each record's equivalence class on the quasi-identifiers q
U.out(lab)        a folder labs/artifacts/<lab>/ for what a lab writes
U.plt(), U.show() matplotlib with the course defaults, and show() that is quiet outside a notebook
"""

from __future__ import annotations

import json as _json
import math
import os
import sys
from pathlib import Path

try:  # a Windows console that is not UTF-8 cannot print the ticks
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
REF = DATA / "reference"
QUICK = os.environ.get("YUSR_QUICK", "0") == "1"
WRITE_REF = os.environ.get("YUSR_WRITE_REF", "0") == "1"
SEED = 309
Z95 = 1.959964


def pick(full, quick):
    return quick if QUICK else full


def load(name: str):
    import pandas as pd
    return pd.read_csv(DATA / name, dtype={"postcode": str})


def json(name: str):
    return _json.loads((DATA / name).read_text(encoding="utf-8"))


def _encode(value):
    import pandas as pd
    if isinstance(value, pd.DataFrame):
        return {"__frame__": _json.loads(value.to_json(orient="split"))}
    if isinstance(value, dict):
        return {k: _encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_encode(v) for v in value]
    if hasattr(value, "item"):
        return value.item()
    return value


def _decode(value):
    import pandas as pd
    if isinstance(value, dict) and "__frame__" in value:
        f = value["__frame__"]
        return pd.DataFrame(f["data"], index=f["index"], columns=f["columns"])
    if isinstance(value, dict):
        return {k: _decode(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_decode(v) for v in value]
    return value


def reference(name: str):
    """The reference result of exercise `name`, so later cells run when it is not done yet."""
    print(f"(safety net: using the reference result for {name})")
    return _decode(_json.loads((REF / f"{name}.json").read_text(encoding="utf-8")))


def keep(name: str, value) -> None:
    """Write a reference result. Only the course team runs this, in full mode, with YUSR_WRITE_REF=1."""
    if WRITE_REF and not QUICK:
        REF.mkdir(exist_ok=True)
        (REF / f"{name}.json").write_text(_json.dumps(_encode(value), indent=1, ensure_ascii=False) + "\n",
                                          encoding="utf-8", newline="\n")


def check(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError("not yet: " + message)
    print("✅", message)


def wilson(k: int, n: int, z: float = Z95) -> tuple[float, float]:
    """The Wilson score interval of the proportion k / n."""
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (max(0.0, centre - half), min(1.0, centre + half))


def classes(df, quasi):
    """For every record, the number of records that share its values on the quasi-identifiers."""
    return df.groupby(list(quasi), dropna=False)[list(quasi)[0]].transform("size")


def out(lab: str) -> Path:
    p = HERE / "artifacts" / lab
    p.mkdir(parents=True, exist_ok=True)
    return p


def plt():
    import matplotlib
    if "MPLBACKEND" not in os.environ and not _in_notebook():
        matplotlib.use("Agg")
    import matplotlib.pyplot as _plt
    _plt.rcParams.update({"figure.figsize": (7, 3.6), "axes.spines.top": False, "axes.spines.right": False})
    return _plt


def _in_notebook() -> bool:
    try:
        from IPython import get_ipython
        return get_ipython() is not None
    except ImportError:
        return False


def show():
    """plt.show() in a notebook; nothing when the source runs as a script."""
    if _in_notebook():
        import matplotlib.pyplot as _plt
        _plt.show()


def generalise(df, b: int, p: int):
    """The reference generalisation of Lab 2.1, used by its safety nets and by later labs."""
    out = df.copy()
    year = out["birth_date"].str[:4].astype(int)
    if b == 0:
        out["birth"] = out["birth_date"]
    elif b == 1:
        out["birth"] = year.astype(str)
    else:
        width = 5 if b == 2 else 10
        lo = 1950 + ((year - 1950) // width) * width
        out["birth"] = lo.astype(str) + "-" + (lo + width - 1).astype(str)
    out["place"] = out[["postcode", "district", "region"][p]]
    return out


try:
    import pandas as _pd
    _pd.set_option("display.width", 160)
    _pd.set_option("display.max_columns", 20)
except ImportError:
    pass
