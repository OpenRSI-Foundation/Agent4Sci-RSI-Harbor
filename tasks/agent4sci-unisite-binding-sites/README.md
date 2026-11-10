# UniSite: ligand binding-site detection

RSI task: `rsi/agent4sci-unisite-binding-sites` · Domain: Bioengineering · Track: suite.

Format and runtime authority: [OpenRSI-Index](https://github.com/OpenRSI-Foundation/OpenRSI-Index),
Harbor schema 1.4 and RSI-Harness. The public Index path is `rsi-tasks/agent4sci-unisite-binding-sites/`.

| Field | Value |
|---|---|
| Upstream project/subtask | `UniSite/binding_site_detection` |
| Primary scientific metric | `ap_0_5` (fraction, maximize) |
| Upstream paper baseline | 0.3835 |
| Upstream reproduction baseline | 0.383 (not remeasured here) |
| Required components | single_run |
| Aggregation | mean |
| Work budget | 12 hours, 8 H200 GPUs |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

UniSite-DS full test set, original AP at IoU threshold 0.5; single run. Preserve original site matching and structure preprocessing.

From the collection root, preview the launch command (no GPU job is started):

```bash
python3 tools/collection.py run agent4sci-unisite-binding-sites --gpus 0,1,2,3,4,5,6,7
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
Image: `ghcr.io/maszhongming/agent4sci-unisite@sha256:737aa1c09bcc41f8772e0cafb367ea6c011ac6ede094364ca5d5c88b96dd8c5c`.
Dataset: `MingZhong/agent4sci@96befc0fb951a312b224af2a33767649d9069a55`.
