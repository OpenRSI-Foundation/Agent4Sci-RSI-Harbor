# GEO-Bench-2: crop-type segmentation

Harbor task: `agent4sci-geobench-pastis` · Domain: Geography · Track: suite.

| Field | Value |
|---|---|
| Upstream project/subtask | `GEO-Bench-2/pastis` |
| Primary scientific metric | `miou` (percent, maximize) |
| Upstream paper baseline | 43.1 |
| Upstream reproduction baseline | 45.9 (not remeasured here) |
| Required components | seed_0, seed_1, seed_2, seed_3, seed_4 |
| Aggregation | mean |
| Work budget | 12 hours, 8 H200 GPUs |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

PASTIS, five seeds 0..4. Macro MulticlassJaccardIndex, ignore void class 19. Fixed split-specific tortilla files; final mIoU in percent.

See [instruction.md](instruction.md) for the full research/submission contract,
[tests/spec.json](tests/spec.json) for pinned inputs and checksums, and the
[collection README](../../README.md) for execution and trust boundaries.
No validated oracle solution is claimed. The image contains upstream reproduction
code and instructions for independently establishing the baseline.

Source: [Agent4Sci at 74b0e8c4dc55](https://github.com/maszhongming/agent4sci/tree/74b0e8c4dc55610072bed4326b6bfac24dc77377).
Image: `ghcr.io/maszhongming/agent4sci-geo-bench-2@sha256:f97191e767499b9ac6e4846d6a6ebcb5baf9526ed0329d40bd8fe9ce5866d5d5`.
Dataset: `MingZhong/agent4sci@96befc0fb951a312b224af2a33767649d9069a55`.
