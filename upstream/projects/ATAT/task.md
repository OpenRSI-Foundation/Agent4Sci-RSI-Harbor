# Hill Climbing Task

**Paper:** ATAT: Astronomical Transformer for time series and Tabular data (Astronomy & Astrophysics 2024)

## Metrics to Optimize

**Macro F1**: Higher is better.

| Task | Model | Metric | Paper | Reproduction (Baseline) |
|------|---------|---------|-------|-------------------------|
| ELAsTiCC transient classification | ATAT (LC + MD + Features + MTA variant) | (Mean) Macro F1 (2048 days) | 83.5 ± 0.6 | 82.79 ± 0.57 |

(Mean) Macro F1 is calculated from the mean performance across five folds.

## Notes
- You may evaluate performance on the validation set instead of the test set as the reference point for hill-climbing.
- It may be useful to monitor additional metrics to avoid performance regression during hill-climbing.
    - Precision, recall, and F1 for individual classes
- Training and evaluation occurs across five folds (seeds) - see Data above and the reference implementation in `reproduction/`.
