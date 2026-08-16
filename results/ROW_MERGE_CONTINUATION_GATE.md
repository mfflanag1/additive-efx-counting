# Row-Merge Continuation Gate

**Status:** cap-free resident-extension lemma proved; the stronger
fixed-partition continuation and all tested bounded local restart rules are
refuted; continuation theorem open  
**Scope:** four positive-additive agents and any finite number of goods  
**Not claimed:** a proof of EFX existence, a counterexample, or established
novelty of the formulation

## Breakthrough reduction

Fix an arbitrary four-agent instance with valuation rows
\(v_0,v_1,v_2,v_3\). Replace one row, say \(v_3\), by the path

\[
v_3(t)=(1-t)v_2+t v_3,\qquad 0\le t\le1. \tag{1}
\]

At \(t=0\), agents 2 and 3 have the same valuation. The instance therefore
has at most three valuation types, so complete EFX exists by the published
three-types theorem of Ghosal, Prakash, Nimbhorkar, and Varma.

Consequently, the following continuation statement would resolve complete
EFX existence for four additive agents:

> **Row-merge continuation conjecture.** Along (1), the set of parameters
> \(t\in[0,1]\) admitting a complete EFX allocation is the entire interval.

Only one ordered merge per instance is needed for this reduction. The
converse is immediate if general four-agent EFX holds, so—given the published
three-types theorem—row-merge continuation is an equivalent reformulation,
not a weaker claim. It is not presented as easier by definition; its value is
as a one-parameter normal form whose first possible failure has much more
structure than an arbitrary counterexample.

