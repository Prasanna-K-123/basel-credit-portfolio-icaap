from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm

from src.basel_irb import asset_correlation
from src.config import N_SIMULATIONS, RANDOM_STATE


def _segments(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby(["rating", "sector"], as_index=False)
        .agg(
            n=("obligor_id", "count"),
            ead=("ead", "sum"),
            pd=("pd", "mean"),
            lgd=("lgd", "mean"),
        )
    )
    grouped["avg_ead"] = grouped["ead"] / grouped["n"]
    grouped["rho"] = asset_correlation(grouped["pd"].to_numpy())
    return grouped


def simulate_one_factor_losses(
    df: pd.DataFrame,
    n_simulations: int = N_SIMULATIONS,
    seed: int = RANDOM_STATE,
) -> np.ndarray:
    seg = _segments(df)
    rng = np.random.default_rng(seed)
    z = rng.standard_normal(n_simulations)
    losses = np.zeros(n_simulations, dtype=float)

    for row in seg.itertuples(index=False):
        pd0 = float(np.clip(row.pd, 1e-8, 1 - 1e-8))
        rho = float(row.rho)
        conditional_pd = norm.cdf(
            (norm.ppf(pd0) - np.sqrt(rho) * z) / np.sqrt(1.0 - rho)
        )
        defaults = rng.binomial(int(row.n), np.clip(conditional_pd, 0, 1))
        losses += defaults * float(row.avg_ead) * float(row.lgd)

    return losses


def economic_capital_metrics(df: pd.DataFrame, losses: np.ndarray) -> dict:
    model_el = float((df["pd"] * df["lgd"] * df["ead"]).sum())
    mean_loss = float(np.mean(losses))
    var_99 = float(np.quantile(losses, 0.99))
    var_999 = float(np.quantile(losses, 0.999))
    es_99 = float(losses[losses >= var_99].mean())
    es_999 = float(losses[losses >= var_999].mean())
    return {
        "model_expected_loss": model_el,
        "simulated_mean_loss": mean_loss,
        "var_99": var_99,
        "var_999": var_999,
        "es_99": es_99,
        "es_999": es_999,
        "economic_capital_99": max(var_99 - model_el, 0.0),
        "economic_capital_999": max(var_999 - model_el, 0.0),
    }
