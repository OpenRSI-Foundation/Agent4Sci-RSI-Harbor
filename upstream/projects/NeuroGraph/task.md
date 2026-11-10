# Hill Climbing Task

**Paper:** NeuroGraph: Benchmarks for Graph Machine Learning in Brain Connectomics (NeurIPS 2023 Datasets and Benchmarks)

## Metrics to Optimize

**MAE**: Lower is better.

| Task | Model | Metric | Paper | Reproduction (Baseline) |
|------|---------|---------|-------|-------------------------|
| HCP Fluid Intelligence | GNN* | Mean Absolute Error (MAE) | 0.264 | 0.272 |

GNN* is implemented as `ResidualGNNs` with `GeneralConv`. Expected runtime for training and evaluation is 30 minutes on a single H200 (see `reproduction/`).

## Notes
* You may evaluate performance on the validation set instead of the test set as the reference point for hill-climbing.
* The paper uses a variant of the standard MAE calculation: examine the reference in `reproduction/` carefully for the correct formula.
* Training and evaluation are conducted with two seeds: report individual and average values.
* Your submission must use a GNN-based architecture: the goal is to improve GNN performance on this task, not to find the best-performing model regardless of architecture. .
