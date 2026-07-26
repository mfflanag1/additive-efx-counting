"""Fast numpy enumerator: for a 4-agent 8-good instance, return the multiset of
shapes admitting an EFX0 allocation (and counts). Vectorized over all 4^8."""
import numpy as np
import itertools

n, m = 4, 8
SIZE = 1 << m

# all assignments 4^8 x 8 (digits 0..3)
_digits = np.array(list(itertools.product(range(n), repeat=m)), dtype=np.int8)  # (65536,8)
_pow = (1 << np.arange(m)).astype(np.int64)
# bundle mask per agent: (65536, 4)
_masks = np.stack([((_digits == i).astype(np.int64) * _pow).sum(axis=1) for i in range(n)], axis=1)
# shape per assignment (sorted sizes desc) as tuple key -> precompute sizes
_sizes = np.stack([(_digits == i).sum(axis=1) for i in range(n)], axis=1)  # (65536,4)
_shape_keys = [tuple(sorted(row, reverse=True)) for row in _sizes]
_shape_arr = np.array(_shape_keys)  # (65536,4)


def precompute_np(values):
    val = np.zeros((n, SIZE), dtype=np.int64)
    minall = np.full((n, SIZE), np.iinfo(np.int64).max, dtype=np.int64)
    for i in range(n):
        vi = values[i]
        for mask in range(1, SIZE):
            g = (mask & -mask).bit_length() - 1
            rest = mask & (mask - 1)
            val[i][mask] = val[i][rest] + vi[g]
            minall[i][mask] = min(minall[i][rest], vi[g])
    minall[:, 0] = 0
    return val, minall


def efx0_mask(values):
    """Boolean array (65536,) True where allocation is EFX0."""
    val, minall = precompute_np(values)
    own = np.empty((SIZE ** 0 + _masks.shape[0], n), dtype=np.int64)  # placeholder
    A = _masks.shape[0]
    ownval = np.empty((A, n), dtype=np.int64)
    for i in range(n):
        ownval[:, i] = val[i][_masks[:, i]]
    ok = np.ones(A, dtype=bool)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            mj = _masks[:, j]
            vj = val[i][mj]
            thr = vj - minall[i][mj]  # tau; for empty bundle mask 0 -> 0
            # empty bundle: mask 0 -> val 0, minall 0 -> thr 0, always ok
            ok &= ownval[:, i] >= thr
    return ok


def efx0_shapes(values):
    ok = efx0_mask(values)
    shapes = {}
    for idx in np.nonzero(ok)[0]:
        key = tuple(_shape_arr[idx])
        shapes[key] = shapes.get(key, 0) + 1
    return shapes


if __name__ == "__main__":
    V = [[11,8,20,1,4,1,16,1],[16,49,32,2,16,2,60,1],[16,40,59,1,60,7,46,8],[10,12,24,1,59,1,17,1]]
    print(efx0_shapes(V))
