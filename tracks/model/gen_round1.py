"""Round 1 generator: diverse structural families for the EFX additive n=4,m=8/9 hunt.
Goal: instances where every complete allocation has some agent strongly-envying.
Key: strong envy needs v_i(X_j)-v_i(X_i) > max_{g in X_j} v_i(g) -> want envied bundles
made of many near-equal middling goods (thin cushion) yet valued far above own bundle.
Positive ints only, <= 60."""
import json


def rot(vec, d):
    return vec[d:] + vec[:d]


def clamp_row(r):
    return [max(1, min(60, int(round(x)))) for x in r]


cands = []


def add(name, values, rationale, m=8):
    n = 4
    assert len(values) == 4 and all(len(r) == m for r in values)
    for r in values:
        assert all(1 <= x <= 60 for x in r), (name, r)
    cands.append({"name": name, "n": n, "m": m, "values": values, "rationale": rationale})


# ---- Family 1: staircase rotations (exploit the 184 winner) ----
# base descending vector rotated by offset 2 per agent (period 8 covers 4 agents)
for tag, base in [
    ("s1", [20, 15, 11, 8, 6, 4, 2, 1]),
    ("s2", [30, 22, 15, 10, 6, 4, 2, 1]),
    ("s3", [18, 16, 13, 10, 7, 5, 3, 1]),   # flatter top -> thinner cushion
    ("s4", [24, 20, 17, 14, 11, 8, 5, 2]),  # near-linear, flat
    ("s5", [40, 25, 15, 9, 5, 3, 2, 1]),    # steep
    ("s6", [14, 13, 12, 11, 9, 6, 3, 1]),   # very flat top block
]:
    vals = [rot(base, (2 * i) % 8) for i in range(4)]
    add(f"stair-rot2-{tag}", vals, f"descending {base}, rot by 2 per agent; flat-top variants shrink cushion")

# staircase with rotation offset 1 and 3 (shear the overlap pattern)
for d in (1, 3):
    base = [20, 15, 11, 8, 6, 4, 2, 1]
    vals = [rot(base, (d * i) % 8) for i in range(4)]
    add(f"stair-rot{d}-s1", vals, f"staircase rot by {d} per agent; changes which goods overlap as 2nd-choices")

# ---- Family 2: circulant bumps (contested peaks, overlapping 2nd choices) ----
# each row is a circular shift of a bump vector by 2; neighbors share second-favorites
for tag, bump in [
    ("b1", [30, 18, 10, 6, 4, 6, 10, 18]),  # symmetric bump, wide skirts overlap
    ("b2", [40, 20, 8, 3, 2, 3, 8, 20]),    # sharp peak, big skirts
    ("b3", [25, 22, 15, 8, 4, 8, 15, 22]),  # broad plateau -> thin cushion, high contest
    ("b4", [50, 12, 5, 2, 1, 2, 5, 12]),    # very sharp
]:
    vals = [rot(bump, (2 * i) % 8) for i in range(4)]
    add(f"circulant-bump-{tag}", vals, f"circulant bump {bump} shift2; every good is someone's peak, skirts overlap 2nd choices")

# ---- Family 3: poison pairs (two goods jointly enormous for one agent) ----
# agent i loves pair {2i,2i+1}; but the pairs are also 2nd-loved by neighbor -> contested
add("poison-pairs-overlap",
    [[28, 28, 20, 3, 3, 3, 3, 20],
     [20, 20, 28, 28, 20, 3, 3, 3],
     [3, 3, 20, 20, 28, 28, 20, 3],
     [3, 3, 3, 3, 20, 20, 28, 28]],
    "each agent's loved pair (28) is 2nd-loved (20) by a neighbor; forces contest for high pairs")
add("poison-pairs-tight",
    [[26, 26, 24, 5, 5, 5, 5, 24],
     [24, 24, 26, 26, 24, 5, 5, 5],
     [5, 5, 24, 24, 26, 26, 24, 5],
     [5, 5, 5, 5, 24, 24, 26, 26]],
    "poison pairs with near-equal top (26 vs 24) so envied bundle has no dominant good -> thin cushion")

# ---- Family 4: near-proportional common base with targeted breaks ----
base = [12, 12, 12, 12, 12, 12, 12, 12]
def perturb(base, deltas):
    return [b + d for b, d in zip(base, deltas)]
