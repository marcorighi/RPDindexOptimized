#!/usr/bin/env python3
"""Deterministic regression tests for RPDindexOptimized."""

from __future__ import annotations

import importlib.util
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


reference = load_module(
    "computeindex_reference", ROOT / "reference" / "computeindex_reference.py"
)
optimized = load_module(
    "computeindex_optimized", ROOT / "src" / "computeindex_optimized.py"
)

FUNCTIONS = (
    "RPDlep",
    "RPDlea",
    "RPDlepr",
    "RPDgep",
    "RPDgea",
    "RPDgepr",
)

REL_TOL = 1e-12
ABS_TOL = 1e-12
SEED = 20260811

FIXED = [
    [1, 2, 4, 6],
    [6, 4, 2, 1],
    [1, 1, 1, 1],
    [1, 3, 2, 5, 4, 4],
    [-3, -1, -2, 4, 0],
    [0, 0.5, -0.5, 0.5, -0.5],
    [1e-9, 1e9, -1e9, 2e-9],
    [0.0183179687636068, 0.66165806279797, 1, 6.51487788578436e-10],
]


def assert_close(a: float, b: float, context: str) -> float:
    diff = abs(a - b)
    if not math.isclose(a, b, rel_tol=REL_TOL, abs_tol=ABS_TOL):
        raise AssertionError(f"{context}: reference={a!r}, optimized={b!r}, diff={diff!r}")
    return diff


def main() -> int:
    rng = random.Random(SEED)
    sequences = list(FIXED)

    for length in range(2, 31):
        for _ in range(300):
            sequences.append([rng.randint(-10, 10) / 3 for _ in range(length)])

    maxima = {name: 0.0 for name in FUNCTIONS}
    comparisons = 0

    for seq_no, seq in enumerate(sequences):
        for name in FUNCTIONS:
            ref_value = getattr(reference, name)(seq)
            opt_value = getattr(optimized, name)(seq)
            diff = assert_close(ref_value, opt_value, f"sequence={seq_no}, function={name}")
            maxima[name] = max(maxima[name], diff)
            comparisons += 1

    # Progressive consistency: compare against repeated optimized evaluation.
    progressive_sequences = FIXED + [
        [rng.randint(-20, 20) / 7 for _ in range(length)]
        for length in range(2, 41)
    ]

    progressive_checks = 0
    for seq_no, seq in enumerate(progressive_sequences):
        trajectories = optimized.progressive_indices(seq)
        for name in FUNCTIONS:
            expected = [getattr(optimized, name)(seq[:k]) for k in range(2, len(seq) + 1)]
            actual = trajectories[name]
            if len(actual) != len(expected):
                raise AssertionError(
                    f"progressive length mismatch sequence={seq_no}, function={name}"
                )
            for k, (a, b) in enumerate(zip(expected, actual), start=2):
                if not math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-11):
                    raise AssertionError(
                        f"progressive mismatch sequence={seq_no}, function={name}, prefix={k}: "
                        f"expected={a!r}, actual={b!r}"
                    )
                progressive_checks += 1

    print(f"PASS: {comparisons:,} reference-vs-optimized comparisons")
    print(f"PASS: {progressive_checks:,} progressive consistency comparisons")
    print("Maximum absolute discrepancy by function:")
    for name in FUNCTIONS:
        print(f"  {name:8s}: {maxima[name]:.17g}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
