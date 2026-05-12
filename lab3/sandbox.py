import io
import sys
import traceback
import base64
import re
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

BLOCKED = [re.compile(r"\bimport\s+(os|sys|subprocess)"), re.compile(r"__import__|eval\(|exec\(|open\(")]
SAFE_BUILTINS = {
    "print": print, "len": len, "range": range, "str": str, "int": int, "float": float,
    "list": list, "dict": dict, "tuple": tuple, "sum": sum, "max": max, "min": min,
    "Exception": Exception, "True": True, "False": False, "None": None
}

def run_code(code, df):
    for p in BLOCKED:
        if p.search(code):
            return "Опасный код", None
    loc = {"__builtins__": SAFE_BUILTINS, "df": df, "pd": pd, "np": np, "plt": plt, "fig": None}
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    err = None
    try:
        exec(code, loc)
    except Exception:
        err = traceback.format_exc(limit=1)
    sys.stdout = old
    out = buf.getvalue()
    if err:
        out += f"\n{err}"
    img = None
    if loc.get("fig") is not None:
        b = io.BytesIO()
        loc["fig"].savefig(b, format="png")
        b.seek(0)
        img = base64.b64encode(b.read()).decode()
        plt.close(loc["fig"])
    elif plt.get_fignums():
        b = io.BytesIO()
        plt.savefig(b, format="png")
        b.seek(0)
        img = base64.b64encode(b.read()).decode()
        plt.close("all")
    return (out[:150] or "OK"), img