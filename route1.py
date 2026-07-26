"""Route 1: edit-distance structure of EFX0 recovery in rotation-FAIL un-parkable configs.

For random instances, find un-parkable EFX0 bases B of M\\{f} where iterated envy-cycle
rotation FAILS to recover EFX0. For each, enumerate all EFX0 allocations of the full
instance and measure the minimum Hamming distance (# goods reassigned) from the base
(with f placed in its least-bad spot) to a genuine EFX0 allocation. Report the distribution
and the move pattern (which goods move, whether one agent's bundle splits).
"""
import sys, random, json
sys.path.insert(0, ".")
from verify import precompute, check_allocation
from coupling_fast import bmask, efx0, park_places, envy_edges, find_cycle, rotate


def base_assign(B, f, n, m, fspot):
    a = [None] * m
    for ag in range(n):
        for g in B[ag]:
            a[g] = ag
    a[f] = fspot
    return a


def all_efx0_assigns(V, n, m, tabs):
    out = []
    assign = [0] * m
    while True:
        bd = [0] * n
        for g in range(m):
            bd[assign[g]] |= 1 << g
        if check_allocation(n, bd, tabs[0], tabs[1], tabs[2])[0]:
            out.append(assign[:])
        g = 0
        while g < m:
            assign[g] += 1
            if assign[g] < n:
                break
            assign[g] = 0
            g += 1
        else:
            break
    return out


def rot_fails(V, B, f, n, m, tabs, mx=12):
    cur = [b[:] for b in B]
    for _ in range(mx):
        if park_places(V, cur, f, n, m, tabs):
            return False
        c = find_cycle(envy_edges(V, cur))
        if c is None:
            return not park_places(V, cur, f, n, m, tabs)
        cur = rotate(cur, c)
    return not park_places(V, cur, f, n, m, tabs)


def hamming(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)


def run(trials, n=4, m=8, vmax=25, seed=3):
    rng = random.Random(seed)
    dist_hist = {}
    move_patterns = {}
    nfail = 0
    examples = []
    for t in range(trials):
        V = [[rng.randint(1, vmax) for _ in range(m)] for _ in range(n)]
        tabs = precompute(n, m, V)
        efx0_allocs = None
        for f in range(m):
            rest = [g for g in range(m) if g != f]
            for _ in range(25):
                B = [[] for _ in range(n)]
                for g in rest:
                    B[rng.randrange(n)].append(g)
                if not all(B):
                    continue
                if not efx0(bmask(B, n), n, tabs):
                    continue
                if park_places(V, B, f, n, m, tabs):
                    continue
                if not rot_fails(V, B, f, n, m, tabs):
                    continue
                # rotation-fail un-parkable base
                if efx0_allocs is None:
                    efx0_allocs = all_efx0_assigns(V, n, m, tabs)
                if not efx0_allocs:
                    print("*** NO EFX0 (CEX) ***", json.dumps(V), "base", B, "f", f, flush=True)
                    break
                # min hamming over f-spots and EFX0 allocs
                best = 99
                bestA = None
                for fs in range(n):
                    ba = base_assign(B, f, n, m, fs)
                    for A in efx0_allocs:
                        d = hamming(ba, A)
                        if d < best:
                            best = d; bestA = A; bestba = ba
                nfail += 1
                dist_hist[best] = dist_hist.get(best, 0) + 1
                # move pattern: goods that differ
                moved = tuple(g for g in range(m) if bestba[g] != bestA[g])
                move_patterns[len(moved)] = move_patterns.get(len(moved), 0) + 1
                if len(examples) < 6:
                    examples.append((best, bestba, bestA, V, B, f))
                break
            if efx0_allocs is not None:
                break
    print(f"rotation-FAIL un-parkable configs: {nfail}")
    print(f"min-Hamming(base->nearest EFX0) histogram: {dict(sorted(dist_hist.items()))}")
    print(f"#goods-moved histogram: {dict(sorted(move_patterns.items()))}")
    for e in examples:
        print(f"  dist={e[0]} base_assign={e[1]} nearestEFX0={e[2]}")
    return nfail, dist_hist


if __name__ == "__main__":
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 3000)
