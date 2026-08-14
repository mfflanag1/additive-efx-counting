# Rank-three two-hole global residual-split lemma

**Date:** 2026-08-13

**Status:** cap-free exhaustion of the sacrificed owner's direct two-hole
split; a selected-core capture return remains

## Rank-three compression

Let `S={r,q,s}` be the three represented sources in an anchor-constrained
rank-three response matching, and let `d` be the sacrifice-eligible missing
source. Assign pairwise-disjoint base-common-safe desired cores `A_i` to
their sources `i in S`, and collect every other physical good into the
residual pool

\[
 P=G\setminus\mathop{\dot\bigcup}_{i\in S}A_i.    \tag{1}
\]

Assume `P` has at least two goods, as it does in the two-target-hole branch.
Put

\[
 \theta_d=\max_{i\in S}\tau_d(A_i).               \tag{2}
\]

Because every selected core is common-safe,

\[
 \theta_d\le v_d(X_d).                            \tag{3}
\]

The priority-valid endpoint need not keep `d` above base: an earlier root is
already strict. It must, however, make `d` directly EFX-safe against every
selected core and against final charity.

## Globally optimal residual split

Choose a least-`d` good `g in P` and define

\[
 Z_d=P\setminus\{g\},\qquad Q'=\{g\}.             \tag{4}
\]

For every nonempty charity packet `C subseteq P`,

\[
 v_d(P\setminus C)\le v_d(P\setminus\{g\}).       \tag{5}
\]

Thus (4) maximizes `d`'s bundle over **every** partition of `P` between `d`
and nonempty charity, not only singleton guesses. Since `P` has another good
whose positive `d`-value is at least `v_d(g)`,

\[
 v_d(P\setminus\{g\})\ge v_d(g),                 \tag{6}
\]

so (4) is automatically charity-safe for `d`.

Consequently a directly safe split exists if and only if

\[
 v_d(P\setminus\{g\})\ge\theta_d.                \tag{7}

When (7) holds, every represented source remains strictly above base and
safe against every selected core. If no represented source envies `Z_d` or
`Q'`, the allocation is EFX and lexicographically improves the base. Any
such wall yields a current-minimal ordinary/decorated response and therefore
response augmentation, current progress, or an exact recurrent record.

## Exact failure separator

If (7) fails, then no allocation of the complete residual pool between `d`
and nonempty charity can make `d` directly safe. Choose a blocking core
`A_k` attaining (2). The unique terminal inequality is

\[
 v_d(P\setminus\{g\})<\tau_d(A_k)\le v_d(X_d).   \tag{8}

Write the base-provenance capture and outside residual as

\[
 C=X_d\cap\mathop{\dot\bigcup}_{i\in S}A_i,
 \qquad
 E=P\setminus X_d.                                \tag{9}
\]

Let `chi=v_d(g)` when `g in X_d\setminus C` and `chi=0` otherwise; let
`epsilon=v_d(g)` when `g in E` and `epsilon=0` otherwise. Then
`P=(X_d\setminus C) dotunion E`, and (8) implies the exact polarity

\[
 v_d(C)+\chi>
 v_d(E)-\epsilon+v_d(X_d)-\tau_d(A_k).           \tag{10}
\]

Thus the **effective removed own support** consists of goods of `X_d`
captured by selected cores together with the parked good when that good came
from `X_d`. Its value exceeds all usable outside compensation plus the
blocking-core safety slack. A proof must either return captured selected-core
support or replace an own good parked by the charity split.

Equation (10), together with the fact that the surviving blocker is the
permanent root core, is the exact next gate. A proof must return captured
support from one selected core, compensate its source, or turn the resulting
core chain into PI/connected charity extraction.

**Support-geometry update (2026-08-13):** returning all base-`d` goods from
their current represented suppliers to `d` and sending charity to `d` is
always complete within four support edges and strictly pays `d`; see
`CAPTURED_OWN_SUPPORT_FOUR_EDGE_STAR_LEMMA_20260813.md`. What remains is not
the physical return or edge count, but the donor deficits
`v_i(Y_i cap X_d)>Delta_i` and their connected compensation/response closure.

## Boundary

The accompanying audit proves global optimality over all nonempty charity
subsets, not a bounded packet menu. This lemma does not return the captured
packet, compensate its selected source, close the rank-three recurrence, or
prove four-agent/general additive EFX.
