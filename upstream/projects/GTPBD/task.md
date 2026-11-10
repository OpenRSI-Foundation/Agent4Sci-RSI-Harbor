# Hill Climbing Task

**Paper:** GTPBD: A Fine-Grained Global Terraced Parcel and Boundary Dataset (NeurIPS 2025 Datasets and Benchmarks)

## Metrics to Optimize

**mIoU**: higher is better

| Task | Metric | Paper | Reproduction (Baseline) |
|------|--------|-------|-------------------------|
| Semantic Segmentation | mIoU (%) | 57.16 | 69.87 |

**Note:** The baseline is Mask2Former, the best-performing method on IoU from the paper (Table 2). The task is binary semantic segmentation on mask_labels (terrace=1, background=0). mIoU is the mean of per-class IoU (background + foreground), matching the official eval script (`caculate_pixel_edge_object.py`). Images are 512x512 patches. The dataset is split 60/20/20 (train/val/test) per geographic region. All paper results are single-run.
