# RPDindexOptimized

`RPDindexOptimized` provides an algorithmically optimized Python implementation of the six RPD indices while preserving the intended semantics of the original RPD software for finite numerical sequences containing at least two elements.

This is a **new and separate repository**. It does not replace the original software artifact associated with the published work.

## Original reference implementation

The historical/reference implementation is preserved and cited independently:

- GitHub: https://github.com/marcorighi/RPDindex
- Zenodo DOI: https://doi.org/10.5281/zenodo.20313771

The original repository and Zenodo deposit remain the authoritative archival references for the software version associated with the original publication.

For reproducible regression testing, this repository also contains an archival snapshot of the original `computeindex.py` under `reference/computeindex_reference.py`. That copy is included only as a fixed comparison baseline; development of the original software remains associated with the repository and DOI above.

## Optimized implementation

The optimized implementation is:

```text
src/computeindex_optimized.py
```

It provides the same six principal functions:

```text
RPDlep
RPDlea
RPDlepr
RPDgep
RPDgea
RPDgepr
```

and adds:

```text
progressive_indices(elements)
```

for calculation of complete RPD trajectories over successive prefixes of a sequence.

## Computational complexity

For a sequence of length `n`, the optimized implementation has the following asymptotic costs for a single final index value:

| Function | Reference | Optimized |
|---|---:|---:|
| `RPDlep` | O(n) | O(n) |
| `RPDlea` | O(n) | O(n) |
| `RPDlepr` | O(n) | O(n) |
| `RPDgep` | O(n²) | O(n log n) |
| `RPDgea` | O(n²) | O(n log n) |
| `RPDgepr` | O(n²) | O(n log n) |

The optimized global functions use coordinate compression and Fenwick trees (Binary Indexed Trees) to maintain cumulative counts and sums.

For complete progressive trajectories, `RPDlep`, `RPDlea`, `RPDgep`, and `RPDgea` are updated incrementally. The current progressive implementations of `RPDlepr` and `RPDgepr` remain O(n²).

## Validation

Run:

```bash
python3 tests/test_equivalence.py
```

The deterministic regression suite compares the six optimized functions against the archival reference implementation on fixed and pseudorandom sequences with negative values, fractional values, and ties. Floating-point outputs are compared with explicit tolerances because changing accumulation order can produce small round-off differences.

See [`VALIDATION.md`](VALIDATION.md).

## Benchmark

Run:

```bash
python3 benchmarks/benchmark.py
```

or choose sequence sizes:

```bash
python3 benchmarks/benchmark.py --sizes 100 300 1000 3000
```

Benchmark results depend on hardware, operating system, Python version, system load, and data distribution. Archive the execution environment and raw output before making performance claims in a technical report.

## Repository structure

```text
RPDindexOptimized/
├── README.md
├── CHANGELOG.md
├── CITATION.cff
├── VALIDATION.md
├── LICENSE
├── DOCUMENTATION_LICENSE.md
├── GITHUB_RELEASE_CHECKLIST.md
├── deploy_RPDindexOptimized.sh
├── src/
│   └── computeindex_optimized.py
├── reference/
│   ├── README.md
│   └── computeindex_reference.py
├── tests/
│   └── test_equivalence.py
├── benchmarks/
│   └── benchmark.py
├── docs/
│   └── OPTIMIZATION.md
└── technical_report/
    └── README.md
```

## Compatibility scope

For sequences with `len(elements) >= 2`, the optimized public functions are intended to preserve the mathematical semantics of the reference implementation.

For sequences with fewer than two values, the optimized functions consistently return `0.0`; the reference code does not behave uniformly for those inputs and `RPDlep`/`RPDgep` can raise `ZeroDivisionError`.

The current validation domain covers finite Python `int` and `float` values. `NaN`, infinities, missing-data sentinels, NumPy scalar types, `Decimal`, `Fraction`, and arbitrary numeric classes are not included in the compatibility claim unless separately validated.

## License and citation

### Software source code

The software source code in this repository is released under the
**BSD 3-Clause License**. See [`LICENSE`](LICENSE).

The license permits use, modification, and redistribution, including in
commercial and research contexts, subject to the conditions stated in the
license.

### Documentation and technical report

Unless otherwise stated, the scientific documentation, explanatory material,
repository-specific figures, and accompanying technical report are released
under the **Creative Commons Attribution 4.0 International (CC BY 4.0)**
license.

See [`DOCUMENTATION_LICENSE.md`](DOCUMENTATION_LICENSE.md).

### Scientific citation

When using the mathematical RPD indices, cite the original publication and/or
the original archived software as appropriate.

Original RPD software:

- GitHub: https://github.com/marcorighi/RPDindex
- Zenodo DOI: https://doi.org/10.5281/zenodo.20313771

When using this optimized implementation, please additionally cite the
archived release of `RPDindexOptimized`.

Optimized software DOI:

`<ZENODO_SOFTWARE_DOI>`

If the optimization technical report is deposited separately, please also cite:

`<ZENODO_TECHNICAL_REPORT_DOI>`

The repository citation metadata are maintained in
[`CITATION.cff`](CITATION.cff).
## Contact

Marco Righi  
marco.righi@cnr.it
