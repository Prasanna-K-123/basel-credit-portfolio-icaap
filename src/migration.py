from __future__ import annotations

import numpy as np
import pandas as pd

RATINGS = ["A", "BBB", "BB", "B", "CCC", "D"]

TRANSITION_MATRIX = pd.DataFrame(
    [
        [0.88, 0.095, 0.018, 0.004, 0.001, 0.002],
        [0.025, 0.875, 0.075, 0.018, 0.003, 0.004],
        [0.005, 0.045, 0.835, 0.085, 0.018, 0.012],
        [0.001, 0.008, 0.060, 0.800, 0.080, 0.051],
        [0.000, 0.002, 0.012, 0.085, 0.730, 0.171],
        [0.000, 0.000, 0.000, 0.000, 0.000, 1.000],
    ],
    index=RATINGS,
    columns=RATINGS,
)

PD_BY_RATING = {"A": 0.002, "BBB": 0.005, "BB": 0.015, "B": 0.045, "CCC": 0.12, "D": 1.0}


def validate_transition_matrix(matrix: pd.DataFrame = TRANSITION_MATRIX) -> None:
    if list(matrix.index) != list(matrix.columns):
        raise ValueError("Transition matrix must use identical row/column ratings")
    if (matrix.to_numpy() < 0).any():
        raise ValueError("Transition probabilities cannot be negative")
    if not np.allclose(matrix.sum(axis=1).to_numpy(), 1.0):
        raise ValueError("Each transition row must sum to 1")


def expected_migrated_pd(df: pd.DataFrame, matrix: pd.DataFrame = TRANSITION_MATRIX) -> pd.Series:
    validate_transition_matrix(matrix)
    pd_vector = pd.Series(PD_BY_RATING)
    expected = matrix.mul(pd_vector, axis=1).sum(axis=1)
    return df["rating"].map(expected).astype(float)


def migration_summary(df: pd.DataFrame, matrix: pd.DataFrame = TRANSITION_MATRIX) -> pd.DataFrame:
    validate_transition_matrix(matrix)
    exposure = df.groupby("rating")["ead"].sum()
    rows = []
    for rating in matrix.index[:-1]:
        ead = float(exposure.get(rating, 0.0))
        row = matrix.loc[rating]
        downgrade_prob = float(row.loc[RATINGS[RATINGS.index(rating)+1:]].sum())
        default_prob = float(row["D"])
        rows.append({
            "rating": rating,
            "ead": ead,
            "downgrade_probability": downgrade_prob,
            "default_probability": default_prob,
            "expected_default_ead": ead * default_prob,
        })
    return pd.DataFrame(rows)
