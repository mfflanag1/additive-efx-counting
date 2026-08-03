# Common-Low Favorite-Triple Lemma

**Status:** cap-free analytic lemma  
**Scope:** four additive agents and nine goods with a strict common favorite

This is the complete-bipartite special case of the exact
[favorite-triple Hall characterization](FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md).
**Role:** repair alternative after the favorite-pair rank route fails

## Statement

Let \(f\) be a strict favorite of every agent and write
\(F_i=v_i(f)\). Suppose there are two other goods \(a,b\) and a partition
of the remaining six goods into three pairs \(P_1,P_2,P_3\) such that

\[
v_i(P_j)\ \ge\
F_i+\max\{v_i(a),v_i(b)\}
\tag{1}
\]

for every agent \(i\) and every \(j\in\{1,2,3\}\).

Then

\[
\{f,a,b\},\quad P_1,\quad P_2,\quad P_3
\]

is an EFX partition: every bijection between the four bundles and the four
agents is an EFX allocation.

## Proof

Fix an observer \(i\). The largest value left after deleting one good from
the favorite triple is

\[
\max_{g\in\{f,a,b\}}
v_i(\{f,a,b\}\setminus\{g\})
=F_i+\max\{v_i(a),v_i(b)\},
\]

because \(f\) is strictly more valuable than either \(a\) or \(b\).
By (1), every pair \(P_j\) is worth at least this amount. Thus an agent
owning any pair has no EFX envy toward the favorite triple.

Deleting one good from any pair leaves a singleton residual good. Its value
is strictly below \(F_i\). The favorite triple is worth at least \(F_i\),
and every pair is worth at least the right-hand side of (1), hence at least
\(F_i\). Consequently, an agent owning the favorite triple or any one of
the pairs has no EFX envy toward any pair.

Every one of the four bundles is therefore feasible for observer \(i\).
Since \(i\) was arbitrary, the four-agent/four-bundle EFX-feasibility graph
is complete. Every bundle assignment is EFX. \(\square\)

## Why this is now the right companion normal form

The former candidate tried to prove that the universal-threshold,
distinct-half-representative branch always had an EFX partition with \(f\)
in a pair. That statement is false. The strict integer profile

\[
\begin{pmatrix}
100&1&2&55&69&59&96&77&95\\
100&5&17&73&69&62&55&68&53\\
100&8&1&48&73&69&61&67&65\\
100&8&1&55&79&90&71&66&82
\end{pmatrix}
\]

satisfies the exact universal owner-threshold envelope and has the
half-favorite representatives \(3,4,5,6\), but none of the 840 balanced
partitions with \(f\) in a pair supports an EFX matching.

Complete EFX nevertheless survives in exactly 15 balanced partitions. All
15 put goods \(1,2\) with \(f\), and nine satisfy (1). Literal enumeration
finds 324 complete EFX allocations, all of shape \(3+2+2+2\) with \(f\) in
that triple. The reproducible census is
[efx49_distinct_half_favorite_pair_rank_boundary_audit.json](efx49_distinct_half_favorite_pair_rank_boundary_audit.json).

## Remaining conversion conjecture

The useful unproved target is now the following dichotomy:

> Under the universal owner-threshold envelope and a saturating
> half-favorite matching, either some balanced favorite-pair partition has
> a perfect EFX-feasibility matching, or the hypotheses of the common-low
> favorite-triple lemma hold.

This statement genuinely adds content. Its first alternative covers the
original owner-floor/exchange route; its second explains the strict
boundary that refutes favorite-pair rank augmentation. Proving the
dichotomy would close the four-distinct-representative side of the
universal-threshold subcase. It would not close the mixed
threshold/Hall-obstruction case or the general additive EFX problem.

The cap-free
[one-defect conversion lemma](ONE_DEFECT_FAVORITE_TRIPLE_CONVERSION_LEMMA.md)
gives a sharper route to this dichotomy. Conditional on the Hall
obstruction to every favorite-pair partition, it is enough to find two
universally safe residual pairs and a third pair with at most one rejecter
plus a two-pair matching condition. A unique rejecter would itself generate
a favorite-pair EFX allocation, so only the all-safe repair can remain.

The current exact boundary is unusually sharp. A branch-valid integer
profile has no favorite-pair EFX partition and exactly one common-low repair;
literal enumeration still finds 252 complete EFX allocations. The profile,
the compact 24/9 CEGAR boundary, and the weaker exact Hall fallback are
frozen in
[DISTINCT_HALF_CONVERSION_DICHOTOMY_GATE.md](DISTINCT_HALF_CONVERSION_DICHOTOMY_GATE.md).
