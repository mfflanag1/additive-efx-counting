"""Construct a (6,9) parking instance to test whether min EFX0 count = n = 6.

Rather than a deep anneal (5.7s/exact count is prohibitive at 10M allocations),
sweep hand-structured parking instances: a 6-agent envy-free base of 8 fixed
singleton/small bundles plus one universally-parkable floater good. Cap-accelerated
counting (cap=40) prunes high-count combos fast; the best few are exact-counted.
"""
import json, os, sys, time, random, itertools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from fast_verify import count_efx0
from tracks.counthunt.hunt import record_elite

CAP = 40


def build(assign_owner, floater_g, base_hi, filler, floater_vals, dom8):
    """9 goods, 6 agents. assign_owner: dict good->owner for the 8 fixed goods.
    floater_g valued floater_vals[i] by agent i; agent i's own fixed goods get base_hi,
    others get filler; good8 is agent5's dominant singleton (dom8)."""
    n, m = 6, 9
    V = [[filler] * m for _ in range(n)]
    for g, o in assign_owner.items():
        for i in range(n):
            V[i][g] = base_hi if i == o else filler
    for i in range(n):
        V[i][floater_g] = floater_vals[i]
    for i in range(n):
        V[i][8] = dom8 if i == 5 else filler
    return V


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else "c69"
    rnd = random.Random(7)
    # fixed owners for goods 0..7 (good6 = floater, good8 = agent5 singleton)
    # give each of agents 0..4 some singletons; agent5 gets good8.
    owner_maps = [
        {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 0, 7: 1},   # agents 0,1 get 2 goods
        {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 7: 3},
        {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 2, 7: 0},
    ]
    best = None
    t0 = time.time(); tested = 0
    for om in owner_maps:
        for base_hi in (40, 50, 60):
            for filler in (1, 2, 3):
                for fv in (8, 12, 16, 20, 26):
                    for dom8 in (40, 55, 60):
                        floater_vals = [fv] * 6
                        V = build(om, 6, base_hi, filler, floater_vals, dom8)
                        c, _ = count_efx0(V, cap=CAP)
                        tested += 1
                        if best is None or c < best[0]:
                            best = (c, [r[:] for r in V])
                            print(f"[{tag}] new best capped={c} ({time.time()-t0:.0f}s) "
                                  f"base_hi={base_hi} filler={filler} fv={fv} dom8={dom8}", flush=True)
    # exact-count the best
    bc = best[0]
    if bc < CAP:
        exact, _ = count_efx0(best[1])
        print(f"[{tag}] BEST exact (6,9) count={exact} values={json.dumps(best[1])}", flush=True)
        if exact <= 6:
            record_elite((6, 9), exact, best[1])
    else:
        print(f"[{tag}] BEST capped at {CAP} (all constructions >= {CAP}); values={json.dumps(best[1])}", flush=True)
    print(f"[{tag}] tested={tested} time={time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
