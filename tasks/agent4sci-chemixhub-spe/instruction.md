# CheMixHub: polymer conductivity

Improve **mae** (native; **minimize**) for
**CheMixHub/SPE**. Only this subtask is scored.

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

Five fixed CV folds; solid polymer electrolyte target ln(kappa); MAE in the original target space.

Required measurement components: `fold_0, fold_1, fold_2, fold_3, fold_4`.
The reproduction baseline is **0.215** in the metric
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

**Paper:** CheMixHub: Datasets and Benchmarks for Chemical Mixture Property Prediction (NeurIPS 2025 Datasets and Benchmarks)

## Metrics to Optimize

**MAE**: lower is better

| Dataset | Task (Target Property) | Paper (MAE) | Reproduction (MAE) |
|------|-----------------|-------------|---------------------|
| Olfactory Mixtures | Perceptual Similarity | 0.121 ± 0.006 | 0.124 ± 0.006 |
| Fuel Mixtures | MON | 4.570 ± 0.348 | 4.699 ± 0.226 |
| Solid Polymer Electrolytes | ln(κ) | 0.222 ± 0.007 | 0.215 ± 0.007 |

**Note:** Evaluation uses 5-fold cross-validation (report mean ± std on test sets). Official scripts: `repo/scripts/run_cv.py`.
