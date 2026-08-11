# Technical note: optimization of the RPD index implementation

## 1. Purpose and provenance

`RPDindexOptimized` is a separate research-software artifact derived from the computational semantics of the original RPD implementation. It does not replace the historical software deposited at:

- https://github.com/marcorighi/RPDindex
- https://doi.org/10.5281/zenodo.20313771

The purpose of the new implementation is to reduce computational cost while retaining the intended mathematical interpretation of the six RPD indices for finite numerical sequences with at least two observations.

## 2. Public interface

The optimized module preserves:

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
progressive_indices
```

No third-party Python packages are required.

## 3. Local indices

The reference local functions already have linear asymptotic complexity. The optimization therefore focuses on implementation overhead:

- temporary `positive` and `negative` lists are removed;
- counts and magnitude sums are accumulated directly;
- extra loops used only to sum temporary lists are removed.

The asymptotic cost remains O(n).

## 4. Global indices

The reference global functions explicitly enumerate observation pairs and therefore require O(n²) comparisons for one final value.

The optimized implementation uses:

1. coordinate compression of observed values into ordered ranks;
2. Fenwick trees storing prefix counts and prefix sums.

For each value, these data structures recover in O(log n):

- the number and sum of smaller earlier/later values;
- the number and sum of greater earlier/later values.

Those quantities are sufficient to reconstruct the positive/negative comparison counts and the sums of absolute differences appearing in the original formulas.

## 5. RPDgep

For a current value `x`, if `c_<` preceding values are strictly smaller and sum to `s_<`, the total positive magnitude contributed by those pairs is:

```text
x * c_< - s_<
```

If `c_>` preceding values are strictly greater and sum to `s_>`, the total negative magnitude is:

```text
s_> - x * c_>
```

Accumulating these counts and magnitudes reconstructs the terms used by the reference `RPDgep`. The common total-comparison factor cancels in the final normalized ratio.

## 6. RPDgea

`RPDgea` groups comparisons by the current/head observation. At each position, the optimized implementation obtains positive/negative counts and magnitude sums from the Fenwick structures and applies the same per-group weighting as the reference algorithm.

## 7. RPDgepr

`RPDgepr` is evaluated from right to left. The Fenwick structures then represent values located later in the original sequence, allowing the same reverse grouping to be reconstructed in O(log n) per observation.

## 8. Progressive trajectories

`progressive_indices(elements)` returns values for every prefix `elements[:k]`, `k = 2, ..., n`.

Current total costs for the complete trajectory are:

- `RPDlep`: O(n)
- `RPDlea`: O(n)
- `RPDgep`: O(n log n)
- `RPDgea`: O(n log n)
- `RPDlepr`: O(n²)
- `RPDgepr`: O(n²)

The reverse-weighted definitions require reweighting older comparisons when a new endpoint is appended, so their current progressive forms remain quadratic.

## 9. Floating-point equivalence

The optimized global algorithms sum mathematically equivalent quantities in a different order. Because binary floating-point addition is non-associative, small numerical differences are expected. Regression validation therefore uses tolerance-based comparison rather than exact bitwise identity.

## 10. Short-input behavior

The strict compatibility claim is limited to sequences with at least two elements.

The optimized code returns `0.0` for all six functions for shorter inputs. The reference implementation is not uniform for these cases; `RPDlep` and `RPDgep` can divide by zero when there are no comparisons.

This should be described as explicit input-domain regularization, not as part of the equivalence claim.

## 11. Scope limitations

The current compatibility validation does not establish behavior for `NaN`, infinities, missing-value encodings, NumPy arrays/scalars, `Decimal`, `Fraction`, or arbitrary user-defined numeric classes.

## 12. Reproducibility

Any scientific workflow adopting the optimized implementation should record:

- repository release/version;
- Git commit hash;
- Python version;
- operating system and hardware for performance claims;
- dataset/version;
- regression-test results;
- raw benchmark output.
