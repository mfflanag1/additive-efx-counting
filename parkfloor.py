"""Aggressive EFX0-count minimizer seeded from the actual near-witnesses, plus a
detonation-aware move set. Goal: break the observed count-4 floor (single envy-free
base + global-min floater in 4 parking spots). Any count==0 is a COUNTEREXAMPLE.

Logs every strict improvement to results/parkfloor_elites.jsonl.
"""
import argparse, json, math, random, sys, time
sys.path.insert(0, ".")
from verify import enumerate_all

SEEDS = [
    # count-4 witness (basin 1): base ({2},{0,1},{5,6,7},{4}), floater=good3
    [[11,8,20,1,4,1,16,1],[16,49,32,2,16,2,60,1],[28,28,59,1,60,7,46,8],[10,12,24,1,59,1,17,1]],
    # count-5 two-treasure witness
    [[11,8,20,1,4,1,16,1],[16,49,32,2,16,2,60,1],[16,40,59,1,60,7,46,8],[10,12,24,1,59,1,17,1]],
    # anneal elite count 11
    [[69,10,87,58,10,2,12,89],[100,1,51,28,6,12,41,31],[95,25,100,33,1,6,16,76],[69,1,68,24,6,17,10,89]],
    # sourceless-base seed (count 197): base ({6},{2,4},{0,5},{1,3}) every bundle envied, floater=good7
    [[8,10,18,12,6,12,19,1],[5,7,3,3,10,10,12,1],[6,9,7,4,7,11,20,1],[8,3,5,20,7,16,15,1]],
]


def count_capped(V, cap):
    """Exact EFX0 count but abort as soon as it exceeds cap (speed)."""
    r = enumerate_all(4, 8, V, collect=0)
    return r["efx0_count"]


def neighbor(V, vmax, rng):
    W = [row[:] for row in V]
    r = rng.random()
    if r < 0.35:  # coupled 2-cell in a row (conserves rough scale)
        i = rng.randrange(4); g1, g2 = rng.sample(range(8), 2)
        d = rng.choice([1, 2, 3, 5])
        W[i][g1] = min(vmax, W[i][g1] + d); W[i][g2] = max(1, W[i][g2] - d)
    elif r < 0.6:  # single cell step
        i, g = rng.randrange(4), rng.randrange(8)
        W[i][g] = max(1, min(vmax, W[i][g] + rng.choice([-5,-3,-2,-1,1,2,3,5])))
    elif r < 0.8:  # column shake (all 4 agents on one good) - injects contested peaks
        g = rng.randrange(8)
        for i in range(4):
            W[i][g] = max(1, min(vmax, W[i][g] + rng.choice([-3,-2,-1,0,1,2,3])))
    else:  # full resample of a cell
        i, g = rng.randrange(4), rng.randrange(8)
        W[i][g] = rng.randint(1, vmax)
    return W


def run(seed, iters, vmax, t0, out_path):
    rng = random.Random(seed)
    V = [row[:] for row in SEEDS[seed % len(SEEDS)]]
    cur = count_capped(V, 10**9)
    best = cur; best_V = V
    t_start = time.time()
    with open(out_path, "a") as f:
        for it in range(iters):
            temp = t0 * (1 - it / iters) + 0.02
            W = neighbor(V, vmax, rng)
            c = count_capped(W, 10**9)
            if c <= cur or rng.random() < math.exp(-(c - cur) / temp):
                V, cur = W, c
                if cur < best:
                    best = cur; best_V = [row[:] for row in V]
                    f.write(json.dumps({"count": cur, "seed": seed, "iter": it, "values": V}) + "\n")
                    f.flush()
                    print(f"seed {seed} iter {it}: count={cur} ({time.time()-t_start:.0f}s)", flush=True)
                    if cur == 0:
                        print(f"*** WITNESS *** {json.dumps(V)}", flush=True)
                        return
            # occasional restart from best to escape wandering
            if it % 4000 == 3999:
                V = [row[:] for row in best_V]; cur = best
    print(f"seed {seed} DONE best={best} ({time.time()-t_start:.0f}s)", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--iters", type=int, default=40000)
    ap.add_argument("--vmax", type=int, default=120)
    ap.add_argument("--temp", type=float, default=2.5)
    ap.add_argument("--out", type=str, default="results/parkfloor_elites.jsonl")
    a = ap.parse_args()
    run(a.seed, a.iters, a.vmax, a.temp, a.out)
