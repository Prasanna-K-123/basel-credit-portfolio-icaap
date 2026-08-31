from __future__ import annotations

import pandas as pd

from src.basel_irb import calculate_irb_capital

SCENARIOS = {
    "base": {"pd_multiplier": 1.00, "lgd_add": 0.00, "ead_multiplier": 1.00},
    "mild": {"pd_multiplier": 1.35, "lgd_add": 0.03, "ead_multiplier": 1.02},
    "adverse": {"pd_multiplier": 1.85, "lgd_add": 0.08, "ead_multiplier": 1.05},
    "severe": {"pd_multiplier": 2.60, "lgd_add": 0.15, "ead_multiplier": 1.10},
}


def apply_stress(df: pd.DataFrame, pd_multiplier: float, lgd_add: float, ead_multiplier: float) -> pd.DataFrame:
    stressed = df.copy()
    stressed["pd"] = (stressed["pd"] * pd_multiplier).clip(upper=0.999)
    stressed["lgd"] = (stressed["lgd"] + lgd_add).clip(upper=1.0)
    stressed["ead"] = stressed["ead"] * ead_multiplier
    return stressed


def stress_summary(df: pd.DataFrame, scenarios: dict = SCENARIOS) -> pd.DataFrame:
    rows = []
    for name, p in scenarios.items():
        s = calculate_irb_capital(apply_stress(df, **p))
        rows.append({
            "scenario": name,
            **p,
            "ead": float(s["ead"].sum()),
            "expected_loss": float(s["expected_loss"].sum()),
            "irb_capital": float(s["irb_capital"].sum()),
            "rwa": float(s["rwa"].sum()),
        })
    return pd.DataFrame(rows)
