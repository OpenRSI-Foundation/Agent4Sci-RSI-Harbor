"""Convert independently evaluated, audited metrics into continuous RSI rewards."""
from __future__ import annotations
import math
import statistics


def score(spec: dict, evaluation: dict, audit: dict) -> dict:
    if evaluation.get('status') != 'ok':
        raise ValueError('Evaluation did not complete successfully')
    for field, expected in (('task_id', spec['id']), ('metric', spec['metric']['name']),
                            ('unit', spec['metric']['unit']), ('split', 'test')):
        if evaluation.get(field) != expected:
            raise ValueError(f'Wrong evaluation {field}')
    if evaluation.get('full_test_set') is not True or evaluation.get('protocol_complete') is not True:
        raise ValueError('Incomplete test coverage or seed/fold protocol')
    if audit.get('task_id') != spec['id'] or audit.get('verdict') != 'CLEAN':
        raise ValueError('Audit did not certify a CLEAN submission')
    if audit.get('complete_trajectory_reviewed') is not True:
        raise ValueError('Audit did not review a complete trajectory')
    if audit.get('evaluation_verified') is not True:
        raise ValueError('Audit did not independently verify evaluation evidence')
    components = evaluation.get('components')
    if not isinstance(components, list) or not components:
        raise ValueError('No per-seed/fold measurements')
    names = [item.get('id') for item in components]
    if len(set(names)) != len(names) or set(names) != set(spec['components']):
        raise ValueError('Missing, duplicate, or unexpected measurement components')
    values = []
    for item in components:
        value = item.get('value')
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError('Metrics must be finite numbers')
        lower, upper = spec['metric']['range']
        if (lower is not None and value < lower) or (upper is not None and value > upper):
            raise ValueError('Metric outside its documented range/units')
        if not isinstance(item.get('evidence'), str) or not item['evidence'].strip():
            raise ValueError('Missing raw measurement evidence')
        values.append(value)
    if spec['aggregation'] == 'iqm':
        # scipy.stats.trim_mean(..., proportiontocut=0.25), rounded-down trimming.
        cut = len(values) // 4
        values = sorted(values)[cut:len(values) - cut]
    elif spec['aggregation'] != 'mean':
        raise ValueError('Unknown aggregation')
    metric = statistics.mean(values)
    baseline = spec['baseline']['reproduction']
    direction = 1 if spec['metric']['direction'] == 'maximize' else -1
    improvement = direction * (metric - baseline) / max(abs(baseline), 1e-12)
    reward = 0.5 + math.atan(improvement) / math.pi
    return {'reward': reward, 'metric': metric, 'relative_improvement': improvement}
