# Hill Climbing Task

**Paper:** CosmoBench: A Multiscale, Multiview, Multitask Cosmology Benchmark for Geometric Deep Learning (NeurIPS 2025 Datasets and Benchmarks)

## Metrics to Optimize

**All metrics**: higher is better

| Task | Modality | Metric | Paper | Reproduction (Baseline) | Source |
|------|----------|--------|-------|-------------------------|--------|
| Tree Cosmo Param Regression (CS-Trees) | Directed Trees | R²(σ₈) | 0.82 | 0.808 ± 0.004 | Table 5 (left) |
| Merger Node Classification (CS-Trees-200) | Directed Trees | Accuracy | 0.72 | 0.717 ± 0.005 | Table 5 (right) |
| Velocity Prediction (CAMELS-SAM) | Point Clouds | R²_v | 0.2865 | 0.2830 ± 0.003 | Table 3 |

**Note:** Each task has a separate model and training script. Baselines are the best single-run results across all methods in the paper. The ± values in the paper are from bootstrap resampling on the test set, not from multiple training runs.

Per-task details:

| Task | Source | Best Model | Params | Training Time (1 GPU) | Train/Val/Test Split |
|------|--------|-----------|--------|-----------------------|---------------------|
| Tree Cosmo Param Regression | Table 5 (left) | GNN (MPNN, 4 layers, d=16) | 2.8K | ~13 min | 600/204/196 cosmo param configs, 25 trees each |
| Merger Node Classification | Table 5 (right) | k-NN (k∈[5,25], feature=a) | — | ~12 sec | 120/40/40 trees |
| Velocity Prediction (CAMELS-SAM) | Table 3 | GNN (MPNN, d=64, L selected from {4,5,6}) | 126K | 1-3 hr | 600/204/196 point clouds |

**Tree Cosmo Param Regression:** Predict cosmological parameters (Ω_m, σ₈) from merger tree graphs. Each tree represents a halo's formation history with node features (mass M, concentration c, max circular velocity v_max, scale factor a). R²(Ω_m) = 0.996 is near-saturated; the optimization target is R²(σ₈) = 0.82. The GNN uses directed message-passing from ancestor to descendant nodes with d=16 hidden size (Sec. 5.1).

**Merger Node Classification:** Given a coarsened merger tree with virtual nodes representing potentially unresolved mergers, classify each virtual node as positive (merger exists in fine-grained tree) or negative. Binary classification on the 200 largest trees from CS-Trees. The best baseline is k-NN using only the scale factor feature a with 1-hop neighbor information; the best trainable GNN achieves 0.69 (Sec. 5.2).

**Velocity Prediction (CAMELS-SAM):** Predict the 3D velocity vector of each galaxy from its 3D position in a point cloud. Input point clouds have 5,000 nodes each. Radius graphs are constructed with cutoff R_c = 0.1 * box_size. R²_v is the per-cloud R² (over all nodes and 3 velocity components) averaged across test clouds (Sec. 4.2, Eq. 1).
