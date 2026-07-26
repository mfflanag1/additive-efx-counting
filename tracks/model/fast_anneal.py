"""Deep simulated annealing using the fast numpy counter (search heuristic).
Any low-count result MUST be re-verified with check_candidates.py (verify.py arbiter).
Usage: python3 fast_anneal.py <rng> <steps> <seed_json> [m]"""
import json, math, random, sys
import numpy as np
from tracks.model.fastcount import Counter


def distinct_rows(vals): return len({tuple(r) for r in vals})
def distinct_vals(vals): return len({x for r in vals for x in r})
def valid(vals): return distinct_rows(vals) == 4 and distinct_vals(vals) >= 3


def anneal(seed, m, steps, rng, cap=60):
    rnd = random.Random(rng)
    C = Counter(m)
    cur = [list(r) for r in seed]; curc = C.efx0_count(cur)
    best = [list(r) for r in cur]; bestc = curc
    T0, T1 = 5.0, 0.03
    stale = 0
    for t in range(steps):
        T = T0 * (T1 / T0) ** (t / steps)
        trial = [list(r) for r in cur]
        nmoves = 1 if rnd.random() < 0.7 else 2
        for _ in range(nmoves):
            i = rnd.randrange(4); g = rnd.randrange(m)
            trial[i][g] = max(1, min(cap, trial[i][g] + rnd.choice([-5,-3,-2,-1,1,2,3,5])))
        if not valid(trial):
            continue
        c = C.efx0_count(trial)
        if c <= curc or rnd.random() < math.exp((curc - c) / max(T, 1e-6)):
            cur, curc = trial, c
            if c < bestc:
                best, bestc = [list(r) for r in trial], c; stale = 0
            else:
                stale += 1
        else:
            stale += 1
        if stale > 0 and t % 400 == 399:
            cur = [list(r) for r in best]; curc = bestc; stale = 0
        if bestc == 0:
            break
    return best, bestc


if __name__ == "__main__":
    rng = int(sys.argv[1]); steps = int(sys.argv[2]); seed = json.loads(sys.argv[3])
    m = int(sys.argv[4]) if len(sys.argv) > 4 else len(seed[0])
    best, bestc = anneal(seed, m, steps, rng)
    print(json.dumps({"rng": rng, "best": bestc, "values": best,
                      "distinct_rows": distinct_rows(best), "distinct_vals": distinct_vals(best)}))
