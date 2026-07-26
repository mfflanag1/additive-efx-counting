"""Track C: boundary landscape. Hill-climb valuation matrices to MINIMIZE #EFX0
allocations. Instances with tiny EFX0 counts are the cliff edge; count 0 = witness.

Objective evaluated with capped counting (abandon once count exceeds incumbent).
Moves: single-cell resample / +-1. Random restarts. Logs elite instances (count <= elite)
to results/boundary_elites.jsonl for perturbation and lemma telemetry.
"""
import argparse
import json
import random
import time

from verify import check_allocation, masks_from_assign, precompute


def count_capped(n, m, values, cap):
    """Count EFX0 allocations, aborting once count > cap. Returns count (maybe cap+1)."""
    val, minall, minpos = precompute(n, m, values)
    c = 0
    assign = [0] * m
    while True:
        bundles = masks_from_assign(n, assign)
        e0, _ = check_allocation(n, bundles, val, minall, minpos)
        if e0:
            c += 1
            if c > cap:
                return c
        g = 0
        while g < m:
            assign[g] += 1
            if assign[g] < n:
                break
            assign[g] = 0
            g += 1
        else:
            return c


def run(n, m, vmax, restarts, iters, elite, seed, out_path):
    rng = random.Random(seed)
    best_global = None
    t0 = time.time()
    with open(out_path, "a") as elite_f:
        for r in range(restarts):
            V = [[rng.randint(1, vmax) for _ in range(m)] for _ in range(n)]
            cur = count_capped(n, m, V, 10**9)
            for it in range(iters):
                i, g = rng.randrange(n), rng.randrange(m)
                old = V[i][g]
                V[i][g] = (
                    max(1, min(vmax, old + rng.choice([-2, -1, 1, 2])))
                    if rng.random() < 0.7 else rng.randint(1, vmax)
                )
                if V[i][g] == old:
                    continue
                cand = count_capped(n, m, V, cur)
                if cand <= cur:  # accept ties: drift along plateaus
                    cur = cand
                    if cur == 0:
                        print(f"*** WITNESS *** {json.dumps(V)}", flush=True)
                        elite_f.write(json.dumps(
                            {"count": 0, "n": n, "m": m, "values": V}) + "\n")
                        elite_f.flush()
                        return
                else:
                    V[i][g] = old
            if cur <= elite:
                elite_f.write(json.dumps(
                    {"count": cur, "n": n, "m": m, "values": [row[:] for row in V],
                     "restart": r}) + "\n")
                elite_f.flush()
            if best_global is None or cur < best_global:
                best_global = cur
                print(f"restart {r}: new best count={cur} "
                      f"({time.time()-t0:.0f}s) V={json.dumps(V)}", flush=True)
    print(f"done: best EFX0 count found = {best_global} over {restarts} restarts", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--m", type=int, default=8)
    ap.add_argument("--vmax", type=int, default=20)
    ap.add_argument("--restarts", type=int, default=40)
    ap.add_argument("--iters", type=int, default=1500)
    ap.add_argument("--elite", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", type=str, default="results/boundary_elites.jsonl")
    a = ap.parse_args()
    run(a.n, a.m, a.vmax, a.restarts, a.iters, a.elite, a.seed, a.out)
