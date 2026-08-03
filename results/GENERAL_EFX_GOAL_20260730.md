# General Additive EFX Goal Ledger

**Snapshot:** 2026-08-01 EDT  
**Goal:** prove complete EFX existence for every finite positive-additive
instance, or produce and rigorously verify a positive-additive
counterexample.  
**Current status:** **open**. No general proof and no additive counterexample
has been obtained.

**August 3 primary gate:** the fixed-radius exchange program is retired even
inside the four-agent identity/unique-defect/full-Hall branch. An exact
positive profile has no improving EFX-with-charity state within three item
relabelings; its first improvement is a connected four-good component
spanning all owners and leading directly to absorption. See
[PARTIAL_THRESHOLD_FULL_UNIQUE_DEFECT_COMPONENT_GATE.md](PARTIAL_THRESHOLD_FULL_UNIQUE_DEFECT_COMPONENT_GATE.md).
The replacement cap-free invariant is now proved in
[GENERAL_TRANSFER_COMPONENT_HYBRID_WALL_LEMMA.md](GENERAL_TRANSFER_COMPONENT_HYBRID_WALL_LEMMA.md):
between any two fixed-charity EFX states, \(\Theta\)-gain is additive over
transfer components, and every infeasible partial component has a wall
crossing to another component with an exact strict row-wise polarity. The
unresolved common four-agent/general gate
is to prove that dependency growth preserves enough positive normalized gain
to close in an eligible union, or else yields an impossible strict wall
cycle. This supersedes bounded item-radius targets but does not prove EFX.

**Parallel four-agent Hall-gradient gate:** the fixed-profile diagonal
theorems have now been coarsened to the full cyclic pair-Hall cell far enough
to prove a new cap-free structural consequence: under global normalized-
threshold maximality and complete blockage of the eligible fixed-core token
orbit, every owner's core good weakly dominates both the floater and the
preceding pair's token.  The first wall is confirmed by three Z3 profiles and
cvc5; the second is triple-Z3 confirmed with cvc5 UNKNOWN. Two further
cross-row clause families, with eight cyclic images, are proved by direct Z3
replays. The residual pair-Hall master is not closed: the augmented exact
58-leaf cover has 4 UNSAT and 54 UNKNOWN leaves, with no SAT witness.
See
[PARTIAL_THRESHOLD_PAIR_HALL_CORE_DOMINANCE_LEMMA.md](PARTIAL_THRESHOLD_PAIR_HALL_CORE_DOMINANCE_LEMMA.md)
and
[PARTIAL_THRESHOLD_PAIR_HALL_CROSS_ROW_CLAUSES.md](PARTIAL_THRESHOLD_PAIR_HALL_CROSS_ROW_CLAUSES.md).

The human rotating-token lemma now gives a valid cyclic symmetry break for
this cell without using any pair-Hall edges or finite global/completion cuts.
The resulting canonical CEGAR pool has 159 global, 78 matching, and 38
whole-orbit cuts, but is not closed. See
[PARTIAL_THRESHOLD_ROTATING_TOKEN_LEMMA.md](PARTIAL_THRESHOLD_ROTATING_TOKEN_LEMMA.md).

**Current live gate:** the strict-common-favorite universal owner-threshold-
failure branch at \((4,9)\) is now closed by a cap-free, proof-checked
computer-assisted theorem. The bottom-pair reduction splits into the
three-agent-bottom case and exactly 20 multiplicity-at-most-two multigraph
patterns. All 20 patterns are independently solver-confirmed and supported
by CPC derivations accepted by Ethos. See
[COMMON_FAVORITE_UNIVERSAL_THRESHOLD_EFX_THEOREM.md](COMMON_FAVORITE_UNIVERSAL_THRESHOLD_EFX_THEOREM.md)
and
[efx49_common_favorite_universal_threshold_efx_audit.json](efx49_common_favorite_universal_threshold_efx_audit.json).
The next common-favorite gate is the mixed threshold/Hall branch: some
favorite-singleton owner passes the scalar threshold, but the residual
three-agent feasibility graph is Hall-deficient. This branch is genuinely
necessary. Two exact cap-20 profiles have 114 and 273 threshold-passing
owner--partition pairs but no Hall-valid favorite-singleton partition; all
their complete EFX support is balanced. A third profile blocks all six
one-transfer repairs of a fixed passing \(3+3+2\) partition. The proposed
rank-two selection precursor is now exactly refuted at value cap 4: a
two-type profile has three threshold passes, all of rank one, no
favorite-singleton EFX allocation, and 3,690 balanced complete allocations.
The next target must therefore treat rank-one and rank-two maxima separately
with owner-changing balanced exchanges. See
[MIXED_THRESHOLD_HALL_GATE.md](MIXED_THRESHOLD_HALL_GATE.md) and the frozen
[mixed-boundary audit](efx49_common_favorite_mixed_hall_boundaries_audit.json).
The first radius-two successor remains open: direct caps 6 and 20 and a
six-model cap-6 CEGAR rebuild all return `UNKNOWN`, with 488 singleton
obstructions learned in the latter. See
[efx49_common_favorite_mixed_hall_radius2_gate_audit.json](efx49_common_favorite_mixed_hall_radius2_gate_audit.json).
The earlier rank-selection frontier is retained as provenance: resumed cap-20
CEGAR grew the rank-two and zero-neighbor motif pools to 119 and 69 before the
smaller cap-4 search found the exact rank-one counterexample. See
[efx49_common_favorite_mixed_selection_gate_audit_v2.json](efx49_common_favorite_mixed_selection_gate_audit_v2.json)
and
[efx49_common_favorite_rank2_selection_refutation_audit.json](efx49_common_favorite_rank2_selection_refutation_audit.json).
The corrected cap-4 search excludes proportional row pairs. Twelve exact
four-type trace profiles first extend its cumulative obstruction pool from
29 to 77 motifs; the next session then finds an exact four-type refutation.
Its three threshold passes all have rank one, none of 966
favorite-singleton partitions supports EFX, and literal enumeration finds
599 balanced supporting partitions and 3,878 complete allocations. Its four
rows are pairwise bundle-order inequivalent, so it lies outside the immediate
ordinal extension of the three-types theorem. See
[efx49_common_favorite_fourtype_rank2_frontier_audit.json](efx49_common_favorite_fourtype_rank2_frontier_audit.json)
and
[efx49_common_favorite_fourtype_rank2_refutation_audit.json](efx49_common_favorite_fourtype_rank2_refutation_audit.json).
The rank-one branch now has a proved common-column normal form and an exact
owner-switch reduction. The natural one-transfer successor is false even
with every favorite-singleton partition excluded: an exact profile blocks
all six transfers but has 366 balanced repairs and 1,259 allocations. A
second cap-6 profile refutes the 21-state contested-partner radius-two
successor as well. A third cap-6 profile now refutes the resulting 30-state
bridge target: all 966 singleton partitions and all 30 repairs fail, although
264 other partitions support 2,790 complete allocations. Its 15 nearest
repairs occupy two additional origin orbits, giving a 45-state successor.
The first exact campaign blocks all 45 states and reaches a six-singleton
Hamming-two local minimum. The cap-6 subcell with three identical resident
rows is now dual-encoded `UNSAT` using one shared 392-partition pool, while
the unequal-resident decision remains `UNKNOWN` after 900 seconds. Through cap 5,
full identity can be weakened to any repeated resident row: both adjacent
equality cases close under independent quotient-matching and quotient-Hall
encodings, with the Hall reduction exhaustively checked on 4,096 graphs.
The wider repeated-row cell remains `UNKNOWN` at cap 6, making cap 6 the next
bounded local-repair gate. This is not an uncovered EFX-existence class:
for four agents, any repeated valuation row gives at most three valuation
types, and complete EFX existence for three types is already known
(Ghosal--Prakash--Nimbhorkar--Varma, EC 2025). The repeated-row computation
is therefore retained as proof mining. The repaired four-type selector is
also now false, so the live mixed-Hall proof must treat rank-one and rank-two
maxima directly. See
[RANK_ONE_RADIUS_TWO_BRIDGE_GATE.md](RANK_ONE_RADIUS_TWO_BRIDGE_GATE.md).

