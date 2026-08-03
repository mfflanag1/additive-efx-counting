# Distinct-Half Rank-Augmentation Gate

**Status:** refuted by a strict branch-valid integer profile  
**Scope:** the universal-threshold, distinct-half-representative branch for four agents and nine goods  
**Not claimed:** a counterexample to EFX existence

## Candidate

Consider the 840 partitions of shape \(3+2+2+2\) in which the strict common
favorite \(f\) lies in a pair. For a partition \(\mathcal P\), form its
four-agent/four-bundle EFX-feasibility graph: agent \(i\) is adjacent to
bundle \(B\) exactly when assigning \(B\) to \(i\) satisfies all of \(i\)'s
EFX comparisons against the other three bundles. Write \(r(\mathcal P)\)
for the maximum matching size in this graph.

Join two partitions when one can be obtained from the other by exchanging
one good between two bundles while preserving shape \(3+2+2+2\) and keeping
\(f\) in a pair. This is a 21-regular graph with 840 vertices and 8,820
undirected edges.

The proposed augmentation lemma is:

> Under the exact universal owner-threshold envelope and a saturating
> half-favorite matching, every connected component of partitions having
> the same rank \(r<4\) has an adjacent partition of strictly larger rank.

If true, the lemma would prove the distinct-representative gate immediately.
Choose a plateau at the largest rank attained by any partition. If that
rank were below four, augmentation would give a still larger rank, a
contradiction. Rank four is exactly a complete EFX allocation.

## Verdict: false

The strict profile

\[
\begin{pmatrix}
100&1&2&55&69&59&96&77&95\\
100&5&17&73&69&62&55&68&53\\
100&8&1&48&73&69&61&67&65\\
100&8&1&55&79&90&71&66&82
\end{pmatrix}
\]

satisfies the exact universal owner-threshold envelope and has the
half-favorite representatives \(3,4,5,6\). Nevertheless, the matching-rank
histogram on the 840 favorite-pair partitions is

\[
r=1:20,\qquad r=2:237,\qquad r=3:583,\qquad r=4:0.
\]

The rank-three component is therefore trapped and the proposed augmentation
lemma is false.

This is not an EFX counterexample. On all 1,260 balanced partitions the
rank histogram is \(278,359,608,15\), and literal enumeration of all
\(4^9\) labeled allocations finds 324 complete EFX allocations. Every one
has shape \(3+2+2+2\), puts the common favorite in a triple, and uses the
same triple \(\{0,1,2\}\). The independent census is
[efx49_distinct_half_favorite_pair_rank_boundary_audit.json](efx49_distinct_half_favorite_pair_rank_boundary_audit.json).

## Radius-two strengthening also fails

The statement permits arbitrarily many rank-preserving swaps before the
augmenting exit. That is essential: individual partitions can have no
one-step rank improvement even when their whole plateau has an exit.

Earlier stress data suggested a radius-two strengthening. A second strict
profile refutes it while retaining 312 rank-four partitions. Its selected
rank-three state has no augmenting swap and no rank-preserving swap followed
by an augmenting swap. The shortest route uses two rank-preserving swaps and
then one augmentation. The exact replay is
[efx49_distinct_half_rank_radius_boundary_audit.json](efx49_distinct_half_rank_radius_boundary_audit.json).

The former 256-profile stress audit remains useful only as historical
falsification evidence:
[efx49_distinct_half_rank_augmentation_audit.json](efx49_distinct_half_rank_augmentation_audit.json).
Its observed radius-two bound must not be generalized.

## Replacement proof target

The refuting profile reveals a structured repair. Goods \(1,2\) are low for
all four agents. Parking them with the favorite and pairing the other six
goods gives nine partitions satisfying the hypotheses of the cap-free
[COMMON_LOW_FAVORITE_TRIPLE_LEMMA.md](COMMON_LOW_FAVORITE_TRIPLE_LEMMA.md).

The surviving conversion target is a two-normal-form dichotomy: either some
favorite-pair balanced partition supports an EFX matching, or a
favorite-triple partition has a three-pair Hall matching at its exact
deletion threshold. The latter criterion is characterized in
[FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md](FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md);
the common-low repair above is its strongest observer-independent special
case. Proving the dichotomy would close the distinct-representative
universal-threshold branch. The old
favorite-pair plateau conjecture and every bounded radius-two version are
closed and must not be used.
