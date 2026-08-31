import numpy as np
import pandas as pd

from src.migration import TRANSITION_MATRIX, expected_migrated_pd, validate_transition_matrix


def test_transition_rows_sum_to_one():
    validate_transition_matrix()
    assert np.allclose(TRANSITION_MATRIX.sum(axis=1), 1.0)


def test_expected_migrated_pd_is_valid():
    df = pd.DataFrame({"rating": ["A", "BBB", "CCC"]})
    pd1 = expected_migrated_pd(df)
    assert pd1.between(0, 1).all()
    assert pd1.iloc[2] > pd1.iloc[0]
