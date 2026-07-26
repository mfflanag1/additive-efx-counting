"""Local exact finisher: CEGAR restricted to an L-inf box around a seed instance.
No symmetry/type cuts (not needed for witness hunting; any hit is verified directly).
Box-UNSAT => no witness within delta of seed (local no-go; escalate delta).
"""
import argparse
import json
import time

from ortools.sat.python import cp_model

from cegar import find_efx0


def run(seed_values, delta, vmax, add_per_iter, out_path, free_col=None):
    n, m = len(seed_values), len(seed_values[0])
    pool = find_efx0(n, m, seed_values, 10 ** 9)  # all current survivors
    print(f"seed survivors: {len(pool)}; box delta={delta}", flush=True)
    t0 = time.time()
    it = 0
    while True:
        it += 1
        model = cp_model.CpModel()
        v = [[model.NewIntVar(1, vmax, f"v{i}{g}") if g == free_col else
              model.NewIntVar(max(1, seed_values[i][g] - delta),
                              min(vmax, seed_values[i][g] + delta), f"v{i}{g}")
              for g in range(m)] for i in range(n)]
        for assign in pool:
            bundles = [[] for _ in range(n)]
            for g, a in enumerate(assign):
                bundles[a].append(g)
            lits = []
            for g, j in enumerate(assign):
                for i in range(n):
                    if i == j:
                        continue
                    b = model.NewBoolVar("")
                    model.Add(sum(v[i][h] for h in bundles[i]) + v[i][g] + 1
                              <= sum(v[i][h] for h in bundles[j])).OnlyEnforceIf(b)
                    lits.append(b)
            model.AddBoolOr(lits)
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 4
        solver.parameters.max_time_in_seconds = 600
        st = solver.Solve(model)
        el = time.time() - t0
        if st == cp_model.INFEASIBLE:
            print(f"BOX-UNSAT after {it} iters, pool={len(pool)}, {el:.1f}s: "
                  f"no witness within delta={delta} of seed", flush=True)
            res = {"status": "BOX_UNSAT", "delta": delta, "iterations": it,
                   "pool": len(pool), "seconds": round(el, 1)}
            break
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print("solver stalled", flush=True)
            res = {"status": "STALL", "delta": delta, "iterations": it}
            break
        values = [[solver.Value(v[i][g]) for g in range(m)] for i in range(n)]
        efx = find_efx0(n, m, values, add_per_iter)
        if not efx:
            print(f"*** WITNESS CANDIDATE *** iter {it} {json.dumps(values)}", flush=True)
            res = {"status": "WITNESS", "delta": delta, "iterations": it,
                   "values": values, "seconds": round(el, 1)}
            break
        pool.extend(efx)
        if it % 20 == 0:
            print(f"iter {it}, pool={len(pool)}, {el:.1f}s", flush=True)
    with open(out_path, "w") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed-file", type=str, required=True)
    ap.add_argument("--delta", type=int, default=6)
    ap.add_argument("--vmax", type=int, default=150)
    ap.add_argument("--add", type=int, default=5)
    ap.add_argument("--out", type=str, required=True)
    ap.add_argument("--free-col", type=int, default=None)
    a = ap.parse_args()
    seed = json.load(open(a.seed_file))
    run(seed["values"], a.delta, a.vmax, a.add, a.out, a.free_col)
