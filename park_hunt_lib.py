"""CEGAR hunt for an additive-goods EFX counterexample.

Master (CP-SAT): find integer valuations V (n x m, values in [lo, K]) such that every
allocation in the current pool S is NOT EFX0. Slave (exact verifier): enumerate EFX0
allocations of V; if none exist -> WITNESS; else add up to --add of them to S and repeat.
Master infeasible -> THEOREM: no counterexample at (n, m, values in [lo, K]).

With lo >= 1 (all-positive values) EFX0 and EFX+ coincide, so results apply to both.

Soundness of search-space cuts (valid vs. the open problem, cited in LEDGER.md):
 - rows pairwise distinct  (<=3 valuation types proven EFX-safe; n=4 needs 4 types)
 - double-lex order on rows and columns (row/col permutation symmetry; Flener et al.:
   every matrix has a representative with both row- and column-lex order)
"""
import argparse
import json
import time

from ortools.sat.python import cp_model

from verify import check_allocation, masks_from_assign, precompute


def add_lex_ge(model, xs, ys):
    """Lexicographic xs >= ys via prefix-equality booleans."""
    k = len(xs)
    eq = []  # eq[t] true => xs[:t+1] == ys[:t+1]
    for t in range(k):
        b = model.NewBoolVar("")
        model.Add(xs[t] == ys[t]).OnlyEnforceIf(b)
        model.Add(xs[t] != ys[t]).OnlyEnforceIf(b.Not())
        eq.append(b)
    # xs[0] >= ys[0]
    model.Add(xs[0] >= ys[0])
    for t in range(1, k):
        pre = eq[:t]
        model.Add(xs[t] >= ys[t]).OnlyEnforceIf(pre)


def build_master(n, m, lo, K, pool):
    return _build_master_ext(n, m, lo, K, pool)


def _build_master_ext(n, m, lo, K, pool):
    model = cp_model.CpModel()
    v = [[model.NewIntVar(lo, K, f"v{i}_{g}") for g in range(m)] for i in range(n)]

    # 4 distinct valuation types (sound: <=3 types proven safe)
    for i in range(n):
        for j in range(i + 1, n):
            nes = []
            for g in range(m):
                b = model.NewBoolVar("")
                model.Add(v[i][g] != v[j][g]).OnlyEnforceIf(b)
                model.Add(v[i][g] == v[j][g]).OnlyEnforceIf(b.Not())
                nes.append(b)
            model.AddBoolOr(nes)

    # double-lex symmetry breaking
    for i in range(n - 1):
        add_lex_ge(model, v[i], v[i + 1])
    for g in range(m - 1):
        add_lex_ge(model, [v[i][g] for i in range(n)], [v[i][g + 1] for i in range(n)])

    # kill constraints: every pooled allocation must fail EFX0
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
                # violation witness: v_i(X_i) + v_i(g) + 1 <= v_i(X_j)
                model.Add(
                    sum(v[i][h] for h in bundles[i]) + v[i][g] + 1
                    <= sum(v[i][h] for h in bundles[j])
                ).OnlyEnforceIf(b)
                lits.append(b)
        model.AddBoolOr(lits)
    return model, v


def find_efx0(n, m, values, k):
    """Return up to k EFX0 allocations (as assign lists), early-stopping."""
    val, minall, minpos = precompute(n, m, values)
    found = []
    assign = [0] * m
    while True:
        bundles = masks_from_assign(n, assign)
        e0, _ = check_allocation(n, bundles, val, minall, minpos)
        if e0:
            found.append(list(assign))
            if len(found) >= k:
                return found
        g = 0
        while g < m:
            assign[g] += 1
            if assign[g] < n:
                break
            assign[g] = 0
            g += 1
        else:
            return found


def run(n, m, lo, K, add_per_iter, time_limit, out_path, telemetry_path=None,
        pool_path=None):
    pool = []
    if pool_path:
        try:
            pool = json.load(open(pool_path))
            print(f"resumed pool {len(pool)}", flush=True)
        except Exception:
            pass
    t_start = time.time()
    it = 0
    while True:
        it += 1
        model, v = build_master(n, m, lo, K, pool)
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit
        solver.parameters.num_search_workers = 8
        status = solver.Solve(model)
        elapsed = time.time() - t_start
        if status == cp_model.INFEASIBLE:
            result = {"status": "UNSAT", "n": n, "m": m, "lo": lo, "K": K,
                      "iterations": it, "pool_size": len(pool), "seconds": round(elapsed, 1)}
            print(f"[K={K}] UNSAT after {it} iters, pool={len(pool)}, {elapsed:.1f}s "
                  f"=> THEOREM: no counterexample with n={n}, m={m}, values in [{lo},{K}]")
            break
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            result = {"status": "TIMEOUT", "n": n, "m": m, "lo": lo, "K": K,
                      "iterations": it, "pool_size": len(pool), "seconds": round(elapsed, 1)}
            print(f"[K={K}] master TIMEOUT at iter {it}, pool={len(pool)}")
            break
        values = [[solver.Value(v[i][g]) for g in range(m)] for i in range(n)]
        efx = find_efx0(n, m, values, add_per_iter)
        if telemetry_path:
            with open(telemetry_path, "a") as tf:
                tf.write(json.dumps({"iter": it, "n": n, "m": m,
                                     "values": values,
                                     "efx0_found_capped": len(efx)}) + "\n")
        if not efx:
            result = {"status": "WITNESS", "n": n, "m": m, "lo": lo, "K": K,
                      "iterations": it, "pool_size": len(pool), "seconds": round(elapsed, 1),
                      "values": values}
            print(f"[K={K}] *** WITNESS CANDIDATE at iter {it} *** {values}")
            break
        pool.extend(efx)
        if pool_path and it % 10 == 0:
            json.dump(pool, open(pool_path, "w"))
        if it % 25 == 0:
            print(f"[K={K}] iter {it}, pool={len(pool)}, {elapsed:.1f}s", flush=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=1)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--m", type=int, default=8)
    ap.add_argument("--lo", type=int, default=1)
    ap.add_argument("--K", type=int, required=True)
    ap.add_argument("--add", type=int, default=3)
    ap.add_argument("--time-limit", type=float, default=600.0)
    ap.add_argument("--out", type=str, default=None)
    ap.add_argument("--telemetry", type=str, default=None)
    ap.add_argument("--pool", type=str, default=None)
    a = ap.parse_args()
    out = a.out or f"results/cegar_n{a.n}_m{a.m}_lo{a.lo}_K{a.K}.json"
    run(a.n, a.m, a.lo, a.K, a.add, a.time_limit, out, a.telemetry, a.pool)
