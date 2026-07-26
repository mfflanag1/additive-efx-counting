"""Directed count-minimizer for (4,7): find the EFX0-count floor and tight instances."""
import random, math, json, sys
from fast47 import Counter

N, M = 4, 7
_C = Counter(N, M)
def count_efx0(v):
    return (_C.count(v), None)


def rand_inst(rng, scale):
    return [[rng.randint(1, scale) for _ in range(M)] for _ in range(N)]


def anneal(seed, iters, scale, seed_inst=None):
    rng = random.Random(seed)
    vals = [r[:] for r in seed_inst] if seed_inst else rand_inst(rng, scale)
    cur = count_efx0(vals)[0]
    best = cur
    bestv = [r[:] for r in vals]
    T = 2.5
    for it in range(iters):
        i = rng.randrange(N); j = rng.randrange(M)
        old = vals[i][j]
        vals[i][j] = rng.randint(0, scale)
        c = count_efx0(vals)[0]
        if c <= cur or rng.random() < math.exp((cur - c) / max(T, 0.01)):
            cur = c
            if c < best:
                best = c; bestv = [r[:] for r in vals]
        else:
            vals[i][j] = old
        T *= 0.99985
    return best, bestv


# Seed instances: count-8 (4,7) from deleting good 0 of basin1
seed8 = [[8,20,1,4,1,16,1],[49,32,2,16,2,60,1],[28,59,1,60,7,46,8],[12,24,1,59,1,17,1]]

gmin = 999; garg = None; sub4 = []
seeds = list(range(int(sys.argv[1]) if len(sys.argv) > 1 else 12))
for s in seeds:
    si = seed8 if s % 2 == 0 else None
    b, v = anneal(s, iters=8000, scale=70, seed_inst=si)
    print(f"seed {s}: best {b}", flush=True)
    if b < gmin:
        gmin = b; garg = v
    if b < 4:
        sub4.append((b, v))
print("GLOBAL MIN", gmin, flush=True)
print(json.dumps(garg), flush=True)
if sub4:
    print("SUB-4 FOUND:", flush=True)
    for b, v in sub4:
        print(b, json.dumps(v), flush=True)
else:
    print("No sub-4 instance found.", flush=True)
