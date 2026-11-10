"""Build tiny synthetic submissions; no benchmark data or checkpoints."""
import hashlib
import json
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parent
work=ROOT/'workspace'
(work/'runs/best_checkpoints').mkdir(parents=True)
(work/'runs/best_checkpoints/model.txt').write_text('synthetic checkpoint')
for name in ('SUMMARY.md','METHODOLOGY.md'):
    (work/'runs'/name).write_text('Synthetic contract-test submission, not scientific results.\n')
shutil.copyfile(ROOT/'infer.py',work/'runs/infer.py')
reference=b'Synthetic immutable reference\n'
(work/'task.md').write_bytes(reference)
for spec in json.loads((ROOT/'catalog.json').read_text())['tasks']:
    spec['reference_sha256']={'task.md':hashlib.sha256(reference).hexdigest()}
    for split in ('train','val','test'):
        has_files=bool(spec['data_files'][split])
        spec['data_files'][split]=([f'{spec["project"]}/{spec["data_task"]}/{split}/fixture.txt']
                                   if has_files else [])
        if split!='test' and has_files:
            path=work/'data'/spec['data_task']/split
            path.mkdir(parents=True,exist_ok=True)
            (path/'fixture.txt').write_text(f'synthetic {split} input')
    folder=ROOT/'specs'/spec['id'];folder.mkdir(parents=True)
    (folder/'spec.json').write_text(json.dumps(spec))
    (folder/'evaluation.md').write_text('Synthetic evaluation instructions; no scientific score.\n')
captured=ROOT/'trajectory';captured.mkdir()
files=[]
for name in ('agent_prompt.md','agent_output.txt'):
    payload=f'Complete synthetic host {name}\n'.encode()
    (captured/name).write_bytes(payload)
    files.append({'path':name,'bytes':len(payload),'source_size':len(payload),'offset':0,
                  'truncated':False,'sha256':hashlib.sha256(payload).hexdigest(),'previous_size':None})
(captured/'manifest.json').write_text(json.dumps({
    'schema_version':1,'round_id':'agent-1','previous_round_id':None,'limit_bytes':268435456,'files':files}))
