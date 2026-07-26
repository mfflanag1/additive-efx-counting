"""Does NC-A + no-universal-min + pairwise-non-proportional force an EFX0
allocation of shape 4211 or 3221? Fast sweep."""
import random, sys
import numpy as np
from fastshape import efx0_shapes, precompute_np
from residual_test import satisfies_NCA, universal_min_good, pairwise_nonproportional

n, m = 4, 8
T4211 = (4, 2, 1, 1)
T3221 = (3, 2, 2, 1)


def has_target(shapes):
    return shapes.get(T4211, 0) + shapes.get(T3221, 0) > 0


def run(seed, hi, N):
    random.seed(seed)
    tested = 0
    no_efx = 0
    no_target = 0
    ex_notarget = []
    ex_noefx = []
    for _ in range(N):
        values = [[random.randint(1, hi) for _ in range(m)] for _ in range(n)]
        if universal_min_good(n, m, values) is not None:
            continue
        if not pairwise_nonproportional(n, m, values):
            continue
        if not satisfies_NCA(n, m, values):
            continue
        tested += 1
        shapes = efx0_shapes(values)
        if not shapes:
            no_efx += 1
            if len(ex_noefx) < 5:
                ex_noefx.append(values)
        elif not has_target(shapes):
            no_target += 1
            if len(ex_notarget) < 8:
                ex_notarget.append((values, {tuple(int(x) for x in k): v for k, v in shapes.items()}))
    print(f"hi={hi} seed={seed} N={N}: tested(3NC)={tested} no_efx={no_efx} efx_but_no_4211/3221={no_target}")
    for v, sh in ex_notarget:
        print("  NO_TARGET", v, sh)
    for v in ex_noefx:
        print("  NO_EFX", v)
    return tested, no_efx, no_target


if __name__ == "__main__":
    hi = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    run(seed, hi, N)
