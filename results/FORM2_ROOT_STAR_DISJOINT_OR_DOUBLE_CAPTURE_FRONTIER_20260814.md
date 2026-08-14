# Form-2 root-star disjoint-or-double-capture frontier

**Date:** 2026-08-14

**Status:** cap-free exact root-star construction; the surviving shared packet
captures two response margins and the disjoint branch has only the root and
current-only `d` payment holes

## Shared root target

Let `B` be the reversed R3 support allocation with singleton charity `p`.
In form 2, sources `s` and `d` both have current-safe desired cores inside
the physical root target:

\[
 S\subseteq B_r,
 \qquad D\subseteq B_r.                            \tag{1}

\]

Write their actual source floors and strict margins as

\[
 \mu_s=v_s(S)-F_s>0,
 \qquad
 \mu_d=v_d(D)-F_d>0.                              \tag{2}

\]

The represented source `s` is already base-paid by its selected R3 core.
The unmatched owner's `d->r` response may be current-only; no base-payment
claim is made for it.

## Disjoint-or-double-capture

Put `K=D\cap S`.  If `D-K` is still desired by `d`, choose an
inclusion-minimal current-safe desired core `D_0 subseteq D-K`; then `D_0`
and `S` are disjoint.  If `S-K` is still desired by `s`, similarly choose
`S_0 subseteq S-K`; then `D` and `S_0` are disjoint.

If neither outside packet remains desired, additivity gives both

\[
 v_d(K)\ge\mu_d,
 \qquad
 v_s(K)\ge\mu_s.                                  \tag{3}

\]

Thus failure of both uncrossings produces one physical packet capturing the
complete strict response margins of two distinct sources.  Deletion preserves
common safety, so the disjoint replacement cores introduce no new core-safety
assumption.

## Root-star allocation and exact holes

There is a stronger payment-first construction that does not require
disjointness.  Since represented owners `q,s` are already base-paid, send the
entire current-only `d` response to `d`, leave `q,s` unchanged, and give the
singleton to the root:

\[
 \widehat Z_r=(B_r\setminus D)+p,
 \qquad \widehat Z_d=B_d+D,
 \qquad \widehat Z_q=B_q,
 \qquad \widehat Z_s=B_s.                         \tag{4}
\]

This uses only `r->d` and `charity->r`.  The overlap with `S` stays assigned
to `d`; source `s` does not need that second response core to remain above
base.  Hence shared-target overlap is not a conservation or owner-payment
obstruction.

Put `Delta_i=v_i(B_i)-v_i(X_i)` (written `\Delta_i` below).  The only payment
conditions for (4) are

\[
 \Delta_d+v_d(D)\ge0,
 \qquad
 \Delta_r+v_r(p)-v_r(D)\ge0.                     \tag{5}
\]

The current desire of `D` cannot silently be promoted to the first
inequality: the signed `d` residual must actually pay the difference.

The disjoint star remains useful as a second candidate and as an exact
response-structure classifier.

Let `D'` and `S'` be either disjoint original cores or one of the uncrossed
pairs above.  Form

\[
\begin{aligned}
 Z_r&=B_r\setminus(D'\mathbin{\dot\cup}S')+p,\\
 Z_d&=B_d+D',\\
 Z_s&=B_s+S',\\
 Z_q&=B_q.                                         \tag{6}
\end{aligned}

The operation uses only

\[
             \mathrm{charity}\to r,\qquad
             r\to d,\qquad r\to s,               \tag{7}

\]

so it is a complete at-most-three-edge allocation for arbitrary packet
sizes.  Owners `q` and `s` remain strictly base-paid.  Put

\[
 \Delta_i=v_i(B_i)-v_i(X_i).

\]

The two exact remaining payment conditions are

\[
 \Delta_d+v_d(D')\ge0,                            \tag{8}

\]

and

\[
 \Delta_r+v_r(p)-v_r(D'\cup S')\ge0.              \tag{9}

\]

There is no third payment hole.  In particular, current desire of `D'`
cannot silently be promoted to (6); the signed `d` residual must actually
pay the difference.

## Consequence

The first topology in the exact form-2 three-topology menu has one exhaustive
frontier:

1. the unconditional two-edge priority assignment (4), with only the
   explicit `r,d` payment inequalities (5);
2. a disjoint at-most-three-edge root star with the same two payment rows in
   (8)--(9); or
3. a shared packet `K` satisfying the two-margin capture (3).

If (5) or (8)--(9) hold for the corresponding candidate, any observer failure
is a paid-splice decorated response.
If either fails, its exact donor/root capture inequality must be combined
with the other two menu topologies.  If (3) holds, the next cap-free lemma
must return or split the common packet without losing both source margins or
the permanent root anchor.

## Claim boundary

Proved: the unconditional two-edge priority assignment, uncrossing
dichotomy, double-margin capture, conservation, edge bounds, and exact
payment identities.

Not proved: base payment of the current-only `d` response, simultaneous
reversal of (3), observer safety of the enlarged final bundles, exhaustion
by the complete three-topology menu, the fixed-U theorem, or general EFX.
