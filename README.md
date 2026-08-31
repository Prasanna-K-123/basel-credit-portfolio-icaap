# Basel Credit Portfolio, Economic Capital & ICAAP

A reproducible **credit portfolio risk and capital analytics platform** covering Basel-style corporate IRB capital, expected/unexpected loss, concentration risk, rating migration, one-factor economic capital, stress testing, reverse stress testing and an ICAAP-style internal capital assessment.

The implementation is intentionally explicit about evidence: the portfolio and several governance assumptions are **synthetic/illustrative**, while the mathematical risk engine is fully reproducible and tested. It does not present invented bank data as empirical evidence.

## What this repository demonstrates

| Layer | Implementation |
|---|---|
| Portfolio controls | deterministic 5,000-obligor synthetic corporate book with rating/sector/region/EAD/PD/LGD/maturity |
| Expected loss | obligor-level `PD × LGD × EAD` aggregation |
| Basel-style capital | corporate IRB one-factor capital formula, PD-dependent correlation, maturity adjustment, RWA |
| Concentration risk | obligor/sector/region HHI, top-name shares, transparent ICAAP concentration add-on |
| Rating migration | one-year transition matrix, downgrade/default exposure analytics |
| Economic capital | one-factor Gaussian/Vasicek conditional PDs, 100,000 loss simulations, 99%/99.9% VaR & ES |
| Stress testing | mild/adverse/severe PD-LGD-EAD shocks and capital impact |
| Reverse stress | searches for deterioration required to exhaust illustrative capital resources |
| ICAAP-style assessment | core credit capital + concentration add-on + stress overlay + capital buffer |
| Governance | assumption register, methodological limits and production-remediation requirements |
| Reproducibility | unit tests + GitHub Actions + generated risk committee-style report |

## Verified reproducible evidence

The current green CI run generates the following evidence from the deterministic synthetic portfolio:

- **5,000 obligors / 16.56bn total EAD**, with EAD-weighted PD **2.58%** and LGD **43.78%**;
- expected loss **185.1m**, Basel-style IRB capital **1.395bn**, and RWA **17.438bn**;
- across **100,000** one-factor credit-loss simulations, 99.9% loss VaR **1.278bn**, 99.9% Expected Shortfall **1.457bn**, and 99.9% economic capital above model EL **1.093bn**;
- sector HHI **0.1490**, top-10 obligor exposure share **3.09%**, and largest-sector share **19.06%**;
- severe PD/LGD/EAD stress raises Basel-style credit capital to approximately **2.768bn**;
- the illustrative reverse-stress boundary is reached at a **1.60× PD multiplier** with the stated +10pp LGD and +5% EAD assumptions.

These are **model-generated synthetic-portfolio results**, not observed bank performance or regulatory capital figures. See [`outputs/metrics.json`](outputs/metrics.json) and [`reports/generated/icaap_assessment.md`](reports/generated/icaap_assessment.md).

## Why this is separate from a PD-model project

A borrower scorecard answers **who is likely to default**. Portfolio risk and capital management ask a different set of questions: how losses co-move, how concentrations affect capital, what tail losses look like, how rating migration changes risk, and whether capital remains adequate under stress.

This repository therefore focuses on **portfolio-level risk aggregation and capital adequacy**, not another classification model.

## Run locally

```bash
python -m pip install -r requirements.txt
python -m pytest
python run_pipeline.py
```

The pipeline regenerates:

- `outputs/metrics.json`
- `outputs/synthetic_portfolio_with_capital.csv`
- `outputs/stress_summary.csv`
- `outputs/migration_summary.csv`
- `reports/generated/icaap_assessment.md`
- `reports/generated/loss_distribution.png`
- `reports/generated/sector_exposure.png`

## Repository map

```text
src/
  portfolio.py          synthetic portfolio generation + validation
  basel_irb.py          corporate IRB capital and RWA
  concentration.py      HHI, top-name shares and concentration add-on
  migration.py          rating migration analytics
  economic_capital.py   one-factor loss simulation, VaR/ES/economic capital
  stress.py             PD/LGD/EAD stress scenarios
  icaap.py              internal capital stack + reverse stress
  reporting.py          figures and risk committee-style report
tests/                  unit tests for formulas, simulation and stress logic
docs/                   methodology, ICAAP framing, governance limitations
run_pipeline.py         end-to-end evidence pipeline
```

## Evidence standard

No real-bank portfolio, capital resource or migration history is claimed. Synthetic inputs are used because institution-level exposure and regulatory capital data are not public in the form needed for this exercise. The value of the project is the **risk architecture, quantitative implementation, reproducibility, governance discipline and explicit limitations**.

Only generated values under `outputs/` and the corresponding generated report are used as quantitative evidence.
