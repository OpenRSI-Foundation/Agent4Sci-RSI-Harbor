import argparse
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import collection


class CollectionTests(unittest.TestCase):
    def test_suite_case_and_domain_manifests_partition_the_catalog(self):
        tasks=collection.catalog()
        suite=collection.select(tasks,track='suite')
        cases=collection.select(tasks,track='case-study')
        self.assertEqual((len(suite),len(cases)),(25,1))
        self.assertEqual(cases[0]['project'],'PFDelta_2000')
        self.assertEqual(len(collection.select(tasks,domain='chemistry')),4)
        self.assertEqual(len(collection.select(tasks,project='CheMixHub')),3)
        expected={f'rsi-tasks/{t["id"]}' for t in tasks}
        domain_paths=[]
        for path in (ROOT/'collections/domains').glob('*.txt'):
            domain_paths.extend(path.read_text().splitlines())
        self.assertEqual(len(domain_paths),26)
        self.assertEqual(set(domain_paths),expected)
        for name,group in [('all',tasks),('suite',suite),('case-study',cases)]:
            self.assertEqual((ROOT/f'collections/{name}.txt').read_text().splitlines(),
                             [f'rsi-tasks/{t["id"]}' for t in group])

    def test_unknown_filters_and_tasks_fail_instead_of_selecting_everything(self):
        tasks=collection.catalog()
        for selector in ({'domain':'unknown'},{'project':'unknown'}):
            with self.assertRaises(ValueError):collection.select(tasks,**selector)
        for name in ('../README.md','agent4sci','pfdelta'):
            with self.assertRaises(ValueError):collection.resolve(tasks,name)
        self.assertEqual(collection.resolve(tasks,'pfdelta-ieee118')['project'],'PFDelta')

    def test_launch_protocol_and_argument_boundaries(self):
        task=collection.catalog()[0]
        args=argparse.Namespace(gpus='0,1,2,3,4,5,6,7',agent='codex',model='model; echo bad',
                                logs_root=Path('/tmp/log path'),data_root=None)
        command=collection.run_command(task,args)
        self.assertEqual(command[command.index('--max-submissions')+1],'1')
        self.assertEqual(command[command.index('--primary-reward')+1],'reward')
        self.assertEqual(command[command.index('--score-direction')+1],'maximize')
        self.assertIn('model; echo bad',command)
        self.assertIn('/tmp/log path',command)
        self.assertTrue(Path(command[2]).is_absolute())
        self.assertEqual(Path(command[2]), ROOT/'rsi-tasks'/task['id'])
        self.assertTrue((Path(command[2])/'task.toml').is_file())
        for gpus in ('0','0,1,2,3,4,5,6,6','0,1,2,3,4,5,6,'):
            args.gpus=gpus
            with self.assertRaises(ValueError):collection.run_command(task,args)

    def test_preview_never_starts_a_job_or_requires_credentials(self):
        with contextlib.redirect_stdout(io.StringIO()) as output, \
             patch.object(collection.subprocess,'run') as launch:
            self.assertEqual(collection.main(['run','pfdelta-ieee118','--gpus','0,1,2,3,4,5,6,7']),0)
        launch.assert_not_called()
        self.assertIn('--max-submissions 1',output.getvalue())

    def test_execute_uses_argv_and_propagates_exit_code(self):
        with contextlib.redirect_stdout(io.StringIO()),patch.object(collection.shutil,'which',return_value='/bin/rsi-harness'), \
             patch.dict(collection.os.environ,ANTHROPIC_API_KEY='test-only',AGENT4SCI_JUDGE_MODEL='fixture'), \
             patch.object(collection.subprocess,'run',return_value=argparse.Namespace(returncode=7)) as launch:
            result=collection.main(['run','pfdelta-ieee118','--gpus','0,1,2,3,4,5,6,7','--execute'])
        self.assertEqual(result,7)
        self.assertEqual(launch.call_args.kwargs,{'check':False})
        self.assertIsInstance(launch.call_args.args[0],list)


if __name__=='__main__':unittest.main()
