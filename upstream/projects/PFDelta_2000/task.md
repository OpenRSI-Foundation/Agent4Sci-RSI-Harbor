# Hill Climbing Task

**Paper:** PFΔ: A Benchmark Dataset for Power Flow under Load, Generation, and Topology Variations

## Metrics to Optimize

**Average PBL at GNN-comparable latency**: lower is better

| Task | Description | Best Baseline Model | Baseline Result (from Reproduction) |
|------|-------------|---------------------|-------------------------------------|
| Full-Topology Training (1.3) | Train on all topologies (N, N-1, N-2) | CANOS-PF | 1.18 ± 0.13 |

**Note:** This task uses the GOC-2000 bus system, which is **not evaluated in the original paper** — the paper only reports results for IEEE-14/30/57/118 and GOC-500. NR solvers fail to converge reliably on GOC-2000, making ML methods the only viable approach for real-time applications at this scale.

Average PBL Mean is the mean across all four test conditions (N, N-1, N-2, close-to-infeasible), equally weighted. Results are mean ± std across **3 runs** with different random weight initializations.

The original paper emphasizes that ML methods are needed for **fast, scalable solvers** on large grids. At 2000-bus scale, this is especially critical: NR takes ~681ms per sample on GPU, while ML methods operate at ~10-55ms per sample (unbatched). The goal is to achieve the best possible PBL within GNN-comparable inference latency (~10-55ms unbatched, ~1-3ms batched on a single GPU).

Per-condition baseline results (CANOS-PF, 3 seeds):

| Test Condition | Seed 11 | Seed 22 | Seed 33 | Mean ± Std |
|----------------|:-------:|:-------:|:-------:|:----------:|
| N (feasible) | 1.14 | 1.08 | 1.42 | 1.21 ± 0.15 |
| N-1 (feasible) | 1.05 | 1.00 | 1.25 | 1.10 ± 0.11 |
| N-2 (feasible) | 1.10 | 1.04 | 1.34 | 1.16 ± 0.13 |
| Close-to-infeasible | 1.19 | 1.12 | 1.45 | 1.25 ± 0.14 |
| **Avg PBL Mean** | **1.12** | **1.06** | **1.37** | **1.18 ± 0.13** |

See `reproduction/runs/CHANGES.md` for full reproduction details including all models (CANOS-PF, GNS-S, NR), training configs, and inference timing.

## Data

- **Bus system:** GOC-2000 (2000 buses, ~5600 branches)
- **Train:** 24,300 samples (8,100 per topology: N, N-1, N-2)
- **Val:** 2,700 samples (900 per topology)
- **Test:** 3,300 feasible (1,000 per topology) + 300 C2I (100 per topology)
- **Note:** GOC-2000 has half the samples of other bus sizes due to data generation cost
