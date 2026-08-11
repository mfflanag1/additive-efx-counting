# One-core/three-hole external-star normal form

**Date:** 2026-08-11

**Status:** cap-free rank-one normal form; elimination of the surviving
one-directional and source-inactive reciprocal stars remains open

## Rank-one state

Let `r` hold a common-safe desired core `A_r`, so

\[
 v_r(A_r)>v_r(X_r),
 \qquad
 \tau_i(A_r)\le v_i(X_i)\quad(i\in N).               \tag{1}
\]

Let `P` be every remaining good and let `H=N\setminus\{r\}` be the three
remaining owners.  By the three-agent additive EFX theorem, choose a
complete EFX allocation

\[
 P=\mathop{\dot\bigcup}_{h\in H}P_h                 \tag{2}
\]

among the holes `H`.  Give `A_r` to `r`.

## Exact wall localization

All hole-to-hole comparisons hold by (2).  The only possible EFX failures
are the six root-star comparisons

\[
 v_h(P_h)<\tau_h(A_r)                                \tag{3}
\]

or

\[
 v_r(A_r)<\tau_r(P_h)                                \tag{4}
\]

for `h in H`.  If none occurs, the complete allocation is EFX and is a
strict lexicographic flower improvement because the root is above base.

## Reciprocal-wall reduction

Suppose (3) and (4) both hold for the same hole `h`.

If `h` is a base-response source for `A_r`, response rigidity makes her
desired response the whole root core.  Equation (4) gives a proper subset
of `P_h` desired by `r`.  Choose an inclusion-minimal root-desired subset
`D_r subseteq P_h`.

1. If `D_r` is common-safe, the two disjoint incoming packets `A_r,D_r`
   are internally supplied by `r,h`.  The response edges form a
   release-compatible two-owner PI component.
2. If `D_r` is not common-safe, a failed base threshold against a deletion
   of `D_r` names an unsafe-core response augmentation.

If `h` is not a base-response source for `A_r`, (1), (3), positivity, and
nondegeneracy give the source-inactive loss band

\[
 v_h(P_h)<\tau_h(A_r)<v_h(A_r)<v_h(X_h).             \tag{5}
\]

Thus a reciprocal EFX wall is never an unclassified two-cycle: it is a PI
component, an unsafe-core augmentation, or the explicit loss band (5).

## Surviving signed stars

Each hole has four possible wall signs relative to the root:

1. no wall;
2. only the hole-to-root wall (3); or
3. only the root-to-hole wall (4); or
4. reciprocal walls (3)--(4).

There are `4^3=64` labeled signed stars.  Exactly `3^3=27` contain no
reciprocal pair, while 37 contain at least one.  In the latter group, every
reciprocal pair either closes/grows as above or is forced into the
source-inactive loss band (5).  This is the complete rank-one combinatorial
boundary.  The flower-specific selection problem is to choose the
three-agent EFX remainder so that all signs disappear, or use a surviving
one-way/loss-band sign to grow a release-compatible component.

## Connection to dimension descent

A source-inactive J-exhaustion at the two-core/two-hole boundary releases
one nonroot core and its active residual cell.  Keep the anchored root core
and include every released or previously residual good in `P`; the
three-agent theorem then supplies (2).  Hence rank-two exhaustion does not
return to an arbitrary allocation problem.  It reaches this exact external
star normal form.

For the `GG` flower, `A_r=T_q+f`.  Any surviving proof must now exploit the
mutual `f`-champion edge, the singleton owner, the external large owner, or
the captured-bottom/top-reset polarities to eliminate the surviving signs.  A
generic theorem for an arbitrary fixed core is neither assumed nor proved.

In fact the external-bottom-edge rank-two anchor rules out this rank-one
state in the `GG` flower itself: the known external desired core inside
`T_r+B_q` is disjoint from `T_q+f` and has source `c` or `s`.  The present
normal form remains the correct generic dimension-descent boundary, but the
flower proof resets to rank two before reaching it.

## Verification and claim boundary

[`one_core_three_hole_external_star_normal_form_audit.json`](one_core_three_hole_external_star_normal_form_audit.json)
checks wall localization, response rigidity, the source-inactive loss band,
two-owner release support, and all 64 signed stars, including the 27
nonreciprocal and 37 reciprocal-containing patterns, under Z3 5.0.0 and
4.15.3.

This lemma gives the exact cap-free rank-one normal form.  It does not prove
the flower-specific external-star selector, terminate unsafe-core
augmentation, close captured-bottom/top-reset recurrence, close `GG`, or
prove four-agent/general additive EFX.
