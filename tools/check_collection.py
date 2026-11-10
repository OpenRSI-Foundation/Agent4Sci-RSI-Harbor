"""Offline structural checks; optional actual RSI-Harness/Harbor compilation."""
import argparse
import ast
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--require-harness', action='store_true')
    args = parser.parse_args()
    tasks = json.loads((ROOT / 'catalog.json').read_text())['tasks']
    assert len(tasks) == 26
    assert sum(t['track'] == 'suite' for t in tasks) == 25
    registry = {line[:-1] for line in (ROOT / 'upstream/registry.yaml').read_text().splitlines()
                if line and not line.startswith((' ', '#'))}
    assert registry == {t['project'] for t in tasks}
    data = json.loads((ROOT / 'upstream/dataset-files.json').read_text())
    pairs = {'/'.join(name.split('/')[:2]) for name in data['files'] if '/' in name}
    assert pairs == {f'{t["project"]}/{t["data_task"]}' for t in tasks}
    assert {p.name for p in (ROOT / 'rsi-tasks').iterdir()} == {t['id'] for t in tasks}
    for spec in tasks:
        folder = ROOT / 'rsi-tasks' / spec['id']
        config = tomllib.loads((folder / 'task.toml').read_text())
        assert config['schema_version'] == '1.4'
        assert config['task']['name'] == f'rsi/{spec["id"]}'
        assert config['metadata']['category'] == 'Science'
        assert config['metadata']['subcategory'] == spec['domain']
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',spec['id'])
        assert '@sha256:' in spec['image'] and ':latest' not in spec['image']
        assert re.fullmatch('[0-9a-f]{40}',spec['dataset']['revision'])
        assert spec['data_files']['train'] and spec['data_files']['test']
        assert config['agent']['user'] == 'agent'
        assert config['verifier']['user'] == 'root'
        assert config['verifier']['environment_mode'] == 'shared'
        assert config['environment']['gpus'] == 8
        assert config['metadata']['agent4sci']['recommended_max_submissions'] == 1
        assert config['metadata']['rsi_harness']['verifier']['clean_image'] is True
        assert config['metadata']['rsi_harness']['verifier']['visibility'] == 'hidden'
        for role in ('environment','tests'):
            assert json.loads((folder / role / 'spec.json').read_text()) == spec
        subprocess.run(['bash','-n',str(folder / 'tests/test.sh')],check=True)
        for file in folder.rglob('*.py'):
            ast.parse(file.read_text(),filename=str(file))
        assert not any(p.name in {'doc','docs'} for p in folder.rglob('*'))
        assert not any(p.is_symlink() for p in folder.rglob('*'))
        for name in ('LICENSE', 'NOTICE'):
            assert (folder / name).read_bytes() == (ROOT / name).read_bytes()
    subprocess.run([sys.executable,str(ROOT / 'tools/generate.py'),'--check'],check=True)
    print('Coverage: 25 suite tasks + 1 case study; all 21 registered images, 11 domains')
    if args.require_harness:
        from rsi_harness.task.compiler import HarborTaskCompiler
        from rsi_harness.models import CompileOptions
        compiler = HarborTaskCompiler()
        for spec in tasks:
            task = compiler.compile(ROOT/'rsi-tasks'/spec['id'],CompileOptions(primary_reward='reward',max_submissions=1))
            assert task.verifier.primary_reward == 'reward'
            assert task.gpu_requirement.count == 8
            assert task.agent.user == 'agent'
            assert task.verifier.user == 'root'
            assert dict(task.verifier.environment)['ANTHROPIC_API_KEY'] == '${ANTHROPIC_API_KEY}'
            assert not task.agent.secret_env_names
        print('All 26 tasks compiled with actual RSI-Harness/Harbor models')


if __name__ == '__main__':
    main()
