# Mixed Threshold/Hall Gate

**Status:** open branch with two exact shortcut refutations  
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

## Rank-maximal selection boundary

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

The rank-one side now has an analytic normal form. Because every feasibility
row is nonempty, matching rank one forces all three residents to accept only
one common bundle (A). Each resident then satisfies the strict inequality

\[
v_i(A)-\min A>\max\{v_i(B),v_i(C)\}.
\]

This yields an exact owner-switch reduction and separates the common-pair
and common-triple cases. The proof, the unconditional three-conversion
counterexample, and the sparse 185-cut successor gate are recorded in
[RANK_ONE_COMMON_COLUMN_NORMAL_FORM.md](RANK_ONE_COMMON_COLUMN_NORMAL_FORM.md).

## Precise next gate

Choose a threshold-passing owner--partition pair lexicographically, first
maximizing the resident matching rank. If the rank is three, the singleton
allocation is EFX. Otherwise the Hall obstruction has one of three forms:

1. a residual bundle has no resident neighbor;
2. two residual bundles have at most one resident neighbor; or
3. the three residual bundles have at most two resident neighbors, with no
   smaller deficient subfamily.

The next analytic target has two steps: first prove the **rank-two selection
lemma** suggested by the exact census; then prove a **selected-pair
alternating-exchange lemma** transforming such a pair, while allowing the
owner and residual partition to change, into a balanced Hall-perfect
partition. The boundaries show why both freedoms are necessary. The finite
proof-mining target should begin with the rank-two/zero-neighbor case and a
radius-two exchange family, then treat the two-bundle Hall witness.

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
