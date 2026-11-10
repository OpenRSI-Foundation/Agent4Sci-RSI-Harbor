# Hill Climbing Task

**Paper:** CheMixHub: Datasets and Benchmarks for Chemical Mixture Property Prediction (NeurIPS 2025 Datasets and Benchmarks)

## Metrics to Optimize

**MAE**: lower is better

| Dataset | Task (Target Property) | Paper (MAE) | Reproduction (MAE) |
|------|-----------------|-------------|---------------------|
| Olfactory Mixtures | Perceptual Similarity | 0.121 ± 0.006 | 0.124 ± 0.006 |
| Fuel Mixtures | MON | 4.570 ± 0.348 | 4.699 ± 0.226 |
| Solid Polymer Electrolytes | ln(κ) | 0.222 ± 0.007 | 0.215 ± 0.007 |

**Note:** Evaluation uses 5-fold cross-validation (report mean ± std on test sets). Official scripts: `repo/scripts/run_cv.py`.
