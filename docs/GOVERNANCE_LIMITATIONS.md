# Governance, assumptions and limitations

This repository demonstrates credit portfolio risk methodology. It is not a regulatory submission, an ICAAP, a capital plan or investment advice.

## What is synthetic / illustrative

- the obligor and facility portfolio;
- rating transition probabilities;
- PD/LGD/EAD portfolio parameters;
- concentration add-on thresholds;
- stress-severity assumptions;
- illustrative available capital;
- reverse-stress management threshold.

## What is implemented analytically

- corporate-style IRB capital mechanics;
- maturity adjustment and PD-dependent asset correlation;
- expected-loss and RWA aggregation;
- EAD concentration metrics and HHI;
- one-factor Gaussian credit-loss simulation;
- loss VaR, Expected Shortfall and economic capital;
- migration, stress and reverse-stress calculations;
- an auditable ICAAP-style internal capital stack.

## Production requirements

A real financial institution would need governed exposure data, applicable regulatory asset-class mapping, validated default definitions, downturn LGD, CCF/EAD models where relevant, approved rating systems, current regulations, stress calibration, finance reconciliation, independent validation, model risk governance, change control, audit trail and senior-management approval.