The safe endpoint is the published theorem
[*EFX Exists for Three Types of Agents*](https://doi.org/10.1145/3736252.3742509)
(EC 2025). A targeted literature search found no prior EFX argument using
this exact row-interpolation continuation, but that search is not an
exhaustive novelty proof.

## Exact interval lemma

For a fixed labeled complete allocation \(X\), EFX feasibility along (1) is
an interval, possibly empty. The EFX inequalities of agents 0, 1, and 2 do
not depend on \(t\). Every inequality of agent 3 has the form

\[
v_3(t)(X_3)\;\ge\;v_3(t)(X_j\setminus\{g\}),
\]

which is one affine inequality in \(t\). Their intersection with
\([0,1]\) is a closed interval. Hence the complete EFX existence set is an
exact finite union of closed rational intervals whenever the endpoint rows
are rational.

This gives a sharp first-gap certificate. If coverage ends at
\(t^*<1\), at least one EFX allocation exists at \(t^*\), at least one of
the moving agent's inequalities is tight there, and no allocation interval
starts soon enough to continue past it. The next analytic target is a pivot
lemma that constructs such a successor allocation from the tight comparison.

## Stable-partition Hall reduction

There is a sharper cap-free formulation in which the bundles remain fixed
and only their owners may change. Fix an unlabeled partition
\(P=(B_0,B_1,B_2,B_3)\). For an agent \(i\), let \(i\to B_k\) mean that
assigning \(B_k\) to \(i\) satisfies all of \(i\)'s EFX comparisons against
the other three bundles. Remove the moving agent \(a\), and define the
resident-extension set

\[
S_a(P)=\{k:\text{the three fixed agents can be perfectly matched to }
P\setminus\{B_k\}\}.
\]

Then \(P\) supports an EFX allocation at parameter \(t\) if and only if the
moving agent has an EFX-feasible edge to some \(B_k\) with \(k\in S_a(P)\).
This is just the perfect-matching characterization, split according to the
bundle assigned to \(a\). For each fixed \(k\), the set of such parameters is
a closed interval, because all of the moving agent's comparisons are affine
in \(t\). Thus support by one fixed partition is a union of at most four
explicit intervals; assignments may pivot while the bundles do not.

The merged endpoint supplies nontrivial redundancy. If \(P\) supports EFX at
\(t=0\), the moving agent and the base agent have identical rows. In any
supporting matching they receive two distinct bundles; swapping those two
agents gives a second supporting matching. Consequently at least two
distinct bundles belong to \(S_a(P)\) and are feasible for the moving agent
at \(t=0\).

A useful sufficient condition also follows. If \(S_a(P)\) contains all four
bundles, then \(P\) supports EFX for every \(t\in[0,1]\): at every parameter,
the moving agent can take a bundle of maximum total value, which is always
EFX-feasible relative to \(P\), and the residents can fill the other three
bundles. More generally, the exact target is to show that the four edge
intervals indexed by \(S_a(P)\) cover the unit interval.

This resident-extension lemma is proved by the preceding matching argument.
The stronger assertion that some fixed partition supports every point of
every row merge is false. An exact positive seven-good profile has nine EFX
partitions at the original endpoint and eight at the merged endpoint, with
disjoint partition sets. Its path is nevertheless fully EFX-covered by two
labeled allocations whose intervals overlap. See
[row_merge_no_stable_partition_m7_audit.json](row_merge_no_stable_partition_m7_audit.json).

At a first failure of a fixed partition, every feasible bundle of the moving
agent lies outside \(S_a(P)\) immediately to the right, while at least one
interval indexed by \(S_a(P)\) ends at a tight affine comparison. This is the
finite Hall/tightness configuration that a successor-pivot lemma must repair.

## Ordinal-chamber corollary

The same reduction closes a cap-free class larger than proportional or
identical rows. Call two valuation rows bundle-order equivalent when they
induce the same weak ordering on all \(2^m\) bundles. If the moving row and
the base row are bundle-order equivalent, take any EFX allocation at the
merged endpoint. Every EFX comparison made by the moving agent has the same
truth value under the target row, while every other agent is unchanged.
The same allocation is therefore EFX at the target.

Consequently, the published theorem for at most three identical valuation
functions immediately extends, for EFX existence, to at most three
bundle-order types. In particular, a genuinely open four-agent instance may
be assumed to have four pairwise bundle-order-inequivalent rows. Along a
row interpolation this says that no pivot is needed while the moving row
stays inside one subset-sum order chamber; pivots are needed only when a
bundle-comparison hyperplane is crossed.

This is a direct ordinal corollary, not claimed as a separately established
literature theorem. A targeted search found work on identical rankings of
individual goods, but not this exact bundle-order-type formulation.

## Single-wall pivot target

For one additive row, bundle-order types are the chambers of a finite
hyperplane arrangement. Its walls have the form

\[
\sum_{g\in U}v(g)=\sum_{g\in W}v(g)
\]

for two bundles \(U,W\). Inside one open chamber, every bundle comparison has
fixed sign. Hence every EFX edge of the moving agent is fixed, and any EFX
allocation remains EFX throughout that chamber.

After the standard nondegenerate perturbation reduction, connect the base row
to the target row by a generic polygonal path in the positive orthant. The
path can be chosen to cross one subset-sum wall at a time, avoiding
intersections of distinct walls. This reduces the continuation conjecture to
the following local statement:

> **Single-wall pivot conjecture.** If only one agent's valuation crosses one
> bundle-order wall while the other three rows remain fixed, complete EFX
> existence cannot disappear at that crossing.

At such a crossing, an existing allocation can fail only if the moving
agent's own bundle and one envied bundle remainder realize the comparison
whose sign flips. All other inequalities and all other agents' feasibility
edges remain unchanged. A proof may change the assignment within the fixed
partition using the resident-extension set, or pivot the partition using
that one tight comparison.

One part of the pivot is immediate. In the feasibility graph of the current
four bundles, the crossing deletes at most one edge, incident to the moving
agent. If some perfect matching avoids that edge, the same matching and
partition remain EFX after the crossing. Therefore a genuine same-partition
failure requires the deleted edge to belong to every perfect matching.
Equivalently, deleting it creates a Hall obstruction, and the moving agent
has no other edge into the resident-extension set. This **essential-edge
lemma** is cap-free; only the essential-edge case requires a bundle-changing
pivot.

The resulting Hall obstruction has only four sizes. Let \(e=(a,B_0)\) be the
deleted essential edge and let \(Q\) be a minimal Hall-deficient agent set in
the graph without \(e\). Then \(a\in Q\), since all other rows are unchanged,
and \(B_0\notin N(Q)\), since otherwise restoring \(e\) would not repair
Hall's condition. Because restoring one edge does repair it,
\(|N(Q)|=|Q|-1\). Therefore \(|Q|\in\{1,2,3,4\}\): the moving agent alone
loses its only edge, or it is confined with one, two, or three fixed agents
to respectively one, two, or three bundles. This **essential-edge Hall
classification** is also cap-free. The bundle-changing wall pivot can be
split into exactly these four deficiency sizes.

The independent graph census
[row_merge_essential_edge_hall_audit.json](row_merge_essential_edge_hall_audit.json)
checks all 4,929 labeled essential-edge graphs, reducing them to 213 orbits
under resident and noncritical-bundle permutations. The four witness sizes
occur in 92, 36, 36, and 49 orbits. This census checks the case split; the
short Hall argument above proves it.

The size-one graph case cannot occur at a genuine additive wall crossing.
Every agent has at least one feasible bundle in every fixed partition: a
maximum-total bundle is feasible. A generic wall crossing deletes at most
the one critical edge and leaves the other three entries of the moving row
unchanged. If that edge were the row's sole neighbor, the row would become
empty, contradicting the maximum-bundle observation. Thus the
bundle-changing pivot has only the three realizable Hall sizes
\(|Q|=2,3,4\), matching the familiar one-, two-, and three-neighbor
deficiencies.

Proving this local conjecture would resolve the four-agent additive problem,
so the reduction does not make it easy by definition. It does replace an
arbitrary valuation matrix by one named equality, one moving feasibility row,
and a fixed three-resident Hall graph. This is now the smallest cap-free
analytic gate.

## Local-radius pivot no-go

The first concrete pivot menu is false. Exact positive-real constructions at
seven goods realize each Hall size \(2,3,4\) at a generic wall where the
original feasibility graph loses exactly the one critical edge. For Hall
sizes two and three, no EFX-supporting partition lies within two good
transfers of the failed partition; their nearest complete EFX partitions are
at distance three. For Hall size four, every one-transfer partition can fail,
with the nearest support at distance two.

These models are independently enumerated in
[row_merge_single_wall_radius_refutation_audit.json](row_merge_single_wall_radius_refutation_audit.json).
They are positive EFX instances, not counterexamples: the three post-wall
profiles have respectively 16, 40, and 57 complete EFX allocations. The
full construction, exact counts, and a dual-solver positive boundary for one
Hall-size-four radius-two cell are documented in
[SINGLE_WALL_PIVOT_GATE.md](SINGLE_WALL_PIVOT_GATE.md).

Proof mining sharpens that positive boundary substantially. In the
\(2+2+2+1\) Hall-size-four cell, the deletion-minimal seven-partition menu
uses only two noncritical subset-order assumptions, exactly
\(\delta<v_0(4)\) and \(\delta<v_0(5)\). These hold automatically for a
sufficiently small continuation step. In the balanced eight-good
\(2+2+2+2\) cell, the symmetric 11-partition pair menu is exact UNSAT under
the analogous four small-step bounds. Z3 and cvc5 independently verify both
formulas.

Consequently, Hall size four now has a positive balanced-wall pivot, but the
live statement is still not a universal bounded one- or two-good repair.
Hall sizes two and three require a longer exchange chain or a global
potential. Hall size four does too once a resident bundle grows: an exact
\(2+2+2+3\) small-step wall blocks all 319 radius-two partitions. It retains
206 complete EFX allocations, beginning at distance three, so this is the
first unbalanced exchange-length boundary rather than a counterexample.

The distance-three census has now been compressed to a simple exchange-chain
candidate: 515 partitions generated by one-good transfer paths and cycles of
length at most three. Eight repair the terminal radius-two profile. The
universal fixed-cell statement is still open. Exact CEGAR finds 48 repairs
after 24 cuts and nine repairs in a fixed Hall graph after 32 cuts, while the
36-, 40-, and 56-cut continuations reach exact-solver limits. Matching-clause
and Hall-selector encodings agree on all 50,625 nonempty-row feasibility
graphs and both time out at the 56-cut fixed cell. See
[ROW_MERGE_EXCHANGE_CHAIN_GATE.md](ROW_MERGE_EXCHANGE_CHAIN_GATE.md).

## Partial-restart boundary

Deleting one good before pivoting does not rescue a Hall-local rule. A
generic seven-good Hall-size-three wall has no EFX partial allocation among
all 150 states obtained by deleting a good from the three deficient bundles
and repartitioning only those bundles. A valid nearest partial state exists
at distance one only by changing a bundle outside the minimal Hall block.
The witness and independent literal audit are
[row_merge_deficient_block_restart_refutation_m7_q3_witness.json](row_merge_deficient_block_restart_refutation_m7_q3_witness.json)
and
[row_merge_deficient_block_restart_refutation_m7_q3_audit.json](row_merge_deficient_block_restart_refutation_m7_q3_audit.json).

For the fixed seven-good shape \(2+2+2+1\), a genuinely global rule does
close the encoded wall cell: for each Hall size \(2,3,4\), one may delete any
good, move at most one remaining good globally, and reassign bundle owners.
At least one of the resulting 81 partitions supports partial EFX. Z3 and
pinned cvc5 independently return UNSAT for the negation in all three Hall
sizes; the aggregate chain is recorded in
[row_merge_global_partial_restart_m7_audit.json](row_merge_global_partial_restart_m7_audit.json).
This is only a seven-good partial-EFX lemma, not a completion lemma.

It is also sharp against the first larger padding. At eight goods, Hall size
three and wall shape \(3+2+2+1\), an exact isolated-wall witness blocks all
126 delete-one/move-at-most-one restart partitions. The nearest partial EFX
partition needs two transfers; the post-wall instance still has 218 complete
EFX allocations. See
[row_merge_global_partial_radius1_m8_uplus_refutation.json](row_merge_global_partial_radius1_m8_uplus_refutation.json).
Three other eight-good padding formulas timed out and prove nothing.

Thus partial restart is useful only when coupled to a scalable completion
invariant. Existence of an arbitrary one-unallocated-good EFX allocation is
already known for four agents; locality without reinsertion structure does
not advance the general theorem.

## Tight \((4,9)\) audit

The exact count-four witness in
[tight49_witness.json](tight49_witness.json) is deliberately hostile: at the
target endpoint it has only four labeled complete EFX allocations. The audit
[tight49_row_merge_interpolation_audit.json](tight49_row_merge_interpolation_audit.json)
enumerates all \(4^9=262{,}144\) labeled allocations for each of the 12
ordered row merges.

Every path is covered by one fixed unlabeled bundle partition, allowing the
owners to change. Nine paths need only one fixed assignment to cover the
whole interval, and the remaining three need two assignments of the same
bundles. Five of the 12 paths have exactly one stable partition, so this is
already a sharp test of the stronger conjecture. For example, when row 3
separates from row 2, the stable partition is

\[
\{0,4\}\mid\{1\}\mid\{2\}\mid\{3,5,6,7,8\},
\]

and two assignments of it have intervals

\[
[0,37/38]\quad\text{and}\quad[8/17,1]
\]

already cover the path. Exactly four allocations survive at \(t=1\), in
agreement with the independent full EFX census.

The other three recorded count-four witnesses, at \((4,7)\), \((4,8)\), and
\((4,10)\), behave the same way: each of their 12 ordered row merges has a
stable partition. The \((4,7)\) witness needs only one assignment per path;
the \((4,8)\) and \((4,10)\) witnesses need at most two. Across these four
tight profiles, 17 of 48 paths have exactly one stable partition. See
[the \((4,7)\) audit](t47_row_merge_interpolation_audit.json),
[the \((4,8)\) audit](tb4_row_merge_interpolation_audit.json), and
[the \((4,10)\) audit](tight410_row_merge_interpolation_audit.json).

This is exact evidence about four extremal profiles, not a general theorem.

The two exact mixed-Hall boundary profiles provide a different adversarial
test. They have 1,532 and 1,494 complete allocations at the target endpoint,
but no favorite-singleton EFX allocation despite 114 and 273 threshold
passes. Across all 24 ordered row merges, one fixed assignment covers each
entire path. The 6+1+1 profile has between 322 and 456 stable partitions per
path; the 3+3+2 profile has between 216 and 396. See
[the 6+1+1 audit](efx49_common_favorite_threshold_pass_hall_611_row_merge_interpolation_audit.json)
and
[the 3+3+2 audit](efx49_common_favorite_threshold_pass_hall_332_row_merge_interpolation_audit.json).

Across all six audited profiles, all 72 ordered paths have a stable
partition. Sixty-three paths have a one-assignment cover and nine need two
assignments of the same bundles. This remains finite-profile evidence only.

## Next decisive tests

1. Construct a Hall-directed exchange chain whose progress measure is
   independent of the number of goods; fixed transfer radii are retired.
2. Couple any partial restart to the exact parking condition for its omitted
   good. A restart without a reinsertion invariant is redundant with the
   published almost-complete theorem.
3. Convert the seven-state and 11-state Hall-size-four cores into one human
   resident-matching lemma, then decide the nine-repair fixed-graph
   length-three exchange cell.
4. Search directly for a row path with two separated EFX interval components.
   Any uncovered parameter is a genuine additive EFX counterexample, not
   merely a refutation of the continuation method.
5. Test exchange-chain or potential statements by linear-arithmetic case splitting,
   with each computer-mined case independently proof-checked.

The executable audit is
[audit_row_merge_interpolation.py](../tracks/parkability/audit_row_merge_interpolation.py).