An independent cap-free route now uses the published three-types theorem as
a safe boundary. Merge one valuation row into another and then interpolate it
back to the target row. Each fixed allocation is EFX on a closed rational
interval of the interpolation parameter. A new resident-extension lemma
reduces one fixed bundle partition to at most four moving-agent intervals and
proves that the merged endpoint starts with at least two extendable bundles.
It also gives an ordinal-chamber corollary: if any two rows induce the same
weak ordering of all bundles, merging them preserves an EFX allocation, so
the open four-agent stratum may assume four distinct bundle-order types.
For a generic single-wall crossing, the current partition fails only if the
one deleted moving-agent edge is essential to every perfect matching. Hall's
theorem then leaves exactly four deficiency sizes, independently checked on
all 4,929 labeled essential-edge graphs. The size-one case is unrealizable
for additive feasibility rows, leaving exactly the three Hall sizes
\(2,3,4\) for a bundle-changing wall pivot.
The first bounded pivot menu is now decisively false. Generic seven-good
wall profiles realize all three Hall sizes while changing exactly one
feasibility edge. Hall sizes two and three can block every partition within
two good transfers, with their nearest EFX support at distance three; Hall
size four can block every one-transfer partition. The three post-wall
profiles retain 16, 40, and 57 complete EFX allocations, so these are local
pivot refutations rather than EFX counterexamples. In the same seven-good
shape, the Hall-size-four radius-two obstruction is dual-solver UNSAT, but
that bounded cell has not been converted into a human lemma and two
eight-good extensions timed out. The live analytic target is therefore a
Hall-directed exchange chain or global potential, not a universal
one- or two-good repair. See
[SINGLE_WALL_PIVOT_GATE.md](SINGLE_WALL_PIVOT_GATE.md).
Proving that coverage never develops a first gap would resolve the
four-agent additive conjecture. Exact enumeration covers all 72 ordered row
merges of the four tight count-four witnesses from \((4,7)\) through
\((4,10)\) and the two hostile mixed-Hall profiles. Every path has one fixed
unlabeled partition valid throughout, allowing assignments to change; 63
paths need one assignment and nine need two. These remain finite-profile
results, not a continuation theorem. See
[ROW_MERGE_CONTINUATION_GATE.md](ROW_MERGE_CONTINUATION_GATE.md).

The stronger common-low target has an exact boundary with zero favorite-pair
repairs,
exactly one common-low repair, and 252 complete EFX allocations. See
[DISTINCT_HALF_CONVERSION_DICHOTOMY_GATE.md](DISTINCT_HALF_CONVERSION_DICHOTOMY_GATE.md).
The strongest surviving proof-mining compression is the
[two-core/Tutte corollary](FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md):
force a parked low pair and two agents accepting every residual edge, while
the graph of edges rejected by both outsiders has no perfect matching. The
stronger routes requiring either three fixed universal acceptors or three
acceptors per edge have exact strict counterexamples.
The two-core negation itself remains unresolved after exact-real matching
and Hall CEGAR boundaries of 40 and 24 cuts, a 120-second timeout on a
separate 55-cut complement frontier, a reified 183-cut boundary, and a
300-second full cap-20 CP-SAT timeout. A bounded CP-SAT CEGAR continuation
also remained `UNKNOWN` on its 331-cut formula after 900 seconds. No solver
endpoint has been promoted to a theorem.

The latest cap-20 CEGAR boundary changes the tactical priority. Its last
profile has only 20 favorite-pair repairs and no two-core witness, yet still
has a full 15-pairing favorite-triple Hall cell. Thus the next decision
target is the weaker full-cell dichotomy: conditional on zero favorite-pair
repairs, force one low pair for which all 15 residual pairings pass Hall.
Two-core/Tutte remains a useful sufficient explanation, but need not be the
first structure forced.
The first exact no-full-cell master found a profile with 289 favorite-pair
repairs. The next 183-cut solve hit its configured 180-second limit; the
two-solve run took 337.7 seconds in total. This is consistent with the
conditional full-cell target and does not prove it.
A separate cap-20 CP-SAT CEGAR trace found a no-full-cell profile with 357
favorite-pair repairs. Its 412-cut continuation remained `UNKNOWN` after
600 seconds. The profile still has 3,563 labeled complete EFX allocations,
so this is another bounded boundary rather than a counterexample.

The same structural branch is now proof-certified on the finite domain in
which all 36 values are integers in \(\{1,\ldots,6\}\). CP-SAT closes a
401-partition obstruction pool; an independent sorting-based QF_LIA replay
closes its 359-partition core and shrinks it to 175; and a third
monotone-threshold CNF encoding reduces to a deletion-minimal 21-partition
core. Its 1,145,090-clause formula is `UNSAT` in CaDiCaL, with a binary DRAT
proof independently accepted by `drat-trim`. The earlier cap-5 proof remains
the smaller 17-core certificate. These are genuine bounded theorems, not a
cap-free result: arbitrary value ratios cannot be reduced to six levels by
scaling. The 17 cap-5 literal templates fail at cap 6 even though the full
cap-6 statement holds, but they occupy only six of the ten natural orbits
under independent permutation of the representatives and unmatched goods.
Their 624-partition orbit closure is now refuted by an exact cap-20 profile
with no full Hall cell, zero repairs in those six orbits, 45 repairs in two
omitted orbits, and 900 labeled complete EFX allocations. This retires the
six-orbit and representative-partner selectors without touching the full
840-partition dichotomy. See
[DISTINCT_HALF_FULL_CELL_CAP5_THEOREM.md](DISTINCT_HALF_FULL_CELL_CAP5_THEOREM.md),
[DISTINCT_HALF_FULL_CELL_CAP6_THEOREM.md](DISTINCT_HALF_FULL_CELL_CAP6_THEOREM.md)
and
[DISTINCT_HALF_FULL_CELL_ORBIT_GATE.md](DISTINCT_HALF_FULL_CELL_ORBIT_GATE.md).

The latest terminal-state compression isolates a 138-partition radius-two
exchange family. At value cap 5, all seven terminal/matching symmetry cells
are closed independently by CP-SAT and Z3 QF_LIA without assuming any Hall
condition. The cap-free statement is false. Its 66 same-favorite and 72
changed-favorite-partner halves were each exactly refuted under the full
no-Hall-cell premise. Guarded cap-20 optimization then refuted their full
union: the resulting profile has no full Hall cell and no radius-two repair,
but it has 336 favorite-pair EFX partitions and 1,439 complete EFX
allocations. Radius two is therefore retired; the live target is again the
global eight-orbit-or-full-Hall dichotomy. See
[DISTINCT_HALF_TERMINAL_EXCHANGE_GATE.md](DISTINCT_HALF_TERMINAL_EXCHANGE_GATE.md).

