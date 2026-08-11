# GitHub / Zenodo publication checklist

## 1. Historical reference remains unchanged

Original software:

- GitHub: https://github.com/marcorighi/RPDindex
- DOI: https://doi.org/10.5281/zenodo.20313771

Do not rewrite or replace this historical artifact when publishing `RPDindexOptimized`.

## 2. Validate the new repository locally

From the repository root:

```bash
python3 tests/test_equivalence.py
python3 benchmarks/benchmark.py --sizes 100 300 1000
```

Record the benchmark environment before making performance claims.

## 3. Check repository contents

Confirm that the first public commit contains no:

- passwords, tokens, API keys, or SSH material;
- private datasets;
- local absolute paths;
- editor caches or temporary files;
- generated benchmark output that has not been reviewed.

## 4. Publish to GitHub

The included script can create/push the repository:

```bash
./deploy_RPDindexOptimized.sh
```

Target repository:

```text
https://github.com/marcorighi/RPDindexOptimized
```

## 5. Before the first formal release

- choose and add an explicit software license;
- verify authors and affiliations;
- run tests on actual research datasets;
- run documented benchmarks;
- finalize the technical report;
- update `CITATION.cff` with the release version/date;
- create a release tag, e.g. `v1.0.0`;
- connect/archive the repository in Zenodo;
- add the resulting Zenodo DOI for `RPDindexOptimized` to `README.md` and `CITATION.cff`.

## 6. Suggested release command

When the exact archived state is final:

```bash
git tag -a v1.0.0 -m "Validated optimized RPD implementation"
git push origin main --tags
```

Do not move or rewrite the archived tag after Zenodo has minted a DOI for it.
