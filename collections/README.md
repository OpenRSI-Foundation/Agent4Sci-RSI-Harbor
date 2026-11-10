# Collection manifests

All manifests are generated from [`catalog.json`](../catalog.json) by
`python3 tools/generate.py`. Each nonempty line is one task directory relative
to the repository root. Every listed task is a standalone Harbor 1.4 package.

| Manifest | Contents |
|---|---|
| [suite.txt](suite.txt) | Exactly the 25 published-suite tasks |
| [case-study.txt](case-study.txt) | PFDelta-2000, outside the published suite |
| [all.txt](all.txt) | All 26 tasks, no duplicates |
| [domains/](domains/) | One disjoint manifest per scientific domain; together all 26 |

Use [TASKS.md](../TASKS.md) for readable task names and metric/baseline tables.
CheMixHub has three independent tasks, CosmoBench three, and Mars-Bench two.
The split tasks have separate 12-hour, eight-H200 allocations; their aggregate
compute differs from the upstream shared-project allocation.

From the repository root:

```bash
# Emit a machine-readable subset, or paths suitable for an external scheduler.
python3 tools/collection.py list --domain Chemistry --format json
python3 tools/collection.py list --track suite --format paths

# Preview one launch command; add --execute only on a prepared host.
python3 tools/collection.py run pfdelta-ieee118 --gpus 0,1,2,3,4,5,6,7
```

The manifests are inventories, not Harbor registry definitions or automatic
batch launchers. See the [README](../README.md) for installation, credentials,
submission limits and the distinction between packaging checks and GPU validation.
