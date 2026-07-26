"""Verifier #1: exact exhaustive EFX checker (bitmask/base-n counter strategy).

Instance JSON: {"n": int, "m": int, "values": [[int,...],...]}  (n rows, m cols, ints >= 0)
Output JSON: efx0_exists/count, efxplus_exists/count, example_efx0.

EFX0:    forall i!=j, forall g in X_j:                 v_i(X_i) >= v_i(X_j) - v_i(g)
EFXplus: forall i!=j, forall g in X_j with v_i(g)>0:   v_i(X_i) >= v_i(X_j) - v_i(g)
Both reduce to comparing against the max-remainder removal (min-valued removable good).
"""
import json
import sys

INF = float("inf")


def precompute(n, m, values):
    """val[i][mask], minall[i][mask], minpos[i][mask] for all 2^m subsets."""
    size = 1 << m
    val = [[0] * size for _ in range(n)]
    minall = [[INF] * size for _ in range(n)]
    minpos = [[INF] * size for _ in range(n)]
    for i in range(n):
        vi = values[i]
        for mask in range(1, size):
            g = (mask & -mask).bit_length() - 1
            rest = mask & (mask - 1)
            val[i][mask] = val[i][rest] + vi[g]
            minall[i][mask] = min(minall[i][rest], vi[g])
            minpos[i][mask] = min(minpos[i][rest], vi[g]) if vi[g] > 0 else minpos[i][rest]
    return val, minall, minpos


def check_allocation(n, bundles, val, minall, minpos):
    """Return (is_efx0, is_efxplus) for bundles given as bitmasks."""
    efx0 = efxp = True
    for i in range(n):
        vi_own = val[i][bundles[i]]
        for j in range(n):
            if i == j or bundles[j] == 0:
                continue
            vj = val[i][bundles[j]]
            if vi_own >= vj:
                continue
            ma = minall[i][bundles[j]]
            mp = minpos[i][bundles[j]]
            if vi_own < vj - (0 if ma is INF else ma):
                efx0 = False
            if mp is not INF and vi_own < vj - mp:
                efxp = False
            if not efx0 and not efxp:
                return False, False
    return efx0, efxp


def enumerate_all(n, m, values, early_exit=False, collect=0):
    """Base-n counter over all n^m complete allocations.

    Returns dict with counts, existence, and up to `collect` EFX0 examples.
    early_exit: stop at first EFX0 allocation (for CEGAR inner loop).
    """
    val, minall, minpos = precompute(n, m, values)
    c0 = cp = 0
    examples = []
    assign = [0] * m
    while True:
        bundles = [0] * n
        for g in range(m):
            bundles[assign[g]] |= 1 << g
        e0, ep = check_allocation(n, bundles, val, minall, minpos)
        if e0:
            c0 += 1
            if len(examples) < max(collect, 1):
                examples.append(list(assign))
            if early_exit:
                break
        if ep:
            cp += 1
        # increment base-n counter
        g = 0
        while g < m:
            assign[g] += 1
            if assign[g] < n:
                break
            assign[g] = 0
            g += 1
        else:
            break
    return {
        "efx0_exists": c0 > 0,
        "efx0_count": c0,
        "efxplus_exists": cp > 0,
        "efxplus_count": cp,
        "examples_efx0": examples,
    }


def masks_from_assign(n, assign):
    bundles = [0] * n
    for g, a in enumerate(assign):
        bundles[a] |= 1 << g
    return bundles


def main():
    with open(sys.argv[1]) as f:
        inst = json.load(f)
    n, m, values = inst["n"], inst["m"], inst["values"]
    assert len(values) == n and all(len(r) == m for r in values)
    res = enumerate_all(n, m, values)
    ex = res["examples_efx0"]
    out = {
        "efx0_exists": res["efx0_exists"],
        "efx0_count": res["efx0_count"],
        "efxplus_exists": res["efxplus_exists"],
        "efxplus_count": res["efxplus_count"],
        "example_efx0": [[g for g in range(m) if ex[0][g] == i] for i in range(n)] if ex else None,
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
