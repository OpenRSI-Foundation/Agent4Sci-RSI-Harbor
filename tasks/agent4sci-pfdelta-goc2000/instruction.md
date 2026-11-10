# PFDelta-2000: latency-constrained power flow

Improve **average_pbl** (native; **minimize**) for
**PFDelta_2000/task_1_3**. Only this subtask is scored.

## Resources and research surface

The upstream reference allocation is **8 H200 GPUs, 12 hours**. Work under
`/workspace/runs/`: develop model architectures, training methods, features,
preprocessing and inference improvements consistent with the scientific task.
Read `/workspace/task.md`, `/workspace/paper/`, `/workspace/repo/` and
`/workspace/reproduction/` first. Copy code into `runs/` to edit it; keep the
reference code, paper and data unchanged. Install extra packages in a local venv.
The allocation is per task here: splitting a multi-task project changes its
budget accounting relative to upstream's shared project run. Report that fact.

## Fixed evaluation protocol

GOC-2000 case study (outside the 25-task suite). Three seeds 11,22,33; equal mean over N,N-1,N-2,C2I conditions. Verify GNN-comparable latency against co-measured baseline on the SAME hardware/batch protocol; upstream references ~10-55 ms unbatched or ~1-3 ms batched. Report both timing and PBL. The IEEE-118 ML-only rule does NOT apply to this case study.

Required measurement components: `seed_11, seed_22, seed_33`.
The reproduction baseline is **1.18** in the metric
units above. This is an upstream reported value, not a new OpenRSI measurement.

Use training and validation only for iterative development. If no validation
partition exists, define a holdout from training without changing final test
membership. Do not download or inspect test data, including the public upstream
Hub test files. Do not tamper with evaluators or hardcode outputs. The auditor
reviews attempted and reverted violations as well as the final code.

## Final submission

At the end of the budget, stop training, consolidate selected models for ALL
required seeds/folds into `/workspace/runs/best_checkpoints/`, and retain the
loading/inference code in `runs/`. Keep only the selected checkpoints.
Create nonempty `runs/SUMMARY.md` (exact loading commands, checkpoint-to-component
mapping and validation selection), `runs/METHODOLOGY.md` (scientific reasoning,
changes and evidence), and `runs/hillclimb_logs.jsonl` (the COMPLETE agent session
transcript, including failed/reverted attempts). Do not summarize the transcript.
Make artifacts readable by the independent evaluator. Use `rsi-submit` **once**
when final; in plain Harbor, finish your turn instead. Do not tune on final Judge
feedback. The operator must enforce `--max-submissions 1` for upstream-comparable
results. The evaluator and auditor run independently in the Judge and may reject
unsupported loading code, incomplete protocols or incomplete trajectories.

## Reward

The verifier recomputes the raw test metric and requires a CLEAN integrity audit.
Let `d=+1` for maximize and `d=-1` for minimize, `b` be the reproduction baseline,
and `m` the measured metric. `improvement=d*(m-b)/abs(b)` and
`reward=0.5+atan(improvement)/pi`. Higher reward is always better; baseline=0.5.
Missing/failed evaluations produce no valid reward, never a fabricated score.

## Original project context (other subtask rows are context only)

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
