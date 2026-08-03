# Bottom-Pair Multiplicity Gate

**Status:** closed structural gate; all canonical patterns proof-checked  
**Scope:** four additive agents, nine goods, a strict common favorite, and
universal owner-threshold failure  
**Not claimed:** complete EFX for four agents and nine goods, for all four-
agent instances, or in general

## Reduction now available

The proof-checked
[three-agent-bottom conversion theorem](THREE_AGENT_BOTTOM_PAIRING_CONVERSION_THEOREM.md)
closes every profile in which some residual pair is jointly bottom-two for at
least three agents. Select one bottom pair for each agent in the remaining
branch. No selected pair can occur more than twice, so the four selected
pairs have multiplicity signature

\[
2+2,\qquad 2+1+1,\qquad\text{or}\qquad 1+1+1+1.
\]

Treating residual goods as vertices and selected bottom pairs as edges gives
a loopless four-edge multigraph with edge multiplicity at most two. Exhaustive
canonicalization of all 30,681 labeled edge multisets leaves exactly 20
unlabeled patterns:

| Multiplicity signature | Canonical patterns |
|---|---:|
| $2+2$ | 2 |
| $2+1+1$ | 7 |
| $1+1+1+1$ | 11 |

The deterministic record is
[efx49_bottom_pair_pattern_census_audit.json](efx49_bottom_pair_pattern_census_audit.json).
It proves only the census, not an EFX selector.

## The first surviving case: $2+2$

The two repeated bottom pairs are either disjoint or share one good. If a
favorite-triple Hall cell for each pair is not full, choose one failed perfect
pairing in each cell. Goods symmetry reduces the relative pair of matchings to

| Bottom-pair geometry | Relative matching orbits |
|---|---:|
| disjoint | 9 |
| overlapping | 4 |

For each orbit, the first local candidate obstructs the twelve conversions
obtained by applying the six-conversion menu separately to the two cells.
Exact QF_LRA gives the following current census.

| Geometry | Local result |
|---|---|
| disjoint | `unsat` in orbits 0, 1, 2, 3, 4, and 6; `sat` in 5, 7, and 8 |
| overlapping | `sat` in all four orbits |

The six `unsat` endpoints are Z3 proof candidates, not yet independently
proof-checked. The seven `sat` endpoints refute only the twelve-conversion
menu. The four overlapping models remain inside the intended residual
branch: none has a three-agent bottom pair or a full Hall cell, while they
retain 222--335 favorite-pair repairs and 937--1,330 complete EFX
allocations. They are positive structural boundaries, not EFX
counterexamples.

### Disjoint $2+2$ pattern closed

The larger 180-partition conversion closure eliminates the three hard local
orbits and closes the entire disjoint geometry. Exact CEGAR selected a
72-partition sufficient pool. Both cardinal and sorting encodings returned
`unsat` in Z3; cvc5 independently returned `unsat`; and cvc5's 35.2 MB CPC
proof was checked by Ethos as `correct`. Therefore, under the scope of this
gate, two disjoint bottom pairs each shared by two agents force either a full
selected Hall cell or a complete EFX conversion.

The proof-checked statement and aggregate audit are
[the disjoint double-bottom theorem](DISJOINT_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md)
and
[efx49_disjoint_double_bottom_pair_conversion_audit.json](efx49_disjoint_double_bottom_pair_conversion_audit.json).
This closes the disjoint $2+2$ multigraph pattern. The overlapping pattern
is closed separately below; the lower-multiplicity cases remain open.

The overlap geometry supplies one additional invariant: the shared good is
bottom-two for every agent. Two symmetry-closed repair families exposed by
the exact boundaries are therefore natural:

1. 315 favorite-pair partitions with the shared bottom good in the triple;
2. 420 partitions with that good either in the triple or paired with the
   common favorite.

Every initial overlap boundary has 158--231 repairs in the 315-family. At
the sharpest learned profiles, all surviving repairs lie in the 420-family;
the 315-family contributes 3 of 7, 12 of 21, 7 of 13, and 6 of 13 repairs in
the four orbits. This is exact profile evidence for a concise cross-pair
lemma, not a proof of either family.

