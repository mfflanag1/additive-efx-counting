"""G1-G3 family CEGARs (theory1 PEAKS_WINDOW §5): the misaligned/bumpy cells that the
flat-tail ladder does NOT cover. Per-cell integer bounds + optional distinct-argmax.
Each family: pool-CEGAR until UNSAT (family no-go at these bands) or witness.
"""
import json
import time

from ortools.sat.python import cp_model

from cegar import find_efx0

N, M = 4, 8

# bounds[i][g] = (lo, hi)
def bands(spec):
    return [[spec(i, g) for g in range(M)] for i in range(N)]

FAMILIES = {
    # G1: private signature good s_i=i (45-65 own, 1-20 others), contested 4,5 (40-60),
    # flat tails 6,7 (1-8)
    "G1_misaligned": bands(lambda i, g:
        (45, 65) if g == i else
        (1, 20) if g < 4 else
        (40, 60) if g in (4, 5) else (1, 8)),
    # G2: shared peaks 0-2 (20-45), BUMPY tails 3-7 (1-20)
    "G2_bumpy": bands(lambda i, g: (20, 45) if g < 3 else (1, 20)),
    # G3a: p=4 contested 0-3 (25-60) with distinct argmax (extra constraints), tails 1-6
    "G3a_p4": bands(lambda i, g: (25, 60) if g < 4 else (1, 6)),
    # G3b: p=2 peaks 0,1 (40-60), elevated block 2-4 (15-25), tails 5-7 (1-8)
    "G3b_p2block": bands(lambda i, g:
        (40, 60) if g < 2 else (15, 25) if g < 5 else (1, 8)),
}


def run_family(name, B, extra_argmax=False):
    pool = []
    t0 = time.time()
    it = 0
    while True:
        it += 1
        md = cp_model.CpModel()
        v = [[md.NewIntVar(B[i][g][0], B[i][g][1], "") for g in range(M)]
             for i in range(N)]
        # NC-A: at most one dominant agent
        doms = []
        for i in range(N):
            tot = sum(v[i])
            gd = []
            for g in range(M):
                b = md.NewBoolVar("")
                md.Add(2 * v[i][g] >= tot).OnlyEnforceIf(b)
                md.Add(2 * v[i][g] < tot).OnlyEnforceIf(b.Not())
                gd.append(b)
            d = md.NewBoolVar("")
            md.AddMaxEquality(d, gd)
            doms.append(d)
        md.Add(sum(doms) <= 1)
        if extra_argmax:  # G3a: agent i's top contested good is good i
            for i in range(N):
                for g in range(4):
                    if g != i:
                        md.Add(v[i][i] >= v[i][g] + 1)
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
        s.parameters.max_time_in_seconds = 1200
        st = s.Solve(md)
        if st == cp_model.INFEASIBLE:
            print(f"[{name}] UNSAT after {it} iters, pool={len(pool)}, "
                  f"{time.time()-t0:.0f}s", flush=True)
            return {"family": name, "status": "UNSAT", "iters": it, "pool": len(pool)}
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print(f"[{name}] STALL at iter {it}", flush=True)
            return {"family": name, "status": "STALL", "iters": it, "pool": len(pool)}
        V = [[s.Value(v[i][g]) for g in range(M)] for i in range(N)]
        efx = find_efx0(N, M, V, 5)
        if not efx:
            print(f"[{name}] *** WITNESS CANDIDATE *** {json.dumps(V)}", flush=True)
            return {"family": name, "status": "WITNESS", "values": V}
        pool.extend(efx)
        if it % 50 == 0:
            print(f"[{name}] iter {it} pool={len(pool)} {time.time()-t0:.0f}s",
                  flush=True)


results = []
for name, B in FAMILIES.items():
    results.append(run_family(name, B, extra_argmax=(name == "G3a_p4")))
    json.dump(results, open("results/families_results.json", "w"), indent=1)
print("ALL FAMILIES DONE", flush=True)
