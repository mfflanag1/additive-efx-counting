"""Hunt a TIGHT (6,9) instance: exactly n=6 EFX0 allocations (third data point for the
m=n+3 tight family; would improve Neoh-Teh's minimum-count bound n!=720 -> 6 at (6,9)).

Master encodes the proven tight anatomy (theory3 TIGHT_FAMILY.md): base on goods 0..7 =
hub triple {0,1,2} owned by agent 0 + singletons goods 3..7 to agents 1..5; base fully
envy-free; good 8 = universal-min floater (parking then gives >= 6 EFX0 allocations,
rigorous). Pool: every discovered NON-parking EFX0 allocation must be strong-envy killed.
Slave: fast_verify exact count; count == 6 -> WITNESS (dual-verify externally).
Fixing the base layout is WLOG up to relabeling for the anatomy class; this is a witness
hunt, not an exclusion run.
"""
import json
import time

from ortools.sat.python import cp_model

from fast_verify import count_efx0
from verify import enumerate_all

N, M, F, VMAX = 6, 9, 8, 200
HUB = [0, 1, 2]
SINGLES = {1: 3, 2: 4, 3: 5, 4: 6, 5: 7}  # agent -> singleton good
BASE_BUNDLES = {0: HUB, **{a: [g] for a, g in SINGLES.items()}}
PARKINGS = []
for park_agent in range(N):
    assign = [0] * M
    for a, gs in BASE_BUNDLES.items():
        for g in gs:
            assign[g] = a
    assign[F] = park_agent
    PARKINGS.append(assign)


def build(pool):
    md = cp_model.CpModel()
    v = [[md.NewIntVar(1, VMAX, "") for g in range(M)] for i in range(N)]
    # floater universal-min
    for i in range(N):
        for g in range(M):
            if g != F:
                md.Add(v[i][F] <= v[i][g])
    # base fully envy-free: for every i, j != i: v_i(B_i) >= v_i(B_j)
    for i in range(N):
        for j in range(N):
            if i != j:
                md.Add(sum(v[i][g] for g in BASE_BUNDLES[i]) >=
                       sum(v[i][g] for g in BASE_BUNDLES[j]))
    # all-distinct values per row (theory3: symmetry-multiplicity must be broken)
    for i in range(N):
        md.AddAllDifferent(v[i])
    for assign in pool:
        bundles = [[] for _ in range(N)]
        for g, a in enumerate(assign):
            bundles[a].append(g)
        lits = []
        for g, j in enumerate(assign):
            for i in range(N):
                if i == j:
                    continue
                b = md.NewBoolVar("")
                md.Add(sum(v[i][h] for h in bundles[i]) + v[i][g] + 1
                       <= sum(v[i][h] for h in bundles[j])).OnlyEnforceIf(b)
                lits.append(b)
        md.AddBoolOr(lits)
    return md, v


pool = []
try:
    pool = json.load(open("results/tight69_pool.json"))
    print(f"resumed {len(pool)}", flush=True)
except Exception:
    pass
t0 = time.time()
it = 0
while True:
    it += 1
    md, v = build(pool)
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = 8
    s.parameters.max_time_in_seconds = 3600
    st = s.Solve(md)
    el = time.time() - t0
    if st == cp_model.INFEASIBLE:
        print(f"ANATOMY-UNSAT after {it} iters pool={len(pool)} {el:.0f}s "
              f"(no tight (6,9) instance in this anatomy at VMAX={VMAX})", flush=True)
        json.dump({"status": "UNSAT", "iters": it, "pool": len(pool)},
                  open("results/tight69_result.json", "w"))
        break
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f"STALL iter {it} pool={len(pool)}", flush=True)
        json.dump({"status": "STALL", "iters": it, "pool": len(pool)},
                  open("results/tight69_result.json", "w"))
        break
    V = [[s.Value(v[i][g]) for g in range(M)] for i in range(N)]
    cnt, _ = count_efx0(V, cap=None)
    if cnt == N:
        print(f"*** TIGHT (6,9) WITNESS: count=6 *** {json.dumps(V)}", flush=True)
        json.dump({"status": "WITNESS", "count": cnt, "values": V},
                  open("results/tight69_result.json", "w"))
        break
    # pool the non-parking EFX0 allocations (pure-python collector, capped)
    res = enumerate_all(N, M, V, collect=40)
    extras = [a for a in res["examples_efx0"] if a not in PARKINGS][:6]
    if not extras:
        # parkings dominate the first examples; collect more
        res = enumerate_all(N, M, V, collect=200)
        extras = [a for a in res["examples_efx0"] if a not in PARKINGS][:6]
    assert extras, f"count={cnt} but no non-parking allocation found?!"
    pool.extend(extras)
    json.dump(pool, open("results/tight69_pool.json", "w"))
    if it % 5 == 0:
        print(f"iter {it} pool={len(pool)} count={cnt} {el:.0f}s", flush=True)
