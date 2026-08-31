from src.basel_irb import calculate_irb_capital
from src.economic_capital import economic_capital_metrics, simulate_one_factor_losses
from src.icaap import build_icaap_assessment
from src.portfolio import generate_synthetic_portfolio
from src.stress import stress_summary


def test_stress_increases_credit_capital():
    df = generate_synthetic_portfolio(n=500, seed=10)
    s = stress_summary(df)
    base = float(s.loc[s["scenario"].eq("base"), "irb_capital"].iloc[0])
    severe = float(s.loc[s["scenario"].eq("severe"), "irb_capital"].iloc[0])
    assert severe > base


def test_icaap_stack_has_positive_buffer():
    df = generate_synthetic_portfolio(n=500, seed=10)
    base = calculate_irb_capital(df)
    losses = simulate_one_factor_losses(base, n_simulations=2000, seed=12)
    ec = economic_capital_metrics(base, losses)
    s = stress_summary(df)
    severe = float(s.loc[s["scenario"].eq("severe"), "irb_capital"].iloc[0])
    result = build_icaap_assessment(base, ec["economic_capital_999"], severe)
    assert result["internal_capital_requirement"] > 0
    assert result["capital_coverage_ratio"] > 1.0
