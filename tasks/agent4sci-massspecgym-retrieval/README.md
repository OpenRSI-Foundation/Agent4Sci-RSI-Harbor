# MassSpecGym: molecule retrieval

Harbor task: `agent4sci-massspecgym-retrieval` · Domain: Chemistry · Track: suite.

| Field | Value |
|---|---|
| Upstream project/subtask | `MassSpecGym/molecule_retrieval` |
| Primary scientific metric | `hit_rate_at_1` (percent, maximize) |
| Upstream paper baseline | 14.64 |
| Upstream reproduction baseline | 16.14 (not remeasured here) |
| Required components | single_run |
| Aggregation | mean |
| Work budget | 12 hours, 8 H200 GPUs |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

Mass-based candidates, up to 256 candidates per spectrum; single fixed-seed run. Hit Rate@1 in percent; bootstrap confidence interval uses 20000 resamples, not training runs.

See [instruction.md](instruction.md) for the full research/submission contract,
[tests/spec.json](tests/spec.json) for pinned inputs and checksums, and the
[collection README](../../README.md) for execution and trust boundaries.
No validated oracle solution is claimed. The image contains upstream reproduction
code and instructions for independently establishing the baseline.

Source: [Agent4Sci at 74b0e8c4dc55](https://github.com/maszhongming/agent4sci/tree/74b0e8c4dc55610072bed4326b6bfac24dc77377).
Image: `ghcr.io/maszhongming/agent4sci-massspecgym@sha256:afa24e47f5e92c8b1da42a4ce09ceaec5f4d5f00164f33ab56812f47a243a099`.
Dataset: `MingZhong/agent4sci@96befc0fb951a312b224af2a33767649d9069a55`.
