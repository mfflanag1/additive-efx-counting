"""CEGAR on theory1 residual: spread-ratio peaks family (theory1 §5 window):
all agents concentrated on the same peak set P={0,1,2}, flat tails; plus NC-A
(proven necessary: at most one agent has a good worth >= half its total).
Witness-hunt mode: family restriction is heuristic; a family-UNSAT is a family no-go.
Pool is persisted to results/peaks_pool.json for restarts.
"""
import json
import time

from ortools.sat.python import cp_model

from cegar import find_efx0

N, M = 4, 8
PEAKS = [0, 1, 2]
PEAK_MIN, TAIL_MAX, VMAX = 12, 12, 50
RATIO_BANDS = [(12, 20), (20, 30), (30, 40), (40, 50)]  # straddle ladder boundaries 2,3,4
TAIL_MIN = 8


def master(pool):
    model = cp_model.CpModel()
    v = [[model.NewIntVar(RATIO_BANDS[i][0] if g in PEAKS else TAIL_MIN,
                          RATIO_BANDS[i][1] if g in PEAKS else TAIL_MAX, "")
          for g in range(M)] for i in range(N)]
    # NC-A: at most one agent with a dominant good (2*v >= row total)
    doms = []
    for i in range(N):
        tot = sum(v[i])
        gd = []
        for g in range(M):
            b = model.NewBoolVar("")
            model.Add(2 * v[i][g] >= tot).OnlyEnforceIf(b)
            model.Add(2 * v[i][g] < tot).OnlyEnforceIf(b.Not())
            gd.append(b)
        d = model.NewBoolVar("")
        model.AddMaxEquality(d, gd)
        doms.append(d)
    model.Add(sum(doms) <= 1)
    for assign in pool:
        bundles = [[] for _ in range(N)]
        for g, a in enumerate(assign):
            bundles[a].append(g)
        lits = []
        for g, j in enumerate(assign):
            for i in range(N):
                if i == j:
                    continue
                b = model.NewBoolVar("")
                model.Add(sum(v[i][h] for h in bundles[i]) + v[i][g] + 1
                          <= sum(v[i][h] for h in bundles[j])).OnlyEnforceIf(b)
                lits.append(b)
        model.AddBoolOr(lits)
    return model, v


pool = []
t0 = time.time()
it = 0
while True:
    it += 1
    model, v = master(pool)
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = 4
    s.parameters.max_time_in_seconds = 900
    st = s.Solve(model)
    if st == cp_model.INFEASIBLE:
        print(f"SPREAD-FAMILY UNSAT after {it} iters, pool={len(pool)}, "
              f"{time.time()-t0:.0f}s", flush=True)
        json.dump({"status": "FAMILY_UNSAT", "iters": it, "pool": len(pool)},
                  open("results/spread_result.json", "w"))
        break
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("stall", flush=True)
        break
    V = [[s.Value(v[i][g]) for g in range(M)] for i in range(N)]
    efx = find_efx0(N, M, V, 5)
    if not efx:
        print(f"*** WITNESS CANDIDATE *** {json.dumps(V)}", flush=True)
        json.dump({"status": "WITNESS", "values": V},
                  open("results/spread_result.json", "w"))
        break
    pool.extend(efx)
    json.dump(pool, open("results/spread_pool.json", "w"))
    if it % 20 == 0:
        print(f"iter {it} pool={len(pool)} {time.time()-t0:.0f}s", flush=True)
