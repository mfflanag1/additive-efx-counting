"""Misaligned two-treasure corridor CEGAR (theory1 PER_K endgame pointer):
treasures for agents 0,1 on goods 0,1 (high for holder, low-mid for others),
six NON-FLAT tails, plus ALL proven witness-necessary conditions:
 - NC-A (at most one agent with a good >= half its row total)
 - NO DOMINANT GOOD (Peeling Theorem): for every i,t: 2*v_i(t) + min_{g!=t} v_i(g) < T_i
 - no universal-min good
Pool CEGAR; pool persisted. UNSAT = corridor no-go at these bands; SAT+0-EFX = witness.
"""
import json
import time

from ortools.sat.python import cp_model

from cegar import find_efx0

N, M = 4, 8


def bounds(i, g):
    if g == 0:
        return (30, 70) if i == 0 else (1, 25)
    if g == 1:
        return (30, 70) if i == 1 else (1, 25)
    return (1, 30)  # non-flat tails allowed


pool = []
try:
    pool = json.load(open("results/corridor_pool.json"))
    print(f"resumed {len(pool)}", flush=True)
except Exception:
    pass
t0 = time.time()
it = 0
while True:
    it += 1
    md = cp_model.CpModel()
    v = [[md.NewIntVar(*bounds(i, g), "") for g in range(M)] for i in range(N)]
    for i in range(N):
        tot = sum(v[i])
        # no dominant good: 2*v_i(t) + min_{g!=t} v_i(g) + 1 <= T_i  for all t
        for t in range(M):
            m2 = md.NewIntVar(1, 70, "")
            md.AddMinEquality(m2, [v[i][g] for g in range(M) if g != t])
            md.Add(2 * v[i][t] + m2 + 1 <= tot)
        # NC-A is implied by no-dominant-good (dominance in the M-residual sense is
        # weaker than half-total dominance), so no separate constraint needed.
    # no universal-min good
    mns = []
    for i in range(N):
        mn = md.NewIntVar(1, 70, "")
        md.AddMinEquality(mn, v[i])
        mns.append(mn)
    for g in range(M):
        lits = []
        for i in range(N):
            b = md.NewBoolVar("")
            md.Add(v[i][g] >= mns[i] + 1).OnlyEnforceIf(b)
            lits.append(b)
        md.AddBoolOr(lits)
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
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = 4
    s.parameters.max_time_in_seconds = 1800
    st = s.Solve(md)
    el = time.time() - t0
    if st == cp_model.INFEASIBLE:
        print(f"CORRIDOR UNSAT after {it} iters pool={len(pool)} {el:.0f}s", flush=True)
        json.dump({"status": "UNSAT", "iters": it, "pool": len(pool)},
                  open("results/corridor_result.json", "w"))
        break
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f"STALL iter {it} pool={len(pool)}", flush=True)
        json.dump({"status": "STALL", "iters": it, "pool": len(pool)},
                  open("results/corridor_result.json", "w"))
        break
    V = [[s.Value(v[i][g]) for g in range(M)] for i in range(N)]
    efx = find_efx0(N, M, V, 5)
    if not efx:
        print(f"*** WITNESS CANDIDATE *** {json.dumps(V)}", flush=True)
        json.dump({"status": "WITNESS", "values": V},
                  open("results/corridor_result.json", "w"))
        break
    pool.extend(efx)
    if it % 10 == 0:
        json.dump(pool, open("results/corridor_pool.json", "w"))
    if it % 25 == 0:
        print(f"iter {it} pool={len(pool)} {el:.0f}s", flush=True)
