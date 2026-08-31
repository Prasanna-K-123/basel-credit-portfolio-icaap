from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from src.basel_irb import calculate_irb_capital
from src.concentration import concentration_metrics
from src.economic_capital import economic_capital_metrics, simulate_one_factor_losses
from src.icaap import build_icaap_assessment, reverse_stress_pd_multiplier
from src.migration import migration_summary
from src.portfolio import generate_synthetic_portfolio, validate_portfolio
from src.reporting import build_icaap_report, save_loss_distribution, save_sector_exposure, write_json
from src.stress import stress_summary


ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"
REPORTS = ROOT / "reports" / "generated"


def main() -> None:
    portfolio = generate_synthetic_portfolio()
    validate_portfolio(portfolio)
    base = calculate_irb_capital(portfolio)
    concentration = concentration_metrics(base)

    losses = simulate_one_factor_losses(base)
    ec = economic_capital_metrics(base, losses)

    stress = stress_summary(portfolio)
    severe_capital = float(stress.loc[stress["scenario"].eq("severe"), "irb_capital"].iloc[0])
    icaap = build_icaap_assessment(base, ec["economic_capital_999"], severe_capital)
    reverse = reverse_stress_pd_multiplier(
        base,
        available_capital=icaap["illustrative_available_capital"],
        concentration_addon_amount=icaap["concentration_addon"],
    )
    migration = migration_summary(base)

    metrics = {
        "methodology_flags": {
            "portfolio_data": "synthetic illustrative corporate portfolio",
            "transition_matrix": "illustrative",
            "capital_resources": "illustrative",
            "stress_scenarios": "illustrative",
            "regulatory_status": "methodology demonstration; not regulatory reporting",
        },
        "portfolio": {
            "obligors": int(len(base)),
            "total_ead": float(base["ead"].sum()),
            "weighted_average_pd": float(np.average(base["pd"], weights=base["ead"])),
            "weighted_average_lgd": float(np.average(base["lgd"], weights=base["ead"])),
            "expected_loss": float(base["expected_loss"].sum()),
            "irb_capital": float(base["irb_capital"].sum()),
            "rwa": float(base["rwa"].sum()),
        },
        "concentration": concentration,
        "economic_capital": ec,
        "icaap": icaap,
        "reverse_stress": reverse,
    }

    OUTPUTS.mkdir(exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    base.to_csv(OUTPUTS / "synthetic_portfolio_with_capital.csv", index=False)
    stress.to_csv(OUTPUTS / "stress_summary.csv", index=False)
    migration.to_csv(OUTPUTS / "migration_summary.csv", index=False)
    write_json(metrics, OUTPUTS / "metrics.json")
    save_loss_distribution(losses, REPORTS / "loss_distribution.png")
    save_sector_exposure(base, REPORTS / "sector_exposure.png")
    build_icaap_report(metrics, stress, migration, REPORTS / "icaap_assessment.md")

    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
