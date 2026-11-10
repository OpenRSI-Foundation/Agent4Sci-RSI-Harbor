import copy
import json
import math
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'adapter'))
import data
import scoring
import verifier

CATALOG = json.loads((ROOT/'catalog.json').read_text())['tasks']


def reports(spec, value=None):
    if value is None:
        value = spec['baseline']['reproduction']
    evaluation = {'task_id':spec['id'],'status':'ok','metric':spec['metric']['name'],
                  'unit':spec['metric']['unit'],'split':'test','full_test_set':True,
                  'protocol_complete':True,'components':[
                      {'id':key,'value':value,'evidence':'judge_outputs/raw.json: measured by trusted evaluator'}
                      for key in spec['components']]}
    audit = {'task_id':spec['id'],'verdict':'CLEAN','complete_trajectory_reviewed':True,
             'evaluation_verified':True,'report':'Test fixture only'}
    return evaluation,audit


class ScoreTests(unittest.TestCase):
    def test_all_baselines_and_directions(self):
        for spec in CATALOG:
            with self.subTest(task=spec['id']):
                e,a = reports(spec)
                self.assertAlmostEqual(scoring.score(spec,e,a)['reward'],.5)
                b = spec['baseline']['reproduction']
                sign = 1 if spec['metric']['direction']=='maximize' else -1
                better,_ = reports(spec,b+sign*abs(b)*.01)
                worse,_ = reports(spec,b-sign*abs(b)*.01)
                self.assertGreater(scoring.score(spec,better,a)['reward'],.5)
                self.assertLess(scoring.score(spec,worse,a)['reward'],.5)

    def test_rejects_incomplete_or_wrong_evaluation(self):
        spec = CATALOG[0]
        for field,value in [('task_id','wrong'),('metric','accuracy'),('unit','fraction'),
                            ('split','val'),('full_test_set',False),('protocol_complete',False),
                            ('status','failed')]:
            with self.subTest(field=field):
                e,a=reports(spec);e[field]=value
                with self.assertRaises(ValueError): scoring.score(spec,e,a)

    def test_all_components_required_no_seed_selection(self):
        spec=CATALOG[0]
        for mode in ('missing','duplicate','extra'):
            e,a=reports(spec)
            if mode=='missing': e['components'].pop()
            elif mode=='duplicate': e['components'][-1]=e['components'][0]
            else: e['components'].append({'id':'unknown','value':90,'evidence':'x'})
            with self.subTest(mode=mode), self.assertRaises(ValueError): scoring.score(spec,e,a)

    def test_bad_numbers_and_units(self):
        for value in (float('nan'),float('inf'),-float('inf'),True,'90',101,-1):
            e,a=reports(CATALOG[0]);e['components'][0]['value']=value
            with self.subTest(value=value),self.assertRaises(ValueError): scoring.score(CATALOG[0],e,a)

    def test_negative_r2_is_valid(self):
        spec=next(s for s in CATALOG if s['metric']['name']=='r2_sigma8')
        e,a=reports(spec,-2.0)
        self.assertGreater(scoring.score(spec,e,a)['reward'],0)
        self.assertLess(scoring.score(spec,e,a)['reward'],.5)

    def test_missing_evidence(self):
        e,a=reports(CATALOG[0]);e['components'][0]['evidence']=''
        with self.assertRaises(ValueError): scoring.score(CATALOG[0],e,a)

    def test_audit_must_be_complete_clean_and_verified(self):
        for field,value in [('verdict','COMPROMISED'),('verdict','INCOMPLETE'),
                            ('complete_trajectory_reviewed',False),('evaluation_verified',False),
                            ('task_id','other')]:
            e,a=reports(CATALOG[0]);a[field]=value
            with self.subTest(field=field,value=value),self.assertRaises(ValueError):
                scoring.score(CATALOG[0],e,a)

    def test_iqm_not_mean_or_best_seed(self):
        spec=next(s for s in CATALOG if s['aggregation']=='iqm')
        e,a=reports(spec)
        for item,value in zip(e['components'],[0,.1,.2,.3,.4,.5,1]): item['value']=value
        self.assertAlmostEqual(scoring.score(spec,e,a)['metric'],.3)


class StreamTests(unittest.TestCase):
    def parse(self,records):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'stream.jsonl';p.write_text('\n'.join(json.dumps(r) for r in records))
            return verifier.result_from_stream(p)

    def test_only_trusted_final_envelope(self):
        self.assertEqual(self.parse([{'type':'assistant','message':'fake score'},
            {'type':'result','is_error':False,'structured_output':{'status':'ok'}}]),{'status':'ok'})

    def test_rejects_failures_missing_and_ambiguous_results(self):
        result={'type':'result','is_error':False,'structured_output':{'status':'ok'}}
        for records in ([],[dict(result,is_error=True)],[result,result],
                        [{'type':'result','is_error':False,'result':'score=1'}]):
            with self.subTest(records=records),self.assertRaises(ValueError): self.parse(records)


