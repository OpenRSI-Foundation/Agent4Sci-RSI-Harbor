# Hill Climbing Task

**Paper:** SR-CACO-2: A Dataset for Confocal Fluorescence Microscopy Image Super-Resolution (NeurIPS 2024 Datasets and Benchmarks)

## Metrics to Optimize

**Average PSNR (ROI)**: higher is better

| Task | Metric | Paper | Reproduction (Baseline) |
|------|--------|-------|-------------------------|
| Super-Resolution X8 | PSNR (ROI) | 29.19 | 29.03 |

**Note:** The baseline is SRCNN, the best-performing method on X8 Mean ROI PSNR from the paper (Table 2). Each cell type (CELL0, CELL1, CELL2) is trained as a separate model at scale X8 (input: 64x64, output: 512x512) with seed 0. PSNR is computed over ROI only (cells, excluding black background), averaged across multiple thresholds {4, 5, 6, 7, 8, 9, 10}. The final metric is the mean PSNR across all 3 cell types (3 training runs total: 1 per cell type).

Per-cell-type reference PSNR (ROI) on X8 test set (SRCNN):

| Cell Type | PSNR (ROI) |
|-----------|------------|
| CELL0 (Survivin) | 33.05 |
| CELL1 (E-cadherin/Tubulin) | 28.04 |
| CELL2 (Histone H2B) | 26.49 |
| **Mean** | **29.19** |
