# NeuroGraph: fluid-intelligence regression

Harbor task: `agent4sci-neurograph-intelligence` · Domain: Neuroscience · Track: suite.

| Field | Value |
|---|---|
| Upstream project/subtask | `NeuroGraph/hcp_fi_gnn` |
| Primary scientific metric | `mae` (native, minimize) |
| Upstream paper baseline | 0.264 |
| Upstream reproduction baseline | 0.272 (not remeasured here) |
| Required components | seed_123, seed_124 |
| Aggregation | mean |
| Work budget | 12 hours, 8 H200 GPUs |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

HCP fluid intelligence, GNN-based architecture REQUIRED. Two seeds 123,124. Use the upstream variant of MAE exactly, not a standard replacement formula.

See [instruction.md](instruction.md) for the full research/submission contract,
[tests/spec.json](tests/spec.json) for pinned inputs and checksums, and the
[collection README](../../README.md) for execution and trust boundaries.
No validated oracle solution is claimed. The image contains upstream reproduction
code and instructions for independently establishing the baseline.

Source: [Agent4Sci at 74b0e8c4dc55](https://github.com/maszhongming/agent4sci/tree/74b0e8c4dc55610072bed4326b6bfac24dc77377).
Image: `ghcr.io/maszhongming/agent4sci-neurograph@sha256:64d547eabfe9b454b53f1709ea06fc4d2f2d2ec39be002a78911631ed92f271c`.
Dataset: `MingZhong/agent4sci@96befc0fb951a312b224af2a33767649d9069a55`.
