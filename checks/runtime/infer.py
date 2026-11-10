"""Run through the REAL candidate helper, as the unprivileged research user."""
import argparse
import hashlib
import json
import os
import pwd
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--test-dir',type=Path,required=True)
parser.add_argument('--output-dir',type=Path,required=True)
args=parser.parse_args()
assert os.getuid()==pwd.getpwnam('agent').pw_uid
assert not any(k in os.environ for k in ('ANTHROPIC_API_KEY','AGENT4SCI_JUDGE_MODEL'))
assert Path.cwd()==args.output_dir
data=(args.test_dir/'fixture.txt').read_bytes()
assert data==b'synthetic test input'
try:
    Path('/workspace/runs/should-not-exist').write_text('bad')
except OSError:
    pass
else:
    raise AssertionError('Candidate mutated the read-only submission')
(args.output_dir/'measurement.json').write_text(json.dumps({
    'synthetic_fixture':True,'uid':os.getuid(),'input_sha256':hashlib.sha256(data).hexdigest()}))
