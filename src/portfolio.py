from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import N_OBLIGORS, RANDOM_STATE, RATING_PDS, REGIONS, SECTORS


def generate_synthetic_portfolio(n: int = N_OBLIGORS, seed: int = RANDOM_STATE) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    ratings = np.array(list(RATING_PDS))
    rating_probs = np.array([0.14, 0.28, 0.28, 0.20, 0.10])

    df = pd.DataFrame(
        {
            "obligor_id": [f"OBL{i:05d}" for i in range(1, n + 1)],
            "rating": rng.choice(ratings, size=n, p=rating_probs),
            "sector": rng.choice(SECTORS, size=n, p=[0.16, 0.19, 0.16, 0.14, 0.10, 0.13, 0.12]),
            "region": rng.choice(REGIONS, size=n, p=[0.28, 0.27, 0.23, 0.22]),
            "ead": rng.lognormal(mean=np.log(2_000_000), sigma=1.0, size=n),
            "maturity": rng.uniform(1.0, 5.0, size=n),
            "secured": rng.binomial(1, 0.56, size=n),
        }
    )

    base_pd = df["rating"].map(RATING_PDS).astype(float)
    sector_pd_multiplier = df["sector"].map(
        {
            "financials": 0.90,
            "industrials": 1.00,
            "consumer": 1.05,
            "technology": 0.85,
            "energy": 1.20,
            "real_estate": 1.25,
            "healthcare": 0.80,
        }
    ).astype(float)

    df["pd"] = np.clip(base_pd * sector_pd_multiplier, 0.0003, 0.35)
    base_lgd = np.where(df["secured"].eq(1), 0.35, 0.55)
    sector_lgd_add = df["sector"].map({"real_estate": -0.05, "energy": 0.05}).fillna(0.0)
    df["lgd"] = np.clip(base_lgd + sector_lgd_add.to_numpy(), 0.20, 0.75)
    return df


def validate_portfolio(df: pd.DataFrame) -> None:
    required = {"obligor_id", "rating", "sector", "region", "ead", "pd", "lgd", "maturity"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if df["obligor_id"].duplicated().any():
        raise ValueError("obligor_id must be unique")
    if (df["ead"] <= 0).any():
        raise ValueError("EAD must be positive")
    if not df["pd"].between(0, 1).all():
        raise ValueError("PD must be in [0, 1]")
    if not df["lgd"].between(0, 1).all():
        raise ValueError("LGD must be in [0, 1]")
