"""(5,9) K=3 completion v2 (referee-corrected): the FOUR-TYPE case.
v1 of this script forced the duplicated type lex-max (UNSOUND, superseded); this version
constrains only singleton-row order.
Sound encoding: any 4-type 5-agent profile has exactly one duplicated row; WLOG
(agent relabeling) agents 0,1 share it. Force v[0]==v[1]; rows 1..4 pairwise distinct;
lex-nonincreasing chain on the SINGLETON rows 2..4 only (the duplicated type's rank is not
relabelable, so no order constraint touches it); no column symmetry-breaking (the Flener
joint canonical form is not guaranteed under this constrained row order). UNSAT here + the 5-distinct-type UNSAT + the <=3-types theorem (2410.13580)
jointly give: no counterexample at n=5, m=9, values {1..3}.
"""
import json, time
from ortools.sat.python import cp_model
from cegar import add_lex_ge, find_efx0

N, M, LO, K = 5, 9, 1, 3
pool = []
try:
    pool = json.load(open("results/pool_n5m9K3_4type_v2.json")); print(f"resumed {len(pool)}", flush=True)
except Exception: pass
t0 = time.time(); it = 0
while True:
    it += 1
    md = cp_model.CpModel()
    v = [[md.NewIntVar(LO, K, "") for g in range(M)] for i in range(N)]
    for g in range(M):
        md.Add(v[0][g] == v[1][g])
    for i in range(1, N):
        for j in range(i + 1, N):
            nes = []
            for g in range(M):
                b = md.NewBoolVar("")
                md.Add(v[i][g] != v[j][g]).OnlyEnforceIf(b)
                md.Add(v[i][g] == v[j][g]).OnlyEnforceIf(b.Not())
                nes.append(b)
            md.AddBoolOr(nes)
    # SOUND ordering (referee round 2): the duplicated TYPE is not relabelable, so no
    # order constraint between the duplicate row and singletons. Only the three singleton
    # agents 2,3,4 are freely relabelable -> sort those rows. Column lex dropped: the
    # Flener double-lex canonical form is not guaranteed under this constrained row order.
    for i in range(2, N - 1):
        add_lex_ge(md, v[i], v[i + 1])
    for assign in pool:
        bundles = [[] for _ in range(N)]
        for g, a in enumerate(assign): bundles[a].append(g)
        lits = []
        for g, j in enumerate(assign):
            for i in range(N):
                if i == j: continue
                b = md.NewBoolVar("")
                md.Add(sum(v[i][h] for h in bundles[i]) + v[i][g] + 1
                       <= sum(v[i][h] for h in bundles[j])).OnlyEnforceIf(b)
                lits.append(b)
        md.AddBoolOr(lits)
    s = cp_model.CpSolver(); s.parameters.num_search_workers = 8
    s.parameters.max_time_in_seconds = 7200
    st = s.Solve(md)
    el = time.time() - t0
    if st == cp_model.INFEASIBLE:
        print(f"FOUR-TYPE UNSAT after {it} iters pool={len(pool)} {el:.0f}s => (5,9) K=3 theorem COMPLETE", flush=True)
        json.dump({"status": "UNSAT", "iters": it, "pool": len(pool)}, open("results/n5m9K3_4type_v2.json", "w")); break
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f"STALL iter {it} pool={len(pool)}", flush=True)
        json.dump({"status": "STALL", "iters": it, "pool": len(pool)}, open("results/n5m9K3_4type_v2.json", "w")); break
    V = [[s.Value(v[i][g]) for g in range(M)] for i in range(N)]
    efx = find_efx0(N, M, V, 5)
    if not efx:
        print(f"*** WITNESS CANDIDATE *** {json.dumps(V)}", flush=True)
        json.dump({"status": "WITNESS", "values": V}, open("results/n5m9K3_4type_v2.json", "w")); break
    pool.extend(efx)
    if it % 10 == 0: json.dump(pool, open("results/pool_n5m9K3_4type_v2.json", "w"))
    if it % 25 == 0: print(f"iter {it} pool={len(pool)} {el:.0f}s", flush=True)
