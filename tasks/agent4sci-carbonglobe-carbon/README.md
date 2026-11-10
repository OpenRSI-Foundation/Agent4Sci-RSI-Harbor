# CarbonGlobe: carbon forecasting

RSI task: `rsi/agent4sci-carbonglobe-carbon` · Domain: Ecology · Track: suite.

Format and runtime authority: [OpenRSI-Index](https://github.com/OpenRSI-Foundation/OpenRSI-Index),
Harbor schema 1.4 and RSI-Harness. The public Index path is `rsi-tasks/agent4sci-carbonglobe-carbon/`.

| Field | Value |
|---|---|
| Upstream project/subtask | `CarbonGlobe/carbon_forecasting` |
| Primary scientific metric | `average_rmse` (native, minimize) |
| Upstream paper baseline | 0.571 |
| Upstream reproduction baseline | 0.604 (not remeasured here) |
| Required components | all_variables |
| Aggregation | mean |
| Work budget | 12 hours, 8 H200 GPUs |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

One model predicts all seven variables. Compute RMSE per variable with the original normalization, then equally average all seven.

From the collection root, preview the launch command (no GPU job is started):

```bash
python3 tools/collection.py run agent4sci-carbonglobe-carbon --gpus 0,1,2,3,4,5,6,7
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
Image: `ghcr.io/maszhongming/agent4sci-carbonglobe@sha256:2aa02bc4892795b54beb686525e07be4901078e01d3f2b48fd80496a30724367`.
Dataset: `MingZhong/agent4sci@96befc0fb951a312b224af2a33767649d9069a55`.
