# PFDelta: IEEE-118 power flow

Harbor task: `agent4sci-pfdelta-ieee118` · Domain: Physics · Track: suite.

| Field | Value |
|---|---|
| Upstream project/subtask | `PFDelta/task_1_3` |
| Primary scientific metric | `average_pbl` (native, minimize) |
| Upstream paper baseline | 0.4 |
| Upstream reproduction baseline | 0.39 (not remeasured here) |
| Required components | seed_11, seed_22, seed_33 |
| Aggregation | mean |
| Work budget | 12 hours, 8 H200 GPUs |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

IEEE-118 full-topology training. Three seeds 11,22,33; within each seed equally average N, N-1, N-2 and close-to-infeasible conditions. ML-only inference; no Newton-Raphson or other iterative solvers.

From the collection root, preview the launch command (no GPU job is started):

```bash
python3 tools/collection.py run agent4sci-pfdelta-ieee118 --gpus 0,1,2,3,4,5,6,7
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
Image: `ghcr.io/maszhongming/agent4sci-pfdelta@sha256:9b36ce7715703470cd235d1c1b852dfa4c8ecb837a0ce01aadf15e077b1552a4`.
Dataset: `MingZhong/agent4sci@96befc0fb951a312b224af2a33767649d9069a55`.
