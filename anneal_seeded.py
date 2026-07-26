"""Seeded simulated annealing on EFX0 count, complementary to boundary.py hill-climb.
Moves: single-cell resample/step + coupled 2-cell (raise one, lower another in same row).
Accepts uphill with temperature. Logs improvements to results/anneal_elites.jsonl.
"""
import argparse
import json
import math
import random
import time

from boundary import count_capped

SEED_INSTANCE = [[14, 2, 49, 1, 12, 8, 1, 19], [6, 12, 13, 10, 12, 3, 7, 40],
                 [14, 8, 20, 1, 14, 13, 8, 26], [18, 1, 56, 1, 13, 11, 1, 22]]


def neighbor(V, n, m, vmax, rng):
    W = [row[:] for row in V]
    if rng.random() < 0.4:  # coupled 2-cell move
        i = rng.randrange(n)
        g1, g2 = rng.sample(range(m), 2)
        d = rng.choice([1, 2, 3])
        W[i][g1] = min(vmax, W[i][g1] + d)
        W[i][g2] = max(1, W[i][g2] - d)
    else:
        i, g = rng.randrange(n), rng.randrange(m)
        if rng.random() < 0.7:
            W[i][g] = max(1, min(vmax, W[i][g] + rng.choice([-3, -2, -1, 1, 2, 3])))
        else:
            W[i][g] = rng.randint(1, vmax)
    return W


def run(n, m, vmax, iters, t0_temp, seed, out_path):
    rng = random.Random(seed)
    V = [row[:] for row in SEED_INSTANCE]
    cur = count_capped(n, m, V, 10 ** 9)
    best = cur
    t_start = time.time()
    with open(out_path, "a") as f:
        for it in range(iters):
            temp = t0_temp * (1 - it / iters) + 0.01
            W = neighbor(V, n, m, vmax, rng)
            c = count_capped(n, m, W, int(cur + 3 * temp) + 2)
            if c <= cur or rng.random() < math.exp(-(c - cur) / temp):
                V, cur = W, c
                if cur < best:
                    best = cur
                    f.write(json.dumps({"count": cur, "seed": seed, "iter": it,
                                        "values": V}) + "\n")
                    f.flush()
                    print(f"seed {seed} iter {it}: count={cur} "
                          f"({time.time()-t_start:.0f}s)", flush=True)
                    if cur == 0:
                        print(f"*** WITNESS *** {json.dumps(V)}", flush=True)
                        return
    print(f"seed {seed} done: best={best}", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--iters", type=int, default=30000)
    ap.add_argument("--vmax", type=int, default=100)
    ap.add_argument("--temp", type=float, default=4.0)
    ap.add_argument("--out", type=str, default="results/anneal_elites.jsonl")
    a = ap.parse_args()
    run(4, 8, a.vmax, a.iters, a.temp, a.seed, a.out)
