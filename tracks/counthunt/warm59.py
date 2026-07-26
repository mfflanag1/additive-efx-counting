"""Warm-start (5,9) anneals from the verified (5,8) count-5 winners.

Append a 9th good (a low-value near-floater column) to each count-5 (5,8) instance
and anneal at m=9. The floor should not fall below n=5 (n=4 stayed at 4 for m=8,9,10),
so this seeds the (5,9) search right at the expected floor instead of grinding down
from the g59 count-12 basin.
"""
import json, os, random, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from tracks.counthunt.hunt import anneal, count_and_slack

A = [[32, 4, 10, 60, 8, 3, 16, 11], [42, 3, 57, 50, 51, 1, 5, 10], [54, 12, 4, 27, 3, 20, 18, 11],
     [33, 9, 31, 42, 45, 10, 13, 5], [45, 13, 52, 47, 49, 21, 2, 21]]
B = [[17, 4, 4, 8, 54, 6, 47, 25], [49, 1, 18, 48, 47, 9, 46, 25], [10, 40, 3, 1, 29, 1, 60, 1],
     [45, 1, 6, 32, 31, 6, 28, 12], [29, 4, 10, 58, 49, 3, 44, 28]]


def append_good(base, col):
    return [row + [col[i]] for i, row in enumerate(base)]


def main():
    rng_base = int(sys.argv[1]); steps = int(sys.argv[2]); tag = sys.argv[3]
    rnd = random.Random(rng_base)
    cell = (5, 9)
    state = {"count": 10**9, "values": None}
    seeds = []
    for name, base in (("A", A), ("B", B)):
        # a few 9th-good columns: universal small (floater), moderate, random
        seeds.append((f"{name}-lo", append_good(base, [rnd.randint(1, 4) for _ in range(5)])))
        seeds.append((f"{name}-mid", append_good(base, [rnd.randint(10, 30) for _ in range(5)])))
        seeds.append((f"{name}-rnd", append_good(base, [rnd.randint(1, 60) for _ in range(5)])))
    import time
    t0 = time.time()
    results = []
    for r, (name, seed) in enumerate(seeds):
        c0, _, _ = count_and_slack(seed)
        best, bc, bo = anneal(seed, 9, steps, rng_base * 1000 + r, cell, state)
        results.append((name, c0, bc, best))
        print(f"[{tag}] seed={name} start={c0} -> best={bc} obj={bo:.3f} ({time.time()-t0:.0f}s) "
              f"values={json.dumps(best)}", flush=True)
        if bc < 5:
            print(f"[{tag}] *** SUB-5 (5,9) {json.dumps(best)}", flush=True)
            break
    results.sort(key=lambda x: x[2])
    print(f"[{tag}] DONE best_count={results[0][2]} seed={results[0][0]} "
          f"values={json.dumps(results[0][3])}", flush=True)


if __name__ == "__main__":
    main()
