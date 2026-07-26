"""Collect ALL surviving EFX0 allocations for a given instance and characterize them:
bundle-size distribution, and per-agent value received. Points at what to kill."""
import json
import sys
from collections import Counter
from verify import precompute, check_allocation

inst = json.loads(sys.argv[1]) if len(sys.argv) > 1 else None
if inst is None:
    # default: stair-rot2-s1
    base = [20, 15, 11, 8, 6, 4, 2, 1]
    vals = [base[(2*i):] + base[:(2*i)] for i in range(4)]
    inst = {"n": 4, "m": 8, "values": vals}

n, m, values = inst["n"], inst["m"], inst["values"]
val, minall, minpos = precompute(n, m, values)

size_patterns = Counter()
survivors = []
assign = [0]*m
while True:
    bundles = [0]*n
    for g in range(m):
        bundles[assign[g]] |= 1 << g
    e0, ep = check_allocation(n, bundles, val, minall, minpos)
    if e0:
        sizes = tuple(sorted(bin(b).count("1") for b in bundles))
        size_patterns[sizes] += 1
        survivors.append(list(assign))
    g = 0
    while g < m:
        assign[g] += 1
        if assign[g] < n:
            break
        assign[g] = 0
        g += 1
    else:
        break

print("total EFX0:", len(survivors))
print("size patterns:", dict(size_patterns.most_common()))
# per-agent value received distribution among survivors
print("\nsample survivors (assign vectors, own values):")
for s in survivors[:12]:
    bundles = [0]*n
    for g in range(m):
        bundles[s[g]] |= 1 << g
    owns = [val[i][bundles[i]] for i in range(n)]
    parts = [[g for g in range(m) if s[g]==i] for i in range(n)]
    print("  ", parts, "own_vals=", owns)
