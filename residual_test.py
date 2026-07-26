"""Test harness for the residual attack: does NC-A + no-universal-min +
pairwise-non-proportional force an EFX0 allocation of shape 4211 or 3221?

Shapes are the sorted bundle-size multiset. We classify each EFX0 allocation.
"""
import random
from math import gcd
from functools import reduce
from verify import precompute, check_allocation

INF = float("inf")


def shape_of(assign, n=4):
    return tuple(sorted((assign.count(i) for i in range(n)), reverse=True))


def tau(i, mask, val, minall):
    if mask == 0:
        return 0
    return val[i][mask] - minall[i][mask]


def dominant_pairs(n, m, values):
    """(i,g) dominant iff v_i(g) >= tau_i(M\\{g})."""
    val, minall, minpos = precompute(n, m, values)
    full = (1 << m) - 1
    D = []
    for i in range(n):
        for g in range(m):
            if values[i][g] >= tau(i, full ^ (1 << g), val, minall):
                D.append((i, g))
    return D


def has_matching_size2(D, n, m):
    """Is there a size-2 matching in the dominant bipartite relation (distinct
    agents AND distinct goods)?"""
    for a in range(n):
        for b in range(n):
            if a == b:
                continue
            for (i, g) in D:
                if i != a:
                    continue
                for (j, h) in D:
                    if j == b and h != g:
                        return True
    return False


def satisfies_NCA(n, m, values):
    D = dominant_pairs(n, m, values)
    return not has_matching_size2(D, n, m)


def universal_min_good(n, m, values):
    """A good f that is every agent's (weak) min."""
    for g in range(m):
        if all(values[i][g] == min(values[i]) for i in range(n)):
            return g
    return None


def proportional(r1, r2):
    """Are two positive integer rows proportional (r1 = c*r2)?"""
    # cross-multiply: r1[k]*r2[l] == r1[l]*r2[k] for all k,l
    m = len(r1)
    for k in range(m):
        for l in range(k + 1, m):
            if r1[k] * r2[l] != r1[l] * r2[k]:
                return False
    return True


def pairwise_nonproportional(n, m, values):
    for i in range(n):
        for j in range(i + 1, n):
            if proportional(values[i], values[j]):
                return False
    return True


def efx0_shapes(n, m, values):
    """Return set of shapes that admit an EFX0 allocation, plus total count and
    whether 4211/3221 present. Full enumeration."""
    val, minall, minpos = precompute(n, m, values)
    assign = [0] * m
    shapes = {}
    while True:
        bundles = [0] * n
        for g in range(m):
            bundles[assign[g]] |= 1 << g
        e0, _ = check_allocation(n, bundles, val, minall, minpos)
        if e0:
            s = shape_of(assign, n)
            shapes[s] = shapes.get(s, 0) + 1
        g = 0
        while g < m:
            assign[g] += 1
            if assign[g] < n:
                break
            assign[g] = 0
            g += 1
        else:
            break
    return shapes


def check_claim_instance(n, m, values):
    """Returns dict: does it satisfy the 3 NCs, and which shapes have EFX0."""
    if universal_min_good(n, m, values) is not None:
        return None
    if not satisfies_NCA(n, m, values):
        return None
    if not pairwise_nonproportional(n, m, values):
        return None
    shapes = efx0_shapes(n, m, values)
    target = shapes.get((4, 2, 1, 1), 0) + shapes.get((3, 2, 2, 1), 0)
    return {
        "shapes": shapes,
        "efx0_exists": len(shapes) > 0,
        "target_4211_3221": target,
        "values": values,
    }


if __name__ == "__main__":
    import sys
    random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    N = int(sys.argv[3]) if len(sys.argv) > 3 else 20000
    n, m = 4, 8
    tested = 0
    no_target_but_efx = 0
    no_efx = 0
    examples = []
    for _ in range(N):
        values = [[random.randint(1, hi) for _ in range(m)] for _ in range(n)]
        res = check_claim_instance(n, m, values)
        if res is None:
            continue
        tested += 1
        if not res["efx0_exists"]:
            no_efx += 1
            examples.append(("NO_EFX", values, res["shapes"]))
        elif res["target_4211_3221"] == 0:
            no_target_but_efx += 1
            if len(examples) < 12:
                examples.append(("NO_TARGET", values, res["shapes"]))
    print(f"tested(satisfying 3 NCs): {tested}")
    print(f"  EFX0-free: {no_efx}")
    print(f"  EFX0 exists but NO 4211/3221: {no_target_but_efx}")
    for tag, v, sh in examples[:12]:
        print(tag, v, dict(sh))
