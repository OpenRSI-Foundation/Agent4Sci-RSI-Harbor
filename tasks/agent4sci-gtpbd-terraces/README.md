# GTPBD: terraced-parcel segmentation

Harbor task: `agent4sci-gtpbd-terraces` · Domain: Geography · Track: suite.

| Field | Value |
|---|---|
| Upstream project/subtask | `GTPBD/semantic_segmentation` |
| Primary scientific metric | `miou` (percent, maximize) |
| Upstream paper baseline | 57.16 |
| Upstream reproduction baseline | 69.87 (not remeasured here) |
| Required components | single_run |
| Aggregation | mean |
| Work budget | 12 hours, 8 H200 GPUs |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

Binary terrace/background segmentation, 512x512 patches, geographic-region 60/20/20 split. mIoU is the mean of BOTH class IoUs; not just foreground IoU.

From the collection root, preview the launch command (no GPU job is started):

```bash
python3 tools/collection.py run agent4sci-gtpbd-terraces --gpus 0,1,2,3,4,5,6,7
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
Image: `ghcr.io/maszhongming/agent4sci-gtpbd@sha256:5cef891acbc51a00db027a5879d6308cda9af9c89c870d9f8faad0a194c5ef53`.
Dataset: `MingZhong/agent4sci@96befc0fb951a312b224af2a33767649d9069a55`.
