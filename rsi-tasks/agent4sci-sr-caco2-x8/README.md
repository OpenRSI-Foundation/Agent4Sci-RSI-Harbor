# SR-CACO-2: microscopy super-resolution

RSI task: `rsi/agent4sci-sr-caco2-x8` · Domain: Biology · Track: suite.

This standalone package lives in **Agent4Sci-RSI-Harbor**, at
`rsi-tasks/agent4sci-sr-caco2-x8/`. It follows the
[OpenRSI-Index task format](https://github.com/OpenRSI-Foundation/OpenRSI-Index/blob/8d170deed4591fc7e4306f2d86ff4d9bcffd1288/RSI-Harness/docs/harbor-task-authoring/task-toml.md)
and runs with RSI-Harness. See the [complete collection](../../TASKS.md).

| Field | Value |
|---|---|
| Upstream project/subtask | `SR-CACO-2/sr-x8` |
| Primary scientific metric | `roi_psnr` (dB, maximize) |
| Upstream paper baseline | 29.19 |
| Upstream reproduction baseline | 29.03 (not remeasured here) |
| Required components | CELL0, CELL1, CELL2 |
| Aggregation | mean |
| Work budget | 12 hours, 8 H200 GPUs |
| Judge allocation | 8 GPUs; may time-share the Work pool |
| CPU / RAM / planned disk | 32 cores / 512 GiB / 1 TiB |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

Separate x8 model per cell type, seed 0. Input 64x64, output 512x512. Within each cell average ROI-only PSNR over thresholds 4..10 using canonical code, then equally average three cell types.

From the collection root, preview the launch command (no GPU job is started):

```bash
python3 tools/collection.py run agent4sci-sr-caco2-x8 --gpus 0,1,2,3,4,5,6,7
```

Append `--execute` to launch on a prepared Linux Docker host. This always uses
`reward`, `maximize`, and one final held-out submission. Judge data and outputs
are outside the read-only `/workspace` snapshot. See the collection README for
credentials, dependencies and runtime validation status.

After installing RSI-Harness and configuring agent/verifier authentication as
described in the collection README, the direct command from this repository root is:

```bash
sudo -E "$(command -v rsi-harness)" run "$PWD/rsi-tasks/agent4sci-sr-caco2-x8" \
  --agent codex --agent-auth local --gpus 0,1,2,3,4,5,6,7 \
  --primary-reward reward --score-direction maximize --max-submissions 1
```

See [instruction.md](instruction.md) for the full research/submission contract,
[tests/spec.json](tests/spec.json) for pinned inputs and checksums, and the
[collection README](../../README.md) for execution and trust boundaries.
No validated oracle solution is claimed. The image contains upstream reproduction
code and instructions for independently establishing the baseline.

Source: [Agent4Sci at 74b0e8c4dc55](https://github.com/maszhongming/agent4sci/tree/74b0e8c4dc55610072bed4326b6bfac24dc77377).
Image: `ghcr.io/maszhongming/agent4sci-sr-caco-2@sha256:47ecc2be0c1fc0ceb8b1645078337796aeaa74998cfc983501667c37043f26ad`.
Dataset: `MingZhong/agent4sci@96befc0fb951a312b224af2a33767649d9069a55`.
