"""Gather LOW-count (4,7) instances via directed anneal; for each, record total count,
the shape multiset of its EFX0 allocations, and |E(H)| for the 4111/3211 graph.

Central question for the lower-bound proof: among instances whose total count is small
(4,5,6), can >=4 allocations always be found within {4111,3211}, or is 2221 essential
to reach the floor of 4?
"""
import random, math, json
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
    return edges


def anneal(rng, iters, scale, seed_inst=None):
    vals = [r[:] for r in seed_inst] if seed_inst else [[rng.randint(1, scale) for _ in range(M)] for _ in range(N)]
    cur = C.count(vals); best = cur; bestv = [r[:] for r in vals]
    T = 2.0
    for _ in range(iters):
        i = rng.randrange(N); j = rng.randrange(M)
        old = vals[i][j]; vals[i][j] = rng.randint(0, scale)
        c = C.count(vals)
        if c <= cur or rng.random() < math.exp((cur - c) / max(T, 0.01)):
            cur = c
            if c < best: best = c; bestv = [r[:] for r in vals]
        else:
            vals[i][j] = old
        T *= 0.9996
    return best, bestv


rng = random.Random(2027)
low = {}          # total_count -> Counter of shape-combos
h_lt4_lowcount = []   # (v,total,|E|) where total<=6 but |E(H)|<4  => 2221 essential to reach floor
essential222 = []     # count-4 instances that INCLUDE a 2221 among their 4
sub4 = []
collected = 0
for t in range(400):
    si = seed8 if t % 4 == 0 else (tight if t % 4 == 1 else None)
    b, v = anneal(rng, 1000, random.choice([30, 50, 80, 120]), seed_inst=si)
    A = C.allocs(v)
    total = len(A)
    if total < 4:
        sub4.append((total, v))
    if total <= 6:
        collected += 1
        shapes = tuple(sorted(Ctr(sh for _, sh in A).items()))
        low.setdefault(total, Ctr())[shapes] += 1
        E = build_H(A)
        if len(E) < 4:
            h_lt4_lowcount.append((v, total, len(E), shapes))
        if total == 4 and any(sh == (2, 2, 2, 1) for _, sh in A):
            essential222.append((v, shapes))

print(f"collected {collected} low-count (<=6) instances")
print(f"SUB-4 instances: {len(sub4)}")
for tt, v in sub4[:5]:
    print("   SUB4", tt, json.dumps(v))
print(f"\nlow-count instances with |E(H_4111/3211)| < 4: {len(h_lt4_lowcount)}")
for v, tot, ne, shapes in h_lt4_lowcount[:10]:
    print(f"   total={tot} |E|={ne} shapes={shapes} v={json.dumps(v)}")
print(f"\ncount-4 instances whose 4 forced allocs INCLUDE a 2221: {len(essential222)}")
for v, shapes in essential222[:5]:
    print("   ", shapes, json.dumps(v))
print("\nshape-combo distribution by total count:")
for tot in sorted(low):
    print(f" total={tot}:")
    for shapes, c in low[tot].most_common():
        print(f"     x{c}  {shapes}")
