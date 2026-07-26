"""Vectorized envy-free-base detector for (4,7): does removing some good leave an
envy-free partition of the other 6 goods into 4 nonempty bundles? (shapes 3111/2211)."""
import numpy as np
from itertools import product

# Precompute, for the 6 "kept" goods, the 4^6 assignment -> per-agent bundle-mask table
# on the LOCAL index 0..5. We map to global goods per floater choice at call time.
_A6 = None
def _tab6():
    global _A6
    if _A6 is None:
        idx = np.arange(4**6)
        D = np.empty((4**6, 6), dtype=np.int8)
        a = idx.copy()
        for g in range(6):
            D[:, g] = a % 4; a //= 4
        _A6 = D  # (4096,6) agent of each local good
    return _A6

def has_ef_base(v):
    v = np.asarray(v)             # (4,7)
    D = _tab6()                    # (4096,6)
    N = 4
    for f in range(7):
        kept = [g for g in range(7) if g != f]     # 6 global goods
        vk = v[:, kept]            # (4,6) values on kept goods
        # bundle value matrix: own[a, assign] and cross. Build per-agent bundle value:
        # val[i, c, owner] = sum over goods g with D[c,g]==owner of v[i, kept[g]]
        # We need, for each assignment c: own_i = val[i,c,i]; and envy-free iff
        # own_i >= val[i,c,j] for all j. Also all 4 bundles nonempty.
        # Compute val[i,c,owner]:
        # onehot (4096,6,4)
        oh = (D[:, :, None] == np.arange(4)[None, None, :])   # (4096,6,4) bool
        # val[i,c,owner] = sum_g vk[i,g]*oh[c,g,owner]
        val = np.einsum('ig,cgo->ico', vk.astype(np.int64), oh.astype(np.int64))  # (4,4096,4)
        own = np.diagonal(val, axis1=0, axis2=2)   # (4096,4): own[c,i]=val[i,c,i]
        # envy-free: for all i, own[c,i] >= val[i,c,j] for all j
        ef = np.ones(4**6, dtype=bool)
        for i in range(N):
            ef &= (val[i] <= own[:, i][:, None]).all(axis=1)  # own_i >= val[i,c,:]
        # nonempty: each owner appears
        cnt = oh.sum(axis=1)   # (4096,4) size of each bundle
        nonempty = (cnt > 0).all(axis=1)
        if np.any(ef & nonempty):
            return True
    return False

if __name__ == "__main__":
    from dichotomy import has_ef_base as slow
    import random
    rng = random.Random(0)
    for _ in range(200):
        v = [[rng.randint(0,6) for _ in range(7)] for _ in range(4)]
        assert has_ef_base(v) == (slow(v) is not None), v
    print("fast_base matches slow on 200 instances")
    import time
    v=[[1]*7 for _ in range(4)]
    t=time.perf_counter()
    for _ in range(200): has_ef_base(v)
    print("per call ms:", (time.perf_counter()-t)/200*1000)
