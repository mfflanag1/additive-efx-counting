# Bottom-tail q-budget canonical-split lemma

**Date:** 2026-08-11

**Status:** cap-free elimination of the root-payment and residual-split
degrees of freedom in the bottom-tail cycle splice; selection of a hole-safe
`K` and final observer-surplus feasibility remain open

## Desired anchors and margins

In the bottom-tail cycle-splice state, let the root and protected `q` cores
satisfy

\[
 v_r(A)>v_r(X_r),
 \qquad
 \mu_q=v_q(Q)-v_q(X_q)>0.                          \tag{1}
\]

The root initially holds `A+H`, `q` holds `Q`, and the external hole holds
residual `W`. For a proposed packet `K subseteq Q` to be sent to the hole,
split

\[
 W=G_r\mathbin{\dot\cup}G_q                       \tag{2}
\]

and give `G_r` to the root and `G_q` to `q`.

## Root payment is automatic

For every split (2), positivity and (1) give

\[
 v_r(A+G_r)>v_r(X_r).                              \tag{3}
\]

The root-tail splice therefore has no root-replacement deficit. Its exact
realized surplus is

\[
 \Delta_r=\bigl(v_r(A)-v_r(X_r)\bigr)+v_r(G_r)>0.  \tag{4}
\]

This surplus remains available for observer-target threshold overshoots.

## Exact q-budget criterion

The protected owner is weakly paid exactly when

\[
 v_q(Q-K+G_q)\ge v_q(X_q),
\]

or equivalently

\[
 v_q(G_q)\ge v_q(K)-\mu_q.                         \tag{5}
\]

Since `G_q subseteq W`, some compensating split exists if and only if

\[
 v_q(K)\le\mu_q+v_q(W).                            \tag{6}
\]

Necessity follows by bounding `v_q(G_q)<=v_q(W)`. For sufficiency, take
`G_q=W`.

Whenever (6) holds, choose an inclusion-minimal `G_q subseteq W` satisfying
(5), with `G_q=empty` when `v_q(K)<=mu_q`, and set `G_r=W\setminus G_q`.
Then `q` is weakly paid, the root is strict, and every `g in G_q` is
payment-critical:

\[
 v_q(G_q-g)<v_q(K)-\mu_q.                          \tag{7}
\]

Among all inclusion-minimal compensators, a deterministic selector may
maximize the root surplus (4) and then the observer-surplus slack vector.
Thus the residual split is canonical once `K` is fixed.

## Exact failure

If (6) fails, then

\[
 v_q(K)-v_q(W)>\mu_q.                              \tag{8}
\]

Even transferring the entire residual to `q` cannot pay for `K`. In
particular `v_q(K)>mu_q`: `K` captures the whole protected response margin
after crediting every available residual good. This is a strict
hole-payment/`q`-budget separating certificate, not another arbitrary Hall
state.

Consequently the universal cycle-splice problem reduces to one packet
choice:

1. find `K subseteq Q` that makes `K+H` directly safe for the external hole
   and satisfies (6); then use its canonical split and check the remaining
   observer surplus budgets; or
2. prove that every hole-safe `K` satisfies (8), in which case a fourth-owner
   compensator or a response augmentation is genuinely necessary.

## Verification and boundary

[`bottom_tail_q_budget_canonical_split_audit.json`](bottom_tail_q_budget_canonical_split_audit.json)
checks the root-surplus identity, q-payment equivalence, necessity and
sufficiency of (6), criticality (7), and strict separation (8) symbolically.

This lemma does not prove that a hole-safe admissible `K` exists, discharge
the remaining observer-surplus inequalities, terminate the fourth-owner
separator, close GG, or prove four-agent/general additive EFX.
