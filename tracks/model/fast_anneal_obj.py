"""Annealing on the surrogate objective (count + margin tiebreak) to escape plateaus.
Reports the true count of the best. Re-verify hits with check_candidates.py.
Usage: python3 fast_anneal_obj.py <rng> <steps> <seed_json> [m]"""
import json, math, random, sys
from tracks.model.fastcount import Counter


def distinct_rows(vals): return len({tuple(r) for r in vals})
def distinct_vals(vals): return len({x for r in vals for x in r})
def valid(vals): return distinct_rows(vals) == 4 and distinct_vals(vals) >= 3


def anneal(seed, m, steps, rng, cap=60):
    rnd = random.Random(rng)
    C = Counter(m)
    cur = [list(r) for r in seed]
    curcnt, curobj = C.efx0_objective(cur)
    best = [list(r) for r in cur]; bestcnt, bestobj = curcnt, curobj
    T0, T1 = 6.0, 0.02
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
        cnt, obj = C.efx0_objective(trial)
        if obj <= curobj or rnd.random() < math.exp((curobj - obj) / max(T, 1e-6)):
            cur, curobj, curcnt = trial, obj, cnt
            if (cnt < bestcnt) or (cnt == bestcnt and obj < bestobj):
                best, bestcnt, bestobj = [list(r) for r in trial], cnt, obj; stale = 0
            else:
                stale += 1
        else:
            stale += 1
        if stale > 0 and t % 500 == 499:
            cur = [list(r) for r in best]; curobj, curcnt = bestobj, bestcnt; stale = 0
        if bestcnt == 0:
            break
    return best, bestcnt, bestobj


if __name__ == "__main__":
    rng = int(sys.argv[1]); steps = int(sys.argv[2]); seed = json.loads(sys.argv[3])
    m = int(sys.argv[4]) if len(sys.argv) > 4 else len(seed[0])
    best, bestcnt, bestobj = anneal(seed, m, steps, rng)
    print(json.dumps({"rng": rng, "best": bestcnt, "obj": round(bestobj,3), "values": best,
                      "distinct_rows": distinct_rows(best), "distinct_vals": distinct_vals(best)}))
