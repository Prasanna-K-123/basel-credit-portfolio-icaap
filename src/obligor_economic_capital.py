"""Opt-in obligor-level Gaussian one-factor credit loss reference.

Does not replace the registered segment-average 100,000-trial historical result.
See docs/OBLIGOR_LEVEL_REFERENCE_PROTOCOL.md for the frozen method and limits.
"""
from __future__ import annotations

from numbers import Integral

import numpy as np
import pandas as pd
from scipy.stats import norm

from src.basel_irb import asset_correlation


def conditional_variance_attenuation(weights, conditional_pd: float) -> float:
    """For common conditional q: exact minus average-weight binomial variance.

    q(1-q) sum[(w_i - mean(w))^2] >= 0; says nothing about monotone VaR.
    """
    w = np.asarray(weights, dtype=float)
    q = float(conditional_pd)
    if w.ndim != 1 or len(w) == 0 or not np.isfinite(w).all() or np.any(w < 0):
        raise ValueError('weights must be a nonempty finite nonnegative vector')
    if not np.isfinite(q) or not 0 <= q <= 1:
        raise ValueError('conditional PD must be finite and within [0,1]')
    return float(q * (1 - q) * np.sum((w - w.mean()) ** 2))


def _validated_obligors(df: pd.DataFrame):
    required = {'obligor_id', 'pd', 'lgd', 'ead'}
    if not isinstance(df, pd.DataFrame) or not required.issubset(df.columns):
        raise ValueError('portfolio must contain obligor_id, pd, lgd, ead')
    if len(df) == 0 or df['obligor_id'].isna().any() or df['obligor_id'].duplicated().any():
        raise ValueError('portfolio must have nonempty unique obligor_id')
    try:
        pdv = df['pd'].to_numpy(dtype=float)
        lgd = df['lgd'].to_numpy(dtype=float)
        ead = df['ead'].to_numpy(dtype=float)
    except (ValueError, TypeError) as exc:
        raise ValueError('PD, LGD and EAD must be numeric') from exc
    if any(not np.isfinite(v).all() for v in (pdv, lgd, ead)):
        raise ValueError('PD, LGD and EAD must be finite')
    if np.any((pdv < 0) | (pdv > 1)) or np.any((lgd < 0) | (lgd > 1)):
        raise ValueError('PD and LGD must be within [0,1]')
    if np.any(ead < 0):
        raise ValueError('EAD must be nonnegative')
    rho = np.asarray(asset_correlation(pdv), dtype=float)
    if not np.isfinite(rho).all() or np.any((rho < 0) | (rho >= 1)):
        raise ValueError('Invalid asset-correlation output')
    return pdv, lgd * ead, rho


def simulate_obligor_one_factor_losses(
    df: pd.DataFrame,
    n_simulations: int = 100_000,
    seed: int = 42,
    batch_size: int = 128,
) -> np.ndarray:
    """Explicit borrower defaults; shared systemic normal + independent idiosyncratic normals.

    Memory scales as O(batch_size * n_obligors) rather than paths * names.
    Batch size controls the random stream ordering; fixed seed and batch repeat exactly.
    """
    for name, value in [('n_simulations', n_simulations), ('batch_size', batch_size)]:
        if not isinstance(value, Integral) or isinstance(value, (bool, np.bool_)) or value <= 0:
            raise ValueError(f'{name} must be a positive integer')
    if not isinstance(seed, Integral) or isinstance(seed, (bool, np.bool_)) or seed < 0:
        raise ValueError('seed must be a nonnegative integer')
    pdv, loss_given_default, rho = _validated_obligors(df)
    critical = norm.ppf(pdv)  # pd=0 -> -inf, pd=1 -> +inf (exact limits)
    systemic_scale = np.sqrt(rho)
    idiosyncratic_scale = np.sqrt(1.0 - rho)
    losses = np.empty(int(n_simulations), dtype=float)
    rng = np.random.default_rng(int(seed))
    for start in range(0, int(n_simulations), int(batch_size)):
        count = min(int(batch_size), int(n_simulations) - start)
        z = rng.standard_normal((count, 1))
        epsilon = rng.standard_normal((count, len(pdv)))
        latent = z * systemic_scale[None, :] + epsilon * idiosyncratic_scale[None, :]
        defaults = latent < critical[None, :]
        losses[start:start + count] = defaults.astype(float) @ loss_given_default
    if not np.isfinite(losses).all() or (losses < 0).any():
        raise ArithmeticError('Invalid loss output')
    return losses
