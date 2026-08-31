# ICAAP-style credit portfolio assessment

## Executive conclusion

This repository demonstrates a quantitative **credit portfolio, Basel-style IRB,
economic-capital, concentration-risk, migration and stress-testing framework**
on a deterministic synthetic corporate portfolio. It is an educational
risk-management implementation, not a regulatory filing and not institution data.

## Base portfolio

- Obligors: **5,000**
- Total EAD: **16,560,830,692**
- Expected loss: **185,055,800**
- Basel-style IRB capital: **1,395,038,336**
- RWA: **17,437,979,194**

## Economic capital

- Simulated 99% loss VaR: **790,658,536**
- Simulated 99.9% loss VaR: **1,277,682,361**
- 99.9% economic capital above model EL: **1,092,626,561**
- 99.9% Expected Shortfall: **1,456,810,025**

## Concentration

- Obligor HHI: **0.000552**
- Sector HHI: **0.1490**
- Top-10 obligor EAD share: **3.09%**
- Largest sector: **industrials (19.06%)**

## ICAAP-style capital stack

- Core credit capital: **1,395,038,336**
- Concentration add-on: **6,268,257**
- Stress overlay: **343,340,374**
- Internal capital requirement: **1,744,646,967**
- Illustrative available capital: **2,093,576,360**
- Coverage ratio: **1.20x**
- Reverse-stress breach: **1.60x PD multiplier**, with +10pp LGD and +5% EAD assumptions.

## Stress results

| scenario   |   pd_multiplier |   lgd_add |   ead_multiplier |       ead |   expected_loss |   irb_capital |       rwa |
|------------|-----------------|-----------|------------------|-----------|-----------------|---------------|-----------|
| base       |            1    |      0    |             1    | 1.656e+10 |       1.851e+08 |     1.395e+09 | 1.744e+10 |
| mild       |            1.35 |      0.03 |             1.02 | 1.689e+10 |       2.724e+08 |     1.682e+09 | 2.103e+10 |
| adverse    |            1.85 |      0.08 |             1.05 | 1.739e+10 |       4.258e+08 |     2.116e+09 | 2.645e+10 |
| severe     |            2.6  |      0.15 |             1.1  | 1.822e+10 |       7.123e+08 |     2.768e+09 | 3.46e+10  |

## Rating migration

| rating   |       ead |   downgrade_probability |   default_probability |   expected_default_ead |
|----------|-----------|-------------------------|-----------------------|------------------------|
| A        | 2.322e+09 |                   0.12  |                 0.002 |              4.644e+06 |
| BBB      | 4.853e+09 |                   0.1   |                 0.004 |              1.941e+07 |
| BB       | 4.85e+09  |                   0.115 |                 0.012 |              5.82e+07  |
| B        | 2.899e+09 |                   0.131 |                 0.051 |              1.479e+08 |
| CCC      | 1.637e+09 |                   0.171 |                 0.171 |              2.799e+08 |

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
