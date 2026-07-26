"""Dichotomy investigation for '>=4 EFX0 at (4,7)':
  arm (a) envy-free base exists  => >=4 by parking (proven conditional)
  arm (b) NO envy-free base      => 'flat-like' => abundance (to establish)

has_ef_base(v): does there exist a good f and an envy-free partition of the other 6 goods
into 4 nonempty bundles (shapes 3111 or 2211)?  Envy-free => EFX0.  If yes, that is a
parking base (the floater f then parks at >=1 agent; envy-free => all 4 agents are
plain-sources).

We test the dichotomy: gather instances, split by has_ef_base, and report the EFX0-count
distribution of the NO-BASE class (must be >=4 for the conjecture; conjectured 'abundant').
"""
import random, itertools
from fast_verify import count_efx0
from fast47 import Counter

N, M = 4, 7
C = Counter(N, M)


def tau0(vi, S):
    if not S:
        return 0
    xs = [vi[g] for g in S]
    return sum(xs) - min(xs)


def is_envy_free(v, bundles):
    own = [sum(v[i][g] for g in bundles[i]) for i in range(N)]
    for i in range(N):
        for j in range(N):
            if i != j and own[i] < sum(v[i][g] for g in bundles[j]):
                return False
    return True


def has_ef_base(v):
    """True iff some good f can be removed leaving an envy-free partition of the other 6
    goods into 4 nonempty bundles. Returns (f, bundles) or None."""
    goods = list(range(M))
    for f in goods:
        rest = [g for g in goods if g != f]           # 6 goods
        # assign 6 goods to 4 agents, all nonempty (shapes 3111/2211). brute force 4^6 with
        # nonempty filter.
        for assign in itertools.product(range(N), repeat=6):
            bundles = [[] for _ in range(N)]
            for idx, g in enumerate(rest):
                bundles[assign[idx]].append(g)
            if any(len(b) == 0 for b in bundles):
                continue
            if is_envy_free(v, bundles):
                return (f, bundles)
    return None


if __name__ == "__main__":
    # 1. all-ones: no base, big count
    allones = [[1] * M for _ in range(N)]
    print("all-ones: has_ef_base =", has_ef_base(allones) is not None,
          " count =", count_efx0(allones)[0])
    # 2. structured no-base witness from team-lead
    w = [[6,2,2,2,2,2,1],[5,1,1,1,1,1,5],[1,1,1,1,1,1,6],[1,1,1,1,1,1,5]]
    print("team witness: has_ef_base =", has_ef_base(w) is not None,
          " count =", count_efx0(w)[0])
    # 3. my (4,7) tight witness: should HAVE a base
    t = [[30,66,69,9,21,19,63],[12,56,58,9,10,24,52],[12,33,45,20,24,8,64],[11,60,1,18,2,6,41]]
    print("tight-4 witness: has_ef_base =", has_ef_base(t) is not None,
          " count =", count_efx0(t)[0])
