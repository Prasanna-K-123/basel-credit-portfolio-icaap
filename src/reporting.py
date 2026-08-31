from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tabulate import tabulate


def save_loss_distribution(losses: np.ndarray, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(losses, bins=60)
    ax.set_title("One-factor portfolio credit-loss distribution")
    ax.set_xlabel("Loss")
    ax.set_ylabel("Simulation count")
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def save_sector_exposure(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sector = df.groupby("sector")["ead"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    sector.plot(kind="bar", ax=ax)
    ax.set_title("Synthetic portfolio exposure by sector")
    ax.set_ylabel("EAD")
    ax.set_xlabel("")
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def write_json(data: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def build_icaap_report(metrics: dict, stress: pd.DataFrame, migration: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    p = metrics["portfolio"]
    ec = metrics["economic_capital"]
    c = metrics["concentration"]
    i = metrics["icaap"]
    reverse = metrics["reverse_stress"]
    breach_text = (
        f'{reverse["breach_pd_multiplier"]:.2f}x'
        if reverse["breach_pd_multiplier"] is not None
        else "not reached within search range"
    )

    text = f"""# ICAAP-style credit portfolio assessment

## Executive conclusion

This repository demonstrates a quantitative **credit portfolio, Basel-style IRB,
economic-capital, concentration-risk, migration and stress-testing framework**
on a deterministic synthetic corporate portfolio. It is an educational
risk-management implementation, not a regulatory filing and not institution data.

## Base portfolio

- Obligors: **{p["obligors"]:,}**
- Total EAD: **{p["total_ead"]:,.0f}**
- Expected loss: **{p["expected_loss"]:,.0f}**
- Basel-style IRB capital: **{p["irb_capital"]:,.0f}**
- RWA: **{p["rwa"]:,.0f}**

## Economic capital

- Simulated 99% loss VaR: **{ec["var_99"]:,.0f}**
- Simulated 99.9% loss VaR: **{ec["var_999"]:,.0f}**
- 99.9% economic capital above model EL: **{ec["economic_capital_999"]:,.0f}**
- 99.9% Expected Shortfall: **{ec["es_999"]:,.0f}**

## Concentration

- Obligor HHI: **{c["obligor_hhi"]:.6f}**
- Sector HHI: **{c["sector_hhi"]:.4f}**
- Top-10 obligor EAD share: **{c["top_10_share"]:.2%}**
- Largest sector: **{c["largest_sector"]} ({c["largest_sector_share"]:.2%})**

## ICAAP-style capital stack

- Core credit capital: **{i["core_credit_capital"]:,.0f}**
- Concentration add-on: **{i["concentration_addon"]:,.0f}**
- Stress overlay: **{i["stress_overlay"]:,.0f}**
- Internal capital requirement: **{i["internal_capital_requirement"]:,.0f}**
- Illustrative available capital: **{i["illustrative_available_capital"]:,.0f}**
- Coverage ratio: **{i["capital_coverage_ratio"]:.2f}x**
- Reverse-stress breach: **{breach_text} PD multiplier**, with +10pp LGD and +5% EAD assumptions.

## Stress results

{tabulate(stress, headers="keys", tablefmt="github", showindex=False, floatfmt=".4g")}

## Rating migration

{tabulate(migration, headers="keys", tablefmt="github", showindex=False, floatfmt=".4g")}

## Model-risk judgement

The engine deliberately separates **methodology** from **empirical claims**.
The obligor portfolio, rating transition matrix, capital resources, stress
severity, concentration add-on thresholds and reverse-stress settings are
illustrative. The Basel-style corporate IRB functional form and one-factor
economic-capital mechanics are implemented for analytical demonstration; a
bank implementation would require jurisdiction-specific rules, approved
parameters, validated data, model governance and reconciliation to finance and
regulatory reporting systems.

## Production remediation

1. replace the synthetic portfolio with governed obligor/facility data;
2. map exposures to the applicable regulatory asset classes and current rule set;
3. validate PD/LGD/EAD, maturity, default definitions and downturn parameters;
4. calibrate rating migration and stress scenarios to observed portfolios and macro history;
5. establish concentration limits, risk appetite, capital planning and management actions;
6. perform independent validation, change control, auditability and reporting reconciliation.
"""
    path.write_text(text, encoding="utf-8")
