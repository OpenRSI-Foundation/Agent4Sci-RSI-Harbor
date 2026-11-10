# ATAT: transient classification

Harbor task: `agent4sci-atat-transient` · Domain: Astronomy · Track: suite.

| Field | Value |
|---|---|
| Upstream project/subtask | `ATAT/atat_transient` |
| Primary scientific metric | `macro_f1` (percent, maximize) |
| Upstream paper baseline | 83.5 |
| Upstream reproduction baseline | 82.79 (not remeasured here) |
| Required components | fold_0, fold_1, fold_2, fold_3, fold_4 |
| Aggregation | mean |
| Work budget | 12 hours, 8 H200 GPUs |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

Five ELAsTiCC folds; LC + metadata + features; macro F1 at 2048 days. Report per-fold and mean scores.

See [instruction.md](instruction.md) for the full research/submission contract,
[tests/spec.json](tests/spec.json) for pinned inputs and checksums, and the
[collection README](../../README.md) for execution and trust boundaries.
No validated oracle solution is claimed. The image contains upstream reproduction
code and instructions for independently establishing the baseline.

Source: [Agent4Sci at 74b0e8c4dc55](https://github.com/maszhongming/agent4sci/tree/74b0e8c4dc55610072bed4326b6bfac24dc77377).
Image: `ghcr.io/maszhongming/agent4sci-atat@sha256:691be4ed70b5735cc6c62f15c3124d87333ae97bb4a189a0698a02567e40cfe2`.
Dataset: `MingZhong/agent4sci@96befc0fb951a312b224af2a33767649d9069a55`.
