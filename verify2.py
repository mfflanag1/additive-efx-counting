#!/usr/bin/env python3
"""Independent exact EFX verifier (verifier #2).

Enumerates every complete labeled allocation of m goods to n agents by a
recursive good-by-good branch, and checks the EFX0 and EFXplus conditions
with exact integer arithmetic.

Definitions (additive valuations v[i][g], nonnegative integers):
  A complete allocation assigns every good to exactly one of n labeled agents.
  EFX0:    for all i != j and EVERY good g in X_j: v_i(X_i) >= v_i(X_j) - v_i(g)
  EFXplus: same, but only over goods g in X_j with v_i(g) > 0

The per-pair constraint "for every g in X_j" is tightest at the good with the
smallest v_i(g) (it subtracts the least), so it reduces to
  v_i(X_i) >= v_i(X_j) - min_{g in X_j} v_i(g)
with the min taken over all goods (EFX0) or positive goods (EFXplus). An empty
bundle X_j (or, for EFXplus, one with no positively-valued good) yields no
constraint.
"""

import json
import sys
import random


def check_both(assign, v, n, m):
    """Return (efx0_ok, efxplus_ok) for one complete allocation.

    assign[g] = agent index that receives good g.
    """
    bv = [[0] * n for _ in range(n)]        # bv[i][j] = v_i(X_j)
    minall = [[None] * n for _ in range(n)] # min v_i(g) over g in X_j
    minpos = [[None] * n for _ in range(n)] # min v_i(g) over g in X_j with v_i(g)>0

    for g in range(m):
        j = assign[g]
        for i in range(n):
            val = v[i][g]
            bv[i][j] += val
            ma = minall[i][j]
            if ma is None or val < ma:
                minall[i][j] = val
            if val > 0:
                mp = minpos[i][j]
                if mp is None or val < mp:
                    minpos[i][j] = val

    efx0 = True
    efxp = True
    for i in range(n):
        bvii = bv[i][i]
        row_bv = bv[i]
        row_all = minall[i]
        row_pos = minpos[i]
        for j in range(n):
            if i == j:
                continue
            if efx0:
                m0 = row_all[j]
                if m0 is not None and bvii < row_bv[j] - m0:
                    efx0 = False
            if efxp:
                mp = row_pos[j]
                if mp is not None and bvii < row_bv[j] - mp:
                    efxp = False
        if not efx0 and not efxp:
            break
    return efx0, efxp


def analyze(n, m, v):
    """Exhaustively count EFX0 / EFXplus allocations via recursive branching.

    Returns (efx0_count, efxplus_count, example_efx0_assignment_or_None).
    """
    assign = [0] * m
    counts = [0, 0]          # [efx0, efxplus]
    example = [None]

    def rec(k):
        if k == m:
            efx0, efxp = check_both(assign, v, n, m)
            if efx0:
                counts[0] += 1
                if example[0] is None:
                    example[0] = list(assign)
            if efxp:
                counts[1] += 1
            return
        for a in range(n):
            assign[k] = a
            rec(k + 1)

    rec(0)
    return counts[0], counts[1], example[0]


def assignment_to_bundles(assign, n):
    bundles = [[] for _ in range(n)]
    for g, a in enumerate(assign):
        bundles[a].append(g)
    return bundles


def run_instance(n, m, v):
    efx0_count, efxplus_count, example = analyze(n, m, v)
    return {
        "efx0_exists": efx0_count > 0,
        "efx0_count": efx0_count,
        "efxplus_exists": efxplus_count > 0,
        "efxplus_count": efxplus_count,
        "example_efx0": assignment_to_bundles(example, n) if example is not None else None,
    }


# --------------------------------------------------------------------------
# Self-test machinery
# --------------------------------------------------------------------------

def naive_efx0(assign, v, n, m, positive_only=False):
    """Definition-faithful checker, independent of check_both (for cross-check)."""
    bundles = assignment_to_bundles(assign, n)
    for i in range(n):
        xi = sum(v[i][g] for g in bundles[i])
        for j in range(n):
            if i == j:
                continue
            xj = sum(v[i][g] for g in bundles[j])
            for g in bundles[j]:
                if positive_only and v[i][g] <= 0:
                    continue
                if xi < xj - v[i][g]:
                    return False
    return True


