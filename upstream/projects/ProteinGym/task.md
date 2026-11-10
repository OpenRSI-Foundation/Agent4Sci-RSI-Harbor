# Hill Climbing Task

**Paper:** ProteinGym: Large-Scale Benchmarks for Protein Fitness Prediction and Design (NeurIPS 2023 Datasets and Benchmarks)

## Papers

`paper/paper.pdf` - ProteinGym benchmark paper
`paper/kermut.pdf` - Kermut paper with model information

## Repo

`repo/` and `reproduction/runs/repo` contain code for training and evaluating Kermut.

## Metrics to Optimize

**Spearman (average)**: higher is better.

| Task | Model | Metric | Paper | Reproduction (Baseline) |
|------|--------|--------|-------|-------------------------|
| Supervised DMS substitution prediction | Kermut | Spearman (average) | 0.657 | 0.6561 |

**Notes:**
* You may evaluate performance on the val set as a reference point for hill-climbing, described in the reference reproduction directory.
* All results are averaged over **3 CV schemes** (random, modulo, contiguous) with 5 folds each.
