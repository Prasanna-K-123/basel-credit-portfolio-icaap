from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm

from src.config import BASEL_CONFIDENCE, BASEL_MIN_PD


def asset_correlation(pd_values):
    pd_values = np.asarray(pd_values, dtype=float)
    pd_values = np.clip(pd_values, BASEL_MIN_PD, 0.999)
    exp_term = (1.0 - np.exp(-50.0 * pd_values)) / (1.0 - np.exp(-50.0))
    return 0.12 * exp_term + 0.24 * (1.0 - exp_term)


def maturity_adjustment(pd_values, maturity):
    pd_values = np.asarray(pd_values, dtype=float)
    maturity = np.asarray(maturity, dtype=float)
    pd_values = np.clip(pd_values, BASEL_MIN_PD, 0.999)
    b = (0.11852 - 0.05478 * np.log(pd_values)) ** 2
    return (1.0 + (maturity - 2.5) * b) / (1.0 - 1.5 * b)


def capital_requirement_rate(pd_values, lgd_values, maturity):
    pd_values = np.asarray(pd_values, dtype=float)
    lgd_values = np.asarray(lgd_values, dtype=float)
    maturity = np.asarray(maturity, dtype=float)

    pd_values = np.clip(pd_values, BASEL_MIN_PD, 0.999)
    lgd_values = np.clip(lgd_values, 0.0, 1.0)
    r = asset_correlation(pd_values)
    stressed_pd = norm.cdf(
        (norm.ppf(pd_values) + np.sqrt(r) * norm.ppf(BASEL_CONFIDENCE))
        / np.sqrt(1.0 - r)
    )
    k = (lgd_values * stressed_pd - pd_values * lgd_values) * maturity_adjustment(pd_values, maturity)
    return np.maximum(k, 0.0)


def calculate_irb_capital(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["expected_loss"] = out["pd"] * out["lgd"] * out["ead"]
    out["capital_rate"] = capital_requirement_rate(out["pd"], out["lgd"], out["maturity"])
    out["irb_capital"] = out["capital_rate"] * out["ead"]
    out["rwa"] = 12.5 * out["irb_capital"]
    return out
