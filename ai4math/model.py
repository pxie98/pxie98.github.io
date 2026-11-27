"""Dependency-free, synthetic graph-smoothed breakthrough-velocity baseline.
Run: python3 model.py (writes demo-data.js). No fitted forecast or probabilities.
"""
import json
from datetime import date, timedelta
from pathlib import Path

FIELDS = ['组合数学 / Combinatorics', '数论 / Number theory', '代数 / Algebra',
          '几何与拓扑 / Geometry & topology', '优化 / Optimization', '数值分析 / Numerical analysis']
# Hand-specified demonstration graph, NOT an inferred MSC knowledge graph.
EDGES = [(0, 1), (0, 2), (0, 4), (1, 2), (2, 3), (2, 5), (4, 5)]
CUTOFF = date(2026, 11, 27)

def velocity(events, cutoff, days, weights=None):
    """Use first VERIFIED availability in (cutoff-days, cutoff]; unique event IDs.
    Fractional field assignments sum to one, preventing cross-field double counts.
    Only verified open-problem resolutions are included in this strict endpoint.
    """
    if days <= 0:
        raise ValueError('days must be positive')
    weights = weights or {'independent': 1., 'collaborative': .5, 'assistance': .2}
    result = [0.] * len(FIELDS)
    seen = set()
    for e in events:
        if e['id'] in seen:
            raise ValueError('Duplicate event ID: ' + e['id'])
        seen.add(e['id'])
        if e['status'] != 'verified' or e['type'] != 'open_problem_resolution':
            continue
        available = date.fromisoformat(e['verified_available'])
        if not cutoff - timedelta(days=days) < available <= cutoff:
            continue
        assignments = e['fields']
        if not assignments or abs(sum(assignments.values()) - 1) > 1e-9:
            raise ValueError('Field assignments must sum to one')
        if any(not 0 <= int(i) < len(FIELDS) or a < 0 for i, a in assignments.items()):
            raise ValueError('Invalid field assignment')
        difficulty = e['difficulty']
        if not 0 < difficulty <= 5:
            raise ValueError('Difficulty must be in (0, 5]')
        for i, fraction in assignments.items():
            result[int(i)] += fraction * weights[e['ai_role']] * difficulty / days * 365
    return result

def smooth(values, strength, edges=EDGES):
    """Solve (I + strength*L) s = v with Gaussian elimination; L = D-A."""
    if strength < 0:
        raise ValueError('strength must be nonnegative')
    n = len(values)
    a = [[float(i == j) for j in range(n)] + [values[i]] for i in range(n)]
    for i, j in edges:
        a[i][i] += strength
        a[j][j] += strength
        a[i][j] -= strength
        a[j][i] -= strength
    for i in range(n):
        pivot = a[i][i]
        a[i] = [x / pivot for x in a[i]]
        for j in range(n):
            if j != i:
                scale = a[j][i]
                a[j] = [x - scale*y for x, y in zip(a[j], a[i])]
    return [row[-1] for row in a]

def main():
    root = Path(__file__).resolve().parent
    events = json.loads((root / 'synthetic-events.json').read_text())['events']
    scenarios = {}
    for days in [90, 180, 365]:
        v = velocity(events, CUTOFF, days)
        for strength in [0, .5, 2]:
            scenarios[f'{days}:{strength:g}'] = {'velocity': v, 'score': smooth(v, strength)}
    data = {'synthetic': True, 'cutoff': str(CUTOFF), 'fields': FIELDS, 'edges': EDGES, 'scenarios': scenarios}
    (root / 'demo-data.js').write_text('window.AI4MATH_DEMO = ' + json.dumps(data, ensure_ascii=False, indent=2) + ';\n')

if __name__ == '__main__':
    main()
