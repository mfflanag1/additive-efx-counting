# Form-2 q-d swap/root-response payment frontier

**Date:** 2026-08-14

**Status:** cap-free exact payment analysis of the third menu topology;
observer continuation and combination of its two separators remain open

## Input cores

Let `B` be the reversed R3 support allocation with singleton charity `p`.
Use the ordinary base-desired unmatched-owner core

\[
 C_d\subseteq B_q,
 \qquad v_d(C_d)>v_d(X_d),                        \tag{1}

\]

and the represented source's root-target core

\[
 C_s\subseteq B_r.                                \tag{2}

\]

Owners `r,q,s` are base-paid in `B`; write

\[
 \Delta_i=v_i(B_i)-v_i(X_i)>0
 \qquad(i=r,q,s).                                 \tag{3}

\]

## Four-edge swap allocation

Move the whole root response to `s`, return `C_d` to `d`, and move the entire
old `d` bundle together with charity to `q`:

\[
\begin{aligned}
 Z_r&=B_r\setminus C_s,\\
 Z_s&=B_s+C_s,\\
 Z_d&=C_d,\\
 Z_q&=(B_q\setminus C_d)+B_d+p.                   \tag{4}
\end{aligned}
\]

This is a complete allocation using exactly the third menu topology

\[
             r\to s,qquad q\to d,qquad
             d\to q,qquad \mathrm{charity}\to q. \tag{5}

\]

Packet sizes are unrestricted.  Owner `d` is strictly paid by (1), and `s`
remains strictly paid because it retains `B_s` and gains a positive packet.
The two exact remaining conditions are

\[
                         v_r(C_s)\le\Delta_r,      \tag{6}

\]

and

\[
 v_q(B_d)+v_q(p)\ge v_q(C_d)-\Delta_q.            \tag{7}

\]

There is no packet-selection problem on the `d->q` edge: since `C_d` alone
strictly pays `d`, sending more of `B_d` to `q` can only help (7) and cannot
create a new owner-payment deficit at `d`.

## Exact failure separators

Failure of (6) is root-margin capture by the represented `s` response:

\[
                         v_r(C_s)>\Delta_r.        \tag{8}

\]

Failure of (7) says that the q-value of the lost ordinary `d` core exceeds
the entire available q-compensation pool:

\[
 v_q(C_d)-\Delta_q>v_q(B_d)+v_q(p).               \tag{9}

\]

Thus the third topology contributes no new graph or subset-sum terminal.  It
either gives an all-owner-paid four-edge candidate or exposes one of the two
aggregate separators (8)--(9).  Any observer failure of a paid candidate is
a full signed paid-splice response.

## Three-topology consequence

Together with
`FORM2_ROOT_STAR_DISJOINT_OR_DOUBLE_CAPTURE_FRONTIER_20260814.md` and
`FORM2_Q_COMPENSATION_PATH_PACKET_FRONTIER_20260814.md`, every topology in
the bounded form-2 menu now has a cap-free payment formula.  A universal
proof must show that simultaneous failure of:

1. the two-edge `{r,d}` root-star payment;
2. the bicriteria `q`-compensation root packet; and
3. inequalities (6)--(7)

forces generalized PI, a full-owner separator, or another saturated signed
exit.  That simultaneous implication is the exact remaining analytic menu
gate.

## Claim boundary

Proved: conservation, four-edge topology, automatic `d,s` payment, and the
exact root/q separators.

Not proved: observer safety, incompatibility of simultaneous menu failure,
exhaustiveness of the three-topology menu outside the bounded atomization,
the complete fixed-U theorem, or general EFX.
