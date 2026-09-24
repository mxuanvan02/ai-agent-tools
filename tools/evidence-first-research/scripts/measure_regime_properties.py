#!/usr/bin/env python3
"""Measure the data-regime properties that justify a point-in-time / closed-form
scheduling rule, and show why future-prediction does not help.

Generic template — adapt PATH, RANGE, SAFE_MIN/MAX and the AR-fit import to the
project. Prints five quantities, each mapping to a plain-language claim:

  1. Persistence  (alpha_hat + shock half-life)   -> "near-random-walk, now≈future"
  2. Innovation   (sigma, sigma/RANGE, z to bound) -> "moves tiny vs safe range"
  3. Approach     (% near / outside band)          -> "how often danger is real"
  4. Forecast skill ratio RMSE(AR1)/RMSE(naive)    -> ~1.0 means no trend to exploit
  5. (range compression is argued analytically, see defending-closed-form-design.md)

Run with the project venv: `.venv/bin/python scripts/measure_regime_properties.py`
(LSP 'numpy could not be resolved' is a Pyright-interpreter false positive; the
venv has numpy/scipy — ignore it.)
"""
from __future__ import annotations
import math
import sys
from pathlib import Path
import numpy as np

# --- adapt these to the project ---------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
DATA_PATH = ROOT / "data" / "raw" / "intel_berkeley" / "intel_panel_30motes.npy"
RANGE, SAFE_MIN, SAFE_MAX = 14.0, 18.0, 32.0
TRAIN_N, TEST_LO, TEST_HI, H = 2000, 2000, 4000, 4   # forecast horizon
# AR1Model must expose .fit(train) -> obj with .alpha, .beta
from probe_transmit.forecast import AR1Model  # noqa: E402
# ----------------------------------------------------------------------------


def main():
    data = np.load(DATA_PATH).astype(float)
    train = data[:TRAIN_N]
    ar = AR1Model.fit(train)
    alpha = np.atleast_1d(ar.alpha)

    print("=== 1. Persistence (near-random-walk?) ===")
    print(f"  alpha_hat mean={alpha.mean():.5f} min={alpha.min():.5f} max={alpha.max():.5f}")
    hl = math.log(0.5) / math.log(alpha.mean())
    print(f"  shock half-life = {hl:.0f} steps")

    resid = train[1:] - (train[:-1] * ar.alpha + ar.beta)
    sigma = resid.std()
    print("\n=== 2. Innovation size ===")
    print(f"  per-step sigma = {sigma:.4f} ({sigma/RANGE*100:.2f}% of RANGE)")
    print(f"  {H}-step forecast sd ~ sigma*sqrt(H) = {sigma*math.sqrt(H):.4f}")
    print(f"  a sensor 0.5 from a bound sits at z = {0.5/(sigma*math.sqrt(H)):.1f} sd")

    print("\n=== 3. How often does the field approach a bound? ===")
    near = ((data > SAFE_MAX - 1.0) | (data < SAFE_MIN + 1.0)).mean()
    over = ((data > SAFE_MAX) | (data < SAFE_MIN)).mean()
    print(f"  within 1 unit of a bound: {near*100:.3f}%   outside band: {over*100:.3f}%")

    print("\n=== 4. Forecast skill: does the model beat 'value now'? ===")
    test = data[TEST_LO:TEST_HI]
    err1 = test[1:] - (test[:-1] * ar.alpha + ar.beta)
    errp = test[1:] - test[:-1]
    xh = test[:-H].copy()
    for _ in range(H):
        xh = xh * ar.alpha + ar.beta
    errh = test[H:] - xh
    r1 = np.sqrt((err1**2).mean()); rp = np.sqrt((errp**2).mean()); rh = np.sqrt((errh**2).mean())
    print(f"  AR1 1-step RMSE={r1:.4f}  naive-persistence RMSE={rp:.4f}  ratio={r1/rp:.3f}")
    print(f"  AR1 {H}-step RMSE={rh:.4f}  (>1-step => far forecast only adds variance)")
    print("  ratio ~1.0 => no exploitable trend; predicting the future = repeating now")


if __name__ == "__main__":
    main()
