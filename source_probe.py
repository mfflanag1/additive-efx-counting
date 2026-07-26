"""SOURCE LEMMA probe at (4,7): hunt a counterexample to
  "every 4-agent 7-good positive-additive instance has an EFX0 allocation whose
   plain-envy graph has a source (un-envied bundle)."

Master (CP-SAT): find V in [1,K]^{4x7} such that every pooled allocation is
(not EFX0) OR (not sourced). Slave: enumerate ALL EFX0 allocations of V (4^7=16384);
if some exist and NONE has a source -> LEMMA COUNTEREXAMPLE (witness recipe for (4,8)).
If UNSAT -> Source Lemma holds for values <= K -> proof target for theory.
Note: every (4,7) instance HAS EFX0 allocations (Mahara m<=n+3), so the slave's
"EFX0 exists" check is a soundness assert, not a branch.
"""
import argparse
import json
import time

from ortools.sat.python import cp_model

from verify import check_allocation, masks_from_assign, precompute

N, M = 4, 7


def efx0_allocations(values):
    val, minall, minpos = precompute(N, M, values)
    out = []
    assign = [0] * M
    while True:
        bundles = masks_from_assign(N, assign)
        e0, _ = check_allocation(N, bundles, val, minall, minpos)
        if e0:
            out.append((list(assign), bundles))
        g = 0
        while g < M:
            assign[g] += 1
            if assign[g] < N:
                break
            assign[g] = 0
            g += 1
        else:
            return out


def sourced(values, bundles, val):
    """True if some bundle j is plainly envied by nobody: v_i(B_j) <= v_i(B_i) all i."""
    for j in range(N):
        if all(val[i][bundles[j]] <= val[i][bundles[i]] for i in range(N) if i != j):
            return True
    return False


def run(K, out_path, pool_path):
    pool = []
    try:
        pool = json.load(open(pool_path))
        print(f"resumed pool {len(pool)}", flush=True)
    except Exception:
        pass
    t0 = time.time()
    it = 0
    while True:
        it += 1
        md = cp_model.CpModel()
        v = [[md.NewIntVar(1, K, "") for g in range(M)] for i in range(N)]
        for assign in pool:
            bundles = [[] for _ in range(N)]
            for g, a in enumerate(assign):
                bundles[a].append(g)
            lits = []
            # (a) strong envy somewhere -> not EFX0
            for g, j in enumerate(assign):
                for i in range(N):
                    if i == j:
                        continue
                    b = md.NewBoolVar("")
                    md.Add(sum(v[i][h] for h in bundles[i]) + v[i][g] + 1
                           <= sum(v[i][h] for h in bundles[j])).OnlyEnforceIf(b)
                    lits.append(b)
            # (b) not sourced: every bundle plainly envied by someone
            env = []
            for j in range(N):
                ej = md.NewBoolVar("")
                envliterals = []
                for i in range(N):
                    if i == j:
                        continue
                    b = md.NewBoolVar("")
                    md.Add(sum(v[i][h] for h in bundles[j]) >=
                           sum(v[i][h] for h in bundles[i]) + 1).OnlyEnforceIf(b)
                    envliterals.append(b)
                md.AddBoolOr(envliterals).OnlyEnforceIf(ej)
                env.append(ej)
            ns = md.NewBoolVar("")
            md.AddBoolAnd(env).OnlyEnforceIf(ns)
            lits.append(ns)
            md.AddBoolOr(lits)
        s = cp_model.CpSolver()
        s.parameters.num_search_workers = 4
        s.parameters.max_time_in_seconds = 1800
        st = s.Solve(md)
        el = time.time() - t0
        if st == cp_model.INFEASIBLE:
            print(f"SOURCE LEMMA HOLDS for values<={K} (UNSAT, {it} iters, "
                  f"pool={len(pool)}, {el:.0f}s)", flush=True)
            json.dump({"status": "LEMMA_HOLDS", "K": K, "iters": it,
                       "pool": len(pool)}, open(out_path, "w"))
            return
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print(f"STALL iter {it} pool={len(pool)}", flush=True)
            json.dump({"status": "STALL", "K": K, "iters": it,
                       "pool": len(pool)}, open(out_path, "w"))
            return
        values = [[s.Value(v[i][g]) for g in range(M)] for i in range(N)]
        allocs = efx0_allocations(values)
        assert allocs, f"soundness violation: (4,7) instance without EFX0! {values}"
        val, _, _ = precompute(N, M, values)
        srcd = [a for a, b in allocs if sourced(values, b, val)]
        if not srcd:
            print(f"*** SOURCE-LEMMA COUNTEREXAMPLE *** {json.dumps(values)} "
                  f"({len(allocs)} EFX0 allocations, all fully envy-cycled)", flush=True)
            json.dump({"status": "COUNTEREXAMPLE", "values": values,
                       "efx0_count": len(allocs)}, open(out_path, "w"))
            return
        pool.extend(srcd[:5])
        if it % 10 == 0:
            json.dump(pool, open(pool_path, "w"))
        if it % 25 == 0:
            print(f"iter {it} pool={len(pool)} {el:.0f}s", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--K", type=int, required=True)
    a = ap.parse_args()
    run(a.K, f"results/source_probe_K{a.K}.json", f"results/source_pool_K{a.K}.json")
