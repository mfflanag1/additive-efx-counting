# R3 singleton-compensated anchor-uncrossing frontier

**Date:** 2026-08-14

**Status:** cap-free conversion of full root-margin capture to a four-edge
priority-valid move or one exact bicriteria critical-packet separator

## Captured-anchor input

Use either later-source residual R3 star from
`R3_LATER_SOURCE_ROOT_PRESERVING_STAR_FRONTIER_LEMMA_20260814.md`.  Let `x`
be its common source, let `E` be its current-safe inclusion-minimal desired
core in the protected root target, and let `A` be the permanent root anchor.
Write

\[
 K=E\cap A,
 \qquad R=A\setminus E,
 \qquad \rho=v_r(X_r)-v_r(R).                    \tag{1}
\]

The only live capture branch satisfies

\[
 v_r(R)\le v_r(X_r)<v_r(A)=v_r(R)+v_r(K),        \tag{2}
\]

so `rho>=0` and

\[
                         v_r(K)>\rho.             \tag{3}
\]

Let `F_x` be the actual source floor at the selected singleton probe and put

\[
 \mu_x=v_x(E)-F_x>0.                              \tag{4}
\]

The singleton charity good is `p`.

## Compensated uncrossing selector

For any packet `H subseteq K`, retain `H` at the root, move only `E-H` to
`x`, complete the incoming matching packet at the other star target exactly
as in the root-preserving absorption, and give `p` to `x`.

The root remains strictly above its base whenever

\[
                         v_r(H)>\rho.             \tag{5}
\]

The moved packet plus the singleton still strictly pays the response source
whenever

\[
                         v_x(H)<\mu_x+v_x(p),      \tag{6}

\]

because

\[
 v_x((E\setminus H)+p)-F_x
   =\mu_x+v_x(p)-v_x(H).                          \tag{7}

\]

Removing `H` cannot hurt the common safety of the selected response core:
for positive additive valuations, the EFX deletion threshold `tau_i` is
monotone under packet inclusion, and `E-H subseteq E`.  The enlarged final
bundle at `x`, which also receives `p` and the other star response, need not
itself be observer-safe; an EFX failure against it is retained as a decorated
response continuation.  The signed support operation is a restriction of
the already audited root-preserving star move; changing the charity recipient
to `x` still contributes exactly one charity edge.  Hence it uses at most
three owner-transfer pairs plus charity.

If the displayed complete allocation is EFX, the strict first-priority root
contradicts global maximality.  Otherwise it returns to the priority-valid
represented-star continuation, where same-source responses strictly shrink
the residual union and a different old represented source is the already
isolated gate.  Thus any `H` satisfying (5)--(6) removes **full anchor
capture** as an additional terminal; it does not by itself close the
different-source continuation.

## Exact critical-packet alternative

By (3), at least one root-feasible `H subseteq K` satisfies (5).  Choose an
inclusion-minimal such packet `H_*`.  Then

\[
 v_r(H_*)>\rho,
 \qquad
 v_r(H_*\setminus\{g\})\le\rho
       \quad(g\in H_*).                           \tag{8}

If the compensated selector fails for every root-feasible packet, it fails
in particular for `H_*`, and therefore

\[
                         v_x(H_*)\ge\mu_x+v_x(p). \tag{9}

\]

Equations (8)--(9) are the exact remaining separator.  It is not merely an
aggregate overlap inequality: `H_*` is a physical inclusion-minimal packet
that crosses the root deficit, while its value to the competing response
source covers both that source's whole response margin and the charity
singleton.

Minimality of `E` supplies a second useful atomwise inequality.  For every
`g in E`, the proper packet `E-g` is not desired, hence

\[
                         v_x(g)\ge\mu_x.          \tag{10}

\]

The scalar separator is feasible by itself.  For example, take one captured
good with root value `2`, retained-anchor value `1`, and base value `2`, so
`rho=1`; give that good source value `3`, source floor `2`, and singleton
value `1/2`.  Then the one-good response is inclusion-minimal, (2)--(4) and
(8)--(10) hold, and the compensated selector fails.  This is not a fixed-U
countermodel: it proves that the remaining contradiction must use the signed
support/saturation premises rather than only the two displayed valuation
rows.

## Consequence and claim boundary

Every full-root-margin capture in a later-source represented star has one of
two outcomes:

1. a singleton-compensated, priority-valid at-most-four-edge uncrossing that
   returns to the represented-star continuation; or
2. a physical critical packet satisfying (8)--(10).

Proved here: the selector margins, selected-core safety inheritance, edge
bound, existence/minimality of `H_*`, and the exact failure separator.

Not proved: observer safety of the enlarged final source bundle, closure of
the different-source continuation, contradiction of (8)--(10) from the
complete saturated fixed-U premises, a release-compatible PI component, the
complete fixed-U theorem, or general additive EFX.  The next universal step
must route `H_*` through its complete signed suppliers: either its
return/replacement recruits the unmatched owner, or an old represented
support cycle must pay the root and source simultaneously.
