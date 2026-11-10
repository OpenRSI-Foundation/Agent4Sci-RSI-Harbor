# ProteinGym: DMS substitution fitness

Harbor task: `agent4sci-proteingym-fitness` · Domain: Bioengineering · Track: suite.

| Field | Value |
|---|---|
| Upstream project/subtask | `ProteinGym/kermut_dms_sub` |
| Primary scientific metric | `spearman` (correlation, maximize) |
| Upstream paper baseline | 0.657 |
| Upstream reproduction baseline | 0.6561 (not remeasured here) |
| Required components | random, modulo, contiguous |
| Aggregation | mean |
| Work budget | 12 hours, 8 H200 GPUs |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

Kermut supervised DMS substitutions. Three CV schemes (random,modulo,contiguous), five folds each, For each assay and CV scheme, concatenate predictions from all five folds BEFORE computing Spearman; average assays within each scheme, then average the three schemes. Do not average per-fold correlations. All assays/folds must be covered; seed 2024.

See [instruction.md](instruction.md) for the full research/submission contract,
[tests/spec.json](tests/spec.json) for pinned inputs and checksums, and the
[collection README](../../README.md) for execution and trust boundaries.
No validated oracle solution is claimed. The image contains upstream reproduction
code and instructions for independently establishing the baseline.

Source: [Agent4Sci at 74b0e8c4dc55](https://github.com/maszhongming/agent4sci/tree/74b0e8c4dc55610072bed4326b6bfac24dc77377).
Image: `ghcr.io/maszhongming/agent4sci-proteingym@sha256:e26305539be83948826900982227170e75c8cd21385d7242d13dd7d0cac918a6`.
Dataset: `MingZhong/agent4sci@96befc0fb951a312b224af2a33767649d9069a55`.
