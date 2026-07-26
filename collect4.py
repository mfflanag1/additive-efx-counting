"""Collect distinct count-4 (4,7) instances and tally the shapes of their 4 EFX0 allocations.

Question the proof must answer: do count-exactly-4 instances ever REQUIRE the 2-2-2
shape, or are their 4 forced allocations always among {4111, 3211}?
"""
import random, math, json
from collections import Counter as Ctr
from fast47 import Counter
from shape_analysis import all_efx0

N, M = 4, 7
C = Counter(N, M)

seed8 = [[8,20,1,4,1,16,1],[49,32,2,16,2,60,1],[28,59,1,60,7,46,8],[12,24,1,59,1,17,1]]


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


found = []       # list of (instance, shape-multiset)
shape_global = Ctr()
combo_global = Ctr()   # multiset of shapes across the 4 allocations
belowfour = []
rng = random.Random(2024)
for t in range(80):
    b, v = anneal(rng, iters=4000, scale=random.choice([40, 70, 100]), seed_inst=(seed8 if t % 3 == 0 else None))
    if b < 4:
        belowfour.append((b, v))
    if b == 4:
        allocs = all_efx0(v)
        shapes = tuple(sorted(Ctr(s for _, s, _ in allocs).items()))
        combo = tuple(sorted(s for _, s, _ in allocs))
        combo_global[combo] += 1
        for _, s, _ in allocs:
            shape_global[s] += 1
        found.append((v, combo))

print("distinct count-4 instances collected:", len(found))
print("BELOW-4 instances:", len(belowfour))
for b, v in belowfour:
    print("   SUB4", b, json.dumps(v))
print("\nShape frequency across all count-4 forced allocations:")
for sh, c in shape_global.most_common():
    print("   ", sh, c)
print("\nPer-instance shape-combo frequency (the 4 shapes each tight instance uses):")
for combo, c in combo_global.most_common():
    print("   ", combo, "x", c)
# does ANY tight instance use 2-2-2?
uses222 = [v for v, combo in found if (2, 2, 2, 1) in combo]
print("\ncount-4 instances whose forced set INCLUDES a 2221 allocation:", len(uses222))
if uses222:
    print("   example:", json.dumps(uses222[0]))
