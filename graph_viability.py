"""Viability test for the graph (non-hypergraph) join-graph approach at (4,7).

Build H from EFX0 allocations of shape 4111 and 3211 only:
  - 4111 -> self-loop on the agent holding 4 goods
  - 3211 -> directed edge (i=holder-of-3, j=holder-of-2)
Check across many instances:
  (Q1) every agent has degree>=1 in H  [Lemma-3.9 analog viable]
  (Q2) |E(H)| >= 4                     [counting >=n viable without 2-2-2]
Also report: instances where the FULL EFX0 count is 4 but H (4111/3211 only) has
             |E|<4 => 2-2-2 is essential there.
"""
import random, math
from collections import Counter as Ctr
from fast47 import Counter
from shape_analysis import all_efx0

N, M = 4, 7
C = Counter(N, M)
seed8 = [[8,20,1,4,1,16,1],[49,32,2,16,2,60,1],[28,59,1,60,7,46,8],[12,24,1,59,1,17,1]]


def build_H(allocs):
    edges = set()          # (i,j) with i!=j for 3211; (i,i) for 4111
    for assign, shape, bundles in allocs:
        sizes = [len(b) for b in bundles]
        if shape == (4, 1, 1, 1):
            i = sizes.index(4); edges.add((i, i))
        elif shape == (3, 2, 1, 1):
            i = sizes.index(3); j = sizes.index(2); edges.add((i, j))
    deg = [0] * N
    for (i, j) in edges:
        deg[i] += 1
        if i != j: deg[j] += 1
    return edges, deg


def anneal(rng, iters, scale, seed_inst=None):
    vals = [r[:] for r in seed_inst] if seed_inst else [[rng.randint(1, scale) for _ in range(M)] for _ in range(N)]
    cur = C.count(vals); best = cur; bestv = [r[:] for r in vals]
    T = 2.5
    for _ in range(iters):
        i = rng.randrange(N); j = rng.randrange(M)
        old = vals[i][j]; vals[i][j] = rng.randint(0, scale)
        c = C.count(vals)
        if c <= cur or rng.random() < math.exp((cur - c) / max(T, 0.01)):
            cur = c
            if c < best: best = c; bestv = [r[:] for r in vals]
        else:
            vals[i][j] = old
        T *= 0.9997
    return best, bestv


rng = random.Random(7)
q1_fail = []   # some agent has degree 0 in H
q2_fail = []   # |E(H)| < 4
tight_needs222 = []
tested = 0
mincount = 999

# mix random + directed-tight instances
insts = []
for _ in range(3000):
    insts.append([[rng.randint(0, 12) for _ in range(M)] for _ in range(N)])
for t in range(60):
    _, v = anneal(rng, iters=2500, scale=random.choice([40, 70]), seed_inst=(seed8 if t % 2 == 0 else None))
    insts.append(v)

for v in insts:
    total = C.count(v)
    if total == 0:
        print("!!! EFX0-FREE INSTANCE (would break Mahara):", v); continue
    mincount = min(mincount, total)
    allocs = all_efx0(v)
    edges, deg = build_H(allocs)
    tested += 1
    if min(deg) == 0:
        q1_fail.append((v, deg, total))
    if len(edges) < 4:
        q2_fail.append((v, len(edges), total))
    if total == 4 and len(edges) < 4:
        tight_needs222.append((v, len(edges)))

print(f"tested {tested} instances; min full EFX0 count seen = {mincount}")
print(f"Q1 (every agent deg>=1 in H): {tested - len(q1_fail)}/{tested} pass")
print(f"Q2 (|E(H)|>=4):               {tested - len(q2_fail)}/{tested} pass")
print(f"tight(count=4) instances needing 2-2-2 (H has <4 edges): {len(tight_needs222)}")
for v, ne in tight_needs222[:5]:
    print("   NEEDS222", ne, v)
for v, deg, tot in q1_fail[:5]:
    print("   Q1FAIL deg", deg, "total", tot, v)
