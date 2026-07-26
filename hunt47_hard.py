"""Aggressive sub-4 hunt at (4,7): surrogate objective = (count, fragility).

Seeded from confirmed count-4 tight instances. If the true floor were <4, a directed
descent that also rewards 'survivors close to being killed' should break through.
"""
import random, math, json, sys
from fast47 import Counter
from shape_analysis import all_efx0

N, M = 4, 7
C = Counter(N, M)

tight = [
    [[30,66,69,9,21,19,63],[12,56,58,9,10,24,52],[12,33,45,20,24,8,64],[11,60,1,18,2,6,41]],
    [[8,20,1,4,1,16,1],[49,32,2,16,2,60,1],[28,59,1,60,7,46,8],[12,24,1,59,1,17,1]],
]


def fragility(v):
    """Sum over EFX0 allocations of (1 / (1 + min slack)): higher = more fragile survivors.
    Slack of an allocation = min over (observer i, owner j) of own_i - tau0_i(Xj)."""
    allocs = all_efx0(v)
    tot = 0.0
    for assign, shape, bundles in allocs:
        own = [sum(v[i][g] for g in bundles[i]) for i in range(N)]
        mslack = 10**9
        for i in range(N):
            for j in range(N):
                if i == j or not bundles[j]:
                    continue
                vals = [v[i][g] for g in bundles[j]]
                tau = sum(vals) - min(vals)
                mslack = min(mslack, own[i] - tau)
        tot += 1.0 / (1 + max(mslack, 0))
    return tot


def obj(v):
    c = C.count(v)
    return (c, -fragility(v)), c


def anneal(rng, iters, scale, seed_inst):
    vals = [r[:] for r in seed_inst]
    best_o, cur_c = obj(vals)
    cur_o = best_o
    best = cur_c; bestv = [r[:] for r in vals]
    T = 1.5
    for _ in range(iters):
        i = rng.randrange(N); j = rng.randrange(M)
        old = vals[i][j]; vals[i][j] = rng.randint(0, scale)
        o, c = obj(vals)
        # accept if objective tuple improves or Metropolis on count
        if o <= cur_o or rng.random() < math.exp((cur_o[0] - o[0]) / max(T, 0.01)):
            cur_o = o
            if c < best: best = c; bestv = [r[:] for r in vals]
        else:
            vals[i][j] = old
        T *= 0.9998
    return best, bestv


rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
gmin = 999; garg = None
for t in range(20):
    seed = tight[t % len(tight)]
    b, v = anneal(rng, iters=3000, scale=random.choice([50, 80, 120]), seed_inst=seed)
    if b < gmin:
        gmin = b; garg = v
        print(f"run {t}: NEW MIN {b} {json.dumps(v)}", flush=True)
    if b < 4:
        print("!!!! SUB-4 !!!!", b, json.dumps(v), flush=True)
print("HARD HUNT GLOBAL MIN", gmin, flush=True)