The global target now has a concise exhaustive refinement. A common
unmatched edge witnesses all six representative-pair cells exactly when its
value is below the favorite plus each agent's second-smallest representative.
Either every unmatched edge clears that threshold for some agent, or one
common witness can be fixed canonically; the latter has 19
second-smallest-map orbits. Independent annealing and cap-100 CP-SAT searches
have reduced the best no-full-cell boundary from 45 to three eight-orbit
repairs, without proving that zero is impossible. The three states are one
perfect-pairing cell and arise as conversions of the three missing matchings
in a 12-of-15 favorite-triple Hall cell. The conversion itself is now a
cap-free analytic lemma; selecting its motif under the no-favorite-pair
conditioning remains open. See
[DISTINCT_HALF_COMMON_UU_SPLIT_GATE.md](DISTINCT_HALF_COMMON_UU_SPLIT_GATE.md)
and
[ZERO_NEIGHBOR_FAVORITE_TRIPLE_CONVERSION_LEMMA.md](ZERO_NEIGHBOR_FAVORITE_TRIPLE_CONVERSION_LEMMA.md).

The conversion was first upgraded on a substantial cap-free subbranch.
If two residual goods are jointly bottom-two for all four agents, every
failed Hall pairing yields one of six distinct favorite-pair conversions.
Consequently (P_f+H_{a,b}\ge15), and (P_f=0) forces a full Hall cell.
The exact theorem has two Z3 encodings, independent cvc5 replay, and a CPC
proof accepted by Ethos. See
[COMMON_BOTTOM_PAIRING_CONVERSION_THEOREM.md](COMMON_BOTTOM_PAIRING_CONVERSION_THEOREM.md).

Proof mining then removed every bottom-order inequality for one agent. It
is enough that the pair be jointly bottom-two for any three agents. The
strengthened theorem is UNSAT in both the cardinal and sorting-network Z3
encodings and in pinned cvc5; its five canonical Hall-role cells are also
UNSAT. The counting injection still gives $P_f+H_{a,b}\ge15$, so a profile
with no favorite-pair EFX state has a full Hall cell whenever such a
three-agent bottom pair exists. Two-agent versions of the same local
six-conversion menu have exact SAT boundaries in every Hall-role type.
Thus the live successor is the multiplicity-at-most-two branch, with bottom
pair sharing patterns $2+2$, $2+1+1$, or $1+1+1+1$. See
[THREE_AGENT_BOTTOM_PAIRING_CONVERSION_THEOREM.md](THREE_AGENT_BOTTOM_PAIRING_CONVERSION_THEOREM.md).
The four chosen pairs reduce exhaustively to 20 unlabeled multigraphs. In the
disjoint-$2+2$ pattern, the full 180-state conversion closure is now a
proof-checked theorem: a 72-partition Z3 core closes under two universal-
threshold encodings, cvc5 independently returns `unsat`, and Ethos accepts
the 434,968-step CPC proof. This eliminates one of the 20 multigraphs. See
[DISJOINT_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md](DISJOINT_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md).
The remaining overlapping-$2+2$ pattern is now also proof-checked. A
theorem-preserving 960-element canonicalization reduces the complete
165-partition conversion closure to a formula that is `unsat` in two Z3
threshold encodings and independently in cvc5. Ethos accepts cvc5's
767,596-step CPC proof. Four independently found exact boundaries retain
three repairs, all in the same size-60 conversion orbit. Together with the
disjoint theorem, this closes both $2+2$ patterns. See
[OVERLAP_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md](OVERLAP_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md)
and [BOTTOM_PAIR_MULTIPLICITY_GATE.md](BOTTOM_PAIR_MULTIPLICITY_GATE.md).

That successor is now exhaustively finite at the pattern level. Viewing the
four selected bottom pairs as a loopless multigraph on the residual goods,
30,681 labeled edge multisets reduce to exactly 20 unlabeled patterns: two of
type $2+2$, seven of type $2+1+1$, and eleven of type $1+1+1+1$. The two
$2+2$ patterns refine to nine disjoint and four overlapping relative
matching orbits. The separate six-conversion menus close six disjoint orbits
in Z3 but have exact local boundaries in the other seven orbits. Global
zero-favorite-pair encodings still stall at 76, 128, 445, 768, or 840 cuts,
but the smaller conversion closures are sufficient and proof-checked for
both $2+2$ patterns. A separate 225-conversion theorem closes the triangle-
with-doubled-edge $2+1+1$ pattern. Subsequent proof-checked conversion
theorems close the other six $2+1+1$ patterns as well. The residual census
now consists of the eleven all-distinct patterns. See
[BOTTOM_PAIR_MULTIPLICITY_GATE.md](BOTTOM_PAIR_MULTIPLICITY_GATE.md) and
[efx49_bottom_pair_pattern_census_audit.json](efx49_bottom_pair_pattern_census_audit.json).
The first two of those eleven—the perfect matching of four disconnected
selected pairs and the four-cycle—are now closed by proof-checked
conversion theorems. See
[FOUR_DISCONNECTED_BOTTOM_PAIRS_CONVERSION_THEOREM.md](FOUR_DISCONNECTED_BOTTOM_PAIRS_CONVERSION_THEOREM.md)
and
[FOUR_CYCLE_BOTTOM_PAIRS_CONVERSION_THEOREM.md](FOUR_CYCLE_BOTTOM_PAIRS_CONVERSION_THEOREM.md).

## Basic explanation

An allocation is EFX when no agent prefers another agent's bundle after any
one good is removed from that other bundle. The general existence question is
open from four agents onward.

This repository now proves the fixed cell with four agents and eight goods.
The next possible four-agent counterexample therefore has at least nine
goods. The current general-goal campaign attacks that first open cell directly
and adversarially tests structural lemmas that could turn the fixed-cell
result into an induction.

The fully dual-encoded bounded-subclass frontier reaches cap 13: every
four-agent/nine-good instance in which each row uses nine distinct integer
values from \(\{1,\ldots,13\}\) has complete EFX. Its structural conclusion
is “balanced allocation or designated-favorite singleton.” This does not
cover arbitrary additive values.

## Chronology and provenance

The frozen counting manuscript in [`paper/main.tex`](../paper/main.tex) and
its Claude Code campaign ledger are a separate earlier track. Their exact
count-\(n\) witnesses, bounded integer-box exclusions, parking theorem, and
stalled-solver endpoints remain valid within their stated scopes. In
particular, a bounded claim such as “no \((4,8)\) counterexample with values
at most four” is not the later unrestricted \((4,8)\) theorem.

The formal \((4,8)\) package described below postdates that frozen ledger.
Accordingly, the earlier statement that the \((4,8)\) Z3 existence run was
paused is historical process state, not the current mathematical frontier.
Nothing in the counting manuscript is being silently upgraded or used as a
premise for the later theorem.

## Established starting point

The internally certified theorem is:

> Every nonnegative additive instance with four agents and eight goods has a
> complete EFX allocation.

Its proof package combines a Lean reduction with eight exact linear-arithmetic
UNSAT certificates checked through cvc5 CPC proofs and Ethos. The proof guide
is [EFX48_PROOF_GUIDE.md](EFX48_PROOF_GUIDE.md), the gate ledger is
[EFX48_REMAINING_GATES_20260730.md](EFX48_REMAINING_GATES_20260730.md), and
the submission source is
[`paper/efx48/submission.tex`](../paper/efx48/submission.tex).

This is a fixed-parameter theorem. It does not prove EFX for four agents with
arbitrarily many goods and does not resolve the general additive conjecture.

## Exact structural formulation

For an unlabeled partition \(P=(B_1,\ldots,B_n)\), define a bipartite graph
between agents and bundles. Agent \(i\) is adjacent to \(B\) exactly when
owning \(B\) would satisfy all of \(i\)'s EFX comparisons against the other
bundles:

