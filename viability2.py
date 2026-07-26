"""Fast viability test: is the 2-2-2 (2221) shape ever ESSENTIAL at (4,7)?

Build H from EFX0 allocations of shape 4111 (self-loop on the 4-agent) and 3211
(edge holder-of-3 -> holder-of-2). Across many instances (random + directed-tight),
check:
  Q1  every agent has degree>=1 in H
  Q2  |E(H)| >= 4
  and flag any count-4 instance whose H has <4 edges (=> 2221 essential there),
  and any EFX0-free instance (would contradict Mahara).
Also tally, for count-exactly-4 instances, the multiset of the 4 forced shapes.
"""
import random, math
from collections import Counter as Ctr
from fast47 import Counter

N, M = 4, 7
C = Counter(N, M)
seed8 = [[8,20,1,4,1,16,1],[49,32,2,16,2,60,1],[28,59,1,60,7,46,8],[12,24,1,59,1,17,1]]
tight = [[30,66,69,9,21,19,63],[12,56,58,9,10,24,52],[12,33,45,20,24,8,64],[11,60,1,18,2,6,41]]


def build_H(allocs):
    edges = set()
    for bundles, shape in allocs:
        sizes = [len(b) for b in bundles]
        if shape == (4, 1, 1, 1):
            edges.add((sizes.index(4), sizes.index(4)))
        elif shape == (3, 2, 1, 1):
            edges.add((sizes.index(3), sizes.index(2)))
    deg = [0] * N
    for (i, j) in edges:
        deg[i] += 1
        if i != j:
            deg[j] += 1
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
insts = [[[rng.randint(0, 12) for _ in range(M)] for _ in range(N)] for _ in range(8000)]
# add all-distinct-value random too
for _ in range(2000):
    pool = random.sample(range(1, 200), M)
    insts.append([random.sample(range(1, 200), M) for _ in range(N)])
# directed-tight
for t in range(200):
    _, v = anneal(rng, 1500, random.choice([40, 70, 100]),
                  seed_inst=(seed8 if t % 3 == 0 else (tight if t % 3 == 1 else None)))
    insts.append(v)

q1_fail = q2_fail = needs222 = efxfree = 0
mincount = 999
combo_ctr = Ctr()
uses222_any = 0
q1ex = q2ex = None
for v in insts:
    allocs = C.allocs(v)
    total = len(allocs)
    if total == 0:
        efxfree += 1; print("EFX0-FREE:", v); continue
    mincount = min(mincount, total)
    edges, deg = build_H(allocs)
    if min(deg) == 0:
        q1_fail += 1; q1ex = q1ex or (v, deg, total)
    if len(edges) < 4:
        q2_fail += 1; q2ex = q2ex or (v, len(edges), total)
    if any(sh == (2, 2, 2, 1) for _, sh in allocs):
        uses222_any += 1
    if total == 4:
        combo = tuple(sorted(sh for _, sh in allocs))
        combo_ctr[combo] += 1
        if len(edges) < 4:
            needs222 += 1
            print("TIGHT NEEDS 2221 (H<4 edges):", len(edges), v)

n = len(insts)
print(f"\ntested {n} instances; min EFX0 count = {mincount}; EFX0-free = {efxfree}")
print(f"Q1 every-agent-deg>=1 in H(4111+3211): {n - q1_fail}/{n} pass")
print(f"Q2 |E(H)|>=4:                          {n - q2_fail}/{n} pass")
print(f"instances having ANY 2221 EFX0 alloc:  {uses222_any}")
print(f"count-4 instances that REQUIRE 2221:   {needs222}")
if q1ex: print("Q1 fail example:", q1ex)
if q2ex: print("Q2 fail example:", q2ex)
print("\ncount-4 forced-shape combos:")
for combo, c in combo_ctr.most_common():
    print("   ", combo, "x", c)
