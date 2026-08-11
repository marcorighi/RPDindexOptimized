# Validation protocol

## Objective

The objective is to provide regression evidence that `RPDindexOptimized` reproduces outputs from the original/reference implementation over the declared compatibility domain while reducing the computational complexity of the global indices.

This is software regression evidence, not a formal mathematical proof of equivalence.

## Historical baseline

Authoritative original software:

- GitHub: https://github.com/marcorighi/RPDindex
- Zenodo DOI: https://doi.org/10.5281/zenodo.20313771

A fixed archival snapshot is stored locally as:

```text
reference/computeindex_reference.py
```

The optimized implementation is:

```text
src/computeindex_optimized.py
```

## Compatibility domain

The automated validation covers finite Python `int` and `float` values and sequences of length at least two. Test data include:

- strictly increasing sequences;
- strictly decreasing sequences;
- constant sequences;
- mixed trends;
- repeated values/ties;
- negative values;
- fractional values.

## Automated regression test

Execute:

```bash
python3 tests/test_equivalence.py
```

The deterministic suite uses pseudo-random seed `20260811` and compares all six functions on:

- 8 fixed sequences;
- 300 pseudorandom sequences for each length from 2 through 30;
- 6 RPD functions for every sequence.

This yields 52,248 reference-versus-optimized comparisons.

Random values are generated from integers in `[-10, 10]` divided by 3, deliberately producing negative values, fractional values, and ties.

The test also verifies `progressive_indices()` against repeated prefix evaluation of each optimized function.

## Numerical criterion

Reference-versus-optimized values are compared using:

```python
math.isclose(reference, optimized, rel_tol=1e-12, abs_tol=1e-12)
```

A tolerance is required because the O(n log n) global algorithms change the accumulation order relative to explicit pair enumeration, and binary floating-point addition is not associative.

## Previously observed deterministic validation

During preparation of this optimized version, all 52,248 comparisons passed. The previously observed maximum absolute discrepancies were approximately:

| Function | Maximum absolute discrepancy |
|---|---:|
| `RPDlep` | 2.22e-16 |
| `RPDlea` | 0 |
| `RPDlepr` | 0 |
| `RPDgep` | 1.11e-15 |
| `RPDgea` | 3.89e-16 |
| `RPDgepr` | 3.89e-16 |

Exact round-off magnitudes may depend on interpreter/platform details.

## Edge cases

For sequences of length zero or one, the optimized implementation returns `0.0` for all six functions. These inputs are intentionally outside the strict equivalence claim because the reference implementation does not behave uniformly and `RPDlep`/`RPDgep` can raise `ZeroDivisionError`.

## Recommended checks before Zenodo release

Before assigning a DOI to `RPDindexOptimized`, also archive:

1. tests on the actual datasets used by the associated research workflow;
2. large random stress tests;
3. adversarial cases with many ties and highly unbalanced magnitudes;
4. benchmark output with hardware, OS, Python version, and command line;
5. the Git commit hash identifying the exact tested implementation.
