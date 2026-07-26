"""Driver: run multiple surrogate-anneal restarts for one (5,m) cell.

Usage: python3 driver.py <m> <rng_base> <n_runs> <steps> [tag]
Seeds cycle through: lifted n=4 count-4 winners + 5th row, trackB g59 count-12,
n=5 staircase rotations, treasure structures, and random restarts.
"""
import json, os, random, sys, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from tracks.counthunt.hunt import anneal, count_and_slack, ELITES

# n=4 count-4 dual-verified winners (CAMPAIGN_LOG / tracks/model/elites.jsonl)
N4_C4_M8 = [[11, 8, 20, 1, 4, 1, 16, 1], [16, 49, 32, 2, 16, 2, 60, 1],
            [28, 28, 59, 1, 60, 7, 46, 8], [10, 12, 24, 1, 59, 1, 17, 1]]
N4_C4_M9 = [[1, 57, 58, 6, 60, 7, 19, 14, 15], [1, 57, 11, 12, 4, 12, 1, 21, 10],
            [4, 59, 60, 2, 23, 3, 28, 8, 12], [8, 48, 57, 1, 58, 34, 1, 1, 3]]
# trackB (5,9) count-12
G59 = [[45, 1, 7, 36, 43, 13, 10, 1, 35], [41, 1, 17, 35, 34, 1, 9, 17, 45],
       [42, 10, 6, 34, 35, 6, 1, 9, 33], [32, 1, 8, 32, 16, 15, 5, 5, 31],
       [19, 10, 5, 43, 45, 1, 1, 7, 30]]


def staircase(n, m, offset, rnd, peak=55):
    """Rotated decreasing profile: agent i's peak good is (i*offset) mod m."""
    base = [max(1, peak - int(peak * k / m) + rnd.randint(-3, 3)) for k in range(m)]
    base = [max(1, min(60, x)) for x in base]
    rows = []
    for i in range(n):
        sh = (i * offset) % m
        rows.append([base[(g - sh) % m] for g in range(m)])
    return rows


def treasure(n, m, rnd):
    """k high 'treasure' goods each agent contests, remainder near-min filler."""
    rows = []
    ntreas = min(n, m // 2)
    for i in range(n):
        row = [rnd.randint(1, 4) for _ in range(m)]
        for t in range(ntreas):
            row[t] = rnd.randint(40, 60)
        rows.append(row)
    return rows


def lift4(base4, m, rnd, mode):
    """Add a 5th agent row to a 4-agent instance."""
    rows = [list(r) for r in base4]
    rows = [(r + [rnd.randint(1, 60)] * (m - len(r)))[:m] for r in rows]
    if mode == "avg":
        r5 = [max(1, min(60, sum(rows[i][g] for i in range(4)) // 4 + rnd.randint(-4, 4))) for g in range(m)]
    elif mode == "shift":
        r5 = [rows[(g) % 4][g] for g in range(m)]
    else:
        r5 = [rnd.randint(1, 60) for _ in range(m)]
    rows.append(r5)
    return rows


def make_seeds(m, rnd, k):
    seeds = []
    base4 = N4_C4_M8 if m <= 8 else N4_C4_M9
    # fresh descent-friendly seeds FIRST (these drove 294->5 at (5,8)); g59 basin last.
    for off in (2, 3, 1):
        seeds.append((f"stair-o{off}", staircase(5, m, off, rnd)))
    seeds.append(("treasure", treasure(5, m, rnd)))
    seeds.append(("lift-avg", lift4(base4, m, rnd, "avg")))
    seeds.append(("lift-shift", lift4(base4, m, rnd, "shift")))
    seeds.append(("lift-rand", lift4(base4, m, rnd, "rand")))
    if m == 9:
        seeds.append(("g59", [r[:m] for r in G59]))
    while len(seeds) < k:
        seeds.append((f"rand{len(seeds)}", [[rnd.randint(1, 60) for _ in range(m)] for _ in range(5)]))
    return seeds[:k]


def main():
    m = int(sys.argv[1]); rng_base = int(sys.argv[2])
    n_runs = int(sys.argv[3]); steps = int(sys.argv[4])
    tag = sys.argv[5] if len(sys.argv) > 5 else "run"
    cell = (5, m)
    rnd = random.Random(rng_base)
    seeds = make_seeds(m, rnd, n_runs)
    # cross-run best; init from current best-known so elites only fire on genuine improvement
    state = {"count": 10**9, "values": None}
    t0 = time.time()
    print(f"[{tag}] cell={cell} runs={n_runs} steps={steps}", flush=True)
    results = []
    for r, (name, seed) in enumerate(seeds):
        rng = rng_base * 1000 + r
        c0, _, _ = count_and_slack(seed)
        best, bc, bo = anneal(seed, m, steps, rng, cell, state)
        results.append((name, c0, bc, best))
        print(f"[{tag}] seed={name} start={c0} -> best={bc} obj={bo:.3f} "
              f"({time.time()-t0:.0f}s) values={json.dumps(best)}", flush=True)
        if bc < 5:
            print(f"[{tag}] *** SUB-5 REFUTATION CANDIDATE at seed {name}: {json.dumps(best)}", flush=True)
            break
    results.sort(key=lambda x: x[2])
    print(f"[{tag}] DONE best_count={results[0][2]} seed={results[0][0]} "
          f"values={json.dumps(results[0][3])} total={time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
