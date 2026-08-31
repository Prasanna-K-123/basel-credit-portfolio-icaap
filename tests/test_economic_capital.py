import numpy as np

from src.economic_capital import economic_capital_metrics, simulate_one_factor_losses
from src.portfolio import generate_synthetic_portfolio


def test_simulation_reproducible():
    df = generate_synthetic_portfolio(n=300, seed=7)
    a = simulate_one_factor_losses(df, n_simulations=1000, seed=11)
    b = simulate_one_factor_losses(df, n_simulations=1000, seed=11)
    assert np.array_equal(a, b)


def test_economic_capital_ordering():
    df = generate_synthetic_portfolio(n=300, seed=7)
    losses = simulate_one_factor_losses(df, n_simulations=2000, seed=11)
    m = economic_capital_metrics(df, losses)
    assert m["var_999"] >= m["var_99"] >= 0
    assert m["es_999"] >= m["var_999"]
