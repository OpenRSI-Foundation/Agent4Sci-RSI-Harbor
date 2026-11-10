"""Real Linux read-only mount + actual evaluator subprocesses, all 26 contracts."""
import errno
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0,'/opt/adapter')
import verifier

try:
    Path('/workspace/readonly-probe').write_text('must fail even as root')
except OSError as error:
    assert error.errno==errno.EROFS, f'Expected a real read-only mount: {error}'
else:
    raise AssertionError('Run this fixture with a read-only /workspace volume')


def inventory():
    return {str(p):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in Path('/workspace').rglob('*') if p.is_file()}


before=inventory()
os.environ.update(ANTHROPIC_API_KEY='fixture-secret-never-print',AGENT4SCI_JUDGE_MODEL='fixture-only',
                  RSI_JUDGE_ISOLATION_FALLBACK='none')
results=[]
for folder in sorted(Path('/fixtures/specs').iterdir()):
    verifier.TESTS=folder
    code=verifier.main()
    output=Path('/logs/verifier')
    target=Path('/results')/folder.name
    try:
        assert code==0, f'Verifier failed for {folder.name}; inspect /results/{folder.name}'
        reward=json.loads((output/'reward.json').read_text())
        assert reward['reward']==0.5
        assert json.loads((output/'provenance.json').read_text())['trajectory_source']=='rsi-harness'
        assert (output/'candidate_outputs/measurement.json').is_file()
        assert inventory()==before
        for path in output.rglob('*'):
            if path.is_file(): assert 'fixture-secret-never-print' not in path.read_text()
        results.append({'task':folder.name,'status':'passed','synthetic_fixture':True})
    finally:
        shutil.move(str(output),str(target))
Path('/results/summary.json').write_text(json.dumps({
    'kind':'synthetic-linux-readonly-contract-test','count':len(results),'tasks':results},indent=2)+'\n')
print(f'PASS: {len(results)} contracts, real read-only mount and UID transitions; no GPU or real LLM calls.')
