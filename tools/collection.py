"""Browse the complete collection and launch one task with its fixed protocol."""
from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def catalog() -> list[dict]:
    return json.loads((ROOT / 'catalog.json').read_text())['tasks']


def select(tasks: list[dict], *, track='all', domain=None, project=None) -> list[dict]:
    for field, value in [('domain', domain), ('project', project)]:
        if value and value.casefold() not in {t[field].casefold() for t in tasks}:
            raise ValueError(f'Unknown {field}: {value}')
    return [t for t in tasks if (track == 'all' or t['track'] == track)
            and (not domain or t['domain'].casefold() == domain.casefold())
            and (not project or t['project'].casefold() == project.casefold())]


def summary(spec: dict) -> dict:
    return {key: spec[key] for key in ('id', 'title', 'project', 'data_task', 'domain',
                                     'track', 'metric', 'baseline', 'validation_status')} | {
        'path': f'tasks/{spec["id"]}',
    }


def resolve(tasks: list[dict], name: str) -> dict:
    # Exact stable IDs, with a convenience alias omitting only the common prefix.
    matches = [t for t in tasks if name in (t['id'], t['id'].removeprefix('agent4sci-'))]
    if len(matches) != 1:
        raise ValueError(f'Unknown task: {name}; use the list command for task IDs')
    return matches[0]


def run_command(spec: dict, args: argparse.Namespace) -> list[str]:
    devices = [part.strip() for part in args.gpus.split(',')]
    if any(not part for part in devices) or len(set(devices)) != len(devices) or len(devices) < 8:
        raise ValueError('Supply at least 8 distinct GPU IDs for the published task allocation')
    command = ['rsi-harness', 'run', str(ROOT / 'tasks' / spec['id']),
               '--agent', args.agent, '--agent-auth', 'local', '--gpus', ','.join(devices),
               '--primary-reward', 'reward', '--score-direction', 'maximize',
               '--max-submissions', '1']
    for option in ('model', 'logs_root', 'data_root'):
        value = getattr(args, option, None)
        if value:
            command.extend(['--' + option.replace('_', '-'), str(value)])
    return command


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='action', required=True)
    listing = subs.add_parser('list', help='list tasks, optionally filtered')
    listing.add_argument('--track', choices=['all', 'suite', 'case-study'], default='all')
    listing.add_argument('--domain')
    listing.add_argument('--project')
    listing.add_argument('--format', choices=['table', 'json', 'paths'], default='table')
    show = subs.add_parser('show', help='show one complete task contract')
    show.add_argument('task')
    run = subs.add_parser('run', help='print a command; --execute launches it')
    run.add_argument('task')
    run.add_argument('--gpus', required=True, help='explicit ordered GPU IDs, comma-separated')
    run.add_argument('--agent', default='codex')
    run.add_argument('--model')
    run.add_argument('--logs-root', type=Path)
    run.add_argument('--data-root', type=Path)
    run.add_argument('--execute', action='store_true', help='run instead of printing the command')
    args = parser.parse_args(argv)
    try:
        tasks = catalog()
        if args.action == 'list':
            selected = select(tasks, track=args.track, domain=args.domain, project=args.project)
            if not selected:
                raise ValueError('No tasks match the requested filters')
            if args.format == 'json':
                print(json.dumps([summary(t) for t in selected], indent=2))
            elif args.format == 'paths':
                print('\n'.join(f'tasks/{t["id"]}' for t in selected))
            else:
                print('ID\tDOMAIN\tTRACK\tNAME')
                for t in selected:
                    print(f'{t["id"]}\t{t["domain"]}\t{t["track"]}\t{t["title"]}')
            return 0
        spec = resolve(tasks, args.task)
        if args.action == 'show':
            print(json.dumps(spec, indent=2))
            return 0
        command = run_command(spec, args)
        print(shlex.join(command), flush=True)
        if not args.execute:
            return 0
        if not shutil.which(command[0]):
            raise ValueError('Install the pinned RSI-Harness first; see README.md')
        missing = [name for name in ('ANTHROPIC_API_KEY', 'AGENT4SCI_JUDGE_MODEL')
                   if not os.environ.get(name)]
        if missing:
            raise ValueError('Set verifier variables before launching: ' + ', '.join(missing))
        # No shell expansion, no batch GPU allocation, and no override of the
        # single held-out submission cap. Credentials stay in the environment.
        return subprocess.run(command, check=False).returncode
    except ValueError as error:
        parser.error(str(error))


if __name__ == '__main__':
    sys.exit(main())
