# Hill Climbing Task

**Paper:** TreeFinder: A US-Scale Benchmark Dataset for Individual Tree Mortality Monitoring Using High-Resolution Aerial Imagery (NeurIPS 2025 Datasets and Benchmarks)

## Metrics to Optimize

**F1 (Dead Tree class)**: higher is better

| Task | Config | Paper (F1 %) | Reproduction (F1 %) |
|------|--------|--------------|---------------------|
| Dead Tree Segmentation | `configs/res_random.yaml` | 51.9 ± 5.5 | 52.6 |

**Note:** Baseline is from Mask2Former (best overall model), mean ± std across 3 runs, evaluated on the standard random 80-10-10 train-val-test split.
