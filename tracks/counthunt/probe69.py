"""(6,9) probe [m=n+3 at n=6]. Test whether the 'min EFX0 count = n at m=n+3'
pattern extends to n=6. ~10M allocations, ~5.7s per exact count, so a shallow
anneal with strong parking-structured seeds rather than a deep one.

Seeds: 6-agent adaptations of the (5,8) count-5 winner A (a base with one floater
good parking into all agents), plus staircase and random restarts.
"""
import json, math, os, random, sys, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from tracks.counthunt.hunt import count_and_slack, objective, record_elite, VMAX

A5 = [[32, 4, 10, 60, 8, 3, 16, 11], [42, 3, 57, 50, 51, 1, 5, 10], [54, 12, 4, 27, 3, 20, 18, 11],
      [33, 9, 31, 42, 45, 10, 13, 5], [45, 13, 52, 47, 49, 21, 2, 21]]


def distinct_rows(v): return len({tuple(r) for r in v})


def seed_from_A(rnd):
    """Build a (6,9): extend A's 5 rows to 9 goods, add a 6th agent, keep a floater good."""
    rows = [r[:8] + [rnd.randint(1, 30)] for r in A5]      # 9 goods: 8 orig + 1 new
    rows.append([rnd.randint(1, 60) for _ in range(9)])    # 6th agent
    return rows


def stair(n, m, off, rnd, peak=55):
    base = [max(1, min(60, peak - int(peak * k / m) + rnd.randint(-3, 3))) for k in range(m)]
    return [[base[(g - i * off) % m] for g in range(m)] for i in range(n)]


def anneal(seed, steps, rng, state, cell=(6, 9), m=9):
    rnd = random.Random(rng)
    n = len(seed)
    cur = [list(r) for r in seed]
    cnt, sl, _ = count_and_slack(cur); curobj = objective(cnt, sl)
    best, bestcnt, bestobj = [list(r) for r in cur], cnt, curobj
    T0, T1 = 4.0, 0.02
    for t in range(steps):
        T = T0 * (T1 / T0) ** (t / steps)
        trial = [list(r) for r in cur]
        r = rnd.random()
        if r < 0.6:
            i, g = rnd.randrange(n), rnd.randrange(m)
            trial[i][g] = max(1, min(VMAX, trial[i][g] + rnd.choice([-5, -3, -2, -1, 1, 2, 3, 5])))
        elif r < 0.8:
            i, g = rnd.randrange(n), rnd.randrange(m)
            trial[i][g] = rnd.randint(1, VMAX)
        else:
            i = rnd.randrange(n); g1, g2 = rnd.sample(range(m), 2); d = rnd.choice([1, 2, 3, 5])
            trial[i][g1] = max(1, min(VMAX, trial[i][g1] + d))
            trial[i][g2] = max(1, min(VMAX, trial[i][g2] - d))
        if distinct_rows(trial) < n:
            continue
        cnt, sl, _ = count_and_slack(trial); obj = objective(cnt, sl)
        if obj <= curobj or rnd.random() < math.exp((curobj - obj) / max(T, 1e-6)):
            cur, curobj = trial, obj
            if obj < bestobj - 1e-12:
                best, bestcnt, bestobj = [list(r) for r in trial], cnt, obj
                if cnt < state["count"]:
                    state["count"] = cnt; state["values"] = [list(r) for r in trial]
                    record_elite(cell, cnt, state["values"])
                    print(f"  [rng{rng}] NEW ELITE count={cnt} obj={obj:.3f} step={t}", flush=True)
        if bestcnt <= 6:
            print(f"  [rng{rng}] reached count={bestcnt} (=n) step={t}", flush=True)
            if bestcnt < 6:
                break
    return best, bestcnt, bestobj


def main():
    rng_base = int(sys.argv[1]); steps = int(sys.argv[2]); tag = sys.argv[3]
    rnd = random.Random(rng_base)
    state = {"count": 10**9, "values": None}
    seeds = [("A6a", seed_from_A(rnd)), ("A6b", seed_from_A(rnd)),
             ("stair2", stair(6, 9, 2, rnd)), ("stair3", stair(6, 9, 3, rnd)),
             ("rand", [[rnd.randint(1, 60) for _ in range(9)] for _ in range(6)])]
    t0 = time.time(); results = []
    for r, (name, seed) in enumerate(seeds):
        c0, _, _ = count_and_slack(seed)
        best, bc, bo = anneal(seed, steps, rng_base * 1000 + r, state)
        results.append((name, c0, bc, best))
        print(f"[{tag}] seed={name} start={c0} -> best={bc} ({time.time()-t0:.0f}s) values={json.dumps(best)}", flush=True)
        if bc < 6:
            print(f"[{tag}] *** SUB-n (6,9) count={bc} {json.dumps(best)}", flush=True); break
    results.sort(key=lambda x: x[2])
    print(f"[{tag}] DONE best_count={results[0][2]} seed={results[0][0]} values={json.dumps(results[0][3])}", flush=True)


if __name__ == "__main__":
    main()
