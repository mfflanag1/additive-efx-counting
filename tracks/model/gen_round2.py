"""Round 2: exploit staircase-rotation disagreement (best mechanism, 184) while breaking
the C4 symmetry that lets 82 balanced (2,2,2,2) splits survive as EFX0.
Strategies: (a) two alternating base vectors, (b) non-uniform rotation offsets,
(c) steepness sweep, (d) one perturbed agent, (e) asymmetric-total rows."""
import json

cands = []
def add(name, values, rationale, m=8):
    assert len(values) == 4 and all(len(r) == m for r in values)
    for r in values:
        assert all(1 <= x <= 60 for x in r), (name, r)
    assert len({tuple(r) for r in values}) == 4, ("dup rows", name)
    assert len({x for r in values for x in r}) >= 3
    cands.append({"name": name, "n": 4, "m": m, "values": values, "rationale": rationale})

def rot(v, d): return v[d:] + v[:d]

# (c) steepness sweep around s1 (base descending, rot2 per agent)
for tag, base in [
    ("g185", [21, 16, 12, 9, 6, 4, 2, 1]),
    ("g19",  [22, 16, 11, 8, 5, 3, 2, 1]),
    ("g20",  [20, 14, 10, 7, 5, 3, 2, 1]),
    ("g21",  [26, 18, 12, 8, 5, 3, 2, 1]),
    ("g22",  [19, 15, 12, 9, 7, 5, 3, 1]),
    ("g23",  [23, 17, 12, 8, 5, 3, 2, 1]),
]:
    add(f"stair-sweep-{tag}", [rot(base, (2*i) % 8) for i in range(4)],
        f"steepness sweep {base}, rot2; fine-tune around the 184 optimum")

# (b) non-uniform rotation offsets (break translational symmetry of the peaks)
base = [20, 15, 11, 8, 6, 4, 2, 1]
for tag, offs in [("o0356", [0,3,5,6]), ("o0246v", [0,2,5,7]), ("o0147", [0,1,4,7]),
                  ("o0257", [0,2,5,7]), ("o0356b", [0,3,4,7])]:
    vals = [rot(base, o) for o in offs]
    if len({tuple(v) for v in vals}) == 4:
        add(f"stair-offs-{tag}", vals, f"staircase base rotated by non-uniform offsets {offs}; asymmetric peak spacing")

# (a) two alternating base vectors (C4 -> C2, disrupts balanced pairing symmetry)
A = [20, 15, 11, 8, 6, 4, 2, 1]
B = [22, 14, 10, 7, 5, 3, 2, 1]
add("stair-twobase-AB",
    [rot(A, 0), rot(B, 2), rot(A, 4), rot(B, 6)],
    "agents 0,2 use base A; 1,3 use base B (both steep, slightly different); breaks C4->C2 symmetry")
C = [24, 16, 11, 7, 5, 3, 2, 1]
add("stair-twobase-AC",
    [rot(A, 0), rot(C, 2), rot(A, 4), rot(C, 6)],
    "two-base with a steeper alternate C; disrupt the 82 balanced splits")

# (d) staircase with one agent perturbed (targeted asymmetry)
def perturb_agent(base_rows, i, deltas):
    rows = [list(r) for r in base_rows]
    for g, d in enumerate(deltas):
        rows[i][g] = max(1, min(60, rows[i][g] + d))
    return rows
S1 = [rot(A, (2*i) % 8) for i in range(4)]
add("stair-perturb-a0",
    perturb_agent(S1, 0, [3, -2, 0, 0, 1, 0, 0, -1]),
    "s1 staircase with agent 0's row nudged to break the symmetric balanced splits")
add("stair-perturb-a0a2",
    perturb_agent(perturb_agent(S1, 0, [2,-2,0,1,0,0,0,-1]), 2, [0,1,-2,0,2,-1,0,0]),
    "s1 with agents 0 and 2 nudged in opposite senses; break C2 residue too")

# (e) asymmetric per-agent totals: scale rows so 'fair shares' don't align
add("stair-scaled-totals",
    [rot(A, 0),
     [int(round(x*1.15)) for x in rot(A, 2)],
     [max(1,int(round(x*0.9))) for x in rot(A, 4)],
     [int(round(x*1.05)) for x in rot(A, 6)]],
    "staircase rows scaled by distinct factors so no common fair-share value -> fewer balanced EFX")

# (f) 'contested staircase': top of each staircase overlaps a neighbor's top strongly
# use base where 2nd and 3rd values are high (broad high shoulder) but still strictly descending
add("stair-broad-shoulder",
    [rot([20, 18, 16, 8, 5, 3, 2, 1], (2*i) % 8) for i in range(4)],
    "broad high shoulder (20,18,16) rotated: an agent's 2nd/3rd goods are others' tops -> heavy contest, still strictly descending (distinct ranks)")

# m=9 with staircase disagreement, but 9th good is a HIGH contested good (not a low crumb)
A9 = [20, 15, 11, 8, 6, 4, 2, 1]
add("stair-m9-highgood",
    [rot(A9, (2*i) % 8) + [17] for i in range(4)],
    "staircase rot2 + 9th good valued HIGH (17) by all -> a single super-contested good that no split can place without envy", m=9)
add("stair-m9-highgood-rotval",
    [rot(A9, (2*i) % 8) + [v] for i, v in zip(range(4), [18, 13, 18, 13])],
    "m9, 9th good high but valued differently per agent to break symmetry", m=9)

with open("tracks/model/round2.jsonl", "w") as f:
    for c in cands:
        f.write(json.dumps(c) + "\n")
print(f"wrote {len(cands)} candidates")
