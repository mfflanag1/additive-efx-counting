"""Fast numpy-vectorized exact EFX0 / EFX+ counter for small cells.

Drop-in fast replacement for the pure-Python enumeration in verify.py, for
n<=5, m<=11 (n^m assignments enumerated in memory-bounded chunks).

EFX0:  forall i!=j, forall g in X_j:                v_i(X_i) >= v_i(X_j) - v_i(g)
EFX+:  forall i!=j, forall g in X_j with v_i(g)>0:  v_i(X_i) >= v_i(X_j) - v_i(g)

Both reduce to a per-bundle removal-threshold under observer i's valuation:
  tau0_i(S) = v_i(S) - min_{g in S} v_i(g)              (0 for S empty)
  tau+_i(S) = v_i(S) - min_{g in S, v_i(g)>0} v_i(g)     (0 if S has no positive good)
An allocation is EFX0 iff v_i(X_i) >= tau0_i(X_j) for all i,j (diagonal & empty
bundles hold trivially), and EFX+ iff v_i(X_i) >= tau+_i(X_j) for all i,j.

Public API (each returns (count, first_example) where first_example is a per-good
assignment list of length m, or None):
  count_efx0(values, cap=None)
  count_efxplus(values, cap=None)
  count_both(values)  -> (efx0_count, efxplus_count, example_efx0)

`cap`: stop and return as soon as `cap` satisfying allocations have been found
(count is then reported as exactly `cap`); use cap=1 for an existence check.
"""
import numpy as np

DEFAULT_CHUNK = 1 << 23


def _precompute(values):
    """Return int32 arrays VAL, TAU0, TAUP of shape (n, 2^m) indexed [observer, bundle_mask]."""
    n = len(values)
    m = len(values[0])
    size = 1 << m
    VAL = np.zeros((n, size), dtype=np.int64)
    TAU0 = np.zeros((n, size), dtype=np.int64)
    TAUP = np.zeros((n, size), dtype=np.int64)
    for i in range(n):
        vi = values[i]
        val = [0] * size
        minall = [0] * size          # value; combined with a finiteness flag below
        minpos = [0] * size
        has_all = [False] * size     # bundle nonempty
        has_pos = [False] * size     # bundle has a positively-valued good (under obs i)
        for mask in range(1, size):
            g = (mask & -mask).bit_length() - 1
            rest = mask & (mask - 1)
            vg = vi[g]
            val[mask] = val[rest] + vg
            has_all[mask] = True
            # min over all goods in mask
            minall[mask] = vg if not has_all[rest] else min(minall[rest], vg)
            # min over positively-valued goods in mask
            if vg > 0:
                minpos[mask] = vg if not has_pos[rest] else min(minpos[rest], vg)
                has_pos[mask] = True
            else:
                minpos[mask] = minpos[rest]
                has_pos[mask] = has_pos[rest]
        for mask in range(size):
            VAL[i, mask] = val[mask]
            TAU0[i, mask] = (val[mask] - minall[mask]) if has_all[mask] else 0
            TAUP[i, mask] = (val[mask] - minpos[mask]) if has_pos[mask] else 0
    # int16 halves memory bandwidth on the (n, chunk) gathers/compares; safe whenever the
    # largest possible bundle value fits (campaign values <= a few hundred, m <= 11).
    dt = np.int16 if int(VAL.max()) < 32000 else np.int32
    return VAL.astype(dt), TAU0.astype(dt), TAUP.astype(dt)


def _chunk_bundles(start, count, n, m):
    """Per-agent bundle bitmasks for assignment indices [start, start+count).

    Returns (bundles, idx): bundles int32 (count, n); idx int64 (count,) global indices.
    Assignment index a encodes good g's agent as base-n digit (a // n**g) % n; the
    per-good digit is peeled off with successive %n, //n to avoid a big (count,m) matrix.
    """
    idx = np.arange(start, start + count, dtype=np.int64)
    D = np.empty((count, m), dtype=np.int8)          # base-n digits, D[c,g] = agent of good g
    a = idx.copy()
    for g in range(m):
        D[:, g] = a % n
        a //= n
    bits = (np.int32(1) << np.arange(m, dtype=np.int32))
    bundles = np.empty((count, n), dtype=np.int32)
    for i in range(n):
        bundles[:, i] = (D == i) @ bits              # sum of bit_g over goods g assigned to i
    return bundles, idx