The 420-family has now crossed the solver-confirmation boundary in relative
matching orbit 1. A 107-partition CEGAR pool is `unsat` under the cardinal Z3
encoding, and cvc5 independently returned `unsat` on the syntax-normalized
sorting formula in 1,160.7 seconds. The sorting formula itself timed out in
Z3, which has no negative evidentiary weight. cvc5 emitted a 52,152,488-byte
CPC proof with 631,679 proof steps, and Ethos checked it as `correct`.
The aggregate record is
[efx49_overlap_orbit1_shared_active_audit.json](efx49_overlap_orbit1_shared_active_audit.json).
Orbit 0 remains at an iteration limit with seven survivors at the sharpest
recorded step, while orbits 2 and 3 remain `unknown`; consequently this is a
proof-checked one-orbit theorem, not a closure of the overlapping pattern.

Primary exact records are
[the cardinal Z3 candidate](efx49_two_pair_bottom_cross_overlap_orbit1_shared_active_cegar_session1.json),
[the sorting-formula Z3 timeout](efx49_two_pair_bottom_cross_overlap_orbit1_shared_active_sorting_z3.json),
[the successful cvc5 replay](efx49_two_pair_bottom_cross_overlap_orbit1_shared_active_cvc5.json),
and the
[CPC/Ethos certificate](efx49_two_pair_bottom_cross_overlap_orbit1_shared_active_cpc_ethos.json).

Primary local records include
[disjoint orbit 5](efx49_two_pair_bottom_cross_conversion_disjoint_orbit5_session1.json),
[disjoint orbit 7](efx49_two_pair_bottom_cross_conversion_disjoint_orbit7_session1.json),
[disjoint orbit 8](efx49_two_pair_bottom_cross_conversion_disjoint_orbit8_session1.json),
and overlapping
[orbit 0](efx49_two_pair_bottom_cross_conversion_overlap_session1.json),
[orbit 1](efx49_two_pair_bottom_cross_conversion_overlap_orbit1_session1.json),
[orbit 2](efx49_two_pair_bottom_cross_conversion_overlap_orbit2_session1.json),
and
[orbit 3](efx49_two_pair_bottom_cross_conversion_overlap_orbit3_session1.json).

### Overlapping $2+2$ pattern closed

The full 165-partition conversion closure also closes the overlapping
geometry. A theorem-preserving 960-element canonicalization orders agents
inside the two repeated-pair blocks, orders the five free goods, and selects
one of the two mirrored sides. The complete formula is `unsat` in the
cardinality Z3 encoding, in a fresh Z3 replay, in the independent
sorting-network Z3 encoding, and in pinned cvc5. cvc5 emitted a
68,745,739-byte, 767,596-step CPC proof, which Ethos checked as `correct`.

The proof-checked statement and aggregate audit are
[the overlapping double-bottom theorem](OVERLAP_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md)
and
[efx49_overlap_double_bottom_pair_conversion_audit.json](efx49_overlap_double_bottom_pair_conversion_audit.json).
Together with the disjoint theorem, this closes both $2+2$ patterns.

### First $2+1+1$ pattern closed

The triangle-with-doubled-edge pattern

\[
\{a,b\},\ \{a,b\},\ \{a,c\},\ \{b,c\}
\]

is also closed by its complete 225-partition conversion family. A
theorem-preserving 480-element canonicalization swaps the agents on the
repeated edge, orders the five free goods, and reflects the two singleton
edges. Cardinal Z3, a fresh-process Z3 replay, independent sorting-network
Z3, and pinned cvc5 all returned `unsat`. cvc5 emitted a 35,862,508-byte,
408,508-step CPC proof, and Ethos checked it as `correct`.

The proof-checked statement and aggregate audit are
[the triangle repeated-edge theorem](TRIANGLE_REPEATED_BOTTOM_PAIR_CONVERSION_THEOREM.md)
and
[efx49_triangle_repeated_bottom_pair_conversion_audit.json](efx49_triangle_repeated_bottom_pair_conversion_audit.json).
This closes one of the seven $2+1+1$ patterns.

