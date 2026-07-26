"""Exhaustive-neighborhood greedy descent for low-count seeds. Evaluates ALL single-cell
retargets (i,g -> any value in 1..cap) and all coupled 2-cell row moves, takes the best by
(count, objective), repeats until no improvement. Search heuristic; re-verify hits officially.
Usage: python3 polish.py <seed_json> [cap] [m]"""
import json, sys
from tracks.model.fastcount import Counter


def distinct_rows(v): return len({tuple(r) for r in v})
def distinct_vals(v): return len({x for r in v for x in r})
def valid(v): return distinct_rows(v) == 4 and distinct_vals(v) >= 3


def polish(seed, m, cap=100, max_sweeps=40):
    C = Counter(m)
    cur = [list(r) for r in seed]
    curcnt, curobj = C.efx0_objective(cur)
    for sweep in range(max_sweeps):
        best = None  # (cnt, obj, i, g, newval) or coupled
        # single-cell retargets
        for i in range(4):
            for g in range(m):
                old = cur[i][g]
                for nv in range(1, cap + 1):
                    if nv == old:
                        continue
                    cur[i][g] = nv
                    if valid(cur):
                        cnt, obj = C.efx0_objective(cur)
                        if best is None or (cnt, obj) < (best[0], best[1]):
                            best = (cnt, obj, ("s", i, g, nv))
                cur[i][g] = old
        # coupled 2-cell moves within a row
        for i in range(4):
            for g1 in range(m):
                for g2 in range(m):
                    if g1 == g2:
                        continue
                    for d in (1, 2, 3, 4, 5, 8, 12):
                        o1, o2 = cur[i][g1], cur[i][g2]
                        n1, n2 = min(cap, o1 + d), max(1, o2 - d)
                        if n1 == o1 and n2 == o2:
                            continue
                        cur[i][g1], cur[i][g2] = n1, n2
                        if valid(cur):
                            cnt, obj = C.efx0_objective(cur)
                            if best is None or (cnt, obj) < (best[0], best[1]):
                                best = (cnt, obj, ("c", i, g1, g2, n1, n2))
                        cur[i][g1], cur[i][g2] = o1, o2
        if best is None or (best[0], best[1]) >= (curcnt, curobj):
            break  # local optimum
        mv = best[2]
        if mv[0] == "s":
            _, i, g, nv = mv; cur[i][g] = nv
        else:
            _, i, g1, g2, n1, n2 = mv; cur[i][g1], cur[i][g2] = n1, n2
        curcnt, curobj = best[0], best[1]
        print(f"sweep {sweep}: count={curcnt} obj={curobj:.3f} move={mv}", flush=True)
        if curcnt == 0:
            break
    return cur, curcnt, curobj


if __name__ == "__main__":
    seed = json.loads(sys.argv[1])
    cap = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    m = int(sys.argv[3]) if len(sys.argv) > 3 else len(seed[0])
    best, cnt, obj = polish(seed, m, cap)
    print(json.dumps({"best": cnt, "obj": round(obj, 3), "values": best,
                      "distinct_rows": distinct_rows(best), "distinct_vals": distinct_vals(best)}))
