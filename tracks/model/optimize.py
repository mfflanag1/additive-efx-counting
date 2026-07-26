"""Simulated-annealing optimizer to MINIMIZE efx0_count (0=witness).
Restarts from best-so-far, geometric cooling, single/double-entry moves.
Usage: python3 optimize.py <rng_seed> <steps> <seed_json> [m]"""
import json
import math
import random
import sys
from verify import enumerate_all


def count(vals, m):
    return enumerate_all(4, m, vals)["efx0_count"]

def distinct_rows(vals):
    return len({tuple(r) for r in vals})

def distinct_vals(vals):
    return len({x for r in vals for x in r})

def valid(vals):
    return distinct_rows(vals) == 4 and distinct_vals(vals) >= 3


def anneal(seed, m, steps, rng, cap=60):
    rnd = random.Random(rng)
    cur = [list(r) for r in seed]
    curc = count(cur, m)
    best = [list(r) for r in cur]; bestc = curc
    T0, T1 = 4.0, 0.05
    for t in range(steps):
        T = T0 * (T1 / T0) ** (t / steps)
        trial = [list(r) for r in cur]
        # move: perturb 1 or 2 entries
        nmoves = 1 if rnd.random() < 0.75 else 2
        for _ in range(nmoves):
            i = rnd.randrange(4); g = rnd.randrange(m)
            trial[i][g] = max(1, min(cap, trial[i][g] + rnd.choice([-4,-3,-2,-1,1,2,3,4])))
        if not valid(trial):
            continue
        c = count(trial, m)
        if c <= curc or rnd.random() < math.exp((curc - c) / max(T, 1e-6)):
            cur, curc = trial, c
            if c < bestc:
                best, bestc = [list(r) for r in trial], c
        # restart from best occasionally when stuck
        if t % 200 == 199:
            cur = [list(r) for r in best]; curc = bestc
    return best, bestc


if __name__ == "__main__":
    rng = int(sys.argv[1]); steps = int(sys.argv[2]); seed = json.loads(sys.argv[3])
    m = int(sys.argv[4]) if len(sys.argv) > 4 else len(seed[0])
    best, bestc = anneal(seed, m, steps, rng)
    print(json.dumps({"rng": rng, "best": bestc, "values": best,
                      "distinct_rows": distinct_rows(best), "distinct_vals": distinct_vals(best)}))
