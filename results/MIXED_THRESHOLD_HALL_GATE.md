# Mixed Threshold/Hall Gate

**Status:** open branch; rank-two selection and two earlier shortcuts exactly
refuted  
**Scope:** four agents, nine goods, positive additive valuations, and a
strict common favorite  
**Not claimed:** complete EFX for the full common-favorite cell, the full
four-agent/nine-good cell, or general additive EFX

## Basic explanation

Fix the common favorite (f). To give (f) alone to agent (a), split the
other eight goods into three bundles. Two independent tests are necessary
and sufficient:

1. the prospective owner (a) must regard every residual bundle as safe
   after its least-valued good is removed; and
2. the other three agents must have a perfect matching to the three
   residual bundles in their EFX-feasibility graph.

The universal-threshold theorem closes the extreme case in which test 1
fails for every owner and every residual partition. The remaining
common-favorite branch is therefore exact:

> some owner--partition pair passes test 1, but every pair that passes test
> 1 fails the resident Hall test; prove that a balanced partition of shape
> (3+2+2+2) supports EFX.

The first tempting shortcut was that a threshold pass might itself force a
Hall-valid singleton allocation, perhaps after changing the residual
partition. The exact boundaries below refute that claim.

## Exact mixed-branch boundaries

The following two positive integer matrices have the strict common favorite
in column zero:

\[
V^{611}=\begin{pmatrix}
20&2&2&6&4&1&6&15&19\\
20&19&1&19&19&19&1&1&18\\
20&19&1&19&1&1&19&19&11\\
20&19&19&1&19&1&19&19&3
\end{pmatrix},
\]

\[
V^{332}=\begin{pmatrix}
20&1&19&1&1&19&1&1&19\\
20&1&1&19&19&1&5&19&1\\
20&17&1&19&19&1&1&19&1\\
20&5&19&1&1&19&1&4&19
\end{pmatrix}.
\]

For (V^{611}), owner zero passes the threshold on

\[
\{1,2,3,4,5,6\}\mid\{7\}\mid\{8\}.
\]

The resident graph has rank one: all three residents accept only the large
bundle. Across the full residual universe, 114 owner--partition pairs pass
the threshold, but every one is Hall-deficient. Literal enumeration finds
606 EFX-supporting unlabeled partitions and 1,532 labeled complete EFX
allocations; every supporting partition has shape (3+2+2+2). The nearest
balanced repair is three good transfers away from the displayed residual
partition.

For (V^{332}), owner zero passes the threshold on

\[
\{1,2,3\}\mid\{4,5,6\}\mid\{7,8\}.
\]

Its resident graph has rank two and the last pair has no resident neighbor.
There are 273 threshold-passing owner--partition pairs, all Hall-deficient.
Literal enumeration finds 396 EFX-supporting partitions and 1,494 complete
EFX allocations, again all balanced. Five supporting balanced partitions
are only one transfer from the displayed residual partition.

The independently regenerated census is
[efx49_common_favorite_mixed_hall_boundaries_audit.json](efx49_common_favorite_mixed_hall_boundaries_audit.json).
The CP-SAT searches merely found the matrices; the frozen audit directly
rechecks every one of the 3,864 owner--residual-partition pairs, all 7,770
complete bundle partitions, and every labeled complete allocation.

## The fixed one-transfer rule is false

For a threshold-passing residual partition of shape (3+3+2), there are six
obvious balanced conversions: move one good from either triple onto the
singleton favorite. A third exact profile blocks all six conversions and
every favorite-singleton partition. It nevertheless has 387 balanced
EFX-supporting partitions and 1,097 labeled complete EFX allocations. Its
nearest repair requires two transfers.

The exact profile, six obstructed conversions, and nearest-repair census are
frozen in
[efx49_common_favorite_mixed_hall_local6_boundary_audit.json](efx49_common_favorite_mixed_hall_local6_boundary_audit.json).
Thus a successful proof cannot fix an arbitrary threshold-passing partition
and perform only one transfer.

## Rank-maximal selection refuted

