"""Hill-climb integer value matrices to MINIMIZE efx0_count (0 = witness).
Legitimate model-driven construction: seed from best hand structures, perturb single
entries, keep positive ints in [1,60]. Enforces live-region constraints softly by
seeding from valid structures; reports if any seed reaches a small count.
Usage: python3 hillclimb.py <seed_tag> <steps> <seed_json?>"""
import json
import random
import sys
from verify import enumerate_all

random.seed(12345)


def count(vals, m):
    return enumerate_all(4, m, vals)["efx0_count"]


def distinct_rows(vals):
    return len({tuple(r) for r in vals})


def climb(seed, m, steps, cap=60):
    vals = [list(r) for r in seed]
    best = count(vals, m)
    hist = [best]
    for t in range(steps):
        i = random.randrange(4)
        g = random.randrange(m)
        old = vals[i][g]
        delta = random.choice([-3, -2, -1, 1, 2, 3])
        nv = old + delta
        if nv < 1 or nv > cap:
            continue
        vals[i][g] = nv
        if distinct_rows(vals) < 4:
            vals[i][g] = old
            continue
        c = count(vals, m)
        # accept improvements; accept equal with small prob to cross plateaus
        if c < best or (c == best and random.random() < 0.3):
            best = c
            hist.append(best)
        else:
            vals[i][g] = old
    return vals, best, hist


if __name__ == "__main__":
    tag = sys.argv[1]
    steps = int(sys.argv[2])
    seed = json.loads(sys.argv[3])
    m = len(seed[0])
    vals, best, hist = climb(seed, m, steps)
    print(json.dumps({"tag": tag, "best": best, "values": vals,
                      "distinct_rows": distinct_rows(vals),
                      "improvements": len(hist)}))
