"""Test a reduction (4,7)->(4,6): park a universal-min good f into EFX allocs of I\\{f}.

Claim under test: if f is a universal minimum (v_i(f) <= v_i(g) for all i and all g!=f),
then #EFX0(I) >= #EFX0(I\\{f})  [each 6-good EFX alloc, after making its envy graph
acyclic, has a source where f parks], and in particular >= 4 by Thm 3.8.

We test the strong form directly: min #EFX0(I) over instances possessing a universal-min
good; and whether #EFX0(I) >= #EFX0(I\\{f}) holds for that f.
"""
import random, math
from fast47 import Counter
from fast_verify import count_efx0

N, M = 4, 7
C = Counter(N, M)


def has_univ_min(v):
    """Return index of a universal-min good if one exists, else None."""
    for f in range(M):
        if all(v[i][f] <= v[i][g] for i in range(N) for g in range(M)):
            return f
    return None


def count6(v, drop):
    v6 = [[v[i][g] for g in range(M) if g != drop] for i in range(N)]
    return count_efx0(v6)[0]


def anneal_univmin(rng, iters, scale):
    """Anneal toward low count while KEEPING good 0 a universal min (clamp)."""
    v = [[rng.randint(1, scale) for _ in range(M)] for _ in range(N)]
    for i in range(N):
        v[i][0] = 1  # good0 tiny -> universal min (others >=1, we allow others=0 rarely)
    def fix(v):
        for i in range(N):
            mn = min(v[i][g] for g in range(1, M))
            if v[i][0] > mn:
                v[i][0] = max(0, mn)
    cur = C.count(v); best = cur; bestv = [r[:] for r in v]
    T = 2.0
    for _ in range(iters):
        i = rng.randrange(N); j = rng.randrange(1, M)
        old = v[i][j]; v[i][j] = rng.randint(0, scale); fix(v)
        c = C.count(v)
        if c <= cur or rng.random() < math.exp((cur - c) / max(T, 0.01)):
            cur = c
            if c < best: best = c; bestv = [r[:] for r in v]
        else:
            v[i][j] = old; fix(v)
        T *= 0.9996
    return best, bestv


rng = random.Random(5)
# (1) random instances that happen to have a universal min
viol = 0; tested = 0; mn = 999; lift_fail = 0
for _ in range(20000):
    v = [[rng.randint(0, 9) for _ in range(M)] for _ in range(N)]
    f = has_univ_min(v)
    if f is None:
        continue
    tested += 1
    c = C.count(v)
    mn = min(mn, c)
    c6 = count6(v, f)
    if c < c6:
        lift_fail += 1
    if c < 4:
        viol += 1
        print("VIOLATION <4 with univ-min:", c, v)
print(f"[random] instances with a universal-min good: {tested}; min #EFX0(I) = {mn}")
print(f"[random]  #EFX0(I) < #EFX0(I\\f) violations: {lift_fail}/{tested}  (0 => lifting bound holds)")
print(f"[random]  #EFX0(I) < 4 violations: {viol}")

# (2) directed: push count down while keeping good0 universal-min
gmin = 999; garg = None
for s in range(10):
    b, v = anneal_univmin(rng, 1200, random.choice([40, 80]))
    if b < gmin: gmin = b; garg = v
print(f"[directed univ-min] min #EFX0 = {gmin}")
if garg:
    f = has_univ_min(garg)
    print("   f=", f, "count6=", count6(garg, f) if f is not None else "NA", "inst=", garg)
