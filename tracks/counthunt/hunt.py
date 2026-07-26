"""n=5 EFX0 count-hunter (counterexample campaign against Neoh-Teh Conj 6.1).

Minimize the number of EFX0 allocations of a single additive integer instance.
Conjecture: >= n EFX0 allocations for n agents. Any (5,*) instance with count < 5
REFUTES it; count == 5 gives a new tight upper bound on the minimum.

Surrogate-directed simulated annealing. Objective = efx0_count + fragility_term,
where the fragility term (always in [0,1), so count strictly dominates) prefers,
among equal-count neighbours, instances whose surviving EFX0 allocations have
minimal total slack in their binding EFX inequalities -- i.e. instances one small
perturbation away from losing a survivor. This slack tiebreak was the decisive
lever at n=4 (300 -> 4).

Uses fast_verify's validated precompute (imported, not modified) for a single
combined count + slack pass. Elites written atomically to elites.jsonl on every
improvement. NEVER trusts a claimed count downstream -- the lead dual-verifies.
"""
import json, math, os, random, sys, time
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from fast_verify import _precompute, _chunk_bundles, _own, DEFAULT_CHUNK

ELITES = os.environ.get("COUNTHUNT_ELITES",
                        os.path.join(os.path.dirname(__file__), "elites.jsonl"))
SLACK_SCALE = 1.0 / 2000.0   # keeps fragility term < 1 for all counts we care about
VMAX = 60


def count_and_slack(values):
    """Return (efx0_count, total_slack, example_assignment).

    total_slack = sum over surviving EFX0 allocations A of
        min_{i != j} [ v_i(X_i) - ( v_i(X_j) - min_{g in X_j} v_i(g) ) ]
      = min_{i != j} [ own_i(A) - tau0_i(X_j) ]     (>= 0 for an EFX0 allocation)
    Lower total slack = more fragile survivors.
    """
    n, m = len(values), len(values[0])
    total = np.int64(n) ** m
    VAL, TAU0, _ = _precompute(values)
    count = 0
    slack_sum = 0
    example = None
    start = 0
    ar = np.arange(n)
    while start < total:
        c = int(min(DEFAULT_CHUNK, total - start))
        bundles, idx = _chunk_bundles(start, c, n, m)     # (c, n), (c,)
        own = _own(bundles, VAL, n)                        # (n, c)
        # tau_j[i, k, c'] would be big; loop owners j like fast_verify does.
        # margin_min[c'] = min over i!=j of own[i] - TAU0[i, bundle_j]
        margin_min = None
        for j in range(n):
            tau_j = TAU0[:, bundles[:, j]]                 # (n, c): tau of owner j's bundle
            marg = own - tau_j                             # (n, c): observer i vs owner j
            marg[j, :] = np.iinfo(marg.dtype).max // 2     # exclude i == j (self)
            col_min = marg.min(axis=0)                     # (c,): tightest observer for owner j
            margin_min = col_min if margin_min is None else np.minimum(margin_min, col_min)
        ok = margin_min >= 0
        hit = int(ok.sum())
        if hit:
            if example is None:
                example = _decode(int(idx[np.argmax(ok)]), n, m)
            slack_sum += int(margin_min[ok].sum())
            count += hit
        start += c
    return count, slack_sum, example


def _decode(a, n, m):
    out = []
    for _ in range(m):
        out.append(a % n)
        a //= n
    return out


def objective(count, slack_sum):
    return count + min(0.99, slack_sum * SLACK_SCALE)


def distinct_rows(v): return len({tuple(r) for r in v})


_write_lock_note = "atomic append; single process per file assumed within a run"


def record_elite(cell, count, values):
    line = json.dumps({"cell": list(cell), "count": count, "values": values}) + "\n"
    with open(ELITES, "a") as f:
        f.write(line)
        f.flush()
        os.fsync(f.fileno())


def perturb(v, m, rnd):
    """Single-cell step/resample, or a coupled row-preserving 2-cell move."""
    n = len(v)
    trial = [list(r) for r in v]
    r = rnd.random()
    if r < 0.45:
        # single-cell +/- step
        i, g = rnd.randrange(n), rnd.randrange(m)
        step = rnd.choice([-5, -3, -2, -1, 1, 2, 3, 5])
        trial[i][g] = max(1, min(VMAX, trial[i][g] + step))
    elif r < 0.70:
        # single-cell full resample
        i, g = rnd.randrange(n), rnd.randrange(m)
        trial[i][g] = rnd.randint(1, VMAX)
    else:
        # coupled 2-cell move in one row: shift value between two goods (row-preserving-ish)
        i = rnd.randrange(n)
        g1, g2 = rnd.sample(range(m), 2)
        d = rnd.choice([1, 2, 3, 5])
        trial[i][g1] = max(1, min(VMAX, trial[i][g1] + d))
        trial[i][g2] = max(1, min(VMAX, trial[i][g2] - d))
    return trial


def anneal(seed, m, steps, rng, cell, state):
    """One annealing run. `state` holds cross-run best {count, values} for elite writes."""
    rnd = random.Random(rng)
    cur = [list(r) for r in seed]
    if len(cur[0]) != m:
        cur = [ (r + [rnd.randint(1, VMAX)] * m)[:m] for r in cur ]
    cnt, sl, _ = count_and_slack(cur)
    curobj = objective(cnt, sl)
    best, bestcnt, bestobj = [list(r) for r in cur], cnt, curobj
    T0, T1 = 5.0, 0.02
    stale = 0
    for t in range(steps):
        T = T0 * (T1 / T0) ** (t / steps)
        trial = perturb(cur, m, rnd)
        if distinct_rows(trial) < 5:
            continue
        cnt, sl, _ = count_and_slack(trial)
        obj = objective(cnt, sl)
        if obj <= curobj or rnd.random() < math.exp((curobj - obj) / max(T, 1e-6)):
            cur, curobj = trial, obj
            if obj < bestobj - 1e-12:
                best, bestcnt, bestobj = [list(r) for r in trial], cnt, obj
                stale = 0
                if cnt < state["count"]:
                    state["count"] = cnt
                    state["values"] = [list(r) for r in trial]
                    record_elite(cell, cnt, state["values"])
                    print(f"  [rng{rng}] NEW ELITE count={cnt} obj={obj:.3f} step={t}", flush=True)
            else:
                stale += 1
        else:
            stale += 1
        if stale and t % 400 == 399:
            cur, curobj = [list(r) for r in best], bestobj
            stale = 0
        if bestcnt < 5:
            print(f"  [rng{rng}] SUB-5 count={bestcnt} -- stopping run", flush=True)
            break
    return best, bestcnt, bestobj
