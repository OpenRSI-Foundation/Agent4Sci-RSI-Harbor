# Hill Climbing Task

**Paper:** Towards Automated Petrography (NeurIPS 2025 Datasets and Benchmarks)

## Metrics to Optimize

**Macro F1**: higher is better

| Task | Benchmark | Metric | Paper | Reproduction (Baseline) |
|------|-----------|--------|-------|-------------------------|
| 25-class Mineral Classification | LITHOS | Macro F1 | 0.432 ± 0.002 | 0.422 ± 0.003 |

**Note:** The best model is LITHOS Baseline (PolarViT with dual PPL+XPL and alpha-gate fusion). The paper reports mean ± std across 2-fold CV. Since the two folds overlap (Fold 2's test data is Fold 1's training data and vice versa), running both folds would risk data leakage. We run **1 fold only**: train on Fold 1, test on Fold 2. The LITHOS Baseline shows very small variance across folds (F1 0.432 ± 0.002), so a single fold is also representative. There is no official validation split from the paper. Run with 3 seeds (e.g., 0, 42, 123) and report the mean ± std of macro F1.

Reference leaderboard (Table 3, macro-averaged):

| Model | PPL | XPL | Acc | F1 |
|-------|-----|-----|-----|-----|
| ResNet | Y | N | 0.573 ± 0.025 | 0.343 ± 0.013 |
| GoogLeNet | Y | N | 0.579 ± 0.029 | 0.380 ± 0.030 |
| ViT | Y | N | 0.573 ± 0.019 | 0.360 ± 0.018 |
| ViT | N | Y | 0.586 ± 0.009 | 0.382 ± 0.025 |
| Swin Transformer | Y | N | 0.593 ± 0.025 | 0.422 ± 0.010 |
| Swin Transformer | N | Y | 0.604 ± 0.017 | 0.424 ± 0.011 |
| LITHOS Baseline | Y | Y | 0.623 ± 0.019 | 0.432 ± 0.002 |
