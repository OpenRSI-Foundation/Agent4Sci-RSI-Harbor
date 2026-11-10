# Hill Climbing Task

**Paper:** MOTIVE: A Drug-Target Interaction Graph For Inductive Link Prediction (NeurIPS 2024 Datasets and Benchmarks)

## Metrics to Optimize

**F1**: higher is better

| Task | Config | Paper (F1) | Reproduction (F1) |
|------|--------|------------|-------------------|
| Cold-Source Link Prediction (new compounds) | `configs/train/st_expanded/cold_source/gin_cp.json` | 0.2827 ± 0.018 | 0.2972 ± 0.011 |

**Note:** Results are mean ± std across 5 runs (fixed data splits and fixed training seed; variance from batch sampling by the data loader and GPU non-determinism) on the `st_expanded` graph (all edge types). Model selection uses validation Hits@500.
