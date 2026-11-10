"""Import inspected pinned image metadata into the reviewed 26-task catalog.

Usage: python tools/import_catalog.py --inspection DIR --upstream CLONE
Inspection layout is produced by tools/inspect_images.py. No data/model download.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def units(prefix, values):
    return [f'{prefix}{x}' for x in values]


# Values and protocols transcribed from each digest-pinned image's task.md and
# reproduction/CHANGES.md. Baselines are UPSTREAM claims, not new measurements.
# project, data task, slug suffix, title, metric, unit, direction, paper,
# reproduction, range, required measurement components, aggregation, protocol.
ROWS = [
    ('ATAT','atat_transient','atat-transient','ATAT: transient classification','macro_f1','percent','maximize',83.5,82.79,[0,100],units('fold_',range(5)),'mean','Five ELAsTiCC folds; LC + metadata + features; macro F1 at 2048 days. Report per-fold and mean scores.'),
    ('CarbonGlobe','carbon_forecasting','carbonglobe-carbon','CarbonGlobe: carbon forecasting','average_rmse','native','minimize',.571,.604,[0,None],['all_variables'],'mean','One model predicts all seven variables. Compute RMSE per variable with the original normalization, then equally average all seven.'),
    ('CheMixHub','olfactory','chemixhub-olfactory','CheMixHub: olfactory similarity','mae','native','minimize',.121,.124,[0,None],units('fold_',range(5)),'mean','Five fixed CV folds; perceptual similarity MAE; preserve the upstream fold partitions.'),
    ('CheMixHub','MON','chemixhub-mon','CheMixHub: motor octane number','mae','native','minimize',4.570,4.699,[0,None],units('fold_',range(5)),'mean','Five fixed CV folds; fuel mixture motor octane number (MON), not RON.'),
    ('CheMixHub','SPE','chemixhub-spe','CheMixHub: polymer conductivity','mae','native','minimize',.222,.215,[0,None],units('fold_',range(5)),'mean','Five fixed CV folds; solid polymer electrolyte target ln(kappa); MAE in the original target space.'),
    ('CosmoBench','tree_regression','cosmobench-tree-regression','CosmoBench: sigma-8 regression','r2_sigma8','fraction','maximize',.82,.808,[None,1],['single_run'],'mean','CS-Trees directed merger trees; optimize R2(sigma_8), not saturated R2(Omega_m). Fixed 600/204/196 cosmological configurations, 25 trees per configuration. Paper uncertainty is bootstrap, not seed averaging.'),
    ('CosmoBench','tree_infilling','cosmobench-merger-nodes','CosmoBench: merger-node classification','accuracy','fraction','maximize',.72,.717,[0,1],['single_run'],'mean','CS-Trees-200; classify virtual merger nodes; fixed 120/40/40 trees. k-NN is an allowed baseline. Paper uncertainty is bootstrap.'),
    ('CosmoBench','velocity_camels_sam','cosmobench-velocity','CosmoBench: galaxy velocity prediction','r2_velocity','fraction','maximize',.2865,.2830,[None,1],['single_run'],'mean','CAMELS-SAM point clouds of 5000 galaxies; per-cloud R2 over all nodes and three velocity components, then average test clouds; fixed 600/204/196 clouds.'),
    ('DART-Eval','t4_gm12878','dart-chromatin','DART-Eval: GM12878 chromatin activity','test_spearman_pos','correlation','maximize',.515,.544,[-1,1],['single_run'],'mean','Task 4 GM12878. Spearman on positive test peaks. Upstream reproduction uses full fine-tuning of NT-v2-500m rather than paper LoRA; preserve split and metric.'),
    ('ESCAPE','amp_classification','escape-amp','ESCAPE: antimicrobial-peptide classification','overall_map','percent','maximize',72.1,71.8,[0,100],units('seed_',[42,1665,8914]),'mean','Three seeds 42,1665,8914; two-fold ensemble per seed (six training runs total). Overall mAP across the five labels in percent.'),
    ('GEO-Bench-2','pastis','geobench-pastis','GEO-Bench-2: crop-type segmentation','miou','percent','maximize',43.1,45.9,[0,100],units('seed_',range(5)),'mean','PASTIS, five seeds 0..4. Macro MulticlassJaccardIndex, ignore void class 19. Fixed split-specific tortilla files; final mIoU in percent.'),
    ('GTPBD','semantic_segmentation','gtpbd-terraces','GTPBD: terraced-parcel segmentation','miou','percent','maximize',57.16,69.87,[0,100],['single_run'],'mean','Binary terrace/background segmentation, 512x512 patches, geographic-region 60/20/20 split. mIoU is the mean of BOTH class IoUs; not just foreground IoU.'),
    ('LITHOS','mineral_classification','lithos-minerals','LITHOS: mineral classification','macro_f1','fraction','maximize',.432,.422,[0,1],units('seed_',[0,42,123]),'mean','25 classes, PPL+XPL inputs. Use only the upstream single fixed fold; opposite CV fold would leak test data. Three seeds 0,42,123; mean macro F1.'),
    ('Mars-Bench','s5mars','mars-terrain','Mars-Bench: terrain segmentation','iou','fraction','maximize',.1806,.1800,[0,1],units('seed_',[0,1,10,42,123,1000,1234]),'iqm','S5Mars terrain segmentation, ten classes; seven seeds 0,1,10,42,123,1000,1234. Report IQM (scipy 25% trim_mean). Use pinned upstream absent-class IoU behavior (torchmetrics 1.7.0).'),
    ('Mars-Bench','conequest_det','mars-cones','Mars-Bench: cone detection','map','fraction','maximize',.1599,.1654,[0,1],units('seed_',[0,1,10,42,123,1000,1234]),'iqm','ConeQuest detection, one grayscale band; seven seeds 0,1,10,42,123,1000,1234. Original mAP implementation and 25%-trimmed IQM; full 333-example test split.'),
    ('MassSpecGym','molecule_retrieval','massspecgym-retrieval','MassSpecGym: molecule retrieval','hit_rate_at_1','percent','maximize',14.64,16.14,[0,100],['single_run'],'mean','Mass-based candidates, up to 256 candidates per spectrum; single fixed-seed run. Hit Rate@1 in percent; bootstrap confidence interval uses 20000 resamples, not training runs.'),
    ('MOTIVE','cold_source','motive-cold-source','MOTIVE: cold-source link prediction','f1','fraction','maximize',.2827,.2972,[0,1],units('run_',range(1,6)),'mean','st_expanded graph with all edge types, cold-source new-compound split. Five runs at fixed training seed and splits; variation from sampling/nondeterminism. Select checkpoints by validation Hits@500.'),
    ('NeuroGraph','hcp_fi_gnn','neurograph-intelligence','NeuroGraph: fluid-intelligence regression','mae','native','minimize',.264,.272,[0,None],units('seed_',[123,124]),'mean','HCP fluid intelligence, GNN-based architecture REQUIRED. Two seeds 123,124. Use the upstream variant of MAE exactly, not a standard replacement formula.'),
    ('PFDelta','task_1_3','pfdelta-ieee118','PFDelta: IEEE-118 power flow','average_pbl','native','minimize',.40,.39,[0,None],units('seed_',[11,22,33]),'mean','IEEE-118 full-topology training. Three seeds 11,22,33; within each seed equally average N, N-1, N-2 and close-to-infeasible conditions. ML-only inference; no Newton-Raphson or other iterative solvers.'),
    ('PFDelta_2000','task_1_3','pfdelta-goc2000','PFDelta-2000: latency-constrained power flow','average_pbl','native','minimize',None,1.18,[0,None],units('seed_',[11,22,33]),'mean','GOC-2000 case study (outside the 25-task suite). Three seeds 11,22,33; equal mean over N,N-1,N-2,C2I conditions. Verify GNN-comparable latency against co-measured baseline on the SAME hardware/batch protocol; upstream references ~10-55 ms unbatched or ~1-3 ms batched. Report both timing and PBL. The IEEE-118 ML-only rule does NOT apply to this case study.'),
    ('ProteinGym','kermut_dms_sub','proteingym-fitness','ProteinGym: DMS substitution fitness','spearman','correlation','maximize',.657,.6561,[-1,1],['random','modulo','contiguous'],'mean','Kermut supervised DMS substitutions. Three CV schemes (random,modulo,contiguous), five folds each, For each assay and CV scheme, concatenate predictions from all five folds BEFORE computing Spearman; average assays within each scheme, then average the three schemes. Do not average per-fold correlations. All assays/folds must be covered; seed 2024.'),
    ('SR-CACO-2','sr-x8','sr-caco2-x8','SR-CACO-2: microscopy super-resolution','roi_psnr','dB','maximize',29.19,29.03,[None,None],['CELL0','CELL1','CELL2'],'mean','Separate x8 model per cell type, seed 0. Input 64x64, output 512x512. Within each cell average ROI-only PSNR over thresholds 4..10 using canonical code, then equally average three cell types.'),
    ('TIDMAD','denoising','tidmad-denoising','TIDMAD: dark-matter signal denoising','fine_score','native','maximize',6.43,6.63,[0,None],['single_run'],'mean','Use the Fine Score, not Coarse Score. No upstream val directory: select models using only a documented training holdout. Files named abra_validation under the test directory are HELD OUT, not tuning data.'),
    ('TreeFinder','dead_tree_seg','treefinder-dead-trees','TreeFinder: dead-tree segmentation','dead_tree_f1','percent','maximize',51.9,52.6,[0,100],units('fold_',range(3)),'mean','Three fixed folds: fold_0 seed2025, fold_1 seed2024, fold_2 seed2023. Original random 80/10/10 splits. Dead-tree-class F1 in percent; not macro F1.'),
    ('UniSite','binding_site_detection','unisite-binding-sites','UniSite: ligand binding-site detection','ap_0_5','fraction','maximize',.3835,.3830,[0,1],['single_run'],'mean','UniSite-DS full test set, original AP at IoU threshold 0.5; single run. Preserve original site matching and structure preprocessing.'),
    ('gRNAde','single_state','grnade-rna-design','gRNAde: 3D RNA inverse design','recovery_scmcc_composite','fraction','maximize',.575,.577,[-.5,1],units('seed_',range(3)),'mean','Das single-state split, max_num_conformers=1; seeds 0,1,2. Sample 16 sequences per structure at temperature0.1. Each component=(Recovery+EternaFold scMCC)/2; average full test structures and seeds. Do not substitute a different folding evaluator.'),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inspection', type=Path, required=True)
    parser.add_argument('--upstream', type=Path, required=True)
    args = parser.parse_args()
    revision = subprocess.check_output(['git','-C',str(args.upstream),'rev-parse','HEAD'], text=True).strip()
    dataset = json.loads((args.inspection / 'dataset.json').read_text())
    files = [x['rfilename'] for x in dataset['siblings']]
    registry = {}
    for line in (args.upstream / 'agent4sci/registry.yaml').read_text().splitlines():
        if line and not line.startswith((' ', '#')):
            project = line[:-1]
            registry[project] = {}
        elif line.startswith('  domain: '):
            registry[project]['domain'] = line.split(': ',1)[1]
    target = ROOT / 'upstream'
    target.mkdir(exist_ok=True)
    shutil.copyfile(args.upstream / 'LICENSE', ROOT / 'LICENSE')
    shutil.copyfile(args.upstream / 'agent4sci/registry.yaml', target / 'registry.yaml')
    image_lock, tasks = {}, []
    for row in ROWS:
        project, data_task, slug, title, metric, unit, direction, paper, baseline, bounds, components, aggregation, protocol = row
        project_root = args.inspection / project / 'opt/project'
        image = json.loads((args.inspection / project / 'image.json').read_text())
        folder = target / 'projects' / project
        folder.mkdir(parents=True, exist_ok=True)
        for name in ('task.md','evaluation.md','AGENTS.md'):
            (folder / name).write_text('\n'.join(line.rstrip() for line in (project_root / name).read_text().splitlines()).rstrip()+'\n')
        image_lock[project] = {'image':image['pinned_image'], 'upstream_tag':image['source_image'],
                               'compressed_bytes':sum(x['size'] for x in image['layers'])}
        reference = {}
        for path in sorted(project_root.rglob('*')):
            if path.is_file() and path.name not in ('AGENTS.md','CLAUDE.md','GEMINI.md','evaluation.md'):
                reference[path.relative_to(project_root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        tasks.append({'id':'agent4sci-'+slug, 'title':title, 'project':project,
                      'data_task':data_task, 'domain':registry[project]['domain'],
                      'track':'case-study' if project=='PFDelta_2000' else 'suite',
                      'image':image['pinned_image'], 'upstream_revision':revision,
                      'dataset':{'repo':dataset['id'],'revision':dataset['sha']},
                      'data_files':{split:sorted(f for f in files if f.startswith(f'{project}/{data_task}/{split}/')) for split in ('train','val','test')},
                      'metric':{'name':metric,'unit':unit,'direction':direction,'range':bounds},
                      'baseline':{'paper':paper,'reproduction':baseline,'source':'digest-pinned upstream image /opt/project/task.md','newly_reproduced':False},
                      'components':components, 'aggregation':aggregation, 'protocol':protocol,
                      'reference_sha256':reference, 'judge_cli_version':'2.1.322',
                      'judge_stage_timeout_sec':21600, 'validation_status':'packaged; GPU baseline and real evaluator not yet run'})
    expected = set('/'.join(f.split('/')[:2]) for f in files if '/' in f)
    assert expected == {f'{x["project"]}/{x["data_task"]}' for x in tasks}
    assert set(registry) == {x['project'] for x in tasks}
    (ROOT / 'catalog.json').write_text(json.dumps({'schema_version':1,'upstream_url':'https://github.com/maszhongming/agent4sci','upstream_revision':revision,'tasks':tasks},indent=2)+'\n')
    (target / 'images.lock.json').write_text(json.dumps(image_lock,indent=2)+'\n')
    (target / 'dataset-files.json').write_text(json.dumps({'repository':dataset['id'],'revision':dataset['sha'],'files':files},indent=2)+'\n')
    print(f'Imported {len(tasks)} tasks from {len(registry)} pinned project images')


if __name__ == '__main__':
    main()
