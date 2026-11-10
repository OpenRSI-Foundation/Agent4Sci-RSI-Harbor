# Hill Climbing Task

**Paper:** MassSpecGym: A benchmark for the discovery and identification of molecules (NeurIPS 2024 Datasets and Benchmarks)

## Metrics to Optimize

**Hit Rate @ 1**: higher is better

| Task | Metric | Paper | Reproduction (Baseline) |
|------|--------|-------|-------------------------|
| Molecule Retrieval | Hit Rate @ 1 | 14.64% | 16.14% |

**Note:** The baseline is MIST (single run, fixed random seed). Evaluation is on the standard molecule retrieval challenge (mass-based candidates, up to 256 candidates per spectrum). Confidence intervals are computed via bootstrapping (20,000 resamples on the test set), not from multiple runs.