def naive_counts(n, m, v):
    """Brute-force counts by an independent product-style inner loop."""
    from itertools import product
    c0 = 0
    cp = 0
    for assign in product(range(n), repeat=m):
        assign = list(assign)
        if naive_efx0(assign, v, n, m, positive_only=False):
            c0 += 1
        if naive_efx0(assign, v, n, m, positive_only=True):
            cp += 1
    return c0, cp


def selftest():
    all_pass = True

    def report(name, ok, detail=""):
        nonlocal all_pass
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_pass = False
        line = f"[{status}] {name}"
        if detail:
            line += f"  ({detail})"
        print(line)

    # Check 1: n=2, identical valuations, m<=6, values 0..9, 30 seeded instances.
    ok1 = True
    fail_detail = ""
    rng = random.Random(1001)
    for _ in range(30):
        m = rng.randint(1, 6)
        row = [rng.randint(0, 9) for _ in range(m)]
        v = [row[:], row[:]]  # identical valuations
        res = run_instance(2, m, v)
        if not res["efx0_exists"]:
            ok1 = False
            fail_detail = f"m={m} v={row}"
            break
    report("1: n=2 identical valuations -> EFX0 always exists", ok1, fail_detail)

    # Check 2: n=3, m<=5, all-positive 1..5, 30 seeded instances.
    ok2 = True
    fail_detail = ""
    rng = random.Random(2002)
    for _ in range(30):
        m = rng.randint(1, 5)
        v = [[rng.randint(1, 5) for _ in range(m)] for _ in range(3)]
        res = run_instance(3, m, v)
        if not res["efx0_exists"]:
            ok2 = False
            fail_detail = f"m={m} v={v}"
            break
    report("2: n=3 all-positive -> EFX0 always exists", ok2, fail_detail)

    # Check 3: single good, n=2, values [[5],[5]].
    res3 = run_instance(2, 1, [[5], [5]])
    ok3 = res3["efx0_exists"]
    report("3: single good n=2 [[5],[5]] -> EFX0 exists", ok3,
           f"efx0_count={res3['efx0_count']}")

    # Check 4: n=2, m=2, [[10,1],[10,1]] cross-checked against naive counts.
    v4 = [[10, 1], [10, 1]]
    res4 = run_instance(2, 2, v4)
    n0, np = naive_counts(2, 2, v4)
    ok4 = (res4["efx0_count"] == n0) and (res4["efxplus_count"] == np)
    report("4: n=2 m=2 [[10,1],[10,1]] counts match naive", ok4,
           f"mine=({res4['efx0_count']},{res4['efxplus_count']}) naive=({n0},{np})")

    # Check 5: monotonicity efxplus_count >= efx0_count, 20 seeded, zeros allowed.
    ok5 = True
    fail_detail = ""
    rng = random.Random(5005)
    for _ in range(20):
        n = rng.randint(2, 3)
        m = rng.randint(1, 6)
        v = [[rng.randint(0, 6) for _ in range(m)] for _ in range(n)]
        res = run_instance(n, m, v)
        if res["efxplus_count"] < res["efx0_count"]:
            ok5 = False
            fail_detail = f"n={n} m={m} v={v}"
            break
    report("5: monotonicity efxplus_count >= efx0_count", ok5, fail_detail)

    print("PASS" if all_pass else "FAIL")
    return all_pass


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        ok = selftest()
        sys.exit(0 if ok else 1)

    if len(argv) != 2:
        sys.stderr.write("usage: python3 verify2.py instance.json | --selftest\n")
        sys.exit(2)

    with open(argv[1]) as f:
        inst = json.load(f)
    n = inst["n"]
    m = inst["m"]
    v = inst["values"]

    if len(v) != n or any(len(row) != m for row in v):
        sys.stderr.write("instance shape mismatch with declared n/m\n")
        sys.exit(2)

    result = run_instance(n, m, v)
    print(json.dumps(result))


if __name__ == "__main__":
    main(sys.argv)
