"""Anatomy CEGAR: master encodes the PROVEN witness skeleton (theory1, Lemma 1' +
floater analysis + almost-full theorem):

Any (4,8) witness, after permuting goods so the almost-full leftover good is column 7,
admits: a base allocation of goods 0..6 into 4 nonempty bundles that is EFX0, such that
parking good 7 in ANY bundle creates strong envy; and (pool CEGAR) no other complete
allocation is EFX0.

Master variables: V in [1,VMAX]^{4x8} AND the base assignment a_g in {0..3}.
SAT + slave check (0 EFX0 overall) -> witness. UNSAT (after pool convergence) ->
no witness with values <= VMAX at (4,8). Conditional on VMAX only.
"""
import json
import time

from ortools.sat.python import cp_model

from cegar import find_efx0

N, M, F, VMAX, BIG = 4, 8, 7, 120, 10 ** 6
BASE = [g for g in range(M) if g != F]


def build(pool):
    md = cp_model.CpModel()
    v = [[md.NewIntVar(1, VMAX, f"v{i}{g}") for g in range(M)] for i in range(N)]
    x = [[md.NewBoolVar(f"x{g}{j}") for j in range(N)] for g in BASE]  # good g -> bundle j
    for gi, g in enumerate(BASE):
        md.AddExactlyOne(x[gi])
    for j in range(N):
        md.Add(sum(x[gi][j] for gi in range(len(BASE))) >= 1)  # nonempty bundles

    # bv[i][j] = v_i(B_j); term t = x ? v : 0
    bv = [[md.NewIntVar(0, VMAX * 7, "") for j in range(N)] for i in range(N)]
    for i in range(N):
        for j in range(N):
            terms = []
            for gi, g in enumerate(BASE):
                t = md.NewIntVar(0, VMAX, "")
                md.Add(t == v[i][g]).OnlyEnforceIf(x[gi][j])
                md.Add(t == 0).OnlyEnforceIf(x[gi][j].Not())
                terms.append(t)
            md.Add(bv[i][j] == sum(terms))

    # mn[i][j] = min value (under i) of goods in B_j
    mn = [[md.NewIntVar(1, BIG, "") for j in range(N)] for i in range(N)]
    for i in range(N):
        for j in range(N):
            terms = []
            for gi, g in enumerate(BASE):
                t = md.NewIntVar(1, BIG, "")
                md.Add(t == v[i][g]).OnlyEnforceIf(x[gi][j])
                md.Add(t == BIG).OnlyEnforceIf(x[gi][j].Not())
                terms.append(t)
            md.AddMinEquality(mn[i][j], terms)

    # base EFX0: v_i(B_i) >= bv[i][j] - mn[i][j]  (mn<=BIG handles nonempty by constr)
    for i in range(N):
        for j in range(N):
            if i != j:
                md.Add(bv[i][i] >= bv[i][j] - mn[i][j])

    # parking good F in B_j fails for every j: exists observer k != j with
    # bv[k][k] < bv[k][j] + v[k][F] - min(mn[k][j], v[k][F])
    for j in range(N):
        lits = []
        for k in range(N):
            if k == j:
                continue
            mm = md.NewIntVar(1, BIG, "")
            md.AddMinEquality(mm, [mn[k][j], v[k][F]])
            b = md.NewBoolVar("")
            md.Add(bv[k][k] + 1 <= bv[k][j] + v[k][F] - mm).OnlyEnforceIf(b)
            lits.append(b)
        md.AddBoolOr(lits)

    # pool: every known complete allocation must fail EFX0
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
    pool = json.load(open("results/anatomy_pool.json"))
    print(f"resumed pool {len(pool)}", flush=True)
except Exception:
    pass
t0 = time.time()
it = 0
while True:
    it += 1
    md, v = build(pool)
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = 10
    s.parameters.max_time_in_seconds = 1800
    st = s.Solve(md)
    if st == cp_model.INFEASIBLE:
        print(f"ANATOMY UNSAT after {it} iters, pool={len(pool)}, "
              f"{time.time()-t0:.0f}s => no (4,8) witness with values<={VMAX}", flush=True)
        json.dump({"status": "UNSAT", "vmax": VMAX, "iters": it, "pool": len(pool)},
                  open("results/anatomy_result.json", "w"))
        break
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f"stall/timeout at iter {it}, pool={len(pool)}", flush=True)
        json.dump({"status": "STALL", "iters": it, "pool": len(pool)},
                  open("results/anatomy_result.json", "w"))
        break
    V = [[s.Value(v[i][g]) for g in range(M)] for i in range(N)]
    efx = find_efx0(N, M, V, 15)
    if not efx:
        print(f"*** WITNESS CANDIDATE *** {json.dumps(V)}", flush=True)
        json.dump({"status": "WITNESS", "values": V},
                  open("results/anatomy_result.json", "w"))
        break
    pool.extend(efx)
    json.dump(pool, open("results/anatomy_pool.json", "w"))
    if it % 10 == 0:
        print(f"iter {it} pool={len(pool)} {time.time()-t0:.0f}s", flush=True)
