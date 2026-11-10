# Hill Climbing Task

**Paper:** A Standardized Benchmark for Multilabel Antimicrobial Peptide Classification (NeurIPS 2025 Datasets and Benchmarks)

## Metrics to Optimize

**Overall mAP (%)**: higher is better

| Task | Benchmark | Metric | Paper | Reproduction (Baseline) |
|------|-----------|--------|-------|-------------------------|
| Multilabel AMP Classification | ESCAPE | mAP (%) | 72.1 | 71.8 ± 0.73 |

**Note:** The baseline is the ESCAPE Baseline (Table 2), evaluated using 2-fold cross-validation ensemble across 3 random seeds (42, 1665, 8914), for a total of 6 training runs per method.

Per-class mAP breakdown (ESCAPE Baseline):

| Class | mAP (%) |
|-------|---------|
| Antibacterial | 94.2 ± 0.21 |
| Antiviral | 69.8 ± 0.46 |
| Antifungal | 63.4 ± 0.74 |
| Antiparasitic | 37.6 ± 2.87 |
| Antimicrobial | 95.6 ± 0.04 |
| **Overall** | **72.1 ± 0.60** |
