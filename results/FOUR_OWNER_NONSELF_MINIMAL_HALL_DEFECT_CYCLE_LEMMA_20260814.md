# Four-owner nonself minimal Hall-defect cycle lemma

**Date:** 2026-08-14

**Status:** exact cap-free graph classification for universally safe current
responses; two external-source defect shapes remain

## Response relation

Let `P` be a set of at most four owner targets.  For each target `t in P`,
let `N(t)` be the owners sourcing a current-desired response core inside that
target.  Positivity excludes current self-responses:

\[
                         t\notin N(t).            \tag{1}
\]

Let `J subseteq P` be an inclusion-minimal Hall-deficient target set, and
assume every target in `J` has a response source.  Then

\[
 |N(J)|=|J|-1.                                    \tag{2}
\]

The nonempty-neighborhood hypothesis excludes singleton defects, so
`2 <= |J| <= 4`.

## Classification

Exactly one of the following holds.

1. **External source.** `N(J)` is not contained in `J`.  A response source
   lies outside the deficient target-owner set.
2. **Internal directed cycle.** `N(J) subseteq J`.  Since (2) leaves a unique
   owner `u in J-N(J)`, minimality of `J` gives a perfect matching from
   `J-{u}=N(J)` to `N(J)`.  Equation (1) makes this matching a derangement.
   A derangement on one owner is impossible, on two owners is the directed
   2-cycle, and on three owners is a directed 3-cycle.

Consequently an internal minimal defect can only have `|J|=3` or `4`, and
contains respectively a 2- or 3-owner response cycle.  A size-two defect is
necessarily the one-external-source/two-target star.

## Application to the singleton relay

Use the universally safe minimum response cores produced by
`FOUR_PLACEMENT_SINGLETON_RESPONSE_TRANSPORT_LEMMA_20260814.md`.  For an
internal cycle of length two or three, park `p` at an owner outside the cycle.
Every cycle core is then current-desired, all are common-safe at that same
probe, their physical target bundles are distinct, and their suppliers and
recipients lie in the cycle.  The simultaneous cycle reversal is therefore
the release-compatible generalized-PI outcome excluded by saturation.

Thus every Hall-deficient survivor of the universally safe relay relation
must expose an external source relative to its deficient target set.  With
four owners the only irreducible shapes are:

\[
 |J|=2,\ |N(J)|=1,
 \qquad\text{or}\qquad
 |J|=3,\ |N(J)|=2,                                \tag{3}
\]

with at least one source outside `J`.  These are the exact remaining
source-parking compression targets; no closed rank-three or arbitrary Hall
graph remains.

## Boundary

This theorem classifies the incidence graph and closes its internally
supplied cycles under the active PI-free saturation premise.  It does not
prove that an external source enlarges the complete signed component rather
than already belonging to it, pay the omitted targets in (3), prove supplier
compatibility of a residual repair, finish fixed-`U`, or prove
four-agent/general additive EFX.