def _own(bundles, VAL, n):
    """Own values in (n, count) layout: own[i, c] = v_i(X_i)."""
    ar = np.arange(n)
    return VAL[ar[:, None], bundles.T]   # (n, count)


def _eval_efx(bundles, own, TAU, n):
    """Boolean (count,) mask: own_i >= tau_i(X_j) for all observers i, owners j.

    Works in (n, count) layout and loops over the (small) owner axis, so the peak
    temporary is (n, count) rather than (count, n, n)."""
    bad = np.zeros(bundles.shape[0], dtype=bool)
    for j in range(n):
        tau_j = TAU[:, bundles[:, j]]        # (n, count): tau_j[i,c] = TAU[i, X_j(c)]
        bad |= (own < tau_j).any(axis=0)     # some observer strongly-envies owner j
    return ~bad


def _decode(idx, n, m):
    a = []
    x = int(idx)
    for _ in range(m):
        a.append(x % n)
        x //= n
    return a


def count_efx0(values, cap=None, chunk=DEFAULT_CHUNK):
    n, m = len(values), len(values[0])
    total = np.int64(n) ** m
    VAL, TAU0, _ = _precompute(values)
    count = 0
    example = None
    start = 0
    while start < total:
        c = int(min(chunk, total - start))
        bundles, idx = _chunk_bundles(start, c, n, m)
        own = _own(bundles, VAL, n)
        ok = _eval_efx(bundles, own, TAU0, n)
        hit = int(ok.sum())
        if hit and example is None:
            example = _decode(idx[np.argmax(ok)], n, m)
        count += hit
        if cap is not None and count >= cap:
            return cap, example
        start += c
    return count, example


def count_efxplus(values, cap=None, chunk=DEFAULT_CHUNK):
    n, m = len(values), len(values[0])
    total = np.int64(n) ** m
    VAL, _, TAUP = _precompute(values)
    count = 0
    example = None
    start = 0
    while start < total:
        c = int(min(chunk, total - start))
        bundles, idx = _chunk_bundles(start, c, n, m)
        own = _own(bundles, VAL, n)
        ok = _eval_efx(bundles, own, TAUP, n)
        hit = int(ok.sum())
        if hit and example is None:
            example = _decode(idx[np.argmax(ok)], n, m)
        count += hit
        if cap is not None and count >= cap:
            return cap, example
        start += c
    return count, example


def count_both(values, chunk=DEFAULT_CHUNK):
    """Return (efx0_count, efxplus_count, example_efx0) in a single pass (no cap)."""
    n, m = len(values), len(values[0])
    total = np.int64(n) ** m
    VAL, TAU0, TAUP = _precompute(values)
    c0 = cp = 0
    example = None
    start = 0
    while start < total:
        c = int(min(chunk, total - start))
        bundles, idx = _chunk_bundles(start, c, n, m)
        own = _own(bundles, VAL, n)
        ok0 = _eval_efx(bundles, own, TAU0, n)
        okp = _eval_efx(bundles, own, TAUP, n)
        h0 = int(ok0.sum())
        if h0 and example is None:
            example = _decode(idx[np.argmax(ok0)], n, m)
        c0 += h0
        cp += int(okp.sum())
        start += c
    return c0, cp, example


