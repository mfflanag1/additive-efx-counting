"""Enumerate ALL EFX0 allocations of a small instance and report structure.

For (4,7): enumerate all 4^7 assignments, keep EFX0 ones, report for each the
partition shape (sorted bundle sizes) and which agents get which bundles.
"""
import numpy as np
from itertools import product
from collections import Counter


def tau0(vi, S):
    if not S:
        return 0
    vals = [vi[g] for g in S]
    return sum(vals) - min(vals)


def is_efx0(values, assign):
    """assign: list length m, assign[g] = agent owning good g."""
    n = len(values)
    m = len(values[0])
    bundles = [[] for _ in range(n)]
    for g in range(m):
        bundles[assign[g]].append(g)
    own = [sum(values[i][g] for g in bundles[i]) for i in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if own[i] < tau0(values[i], bundles[j]):
                return False
    return True


def all_efx0(values):
    """Return list of (assign_tuple, shape, bundles) for every EFX0 allocation."""
    n = len(values)
    m = len(values[0])
    out = []
    for assign in product(range(n), repeat=m):
        if is_efx0(values, assign):
            bundles = [[] for _ in range(n)]
            for g in range(m):
                bundles[assign[g]].append(g)
            shape = tuple(sorted((len(b) for b in bundles), reverse=True))
            out.append((assign, shape, bundles))
    return out


def summarize(values, label=""):
    allocs = all_efx0(values)
    shapes = Counter(s for _, s, _ in allocs)
    print(f"--- {label} n={len(values)} m={len(values[0])} : {len(allocs)} EFX0 allocations")
    for sh, cnt in sorted(shapes.items(), key=lambda x: -x[1]):
        print(f"    shape {sh}: {cnt}")
    return allocs, shapes


if __name__ == "__main__":
    import sys, json
    data = json.loads(sys.argv[1])
    allocs, shapes = summarize(data, "cli")
    for assign, sh, bundles in allocs:
        print(sh, bundles)
