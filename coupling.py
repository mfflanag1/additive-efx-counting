"""Coupling-conjecture sweep + cycle-rotation mechanism test.

For random 4-agent instances, find EFX0 bases B of M\\{f} that are UN-PARKABLE
(f-envy sourceless: every placement of f detonates). For each such (V,B,f):
  - Does the FULL instance have ANY EFX0 allocation? (NO => COUNTEREXAMPLE)
  - Does cycle-rotation of B recover an EFX0 allocation (rotated base + park f)?
Iterated rotation: keep eliminating envy cycles (Lipton) until acyclic or EFX0 found.
"""
import sys, random
sys.path.insert(0, ".")
from verify import precompute, check_allocation, enumerate_all
from genpark import vv, f_envy_sources


def is_efx0_base(V, B, n, m):
    val, minall, minpos = precompute(n, m, V)
    bd = [0] * n
    for a in range(n):
        for g in B[a]:
            bd[a] |= 1 << g
    return check_allocation(n, bd, val, minall, minpos)[0]


def park_placements(V, B, f, n, m):
    val, minall, minpos = precompute(n, m, V)
    good = []
    for i in range(n):
        assign = [None] * m
        for a in range(n):
            for g in B[a]:
                assign[g] = a
        assign[f] = i
        bd = [0] * n
        for g, a in enumerate(assign):
            bd[a] |= 1 << g
        if check_allocation(n, bd, val, minall, minpos)[0]:
            good.append(i)
    return good


def envy_edges(V, B):
    n = len(B)
    return [[i != j and vv(V, i, B[i]) < vv(V, i, B[j]) for j in range(n)] for i in range(n)]


def find_cycle(E):
    n = len(E)
    for start in range(n):
        stack = [(start, [start])]
        while stack:
            u, path = stack.pop()
            for v in range(n):
                if E[u][v]:
                    if v == start and len(path) >= 2:
                        return path
                    if v not in path:
                        stack.append((v, path + [v]))
    return None


def rotate(B, cyc):
    B2 = [b[:] for b in B]
    for idx in range(len(cyc)):
        a = cyc[idx]; nxt = cyc[(idx + 1) % len(cyc)]
        B2[a] = B[nxt][:]
    return B2


def rotation_recovers(V, B, f, n, m, max_iter=12):
    """Iterated envy-cycle rotation; return True if some rotated base parks f EFX0."""
    cur = [b[:] for b in B]
    for _ in range(max_iter):
        if park_placements(V, cur, f, n, m):
            return True
        E = envy_edges(V, cur)
        cyc = find_cycle(E)
        if cyc is None:
            return bool(park_placements(V, cur, f, n, m))
        cur = rotate(cur, cyc)
    return bool(park_placements(V, cur, f, n, m))


def sweep(trials, n=4, m=8, vmax=25, seed=1):
    rng = random.Random(seed)
    unpark = 0
    rot_ok = 0
    full_has_efx0 = 0
    counterexamples = []
    rot_fail = []
    for t in range(trials):
        V = [[rng.randint(1, vmax) for _ in range(m)] for _ in range(n)]
        for f in range(m):
            rest = [g for g in range(m) if g != f]
            # try a few random EFX0 bases of M\\{f}
            for _ in range(30):
                B = [[] for _ in range(n)]
                for g in rest:
                    B[rng.randrange(n)].append(g)
                if not all(B):  # need every agent nonempty for a proper base
                    continue
                if not is_efx0_base(V, B, n, m):
                    continue
                if park_placements(V, B, f, n, m):
                    continue  # parkable -> not the hard case
                # UN-PARKABLE base found
                unpark += 1
                full = enumerate_all(n, m, V, collect=1)
                if full["efx0_exists"]:
                    full_has_efx0 += 1
                else:
                    counterexamples.append((V, B, f))
                if rotation_recovers(V, B, f, n, m):
                    rot_ok += 1
                else:
                    if len(rot_fail) < 8:
                        rot_fail.append((V, B, f))
                break  # one un-parkable base per (V,f) is enough
    return unpark, rot_ok, full_has_efx0, counterexamples, rot_fail


if __name__ == "__main__":
    import json
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    unpark, rot_ok, full, cex, rf = sweep(trials)
    print(f"un-parkable bases found: {unpark}")
    print(f"full instance HAS EFX0 elsewhere: {full}/{unpark}")
    print(f"cycle-rotation recovers EFX0: {rot_ok}/{unpark}")
    print(f"COUNTEREXAMPLES (un-parkable base, NO EFX0 anywhere): {len(cex)}")
    for c in cex[:5]:
        print("  *** CEX ***", json.dumps(c[0]), "base", c[1], "f", c[2])
    print(f"rotation-FAILED cases (EFX0 exists but rotation missed it): {len(rf)}")
    for c in rf[:8]:
        print("  rotfail", json.dumps(c[0]), "base", c[1], "f", c[2])
