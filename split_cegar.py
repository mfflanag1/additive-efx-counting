"""Double-pool CEGAR: exists V at (4,7), values<=K, with NO envy-free 3111 base AND
at most 5 EFX0 allocations? UNSAT => bounded proof of theory3's split: no-base => count>=6.
Pool A: envy-free-base candidates (each must be envy-broken). Pool B: allocations
(each killed or matched to one of 5 slots)."""
import json, time
from ortools.sat.python import cp_model
from cegar import add_lex_ge
from verify import enumerate_all
from base_cegar import envy_free_3111_bases

N, M, K = 4, 7, 6
poolA, poolB = [], []
try:
    d = json.load(open("results/split_pools.json"))
    poolA = [(f, {int(k): v for k, v in b.items()}) for f, b in d["A"]]
    poolB = d["B"]
    print(f"resumed A={len(poolA)} B={len(poolB)}", flush=True)
except Exception:
    pass
t0 = time.time(); it = 0
while True:
    it += 1
    md = cp_model.CpModel()
    v = [[md.NewIntVar(1, K, "") for g in range(M)] for i in range(N)]
    for i in range(N-1): add_lex_ge(md, v[i], v[i+1])
    for g in range(M-1): add_lex_ge(md, [v[i][g] for i in range(N)], [v[i][g+1] for i in range(N)])
    for f, bundles in poolA:
        lits = []
        for i in range(N):
            for j in range(N):
                if i == j: continue
                b = md.NewBoolVar("")
                md.Add(sum(v[i][g] for g in bundles[j]) >= sum(v[i][g] for g in bundles[i]) + 1).OnlyEnforceIf(b)
                lits.append(b)
        md.AddBoolOr(lits)
    slots = [[md.NewIntVar(0, N-1, "") for g in range(M)] for t in range(5)]
    for assign in poolB:
        bundles = [[] for _ in range(N)]
        for g, a in enumerate(assign): bundles[a].append(g)
        lits = []
        for g, j in enumerate(assign):
            for i in range(N):
                if i == j: continue
                b = md.NewBoolVar("")
                md.Add(sum(v[i][h] for h in bundles[i]) + v[i][g] + 1 <= sum(v[i][h] for h in bundles[j])).OnlyEnforceIf(b)
                lits.append(b)
        for t in range(5):
            eq = md.NewBoolVar("")
            for g, a in enumerate(assign): md.Add(slots[t][g] == a).OnlyEnforceIf(eq)
            lits.append(eq)
        md.AddBoolOr(lits)
    s = cp_model.CpSolver(); s.parameters.num_search_workers = 4
    s.parameters.max_time_in_seconds = 3600
    st = s.Solve(md)
    el = time.time()-t0
    if st == cp_model.INFEASIBLE:
        print(f"SPLIT-UNSAT after {it} iters A={len(poolA)} B={len(poolB)} {el:.0f}s => THEOREM: every (4,7) no-base instance with values<={K} has >=6 EFX0 allocations", flush=True)
        json.dump({"status":"UNSAT","K":K,"iters":it}, open("results/split_cegar.json","w")); break
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f"STALL iter {it} A={len(poolA)} B={len(poolB)}", flush=True)
        json.dump({"status":"STALL","iters":it}, open("results/split_cegar.json","w")); break
    V = [[s.Value(v[i][g]) for g in range(M)] for i in range(N)]
    bases = envy_free_3111_bases(V, cap=3)
    if bases:
        poolA.extend(bases)
        if it % 10 == 0:
            json.dump({"A": poolA, "B": poolB}, open("results/split_pools.json", "w"))
        continue
    res = enumerate_all(N, M, V, collect=8)
    if res["efx0_count"] <= 5:
        print(f"*** SPLIT COUNTEREXAMPLE: no-base with count={res['efx0_count']} *** {json.dumps(V)}", flush=True)
        json.dump({"status":"WITNESS","count":res["efx0_count"],"values":V}, open("results/split_cegar.json","w")); break
    poolB.extend(res["examples_efx0"][:6])
    json.dump({"A": poolA, "B": poolB}, open("results/split_pools.json", "w"))
    if it % 25 == 0: print(f"iter {it} A={len(poolA)} B={len(poolB)} {el:.0f}s", flush=True)
