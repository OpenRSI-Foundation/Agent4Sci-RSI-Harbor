# Agent4Sci — RSI Harbor Task Collection

**Canonical RSI task entry point:** [Agent4Sci in OpenRSI-Index](https://github.com/OpenRSI-Foundation/OpenRSI-Index/blob/main/rsi-tasks/AGENT4SCI.md).
The Index contains complete packages at `rsi-tasks/agent4sci-*/`, with source
commits and per-file publication hashes. This repository maintains the upstream
imports, task generator and adapter regression tests. OpenRSI-Index's task
format, publication checks and RSI-Harness define the integration contract.

将 [Agent4Sci](https://github.com/maszhongming/agent4sci) 全集转换为可由
RSI-Harness 加载的 Harbor 1.4 task：**25 个正式任务 + PFDelta-2000 案例，共 26 个**。
每个任务都有独立且可读的名称、研究说明、固定环境、评分入口和来源记录。

This repository packages every Agent4Sci scientific task for
[RSI-Harness](https://github.com/OpenRSI-Foundation/OpenRSI-Index/tree/main/RSI-Harness)
and Harbor. It covers all **21 registered project images**, including the case
study, across **11 scientific domains**. CheMixHub (3), CosmoBench (3), and
Mars-Bench (2) are split into individual tasks.

**Release status: task packaging and CPU validation.** All 26 tasks compile with
the actual Harbor/RSI-Harness models and pass adapter tests. Full image builds,
GPU baseline reproduction, real evaluation/audit agent calls, and the complete
Work → snapshot → Judge runtime have **not yet been validated**. The baseline
numbers are attributed upstream results, not measurements made in this port.
There is no claimed validated oracle solution. CI tests use synthetic fixtures;
their reward values are not benchmark results.

## Tasks and names

See **[TASKS.md](TASKS.md)** for all 26 names, upstream mappings, metrics, units,
directions and baselines. Each row links to a task README and its full contract.
[catalog.json](catalog.json) is the machine-readable source of truth.

任务按 **11 个领域**整理；[正式套件](collections/suite.txt)含 25 个任务，
[案例研究](collections/case-study.txt)单列 PFDelta-2000，
[完整合集](collections/all.txt)含全部 26 个。每个清单一行一个仓库相对路径。
所有索引由同一份 catalog 自动生成，避免漏项或名称不一致。

```bash
python3 tools/collection.py list
python3 tools/collection.py list --track suite --domain Chemistry
python3 tools/collection.py list --project CosmoBench --format json
python3 tools/collection.py list --track case-study --format paths
python3 tools/collection.py show pfdelta-ieee118
```

The [collection manifests](collections/) and task table are generated together
with the standalone packages. `list` supports domain, upstream project and track
filters; `show` prints the full pinned task contract. These commands need only
Python 3.10+ and do not download data or allocate GPUs.

Each directory is standalone (no symlink or import to a neighboring task):

```text
tasks/agent4sci-pfdelta-ieee118/
├── README.md
├── instruction.md
├── task.toml                  # Harbor schema 1.4
├── environment/
│   ├── Dockerfile             # immutable upstream image digest
│   ├── bootstrap.py           # stage reference + train/val during build
│   ├── data.py
│   ├── candidate_exec.py
│   ├── instruction.md
│   └── spec.json
└── tests/
    ├── test.sh                # Harbor/RSI verifier entry point
    ├── verifier.py            # independent evaluation, then audit
    ├── scoring.py
    ├── trajectory.py         # checks the frozen host trajectory when supplied
    ├── data.py
    ├── evaluation.md
    └── spec.json
```

## Evaluation and conversion decisions

Agent4Sci uses a research agent, a separate evaluation agent, and a separate
academic-integrity auditor. Its published images do **not** expose one uniform,
deterministic verifier API for arbitrary new scientific models. This port retains
that agent-based evaluation protocol: the evaluator runs the pinned reference
metric code against submitted models; a fresh auditor checks the trajectory,
coverage and evidence. Python validates the structured results and computes the
reward only after both stages pass. Candidate-authored scores are never read as
the reward. Missing components, nonfinite metrics, incorrect units/ranges,
incomplete trajectories, evaluation errors or a non-CLEAN audit produce a failed
verification with **no valid reward**, rather than a synthetic zero score.

The required seeds/folds, task-specific constraints and original metric formulas
are recorded per task. For example, ProteinGym concatenates five folds within
each assay before computing Spearman and averaging assays/schemes; Mars-Bench
uses the upstream 25%-trimmed IQM over seven seeds. These cannot be replaced with
the best seed or an arbitrary average. PFDelta-118 forbids iterative solvers at
inference; PFDelta-2000 instead imposes GNN-comparable latency, measured alongside
the baseline on the same hardware. TIDMAD has no validation partition: its files
named `abra_validation_*` in `test/` remain held out.

The adapter adds a monotonic, continuous RSI reward. With raw metric `m`, upstream
reproduction baseline `b`, and `d=+1` for maximize or `-1` for minimize:

```text
relative_improvement = d * (m - b) / abs(b)
reward = 0.5 + atan(relative_improvement) / pi
```

Use **`reward` / `maximize`** for every task. Baseline maps to 0.5; improvement is
above 0.5. Raw metric and relative improvement are also retained in
`/logs/verifier/reward.json`. This reward is an adapter convention, not an
upstream Agent4Sci leaderboard score; it is not evidence of cross-task scientific
comparability.

The agent iterates using train/val during its research budget and makes **one
final held-out submission**. Set `--max-submissions 1`. Repeated hidden-test
submissions are a different, test-adaptive protocol and must not be reported as
upstream-comparable results. The task metadata documents the cap; the launcher
flag enforces it. This port does not silently substitute validation metrics for
the original test metric.

The source images specify **8 H200 GPUs and 12 hours per project run**. These are
the default Work resources for each independent task here. Splitting CheMixHub,
CosmoBench and Mars-Bench gives each subtask its own budget; running them all is
not the same total compute as one upstream shared-project run. CPU (32), RAM
(512 GiB), disk (1 TiB), build/download and Judge timeouts are conservative
packaging defaults, not measured minimum requirements. Each Judge agent is
capped at six hours; the 24-hour verifier cap also includes test-data staging.
Research skills bundled upstream are optional and are not installed by this port.

## Running one task

Use an **approved Linux x86-64 Docker host** with NVIDIA Container Toolkit,
8 H200 GPUs and enough local storage. The pinned upstream images contain the
scientific runtimes. Image construction downloads only the selected task's
train/val files from the pinned public Hub revision; test files are downloaded
only inside the fresh Judge. Large datasets can make the first build expensive.
Models additionally required by a training recipe may need downloads during Work.

Install the validated RSI-Harness revision from OpenRSI-Index, then clone this
collection (Python 3.12 for installation/validation):

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install 'git+https://github.com/OpenRSI-Foundation/OpenRSI-Index.git@8d170deed4591fc7e4306f2d86ff4d9bcffd1288#subdirectory=RSI-Harness'
```

Supply research
agent authentication through the harness's documented auth mechanism. Separately,
provide `ANTHROPIC_API_KEY` and `AGENT4SCI_JUDGE_MODEL` in the operator's environment;
they are templated into **verifier.env only**, never written into task files.
Choose an accessible Claude model explicitly; upstream's default preset at the
source commit is `claude-opus-4-8[1m]`. The evaluator CLI is pinned to **2.1.322**.
Evaluation and audit incur additional model API usage outside the research budget.

```bash
git clone https://github.com/OpenRSI-Foundation/Agent4Sci-RSI-Harbor.git
cd Agent4Sci-RSI-Harbor

# Set ANTHROPIC_API_KEY privately; do not commit credentials.
export AGENT4SCI_JUDGE_MODEL='claude-opus-4-8[1m]'

# Print the exact command first; this does not launch a job.
python3 tools/collection.py run pfdelta-ieee118 --gpus 0,1,2,3,4,5,6,7

# Execute one task on the prepared host.
python3 tools/collection.py run pfdelta-ieee118 \
  --gpus 0,1,2,3,4,5,6,7 --agent codex --execute
```

The launcher fixes `--primary-reward reward --score-direction maximize
--max-submissions 1`, validates the GPU pool, and checks verifier credentials
before execution. It supports `--model`, `--logs-root` and `--data-root`; credentials
are inherited privately and never inserted into the printed command. It launches
only the selected task. Manifests do not automatically schedule the whole suite.

In the Judge, `/workspace` is a **read-only snapshot**. Held-out data is staged
in a separate temporary data tree, with links to the snapshot's train/val splits.
The evaluator receives explicit data paths and writes retained inference evidence
to `/logs/verifier/candidate_outputs/`. Loading adapters must support these path
arguments instead of hardcoding `/workspace/data/<task>/test` or writing into
`/workspace/runs`. Any added Python environment must be under `/workspace/runs/`
to survive a clean Judge; packages installed only into the Work home do not.

This command is for the harness's Docker backend. On a managed cluster, use only
a site backend that has validated snapshotting, Judge isolation, networking and
recovery. In particular, Docker instructions are **not** a VISION/Pyxis launcher.
Changing hardware or budgets creates a distinct experimental setting and must be
reported. No scientific runs or GPU allocations were launched for this release.

These are **RSI tasks using Harbor 1.4 syntax**. Run them with OpenRSI-Index's
`rsi-harness`, following its [Quick Start](https://github.com/OpenRSI-Foundation/OpenRSI-Index/blob/main/assets/docs/quick-start.md).
Plain `harbor run` is not the supported entry point for this collection.

## Data and trust boundaries

- The source Git revision, all image digests and the dataset revision are fixed.
  [upstream/images.lock.json](upstream/images.lock.json) and
  [upstream/dataset-files.json](upstream/dataset-files.json) record the inventory.
  No benchmark data, model weights, API keys or experiment results are committed.
- Work contains reference code/papers and train/val. The build clears the upstream
  startup script and stages at **build time**, because RSI-Harness overrides image
  entrypoints. Each task fetches its own subtask, rather than all project subtasks.
- The original public-network research capability is retained. Since the source
  test dataset is public, filesystem separation is **not a network access control**;
  prohibited test downloads remain an audit rule, as in the upstream protocol.
- Reference assets are built without write permission and checked against pinned
  hashes. RSI-Harness currently runs Work with root authority even when `agent.user`
  names a non-root user, so these permissions are not an access-control boundary.
  The upstream passwordless-sudo grant is removed. Evaluators start with separate fresh homes and bare CLI mode, away
  from candidate hooks/configuration. A credential-scrubbing helper executes
  candidate inference as the unprivileged research user.
- This is a scientific-integrity workflow, **not a hardened adversarial-code
  sandbox**. Evaluator and auditor judgments remain model-dependent; a CLEAN audit
  is not proof. The evaluator must use the provided helper when executing candidate
  code. Its compliance is a trust assumption, not a kernel-enforced tool policy.
  RSI's frozen `/logs/agent` trajectory is the primary audit evidence: the verifier
  checks its manifest, file sizes and SHA-256 digests and refuses truncated or
  incomplete captures. Candidate logs cannot override this record. Native Harbor
  falls back to the upstream candidate-provided transcript, marked explicitly in
  provenance; it is not host-authenticated evidence.
- Preserve the entire private `/logs/verifier/` directory: evaluation/audit streams,
  structured reports, prompts, errors and provenance are the assessment evidence.
  Review them before making scientific claims. Do not feed held-out evidence back
  into continued optimization of the same evaluation run.

## Validation and maintenance

Python 3.12 is needed for the host-side TOML checks. The runtime adapter uses the
Python supplied by each source image.

```bash
python3 tools/generate.py --check
python3 tools/check_collection.py --require-harness
python3 -m unittest discover -s checks -v
```

CI installs RSI-Harness from a fixed OpenRSI-Index commit, compiles every task and
runs CPU regression tests. A second CI job mounts a synthetic workspace and host
trajectory read-only in Linux Docker and exercises all 26 contracts through real
evaluator subprocesses and the real candidate UID/credential-scrubbing helper.
Its Hub and model CLI are fixtures; networking is disabled. Evidence is uploaded
as `synthetic-runtime-evidence`. This checks filesystem and process contracts,
not scientific correctness or a live RSI snapshot lifecycle.
Tests cover every task's metric direction, exact
components, nonfinite/bad scores, failed audits, stale rewards, split scoping and
mocked evaluator orchestration. They make no GPU, dataset or model-API calls.
See [VALIDATION.md](VALIDATION.md) for the release evidence and remaining checks.

Edit canonical code in `adapter/`, reviewed task contracts in `catalog.json`,
then run `python3 tools/generate.py` and all checks. Generated copies intentionally
make each task portable. To re-import a newer upstream revision, inspect the
images on a suitable preparation host with `tools/inspect_images.py`, obtain the
Hub metadata with `hf datasets info MingZhong/agent4sci --format json`, and use
`tools/import_catalog.py`; review all changed protocols/baselines before regenerating.

To refresh the complete public packages in an OpenRSI-Index checkout from an
immutable committed collection revision:

```bash
python3 tools/publish_index.py --index /path/to/OpenRSI-Index --revision COMMIT_SHA
python3 tools/publish_index.py --index /path/to/OpenRSI-Index --revision COMMIT_SHA --check
```

This exports all 26 packages, their licenses, `publication.json` receipts and
the grouped `rsi-tasks/AGENT4SCI.md` index. It does not execute task code, touch
the Index Harness or alter its publication policy. Commit the resulting Index
files and run its own `checks/check_publication.py --compile` before publication.

## Attribution

Upstream: [maszhongming/agent4sci](https://github.com/maszhongming/agent4sci), commit
`74b0e8c4dc55610072bed4326b6bfac24dc77377`.
Data: [MingZhong/agent4sci](https://huggingface.co/datasets/MingZhong/agent4sci), revision
`96befc0fb951a312b224af2a33767649d9069a55`.

Ming Zhong, Stacy Li, Nicholas Carlini and Matthew Jagielski, *Automating ML for
Science: Can Frontier Agents Climb Scientific Hills in the Wild?* (2026),
[arXiv:2610.28763](https://arxiv.org/abs/2610.28763).

The adapter is Apache-2.0; see [LICENSE](LICENSE) and [NOTICE](NOTICE). Benchmark
code, datasets, papers and pretrained weights retain their original terms. This
is an OpenRSI adaptation, not a claim of endorsement by the upstream authors.
