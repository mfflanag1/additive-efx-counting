"""Potential-function route to the coupling conjecture.

For each instance, enumerate all n^m allocations once, recording each allocation's
utility vector and EFX0 status. Then extract canonical maximizers (utilitarian, Nash,
egalitarian/leximin, and an EFX0-tailored 'min-strong-envy' potential) and check whether
the canonical allocation is EFX0. A rule that is EFX0 on 100% of instances (esp. the
near-witnesses and un-parkable configs) is a candidate proof skeleton.
"""
import sys, random, json
from math import log
sys.path.insert(0, ".")
from verify import precompute, check_allocation


def analyze_instance(V, n, m):
    val, minall, minpos = precompute(n, m, V)
    assign = [0] * m
    best = {}  # rule -> (key, is_efx0)
    any_efx0 = False
    while True:
        bd = [0] * n
        for g in range(m):
            bd[assign[g]] |= 1 << g
        util = [val[i][bd[i]] for i in range(n)]
        e0 = check_allocation(n, bd, val, minall, minpos)[0]
        any_efx0 = any_efx0 or e0
        # rule keys (all "maximize")
        util_k = sum(util)
        nash_k = sum(log(u) if u > 0 else -1e9 for u in util)
        egal_k = tuple(sorted(util))  # leximin: maximize sorted-ascending vector lexicographically
        # min-strong-envy potential: minimize total strong-envy magnitude -> maximize its negation
        se = 0
        for i in range(n):
            for j in range(n):
                if i == j or bd[j] == 0:
                    continue
                thr = val[i][bd[j]] - (0 if minall[i][bd[j]] == float("inf") else minall[i][bd[j]])
                if util[i] < thr:
                    se += thr - util[i]
        se_k = -se
        for rule, k in (("util", util_k), ("nash", nash_k), ("egal", egal_k), ("minse", se_k)):
            if rule not in best or k > best[rule][0]:
                best[rule] = (k, e0)
        g = 0
        while g < m:
            assign[g] += 1
            if assign[g] < n:
                break
            assign[g] = 0
            g += 1
        else:
            break
    return any_efx0, {r: best[r][1] for r in best}


def sweep(trials, n=4, m=8, vmax=25, seed=1):
    rng = random.Random(seed)
    rules = ["util", "nash", "egal", "minse"]
    ok = {r: 0 for r in rules}
    fails = {r: [] for r in rules}
    total = 0
    no_efx0 = 0
    for t in range(trials):
        V = [[rng.randint(1, vmax) for _ in range(m)] for _ in range(n)]
        any0, res = analyze_instance(V, n, m)
        if not any0:
            no_efx0 += 1
            print("*** INSTANCE WITH NO EFX0 (counterexample!) ***", json.dumps(V), flush=True)
            continue
        total += 1
        for r in rules:
            if res[r]:
                ok[r] += 1
            elif len(fails[r]) < 3:
                fails[r].append(V)
    print(f"instances with EFX0: {total}, NO-EFX0: {no_efx0}")
    for r in rules:
        print(f"  rule {r}: canonical allocation is EFX0 in {ok[r]}/{total}")
    for r in rules:
        if fails[r]:
            print(f"  {r} first failure:", json.dumps(fails[r][0]))
    return ok, total


if __name__ == "__main__":
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    # also test the near-witnesses explicitly
    NW = {
        "count4": [[11,8,20,1,4,1,16,1],[16,49,32,2,16,2,60,1],[28,28,59,1,60,7,46,8],[10,12,24,1,59,1,17,1]],
        "count5": [[11,8,20,1,4,1,16,1],[16,49,32,2,16,2,60,1],[16,40,59,1,60,7,46,8],[10,12,24,1,59,1,17,1]],
        "srcless": [[8,10,18,12,6,12,19,1],[5,7,3,3,10,10,12,1],[6,9,7,4,7,11,20,1],[8,3,5,20,7,16,15,1]],
    }
    print("=== near-witnesses ===")
    for name, V in NW.items():
        any0, res = analyze_instance(V, 4, 8)
        print(f"  {name}: any_efx0={any0} canonical-EFX0={res}")
    print("=== random sweep ===")
    sweep(trials)
