# Flower dual-full-capture escape lemma

**Date:** 2026-08-10

**Status:** cap-free analytic theorem; the residual-top retention branch remains
open

## Setting

Work in the surviving full-capture `GG` flower.  Write

\[
X_r=T_r\mathbin{\dot\cup}B_r,
\qquad
X_q=T_q\mathbin{\dot\cup}B_q,
\]

where all four packets are nonempty.  The mutual desired bundles

\[
D_r=T_q+f,
\qquad
D_q=T_r+f
\]

are common-safe and are strictly desired by `r` and `q`, respectively.  The
external `(B_q|B_r)` edge into `r` has a common-safe desired bundle

\[
A_r=K\mathbin{\dot\cup}B_q,
\qquad K\subseteq T_r.
\]

Put `J=T_r\K`.  Full bottom capture is the premise `B_q subseteq A_r`;
**dual full capture** is the stronger condition `J=empty`, equivalently
`A_r=T_r+B_q`.

## Theorem

Under dual full capture there is an EFX-with-charity allocation `Y` with

\[
v_r(Y_r)\ge v_r(X_r),
\qquad
v_q(Y_q)>v_q(X_q).
\]

The conclusion is independent of packet cardinalities and does not require
the source-safe/strictly-separated item orientation.

## Proof

First consider the packet-for-charity replacement

\[
Y^{(1)}=(X_r,\ T_q+f,\ X_c,\ X_s;\ B_q).
\]

Every assigned bundle is common-safe.  The charity packet `B_q` is dominated
by every owner: for any observer `i`, choose any `t in T_q`; base EFX gives

\[
v_i(X_i)\ge v_i(X_q-\{t\})\ge v_i(B_q).
\]

Thus, if `v_q(f)>v_q(B_q)`, allocation `Y^(1)` is EFX with charity, fixes
`r`, and strictly improves `q`.

Suppose instead that

\[
v_q(f)\le v_q(B_q). \tag{1}
\]

Because `q` strictly desires `D_q=T_r+f`,

\[
v_q(T_r)+v_q(f)>v_q(T_q)+v_q(B_q).
\]

Together with (1), this implies

\[
v_q(T_r)>v_q(T_q). \tag{2}
\]

Now form the dual rotation

\[
Y^{(2)}=(T_q+f,\ T_r+B_q,\ X_c,\ X_s;\ B_r).
\]

Agent `r` strictly improves because she receives `D_r`.  Equation (2) says
that `q` strictly improves.  Under dual full capture the four assigned
bundles are exactly the common-safe bundles `D_r,A_r,X_c,X_s`.  The charity
packet `B_r` is dominated by every owner by the same containment argument,
using any good of nonempty `T_r`.  Hence `Y^(2)` is EFX with charity.  \(\square\)

## Retained-top payment extension

The same rotation closes a broader subcase even when `J` is nonempty.  If
`K` is nonempty and

\[
v_q(K)>v_q(T_q), \tag{3}
\]

use

\[
Y^{(3)}=(T_q+f,\ K+B_q,\ X_c,\ X_s;\ B_r+J).
\]

The assigned bundles are the common-safe bundles `D_r,A_r,X_c,X_s`.
Agent `r` improves, and (3) makes `q` improve.  For charity dominance, fix
any `k in K`.  Base EFX against `X_r` gives, for every observer `i`,

\[
v_i(X_i)\ge v_i(X_r-\{k\})\ge v_i(B_r+J).
\]

Hence `Y^(3)` is EFX with charity.  Consequently every surviving residual
state also satisfies

\[
v_q(K)\le v_q(T_q)<v_q(K+J).
\]

The omitted top packet is therefore not merely nonempty: it is necessary to
cross `q`'s payment threshold.

## Residual-top localization

Without dual full capture, write `A_r=K+B_q` and
`J=T_r\K != empty`.  The same payment dichotomy remains valid.  If the first
replacement fails to improve `q`, the second rotation still improves both
`r` and `q`; every EFX comparison is already certified except external
comparisons against

\[
T_r+B_q=A_r+J.
\]

Thus failure is localized to a strong-envy wall created by reinserting the
residual top packet `J` into the known common-safe bundle `A_r`.

This wall does give another generalized `(B_q|B_r)` championship into `r`,
but its desired subset may discard all of `J` and reproduce the original
edge.  Common safety of `A_r` does **not** force a most-envious subset of
`A_r+J` to retain a residual good.  Therefore the next cap-free step must
prove a residual-retention/recapture operation or use a potential that can
progress even when the newly selected desired bundle discards `J` again.

## Exact proof-mining provenance

An exact eight-good symbolic flower gate blocked every possible
EFX-with-charity allocation satisfying `v_r(Y_r)>=v_r(X_r)` and
`v_q(Y_q)>v_q(X_q)`.  The replayed master became UNSAT after 256 rival allocations.
Deletion minimization reduced the contradiction to exactly the two
allocations `Y^(1)` and `Y^(2)`, and the core remains UNSAT without any
nondegeneracy constraints.  See
[`minimal_flower_flexible_completion_audit.json`](minimal_flower_flexible_completion_audit.json).

The scalar payment implication replays independently as QF_LRA-UNSAT in
[`flower_dual_full_capture_escape_audit.json`](flower_dual_full_capture_escape_audit.json).

## Claim boundary

This closes the arbitrary-packet dual-full-capture subcase `J=empty` and the
broader retained-top-payment subcase (3).  It does not close the general
full-bottom-capture flower because the desired bottom edge may discard a
payment-critical part of `T_r`.  It does not close the other seven
three-nonsingleton cycle classes or four-agent additive EFX.
