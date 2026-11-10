# Mars-Bench: terrain segmentation

RSI task: `rsi/agent4sci-mars-terrain` · Domain: Astronomy · Track: suite.

Format and runtime authority: [OpenRSI-Index](https://github.com/OpenRSI-Foundation/OpenRSI-Index),
Harbor schema 1.4 and RSI-Harness. The public Index path is `rsi-tasks/agent4sci-mars-terrain/`.

| Field | Value |
|---|---|
| Upstream project/subtask | `Mars-Bench/s5mars` |
| Primary scientific metric | `iou` (fraction, maximize) |
| Upstream paper baseline | 0.1806 |
| Upstream reproduction baseline | 0.18 (not remeasured here) |
| Required components | seed_0, seed_1, seed_10, seed_42, seed_123, seed_1000, seed_1234 |
| Aggregation | iqm |
| Work budget | 12 hours, 8 H200 GPUs |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

S5Mars terrain segmentation, ten classes; seven seeds 0,1,10,42,123,1000,1234. Report IQM (scipy 25% trim_mean). Use pinned upstream absent-class IoU behavior (torchmetrics 1.7.0).

From the collection root, preview the launch command (no GPU job is started):

```bash
python3 tools/collection.py run agent4sci-mars-terrain --gpus 0,1,2,3,4,5,6,7
```

Append `--execute` to launch on a prepared Linux Docker host. This always uses
`reward`, `maximize`, and one final held-out submission. Judge data and outputs
are outside the read-only `/workspace` snapshot. See the collection README for
credentials, dependencies and runtime validation status.

See [instruction.md](instruction.md) for the full research/submission contract,
[tests/spec.json](tests/spec.json) for pinned inputs and checksums, and the
[collection README](../../README.md) for execution and trust boundaries.
No validated oracle solution is claimed. The image contains upstream reproduction
code and instructions for independently establishing the baseline.

Source: [Agent4Sci at 74b0e8c4dc55](https://github.com/maszhongming/agent4sci/tree/74b0e8c4dc55610072bed4326b6bfac24dc77377).
Image: `ghcr.io/maszhongming/agent4sci-mars-bench@sha256:e2d6357b3e1f01c567091b6a0fca1500e14b81d11e34255790fecb23a3c82737`.
Dataset: `MingZhong/agent4sci@96befc0fb951a312b224af2a33767649d9069a55`.
