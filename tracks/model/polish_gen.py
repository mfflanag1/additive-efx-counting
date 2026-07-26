"""Exhaustive-neighborhood greedy descent for arbitrary (n,m) low-count seeds.
Single-cell retargets + coupled 2-cell row moves; best by (count, objective) until stuck.
Search heuristic; re-verify hits officially. Usage: python3 polish_gen.py <n> <m> <seed_json> [cap]"""
import json, sys
from tracks.model.fastcount import Counter


def distinct_rows(v): return len({tuple(r) for r in v})
def distinct_vals(v): return len({x for r in v for x in r})
def valid(v, n): return distinct_rows(v) == n and distinct_vals(v) >= 3


def polish(seed, n, m, cap=100, max_sweeps=30):
    C = Counter(n, m)
    cur = [list(r) for r in seed]
    curcnt, curobj = C.efx0_objective(cur)
    for sweep in range(max_sweeps):
        best = None
        for i in range(n):
            for g in range(m):
                old = cur[i][g]
                for nv in range(1, cap + 1):
                    if nv == old:
                        continue
                    cur[i][g] = nv
                    if valid(cur, n):
                        cnt, obj = C.efx0_objective(cur)
                        if best is None or (cnt, obj) < (best[0], best[1]):
                            best = (cnt, obj, ("s", i, g, nv))
                cur[i][g] = old
        for i in range(n):
            for g1 in range(m):
                for g2 in range(m):
                    if g1 == g2:
                        continue
                    for d in (1, 2, 3, 5, 8, 12):
                        o1, o2 = cur[i][g1], cur[i][g2]
                        n1, n2 = min(cap, o1 + d), max(1, o2 - d)
                        if n1 == o1 and n2 == o2:
                            continue
                        cur[i][g1], cur[i][g2] = n1, n2
                        if valid(cur, n):
                            cnt, obj = C.efx0_objective(cur)
                            if best is None or (cnt, obj) < (best[0], best[1]):
                                best = (cnt, obj, ("c", i, g1, g2, n1, n2))
                        cur[i][g1], cur[i][g2] = o1, o2
        if best is None or (best[0], best[1]) >= (curcnt, curobj):
            break
        mv = best[2]
        if mv[0] == "s":
            _, i, g, nv = mv; cur[i][g] = nv
        else:
            _, i, g1, g2, n1, n2 = mv; cur[i][g1], cur[i][g2] = n1, n2
        curcnt, curobj = best[0], best[1]
        print(f"sweep {sweep}: count={curcnt} obj={curobj:.3f}", flush=True)
        if curcnt == 0:
            break
    return cur, curcnt, curobj


if __name__ == "__main__":
    n = int(sys.argv[1]); m = int(sys.argv[2]); seed = json.loads(sys.argv[3])
    cap = int(sys.argv[4]) if len(sys.argv) > 4 else 100
    best, cnt, obj = polish(seed, n, m, cap)
    print(json.dumps({"n": n, "m": m, "best": cnt, "obj": round(obj, 3), "values": best,
                      "distinct_rows": distinct_rows(best), "distinct_vals": distinct_vals(best)}))