### Second $2+1+1$ pattern closed

The three-leaf-star pattern

\[
\{a,b\},\ \{a,b\},\ \{a,c\},\ \{a,d\}
\]

is closed by its complete 228-partition conversion family. A
theorem-preserving 96-element canonicalization swaps the agents on the
repeated edge, orders the four free goods, and exchanges the two singleton
leaves. Cardinal Z3, a fresh-process Z3 replay, independent sorting-network
Z3, and pinned cvc5 all returned `unsat`. cvc5 emitted a 51,302,181-byte,
602,783-step CPC proof, and Ethos checked it as `correct`.

The proof-checked statement and aggregate audit are
[the star repeated-edge theorem](STAR_REPEATED_BOTTOM_PAIR_CONVERSION_THEOREM.md)
and
[efx49_star_repeated_bottom_pair_conversion_audit.json](efx49_star_repeated_bottom_pair_conversion_audit.json).
This closes a second of the seven $2+1+1$ patterns.

### Both repeated-edge path patterns closed

The central-edge and end-edge path patterns

\[
\{a,b\},\{a,b\},\{a,c\},\{b,d\}
\quad\text{and}\quad
\{a,b\},\{a,b\},\{a,c\},\{c,d\}
\]

are each closed by their complete 240-partition conversion families. Their
formula symmetry groups have 96 and 48 actions. For both cells, cardinal Z3,
a fresh-process Z3 replay, sorting-network Z3, and pinned cvc5 returned
`unsat`; Ethos accepted CPC proofs with 586,111 and 333,221 proof steps.

The statements and primary audits are collected in
[the path repeated-edge theorems](PATH_REPEATED_BOTTOM_PAIR_CONVERSION_THEOREMS.md),
[the central-edge audit](efx49_bottom_pattern3_conversion_audit.json), and
[the end-edge audit](efx49_bottom_pattern4_conversion_audit.json).
Four of the seven $2+1+1$ patterns are now proof-checked.

### All remaining $2+1+1$ patterns closed

The remaining geometries are a wedge plus a detached edge, a repeated edge
plus a detached two-edge fork, and three disconnected edges:

\[
\{a,b\},\{a,b\},\{a,c\},\{d,e\},\qquad
\{a,b\},\{a,b\},\{c,d\},\{c,e\},\qquad
\{a,b\},\{a,b\},\{c,d\},\{e,g\}.
\]

Their complete conversion families contain 255, 255, and 270 partitions.
All three passed cardinal Z3, fresh-process Z3, sorting-network Z3, pinned
cvc5, and CPC/Ethos checking. Their checked proofs contain 262,384, 166,744,
and 152,810 proof steps.

The exhaustive seven-case aggregate is
[the repeated bottom-pair exclusion theorem](REPEATED_BOTTOM_PAIR_EXCLUSION_THEOREM.md)
with machine audit
[efx49_all_repeated_bottom_pair_conversions_audit.json](efx49_all_repeated_bottom_pair_conversions_audit.json).
All seven $2+1+1$ patterns are now proof-checked.

### First $1+1+1+1$ pattern closed

The maximally disconnected geometry

\[
\{a,b\},\{c,d\},\{e,g\},\{h,k\}
\]

is closed by its complete 360-partition conversion family. Its exact
relabeling group has 384 actions, and the family has four allocation orbits
of sizes 24, 48, 96, and 192. Cardinal Z3, sorting-network Z3, a fresh Z3
replay, and pinned cvc5 all returned `unsat`; Ethos accepted cvc5's
27,789,102-byte, 339,968-step CPC proof.

Proof mining reduces the complete family to a canonical six-partition core
drawn entirely from the largest conversion orbit. The compact 355 KB
formula is independently `unsat` in cvc5, whose 8,863,864-byte,
112,158-step CPC proof is also accepted by Ethos. Six deletion solves show
the core is deletion-minimal. Without the relabeling
cuts the same six labeled partitions admit an exact SAT boundary, so the
canonicalization is a substantive WLOG step in the concise lemma.

