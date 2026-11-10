"""Prefer the frozen, host-captured RSI trajectory over candidate-authored logs."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def evidence(work: Path, captured: Path, *, require_host: bool = False) -> dict:
    manifest_path = captured / 'manifest.json'
    if require_host or manifest_path.exists() or manifest_path.is_symlink():
        if captured.is_symlink() or manifest_path.is_symlink():
            raise ValueError('Symlinked host trajectory')
        manifest = json.loads(manifest_path.read_text())
        if manifest.get('schema_version') != 1:
            raise ValueError('Unsupported host trajectory schema')
        entries = manifest.get('files', [])
        if sorted(item['path'] for item in entries) != ['agent_output.txt', 'agent_prompt.md']:
            raise ValueError('Host trajectory is missing the prompt or agent output')
        for item in entries:
            path = captured / item['path']
            if item.get('truncated') is not False or item.get('offset') != 0:
                raise ValueError('Host trajectory is truncated; a complete audit is impossible')
            if path.is_symlink() or not path.is_file():
                raise ValueError('Host trajectory is not a regular file')
            size = path.stat().st_size
            if not size or size != item.get('bytes') or size != item.get('source_size'):
                raise ValueError('Host trajectory length mismatch')
            digest = hashlib.sha256()
            with path.open('rb') as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    digest.update(chunk)
            if digest.hexdigest() != item.get('sha256'):
                raise ValueError('Host trajectory digest mismatch')
        return {'source': 'rsi-harness', 'root': str(captured), 'manifest': manifest}

    # Native Harbor does not provide RSI's /logs/agent contract. Preserve the
    # upstream submission requirement, without calling it host-authenticated.
    path = work / 'runs/hillclimb_logs.jsonl'
    if path.is_symlink() or not path.is_file() or not path.stat().st_size:
        raise ValueError('No host trajectory or complete submitted session log')
    return {'source': 'candidate-provided', 'path': str(path)}
