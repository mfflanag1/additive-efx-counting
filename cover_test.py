"""Test which minimal shape-set covers all EFX0-existent (4,8) instances.
Question: is {2222,4211,3221} sufficient (5111,3311 never sole)?
Also record when EFX0 exists but the covering set is empty."""
import random, sys
import numpy as np
from fastshape import efx0_shapes

n, m = 4, 8
SHAPES = [(2,2,2,2),(4,2,1,1),(3,2,2,1),(5,1,1,1),(3,3,1,1)]


def gen(hi, mode):
    if mode == "flat":
        return [[random.randint(1, hi) for _ in range(m)] for _ in range(n)]
    if mode == "lumpy":
        # each agent has 1-2 big peaks, rest small
        V = []
        for i in range(n):
            row = [random.randint(1, 3) for _ in range(m)]
            for _ in range(random.randint(1, 3)):
                row[random.randrange(m)] = random.randint(hi//2, hi)
            V.append(row)
        return V
    if mode == "skew":
        return [[random.choice([1,1,1,2,2,3,hi//2,hi]) for _ in range(m)] for _ in range(n)]


def run(hi, N, mode, seed):
    random.seed(seed)
    cover_fail = []   # EFX0 exists but not in {2222,4211,3221}
    no_efx = 0
    sole_5111 = 0
    sole_3311 = 0
    total_efx = 0
    for _ in range(N):
        V = gen(hi, mode)
        sh = efx0_shapes(V)
        if not sh:
            no_efx += 1
            continue
        total_efx += 1
        keys = {tuple(int(x) for x in k) for k in sh}
        cover = keys & {(2,2,2,2),(4,2,1,1),(3,2,2,1)}
        if not cover:
            cover_fail.append((V, {tuple(int(x) for x in k): v for k, v in sh.items()}))
        if keys == {(5,1,1,1)}:
            sole_5111 += 1
        if keys == {(3,3,1,1)}:
            sole_3311 += 1
    print(f"mode={mode} hi={hi} N={N} seed={seed}: efx0_exists={total_efx} no_efx={no_efx} "
          f"cover_fail(not in 2222/4211/3221)={len(cover_fail)} sole_5111={sole_5111} sole_3311={sole_3311}")
    for V, sh in cover_fail[:10]:
        print("  COVER_FAIL", V, sh)


if __name__ == "__main__":
    hi = int(sys.argv[1]); N = int(sys.argv[2]); mode = sys.argv[3]; seed = int(sys.argv[4]) if len(sys.argv)>4 else 0
    run(hi, N, mode, seed)
