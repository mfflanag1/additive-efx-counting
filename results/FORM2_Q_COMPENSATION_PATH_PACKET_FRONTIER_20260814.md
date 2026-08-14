# Form-2 q-compensation path-packet frontier

**Date:** 2026-08-14

**Status:** cap-free reduction of the second menu topology to one exact
bicriteria root packet; observer continuation and elimination of the
critical packet remain open

## Ordinary d-core return

Let `B` be the reversed R3 support allocation with singleton charity `p`.
The unmatched source has an ordinary base-desired common-safe core

\[
                         C_d\subseteq B_q,
 \qquad v_d(C_d)>v_d(X_d).                        \tag{1}

\]

Unlike the current-only `d->r` wall, this `d->q` core unconditionally pays
`d` when returned.  Owners `r,q,s` are represented in the selected R3
matching, so their current margins

\[
 \Delta_i=v_i(B_i)-v_i(X_i)
\]

are positive.

## Three-edge compensation path

For any physical packet `P subseteq B_r`, form

\[
\begin{aligned}
 Z_r&=(B_r\setminus P)+p,\\
 Z_q&=(B_q\setminus C_d)+P,\\
 Z_d&=B_d+C_d,\\
 Z_s&=B_s.                                         \tag{2}
\end{aligned}
\]

This is a complete allocation using only

\[
             \mathrm{charity}\to r\to q\to d.    \tag{3}

\]

Owners `d,s` are strictly base-paid.  The remaining exact conditions are

\[
 v_q(P)\ge \alpha_q,
 \qquad
 \alpha_q=v_q(C_d)-\Delta_q,                      \tag{4}

\]

and

\[
 v_r(P)\le \beta_r,
 \qquad
 \beta_r=\Delta_r+v_r(p).                         \tag{5}

\]

Thus every `P` satisfying (4)--(5) is an all-owner-paid at-most-three-edge
candidate.  Its final bundles need not be observer-safe; any EFX failure is
a paid-splice decorated response.

If `alpha_q<=0`, the empty packet already satisfies (4) and the path reduces
to `charity->r` and `q->d`; the root condition is then automatic because
`beta_r>0`.  Hence the critical-packet branch has `alpha_q>0` and a nonempty
`P_*`.

The omitted `r->d` edge in the bounded menu's second topology is not needed
for payment.  It can be added only when a later observer/response repair
requires it, still staying within four edges.

## Exact critical-packet separator

The q-feasible family in (4) is nonempty whenever a root-target response
packet pays `q` after the loss of `C_d`; this is the precise current-floor
status that must be checked in the signed record.  Choose an
inclusion-minimal q-feasible packet `P_*`.  Then

\[
 v_q(P_*)\ge\alpha_q,
 \qquad
 v_q(P_*-g)<\alpha_q\quad(g\in P_*).              \tag{6}

\]

If no all-owner-paid path packet exists, every q-feasible packet violates
(5), and in particular

\[
                         v_r(P_*)>\beta_r.         \tag{7}

\]

Equations (6)--(7) are an exact bicriteria separator: `P_*` is
inclusion-minimal for compensating `q`, while its root value exceeds the
entire available root margin including charity.  Packet cardinality is
unrestricted.

## Relation to captured-anchor uncrossing

When `P_*` is a later-source response inside the root target, (7) is exactly
the root-capture side of
`R3_SINGLETON_COMPENSATED_ANCHOR_UNCROSSING_FRONTIER_20260814.md`.  The
present formulation identifies what that packet must pay on the other side:
the loss of the ordinary `d` core from `q`.  The universal form-2 gate is
therefore a two-row path-packet theorem, not an arbitrary four-edge graph.

## Claim boundary

Proved: conservation, the three-edge path, automatic `d,s` payment, exact
`r,q` thresholds, and the minimal-packet separator.

Not proved: that a q-feasible root packet always exists at the required
post-return floor, observer safety of (2), contradiction of (6)--(7) from
full saturation, exhaustion by the other two menu topologies, the fixed-U
theorem, or general EFX.
