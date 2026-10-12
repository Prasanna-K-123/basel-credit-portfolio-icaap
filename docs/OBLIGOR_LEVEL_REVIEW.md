# Obligor-level one-factor credit loss — bounded mathematical correction

The accepted `src/economic_capital.py` model represents every obligor in a common `(rating, sector)` segment by its segment-average PD, LGD and EAD. This is an intentional historical approximation, but its loss distribution cannot retain exposure heterogeneity within a segment, as transparently disclosed in the README. The new `src/obligor_economic_capital.py` is **opt-in**, not used by historical `run_pipeline.py`, and does not alter any previously released empirical VaR or ICAAP conclusion.

## Intuition and proof

When a common macroeconomic state produces a common conditional borrower default probability `q` within a segment, actual obligor weights `w_i = EAD_i * LGD_i` yield independent conditional Bernoulli events. Their conditional portfolio-loss variance is `q(1−q) Σw_i²`. The segment-average replacement treats each default as the same weight `w̄`, with variance `q(1−q) n w̄²`. Subtract to get **`q(1−q) Σ(w_i − w̄)² ≥ 0`**. Positive within-segment weight dispersion strictly attenuates *conditional variance* in the approximation when 0<q<1. This proof **does not** prove a universally larger 99%/99.9% VaR, ES, or any monotonic capital impact, because quantiles need not respect variance ordering.

The opt-in algorithm samples shared standard-normal `Z` plus independent `epsilon_i`, borrower-specific `PD_i`, repository-native `rho(PD_i)` and borrower-specific `LGD_i * EAD_i`. Default occurs when `sqrt(rho_i) Z + sqrt(1−rho_i) epsilon_i < Phi^{-1}(PD_i)`. PD0/PD1 remain deterministic. Bounded scenario batches avoid building a 100,000 x 5,000 matrix. Reproducible fixed-seed/fixed-batch testing; batch changes are not guaranteed to replay identical underlying random-number streams. No extra industry or regulatory calibration is claimed.

## Verification and boundaries

- Separate registration committed BEFORE implementation/testing: `docs/OBLIGOR_LEVEL_REFERENCE_PROTOCOL.md`.
- Tests check mathematical variance identity, same-seed repeat, PD endpoints, correct support {1,99} for a {99,1} two-name portfolio versus historical segment-averaged support {50}, marginal expected-loss convergence and rejection of invalid inputs. The old function, frozen reference outputs and generated reports must remain identical Git blobs.
- Passing a small synthetic test does **not** authorize new 99.9% economic-capital claims, operational limits or regulator-specified internal capital adequacy. Full large-sample re-evaluation would need a separately registered study and adversarial CI audit, outside this bounded method release.
