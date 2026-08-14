# PI-free desired-core support-drainage lemma

**Date:** 2026-08-13

**Status:** cap-free structural theorem; valuation/observer-safe arborescence
transfer remains

## Support dependency graph

Let `R` be a nonempty proper subset of the owners. For every `i in R`, let
`D_i` be a minimal common-safe desired core, and assume the `D_i` are
pairwise disjoint. Define a directed owner graph `G_D` by

\[
 i\longrightarrow a
 \quad\Longleftrightarrow\quad
 D_i\cap X_a\ne\varnothing,
 \qquad i\in R,\ a\in N.                         \tag{1}
\]

Base-charity goods create no owner edge.

## No closed represented subset

If the base champion graph has no generalized PI cycle, then every nonempty
`S subseteq R` has an outgoing support edge:

\[
                 \exists i\in S,\ a\notin S:
                 D_i\cap X_a\ne\varnothing.       \tag{2}
\]

Otherwise the subfamily `(D_i)_{i in S}` would be pairwise disjoint and all
its goods would be base-owned inside `S` or by charity. The closed
disjoint-core characterization would make it a generalized PI cycle.

Consequently every `i in R` has a directed path in `G_D` to an owner outside
`R`. Indeed, the set reachable from `i` would otherwise be a nonempty closed
subset of `R`, contradicting (2).

## Rank-three arborescence

For four owners and `R=N-{d}`, every represented source reaches the unique
outside owner `d`. Choosing, for each represented owner, one first edge on a
shortest path to `d` gives an in-arborescence rooted at `d`, with at most
three directed support incidences. Each incidence can be witnessed by a
distinct physical good because the source cores are disjoint.

Thus the selected rank-three matching carries a cap-free base-support
drainage tree into the sacrificed owner. This strengthens the earlier
statement that *some* selected core captures `d` support: all represented
sources lie upstream of `d` through selected-core provenance.

The same result applies after replacing one selected core by a disjoint
`d`-response core. The resulting three-source family drains to the displaced
represented owner. Hence both shared-target replacements generate crossed
drainage trees, exactly matching the crossed-provenance import lemma.

## Relation to four-edge extraction

The arborescence uses at most three owner-owner support incidences, leaving
one edge for the singleton charity transfer. This is the correct cap-free
edge geometry for the target theorem. However, (1) records base ownership of
goods inside desired cores, whereas the target edge count uses their current
physical suppliers. A complete proof must translate the drainage tree into
signed packet transfers that pay every intermediate owner and preserve all
observer thresholds. The base-support closure theorem pays the uncompressed
return; the missing step is observer-safe compression onto this three-edge
arborescence.

## Verification and boundary

`audit_pi_free_desired_core_support_drainage.py` exhausts all directed owner
support graphs on every nonempty proper source set. It independently checks
that the no-closed-subset condition is equivalent to reachability of the
outside set and constructs a shortest-path forest with at most one outgoing
edge per represented owner.

This theorem establishes support geometry only. It does not assert that a
single witness good has enough value to pay a donor, identify current
physical suppliers with base owners, prove observer safety, or finish the
four-edge theorem.
