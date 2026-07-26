"""CEGAR with a Z3 LRA master: resolves an (n, m) cell over ALL positive real
valuations, not just bounded integers.

Soundness: EFX conditions are invariant under per-agent positive scaling, so WLOG each
row is normalized to sum 1. Master seeks real V > 0 (row-normalized) killing every pooled
allocation, using exact rational arithmetic and strict inequalities (native in Z3 LRA).

  SAT   -> candidate witness (exact rationals -> scaled to integers -> dual verification)
  UNSAT -> THEOREM: every additive instance with n agents, m goods, all-positive values
           admits an EFX0 (= EFX+) allocation, PROVIDED rows pairwise non-proportional;
           proportional rows reduce to <= (n-1) distinct types, covered by the types
           theorems (cite in LEDGER.md). Zeros: covered for UNSAT via the 2001.09838 eps-perturbation reduction (superseding earlier caveat).

Optional cut --distinct-rows: witness must have pairwise non-proportional rows (sound via
types theorem for n=4: <=3 types proven safe).
"""
import argparse
import json
import time
from fractions import Fraction

import z3
# parallel mode removed: portfolio search defeats incremental learned-clause reuse,
# which is the dominant cost saver in a CEGAR loop (reviewer note, 2026-07-25)

from verify import enumerate_all


def find_efx0_assigns(n, m, values, k):
    res = enumerate_all(n, m, values, early_exit=False, collect=k)
    return res["examples_efx0"][:k], res["efx0_count"]


def bundles_of(assign, n):
    b = [[] for _ in range(n)]
    for g, a in enumerate(assign):
        b[a].append(g)
    return b


def model_to_int_values(model, v, n, m):
    """Exact rationals from Z3 model -> integer matrix via common denominator."""
    fr = [[Fraction(model[v[i][g]].numerator_as_long(),
                    model[v[i][g]].denominator_as_long())
           for g in range(m)] for i in range(n)]
    out = []
    for i in range(n):
        den = 1
        for x in fr[i]:
            den = den * x.denominator // __import__("math").gcd(den, x.denominator)
        row = [int(x * den) for x in fr[i]]
        from math import gcd
        gg = 0
        for x in row:
            gg = gcd(gg, x)
        out.append([x // max(gg, 1) for x in row])
    return out


def run(n, m, add_per_iter, distinct_rows, out_path, log_every=10):
    v = [[z3.Real(f"v_{i}_{g}") for g in range(m)] for i in range(n)]
    s = z3.Solver()
    for i in range(n):
        for g in range(m):
            s.add(v[i][g] > 0)
        s.add(z3.Sum(v[i]) == 1)
    # PROVEN witness-necessary conditions (sound cuts; see PER_K.md Peeling Theorem and
    # PARKING_FLOOR_LEMMA + Mahara Lemma 7 for no-universal-min):
    # SCOPE GUARD (referee): Peeling needs n=4 (peel leaves 3 agents -> CGM); universal-min
    # parking needs a Mahara base on m-1 <= n+3 goods. Cuts apply ONLY when n==4 and m<=8.
    apply_cuts = (n == 4 and m <= 8)
    # (a) no dominant good: forall i,t: v[i][t] < sum_{g!=t} v[i][g] - min_{g!=t} v[i][g]
    #     encoded exactly as: exists g'!=t with v[i][t] < sum_{g!=t} v[i][g] - v[i][g']
    if apply_cuts:
        for i in range(n):
            for t in range(m):
                rest = [g for g in range(m) if g != t]
                tot_rest = z3.Sum([v[i][g] for g in rest])
                s.add(z3.Or([v[i][t] < tot_rest - v[i][gp] for gp in rest]))
        # (b) no universal-min good: forall g: exists i, g' with v[i][g] > v[i][g']
        for g in range(m):
            s.add(z3.Or([v[i][g] > v[i][gp] for i in range(n) for gp in range(m) if gp != g]))
    if distinct_rows:
        for i in range(n):
            for j in range(i + 1, n):
                s.add(z3.Or([v[i][g] != v[j][g] for g in range(m)]))

    pool = 0
    warm = []
    try:
        warm = json.load(open("results/z3_pool.json"))
    except Exception:
        try:
            warm = json.load(open("results/anatomy_pool.json"))[:2000]
        except Exception:
            pass
    saved_assigns = []
    for assign in warm:
        bl = bundles_of(assign, n)
        lits = []
        for g, j in enumerate(assign):
            for i in range(n):
                if i == j:
                    continue
                lhs = z3.Sum([v[i][h] for h in bl[i]]) if bl[i] else z3.RealVal(0)
                rhs = z3.Sum([v[i][h] for h in bl[j] if h != g])
                lits.append(lhs < rhs)
        s.add(z3.Or(lits))
        pool += 1
        saved_assigns.append(assign)
    if warm:
        print(f"warm-started with {pool} pooled allocations", flush=True)
    t0 = time.time()
    it = 0
    while True:
        it += 1
        st = s.check()
        el = time.time() - t0
        if st == z3.unsat:
            result = {"status": "UNSAT", "n": n, "m": m, "iterations": it,
                      "pool_size": pool, "seconds": round(el, 1),
                      "distinct_rows": distinct_rows}
            print(f"UNSAT after {it} iters, pool={pool}, {el:.1f}s => THEOREM: "
                  f"every additive n={n}, m={m}, all-positive instance"
                  f"{' (non-proportional rows)' if distinct_rows else ''} "
                  f"has an EFX allocation")
            break
        if st != z3.sat:
            result = {"status": str(st), "n": n, "m": m, "iterations": it,
                      "pool_size": pool, "seconds": round(el, 1)}
            print(f"solver returned {st} at iter {it}")
            break
        mdl = s.model()
        values = model_to_int_values(mdl, v, n, m)
        efx, count = find_efx0_assigns(n, m, values, add_per_iter)
        if count == 0:
            result = {"status": "WITNESS", "n": n, "m": m, "iterations": it,
                      "pool_size": pool, "seconds": round(el, 1), "values": values}
            print(f"*** WITNESS CANDIDATE at iter {it} *** {json.dumps(values)}")
            break
        for assign in efx:
            saved_assigns.append(assign)
            bl = bundles_of(assign, n)
            lits = []
            for g, j in enumerate(assign):
                for i in range(n):
                    if i == j:
                        continue
                    lhs = z3.Sum([v[i][h] for h in bl[i]]) if bl[i] else z3.RealVal(0)
                    rhs = z3.Sum([v[i][h] for h in bl[j] if h != g])
                    lits.append(lhs < rhs)
            s.add(z3.Or(lits))
            pool += 1
        if it % log_every == 0:
            print(f"iter {it}, pool={pool}, {el:.1f}s", flush=True)
            json.dump(saved_assigns, open("results/z3_pool.json", "w"))
    with open(out_path, "w") as f:
        json.dump(result, f, indent=1)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--m", type=int, default=8)
    ap.add_argument("--add", type=int, default=5)
    ap.add_argument("--no-distinct-rows", action="store_true")
    ap.add_argument("--out", type=str, required=True)
    a = ap.parse_args()
    run(a.n, a.m, a.add, not a.no_distinct_rows, a.out)
