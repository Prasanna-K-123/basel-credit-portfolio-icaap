# Methodology

## Portfolio layer

The project uses a deterministic synthetic corporate portfolio so that the full analytics stack is reproducible without implying access to confidential bank data. Each obligor has a rating, sector, region, EAD, PD, LGD and maturity.

## Basel-style corporate IRB layer

For each exposure, the engine applies the standard corporate IRB one-factor functional form: PD-dependent asset correlation, a 99.9% systematic-factor quantile, expected-loss subtraction and maturity adjustment. Risk-weighted assets are represented as `12.5 × capital requirement`.

This repository is a methodology implementation. It does not claim compliance with any jurisdiction's complete current capital rules or supervisory interpretation.

## Economic capital

A one-factor Gaussian/Vasicek construction produces conditional default probabilities. Rating-sector segments are simulated with binomial defaults. Portfolio loss VaR and Expected Shortfall are reported at 99% and 99.9%, and economic capital is defined as tail loss VaR less model expected loss.

## Concentration

Single-name, sector and regional concentration are summarised using EAD shares and the Herfindahl-Hirschman Index. A transparent internal concentration add-on is used only for the ICAAP demonstration; it is not presented as a regulatory formula.

## Migration

A clearly labelled illustrative one-year rating transition matrix supports downgrade and default exposure analysis. It is not fitted to empirical agency or bank history.

## Stress and reverse stress

Mild, adverse and severe scenarios increase PD, LGD and EAD. Reverse stress searches for the PD multiplier at which stressed credit capital plus the concentration add-on exhausts illustrative available capital.

## ICAAP-style capital stack

Internal requirement is constructed from the greater of Basel-style credit capital and 99.9% economic capital, plus concentration and stress overlays. The available-capital amount is illustrative so the framework demonstrates capital adequacy logic rather than claiming a real institution's resources.
