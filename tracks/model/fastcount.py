"""Fast numpy EFX0-count heuristic for search ONLY. The official arbiter remains
verify.py / check_candidates.py; every promising candidate is re-verified there.
Matches verify.py EFX0 semantics exactly (validated in __main__) for general (n, m).

EFX0 strong envy of i at j: v_i(X_i) < v_i(X_j) - min_{g in X_j} v_i(g).
An allocation is EFX0 iff NO ordered pair (i,j), j's bundle nonempty, is strongly envied.

Counter(n, m). For n=4 callers, Counter(4, m) preserves old behavior.
"""
import numpy as np


class Counter:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.size = 1 << m
        self.N = n ** m
        # allocation table (N, m) of agent indices, built vectorized (no itertools spike)
        ar = np.arange(self.N, dtype=np.int64)
        alloc = np.empty((self.N, m), dtype=np.int64)
        for g in range(m):
            alloc[:, g] = (ar // (n ** g)) % n
        pow2 = (1 << np.arange(m)).astype(np.int64)
        self.bmask = np.zeros((self.N, n), dtype=np.int64)
        for i in range(n):
            self.bmask[:, i] = ((alloc == i).astype(np.int64) * pow2).sum(axis=1)
        masks = np.arange(self.size, dtype=np.int64)[:, None]
        self.bit_mat = ((masks >> np.arange(m)[None, :]) & 1).astype(bool)
        self.bit_mat_i = self.bit_mat.astype(np.int64)

    def subset_vals(self, values):
        v = np.asarray(values, dtype=np.int64)          # (n, m)
        val = (self.bit_mat_i @ v.T).T                   # (n, size)
        BIG = 1 << 30
        minall = np.empty((self.n, self.size), dtype=np.int64)
        for i in range(self.n):
            masked = np.where(self.bit_mat, v[i][None, :], BIG)
            minall[i] = masked.min(axis=1)
        return val, minall

    def _margin(self, values):
        val, minall = self.subset_vals(values)
        bmask = self.bmask; N = self.N; n = self.n
        own = np.empty((N, n), dtype=np.int64)
        for i in range(n):
            own[:, i] = val[i][bmask[:, i]]
        margin = np.full(N, 1 << 30, dtype=np.int64)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                bj = bmask[:, j]
                vj = val[i][bj]; mn = minall[i][bj]
                slack = np.where(bj != 0, own[:, i] - (vj - mn), 1 << 30)
                margin = np.minimum(margin, slack)
        return margin

    def efx0_count(self, values):
        return int((self._margin(values) >= 0).sum())

    def has_global_min_good(self, values):
        """True if some good g is EVERY agent's least-valued good (v_i[g]==min_i for all i).
        Source Lemma: such a good always parks -> instance provably EFX0 (never a witness)."""
        v = np.asarray(values, dtype=np.int64)          # (n, m)
        rowmin = v.min(axis=1, keepdims=True)           # (n,1)
        is_min = (v == rowmin)                          # (n,m) bool
        return bool(is_min.all(axis=0).any())           # any column all-True

    def efx0_objective(self, values, alpha=0.02, gmpen=0.5):
        """Surrogate = count + alpha*mean(robustness margin of surviving EFX allocs)
        + gmpen if a global-min good exists (theory: such instances can never be witnesses).
        Count (ground truth) dominates; the extra terms only break ties among equal-count
        neighbors, steering toward the parkability-failure region (tight slacks, no global-min)."""
        margin = self._margin(values)
        is_efx = margin >= 0
        cnt = int(is_efx.sum())
        pen = gmpen if self.has_global_min_good(values) else 0.0
        if cnt == 0:
            return 0, 0.0
        return cnt, cnt + alpha * float(margin[is_efx].mean()) + pen


if __name__ == "__main__":
    import random
    from verify import enumerate_all
    rng = random.Random(0)
    for (n, m, T) in [(4, 8, 30), (4, 9, 12), (5, 8, 10), (5, 9, 5)]:
        C = Counter(n, m)
        ok = True
        for _ in range(T):
            vals = [[rng.randint(1, 30) for _ in range(m)] for _ in range(n)]
            a = C.efx0_count(vals)
            b = enumerate_all(n, m, vals)["efx0_count"]
            if a != b:
                ok = False
                print(f"MISMATCH n={n} m={m}: fast {a} slow {b} vals={vals}")
                break
        print(f"n={n} m={m} validation: {'OK' if ok else 'FAILED'}")
