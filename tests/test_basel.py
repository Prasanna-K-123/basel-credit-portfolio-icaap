import numpy as np
import pandas as pd

from src.basel_irb import asset_correlation, calculate_irb_capital, capital_requirement_rate


def test_asset_correlation_bounds():
    r = asset_correlation(np.array([0.0003, 0.01, 0.10]))
    assert np.all((r >= 0.12) & (r <= 0.24))


def test_capital_rate_positive_and_higher_for_more_risk():
    k = capital_requirement_rate(
        np.array([0.005, 0.05]),
        np.array([0.45, 0.45]),
        np.array([2.5, 2.5]),
    )
    assert np.all(k > 0)
    assert k[1] > k[0]


def test_rwa_identity():
    df = pd.DataFrame({"pd": [0.01], "lgd": [0.45], "ead": [1_000_000.0], "maturity": [2.5]})
    out = calculate_irb_capital(df)
    assert np.isclose(out.loc[0, "rwa"], 12.5 * out.loc[0, "irb_capital"])
