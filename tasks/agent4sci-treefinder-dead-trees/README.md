# TreeFinder: dead-tree segmentation

Harbor task: `agent4sci-treefinder-dead-trees` · Domain: Ecology · Track: suite.

| Field | Value |
|---|---|
| Upstream project/subtask | `TreeFinder/dead_tree_seg` |
| Primary scientific metric | `dead_tree_f1` (percent, maximize) |
| Upstream paper baseline | 51.9 |
| Upstream reproduction baseline | 52.6 (not remeasured here) |
| Required components | fold_0, fold_1, fold_2 |
| Aggregation | mean |
| Work budget | 12 hours, 8 H200 GPUs |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

Three fixed folds: fold_0 seed2025, fold_1 seed2024, fold_2 seed2023. Original random 80/10/10 splits. Dead-tree-class F1 in percent; not macro F1.

See [instruction.md](instruction.md) for the full research/submission contract,
[tests/spec.json](tests/spec.json) for pinned inputs and checksums, and the
[collection README](../../README.md) for execution and trust boundaries.
No validated oracle solution is claimed. The image contains upstream reproduction
code and instructions for independently establishing the baseline.

Source: [Agent4Sci at 74b0e8c4dc55](https://github.com/maszhongming/agent4sci/tree/74b0e8c4dc55610072bed4326b6bfac24dc77377).
Image: `ghcr.io/maszhongming/agent4sci-treefinder@sha256:fe6cef0ef92df70ff9ac75338f7161b3f596c0639fe05dfc57fe0cc475567d30`.
Dataset: `MingZhong/agent4sci@96befc0fb951a312b224af2a33767649d9069a55`.
