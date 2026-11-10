"""Pinned, task-scoped Agent4Sci data staging."""
from __future__ import annotations
import json
import shutil
import tempfile
from pathlib import Path


def download_split(spec: dict, split: str, destination: Path) -> None:
    from huggingface_hub import snapshot_download
    if split not in {"train", "val", "test"}:
        raise ValueError(f"Unsupported split: {split}")
    expected = spec["data_files"][split]
    if not expected:
        if split == "val":
            return  # TIDMAD has no upstream validation partition.
        raise ValueError(f"No upstream {split} files in the pinned manifest")
    prefix = f'{spec["project"]}/{spec["data_task"]}/{split}/'
    if any(not name.startswith(prefix) or ".." in Path(name).parts for name in expected):
        raise ValueError("Data manifest escapes the selected task/split")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() or destination.is_symlink():
        raise ValueError(f"Refusing to merge into pre-existing split: {destination}")
    with tempfile.TemporaryDirectory(prefix="agent4sci-download-") as tmp:
        snapshot_download(repo_id=spec["dataset"]["repo"], repo_type="dataset",
                          revision=spec["dataset"]["revision"], allow_patterns=expected,
                          local_dir=tmp, token=False)
        source = Path(tmp) / spec["project"] / spec["data_task"] / split
        actual = sorted(p.relative_to(Path(tmp)).as_posix() for p in source.rglob("*") if p.is_file())
        if actual != sorted(expected) or any(p.is_symlink() for p in source.rglob("*")):
            raise ValueError("Downloaded split does not match the pinned file inventory")
        shutil.copytree(source, destination)


def load_spec(path: Path) -> dict:
    return json.loads(path.read_text())
