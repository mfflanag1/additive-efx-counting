# Two-by-two response-Hall normal form

**Date:** 2026-08-11

**Status:** exact cap-free classification and cross-block PI closure;
termination of the surviving empty-target/lower-dimensional forms remains
open

## Graph theorem

Let `U={u_0,u_1}` be two candidate response sources and
`V={v_0,v_1}` two targets.  For an arbitrary response relation
`E subseteq U times V`, exactly one of the following holds:

1. `E` has a matching covering both targets;
2. some target has empty response neighborhood; or
3. both target neighborhoods equal the same singleton `{u}`.

Indeed, if both neighborhoods are nonempty but there is no covering
matching, Hall's inequality forces their union to have size one.  Hence both
nonempty neighborhoods are the same singleton.  Conversely either an empty
target or a common singleton neighborhood plainly prevents a two-target
matching.

The classification is exhaustive for arbitrary bundles and uses no item
cap.  Among the 16 labeled two-by-two relations, seven have a covering
matching and nine do not.  Of the nine deficient relations, seven have an
empty target and the remaining two are the two possible common-singleton
stars.

## Cross-block PI theorem

After the two-hole selector, the wall localization gives two opposite
response blocks on the four displayed targets:

- represented core sources responding to the two residual targets; and
- the two holes responding to the two fixed core targets.

If both blocks have covering matchings, their disjoint union is the
release-compatible four-target SDR already proved by the two-hole lemma.
Suppose instead that neither block has an empty target.  Each block is then
either matching or a common-singleton star.  If one block is deficient, let
`u` be its common unique source.  The target owned by `u` is nonempty in the
opposite block, so some opposite-side source `v` responds to it.  Since `u`
responds to both opposite-side targets, it responds in particular to the
target owned by `v`.  Hence

\[
 u\longrightarrow v\longrightarrow u
\]

is a two-owner response cycle.  Its desired cores lie in the two distinct
owner bundles, so they are disjoint and internally supplied.  It is a
release-compatible PI component.

Therefore every two-hole boundary has one of three outcomes:

1. both blocks match, giving the full four-target SDR;
2. a cross-block two-owner response cycle gives a PI component; or
3. at least one displayed target has empty opposite-side response
   neighborhood.

This statement exhausts all 256 ordered pairs of labeled two-by-two
relations.  The exact audit finds no pair outside the three outcomes.

## Surviving empty-target reduction

If an empty target participates in an actual wall, the wall is
source-inactive relative to the opposite side.  For a hole strongly envying
a core while remaining below base, this is exactly the strict loss-band
branch of the cross-star and core/residual repair lemmas.

If the empty target participates in no wall, it is already irrelevant to
the EFX obstruction and can be deleted from the response boundary.  What
remains is a lower-dimensional aligned or disjoint star.  The aligned case
enters recapture; a source-active disjoint pair enters the cross-star hole
pivot; a source-inactive pair enters the repair chain.

Thus the two-hole conversion reduces every PI-free non-EFX survivor to a
source-inactive wall or a lower-dimensional pivot/recurrence, possibly
together with the root-critical polarity produced by the root-preserving
selector.  The full single-source two-target star cannot survive on its own.

## Why this is not yet closure

The graph theorem supplies no inequality reversing a source-inactive loss
band and does not itself terminate the lower-dimensional hole pivot.  A
valid termination proof must use one of the flower's global facts—minimal
payment, root criticality, lexicographic maximality, or generalized
PI-freeness—to turn the named inactive source into a connected transfer or
to make a revisit close a response cycle.

## Claim boundary

This result completely classifies the residual 2-by-2 Hall combinatorics and
eliminates the common-singleton star by a release-compatible PI cycle.  It
does not eliminate the empty-target/source-inactive form, terminate the
lower-dimensional pivot, prove recurrence termination, convert the
root-critical polarity into a contradiction, close `GG`, or prove
four-agent/general additive EFX.
