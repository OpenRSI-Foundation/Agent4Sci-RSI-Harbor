# Hill Climbing Task

**Paper:** Mars-Bench: A Benchmark for Evaluating Foundation Models for Mars Science Tasks (NeurIPS 2025 Datasets and Benchmarks)

## Metrics to Optimize

**Average IoU/mAP**: higher is better

| Task | Dataset | Metric | Paper | Reproduction (Baseline) |
|------|---------|--------|-------|-------------------------|
| Mars Terrain Segmentation | mb-s5mars | IoU | 0.1806 | 0.1800 |
| Cone Detection | mb-conequest_det | mAP | 0.1599 | 0.1654 |

**Note:** The best model for segmentation IoU is DPT (Feature Extraction) and the best model for detection mAP is RetinaNet (Feature Extraction). Baselines are from the [official Mars-Bench leaderboard](https://huggingface.co/spaces/Mirali33/Mars-Bench). Results are reported as IQM (InterQuartile Mean) across 7 random seeds (0, 1, 10, 42, 123, 1000, 1234).

Per-task reference:

| Dataset | Task | Classes | Image Size | Train | Val | Test | Bands |
|---------|------|---------|------------|-------|-----|------|-------|
| mb-s5mars | Segmentation | 10 | 1200 x 1200 | 4,997 | 200 | 800 | 3 (RGB) |
| mb-conequest_det | Detection | 1 | 512 x 512 | 1,158 | 167 | 333 | 1 (Grayscale) |