\[
v_i(B)\ge
\max_{C\ne B}\left(v_i(C)-\min_{g\in C}v_i(g)\right).
\]

The partition supports a complete EFX allocation exactly when this graph has
a perfect matching. This formulation is the basis of both the certified
\((4,8)\) proof and the new \((4,9)\) workbench.

The generic threshold-cycle normal-form theorem also remains valid: any
complete EFX allocation with nonempty bundles can be rotated through strict
threshold-improvement cycles until some owned good is removable. Hence
complete EFX existence is equivalent to existence of a parkable-deletion
triple. See [REVERSE_PARKING_LEMMA.md](REVERSE_PARKING_LEMMA.md).

## Structural routes falsified in this campaign

### Static deletion selectors

The following proposed rules were adversarially tested and refuted:

- park a normalized aggregate-minimum good;
- park some row-minimum good;
- park a good selected by the first Hall-feasible layer of bottom rankings;
- minimize raw or weighted cross-observer bundle variance; and
- minimize several canonical threshold-partition potentials.

The exact or replayed witnesses are in:

- [aggregate_selector_cegar_n3m5.json](aggregate_selector_cegar_n3m5.json);
- [row_min_selector_anneal_20260730.json](row_min_selector_anneal_20260730.json);
- [hall_low_selector_anneal_deep_20260730.json](hall_low_selector_anneal_deep_20260730.json);
- [weighted_variance_row_min_cex.json](weighted_variance_row_min_cex.json); and
- [partition_potentials_tb4.json](partition_potentials_tb4.json).

These failures rule out the stated selectors, not EFX existence.

### One-good matching-rank plateau augmentation

A natural conjecture said that every connected component of partitions with
the same deficient matching rank has a one-good transfer edge to a higher
rank. Exact QF_LRA found the following positive-additive counterexample:

\[
\begin{pmatrix}
4&286&140&424&422&278&75&67\\
417&413&842&870&24&814&8&4\\
881&48&817&1690&1682&1626&24&16\\
48&54&24&1670&1628&6&835&823
\end{pmatrix}.
\]

At source partition
\(\{\{0,1\},\{2,4\},\{3\},\{5,6,7\}\}\), the feasibility graph has matching
rank 3, while every one-good-transfer neighbor has rank at most 2. Full
enumeration confirms that this is a trapped singleton rank-3 component, even
though the instance has 23 perfect-rank partitions elsewhere.

Evidence:

- [strict_rank_trap_3221.json](strict_rank_trap_3221.json);
- [strict_rank_trap_3221.smt2](strict_rank_trap_3221.smt2); and
- [matching_augmentation_strict_trap_3221.json](matching_augmentation_strict_trap_3221.json).

### Every augmentation within three transferred goods

The stronger conjecture said that a rank-3 four-agent partition can always
reach a perfect-rank partition by moving at most three goods. Exact CEGAR
refuted it with:

\[
\begin{pmatrix}
383&8&24&15&342&382&2&4\\
4693&168&6903&105&2294&8092&1231&874\\
633&588&1739&40&523&2247&10&20\\
2272&1193&2284&36&18&953&132&72
\end{pmatrix}.
\]

For the same source partition shape:

- the source matching rank is 3;
- all 884 partitions within transfer radius 3 have rank at most 3;
- only 5 of all 1,701 partitions have perfect rank; and
- the nearest perfect-rank partition has distance exactly 4.

The CEGAR model was independently replayed over the full partition universe.

Evidence:

- [matching_radius3_cegar_resume_20260730.json](matching_radius3_cegar_resume_20260730.json);
- [matching_radius3_cegar_resume_20260730.smt2](matching_radius3_cegar_resume_20260730.smt2); and
- [matching_radius_profile_r3_counterexample.json](matching_radius_profile_r3_counterexample.json).

Radius 4 remains inconclusive:
[matching_radius4_cegar_20260730.json](matching_radius4_cegar_20260730.json).

A later full-universe distance audit shows that radius 4 cannot be a general
four-agent lemma. The exact-count-four \(4\times9\) witness has maximum
rank-3-to-perfect distance 4, but the exact-count-four \(4\times10\) witness
has rank-3 partitions at distance 5 from every perfect partition. Both the
matching count and an independent literal allocation enumerator return
exactly four complete EFX allocations in each instance. In the \(4\times10\)
witness, one shortest path to perfect rank has rank profile
\(3,2,2,2,3,4\), so even the shortest repair must first lose matching rank.

Evidence:

- [matching_radius_landscape_tight49.json](matching_radius_landscape_tight49.json);
- [matching_radius_landscape_tight410.json](matching_radius_landscape_tight410.json); and
- [`audit_matching_radius_landscape.py`](../tracks/parkability/audit_matching_radius_landscape.py).

The local-movement family is therefore deprioritized: radius 3 is false
already at \(4\times8\), and radius 4 is false at \(4\times10\).

## Direct attack on the first open cell: \((4,9)\)

### Strong seed and heuristic search

The known nine-good witness has exactly four labeled complete EFX
allocations. Its canonical \(2+1+1\) favorite-pattern form is
[tight49_witness_canonical_211.json](tight49_witness_canonical_211.json).

A 5,000-step exact-census anneal accepted 3,897 moves but found no improvement
below four:
[efx49_anneal_seed30.json](efx49_anneal_seed30.json).
This is heuristic evidence only.

### Allocation-level exact CEGAR

The parameterized exact-real master reached a pool of 657 labeled EFX
allocations after two rational models, then timed out:

- [efx49_lra_result_session1.json](efx49_lra_result_session1.json);
- [efx49_lra_pool.json](efx49_lra_pool.json); and
- [efx49_lra_session1.smt2](efx49_lra_session1.smt2).

Status: `MASTER_UNKNOWN`, not a theorem.

### Partition-level exact CEGAR

The new parameterized partition workbench searches the 7,770 unlabeled
nonempty partitions instead of 186,480 labeled onto allocations.

In the canonical strict favorite cell \((0,0,1,2)\):

1. an adaptive Z3 run reached a 196-partition boundary;
2. Z3 timed out on that exact formula;
3. identity-only SMT normalization produced strict QF_LRA for cvc5;
4. pinned cvc5 1.3.3 returned `sat`;
5. the dumped rational model was decoded to primitive integer rows;
6. exact replay found 576 complete EFX allocations supported by 159 new
   partitions;
7. a second cvc5 model was obtained from the resulting 355-obstruction
   formula; and
8. independent exact replay found 164 complete EFX allocations supported by
   119 previously unseen partitions.

The expanded pool reached 474 partitions. Z3 returned `unknown` at its
600-second limit on that boundary. A new pinned-external-solver CEGAR driver
passed an end-to-end \(2\times3\) calibration and continued the solve
directly with cvc5. Six further exact rational models contributed
78, 61, 13, 58, 19, and 13 new supporting partitions. Four independent hard
seeds contributed another 23, and one final exact model contributed 33.
The learned pool therefore reached 772 partitions. Every model was decoded
to primitive integer rows and replayed over all 7,770 nonempty partitions
and all \(4^9\) labeled allocations.

Adding the complete \(6+1+1+1\) shape class supplied 82 previously unseen
partitions and produced an 854-partition boundary. Pinned cvc5 and two Z3
arithmetic portfolios all reached their time limits on the sound
generic-position formula. Their status is `MASTER_UNKNOWN`.

Primary evidence:

