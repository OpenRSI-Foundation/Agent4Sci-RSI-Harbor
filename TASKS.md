# Complete task catalog

25 suite tasks plus the separately marked PFDelta-2000 case study. Baselines are upstream reports, not new measurements. Every task has an independent RSI task in Harbor 1.4 format, a readable name and its own fixed protocol.

Generated from [catalog.json](catalog.json). Use [collections/](collections/) for plain-text manifests or `python3 tools/collection.py list --domain Chemistry` to filter tasks.

| Domain | Suite | Case study | Manifest |
|---|---:|---:|---|
| [Astronomy](#astronomy) | 3 | 0 | [paths](collections/domains/astronomy.txt) |
| [Bioengineering](#bioengineering) | 5 | 0 | [paths](collections/domains/bioengineering.txt) |
| [Biology](#biology) | 1 | 0 | [paths](collections/domains/biology.txt) |
| [Chemistry](#chemistry) | 4 | 0 | [paths](collections/domains/chemistry.txt) |
| [Cosmology](#cosmology) | 3 | 0 | [paths](collections/domains/cosmology.txt) |
| [Ecology](#ecology) | 2 | 0 | [paths](collections/domains/ecology.txt) |
| [Genomics](#genomics) | 1 | 0 | [paths](collections/domains/genomics.txt) |
| [Geography](#geography) | 2 | 0 | [paths](collections/domains/geography.txt) |
| [Geology](#geology) | 1 | 0 | [paths](collections/domains/geology.txt) |
| [Neuroscience](#neuroscience) | 1 | 0 | [paths](collections/domains/neuroscience.txt) |
| [Physics](#physics) | 2 | 1 | [paths](collections/domains/physics.txt) |

## Astronomy

| Task and directory | Upstream subtask | Metric / units | Direction | Paper | Reproduction |
|---|---|---|---|---|---|
| [ATAT: transient classification](tasks/agent4sci-atat-transient/) · `agent4sci-atat-transient` | `ATAT/atat_transient` | macro_f1 / percent | maximize | 83.5 | 82.79 |
| [Mars-Bench: terrain segmentation](tasks/agent4sci-mars-terrain/) · `agent4sci-mars-terrain` | `Mars-Bench/s5mars` | iou / fraction | maximize | 0.1806 | 0.18 |
| [Mars-Bench: cone detection](tasks/agent4sci-mars-cones/) · `agent4sci-mars-cones` | `Mars-Bench/conequest_det` | map / fraction | maximize | 0.1599 | 0.1654 |

## Bioengineering

| Task and directory | Upstream subtask | Metric / units | Direction | Paper | Reproduction |
|---|---|---|---|---|---|
| [ESCAPE: antimicrobial-peptide classification](tasks/agent4sci-escape-amp/) · `agent4sci-escape-amp` | `ESCAPE/amp_classification` | overall_map / percent | maximize | 72.1 | 71.8 |
| [MOTIVE: cold-source link prediction](tasks/agent4sci-motive-cold-source/) · `agent4sci-motive-cold-source` | `MOTIVE/cold_source` | f1 / fraction | maximize | 0.2827 | 0.2972 |
| [ProteinGym: DMS substitution fitness](tasks/agent4sci-proteingym-fitness/) · `agent4sci-proteingym-fitness` | `ProteinGym/kermut_dms_sub` | spearman / correlation | maximize | 0.657 | 0.6561 |
| [UniSite: ligand binding-site detection](tasks/agent4sci-unisite-binding-sites/) · `agent4sci-unisite-binding-sites` | `UniSite/binding_site_detection` | ap_0_5 / fraction | maximize | 0.3835 | 0.383 |
| [gRNAde: 3D RNA inverse design](tasks/agent4sci-grnade-rna-design/) · `agent4sci-grnade-rna-design` | `gRNAde/single_state` | recovery_scmcc_composite / fraction | maximize | 0.575 | 0.577 |

## Biology

| Task and directory | Upstream subtask | Metric / units | Direction | Paper | Reproduction |
|---|---|---|---|---|---|
| [SR-CACO-2: microscopy super-resolution](tasks/agent4sci-sr-caco2-x8/) · `agent4sci-sr-caco2-x8` | `SR-CACO-2/sr-x8` | roi_psnr / dB | maximize | 29.19 | 29.03 |

## Chemistry

| Task and directory | Upstream subtask | Metric / units | Direction | Paper | Reproduction |
|---|---|---|---|---|---|
| [CheMixHub: olfactory similarity](tasks/agent4sci-chemixhub-olfactory/) · `agent4sci-chemixhub-olfactory` | `CheMixHub/olfactory` | mae / native | minimize | 0.121 | 0.124 |
| [CheMixHub: motor octane number](tasks/agent4sci-chemixhub-mon/) · `agent4sci-chemixhub-mon` | `CheMixHub/MON` | mae / native | minimize | 4.57 | 4.699 |
| [CheMixHub: polymer conductivity](tasks/agent4sci-chemixhub-spe/) · `agent4sci-chemixhub-spe` | `CheMixHub/SPE` | mae / native | minimize | 0.222 | 0.215 |
| [MassSpecGym: molecule retrieval](tasks/agent4sci-massspecgym-retrieval/) · `agent4sci-massspecgym-retrieval` | `MassSpecGym/molecule_retrieval` | hit_rate_at_1 / percent | maximize | 14.64 | 16.14 |

## Cosmology

| Task and directory | Upstream subtask | Metric / units | Direction | Paper | Reproduction |
|---|---|---|---|---|---|
| [CosmoBench: sigma-8 regression](tasks/agent4sci-cosmobench-tree-regression/) · `agent4sci-cosmobench-tree-regression` | `CosmoBench/tree_regression` | r2_sigma8 / fraction | maximize | 0.82 | 0.808 |
| [CosmoBench: merger-node classification](tasks/agent4sci-cosmobench-merger-nodes/) · `agent4sci-cosmobench-merger-nodes` | `CosmoBench/tree_infilling` | accuracy / fraction | maximize | 0.72 | 0.717 |
| [CosmoBench: galaxy velocity prediction](tasks/agent4sci-cosmobench-velocity/) · `agent4sci-cosmobench-velocity` | `CosmoBench/velocity_camels_sam` | r2_velocity / fraction | maximize | 0.2865 | 0.283 |

## Ecology

| Task and directory | Upstream subtask | Metric / units | Direction | Paper | Reproduction |
|---|---|---|---|---|---|
| [CarbonGlobe: carbon forecasting](tasks/agent4sci-carbonglobe-carbon/) · `agent4sci-carbonglobe-carbon` | `CarbonGlobe/carbon_forecasting` | average_rmse / native | minimize | 0.571 | 0.604 |
| [TreeFinder: dead-tree segmentation](tasks/agent4sci-treefinder-dead-trees/) · `agent4sci-treefinder-dead-trees` | `TreeFinder/dead_tree_seg` | dead_tree_f1 / percent | maximize | 51.9 | 52.6 |

## Genomics

| Task and directory | Upstream subtask | Metric / units | Direction | Paper | Reproduction |
|---|---|---|---|---|---|
| [DART-Eval: GM12878 chromatin activity](tasks/agent4sci-dart-chromatin/) · `agent4sci-dart-chromatin` | `DART-Eval/t4_gm12878` | test_spearman_pos / correlation | maximize | 0.515 | 0.544 |

## Geography

| Task and directory | Upstream subtask | Metric / units | Direction | Paper | Reproduction |
|---|---|---|---|---|---|
| [GEO-Bench-2: crop-type segmentation](tasks/agent4sci-geobench-pastis/) · `agent4sci-geobench-pastis` | `GEO-Bench-2/pastis` | miou / percent | maximize | 43.1 | 45.9 |
| [GTPBD: terraced-parcel segmentation](tasks/agent4sci-gtpbd-terraces/) · `agent4sci-gtpbd-terraces` | `GTPBD/semantic_segmentation` | miou / percent | maximize | 57.16 | 69.87 |

## Geology

| Task and directory | Upstream subtask | Metric / units | Direction | Paper | Reproduction |
|---|---|---|---|---|---|
| [LITHOS: mineral classification](tasks/agent4sci-lithos-minerals/) · `agent4sci-lithos-minerals` | `LITHOS/mineral_classification` | macro_f1 / fraction | maximize | 0.432 | 0.422 |

## Neuroscience

| Task and directory | Upstream subtask | Metric / units | Direction | Paper | Reproduction |
|---|---|---|---|---|---|
| [NeuroGraph: fluid-intelligence regression](tasks/agent4sci-neurograph-intelligence/) · `agent4sci-neurograph-intelligence` | `NeuroGraph/hcp_fi_gnn` | mae / native | minimize | 0.264 | 0.272 |

## Physics

| Task and directory | Upstream subtask | Metric / units | Direction | Paper | Reproduction |
|---|---|---|---|---|---|
| [PFDelta: IEEE-118 power flow](tasks/agent4sci-pfdelta-ieee118/) · `agent4sci-pfdelta-ieee118` | `PFDelta/task_1_3` | average_pbl / native | minimize | 0.4 | 0.39 |
| [PFDelta-2000: latency-constrained power flow **[case study]**](tasks/agent4sci-pfdelta-goc2000/) · `agent4sci-pfdelta-goc2000` | `PFDelta_2000/task_1_3` | average_pbl / native | minimize | — | 1.18 |
| [TIDMAD: dark-matter signal denoising](tasks/agent4sci-tidmad-denoising/) · `agent4sci-tidmad-denoising` | `TIDMAD/denoising` | fine_score / native | maximize | 6.43 | 6.63 |