# ---------------------------------------------------------------------------
# CLI: validation against reference verify.enumerate_all, and benchmarking.
# ---------------------------------------------------------------------------
def _validate():
    import random
    from verify import enumerate_all

    rng = random.Random(20260723)
    cases = []
    # 60+ random instances spanning the required grid, both value ranges.
    for n in (2, 3, 4, 5):
        for m in range(2, 10):
            for positive in (False, True):
                # keep total assignments modest for the reference (pure-Python)
                if n ** m > 400_000:
                    continue
                lo = 1 if positive else 0
                vals = [[rng.randint(lo, 9) for _ in range(m)] for _ in range(n)]
                cases.append((n, m, vals, positive))

    print(f"Validating {len(cases)} random instances against verify.enumerate_all ...")
    fails = 0
    for k, (n, m, vals, positive) in enumerate(cases):
        ref = enumerate_all(n, m, vals)
        f0, fp, _ = count_both(vals)
        if f0 != ref["efx0_count"] or fp != ref["efxplus_count"]:
            fails += 1
            print(f"  MISMATCH #{k} n={n} m={m} pos={positive}: "
                  f"fast=({f0},{fp}) ref=({ref['efx0_count']},{ref['efxplus_count']})")
            print(f"    values={vals}")
    print(f"Random: {len(cases) - fails}/{len(cases)} exact match "
          f"(n in {{2,3,4,5}}, m in 2..9, both value ranges).")

    # Documented near-witnesses (results/CAMPAIGN_LOG.md + TWO_TREASURE_LEMMA.md).
    witnesses = [
        ("count5_running", 5,
         [[11, 8, 20, 1, 4, 1, 16, 1], [16, 49, 32, 2, 16, 2, 60, 1],
          [16, 40, 59, 1, 60, 7, 46, 8], [10, 12, 24, 1, 59, 1, 17, 1]]),
        ("count4_basin1", 4,
         [[11, 8, 20, 1, 4, 1, 16, 1], [16, 49, 32, 2, 16, 2, 60, 1],
          [28, 28, 59, 1, 60, 7, 46, 8], [10, 12, 24, 1, 59, 1, 17, 1]]),
        ("count4_parkfloor", 4,
         [[3, 13, 8, 40, 7, 39, 38, 13], [13, 1, 1, 4, 11, 1, 40, 12],
          [7, 3, 2, 12, 2, 39, 25, 12], [2, 13, 2, 40, 2, 39, 38, 2]]),
    ]
    wfail = 0
    print("Near-witness instances (expected efx0 counts 4,4,5):")
    for name, expect, vals in witnesses:
        ref = enumerate_all(4, 8, vals)
        f0, fp, _ = count_both(vals)
        ok = (f0 == ref["efx0_count"] == expect and fp == ref["efxplus_count"])
        wfail += not ok
        print(f"  {name}: fast efx0={f0} efx+={fp} | ref efx0={ref['efx0_count']} "
              f"efx+={ref['efxplus_count']} | expect efx0={expect} | {'OK' if ok else 'FAIL'}")

    total_fail = fails + wfail
    print()
    if total_fail == 0:
        print("VALIDATION PASSED: 100% exact match with reference (random + near-witnesses).")
    else:
        print(f"VALIDATION FAILED: {total_fail} mismatch(es). DO NOT TRUST fast_verify.")
    return total_fail == 0


def _bench():
    import random
    import time
    from verify import enumerate_all

    rng = random.Random(7)

    def rand(n, m):
        return [[rng.randint(0, 9) for _ in range(m)] for _ in range(n)]

    print(f"{'cell':>8} | {'fast (s)':>10} | {'ref (s)':>12} | {'speedup':>8}")
    print("-" * 50)
    for n, m, do_ref in [(4, 10, True), (5, 9, True), (5, 10, False)]:
        vals = rand(n, m)
        t = time.perf_counter()
        f0, fp, _ = count_both(vals)
        tf = time.perf_counter() - t
        if do_ref:
            t = time.perf_counter()
            ref = enumerate_all(n, m, vals)
            tr = time.perf_counter() - t
            match = (f0 == ref["efx0_count"] and fp == ref["efxplus_count"])
            print(f"({n},{m}) | {tf:10.3f} | {tr:12.3f} | {tr / tf:7.1f}x  "
                  f"[{'match' if match else 'MISMATCH'}]")
        else:
            print(f"({n},{m}) | {tf:10.3f} | {'(skipped)':>12} | {'-':>8}")


if __name__ == "__main__":
    import sys
    if "--validate" in sys.argv:
        ok = _validate()
        sys.exit(0 if ok else 1)
    elif "--bench" in sys.argv:
        _bench()
    else:
        print("usage: python fast_verify.py [--validate | --bench]")
