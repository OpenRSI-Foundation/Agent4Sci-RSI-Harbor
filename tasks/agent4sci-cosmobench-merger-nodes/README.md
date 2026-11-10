# CosmoBench: merger-node classification

RSI task: `rsi/agent4sci-cosmobench-merger-nodes` · Domain: Cosmology · Track: suite.

Format and runtime authority: [OpenRSI-Index](https://github.com/OpenRSI-Foundation/OpenRSI-Index),
Harbor schema 1.4 and RSI-Harness. The public Index path is `rsi-tasks/agent4sci-cosmobench-merger-nodes/`.

| Field | Value |
|---|---|
| Upstream project/subtask | `CosmoBench/tree_infilling` |
| Primary scientific metric | `accuracy` (fraction, maximize) |
| Upstream paper baseline | 0.72 |
| Upstream reproduction baseline | 0.717 (not remeasured here) |
| Required components | single_run |
| Aggregation | mean |
| Work budget | 12 hours, 8 H200 GPUs |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

CS-Trees-200; classify virtual merger nodes; fixed 120/40/40 trees. k-NN is an allowed baseline. Paper uncertainty is bootstrap.

From the collection root, preview the launch command (no GPU job is started):

```bash
python3 tools/collection.py run agent4sci-cosmobench-merger-nodes --gpus 0,1,2,3,4,5,6,7
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
Image: `ghcr.io/maszhongming/agent4sci-cosmobench@sha256:000018bd03db0919ee3e95ff98d6d3e112cdc092d13fc253a7ec1e34ff4a058d`.
Dataset: `MingZhong/agent4sci@96befc0fb951a312b224af2a33767649d9069a55`.
