"""Counting-CEGAR for Neoh-Teh Conjecture 6.1 at (4,7), bounded values.

Question: does some V in [1,K]^{4x7} have AT MOST 3 EFX0 allocations? (Existence of
EFX0 at (4,7) is guaranteed by Mahara m<=n+3, so counts are >=1; a count<=3 instance
refutes Conjecture 6.1 [Neoh-Teh AAAI-25: at least n]. UNSAT = bounded verification:
every (4,7) instance with values<=K has >=4 EFX0 allocations.)

Master: V vars + THREE slot allocations s[t] (assignments the master may protect).
Every pooled allocation must be killed (strong envy exists) OR equal some slot.
Slave: exact count with cap; count<=3 -> witness candidate (dual-verify externally).
Cuts: row/col double-lex only (count is permutation-invariant; no type cuts — the
types theorems say nothing about counts).
"""
import argparse
import json
import time

from ortools.sat.python import cp_model

from cegar import add_lex_ge
from verify import enumerate_all

N, M = 4, 7


def run(K, out_path, pool_path):
    pool = []
    try:
        pool = json.load(open(pool_path))
        print(f"resumed {len(pool)}", flush=True)
    except Exception:
        pass
    t0 = time.time()
    it = 0
    while True:
        it += 1
        md = cp_model.CpModel()
        v = [[md.NewIntVar(1, K, "") for g in range(M)] for i in range(N)]
        for i in range(N - 1):
            add_lex_ge(md, v[i], v[i + 1])
        for g in range(M - 1):
            add_lex_ge(md, [v[i][g] for i in range(N)], [v[i][g + 1] for i in range(N)])
        slots = [[md.NewIntVar(0, N - 1, "") for g in range(M)] for t in range(3)]
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
            for t in range(3):
                eq = md.NewBoolVar("")
                for g, a in enumerate(assign):
                    md.Add(slots[t][g] == a).OnlyEnforceIf(eq)
                lits.append(eq)
            md.AddBoolOr(lits)
        s = cp_model.CpSolver()
        s.parameters.num_search_workers = 6
        s.parameters.max_time_in_seconds = 10800
        st = s.Solve(md)
        el = time.time() - t0
        if st == cp_model.INFEASIBLE:
            print(f"COUNT-UNSAT after {it} iters pool={len(pool)} {el:.0f}s => "
                  f"THEOREM: every (4,7) instance with values<={K} has >=4 EFX0 "
                  f"allocations (Conjecture 6.1 verified, bounded)", flush=True)
            json.dump({"status": "UNSAT", "K": K, "iters": it, "pool": len(pool)},
                      open(out_path, "w"))
            return
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print(f"STALL iter {it} pool={len(pool)}", flush=True)
            json.dump({"status": "STALL", "K": K, "iters": it, "pool": len(pool)},
                      open(out_path, "w"))
            return
        V = [[s.Value(v[i][g]) for g in range(M)] for i in range(N)]
        res = enumerate_all(N, M, V, collect=8)
        cnt = res["efx0_count"]
        assert cnt >= 1, f"Mahara violation?! {V}"
        if cnt <= 3:
            print(f"*** CONJECTURE 6.1 COUNTEREXAMPLE CANDIDATE *** count={cnt} "
                  f"{json.dumps(V)}", flush=True)
            json.dump({"status": "WITNESS", "count": cnt, "values": V},
                      open(out_path, "w"))
            return
        pool.extend(res["examples_efx0"][:5])
        if it % 10 == 0:
            json.dump(pool, open(pool_path, "w"))
        if it % 25 == 0:
            print(f"iter {it} pool={len(pool)} {el:.0f}s", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--K", type=int, required=True)
    a = ap.parse_args()
    run(a.K, f"results/countcegar_K{a.K}.json", f"results/countpool_K{a.K}.json")
