#!/usr/bin/env python3
"""Simple standard-library benchmark for reference vs optimized RPD functions."""

from __future__ import annotations

import argparse
import importlib.util
import platform
import random
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


reference = load_module("computeindex_reference", ROOT / "reference" / "computeindex_reference.py")
optimized = load_module("computeindex_optimized", ROOT / "src" / "computeindex_optimized.py")

FUNCTIONS = ("RPDlep", "RPDlea", "RPDlepr", "RPDgep", "RPDgea", "RPDgepr")


def measure(func, data, repeats: int) -> float:
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        func(data)
        samples.append(time.perf_counter() - start)
    return statistics.median(samples)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", nargs="+", type=int, default=[100, 300, 1000])
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20260811)
    args = parser.parse_args()

    print(f"Python: {platform.python_version()}")
    print(f"Platform: {platform.platform()}")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor() or 'not reported'}")
    print(f"Seed: {args.seed}")
    print(f"Repeats: {args.repeats}")
    print()

    rng = random.Random(args.seed)

    header = f"{'n':>7} {'function':>9} {'reference_s':>14} {'optimized_s':>14} {'speedup':>10}"
    print(header)
    print("-" * len(header))

    for n in args.sizes:
        data = [rng.uniform(-1.0, 1.0) for _ in range(n)]
        for name in FUNCTIONS:
            ref_t = measure(getattr(reference, name), data, args.repeats)
            opt_t = measure(getattr(optimized, name), data, args.repeats)
            speedup = ref_t / opt_t if opt_t > 0 else float("inf")
            print(f"{n:7d} {name:>9s} {ref_t:14.6g} {opt_t:14.6g} {speedup:10.3f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
