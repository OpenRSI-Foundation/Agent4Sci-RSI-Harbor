"""Synthetic Hub fixture: never imports a client or performs network I/O."""
from pathlib import Path


def snapshot_download(*, repo_id, repo_type, revision, allow_patterns, local_dir, token):
    assert repo_type=='dataset' and len(revision)==40 and token is False
    for name in allow_patterns:
        assert '/test/' in name
        path=Path(local_dir)/name;path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text('synthetic test input')
