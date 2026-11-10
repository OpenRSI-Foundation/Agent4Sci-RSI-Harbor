"""Generate standalone Harbor 1.4 tasks; --check detects stale generated files."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def files(spec):
    slug = spec['id']
    project = ROOT / 'upstream/projects' / spec['project']
    metric = spec['metric']
    instruction = f'''# {spec['title']}

Improve **{metric['name']}** ({metric['unit']}; **{metric['direction']}**) for
**{spec['project']}/{spec['data_task']}**. Only this subtask is scored.

## Resources and research surface

The upstream reference allocation is **8 H200 GPUs, 12 hours**. Work under
`/workspace/runs/`: develop model architectures, training methods, features,
preprocessing and inference improvements consistent with the scientific task.
Read `/workspace/task.md`, `/workspace/paper/`, `/workspace/repo/` and
`/workspace/reproduction/` first. Copy code into `runs/` to edit it; keep the
reference code, paper and data unchanged. Install extra packages in a venv under
`/workspace/runs/` (for example `runs/.venv`); home/system changes do not reach
the clean Judge. Loading code must accept explicit data and output paths: the
Judge reads `/workspace` as a read-only snapshot, stages test data separately,
and supplies a writable output directory. Do not hardcode test or output paths.
The allocation is per task here: splitting a multi-task project changes its
budget accounting relative to upstream's shared project run. Report that fact.

## Fixed evaluation protocol

{spec['protocol']}

Required measurement components: `{', '.join(spec['components'])}`.
The reproduction baseline is **{spec['baseline']['reproduction']}** in the metric
units above. This is an upstream reported value, not a new OpenRSI measurement.

Use training and validation only for iterative development. If no validation
partition exists, define a holdout from training without changing final test
membership. Do not download or inspect test data, including the public upstream
Hub test files. Do not tamper with evaluators or hardcode outputs. The auditor
reviews attempted and reverted violations as well as the final code.

## Final submission

At the end of the budget, stop training, consolidate selected models for ALL
required seeds/folds into `/workspace/runs/best_checkpoints/`, and retain the
loading/inference code in `runs/`. Keep only the selected checkpoints.
Create nonempty `runs/SUMMARY.md` (exact loading commands, checkpoint-to-component
mapping and validation selection), `runs/METHODOLOGY.md` (scientific reasoning,
changes and evidence), and `runs/hillclimb_logs.jsonl` (the COMPLETE agent session
transcript, including failed/reverted attempts). Do not summarize the transcript.
RSI-Harness also supplies its frozen host trajectory at `/logs/agent` to the
Judge; that is the primary audit record and may substitute for the copied log.
Native Harbor requires the complete copied `hillclimb_logs.jsonl`.
Make artifacts readable by the independent evaluator. Use `rsi-submit` **once**
when final; in plain Harbor, finish your turn instead. Do not tune on final Judge
feedback. The operator must enforce `--max-submissions 1` for upstream-comparable
results. The evaluator and auditor run independently in the Judge and may reject
unsupported loading code, incomplete protocols or incomplete trajectories.

## Reward

The verifier recomputes the raw test metric and requires a CLEAN integrity audit.
Let `d=+1` for maximize and `d=-1` for minimize, `b` be the reproduction baseline,
and `m` the measured metric. `improvement=d*(m-b)/abs(b)` and
`reward=0.5+atan(improvement)/pi`. Higher reward is always better; baseline=0.5.
Missing/failed evaluations produce no valid reward, never a fabricated score.

## Original project context (other subtask rows are context only)

{(project / 'task.md').read_text().rstrip()}
'''
    config = f'''schema_version = "1.4"

[task]
name = "rsi/{slug}"
version = "1.0.1"
description = {json.dumps(spec['title'])}

[metadata]
author_name = "OpenRSI contributors; upstream Agent4Sci authors"
category = "ML"
subcategory = "Scientific discovery"
tags = ["autoresearch", "agent4sci", {json.dumps(spec['domain'].lower())}]
difficulty_explanation = "Long-horizon scientific model development with fixed data splits and seed/fold coverage."
verification_explanation = "Upstream independent evaluation agent plus separate integrity auditor, then strict continuous reward conversion."
expert_time_estimate_hours = 12

[metadata.agent4sci]
project = {json.dumps(spec['project'])}
subtask = {json.dumps(spec['data_task'])}
track = {json.dumps(spec['track'])}
upstream_revision = {json.dumps(spec['upstream_revision'])}
validation_status = "packaged; GPU baseline and real evaluator not yet run"
recommended_max_submissions = 1

[metadata.rsi_harness.verifier]
gpus = 8
visibility = "hidden"
clean_image = true

[environment]
os = "linux"
cpus = 32
memory_mb = 524288
storage_mb = 1048576
gpus = 8
gpu_types = ["H200"]
workdir = "/workspace"
build_timeout_sec = 86400
network_mode = "public"

[agent]
user = "agent"
timeout_sec = 43200
network_mode = "public"

[verifier]
user = "root"
timeout_sec = 86400
environment_mode = "shared"
network_mode = "public"

[verifier.env]
ANTHROPIC_API_KEY = "${{ANTHROPIC_API_KEY}}"
AGENT4SCI_JUDGE_MODEL = "${{AGENT4SCI_JUDGE_MODEL}}"
'''
    dockerfile = f'''FROM {spec['image']}
USER root
COPY spec.json instruction.md bootstrap.py data.py /opt/agent4sci/
COPY candidate_exec.py /usr/local/bin/agent4sci-candidate
RUN npm install --prefix /opt/agent4sci/judge-cli --no-audit --no-fund @anthropic-ai/claude-code@{spec['judge_cli_version']} \\
    && useradd --create-home --shell /bin/bash a4sci-judge \\
    && chmod 0755 /usr/local/bin/agent4sci-candidate \\
    && printf '%s\\n' 'a4sci-judge ALL=(root) NOPASSWD: /usr/local/bin/agent4sci-candidate *' > /etc/sudoers.d/agent4sci-judge \\
    && chmod 0440 /etc/sudoers.d/agent4sci-judge \\
    && /usr/bin/python3 -I /opt/agent4sci/bootstrap.py
ENV PYTHONDONTWRITEBYTECODE=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /workspace
USER agent
ENTRYPOINT []
CMD ["sleep", "infinity"]
'''
    readme = f'''# {spec['title']}

Harbor task: `{slug}` · Domain: {spec['domain']} · Track: {spec['track']}.

| Field | Value |
|---|---|
| Upstream project/subtask | `{spec['project']}/{spec['data_task']}` |
| Primary scientific metric | `{metric['name']}` ({metric['unit']}, {metric['direction']}) |
| Upstream paper baseline | {spec['baseline']['paper'] if spec['baseline']['paper'] is not None else 'Not in original paper'} |
| Upstream reproduction baseline | {spec['baseline']['reproduction']} (not remeasured here) |
| Required components | {', '.join(spec['components'])} |
| Aggregation | {spec['aggregation']} |
| Work budget | 12 hours, 8 H200 GPUs |
| RSI primary reward | `reward`, maximize |
| Final hidden-test submissions | 1 |
| Validation | Packaged; real image build, GPU baseline, evaluator and auditor not yet run |

{spec['protocol']}

From the collection root, preview the launch command (no GPU job is started):

```bash
python3 tools/collection.py run {slug} --gpus 0,1,2,3,4,5,6,7
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

Source: [Agent4Sci at {spec['upstream_revision'][:12]}](https://github.com/maszhongming/agent4sci/tree/{spec['upstream_revision']}).
Image: `{spec['image']}`.
Dataset: `MingZhong/agent4sci@{spec['dataset']['revision']}`.
'''
    payload = {'task.toml':config.encode(), 'instruction.md':(instruction.rstrip()+'\n').encode(),
               'README.md':readme.encode(), 'environment/Dockerfile':dockerfile.encode(),
               'environment/instruction.md':(instruction.rstrip()+'\n').encode(),
               'tests/test.sh':b'#!/bin/bash\nset -euo pipefail\ncd /workspace\nexec /usr/bin/python3 -I /tests/verifier.py\n',
               'tests/evaluation.md':(project / 'evaluation.md').read_bytes()}
    for role, names in {'environment':['bootstrap.py','data.py','candidate_exec.py'],
                        'tests':['verifier.py','data.py','scoring.py','trajectory.py']}.items():
        payload[f'{role}/spec.json'] = (json.dumps(spec,indent=2)+'\n').encode()
        for name in names:
            payload[f'{role}/{name}'] = (ROOT / 'adapter' / name).read_bytes()
    return payload


def collection_files(catalog):
    tasks = catalog['tasks']
    groups = {'all': tasks, 'suite': [t for t in tasks if t['track'] == 'suite'],
              'case-study': [t for t in tasks if t['track'] == 'case-study']}
    domains = sorted({t['domain'] for t in tasks})
    for domain in domains:
        groups[f'domains/{domain.lower()}'] = [t for t in tasks if t['domain'] == domain]
    payload = {f'collections/{key}.txt': ('\n'.join(f'tasks/{t["id"]}' for t in group) + '\n').encode()
               for key, group in groups.items()}
    rows = ['# Complete task catalog', '',
            '25 suite tasks plus the separately marked PFDelta-2000 case study. '
            'Baselines are upstream reports, not new measurements. Every task has '
            'an independent Harbor 1.4 package, a readable name and its own fixed protocol.', '',
            'Generated from [catalog.json](catalog.json). '
            'Use [collections/](collections/) for plain-text manifests or '
            '`python3 tools/collection.py list --domain Chemistry` to filter tasks.', '',
            '| Domain | Suite | Case study | Manifest |', '|---|---:|---:|---|']
    for domain in domains:
        group = groups[f'domains/{domain.lower()}']
        rows.append(f'| [{domain}](#{domain.lower()}) | '
                    f'{sum(t["track"] == "suite" for t in group)} | '
                    f'{sum(t["track"] == "case-study" for t in group)} | '
                    f'[paths](collections/domains/{domain.lower()}.txt) |')
    for domain in domains:
        rows.extend(['', f'## {domain}', '',
                     '| Task and directory | Upstream subtask | Metric / units | Direction | Paper | Reproduction |',
                     '|---|---|---|---|---|---|'])
        for t in groups[f'domains/{domain.lower()}']:
            metric = t['metric']
            case = ' **[case study]**' if t['track'] == 'case-study' else ''
            paper = t['baseline']['paper'] if t['baseline']['paper'] is not None else '—'
            rows.append(f'| [{t["title"]}{case}](tasks/{t["id"]}/) · `{t["id"]}` | '
                        f'`{t["project"]}/{t["data_task"]}` | {metric["name"]} / {metric["unit"]} | '
                        f'{metric["direction"]} | {paper} | {t["baseline"]["reproduction"]} |')
    payload['TASKS.md'] = ('\n'.join(rows) + '\n').encode()
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    catalog = json.loads((ROOT / 'catalog.json').read_text())
    stale = []
    payload = collection_files(catalog)
    for spec in catalog['tasks']:
        for name, contents in files(spec).items():
            payload[f'tasks/{spec["id"]}/{name}'] = contents
    for name, contents in payload.items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_bytes() != contents:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(contents)
            path.chmod(0o755 if name.endswith('.sh') else 0o644)
    if stale:
        raise SystemExit('Stale generated files:\n'+'\n'.join(stale))
    print(f'{"Checked" if args.check else "Generated"} {len(catalog["tasks"])} standalone Harbor tasks')


if __name__ == '__main__':
    main()
