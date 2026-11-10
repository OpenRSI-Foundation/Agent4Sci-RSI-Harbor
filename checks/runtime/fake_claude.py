#!/usr/local/bin/python3
"""CLI protocol fixture: exercises UID, stdin, streams and inference, NOT an LLM."""
import json
import os
import pwd
import subprocess
import sys
from pathlib import Path

assert os.getuid()==pwd.getpwnam('a4sci-judge').pw_uid
assert os.environ['ANTHROPIC_API_KEY']=='fixture-secret-never-print'
prompt=sys.stdin.read()
assert 'READ-ONLY submission snapshot' in prompt
schema=json.loads(sys.argv[sys.argv.index('--json-schema')+1])
task_id=schema['properties']['task_id']['const']
spec=json.loads((Path('/fixtures/specs')/task_id/'spec.json').read_text())
paths=json.loads(Path('/logs/verifier/paths.json').read_text())
assert Path(paths['evaluation_instructions']).is_file()
assert not Path('/workspace/data',spec['data_task'],'test').exists()
if 'components' in schema['properties']:
    adapter=Path(paths['candidate_outputs'])/'loading_adapter.py'
    adapter.write_text(Path('/workspace/runs/infer.py').read_text())
    subprocess.run(['sudo','-n','/usr/local/bin/agent4sci-candidate',
                    '--cwd',paths['candidate_outputs'],sys.executable,str(adapter),
                    '--test-dir',paths['test_data'],'--output-dir',paths['candidate_outputs']],check=True)
    measurement=Path(paths['candidate_outputs'])/'measurement.json'
    assert json.loads(measurement.read_text())['synthetic_fixture'] is True
    result={'task_id':task_id,'status':'ok','metric':spec['metric']['name'],'unit':spec['metric']['unit'],
            'split':'test','full_test_set':True,'protocol_complete':True,
            'components':[{'id':key,'value':spec['baseline']['reproduction'],
                           'evidence':f'SYNTHETIC FIXTURE ONLY: {measurement}'} for key in spec['components']],
            'report':'Synthetic protocol fixture; these values are NOT benchmark measurements.'}
else:
    assert 'rsi-harness' in prompt
    assert Path('/logs/agent/agent_output.txt').read_text().startswith('Complete synthetic')
    assert json.loads(Path('/logs/verifier/evaluation.json').read_text())['task_id']==task_id
    result={'task_id':task_id,'verdict':'CLEAN','complete_trajectory_reviewed':True,
            'evaluation_verified':True,'report':'Synthetic audit fixture, not an integrity assessment.'}
print(json.dumps({'type':'result','is_error':False,'structured_output':result}))
