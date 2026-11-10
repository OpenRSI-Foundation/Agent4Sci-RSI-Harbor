# LITHOS: mineral classification

RSI task: `rsi/agent4sci-lithos-minerals` · Domain: Geology · Track: suite.

Format and runtime authority: [OpenRSI-Index](https://github.com/OpenRSI-Foundation/OpenRSI-Index),
Harbor schema 1.4 and RSI-Harness. The public Index path is `rsi-tasks/agent4sci-lithos-minerals/`.

| Field | Value |
|---|---|
| Upstream project/subtask | `LITHOS/mineral_classification` |
| Primary scientific metric | `macro_f1` (fraction, maximize) |
| Upstream paper baseline | 0.432 |
| Upstream reproduction baseline | 0.422 (not remeasured here) |
| Required components | seed_0, seed_42, seed_123 |
| Aggregation | mean |
| Work budget | 12 hours, 8 H200 GPUs |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

25 classes, PPL+XPL inputs. Use only the upstream single fixed fold; opposite CV fold would leak test data. Three seeds 0,42,123; mean macro F1.

From the collection root, preview the launch command (no GPU job is started):

```bash
python3 tools/collection.py run agent4sci-lithos-minerals --gpus 0,1,2,3,4,5,6,7
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
Image: `ghcr.io/maszhongming/agent4sci-lithos@sha256:3710a8a165956feb1a9ab3202e4406d0f4490553171bff0842138c91fb2dc07b`.
Dataset: `MingZhong/agent4sci@96befc0fb951a312b224af2a33767649d9069a55`.
