#!/usr/bin/python3
"""Root-owned sudo helper: run inference as agent without evaluator credentials."""
import os
import pwd
import sys

if len(sys.argv) < 2:
    raise SystemExit('usage: sudo agent4sci-candidate COMMAND [ARGS...]')
user = pwd.getpwnam('agent')
env = {'HOME': user.pw_dir, 'USER': 'agent', 'LOGNAME': 'agent',
       'PATH': '/home/agent/.local/bin:/usr/local/cuda/bin:/usr/local/bin:/usr/bin:/bin',
       'PYTHONNOUSERSITE': '1', 'TMPDIR': '/tmp'}
for name in ('CUDA_VISIBLE_DEVICES', 'NVIDIA_VISIBLE_DEVICES', 'LD_LIBRARY_PATH'):
    if name in os.environ:
        env[name] = os.environ[name]
os.setgroups([])
os.setgid(user.pw_gid)
os.setuid(user.pw_uid)
os.chdir('/workspace/runs')
os.execvpe(sys.argv[1], sys.argv[1:], env)
