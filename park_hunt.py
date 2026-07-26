"""Parkability-guided CEGAR (4,8): plain CEGAR + proven necessary conditions:
NC-A (<=1 dominant agent), no global-min good (theory1 SOURCE_LEMMA correction:
a witness cannot have a good that is simultaneously every agent's minimum),
distinct rows + double-lex (as in cegar.py). Values [1,30]."""
import json, time
from ortools.sat.python import cp_model
from cegar import build_master, find_efx0

N, M, LO, K = 4, 8, 1, 30
pool = []
try:
    pool = json.load(open("results/park_pool.json")); print(f"resumed {len(pool)}", flush=True)
except Exception: pass
t0 = time.time(); it = 0
while True:
    it += 1
    model, v = build_master(N, M, LO, K, pool)
    # NC-A
    doms = []
    for i in range(N):
        tot = sum(v[i]); gd = []
        for g in range(M):
            b = model.NewBoolVar("")
            model.Add(2*v[i][g] >= tot).OnlyEnforceIf(b)
            model.Add(2*v[i][g] < tot).OnlyEnforceIf(b.Not())
            gd.append(b)
        d = model.NewBoolVar(""); model.AddMaxEquality(d, gd); doms.append(d)
    model.Add(sum(doms) <= 1)
    # no global-min good
    mns = []
    for i in range(N):
        mn = model.NewIntVar(LO, K, ""); model.AddMinEquality(mn, v[i]); mns.append(mn)
    for g in range(M):
        lits = []
        for i in range(N):
            b = model.NewBoolVar("")
            model.Add(v[i][g] >= mns[i] + 1).OnlyEnforceIf(b)
            lits.append(b)
        model.AddBoolOr(lits)
    s = cp_model.CpSolver(); s.parameters.num_search_workers = 6
    s.parameters.max_time_in_seconds = 3600
    st = s.Solve(model)
    el = time.time()-t0
    if st == cp_model.INFEASIBLE:
        print(f"PARK-HUNT UNSAT after {it} iters pool={len(pool)} {el:.0f}s => no witness values<=30 outside proven-safe conditions", flush=True)
        json.dump({"status":"UNSAT","K":K,"iters":it,"pool":len(pool)}, open("results/park_hunt.json","w")); break
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f"STALL iter {it} pool={len(pool)}", flush=True)
        json.dump({"status":"STALL","iters":it,"pool":len(pool)}, open("results/park_hunt.json","w")); break
    V = [[s.Value(v[i][g]) for g in range(M)] for i in range(N)]
    efx = find_efx0(N, M, V, 5)
    if not efx:
        print(f"*** WITNESS CANDIDATE *** {json.dumps(V)}", flush=True)
        json.dump({"status":"WITNESS","values":V}, open("results/park_hunt.json","w")); break
    pool.extend(efx)
    if it % 10 == 0: json.dump(pool, open("results/park_pool.json","w"))
    if it % 25 == 0: print(f"iter {it} pool={len(pool)} {el:.0f}s", flush=True)