- [efx49_partition_211_batch64_result_session1.json](efx49_partition_211_batch64_result_session1.json);
- [efx49_partition_211_batch64_cvc5_model_session1.json](efx49_partition_211_batch64_cvc5_model_session1.json);
- [efx49_partition_211_cvc5_model1_values.json](efx49_partition_211_cvc5_model1_values.json);
- [efx49_partition_211_batch64_cvc5_model_session2.json](efx49_partition_211_batch64_cvc5_model_session2.json);
- [efx49_partition_211_cvc5_model2_values.json](efx49_partition_211_cvc5_model2_values.json);
- [efx49_partition_211_batch64_result_session3.json](efx49_partition_211_batch64_result_session3.json);
- [efx49_partition_211_batch64_pool.json](efx49_partition_211_batch64_pool.json); and
- [efx49_partition_211_batch64_session3.smt2](efx49_partition_211_batch64_session3.smt2).

No zero-EFX model has been found.

### Candidate anchored \(4\times9\) lemma

The learned obstructions suggest a direct analogue of the certified
\(4\times8\) anchored family. For strict favorite pattern \((0,0,1,2)\),
define \(\mathcal A_9\) as the union of:

1. 473 partitions in which good 0 is a singleton, goods 0, 1, and 2 are
   separated, and no nonfavorite good is a singleton; and
2. 480 partitions of shape \(3+2+2+2\) in which goods 0, 1, and 2 are
   separated and good 0 lies in a pair.

Thus \(|\mathcal A_9|=953\). This family covers every hard rational model
learned so far. It also has a clean induction interpretation: delete a
nonfavorite good, use the \(4\times8\) anchored theorem, and reinsert the
good without placing it into the bundle containing shared favorite 0.

Two pinned cvc5 solves of the complete 953-partition matching-clause formula,
using different decision heuristics, each reached a 900-second limit without
a verdict. A sound fixed top-two orbit also returned no verdict at 300
seconds. All statuses are `MASTER_UNKNOWN`, not theorems and not
counterexamples. A solver-independent Hall-selector encoding also returned
`MASTER_UNKNOWN` at 900 seconds. The full 953-family formula is therefore
retained as an analytic target rather than the primary computational engine.

Evidence:

- [EFX49_ANCHORED_LEMMA_TARGET.md](EFX49_ANCHORED_LEMMA_TARGET.md);
- [efx49_partition_211_anchored953_audit.json](efx49_partition_211_anchored953_audit.json);
- [efx49_partition_211_anchored953_pool.json](efx49_partition_211_anchored953_pool.json);
- [efx49_partition_211_anchored953_external_session1.json](efx49_partition_211_anchored953_external_session1.json); and
- [`build_anchored49_pool.py`](../tracks/parkability/build_anchored49_pool.py).

### Refuted lex-max one-unallocated reduction

A stronger finite reduction was tested across valuation cells at
\((4,9)\), rather than only favorite pattern \(2+1+1\).

The almost-full four-agent theorem supplies an EFX allocation of eight goods
with one unallocated good \(f\), where no agent envies \(\{f\}\). Among all
such states, fix an agent order and choose one that lexicographically
maximizes the four own-bundle utilities. The candidate lemma says that \(f\)
can then be inserted directly into some bundle.

In a generic positive instance, all four base bundles are nonempty. Their
ordered sizes are a positive composition of eight into four parts, leaving
exactly \(\binom73=35\) canonical cells. For a fixed candidate base, exact
CEGAR requires it to be strictly EFX, strictly dominate the singleton
\(\{f\}\), and fail all four insertions. It then blocks every other
one-unallocated EFX base whose floater is not envied and whose utility vector
is lexicographically nonlower.

The exact \(2\times3\) calibration learned one rival and closed UNSAT. At
\(4\times9\), the \(1,1,1,5\) and \(2,2,2,2\) cells learned thousands of
exact rival bases without an endpoint. Those two cells missed the decisive
ordered \(2,3,2,1\) obstruction.

Chaudhury's nine-good lexicographic-potential example was lifted to the
strictly positive, fully bundle-nondegenerate matrix

\[
\begin{pmatrix}
1&2&4&8&16&32&6208&4224&256\\
16385&4098&24580&4104&16&34848&31808&128&2304\\
10241&2&18436&8200&20496&32&29760&128&6400\\
1&2&4&8&18448&20512&19520&128&4352
\end{pmatrix}.
\]

Exact replay finds 322 eligible one-unallocated bases. The unique
lexicographic maximum is blocked at every host. Its first-agent utility is
10432, while all 103 complete EFX allocations give that agent utility at
most 6464. This refutes only the completion lemma; it is not an additive-EFX
counterexample. It decisively rules out ordinary lexicographic own utility
with an arbitrarily fixed first agent as the missing potential. The
existential-order weakening survives this instance: 18 of its 24 agent
orders have an insertable lexicographic maximum. That weakening is an active
falsification target, not a theorem. A 15,000-step continuation retained
those 18 rescue orders while reducing their largest normalized insertion
margin from \(0.3163\) to \(0.002263\); exact replay still found no
all-orders-blocked endpoint.

This isolates the adaptive-priority completion conjecture: some one of the
24 agent orders has an insertable lexicographic maximum. Unlike the
fixed-\((4,9)\) theorem target, an analytic proof of this statement for an
arbitrary number of goods would settle complete additive EFX for four
agents. Its exact scope and proof gates are in
[ADAPTIVE_PRIORITY_COMPLETION_TARGET.md](ADAPTIVE_PRIORITY_COMPLETION_TARGET.md).

The simultaneous all-order CEGAR has now closed five structurally distinct
fixed candidate cells whose blocked-state premises were jointly
satisfiable. The cells used 4, 6, 6, 5, and 5 distinct candidate states and
became UNSAT after learning 420, 309, 448, 964, and 660 nonlower-rival
clauses, respectively. Across 44 annealing improvement records there are 26
distinct candidate-identity cells; exactly five permit all candidates to be
blocked simultaneously, and those are exactly the five closed cells. These
endpoints do not prove the adaptive conjecture because the trace census is
not the combinatorial universe of candidate identities.

One deletion-minimal core contains only two candidate states and one rival.
It converts to a genuine analytic result valid for arbitrary goods: the
[forced singleton-swap handoff lemma](FORCED_SINGLETON_SWAP_LEMMA.md).
In the lemma, one EFX state owns a pair \(\{p,q\}\), while another EFX state
splits \(p,q\) as two singleton bundles. Three failed insertions force the
crossed strict preferences

\[
v_a(p)>v_a(q),\qquad v_c(q)>v_c(p).
\]

Swapping the singleton goods therefore preserves EFX and floater nonenvy
and gives a strict lexicographic improvement. The proof uses only weak EFX,
weak floater nonenvy, and strict positivity. Its frozen QF_LRA encoding is
reconstructed by Z3 and independently replayed UNSAT by cvc5. This is a
local exchange theorem, not yet a covering theorem for all possible blocked
families.

Evidence:

