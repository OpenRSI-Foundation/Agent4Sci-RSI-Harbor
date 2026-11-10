"""Prepare Work at image BUILD time; RSI-Harness overrides image ENTRYPOINT."""
from __future__ import annotations
import hashlib
import json
import os
import pwd
import shutil
import stat
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data import download_split, load_spec


def main() -> None:
    spec = load_spec(Path('/opt/agent4sci/spec.json'))
    source, work = Path('/opt/project'), Path('/workspace')
    work.mkdir(exist_ok=True)
    for name in ('task.md', 'paper', 'repo', 'reproduction'):
        src, dst = source / name, work / name
        if not src.exists():
            raise RuntimeError(f'Pinned image is missing {src}')
        if dst.exists():
            raise RuntimeError(f'Unexpected pre-existing workspace asset: {dst}')
        if src.is_dir():
            shutil.copytree(src, dst, symlinks=True)
        else:
            shutil.copyfile(src, dst)
    for key, digest in spec['reference_sha256'].items():
        path = work / key
        if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise RuntimeError(f'Pinned reference mismatch: {key}')
    shutil.copyfile('/opt/agent4sci/instruction.md', work / 'AGENTS.md')
    shutil.copyfile('/opt/agent4sci/instruction.md', work / 'CLAUDE.md')
    for split in ('train', 'val'):
        download_split(spec, split, work / 'data' / spec['data_task'] / split)
    if any((work / 'data').rglob('test')):
        raise RuntimeError('A test directory unexpectedly exists in Work')
    shutil.rmtree(source)
    Path('/tmp/download_data.py').unlink(missing_ok=True)
    Path('/entrypoint.sh').unlink(missing_ok=True)
    identity = pwd.getpwnam('agent')
    runs = work / 'runs'
    runs.mkdir()
    os.chown(runs, identity.pw_uid, identity.pw_gid)
    for name in ('task.md', 'AGENTS.md', 'CLAUDE.md', 'repo', 'reproduction', 'paper', 'data'):
        root = work / name
        paths = [root, *root.rglob('*')] if root.is_dir() else [root]
        for path in paths:
            if not path.is_symlink():
                path.chmod(path.stat().st_mode & ~(stat.S_IWGRP | stat.S_IWOTH | stat.S_IWUSR))
    sudoers = Path('/etc/sudoers')
    if sudoers.exists():
        sudoers.write_text('\n'.join(line for line in sudoers.read_text().splitlines()
                                     if not line.lstrip().startswith('agent ')) + '\n')
    os.system('gpasswd -d agent sudo >/dev/null 2>&1')
    claude = Path('/opt/agent4sci/judge-cli/node_modules/.bin/claude')
    if not claude.exists():
        raise RuntimeError('Pinned evaluator CLI is missing')
    Path('/opt/agent4sci/claude-path').write_text(str(claude.resolve()) + '\n')
    Path('/opt/agent4sci/prepared.json').write_text(json.dumps({
        'task': spec['id'], 'image': spec['image'], 'dataset': spec['dataset'],
        'splits': ['train', 'val'] if spec['data_files']['val'] else ['train'],
    }, indent=2) + '\n')


if __name__ == '__main__':
    main()
