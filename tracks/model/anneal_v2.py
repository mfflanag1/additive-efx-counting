"""v2 surrogate annealer: cap up to 100, coupled 2-cell moves (raise v_i(g), lower v_i(g')
in same row to roughly preserve row-sum), reheating restarts. Search heuristic only;
re-verify hits with check_candidates.py. Stops immediately if count hits 0.
Usage: python3 anneal_v2.py <rng> <steps> <seed_json> [cap] [m]"""
import json, math, random, sys
from tracks.model.fastcount import Counter


def distinct_rows(v): return len({tuple(r) for r in v})
def distinct_vals(v): return len({x for r in v for x in r})
def valid(v): return distinct_rows(v) == 4 and distinct_vals(v) >= 3


def anneal(seed, m, steps, rng, cap=100):
    rnd = random.Random(rng)
    C = Counter(m)
    cur = [list(r) for r in seed]
    curcnt, curobj = C.efx0_objective(cur)
    best = [list(r) for r in cur]; bestcnt, bestobj = curcnt, curobj
    T0, T1 = 8.0, 0.02
    stale = 0
    for t in range(steps):
        frac = (t % 1500) / 1500        # sawtooth reheating every 1500 steps
        T = T0 * (T1 / T0) ** frac
        trial = [list(r) for r in cur]
        mv = rnd.random()
        if mv < 0.45:                    # single-cell
            i = rnd.randrange(4); g = rnd.randrange(m)
            trial[i][g] = max(1, min(cap, trial[i][g] + rnd.choice([-6,-4,-2,-1,1,2,4,6])))
        elif mv < 0.85:                  # coupled: raise one, lower another in same row
            i = rnd.randrange(4)
            g1, g2 = rnd.sample(range(m), 2)
            d = rnd.choice([2, 3, 5, 8])
            trial[i][g1] = min(cap, trial[i][g1] + d)
            trial[i][g2] = max(1, trial[i][g2] - d)
        else:                            # big single jump (explore)
            i = rnd.randrange(4); g = rnd.randrange(m)
            trial[i][g] = rnd.randint(1, cap)
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
        if stale > 0 and t % 600 == 599:
            cur = [list(r) for r in best]; curobj, curcnt = bestobj, bestcnt; stale = 0
        if bestcnt == 0:
            break
    return best, bestcnt, bestobj


if __name__ == "__main__":
    rng = int(sys.argv[1]); steps = int(sys.argv[2]); seed = json.loads(sys.argv[3])
    cap = int(sys.argv[4]) if len(sys.argv) > 4 else 100
    m = int(sys.argv[5]) if len(sys.argv) > 5 else len(seed[0])
    best, bestcnt, bestobj = anneal(seed, m, steps, rng, cap)
    print(json.dumps({"rng": rng, "best": bestcnt, "obj": round(bestobj, 3),
                      "values": best, "distinct_rows": distinct_rows(best),
                      "distinct_vals": distinct_vals(best)}))
