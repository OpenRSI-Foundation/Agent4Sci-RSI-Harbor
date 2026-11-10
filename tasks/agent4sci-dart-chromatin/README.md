# DART-Eval: GM12878 chromatin activity

RSI task: `rsi/agent4sci-dart-chromatin` · Domain: Genomics · Track: suite.

Format and runtime authority: [OpenRSI-Index](https://github.com/OpenRSI-Foundation/OpenRSI-Index),
Harbor schema 1.4 and RSI-Harness. The public Index path is `rsi-tasks/agent4sci-dart-chromatin/`.

| Field | Value |
|---|---|
| Upstream project/subtask | `DART-Eval/t4_gm12878` |
| Primary scientific metric | `test_spearman_pos` (correlation, maximize) |
| Upstream paper baseline | 0.515 |
| Upstream reproduction baseline | 0.544 (not remeasured here) |
| Required components | single_run |
| Aggregation | mean |
| Work budget | 12 hours, 8 H200 GPUs |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

Task 4 GM12878. Spearman on positive test peaks. Upstream reproduction uses full fine-tuning of NT-v2-500m rather than paper LoRA; preserve split and metric.

From the collection root, preview the launch command (no GPU job is started):

```bash
python3 tools/collection.py run agent4sci-dart-chromatin --gpus 0,1,2,3,4,5,6,7
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
Image: `ghcr.io/maszhongming/agent4sci-dart-eval@sha256:747c723fb7468fbaab1f1b1fc4bdd3f92b30792c22320eac2e987ef377902439`.
Dataset: `MingZhong/agent4sci@96befc0fb951a312b224af2a33767649d9069a55`.
