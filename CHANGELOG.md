# Changelog

## Unreleased — RPDindexOptimized

### Added

- Separate optimized implementation in `src/computeindex_optimized.py`.
- `progressive_indices(elements)` for complete prefix trajectories.
- Fixed archival snapshot of the original implementation for regression testing.
- Deterministic equivalence/regression tests using only the Python standard library.
- Reproducible benchmark script.
- Technical documentation of the algorithmic changes and compatibility domain.
- Citation metadata referencing the original RPDindex repository and Zenodo DOI `10.5281/zenodo.20313771`.

### Changed relative to the reference implementation

- Removed temporary positive/negative value lists from optimized local implementations and replaced them with direct accumulators.
- Replaced explicit O(n²) pair enumeration in `RPDgep`, `RPDgea`, and `RPDgepr` with coordinate compression and Fenwick trees, reducing single-value global-index computation to O(n log n).
- Added internal helpers, type annotations, and a unified final-ratio calculation.

### Numerical compatibility

- For finite numerical sequences with at least two elements, the six optimized public functions are intended to preserve the semantics of the reference implementation.
- Small floating-point round-off differences may occur because arithmetic operations are accumulated in a different order.
- Regression comparisons therefore use tolerance-based comparison rather than bitwise equality.

### Edge-case behavior

- The optimized implementation returns `0.0` for sequences with fewer than two elements for all six indices.
- The original reference implementation is not uniform on these inputs; in particular, `RPDlep` and `RPDgep` can raise `ZeroDivisionError` when there are no comparisons.
