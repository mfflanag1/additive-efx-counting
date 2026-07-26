"""Exhaustive local intensifier around a best-so-far instance.

Given a starting instance, repeatedly scan the FULL single-cell neighbourhood
(every (agent,good) set to every value 1..60) and take the move that most
improves the surrogate objective (count, then total slack). Also scans coupled
2-cell within-row shifts. Greedy best-improvement descent to a local optimum;
optional random kicks to escape. Meant to squeeze the last few counts after
annealing plateaus, where a fine full-neighbourhood sweep beats stochastic moves.

Usage: python3 intensify.py <m> '<json instance>' [kicks] [tag]
"""
import json, os, random, sys, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from tracks.counthunt.hunt import count_and_slack, objective, record_elite, distinct_rows

VMAX = 60


def best_single_cell(v, m, cur_obj):
    """Return (best_trial, best_count, best_obj) over all single-cell resets."""
    n = len(v)
    best = None
    for i in range(n):
        orig = v[i][:]
        for g in range(m):
            for val in range(1, VMAX + 1):
                if val == orig[g]:
                    continue
                v[i][g] = val
                if distinct_rows(v) < 5:
                    continue
                c, s, _ = count_and_slack(v)
                o = objective(c, s)
                if best is None or o < best[2]:
                    best = ([row[:] for row in v], c, o)
            v[i][g] = orig[g]
    return best


def main():
    m = int(sys.argv[1]); inst = json.loads(sys.argv[2])
    kicks = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    tag = sys.argv[4] if len(sys.argv) > 4 else "intens"
    cell = (5, m)
    rnd = random.Random(hash(tag) & 0xffff)
    cur = [r[:] for r in inst]
    c, s, _ = count_and_slack(cur)
    best_obj = objective(c, s)
    best_c = c
    best_inst = [r[:] for r in cur]
    print(f"[{tag}] start count={c} obj={best_obj:.3f}", flush=True)
    t0 = time.time()
    for k in range(kicks + 1):
        # greedy best-improvement descent to local optimum
        while True:
            cand = best_single_cell(cur, m, objective(*count_and_slack(cur)[:2]))
            if cand is None:
                break
            ti, tc, to = cand
            cur_c, cur_s, _ = count_and_slack(cur)
            if to < objective(cur_c, cur_s) - 1e-12:
                cur = ti
                if tc < best_c or (tc == best_c and to < best_obj):
                    if tc < best_c:
                        record_elite(cell, tc, ti)
                        print(f"[{tag}] NEW ELITE count={tc} obj={to:.3f} ({time.time()-t0:.0f}s)", flush=True)
                    best_c, best_obj, best_inst = tc, to, [r[:] for r in ti]
                if tc < 5:
                    print(f"[{tag}] *** SUB-5 {json.dumps(ti)}", flush=True)
                    return
            else:
                break
        print(f"[{tag}] local-opt count={best_c} obj={best_obj:.3f} kick {k}/{kicks} ({time.time()-t0:.0f}s) "
              f"values={json.dumps(best_inst)}", flush=True)
        # random kick from best
        cur = [r[:] for r in best_inst]
        for _ in range(rnd.randint(2, 4)):
            i, g = rnd.randrange(5), rnd.randrange(m)
            cur[i][g] = rnd.randint(1, VMAX)
        if distinct_rows(cur) < 5:
            cur = [r[:] for r in best_inst]
    print(f"[{tag}] DONE best_count={best_c} values={json.dumps(best_inst)}", flush=True)


if __name__ == "__main__":
    main()