Across the three exact profiles above, the maximum resident matching rank
among threshold-passing pairs is two. The numbers of rank-two passes are 49,
273, and 17; respectively 40, 153, and 11 of them contain a residual bundle
with no resident neighbor. Thus all three profiles are consistent with the
selection lemma that every mixed profile has a rank-two threshold pass, and
even with the stronger zero-neighbor version.

Two bounded cap-20 CEGAR searches did not decide either statement. The
zero-neighbor search found 49 motifs in its first exact model, learned all of
them, and then timed out. The rank-two search found 61 and then 5 new motifs
in two exact models before reaching its iteration limit. The independently
reconstructed profile and search censuses are frozen in
[efx49_common_favorite_mixed_selection_gate_audit.json](efx49_common_favorite_mixed_selection_gate_audit.json).
These endpoints are neither proofs nor counterexamples.

A symmetry-reduced continuation now extends those exact frontiers. Four new
rank-two models add \(9,1,13,30\) motifs, taking the cumulative pool from 66
to 119. Four new zero-neighbor models add \(11,3,3,3\), taking that pool from
49 to 69. Every trace model, seed hash, motif census, and learned-count
transition is independently reconstructed in
[efx49_common_favorite_mixed_selection_gate_audit_v2.json](efx49_common_favorite_mixed_selection_gate_audit_v2.json).
The endpoints remain iteration limits, not evidence that the claims are true
or false.

The candidate lemma is now exactly false, already at value cap 4. The profile

\[
\begin{pmatrix}
4&3&1&1&2&2&2&3&3\\
4&3&1&1&3&3&3&2&2\\
4&3&1&1&3&3&3&2&2\\
4&3&1&1&3&3&3&2&2
\end{pmatrix}
\]

has a strict common favorite and exactly three threshold-passing
owner--partition pairs, but every corresponding resident graph has matching
rank one. None of the 966 favorite-singleton partitions supports EFX. Literal
enumeration nevertheless finds 195 supporting partitions, all balanced, and
3,690 labeled complete EFX allocations. The three nearest balanced repairs
are one transfer away. The independent replay is
[efx49_common_favorite_rank2_selection_refutation_audit.json](efx49_common_favorite_rank2_selection_refutation_audit.json).

Thus both unconditional selectors are retired. The profile has only two
valuation types, so it is deliberately not an EFX counterexample and lies
inside a previously known existence class. The first computational repair
required four pairwise nonproportional rows. The sharper mathematical
boundary is ordinal: because EFX depends only on bundle comparisons, the
three-types theorem immediately extends to at most three bundle-order types.
A genuinely open four-agent profile may therefore be assumed to have four
pairwise bundle-order-inequivalent rows.

Two cumulative symmetry-reduced runs in that repaired stratum first started
from 29 valid rank-two obstruction motifs, found 12 further exact four-type
profiles, and enlarged the pool to 77 motifs. The new-motif sequence was
\(6,3,3,3,3,3,3,3,6,3,6,6\). Every trace profile has four pairwise
nonproportional rows, and every seed hash, proto hash, motif census, and
learned-count transition is replayed in
[efx49_common_favorite_fourtype_rank2_frontier_audit.json](efx49_common_favorite_fourtype_rank2_frontier_audit.json).
Those two endpoints were iteration limits.

The next cumulative session exactly refutes the repaired selector. Its
profile is

\[
\begin{pmatrix}
4&2&2&2&3&1&1&3&3\\
4&3&1&1&2&3&3&3&2\\
4&1&2&2&2&3&3&3&2\\
4&1&2&2&2&3&3&2&3
\end{pmatrix}.
\]

All four rows are pairwise nonproportional and, more strongly, pairwise
bundle-order inequivalent across all \(2^9\) bundles. Exactly three
owner--partition pairs pass the threshold, all for owner zero and all with
resident matching rank one; none of the 966 favorite-singleton partitions
supports EFX. Literal enumeration nevertheless finds 599 supporting
partitions, all balanced, and two independent counters agree on 3,878
complete EFX allocations. The three nearest balanced repairs are one
transfer away. See
[efx49_common_favorite_fourtype_rank2_refutation_audit.json](efx49_common_favorite_fourtype_rank2_refutation_audit.json).

