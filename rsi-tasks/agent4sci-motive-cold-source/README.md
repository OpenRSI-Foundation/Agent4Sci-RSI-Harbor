# MOTIVE: cold-source link prediction

RSI task: `rsi/agent4sci-motive-cold-source` · Domain: Bioengineering · Track: suite.

This standalone package lives in **Agent4Sci-RSI-Harbor**, at
`rsi-tasks/agent4sci-motive-cold-source/`. It follows the
[OpenRSI-Index task format](https://github.com/OpenRSI-Foundation/OpenRSI-Index/blob/8d170deed4591fc7e4306f2d86ff4d9bcffd1288/RSI-Harness/docs/harbor-task-authoring/task-toml.md)
and runs with RSI-Harness. See the [complete collection](../../TASKS.md).

| Field | Value |
|---|---|
| Upstream project/subtask | `MOTIVE/cold_source` |
| Primary scientific metric | `f1` (fraction, maximize) |
| Upstream paper baseline | 0.2827 |
| Upstream reproduction baseline | 0.2972 (not remeasured here) |
| Required components | run_1, run_2, run_3, run_4, run_5 |
| Aggregation | mean |
| Work budget | 12 hours, 8 H200 GPUs |
| Judge allocation | 8 GPUs; may time-share the Work pool |
| CPU / RAM / planned disk | 32 cores / 512 GiB / 1 TiB |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

st_expanded graph with all edge types, cold-source new-compound split. Five runs at fixed training seed and splits; variation from sampling/nondeterminism. Select checkpoints by validation Hits@500.

From the collection root, preview the launch command (no GPU job is started):

```bash
python3 tools/collection.py run agent4sci-motive-cold-source --gpus 0,1,2,3,4,5,6,7
```

Append `--execute` to launch on a prepared Linux Docker host. This always uses
`reward`, `maximize`, and one final held-out submission. Judge data and outputs
are outside the read-only `/workspace` snapshot. See the collection README for
credentials, dependencies and runtime validation status.

After installing RSI-Harness and configuring agent/verifier authentication as
described in the collection README, the direct command from this repository root is:

```bash
sudo -E "$(command -v rsi-harness)" run "$PWD/rsi-tasks/agent4sci-motive-cold-source" \
  --agent codex --agent-auth local --gpus 0,1,2,3,4,5,6,7 \
  --primary-reward reward --score-direction maximize --max-submissions 1
```

See [instruction.md](instruction.md) for the full research/submission contract,
[tests/spec.json](tests/spec.json) for pinned inputs and checksums, and the
[collection README](../../README.md) for execution and trust boundaries.
No validated oracle solution is claimed. The image contains upstream reproduction
code and instructions for independently establishing the baseline.

Source: [Agent4Sci at 74b0e8c4dc55](https://github.com/maszhongming/agent4sci/tree/74b0e8c4dc55610072bed4326b6bfac24dc77377).
Image: `ghcr.io/maszhongming/agent4sci-motive@sha256:8b66346ddc0976f2eb2639ba0f790b0954e265b03502f5cbe59ea6d127533d79`.
Dataset: `MingZhong/agent4sci@96befc0fb951a312b224af2a33767649d9069a55`.
