# Two-by-two response-Hall normal form

**Date:** 2026-08-11

**Status:** exact cap-free classification; termination of the two surviving
star forms remains open

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

## Application to the two-hole state

After the two-hole selector, retain only targets participating in an actual
EFX wall.  The wall localization gives two opposite response blocks:

- represented core sources responding to the two residual targets; and
- the two holes responding to the two fixed core targets.

If both blocks have covering matchings, their disjoint union is the
release-compatible four-target SDR already proved by the two-hole lemma.
If not, a deficient block has one of the following named forms.

### Empty-target form

An actual wall target has no response source on the opposite side.  The
wall is therefore source-inactive relative to that side.  For a hole
strongly envying a core while remaining below base, this is exactly the
strict loss-band branch of the cross-star and core/residual repair lemmas.

### Common-singleton form

One opposite-side source `u` responds to both wall targets and the other
source is inactive for both.  The obstruction is a single-source,
two-target star.  Choosing either response edge leaves the other target as
the unique unmatched target of that block; there is no higher-rank Hall
defect.

Thus the two-hole conversion reduces every PI-free non-EFX survivor to a
source-inactive wall or a single-source two-target star, possibly together
with the root-critical polarity produced by the root-preserving selector.

## Why this is not yet closure

The graph theorem supplies no inequality reversing a source-inactive loss
band, and the common-singleton star may choose different desired subsets in
its two targets.  A valid termination proof must use one of the flower's
global facts—minimal payment, root criticality, lexicographic maximality, or
generalized PI-freeness—to turn the named inactive source into a connected
transfer or to make a revisited star close a response cycle.

## Claim boundary

This result completely classifies the residual 2-by-2 Hall combinatorics.
It does not eliminate either normal form, prove recurrence termination,
convert the root-critical polarity into a contradiction, close `GG`, or
prove four-agent/general additive EFX.
