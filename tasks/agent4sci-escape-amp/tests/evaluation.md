# Evaluation

The hill-climbing phase is complete. During hill-climbing, the agent had no access to test data. Test data is now available.

## Your Task

Evaluate the best models from the hill-climbing phase on the test set and report final metrics.

## Working Directory

```
/workspace/
├── task.md              # Metrics to evaluate (read-only)
├── paper/paper.pdf      # Background paper (read-only)
├── repo/                # Reference codebase (read-only)
├── reproduction/        # Reference reproduction output (read-only)
├── data/
│   └── {task}/
│       ├── train/
│       ├── val/
│       └── test/        # Now available
└── runs/                # Hill-climbing results
    ├── best_checkpoints/
    ├── outputs/
    ├── logs/
    └── SUMMARY.md
```

## Steps

1. Read `task.md` to understand the evaluation metrics.
2. Read `runs/SUMMARY.md` to understand what the agent tried and what worked.
3. Explore `runs/best_checkpoints/` to find the best model(s).
4. Evaluate the best model(s) on `data/{task}/test/` using `eval_test.py` from `repo/` or `reproduction/`.
5. Report **final metrics** and **compute cost** (GPU hours or CPU time for inference) in `runs/EVAL_RESULTS.md`.
6. Find your current session log (e.g., `/home/agent/.claude/projects/-workspace/*.jsonl` for Claude Code, `/home/agent/.codex/sessions/YYYY/MM/DD/*.jsonl` for Codex, `/home/agent/.gemini/tmp/<project>/chats/session-*.json` for Gemini CLI) and sync it to `runs/eval_logs.jsonl`.