Thus even the relevant preference-type restriction does not rescue
rank-maximal selection. A proof of the mixed branch must handle a rank-one
maximum inside the genuinely open four-preference-type stratum.

The rank-one side now has an analytic normal form. Because every feasibility
row is nonempty, matching rank one forces all three residents to accept only
one common bundle (A). Each resident then satisfies the strict inequality

\[
v_i(A)-\min A>\max\{v_i(B),v_i(C)\}.
\]

This yields an exact owner-switch reduction and separates the common-pair
and common-triple cases. The proof and exact boundaries are recorded in
[RANK_ONE_COMMON_COLUMN_NORMAL_FORM.md](RANK_ONE_COMMON_COLUMN_NORMAL_FORM.md).
The strongest local result is negative: even with every favorite-singleton
allocation excluded, one rank-one profile blocks all six one-good transfers.
Its nearest EFX repairs require two transfers. Bundle-origin symmetry first
compressed the natural successor to 21 states in which the favorite receives
a good from the contested triple; a second exact profile now refutes that
implication too, while forcing all nine nearest repairs into one missing
role-switching bridge orbit. The resulting 30-state union is also now
exactly refuted by a zero-singleton cap-6 profile. Its 15 nearest repairs add
two origin orbits, leaving a 45-state successor whose first bounded campaign
reaches a six-singleton Hamming-two local minimum. Its identical-resident
cap-6 subcell is dual-encoded `UNSAT`; unequal residents remain open. The current gate is
recorded in
[RANK_ONE_RADIUS_TWO_BRIDGE_GATE.md](RANK_ONE_RADIUS_TWO_BRIDGE_GATE.md).
The repeated-resident cap-5 certificate has since been compressed from 392
singleton cuts to one shared 112-partition dual-encoded menu. A cap-6 ladder
refutes the cap-free extension of that menu and remains SAT through 196 cuts;
see [RANK_ONE_CORE_SHAPE_LADDER_GATE.md](RANK_ONE_CORE_SHAPE_LADDER_GATE.md).

## Precise next gate

Choose a threshold-passing owner--partition pair lexicographically, first
maximizing the resident matching rank. If the rank is three, the singleton
allocation is EFX. Otherwise the Hall obstruction has one of three forms:

1. a residual bundle has no resident neighbor;
2. two residual bundles have at most one resident neighbor; or
3. the three residual bundles have at most two resident neighbors, with no
   smaller deficient subfamily.

Rank maximization no longer removes the rank-one branch. The exact proof split
must instead handle both possibilities:

1. a rank-one maximum, using the common-column normal form and an adaptive
   balanced conversion (the new cap-4 refutation itself has three successful
   one-transfer repairs); and
2. a rank-two maximum, using a selected-pair alternating exchange and then the
   two-bundle Hall witness.

Owner and residual-partition changes remain necessary. The finite proof-mining
target should search for one conversion family that covers the new rank-one
boundary together with the earlier 45-state bridge boundaries, rather than
trying to force rank two first.

The radius-two family has exactly 63 balanced partitions around the fixed
canonical \(3+3+2\) state. Direct CP-SAT models remained `UNKNOWN` at caps 6
and 20 after 180 and 300 seconds. A cap-6 counterexample-guided rebuild
learned 488 of the 966 singleton obstructions across six exact models before
its next 60-second master also returned `UNKNOWN`. The reconstructed trace
and all three model hashes are frozen in
[efx49_common_favorite_mixed_hall_radius2_gate_audit.json](efx49_common_favorite_mixed_hall_radius2_gate_audit.json).
This is an open computational boundary, not evidence of either truth value.

This gate is smaller than the original common-favorite dichotomy but is not
yet a theorem. A proof would close the strict common-favorite
four-agent/nine-good cell when combined with the universal-threshold theorem;
it would still leave the other favorite-multiplicity cells and the general
additive EFX conjecture open.