- [LEXMAX_PARTIAL_COMPLETION_TARGET.md](LEXMAX_PARTIAL_COMPLETION_TARGET.md);
- [ADAPTIVE_PRIORITY_COMPLETION_TARGET.md](ADAPTIVE_PRIORITY_COMPLETION_TARGET.md);
- [lexmax_partial_counterexample_4x9.json](lexmax_partial_counterexample_4x9.json);
- [lexmax_all_orders_anneal_4x9_seed93.json](lexmax_all_orders_anneal_4x9_seed93.json);
- [lexmax_all_orders_seed93_exact_replay.json](lexmax_all_orders_seed93_exact_replay.json);
- [adaptive_priority_trace92_i5_compact_core.json](adaptive_priority_trace92_i5_compact_core.json);
- [adaptive_priority_seed93_compact_core.json](adaptive_priority_seed93_compact_core.json);
- [adaptive_priority_trace_cell_census.json](adaptive_priority_trace_cell_census.json);
- [FORCED_SINGLETON_SWAP_LEMMA.md](FORCED_SINGLETON_SWAP_LEMMA.md);
- [forced_singleton_swap_lemma.json](forced_singleton_swap_lemma.json);
- [lexmax_partial_cells49.json](lexmax_partial_cells49.json);
- [lexmax_partial_5111_pool.json](lexmax_partial_5111_pool.json);
- [lexmax_partial_2222_pool.json](lexmax_partial_2222_pool.json); and
- [`run_lexmax_partial_cegar.py`](../tracks/parkability/run_lexmax_partial_cegar.py).

### Small-integer counterexample bound

The fixed-cell value-cap gap is now closed analytically. If an additive
counterexample exists for \(n\) agents and \(m\) goods, one exists with
strictly positive integer item values bounded by

\[
K_m=\left\lfloor m^{m/2}\right\rfloor .
\]

The proof selects one strict EFX violation for every complete allocation,
normalizes each observer row independently, maximizes a common strict margin,
and applies Cramer's rule plus Hadamard's determinant bound to an LP vertex.
Independent row scaling is why the cap depends only on \(m\), not \(n\).
For the first open cell \(m=9\), \(K_9=19{,}683\).

This gives an unconditional finite decision procedure for every fixed
\((n,m)\). It does not bound the number of goods in a smallest
counterexample, and literal enumeration of the resulting valuation box is
not practical. The proof and exact scope are in
[SMALL_INTEGER_COUNTEREXAMPLE_BOUND.md](SMALL_INTEGER_COUNTEREXAMPLE_BOUND.md).

### Borda-additive \(4\times9\) shape theorem candidate

The new bounded-integer master produced a complete finite-subclass result.
If every agent's item values are a permutation of \(1,\ldots,9\), then the
instance has a complete EFX allocation with bundle sizes \(3,2,2,2\).

The proof splits profiles by the five possible multiplicity patterns of
their unique favorite goods:

\[
4,\quad 3+1,\quad 2+2,\quad 2+1+1,\quad 1+1+1+1.
\]

For every pattern, an exact CP-SAT model proves that no Borda profile can
obstruct all 417 pooled \(3+2+2+2\) partitions. The result was replayed with
two distinct formulations: direct matching clauses and explicit Hall
deficiency selectors. Neither formulation uses universal-minimum,
peelability, pairwise-row-distinctness, or lexicographic stabilizer cuts.

The stabilized \(2+1+1\) cell shrinks further to 17 partitions. That core is
independently UNSAT in Z3 and pinned cvc5 1.3.3. cvc5 emitted a 52.3 MB CPC
proof with 555,808 steps; the separate Ethos 0.2.3 checker returned
`correct`. The other four cells have dual CP-SAT encodings but do not yet
have external proof logs, so the combined statement remains conservatively
labeled a computer-assisted theorem candidate.

Evidence:

- [BORDA_EFX_4X9_THEOREM.md](BORDA_EFX_4X9_THEOREM.md);
- [efx49_borda_shape3222_dual_encoding_audit.json](efx49_borda_shape3222_dual_encoding_audit.json);
- [efx49_borda_shape3222_favorites211_core17_cpc_ethos.json](efx49_borda_shape3222_favorites211_core17_cpc_ethos.json); and
- [efx49_partition_211_integer9_cpsat_matching_minimal_core_pool.json](efx49_partition_211_integer9_cpsat_matching_minimal_core_pool.json).

This is the strongest new positive \(4\times9\) subclass result in the
campaign. It does not approach the full value cap \(K_9=19{,}683\) by
monotonicity: allowing unequal score gaps is a substantive change.

### Rank-cap-12 complete-EFX theorem candidate

The Borda pool remains balanced-shape covering through the domain where
every row chooses nine distinct integers from \(1,\ldots,11\). At cap 12
the common-favorite cell supplies a sharp shape counterexample: it has no
\(3+2+2+2\) EFX allocation, but literal enumeration finds 838 complete EFX
allocations, all isolating the common favorite.

Adding the 48 supporting singleton partitions gives a 472-partition
balanced-or-singleton pool. Matching-clause and Hall-selector encodings both
close that common-favorite cell. The other four favorite orbits close under
both encodings using the original 417 balanced partitions. Therefore:

> Every four-agent/nine-good instance whose rows contain nine distinct
> integer values in \(\{1,\ldots,12\}\) has a complete EFX allocation.

This is a computer-assisted theorem candidate, not an arbitrary-value
result; both encodings use CP-SAT and the cap-12 cells lack external proof
logs. The exact human reduction is now the singleton-owner threshold
condition: after assigning the common favorite alone, only that owner's
comparisons against a three-agent EFX allocation remain.

Evidence:

- [RANK_GAP_EFX_4X9.md](RANK_GAP_EFX_4X9.md);
- [efx49_rankgap12_dual_encoding_audit.json](efx49_rankgap12_dual_encoding_audit.json);
- [efx49_rankgap12_shape_boundary_audit.json](efx49_rankgap12_shape_boundary_audit.json); and
- [COMMON_FAVORITE_SINGLETON_REDUCTION.md](COMMON_FAVORITE_SINGLETON_REDUCTION.md).

### Rank-cap-13 structural extension

At cap 13 the balanced shape also fails in the \(3+1\) and \(2+2\)
favorite cells. Their frozen witnesses have 467 and 350 labeled complete
EFX allocations respectively, and every supporting partition isolates one
of the designated favorite goods.

After learning those singleton repairs, all five matching-clause cells are
infeasible. The resulting structural statement is:

> Every four-agent/nine-good instance whose rows contain nine distinct
> integer values in \(\{1,\ldots,13\}\) has an EFX allocation that is
> either of shape \(3+2+2+2\), or isolates a designated favorite good as a
> singleton.

Hall-selector encodings independently close all five cells. The hard
common-favorite cell was rebuilt on a sparse 446-partition pool and both
encodings are infeasible on exactly that pool. Cap 13 is therefore the
fully dual-encoded frontier.

Evidence:

- [efx49_rankgap13_theorem_audit.json](efx49_rankgap13_theorem_audit.json);
- [efx49_rankgap13_shape_boundaries_audit.json](efx49_rankgap13_shape_boundaries_audit.json); and
- [RANK_GAP_EFX_4X9.md](RANK_GAP_EFX_4X9.md).

### Residual-threshold matching lemma

The most adversarial common-favorite search profile found in the structural
campaign has only 18 complete EFX allocations, supported by two unlabeled
partitions. All 18 isolate the common favorite, and one supporting
partition has shape \(6+1+1+1\).

This extreme repair has a cap-free analytic characterization. Choose three
singleton goods \(S\) and let the other six goods be \(R\). Join agent \(i\)
to singleton good \(g\) when

\[
v_i(g)\ge v_i(R)-\min_{r\in R}v_i(r).
\]

The singleton--singleton--singleton--residual partition supports EFX if and
only if this graph has a matching saturating the three singleton goods.
Thus its complete obstruction is an ordinary three-column Hall witness.
The proof is
[RESIDUAL_THRESHOLD_MATCHING_LEMMA.md](RESIDUAL_THRESHOLD_MATCHING_LEMMA.md).
It does not prove that some residual set always works. In fact the stronger
“balanced \(3+2+2+2\) or residual \(6+1+1+1\)” covering statement is false:
four identical rows

