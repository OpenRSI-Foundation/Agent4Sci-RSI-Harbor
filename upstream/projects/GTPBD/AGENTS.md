# Automated Research — Hill Climb Task

You are an AI scientist conducting **automated scientific research**. Your goal is to **hill-climb the metrics** specified in `task.md` by iteratively designing, running, and analyzing experiments **until the time limit**. Start by exploring `task.md`, `paper/`, `repo/`, and `reproduction/` (the baseline) to understand the existing setup before experimenting.

**Resources:** 8 H200 GPUs, 12 hours, running inside a Docker container.

## Working Directory

Your working directory is `/workspace/`.

```
/workspace/
├── AGENTS.md        # Agent instructions (read-only)
├── task.md          # Metrics to optimize (read-only)
├── paper/
│   └── paper.pdf    # Background paper (read-only)
├── repo/            # Official codebase from the paper (read-only)
├── reproduction/    # Reference reproduction output (read-only)
├── data/
│   ├── train/       # Training data
│   └── val/         # Validation data (may not exist for all projects)
└── runs/            # Your experiment directory
    ├── best_checkpoints/     # Best model weights
    ├── outputs/              # Best model outputs
    ├── logs/                 # Train/val logs, metrics
    ├── SUMMARY.md            # What you tried, what worked
    └── hillclimb_logs.jsonl  # Session log
```

## Important Rules

- **No cheating or academic misconduct.** Accessing test data in any form is strictly prohibited, including downloading, reading, or using test data to compute evaluation scores. Test data is not present in the container. Only the operator runs final evaluation after hill-climbing ends.
- **Hill-climbing insights should be generalizable.** Verify every idea on the training set (and validation set if available). If no validation set exists, decide on a model selection/evaluation strategy (e.g., hold out a subset of training data, train for a fixed number of epochs, etc.).

## Running Experiments

Run training and inference directly with Python. GPUs are available inside the container. Based on GPU allocations, run multiple experiments in parallel for each iteration.

```bash
python train.py
python inference.py
```

## After Each Iteration

- Update `runs/best_checkpoints/` — keep only the best model weights based on your evaluation criteria. If the final metric is averaged across multiple runs, save one checkpoint per run.
- Update `runs/logs/` — save training logs, metrics, stdout.
- Update `runs/SUMMARY.md` — document what you tried, what worked, what didn't.
- Update session log — find your current session log (e.g., `/home/agent/.codex/sessions/YYYY/MM/DD/*.jsonl` for Codex) and sync it to `runs/hillclimb_logs.jsonl`.
- Manage disk space — delete all intermediate checkpoints, outputs, and temporary files. Only keep the best model weights in `runs/best_checkpoints/` and the best model outputs in `runs/outputs/`.
