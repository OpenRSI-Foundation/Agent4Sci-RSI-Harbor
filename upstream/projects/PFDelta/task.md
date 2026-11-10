# Hill Climbing Task

**Paper:** PFΔ: A Benchmark Dataset for Power Flow under Load, Generation, and Topology Variations (NeurIPS 2025 Datasets and Benchmarks)

## Metrics to Optimize

**Power Balance Loss (Mean)**: lower is better

| Task | Description | Best Baseline Model | Paper (Avg PBL Mean) | Reproduction (Avg PBL Mean) |
|------|-------------|---------------------|----------------------|----------------------------|
| Full-Topology Training (1.3) | Train on all topologies (N, N-1, N-2) | CANOS-PF | 0.40 | 0.39 |

**Note:** This task is on the IEEE-118 bus system. Average PBL Mean is the mean across all four test conditions (N, N-1, N-2, close-to-infeasible), equally weighted. Results are mean ± std across **3 runs** with different random weight initializations.

Newton-Raphson (NR) solvers may achieve excellent PBL on IEEE-118 but require iterative O(n³) Jacobian solves. The motivation of this benchmark is developing ML methods that offer constant-time inference without iterative solving, critical for large grids and real-time applications. Focus on ML-only methods — no NR or other iterative solvers at inference time.

Per-condition PBL Mean for reference:

| Test Condition | Task 1.3 CANOS-PF |
|----------------|-------------------|
| N (unperturbed) | 0.19 ± 0.02 |
| N-1 | 0.21 ± 0.01 |
| N-2 | 0.22 ± 0.01 |
| Close-to-infeasible | 0.97 ± 0.07 |
