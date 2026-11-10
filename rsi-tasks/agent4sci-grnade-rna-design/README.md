# gRNAde: 3D RNA inverse design

RSI task: `rsi/agent4sci-grnade-rna-design` · Domain: Bioengineering · Track: suite.

This standalone package lives in **Agent4Sci-RSI-Harbor**, at
`rsi-tasks/agent4sci-grnade-rna-design/`. It follows the
[OpenRSI-Index task format](https://github.com/OpenRSI-Foundation/OpenRSI-Index/blob/8d170deed4591fc7e4306f2d86ff4d9bcffd1288/RSI-Harness/docs/harbor-task-authoring/task-toml.md)
and runs with RSI-Harness. See the [complete collection](../../TASKS.md).

| Field | Value |
|---|---|
| Upstream project/subtask | `gRNAde/single_state` |
| Primary scientific metric | `recovery_scmcc_composite` (fraction, maximize) |
| Upstream paper baseline | 0.575 |
| Upstream reproduction baseline | 0.577 (not remeasured here) |
| Required components | seed_0, seed_1, seed_2 |
| Aggregation | mean |
| Work budget | 12 hours, 8 H200 GPUs |
| Judge allocation | 8 GPUs; may time-share the Work pool |
| CPU / RAM / planned disk | 32 cores / 512 GiB / 1 TiB |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

Das single-state split, max_num_conformers=1; seeds 0,1,2. Sample 16 sequences per structure at temperature0.1. Each component=(Recovery+EternaFold scMCC)/2; average full test structures and seeds. Do not substitute a different folding evaluator.

From the collection root, preview the launch command (no GPU job is started):

```bash
python3 tools/collection.py run agent4sci-grnade-rna-design --gpus 0,1,2,3,4,5,6,7
```

Append `--execute` to launch on a prepared Linux Docker host. This always uses
`reward`, `maximize`, and one final held-out submission. Judge data and outputs
are outside the read-only `/workspace` snapshot. See the collection README for
credentials, dependencies and runtime validation status.

After installing RSI-Harness and configuring agent/verifier authentication as
described in the collection README, the direct command from this repository root is:

```bash
sudo -E "$(command -v rsi-harness)" run "$PWD/rsi-tasks/agent4sci-grnade-rna-design" \
  --agent codex --agent-auth local --gpus 0,1,2,3,4,5,6,7 \
  --primary-reward reward --score-direction maximize --max-submissions 1
```

See [instruction.md](instruction.md) for the full research/submission contract,
[tests/spec.json](tests/spec.json) for pinned inputs and checksums, and the
[collection README](../../README.md) for execution and trust boundaries.
No validated oracle solution is claimed. The image contains upstream reproduction
code and instructions for independently establishing the baseline.

Source: [Agent4Sci at 74b0e8c4dc55](https://github.com/maszhongming/agent4sci/tree/74b0e8c4dc55610072bed4326b6bfac24dc77377).
Image: `ghcr.io/maszhongming/agent4sci-grnade@sha256:7ea16dead2b7ab59330eb622d22c5ad3dc81a4555e41cd96699329e745882724`.
Dataset: `MingZhong/agent4sci@96befc0fb951a312b224af2a33767649d9069a55`.