add("near-prop-break1",
    [perturb(base, [6, 6, -4, -4, 2, 2, -4, -4]),
     perturb(base, [-4, -4, 6, 6, 6, 6, -4, -4]),
     perturb(base, [2, 2, -4, -4, 6, 6, 6, 6]),
     perturb(base, [6, 6, 6, 6, -4, -4, 2, 2])],
    "all rows near-uniform 12 with small distinct +6/-4 breaks; thin cushion (near-equal goods), each agent slightly prefers a different pair")
add("near-prop-break2",
    [perturb([15]*8, [5, 4, -6, -6, 1, 1, -6, -6]),
     perturb([15]*8, [-6, -6, 5, 4, 5, 4, -6, -6]),
     perturb([15]*8, [1, 1, -6, -6, 5, 4, 5, 4]),
     perturb([15]*8, [5, 4, 5, 4, -6, -6, 1, 1])],
    "near-uniform 15 with asymmetric small breaks; distinct rows, very thin cushion")

# ---- Family 5: geometric per-agent scales ----
# agent i: values decay geometrically from a personal peak position; sums dominate singletons per-agent differently
add("geom-peak-rot",
    [clamp_row([32, 16, 8, 4, 2, 4, 8, 16]),
     clamp_row([16, 32, 16, 8, 4, 2, 4, 8]),
     clamp_row([8, 4, 2, 4, 8, 16, 32, 16]),
     clamp_row([4, 8, 16, 32, 16, 8, 4, 2])],
    "powers-of-2 bumps at different centers; steep per-agent geometry makes bundle-sums dominate singletons unevenly")

# ---- Family 6: block-overlap (favorite blocks overlap by one good) ----
add("block-overlap-3",
    [[20, 20, 20, 2, 2, 2, 2, 2],
     [2, 2, 20, 20, 20, 2, 2, 2],
     [2, 2, 2, 2, 20, 20, 20, 2],
     [20, 2, 2, 2, 2, 2, 20, 20]],
    "each agent loves a block of 3 (20), blocks overlap by 1 good with next agent; overlap good is doubly contested")
add("block-overlap-flat",
    [[16, 15, 14, 3, 3, 3, 3, 3],
     [3, 3, 16, 15, 14, 3, 3, 3],
     [3, 3, 3, 3, 16, 15, 14, 3],
     [15, 3, 3, 3, 3, 3, 16, 14]],
    "block-of-3 loved but internally near-equal (16/15/14) so no dominant good; overlapping blocks")

# ---- Family 7: two-tier contested top + shared filler ----
add("contested-top4-filler",
    [[24, 6, 6, 6, 10, 10, 10, 10],
     [6, 24, 6, 6, 10, 10, 10, 10],
     [6, 6, 24, 6, 10, 10, 10, 10],
     [6, 6, 6, 24, 10, 10, 10, 10]],
    "each agent uniquely craves 1 of goods 0-3 (24), filler 5-8 flat 10; 2 agents must miss craved good")
add("contested-top4-filler-v2",
    [[30, 8, 8, 8, 12, 12, 11, 11],
     [8, 30, 8, 8, 11, 12, 12, 11],
     [8, 8, 30, 8, 11, 11, 12, 12],
     [8, 8, 8, 30, 12, 11, 11, 12]],
    "stronger craved good (30), filler near-equal 11/12 rotated so filler bundles also mildly contested")

# ---- Family 8: staircase m=9 variants (extra contested crumb / mid good) ----
for tag, base9 in [
    ("m9a", [20, 15, 11, 8, 6, 4, 2, 1, 12]),  # extra mid-value shared good
    ("m9b", [18, 16, 13, 10, 7, 5, 3, 1, 9]),
]:
    vals = [rot(base9[:8], (2 * i) % 8) + [base9[8]] for i in range(4)]
    add(f"stair-m9-{tag}", vals, f"staircase rot2 plus a 9th shared mid good {base9[8]}; odd m breaks parity of balanced split", m=9)

# circulant bump m=9
bump9 = [30, 18, 10, 6, 4, 6, 10, 18]
vals = [rot(bump9, (2 * i) % 8) + [14] for i in range(4)]
add("circulant-bump-m9", vals, "circulant bump plus 9th shared mid good 14; extra contested crumb", m=9)


with open("tracks/model/round1.jsonl", "w") as f:
    for c in cands:
        f.write(json.dumps(c) + "\n")
print(f"wrote {len(cands)} candidates")
