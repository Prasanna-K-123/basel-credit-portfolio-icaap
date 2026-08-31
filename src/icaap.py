from __future__ import annotations

import pandas as pd

from src.basel_irb import calculate_irb_capital
from src.concentration import concentration_addon, concentration_metrics
from src.stress import apply_stress


def build_icaap_assessment(df: pd.DataFrame, ec_999: float, severe_stress_capital: float) -> dict:
    base = calculate_irb_capital(df)
    irb_capital = float(base["irb_capital"].sum())
    metrics = concentration_metrics(df)
    concentration = concentration_addon(irb_capital, metrics)

    core_credit_capital = max(irb_capital, float(ec_999))
    stress_overlay = max(severe_stress_capital - irb_capital, 0.0) * 0.25
    internal_requirement = core_credit_capital + concentration + stress_overlay

    available_capital = internal_requirement * 1.20
    surplus = available_capital - internal_requirement
    coverage_ratio = available_capital / internal_requirement if internal_requirement else float("inf")

    return {
        "irb_capital": irb_capital,
        "economic_capital_999": float(ec_999),
        "core_credit_capital": core_credit_capital,
        "concentration_addon": concentration,
        "stress_overlay": stress_overlay,
        "internal_capital_requirement": internal_requirement,
        "illustrative_available_capital": available_capital,
        "capital_surplus": surplus,
        "capital_coverage_ratio": coverage_ratio,
    }


def reverse_stress_pd_multiplier(
    df: pd.DataFrame,
    available_capital: float,
    concentration_addon_amount: float,
    max_multiplier: float = 12.0,
    step: float = 0.05,
) -> dict:
    multiplier = 1.0
    while multiplier <= max_multiplier + 1e-12:
        stressed = calculate_irb_capital(
            apply_stress(df, pd_multiplier=multiplier, lgd_add=0.10, ead_multiplier=1.05)
        )
        capital = float(stressed["irb_capital"].sum()) + concentration_addon_amount
        if capital >= available_capital:
            return {
                "breach_pd_multiplier": round(multiplier, 10),
                "capital_at_breach": capital,
                "available_capital": available_capital,
            }
        multiplier += step
    return {
        "breach_pd_multiplier": None,
        "capital_at_breach": None,
        "available_capital": available_capital,
    }
