# Hill Climbing Task

**Paper:** gRNAde: Geometric Deep Learning for 3D RNA inverse design (ICLR 2025)

## Metrics to Optimize

**Composite Score (average of Recovery and EternaFold scMCC)**: higher is better

| Task | Metric | Paper | Reproduction (Baseline) |
|------|--------|-------|-------------------------|
| Single-state RNA Inverse Design | (Recovery + EternaFold scMCC) / 2 | 0.575 | 0.577 |

**Note:** The composite score balances two complementary aspects of RNA inverse design quality:

| Component | Description | Baseline |
|-----------|-------------|----------|
| Recovery | Fraction of native nucleotides recovered in designed sequences | 0.538±0.03 |
| EternaFold scMCC | 2D self-consistency MCC: whether designed sequences fold into the target secondary structure (evaluated by EternaFold) | 0.612±0.02 |

All results are averaged over **3 runs** with consistent random seeds (0, 1, 2). Both metrics are computed by sampling 16 sequences per structure at temperature 0.1, then averaging across the test set. The baseline is from the 1-state gRNAde configuration on the single-state (Das) split: 1-state input (max_num_conformers=1), autoregressive decoder, equivariant GVP-GNN, 4 encoder + 4 decoder layers, ~2.1M parameters, trained for 50 epochs on the Das single-state split.
