# Hill Climbing Task

**Paper:** DART-Eval: A Comprehensive DNA Language Model Evaluation Benchmark on Regulatory DNA (NeurIPS 2024 Datasets and Benchmarks)

## Metrics to Optimize

**Spearman r (test_spearman_pos)**: higher is better

| Task | Metric | Paper | Reproduction (Baseline) |
|------|--------|-------|-------------------------|
| Task 4 Chromatin Activity Prediction (GM12878) | Spearman r (`test_spearman_pos`) | 0.515 | 0.544 |

**Note:** The baseline is Nucleotide Transformer v2-500m (494M params, single run, Table 5 in the paper). The paper uses LoRA fine-tuning; for reproduction and hill climbing, use full fine-tuning instead, which may achieve comparable performance to the paper-reported SOTA ChromBPNet (ab initio CNN) at 0.540.
