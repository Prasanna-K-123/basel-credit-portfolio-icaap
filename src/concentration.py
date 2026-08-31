from __future__ import annotations

import numpy as np
import pandas as pd


def hhi_from_exposure(exposure: pd.Series) -> float:
    exposure = pd.Series(exposure, dtype=float)
    total = float(exposure.sum())
    if total <= 0:
        raise ValueError("Total exposure must be positive")
    shares = exposure / total
    return float(np.square(shares).sum())


def concentration_metrics(df: pd.DataFrame) -> dict:
    total = float(df["ead"].sum())
    obligor_hhi = hhi_from_exposure(df["ead"])
    sector = df.groupby("sector")["ead"].sum().sort_values(ascending=False)
    region = df.groupby("region")["ead"].sum().sort_values(ascending=False)

    return {
        "total_ead": total,
        "obligor_hhi": obligor_hhi,
        "sector_hhi": hhi_from_exposure(sector),
        "region_hhi": hhi_from_exposure(region),
        "top_1_share": float(df["ead"].max() / total),
        "top_10_share": float(df.nlargest(10, "ead")["ead"].sum() / total),
        "top_20_share": float(df.nlargest(20, "ead")["ead"].sum() / total),
        "largest_sector": str(sector.index[0]),
        "largest_sector_share": float(sector.iloc[0] / total),
    }


def concentration_addon(irb_capital: float, metrics: dict) -> float:
    sector_excess = max(metrics["sector_hhi"] - 0.14, 0.0)
    top10_excess = max(metrics["top_10_share"] - 0.10, 0.0)
    scalar = 0.50 * sector_excess + 0.75 * top10_excess
    return float(irb_capital * scalar)
