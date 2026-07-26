"""Crux-lemma CEGAR (theory3 COUNT_LB_M_N3 reduction): does every (4,7) instance with
values in [1,K] admit a fully ENVY-FREE base of shape 3111 on some 6 goods?

Master: find V killing every pooled base (some plain envy in it). Slave: enumerate all
(floater f, 3111 envy-free base of M\{f}) for candidate V.
  UNSAT  -> bounded verification of the crux lemma => with theory3's conditional theorem,
            every (4,7) instance with values<=K has >=4 EFX0 allocations.
  no-base instance found -> the hard case for Conjecture 6.1 made explicit (check its
            EFX0 count immediately; a low count would be a refutation path).
"""
import argparse
import itertools
import json
import time

from ortools.sat.python import cp_model

from cegar import add_lex_ge
from verify import enumerate_all

N, M = 4, 7


def envy_free_3111_bases(values, cap=5):
    """Return up to cap (floater, owner-assignment) envy-free 3111 bases."""
    out = []
    for f in range(M):
        goods = [g for g in range(M) if g != f]
        # choose the 3-bundle's owner and goods; remaining 3 goods are singletons
        for owner3 in range(N):
            for trip in itertools.combinations(goods, 3):
                rest = [g for g in goods if g not in trip]
                for perm in itertools.permutations(range(N)):
                    # perm maps positions to owners of singletons; owner3 fixed
                    singles = [p for p in range(N) if p != owner3]
                    for assign_s in itertools.permutations(rest, 3):
                        bundles = {owner3: list(trip)}
                        for ag, gd in zip(singles, assign_s):
                            bundles[ag] = [gd]
                        vals = [sum(values[i][g] for g in bundles[i]) for i in range(N)]
                        ok = True
                        for i in range(N):
                            for j in range(N):
                                if i != j and sum(values[i][g] for g in bundles[j]) > vals[i]:
                                    ok = False
                                    break
                            if not ok:
                                break
                        if ok:
                            out.append((f, {a: sorted(b) for a, b in bundles.items()}))
                            if len(out) >= cap:
                                return out
                    break  # perm loop redundant with assign_s permutations
    return out


def run(K):
    pool = []
    t0 = time.time()
    it = 0
    while True:
        it += 1
        md = cp_model.CpModel()
        v = [[md.NewIntVar(1, K, "") for g in range(M)] for i in range(N)]
        for i in range(N - 1):
            add_lex_ge(md, v[i], v[i + 1])
        # hunt-mode structure constraints (exclude flat/identical regime where no-base is
        # trivial but counts are combinatorially large): distinct rows + per-agent spread
        for i in range(N):
            for j in range(i + 1, N):
                nes = []
                for g in range(M):
                    b = md.NewBoolVar("")
                    md.Add(v[i][g] != v[j][g]).OnlyEnforceIf(b)
                    md.Add(v[i][g] == v[j][g]).OnlyEnforceIf(b.Not())
                    nes.append(b)
                md.AddBoolOr(nes)
        for i in range(N):
            mx = md.NewIntVar(1, K, ""); mn = md.NewIntVar(1, K, "")
            md.AddMaxEquality(mx, v[i]); md.AddMinEquality(mn, v[i])
            md.Add(mx - mn >= 4)
        for g in range(M - 1):
            add_lex_ge(md, [v[i][g] for i in range(N)], [v[i][g + 1] for i in range(N)])
        for f, bundles in pool:
            lits = []
            for i in range(N):
                for j in range(N):
                    if i == j:
                        continue
                    b = md.NewBoolVar("")
                    md.Add(sum(v[i][g] for g in bundles[j]) >=
                           sum(v[i][g] for g in bundles[i]) + 1).OnlyEnforceIf(b)
                    lits.append(b)
            md.AddBoolOr(lits)
        s = cp_model.CpSolver()
        s.parameters.num_search_workers = 4
        s.parameters.max_time_in_seconds = 1800
        st = s.Solve(md)
        el = time.time() - t0
        if st == cp_model.INFEASIBLE:
            print(f"CRUX-UNSAT after {it} iters pool={len(pool)} {el:.0f}s => every "
                  f"(4,7) instance with values<={K} has an envy-free 3111 base "
                  f"(=> >=4 EFX0 via theory3 conditional theorem)", flush=True)
            json.dump({"status": "UNSAT", "K": K, "iters": it, "pool": len(pool)},
                      open(f"results/base_cegar_K{K}.json", "w"))
            return
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print(f"STALL iter {it}", flush=True)
            json.dump({"status": "STALL", "K": K, "iters": it, "pool": len(pool)},
                      open(f"results/base_cegar_K{K}.json", "w"))
            return
        V = [[s.Value(v[i][g]) for g in range(M)] for i in range(N)]
        bases = envy_free_3111_bases(V, cap=5)
        if not bases:
            cnt = enumerate_all(N, M, V)["efx0_count"]
            print(f"*** NO-BASE INSTANCE *** efx0_count={cnt} {json.dumps(V)}", flush=True)
            json.dump({"status": "NO_BASE", "efx0_count": cnt, "values": V},
                      open(f"results/base_cegar_K{K}.json", "w"))
            return
        pool.extend(bases)
        if it % 25 == 0:
            print(f"iter {it} pool={len(pool)} {el:.0f}s", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--K", type=int, required=True)
    a = ap.parse_args()
    run(a.K)