\[
(13,12,7,6,5,4,3,2,1)
\]

have no EFX allocation of either shape. Exact enumeration still finds 480
complete EFX allocations on 20 favorite-singleton partitions, of shape
\(3+3+2+1\), \(4+2+2+1\), or \(4+3+1+1\). This falsification preserves
the broader balanced-or-favorite-singleton target while showing that the
three-agent side cannot be compressed to one residual bundle alone.

The frozen audit
[efx49_common_favorite_boundaries_audit.json](efx49_common_favorite_boundaries_audit.json)
independently enumerates all \(4^9\) allocations and all 7,770 nonempty
partitions for both this falsification profile and the 18-allocation
heuristic boundary. It also replays the residual-threshold matching
criterion and exhausts all 841 positive one-row transfers around the tight
profile.

### Robust MILP

A full robust mixed-integer model used:

- 7,770 partitions;
- 45,312 comparison variables;
- 124,320 feasibility-edge variables;
- 186,480 matching constraints; and
- 1,136,328 total constraints.

SCIP returned `NOT_SOLVED` after 611 seconds with no incumbent:
[efx49_partition_211_milp_session1.json](efx49_partition_211_milp_session1.json).
This is diagnostic only.

## The actual induction bottleneck

Assume a minimal four-agent counterexample exists and delete any good \(f\).
Minimality gives an EFX allocation \(B\) of the remaining goods. The
generalized parking theorem says that \(f\) can be inserted into host bundle
\(B_h\) exactly when every other observer \(k\) satisfies

\[
v_k(B_k)\ge v_k(B_h)+
\max\{0,v_k(f)-\min_{g\in B_h}v_k(g)\}.
\]

Therefore every good and every deletion-base allocation in a minimal
counterexample must have a sourceless \(f\)-envy digraph. On four vertices
this forces a directed obstruction cycle. Converting those cycles into a
complete EFX reallocation—without leaving new bottom goods unallocated—is
the genuine induction gate. It is also where the known one-unallocated-good
theorem stops.

## Current research assessment

- **General-goal status:** unresolved.
- **Strongest positive theorem:** nonnegative additive EFX at \((4,8)\).
- **Strongest \(4\times9\) subclass result:** every instance with nine
  distinct integer values per row in \(\{1,\ldots,13\}\) has complete EFX,
  matching- and Hall-closed in all five cells. The Borda subcase has a
  CPC/Ethos proof-checked
  \(2+1+1\) core.
- **Strongest new negative results:** exact counterexamples to one-good
  plateau augmentation, every three-transfer augmentation lemma, and a
  universal four-transfer augmentation lemma, plus a positive generic
  \(4\times9\) counterexample to fixed-order lex-max completion.
- **Strongest new analytic bridges:** the forced singleton-swap handoff
  lemma excludes one recurring two-state obstruction motif, while the
  favorite-singleton reduction turns the new shape transitions into one
  scalar threshold alternative: negative best-owner slack over all
  three-agent EFX residual allocations must force a balanced allocation. The
  favorite-singleton Hall lemma removes assignment labels as well: a
  residual partition works exactly when its owner threshold passes and its
  three-agent feasibility graph has a perfect matching, so every failure is
  certified by one scalar inequality or an ordinary Hall-deficient subset.
  On the balanced-only real boundary, the scalar threshold fails for all
  3,864 owner--residual-partition pairs; this isolates universal threshold
  failure as a clean first subcase, while the full target must also handle
  threshold-passing but Hall-deficient partitions. Sorting each row's eight
  residual values reduces universal threshold failure exactly to
  \(x_5+x_6+x_7>f\) together with the disjunction
  \(x_3+x_7>f\) or \(x_4+x_5>f\). These are the exact optima for the
  \(4+2+2\) and \(3+3+2\) residual shapes. Safe partitions in the other
  three shapes reduce to one of these two shapes, so the two displayed
  conditions characterize all 966 residual partitions;
  hence at least five
  residual goods exceed one third of the favorite and the residual row
  totals more than \(7f/3\). See
  [OWNER_THRESHOLD_SHAPE_ENVELOPE.md](OWNER_THRESHOLD_SHAPE_ENVELOPE.md).
  Equivalently, without sorting, every residual four-set contains a triple
  above \(f\), and the threshold pair graph has either three vertices of
  degree at least six or four vertices of degree at least four; see
  [OWNER_THRESHOLD_PAIR_DEGREE_ENCODING.md](OWNER_THRESHOLD_PAIR_DEGREE_ENCODING.md).
  A Hall argument collapses the 16
  row branches again: either the agents have four distinct residual goods
  each worth more than half their favorite, or every agent has exactly the
  same three half-favorite goods. In the latter branch, a Hall matching
  constructs an explicit four-pair partial EFX allocation with one
  unenvied low floater. The new common-three lexicographic parking lemma
  closes the final step: a blocked insertion would let an earlier-priority
  agent take a strictly better host pair, while the last-priority host can
  absorb the displaced anchor because at most one low is bad. Thus the
  common-three branch has complete balanced EFX, leaving only the
  four-distinct-representatives branch of universal threshold failure. A
  cap-free three-set construction already gives that branch a balanced
  favorite-pair allocation in which every owner receives at least its
  favorite; only envy of the triple remains. Ordinary Nash-product and
  favorite-surplus-product rules do not finish it. Exact adversarial search
  now also refutes the favorite-pair matching-rank route: a strict
  branch-valid profile has zero EFX states among all 840 favorite-pair
  partitions, but 324 complete EFX allocations with the favorite in the
  common-low triple \(\{f,1,2\}\). This yields a cap-free alternate repair
  lemma and a sharper two-normal-form dichotomy; see
  [DISTINCT_HALF_RANK_AUGMENTATION_GATE.md](DISTINCT_HALF_RANK_AUGMENTATION_GATE.md)
  and
  [COMMON_LOW_FAVORITE_TRIPLE_LEMMA.md](COMMON_LOW_FAVORITE_TRIPLE_LEMMA.md).
  The
  same exchange principle gives a separate general theorem for any \(n\)
  and \(2n+1\) goods when every residual pair clears the common-favorite
  floor; see
  [UNIVERSAL_PAIR_FLOOR_LEX_PARKING_LEMMA.md](UNIVERSAL_PAIR_FLOOR_LEX_PARKING_LEMMA.md).
  This pair-floor premise is not implied by universal threshold failure. The
  residual-threshold matching lemma gives an exact Hall characterization
  of the extreme \(6+1+1+1\) branch, while an exact cap-13 profile proves
  that intermediate singleton shapes remain necessary. The new small-
  integer witness lemma also makes every fixed \((n,m)\) cell
  unconditionally finite, with cap \(\lfloor m^{m/2}\rfloor\).
- **Strongest active computational targets:** the unrestricted-real
  balanced-or-favorite-singleton common-favorite cell at the full
  sufficient cap, the cap-14 orbit ladder, the near-wall adaptive-priority
  falsification search,
  exchange-motif covering, and the 790-partition favorite-\(2+1+1\)
  boundary at the sufficient integer cap 19,683. The
  complete-partition/Hall formulation remains the independent structural
  route.
- **Review level:** the \((4,8)\) theorem has deep internal formal and
  certificate review; the new general-goal experiments have exact replay
  where stated but have not received external review.
- **Research level:** the fixed-cell theorem and formal package are
  specialized research-paper level. The general goal would be a field-level
  breakthrough. The present campaign has not reached that threshold.

## Ordered next gates

