# Hill Climbing Task

**Paper:** GEO-Bench-2: From Performance to Capability, Rethinking Evaluation in Geospatial AI (2025 IEEE International Geoscience and Remote Sensing Symposium)

## Metrics to Optimize

**mIoU** (Multiclass Jaccard Index): higher is better

| Task | Dataset | Metric | Paper | Reproduction (Baseline) |
|------|---------|--------|-------|-------------------------|
| Crop Type Segmentation | PASTIS | mIoU | 43.1 ± 0.1 | 45.9 ± 0.3 |

**Note:** The best model is TerraMind-V1-Large (300M). Baselines are from the [official GEO-Bench-2 leaderboard](https://huggingface.co/spaces/aialliance/GEO-Bench-2-Leaderboard). **Results are reported as mean ± std across 5 random seeds.**

PASTIS leaderboard (mIoU):

| Rank | Model | Params | mIoU |
|------|-------|--------|------|
| 1 | TerraMind-V1-Large | 300M | 43.1 ± 0.1 |
| 2 | TerraMind-V1-Base | 100M | 42.2 ± 0.3 |
| 3 | Clay-V1 ViT-B | 100M | 41.5 ± 0.3 |
| 4 | Prithvi-EO-V2 600M TL | 600M | 39.7 ± 0.3 |
| 5 | Satlas-Swin 100M | 100M | 39.7 ± 0.2 |
| 6 | Prithvi-EO-V2 300M TL | 300M | 39.4 ± 0.4 |
| 7 | DOFA-ViT 300M | 300M | 36.4 ± 0.3 |
| 8 | DinoV3-ViT-L-SAT | 300M | 33.0 ± 0.4 |
| 9 | Satlas-SwinB-Naip | 100M | 31.8 ± 0.4 |
| 10 | ConvNext-XLarge-ImageNet | 390M | 31.6 ± 0.1 |
| 11 | DinoV3-ConvNext-Large-WEB | 230M | 31.5 ± 0.2 |
| 12 | ConvNext-Large-ImageNet | 230M | 31.3 ± 0.3 |
| 13 | Resnet50-DeCUR | 25M | 29.2 ± 0.3 |
| 14 | Resnet50-ImageNet | 25M | 21.8 ± 0.5 |
