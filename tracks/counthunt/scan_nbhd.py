"""Exhaustive radius-1 neighbourhood histogram around a count-5 instance.

Move set: every single cell (agent i, good g) reset to every value in 1..60
(excluding the original), keeping >=5 distinct rows. 5*8*59 = 2360 neighbours.
Reports the full EFX0-count distribution over the neighbourhood and the min count
(any neighbour with count <= 4 is a refutation and is printed immediately).

Usage: python3 scan_nbhd.py <name> '<json instance>'
"""
import json, sys, os
from collections import Counter
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from tracks.counthunt.hunt import count_and_slack, distinct_rows

VMAX = 60


def main():
    name = sys.argv[1]; V = json.loads(sys.argv[2])
    n, m = len(V), len(V[0])
    base_c, base_s, _ = count_and_slack(V)
    hist = Counter()
    minc = base_c; minarg = None
    nbrs = 0
    for i in range(n):
        orig = V[i][:]
        for g in range(m):
            for val in range(1, VMAX + 1):
                if val == orig[g]:
                    continue
                V[i][g] = val
                if distinct_rows(V) < 5:
                    continue
                c, s, _ = count_and_slack(V)
                hist[c] += 1
                nbrs += 1
                if c < minc:
                    minc = c; minarg = ([r[:] for r in V], i, g, val)
                if c <= 4:
                    print(f"[{name}] *** COUNT<=4 NEIGHBOUR c={c} cell=({i},{g}) val={val} "
                          f"{json.dumps([r[:] for r in V])}", flush=True)
            V[i][g] = orig[g]
    print(f"[{name}] base_count={base_c} neighbours={nbrs} min_neighbour_count={minc}", flush=True)
    print(f"[{name}] count histogram (count: #neighbours): "
          f"{json.dumps(dict(sorted(hist.items())))}", flush=True)
    if minarg:
        print(f"[{name}] best neighbour @cell{minarg[1:]}: {json.dumps(minarg[0])}", flush=True)


if __name__ == "__main__":
    main()
