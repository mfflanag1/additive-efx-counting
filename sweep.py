"""Phase-diagram sweep (theory1 §7): rho x beta grid across misalignment patterns.
Each cell = pool-CEGAR with per-solve cap; verdict UNSAT / WITNESS / STALL per cell.
Cell order: most probative first (V-template, then gap-closing strip upward).
Results appended to results/sweep_results.jsonl as they land.
"""
import json
import time

from ortools.sat.python import cp_model

from cegar import find_efx0

N, M = 4, 8


def sig_cell(beta, inter=True):
    """Signature pattern: private goods 0-3, contested 4(,5), tails; beta = tail cap.
    inter: good 5 becomes the intermediate shared good [10,35] (the V role)."""
    B = [[None] * M for _ in range(N)]
    for i in range(N):
        for g in range(M):
            if g < 4:
                B[i][g] = (45, 65) if g == i else (1, 20)
            elif g == 4:
                B[i][g] = (40, 60)
            elif g == 5:
                B[i][g] = (10, 35) if inter else (40, 60)
            else:
                B[i][g] = (1, beta)
    return B


def aligned_cell(beta, p=3):
    B = [[None] * M for _ in range(N)]
    for i in range(N):
        for g in range(M):
            B[i][g] = (40, 60) if g < p else (1, beta)
    return B


CELLS = [
    ("Vtemplate_sig_inter_b8", sig_cell(8, inter=True)),
    ("Vtemplate_sig_inter_b20", sig_cell(20, inter=True)),
    ("Vtemplate_sig_inter_b35", sig_cell(35, inter=True)),
    ("sig_nointer_b20", sig_cell(20, inter=False)),
    ("sig_nointer_b35", sig_cell(35, inter=False)),
    ("sig_gapclose_b45", sig_cell(45, inter=True)),
    ("aligned_p3_b25", aligned_cell(25)),
    ("aligned_p3_b38", aligned_cell(38)),   # beta ~ peak_lo: THE gap-closing strip
    ("aligned_p4_b38", aligned_cell(38, p=4)),
    ("aligned_p2_b38", aligned_cell(38, p=2)),
]


def run_cell(name, B):
    pool = []
    t0 = time.time()
    it = 0
    while True:
        it += 1
        md = cp_model.CpModel()
        v = [[md.NewIntVar(B[i][g][0], B[i][g][1], "") for g in range(M)]
             for i in range(N)]
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
        md.Add(sum(doms) <= 1)  # NC-A (proven necessary)
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
        s.parameters.num_search_workers = 3
        s.parameters.max_time_in_seconds = 300
        st = s.Solve(md)
        if st == cp_model.INFEASIBLE:
            return {"cell": name, "status": "UNSAT", "iters": it,
                    "pool": len(pool), "seconds": round(time.time() - t0)}
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return {"cell": name, "status": "STALL", "iters": it,
                    "pool": len(pool), "seconds": round(time.time() - t0)}
        V = [[s.Value(v[i][g]) for g in range(M)] for i in range(N)]
        efx = find_efx0(N, M, V, 5)
        if not efx:
            return {"cell": name, "status": "WITNESS", "values": V}
        pool.extend(efx)


with open("results/sweep_results.jsonl", "a") as out:
    for name, B in CELLS:
        r = run_cell(name, B)
        out.write(json.dumps(r) + "\n")
        out.flush()
        print(json.dumps(r), flush=True)
        if r["status"] == "WITNESS":
            print("STOPPING SWEEP — WITNESS FOUND", flush=True)
            break
print("SWEEP DONE", flush=True)