The statement and proof audit are
[the four-disconnected-pairs theorem](FOUR_DISCONNECTED_BOTTOM_PAIRS_CONVERSION_THEOREM.md)
and
[efx49_bottom_pattern19_conversion_audit.json](efx49_bottom_pattern19_conversion_audit.json).
This closes one of the eleven $1+1+1+1$ patterns.

### Second $1+1+1+1$ pattern closed

The four-cycle geometry

\[
\{a,b\},\{a,c\},\{b,d\},\{c,d\}
\]

is closed by its complete 300-partition conversion family. Its 192-action
symmetry group splits the family into five orbits of sizes 12, 48, 48, 96,
and 96. Cardinal Z3, sorting-network Z3, a fresh Z3 replay, and pinned cvc5
all returned `unsat`; Ethos accepted cvc5's 58,694,950-byte,
696,642-step CPC proof.

The statement and proof audit are
[the four-cycle theorem](FOUR_CYCLE_BOTTOM_PAIRS_CONVERSION_THEOREM.md) and
[efx49_bottom_pattern14_conversion_audit.json](efx49_bottom_pattern14_conversion_audit.json).
This closes a second of the eleven $1+1+1+1$ patterns.

## Historical global zero-repair boundary

The theorem actually needed is weaker than a universal local conversion:

> If no favorite-pair partition supports EFX, two bottom pairs shared by
> complementary pairs of agents cannot both have a Hall-failed residual
> pairing.

Closing this statement in all 13 relative matching orbits would have settled
both $2+2$ multigraph patterns. The smaller full conversion closures above
have now settled them instead; the 840-state experiments below remain useful
historical scaling evidence.

The direct 840-partition encodings for the three hard disjoint orbits returned
`unknown` after 300 seconds. A 445-cut seeded CEGAR master also timed out in
each orbit. Starting from only the twelve local conversions produced one
model per orbit with 224--253 additional repairs; the next 76-cut masters
returned `unknown`. These are honest scaling boundaries, not evidence of
UNSAT and not counterexamples.

The coarser selected-cell encoding tells the same story. Direct exact-real
searches for the two canonical $2+2$ multigraph patterns found first models
with 651 and 781 repairs and no full Hall cell; their 128-cut continuations
returned `unknown`. Monolithic split-bottom searches with a 768-partition
pool also timed out after 600 seconds in both geometries.

Targeted adversarial search has now compressed the overlapping pattern much
further. Three stochastic runs and a separate cap-100 CP-SAT optimization
each produce a distinct profile with exactly three
favorite-pair repairs, no full Hall cell, no three-agent bottom pair, and 180
labeled complete EFX allocations. In every profile, one selected cell has
exactly 12 Hall-valid and three Hall-failed pairings, the other selected cell
has zero Hall-valid pairings, and the three failures share one residual edge.
Each failure has exactly one converted repair, and those three conversions
are the profile's complete favorite-pair repair set. The ordered
three-repair agent--bundle feasibility-graph signature agrees across all four
profiles.
The hash-pinned replay is
[efx49_overlap22_three_repair_motif_audit.json](efx49_overlap22_three_repair_motif_audit.json).

The CP-SAT run achieves objective 837 of 840 with best bound 840, so it does
not certify optimality. This replicated equality case is strong proof-mining
evidence, not a proof of a three-repair floor. A zero-repair profile would refute the
favorite-pair/full-cell selector while still retaining the possibility of
complete EFX in another balanced state.

All four sharp profiles survive a deterministic 960-element canonicalization
of the overlap pattern. The group orders agents within each repeated-pair
block, orders the five free goods, and identifies the two mirrored sides.
Every one of their three repairs lies in the same size-60 conversion orbit
(orbit 3 of sizes 15, 60, 30, 60). The full symmetry-reduced 165-partition
cardinality formula has now returned `unsat` in Z3 after 543.8 seconds. This
verdict was reproduced by a fresh Z3 process in 753.2 seconds, and the
independent sorting-network formula returned `unsat` in Z3 after 697.6
seconds. Pinned cvc5 independently returned `unsat` on the normalized
sorting formula in 672.4 seconds. The proof gate also passed: cvc5's
68,745,739-byte proof contains 767,596 proof-step lines, and Ethos returned
`correct`. The symmetry and exact boundary audit is
[efx49_overlap22_pattern_symmetry_audit.json](efx49_overlap22_pattern_symmetry_audit.json).

