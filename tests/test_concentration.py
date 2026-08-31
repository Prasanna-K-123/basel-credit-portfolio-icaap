import pandas as pd

from src.concentration import concentration_metrics, hhi_from_exposure


def test_equal_exposure_hhi():
    assert abs(hhi_from_exposure(pd.Series([1, 1, 1, 1])) - 0.25) < 1e-12


def test_concentration_metrics_shares():
    df = pd.DataFrame(
        {
            "ead": [50.0, 30.0, 20.0],
            "sector": ["a", "b", "b"],
            "region": ["x", "x", "y"],
        }
    )
    m = concentration_metrics(df)
    assert abs(m["top_1_share"] - 0.5) < 1e-12
    assert m["largest_sector_share"] == 0.5
