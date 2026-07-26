"""Specialized fast EFX0 counter for fixed (n,m) with reused assignment table.

Precompute the (n^m, n) bundle-mask table ONCE (depends only on n,m, not values).
Per call, rebuild the (n, 2^m) VAL/TAU0 tables from `values` and evaluate. ~10-40x
faster than fast_verify.count_efx0 for repeated calls at small (n,m).
"""
import numpy as np


class Counter:
    def __init__(self, n, m):
        self.n, self.m = n, m
        total = n ** m
        idx = np.arange(total, dtype=np.int64)
        D = np.empty((total, m), dtype=np.int8)
        a = idx.copy()
        for g in range(m):
            D[:, g] = a % n
            a //= n
        bits = (np.int64(1) << np.arange(m, dtype=np.int64))
        self.BM = np.empty((total, n), dtype=np.int64)   # (total, n) bundle masks
        for i in range(n):
            self.BM[:, i] = (D == i) @ bits
        self.size = 1 << m
        # masks -> list of good indices for TAU precompute
        self._masks = np.arange(self.size, dtype=np.int64)

    def _tables(self, values):
        n, m, size = self.n, self.m, self.size
        VAL = np.zeros((n, size), dtype=np.int64)
        TAU0 = np.zeros((n, size), dtype=np.int64)
        for i in range(n):
            vi = values[i]
            val = np.zeros(size, dtype=np.int64)
            minall = np.zeros(size, dtype=np.int64)
            has = np.zeros(size, dtype=bool)
            for mask in range(1, size):
                g = (mask & -mask).bit_length() - 1
                rest = mask & (mask - 1)
                vg = vi[g]
                val[mask] = val[rest] + vg
                minall[mask] = vg if not has[rest] else min(minall[rest], vg)
                has[mask] = True
            VAL[i] = val
            TAU0[i] = val - minall
        return VAL, TAU0

    def _ok_mask(self, values):
        n = self.n
        VAL, TAU0 = self._tables(values)
        BM = self.BM
        own = np.empty(BM.shape, dtype=np.int64)     # (total, n)
        for i in range(n):
            own[:, i] = VAL[i, BM[:, i]]
        bad = np.zeros(BM.shape[0], dtype=bool)
        for j in range(n):
            tau_j = TAU0[:, BM[:, j]]                 # (n, total): tau_j[i,c]
            bad |= (own.T < tau_j).any(axis=0)
        return ~bad

    def count(self, values):
        return int(self._ok_mask(values).sum())

    def allocs(self, values):
        """Return list of (bundles, shape) for every EFX0 allocation.

        bundles: list of n lists of good indices; shape: sorted sizes desc."""
        n, m = self.n, self.m
        ok = self._ok_mask(values)
        idxs = np.nonzero(ok)[0]
        out = []
        popcount = [bin(x).count("1") for x in range(1 << m)]
        BM = self.BM
        for a in idxs:
            masks = BM[a]
            bundles = [[g for g in range(m) if (masks[i] >> g) & 1] for i in range(n)]
            shape = tuple(sorted((popcount[int(masks[i])] for i in range(n)), reverse=True))
            out.append((bundles, shape))
        return out


if __name__ == "__main__":
    import time
    from fast_verify import count_efx0
    C = Counter(4, 7)
    import random
    rng = random.Random(1)
    # correctness vs reference
    for _ in range(200):
        v = [[rng.randint(0, 9) for _ in range(7)] for _ in range(4)]
        assert C.count(v) == count_efx0(v)[0], v
    print("correctness OK (200 instances match count_efx0)")
    v = [[8,20,1,4,1,16,1],[49,32,2,16,2,60,1],[28,59,1,60,7,46,8],[12,24,1,59,1,17,1]]
    t = time.perf_counter()
    for _ in range(1000):
        C.count(v)
    print("per call ms", (time.perf_counter() - t))