## Gate closure and next target

Both $2+2$ patterns, all seven $2+1+1$ patterns, and all eleven
$1+1+1+1$ patterns are now proof-checked. Every all-distinct case has two
exact-real Z3 encodings, a fresh-process Z3 replay, an independent pinned
cvc5 replay, and a CPC derivation accepted as `correct` by Ethos. The
eleven-case aggregate is
[efx49_all_distinct_bottom_pair_conversions_audit.json](efx49_all_distinct_bottom_pair_conversions_audit.json).

Together with the three-agent-bottom theorem, the 20-pattern census now
closes the entire strict-common-favorite/universal-owner-threshold-failure
branch. The theorem and class audit are
[COMMON_FAVORITE_UNIVERSAL_THRESHOLD_EFX_THEOREM.md](COMMON_FAVORITE_UNIVERSAL_THRESHOLD_EFX_THEOREM.md)
and
[efx49_common_favorite_universal_threshold_efx_audit.json](efx49_common_favorite_universal_threshold_efx_audit.json).
The next common-favorite target is the mixed branch where some
favorite-singleton owner passes the scalar threshold but the residual
three-agent feasibility graph is Hall-deficient.

The completed conversion closures have small allocation-orbit censuses:

| Geometry | Automorphisms | Conversion-orbit sizes |
|---|---:|---|
| overlapping | 240 | 15, 60, 30, 60 |
| disjoint | 192 | 12, 96, 24, 48 |
| triangle with doubled edge | 240 | 30, 60, 60, 15, 60 |
| three-leaf star with doubled edge | 48 | 12, 3, 24, 12, 24, 6, 12, 3, 24, 6, 12, 6, 24, 24, 12, 24 |
| central-edge path | 48 | 6, 24, 12, 24, 24, 24, 12, 24, 6, 24, 24, 12, 24 |
| end-edge path | 24 | 3, 12, 6, 12, 12, 12, 6, 12, 3, 12, 12, 6, 12, 6, 3, 12, 12, 12, 12, 6, 12, 6, 3, 12, 12, 12 |
| wedge plus detached edge | 12 | 41 orbits, sizes 3, 6, or 12 |
| repeated edge plus detached fork | 24 | 24 orbits, sizes 3, 6, 12, or 24 |
| three disconnected edges | 32 | 20 orbits, sizes 2, 4, 8, 16, or 32 |
| all-distinct four-cycle | 192 | 12, 48, 48, 96, 96 |
| all-distinct perfect matching | 384 | 24, 48, 96, 192 |

The deterministic records are
[the overlapping orbit audit](efx49_bottom_pattern0_conversion_orbit_audit.json)
and
[the disjoint orbit audit](efx49_bottom_pattern6_conversion_orbit_audit.json),
with the seven closed $2+1+1$ censuses and proof records aggregated in
[efx49_all_repeated_bottom_pair_conversions_audit.json](efx49_all_repeated_bottom_pair_conversions_audit.json).
Representative component censuses include
[the triangle orbit audit](efx49_bottom_pattern2_conversion_orbit_audit.json)
and
[the star orbit audit](efx49_bottom_pattern1_conversion_orbit_audit.json),
[the central-path orbit audit](efx49_bottom_pattern3_conversion_orbit_audit.json),
and
[the end-path orbit audit](efx49_bottom_pattern4_conversion_orbit_audit.json).
The smaller orbit censuses suggest concise human templates for several
geometries; the 24- and 41-orbit cases show where a graph-independent lemma
would add the most value. Core mining can still shorten their analytic
exposition, but it is no longer a mathematical gate. The first guarded
overlap core has size 97, distributed
6, 12, 28, and 51 across the four orbits; its unguarded 1,200-second replay
timed out, so it is not promoted beyond proof-mining evidence. The next
analytic step is to compress the certified all-distinct cases into a
graph-independent Hall-witness conversion proof.

No solver timeout or finite census in this note is promoted to an existence
theorem.
