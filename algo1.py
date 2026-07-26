"""Implement Neoh-Teh Algorithm 1 (m=n+2) and a naive m=n+3 variant, to LOCATE the break.

Algorithm 1 (m=n+2): n-1 greedy singletons; pool P (3 goods); give the '2-good virtual l'
to the empty agent; envy-cycle-eliminate to a non-envied agent i; give i the 'min virtual
s'; realize. We check the produced allocation is EFX0 on random (n, n+2) instances.

m=n+3 naive variant: n greedy singletons; pool P (3 goods); place l/s on ENDOWED agents.
We check how often the produced allocation is EFX0 and report the failure mode.
"""
import random
from itertools import product
from fast_verify import count_efx0


def tau0(vi, S):
    if not S: return 0
    xs = [vi[g] for g in S]; return sum(xs) - min(xs)


def is_efx0(values, bundles):
    n = len(values)
    own = [sum(values[i][g] for g in bundles[i]) for i in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and own[i] < tau0(values[i], bundles[j]):
                return False
    return True


def envy_graph_source(values, bundles):
    """Return a non-envied agent (no one... rather an agent nobody envies), after
    conceptual envy-cycle elimination. We just look for an agent that is a source of
    the envy graph among the current bundles; if none (cycle), rotate. Returns index."""
    n = len(values)
    own = [sum(values[i][g] for g in bundles[i]) for i in range(n)]
    # envy: i envies j if own[i] < v_i(bundle_j)
    def envied(j):
        return any(own[i] < sum(values[i][g] for g in bundles[j]) for i in range(n) if i != j)
    # try to find a non-envied agent; if all envied there's a cycle -> resolve by picking
    # the agent maximizing own value (welfare source proxy)
    for j in range(n):
        if not envied(j):
            return j
    return max(range(n), key=lambda j: own[j])


def algo1_nplus2(values):
    n = len(values); m = len(values[0]); assert m == n + 2
    P = list(range(m)); bundles = [[] for _ in range(n)]
    for i in range(n - 1):
        g = max(P, key=lambda x: values[i][x])
        bundles[i] = [g]; P.remove(g)
    # P has 3 goods. virtual l = top-2 (per owner-to-be = agent n-1? use agent n-1 view),
    # realize concretely: agent n-1 (empty) gets top-2 of P under its own valuation.
    empty = n - 1
    top2 = sorted(P, key=lambda x: values[empty][x], reverse=True)[:2]
    bundles[empty] = list(top2)
    for g in top2: P.remove(g)
    # State 2: envy-cycle elim -> non-envied agent gets s (the remaining 1 good)
    i = envy_graph_source(values, bundles)
    bundles[i] = bundles[i] + P  # add remaining good(s)
    return bundles


def algo_nplus3_naive(values):
    n = len(values); m = len(values[0]); assert m == n + 3
    P = list(range(m)); bundles = [[] for _ in range(n)]
    for i in range(n):                      # n greedy singletons
        g = max(P, key=lambda x: values[i][x])
        bundles[i] = [g]; P.remove(g)
    # P has 3 goods. Give 'l'=top-2 (under a chosen agent) then 's'=last to non-envied.
    i = envy_graph_source(values, bundles)
    top2 = sorted(P, key=lambda x: values[i][x], reverse=True)[:2]
    bundles[i] = bundles[i] + top2
    for g in top2: P.remove(g)
    j = envy_graph_source(values, bundles)
    bundles[j] = bundles[j] + P
    return bundles


def run(n, m, algo, trials=5000, lo=0):
    rng = random.Random(0)
    ok = 0
    for _ in range(trials):
        v = [[rng.randint(lo, 9) for _ in range(m)] for _ in range(n)]
        b = algo(v)
        if sum(len(x) for x in b) == m and is_efx0(v, b):
            ok += 1
    return ok, trials


if __name__ == "__main__":
    ok, t = run(4, 6, algo1_nplus2)
    print(f"Algorithm 1 at (4,6): produced EFX0 in {ok}/{t} random instances")
    ok, t = run(4, 7, algo_nplus3_naive)
    print(f"naive m=n+3 variant at (4,7): produced EFX0 in {ok}/{t} random instances")