class DataTests(unittest.TestCase):
    def setUp(self):
        self.spec={'project':'P','data_task':'sub','dataset':{'repo':'owner/repo','revision':'a'*40},
                   'data_files':{'train':['P/sub/train/a.txt'],'val':[],'test':['P/sub/test/b.txt']}}

    def fake(self,**kwargs):
        self.assertEqual(kwargs['revision'],'a'*40)
        self.assertIs(kwargs['token'],False)
        for name in kwargs['allow_patterns']:
            p=Path(kwargs['local_dir'])/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(name)

    def test_exact_split_scoping_and_no_work_test_data(self):
        with tempfile.TemporaryDirectory() as tmp,patch.dict(sys.modules,{'huggingface_hub':types.SimpleNamespace(snapshot_download=self.fake)}):
            dest=Path(tmp)/'data/sub/train';data.download_split(self.spec,'train',dest)
            self.assertEqual((dest/'a.txt').read_text(),'P/sub/train/a.txt')
            self.assertFalse((dest.parent/'test').exists())
            data.download_split(self.spec,'val',dest.parent/'val')
            self.assertFalse((dest.parent/'val').exists())

    def test_rejects_preexisting_split_and_cross_task_manifest(self):
        with tempfile.TemporaryDirectory() as tmp,patch.dict(sys.modules,{'huggingface_hub':types.SimpleNamespace(snapshot_download=self.fake)}):
            with self.assertRaises(ValueError):data.download_split(self.spec,'test',Path(tmp))
            bad=copy.deepcopy(self.spec);bad['data_files']['train']=['P/other/test/secret']
            with self.assertRaises(ValueError):data.download_split(bad,'train',Path(tmp)/'new')

    def test_missing_download_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp,patch.dict(sys.modules,{'huggingface_hub':types.SimpleNamespace(snapshot_download=lambda **kw:None)}):
            with self.assertRaises(ValueError):data.download_split(self.spec,'test',Path(tmp)/'test')


class VerifierFlowTests(unittest.TestCase):
    def fixture(self,tmp):
        root=Path(tmp);work=root/'work';out=root/'logs';tests=root/'tests'
        spec=copy.deepcopy(CATALOG[0]);spec['reference_sha256']={}
        (work/'runs/best_checkpoints').mkdir(parents=True)
        (work/'runs/best_checkpoints/model').write_text('fixture')
        for name in ('SUMMARY.md','METHODOLOGY.md','hillclimb_logs.jsonl'):(work/'runs'/name).write_text('fixture')
        (work/'data'/spec['data_task']).mkdir(parents=True)
        tests.mkdir();(tests/'spec.json').write_text(json.dumps(spec))
        return spec,work,out,tests

    def test_end_to_end_mocked_judge_all_tasks(self):
        # Exercise orchestration and scoring without claiming GPU/LLM validation.
        for catalog_spec in CATALOG:
            with self.subTest(task=catalog_spec['id']),tempfile.TemporaryDirectory() as tmp:
                _,work,out,tests=self.fixture(tmp)
                spec=copy.deepcopy(catalog_spec);spec['reference_sha256']={}
                (work/'data'/spec['data_task']).mkdir(parents=True,exist_ok=True)
                (tests/'spec.json').write_text(json.dumps(spec))
                e,a=reports(spec)
                def stage(name,prompt,actual,directory):
                    self.assertIn(spec['protocol'],prompt)
                    return e if name=='evaluation' else a
                with patch.multiple(verifier,WORK=work,OUTPUT=out,TESTS=tests), \
                     patch.dict(os.environ,ANTHROPIC_API_KEY='fixture',AGENT4SCI_JUDGE_MODEL='fixture'), \
                     patch.object(verifier,'download_split',side_effect=lambda s,split,p:p.mkdir()), \
                     patch.object(verifier,'run_stage',side_effect=stage):
                    self.assertEqual(verifier.main(),0)
                self.assertAlmostEqual(json.loads((out/'reward.json').read_text())['reward'],.5)

    def test_audit_failure_removes_stale_reward(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec,work,out,tests=self.fixture(tmp);out.mkdir()
            (out/'reward.json').write_text('{"reward":1}')
            e,a=reports(spec);a['verdict']='COMPROMISED'
            with patch.multiple(verifier,WORK=work,OUTPUT=out,TESTS=tests), \
                 patch.dict(os.environ,ANTHROPIC_API_KEY='fixture',AGENT4SCI_JUDGE_MODEL='fixture'), \
                 patch.object(verifier,'download_split',side_effect=lambda s,split,p:p.mkdir()), \
                 patch.object(verifier,'run_stage',side_effect=[e,a]):
                self.assertEqual(verifier.main(),1)
            self.assertFalse((out/'reward.json').exists())
            self.assertTrue((out/'error.json').exists())

    def test_existing_test_split_and_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec,work,out,tests=self.fixture(tmp)
            (work/'runs/SUMMARY.md').unlink();(work/'runs/SUMMARY.md').symlink_to('/etc/passwd')
            with self.assertRaises(ValueError):verifier.check_submission(work,spec)


if __name__=='__main__':unittest.main()
