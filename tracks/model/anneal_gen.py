"""Generalized surrogate annealer for arbitrary (n, m). Cap, coupled moves, reheating.
Search heuristic only; re-verify hits with check_candidates.py. Stops if count hits 0.
Crash-safe: writes best-so-far to <outpath> on every improvement (survives OOM kills).
Usage: python3 anneal_gen.py <n> <m> <rng> <steps> <seed_json> [cap] [outpath]"""
import json, math, random, sys
from tracks.model.fastcount import Counter


def distinct_rows(v): return len({tuple(r) for r in v})
def distinct_vals(v): return len({x for r in v for x in r})


def valid(v, n):
    return distinct_rows(v) == n and distinct_vals(v) >= 3


def _dump(outpath, obj):
    if outpath:
        tmp = outpath + ".tmp"
        with open(tmp, "w") as f:
            json.dump(obj, f)
        import os
        os.replace(tmp, outpath)


def anneal(seed, n, m, steps, rng, cap=100, outpath=None):
    rnd = random.Random(rng)
    C = Counter(n, m)
    cur = [list(r) for r in seed]
    curcnt, curobj = C.efx0_objective(cur)
    best = [list(r) for r in cur]; bestcnt, bestobj = curcnt, curobj
    T0, T1 = 8.0, 0.02
    stale = 0
    for t in range(steps):
        frac = (t % 1500) / 1500
        T = T0 * (T1 / T0) ** frac
        trial = [list(r) for r in cur]
        mv = rnd.random()
        if mv < 0.45:
            i = rnd.randrange(n); g = rnd.randrange(m)
            trial[i][g] = max(1, min(cap, trial[i][g] + rnd.choice([-6,-4,-2,-1,1,2,4,6])))
        elif mv < 0.85:
            i = rnd.randrange(n)
            g1, g2 = rnd.sample(range(m), 2)
            d = rnd.choice([2, 3, 5, 8])
            trial[i][g1] = min(cap, trial[i][g1] + d)
            trial[i][g2] = max(1, trial[i][g2] - d)
        else:
            i = rnd.randrange(n); g = rnd.randrange(m)
            trial[i][g] = rnd.randint(1, cap)
        if not valid(trial, n):
            continue
        cnt, obj = C.efx0_objective(trial)
        if obj <= curobj or rnd.random() < math.exp((curobj - obj) / max(T, 1e-6)):
            cur, curobj, curcnt = trial, obj, cnt
            if (cnt < bestcnt) or (cnt == bestcnt and obj < bestobj):
                best, bestcnt, bestobj = [list(r) for r in trial], cnt, obj; stale = 0
                _dump(outpath, {"n": n, "m": m, "rng": rng, "best": bestcnt,
                                "obj": round(bestobj, 3), "values": best, "step": t,
                                "distinct_rows": distinct_rows(best),
                                "distinct_vals": distinct_vals(best)})
            else:
                stale += 1
        else:
            stale += 1
        if stale > 0 and t % 600 == 599:
            cur = [list(r) for r in best]; curobj, curcnt = bestobj, bestcnt; stale = 0
        if bestcnt == 0:
            break
    return best, bestcnt, bestobj


if __name__ == "__main__":
    n = int(sys.argv[1]); m = int(sys.argv[2]); rng = int(sys.argv[3])
    steps = int(sys.argv[4]); seed = json.loads(sys.argv[5])
    cap = int(sys.argv[6]) if len(sys.argv) > 6 else 100
    outpath = sys.argv[7] if len(sys.argv) > 7 else None
    best, bestcnt, bestobj = anneal(seed, n, m, steps, rng, cap, outpath)
    print(json.dumps({"n": n, "m": m, "rng": rng, "best": bestcnt, "obj": round(bestobj, 3),
                      "values": best, "distinct_rows": distinct_rows(best),
                      "distinct_vals": distinct_vals(best)}))
