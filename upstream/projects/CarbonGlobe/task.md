# Hill Climbing Task

**Paper:** CarbonGlobe: A Global-Scale, Multi-Decade Dataset and Benchmark for Carbon Forecasting in Forest Ecosystems (NeurIPS 2025 Datasets and Benchmarks)

## Metrics to Optimize

**Average RMSE**: lower is better

| Task | Metric | Paper | Reproduction (Baseline) |
|------|--------|-------|-------------------------|
| Carbon Forecasting | Average RMSE | 0.571 | 0.604 |

**Note:** A single model predicts all 7 target variables simultaneously. Average RMSE is computed across the 7 variables. The best model for average RMSE is DeepED. Per-variable RMSE for reference:

| Variable | DeepED (RMSE) |
|----------|--------------|
| Height | 1.900 |
| AGB | 0.491 |
| SC | 0.660 |
| LAI | 0.416 |
| GPP | 0.258 |
| NPP | 0.127 |
| Rh | 0.148 |
