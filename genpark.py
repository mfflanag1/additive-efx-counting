"""Test the GENERALIZED parking lemma and the CYCLE-ROTATION mechanism.

Generalized parking lemma (claim): for ANY leftover good f and EFX0 base B of M\\{f},
  #(EFX0 completions of f into B) = #(sources of the f-envy digraph),
where agent k "f-envies" bundle B_i (k!=i) iff
  v_k(B_k) < v_k(B_i) + max(0, v_k(f) - min_{g in B_i} v_k(g)).
(For a universal-min f this collapses to plain envy v_k(B_k) < v_k(B_i).)
A "source" is a bundle i that no k f-envies. Parking f in B_i is EFX0 iff i is a source.

Cycle-rotation (coupling-conjecture mechanism): if the base's plain-envy digraph is
sourceless, rotate bundles along an envy cycle and test whether any resulting complete
allocation (rotated base + floater parked) is EFX0 -- i.e. whether the alternative EFX0
allocation is reachable by cycle rotation.
"""
import sys, random, itertools
sys.path.insert(0, ".")
from verify import precompute, check_allocation


def vv(V, k, S):
    return sum(V[k][g] for g in S)


def f_envy_sources(V, B, f):
    """Return set of source bundle-indices of the f-envy digraph."""
    n = len(B)
    src = []
    for i in range(n):
        Bi = B[i]
        envied = False
        for k in range(n):
            if k == i:
                continue
            if not Bi:
                mki = 0
            else:
                mki = min(V[k][g] for g in Bi)
            if vv(V, k, B[k]) < vv(V, k, Bi) + max(0, V[k][f] - mki):
                envied = True
                break
        if not envied:
            src.append(i)
    return src


def efx0_completions(V, B, f, n, m):
    """Which placements of f into B give an EFX0 allocation."""
    val, minall, minpos = precompute(n, m, V)
    good = []
    for i in range(n):
        assign = [None] * m
        for a in range(n):
            for g in B[a]:
                assign[g] = a
        assign[f] = i
        bundles = [0] * n
        for g, a in enumerate(assign):
            bundles[a] |= 1 << g
        e0, _ = check_allocation(n, bundles, val, minall, minpos)
        if e0:
            good.append(i)
    return good


def random_base_and_test(rng, n=4, m=8, vmax=20):
    """Random instance; pick a random leftover f and a random EFX0 base of M\\{f}
    if we can find one; test the identity."""
    V = [[rng.randint(1, vmax) for _ in range(m)] for _ in range(n)]
    f = rng.randrange(m)
    rest = [g for g in range(m) if g != f]
    # random partition of rest into n bundles, retry until EFX0 base found (few tries)
    val, minall, minpos = precompute(n, m, V)
    for _ in range(200):
        B = [[] for _ in range(n)]
        for g in rest:
            B[rng.randrange(n)].append(g)
        # EFX0 check on the base (as an allocation of M\\{f}: f unassigned -> treat as empty)
        bundles = [0] * n
        for a in range(n):
            for g in B[a]:
                bundles[a] |= 1 << g
        e0, _ = check_allocation(n, bundles, val, minall, minpos)
        if e0:
            src = f_envy_sources(V, B, f)
            comp = efx0_completions(V, B, f, n, m)
            return (sorted(src) == sorted(comp), V, B, f, src, comp)
    return None


if __name__ == "__main__":
    rng = random.Random(12345)
    ok = fail = tried = 0
    failures = []
    for _ in range(20000):
        r = random_base_and_test(rng)
        if r is None:
            continue
        tried += 1
        if r[0]:
            ok += 1
        else:
            fail += 1
            if len(failures) < 5:
                failures.append(r[1:])
    print(f"GENERALIZED PARKING LEMMA test: {ok}/{tried} match, {fail} mismatches")
    for f in failures:
        print("  MISMATCH", f)