1. Treat fixed-order lex-max partial completion as closed and falsified.
   Continue the all-order CEGAR over jointly feasible candidate cells; a
   terminal SAT model would refute adaptive priority.
2. Canonicalize the small takeover motifs in closed cells. Generalize the
   forced singleton-swap proof to one-transfer bundle exchanges and prove
   that every all-orders-blocked family contains a covered motif.
3. Prove the balanced-or-designated-favorite-singleton dichotomy without a
   value cap. The cap-12/13 boundaries identify three separate balanced
   failures, and the singleton reduction leaves only one owner's threshold
   inequalities. Two unrestricted-real boundary profiles now show that
   each branch is independently necessary: one has only balanced EFX and
   the other only favorite-singleton EFX.
   The full-cap residual gate and exact trust boundary are in
   [COMMON_FAVORITE_SUFFICIENT_CAP_GATE.md](COMMON_FAVORITE_SUFFICIENT_CAP_GATE.md).
   Its matching and Hall encodings both remain unknown on the
   811-partition pool; the independently reconstructed chain is
   [efx49_common_favorite_sufficient_cap_audit.json](efx49_common_favorite_sufficient_cap_audit.json).
4. Continue the 790-partition favorite-\(2+1+1\) boundary at cap 19,683, but
   do not spend more solver time on the full 953-family formula without a
   smaller learned core.
5. Use the favorite-singleton Hall lemma as the common language for the two
   branches: combine the scalar/Hall obstruction attached to every residual
   partition with the Hall obstruction attached to every balanced partition,
   and search for a short Farkas or exchange contradiction. In the
   universal-threshold subcase, the common-three side of the half-favorite
   dichotomy is now proved; attack the remaining four-distinct-
   representatives side. A cap-free analytic three-set construction now
   supplies a balanced favorite-pair state in which every owner receives at
   least its favorite; the dual exact-real closure is retained as an
   independent check. The favorite-pair rank-augmentation route is refuted,
   as is its radius-two strengthening. Prove instead that either some
   favorite-pair partition supports an EFX matching or two goods can join
   the favorite while the remaining three pairs have a Hall matching to
   three agents at the favorite-triple deletion threshold. The latter is
   now an exact cap-free characterization, not merely a sufficient repair.
   The immediate computational target is the stronger full-cell dichotomy;
   the ultimate analytic gate below needs only one such pairing.
   Its only obstructions are a zero-neighbor pair, two pairs with at most
   one combined neighbor, or three pairs with at most two combined
   neighbors. The next proof unit is to convert the Hall obstruction to
   every favorite-pair partition into an edge-labeled perfect matching
   avoiding those three witnesses.
   A useful sufficient local bridge is two universally safe pairs and a
   third with at most one rejecter; this already gives favorite-triple EFX
   without the comparison condition needed to move the favorite back into
   a pair.
   Two stronger observer-independent normal forms are exactly refuted by
   strict generic profiles. Then tackle mixed threshold/Hall obstructions.
   The closed branch and proof are in
   [COMMON_THREE_LEXICOGRAPHIC_PARKING_LEMMA.md](COMMON_THREE_LEXICOGRAPHIC_PARKING_LEMMA.md).
   The live branch is in
   [DISTINCT_HALF_FAVORITE_GATE.md](DISTINCT_HALF_FAVORITE_GATE.md).
   The analytic floor construction is
   [DISTINCT_HALF_DENSITY_FLOOR_LEMMA.md](DISTINCT_HALF_DENSITY_FLOOR_LEMMA.md).
   The refuted rank target and exact diagnostic boundaries are
   [DISTINCT_HALF_RANK_AUGMENTATION_GATE.md](DISTINCT_HALF_RANK_AUGMENTATION_GATE.md).
   The replacement analytic repair is
   [COMMON_LOW_FAVORITE_TRIPLE_LEMMA.md](COMMON_LOW_FAVORITE_TRIPLE_LEMMA.md).
   The exact favorite-triple criterion is
   [FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md](FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md).
   The local conversion is
   [ONE_DEFECT_FAVORITE_TRIPLE_CONVERSION_LEMMA.md](ONE_DEFECT_FAVORITE_TRIPLE_CONVERSION_LEMMA.md).
   The finite cap-5 and cap-6 closures, with deletion-minimal 17- and
   21-partition certificates, are in
   [DISTINCT_HALF_FULL_CELL_CAP5_THEOREM.md](DISTINCT_HALF_FULL_CELL_CAP5_THEOREM.md)
   and
   [DISTINCT_HALF_FULL_CELL_CAP6_THEOREM.md](DISTINCT_HALF_FULL_CELL_CAP6_THEOREM.md).
   The cap-5 core's 17 literal templates already fail at cap 6 even though
   the larger cap-6 theorem holds. Their six-orbit symmetry closure is also
   refuted at cap 20. Adding both repair orbits gives a natural conservative
   eight-orbit successor—equivalently, the favorite-pair states whose triple
   is not all representatives—leaving only two terminal orbit types outside
   it. The one profile logically forces inclusion of at least one repair
   orbit, not both. A correctly scoped 780-partition
   cap-20 CP-SAT test returned `UNKNOWN` after 473.93 seconds. A separate
   exact-real cardinal CEGAR reached a 173-cut `unknown` boundary after one
   new 300-repair trace model and a 300-second continuation. A later
   diversified pool obstructing 708 of 780 states also returned `unknown`
   after 600 seconds. Cap-20 optimization found a 30-repair checkpoint with
   684 complete EFX allocations, but no positive lower bound. See
   [DISTINCT_HALF_FULL_CELL_ORBIT_GATE.md](DISTINCT_HALF_FULL_CELL_ORBIT_GATE.md).
   The live Hall-witness route splits exhaustively into six simultaneous
   representative-pair singleton witnesses or one canonical nonsingleton
   cell. Inside the singleton side, 17 of 21 cap-6 boundaries share one
   unrepresented witness edge across all six cells. That condition is four
   second-order-statistic inequalities; its 256 labeled representative maps
   reduce to 19 conjugacy orbits. Exact-real common-edge and complementary
   formulas both remain `UNKNOWN`, so this is a proof-search compression,
   not a cap-free theorem. See
   [DISTINCT_HALF_RR_HALL_SPLIT_GATE.md](DISTINCT_HALF_RR_HALL_SPLIT_GATE.md).
   At the two terminal orbits, one-swap exchange is false but radius two is
   now a dual-verified cap-5 theorem across all seven canonical EFX-matching
   cells, without any full-Hall-cell exclusion. This is a local proof-mining
   result, not a new existence range. The unrestricted implication is false
   at cap 20 despite earlier timeouts. See
   [DISTINCT_HALF_TERMINAL_EXCHANGE_GATE.md](DISTINCT_HALF_TERMINAL_EXCHANGE_GATE.md).
   In the first canonical R-cell, a cap-20 profile blocks the entire
   138-state family while having no full Hall cell. Its 290 eight-orbit
   repairs begin at distance three, so the global 780-state selector remains
   viable but the local proof route does not.
   Do not infer a cap-free conclusion from the finite-domain UNSAT result.
6. If a zero-complete-EFX model appears anywhere, accept it only after
   independent enumeration of all 7,770 partitions and all \(4^9\) labeled
   allocations.
7. Convert every useful finite closure into an analytic Hall or exchange
   lemma that can apply beyond nine goods; static selectors and bounded
   local-transfer potentials already refuted here remain abandoned.
8. Replace heuristic small-value searches with proof-producing bit-vector
   or pseudo-Boolean coverage up to the sufficient cap \(K_m\), using
   CEGAR and symmetry rather than literal valuation enumeration.
