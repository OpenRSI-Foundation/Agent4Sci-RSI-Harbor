# Validation record

Initial port prepared on 2026-11-10. Upstream Git:
`74b0e8c4dc55610072bed4326b6bfac24dc77377`.

| Check | Result |
|---|---|
| Every upstream registry project covered | 21/21 |
| Every pinned dataset project/subtask pair covered | 26/26 |
| Published-suite tasks / extra case-study tasks | 25 / 1 |
| GHCR linux/amd64 manifests and selected source layers | Retrieved and SHA-256 checked for all 21 images |
| Harbor 1.4 + RSI-Harness compilation | 26/26 passed with Harbor 0.21.0 |
| Work/Judge identity and verifier-only auth templates | 26/26 checked by the actual compiler |
| Generated file consistency, Python AST and bash syntax | Passed |
| CPU adapter regression suite | 16 tests passed, including parameterized coverage of all 26 tasks |
| Full Docker image builds / runtime bootstrap | Not run |
| GPU baseline reproductions | Not run |
| Real evaluation and audit model calls | Not run |
| Live RSI Work/snapshot/Judge/feedback integration | Not run |
| Native Harbor live execution | Not run |
| Oracle solutions | Not supplied or claimed |

The initial local compiler check used OpenRSI-Index
`d98049f0a968e4e7258293b6e55cd0aaa93eb0c4`. CI independently installs the public
revision `8d170deed4591fc7e4306f2d86ff4d9bcffd1288` and Harbor 0.21.0.
See the repository's **Validate Harbor collection** workflow for its current
commit-specific result. The local scientific Docker runtime was unavailable;
VISION was in scheduled maintenance. No GPU resources or scientific jobs were
started. These limitations are not substitutes for the pending runtime checks.

Before certifying a task for scientific use, build its image, verify data and
credential boundaries under the selected runtime, reproduce its complete
seed/fold baseline, exercise a valid candidate and failure cases through a real
Judge, and compare the auditor's transcript with host-side research logs. Record
hardware, image/data/source revisions, evaluator model/CLI and raw metrics.
