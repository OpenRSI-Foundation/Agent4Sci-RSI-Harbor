# ESCAPE: antimicrobial-peptide classification

RSI task: `rsi/agent4sci-escape-amp` · Domain: Bioengineering · Track: suite.

Format and runtime authority: [OpenRSI-Index](https://github.com/OpenRSI-Foundation/OpenRSI-Index),
Harbor schema 1.4 and RSI-Harness. The public Index path is `rsi-tasks/agent4sci-escape-amp/`.

| Field | Value |
|---|---|
| Upstream project/subtask | `ESCAPE/amp_classification` |
| Primary scientific metric | `overall_map` (percent, maximize) |
| Upstream paper baseline | 72.1 |
| Upstream reproduction baseline | 71.8 (not remeasured here) |
| Required components | seed_42, seed_1665, seed_8914 |
| Aggregation | mean |
| Work budget | 12 hours, 8 H200 GPUs |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

Three seeds 42,1665,8914; two-fold ensemble per seed (six training runs total). Overall mAP across the five labels in percent.

From the collection root, preview the launch command (no GPU job is started):

```bash
python3 tools/collection.py run agent4sci-escape-amp --gpus 0,1,2,3,4,5,6,7
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
Image: `ghcr.io/maszhongming/agent4sci-escape@sha256:dc9569a103e5793735335138f99d17a1f994cec78549f9768acd71bcc9773979`.
Dataset: `MingZhong/agent4sci@96befc0fb951a312b224af2a33767649d9069a55`.
