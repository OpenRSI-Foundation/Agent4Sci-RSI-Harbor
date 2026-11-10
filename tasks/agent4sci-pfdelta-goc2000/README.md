# PFDelta-2000: latency-constrained power flow

Harbor task: `agent4sci-pfdelta-goc2000` · Domain: Physics · Track: case-study.

| Field | Value |
|---|---|
| Upstream project/subtask | `PFDelta_2000/task_1_3` |
| Primary scientific metric | `average_pbl` (native, minimize) |
| Upstream paper baseline | Not in original paper |
| Upstream reproduction baseline | 1.18 (not remeasured here) |
| Required components | seed_11, seed_22, seed_33 |
| Aggregation | mean |
| Work budget | 12 hours, 8 H200 GPUs |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

GOC-2000 case study (outside the 25-task suite). Three seeds 11,22,33; equal mean over N,N-1,N-2,C2I conditions. Verify GNN-comparable latency against co-measured baseline on the SAME hardware/batch protocol; upstream references ~10-55 ms unbatched or ~1-3 ms batched. Report both timing and PBL. The IEEE-118 ML-only rule does NOT apply to this case study.

From the collection root, preview the launch command (no GPU job is started):

```bash
python3 tools/collection.py run agent4sci-pfdelta-goc2000 --gpus 0,1,2,3,4,5,6,7
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
Image: `ghcr.io/maszhongming/agent4sci-pfdelta_2000@sha256:b4b4df1a8e03825d1cd9d1e1712d03bdebc75a8cb15f38a21d94ca07d13bd397`.
Dataset: `MingZhong/agent4sci@96befc0fb951a312b224af2a33767649d9069a55`.
