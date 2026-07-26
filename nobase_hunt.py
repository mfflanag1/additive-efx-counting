"""Find the minimum EFX0 count among NO-BASE (4,7) instances.

Arm (b) of the dichotomy needs: no envy-free base => count >= 4 (conjectured 'abundant').
We directed-search for a no-base instance with the SMALLEST possible count to measure the
margin. If the floor over no-base instances is comfortably > 4, abundance is 'easy'; if it
approaches 4, arm (b) is delicate.
"""
import random, math, json, sys
from fast47 import Counter
from dichotomy import has_ef_base

N, M = 4, 7
C = Counter(N, M)


def obj(v):
    c = C.count(v)
    # only pay the expensive base check when count is low enough to matter
    if c <= 24:
        nobase = has_ef_base(v) is None
    else:
        nobase = False
    # objective: minimize count but REQUIRE no-base (huge penalty if base exists)
    return c + (0 if nobase else 100000), c, nobase


def anneal(rng, iters, scale, seed=None):
    v = [r[:] for r in seed] if seed else [[rng.randint(0, scale) for _ in range(M)] for _ in range(N)]
    o, c, nb = obj(v)
    cur = o
    best = (c if nb else 10**9)
    bestv = [r[:] for r in v]
    T = 3.0
    for _ in range(iters):
        i = rng.randrange(N); j = rng.randrange(M)
        old = v[i][j]; v[i][j] = rng.randint(0, scale)
        o2, c2, nb2 = obj(v)
        if o2 <= cur or rng.random() < math.exp((cur - o2) / max(T, 0.01)):
            cur = o2
            if nb2 and c2 < best:
                best = c2; bestv = [r[:] for r in v]
        else:
            v[i][j] = old
        T *= 0.9995
    return best, bestv


rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
allones = [[1] * M for _ in range(N)]
gmin = 10**9; garg = None
for t in range(12):
    seed = allones if t % 3 == 0 else None
    b, v = anneal(rng, 3000, random.choice([2, 3, 5, 9]), seed=seed)
    if b < gmin:
        gmin = b; garg = v
        print(f"run {t}: new no-base min count = {b}  {json.dumps(v)}", flush=True)
print("MIN no-base EFX0 count =", gmin, flush=True)
print(json.dumps(garg), flush=True)
if garg:
    print("confirm has_ef_base:", has_ef_base(garg) is not None, " count:", C.count(garg), flush=True)
