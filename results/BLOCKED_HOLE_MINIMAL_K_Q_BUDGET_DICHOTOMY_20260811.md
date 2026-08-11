# Blocked-hole minimal-K / q-budget dichotomy

**Date:** 2026-08-11

**Status:** cap-free payment-layer closure for a hole blocked on the protected
`q` core; observer-target safety and the strict two-row separator remain open

## Blocked-source state

Use the bottom-tail cycle state with root desired core `A`, protected `q`
core `Q`, retained tail `H`, and residual `W`. Suppose the distinguished
external hole `d` is blocked on `Q`: both `q` and `d` strictly desire the
same common-safe core,

\[
 \mu_q=v_q(Q)-v_q(X_q)>0,
 \qquad v_d(Q)>v_d(X_d).                            \tag{1}
\]

The full-priority matching assigns `Q` to `q` and leaves `d` unmatched
because `q` has earlier protected priority.

## Minimal hole-restoring packet

Positivity and (1) give `v_d(Q+H)>v_d(X_d)`. Choose an inclusion-minimal
packet

\[
 K\subseteq Q
 \quad\text{such that}\quad
 v_d(K+H)>v_d(X_d).                                \tag{2}
\]

It exists, and every `k in K` is payment-critical:

\[
 v_d((K-k)+H)\le v_d(X_d).                         \tag{3}
\]

## Exact dichotomy

Apply the q-budget canonical-split criterion to `K`.

1. **Admissible minimal packet.** If
   \[
   v_q(K)\le\mu_q+v_q(W),                          \tag{4}
   \]
   choose an inclusion-minimal `G_q subseteq W` satisfying
   `v_q(G_q)>=v_q(K)-mu_q`, and set `G_r=W\setminus G_q`. Then the cycle
   splice
   \[
   Y_r=A+G_r,\quad Y_q=Q-K+G_q,\quad Y_d=K+H       \tag{5}
   \]
   pays the root and `d` strictly and pays `q` weakly. Every other selected
   source is unchanged and remains above base. If the changed targets meet
   the observer-surplus inequalities, (5) is an EFX lexicographic endpoint;
   otherwise the failed threshold supplies a named response augmentation.
2. **Strict q-budget separator.** If (4) fails, then
   \[
   v_q(K)-v_q(W)>\mu_q,                            \tag{6}
   \]
   while (2)--(3) say that the same `K` is inclusion-minimal for restoring
   the blocked hole using `H`. Even giving every residual good to `q` cannot
   finance this packet. The obstruction is therefore the exact two-row
   separator
   \[
   \begin{cases}
   d(K+H)>d(X_d),\\
   d(K-k+H)\le d(X_d)&(k\in K),\\
   q(K)-q(W)>\mu_q.
   \end{cases}                                     \tag{7}
   \]

These alternatives are exhaustive and use no item cap.

## Consequence

A response-active hole blocked by protected `q` can no longer remain an
untyped Hall defect. It yields a fully paid three-owner cycle before safety
checking, or the minimal packet (7). The smallest next operation in the
second branch must recruit the fourth represented owner's surplus or replace
part of `K` through a response augmentation; further repartition of `W`
cannot help.

## Verification and boundary

[`blocked_hole_minimal_k_q_budget_dichotomy_audit.json`](blocked_hole_minimal_k_q_budget_dichotomy_audit.json)
checks existence from (1), criticality of an inclusion-minimal packet, all
three payment implications, and the exact separator (6) symbolically.

This lemma does not discharge observer-target surplus budgets, force a
fourth-owner compensator in branch (7), handle a hole with no response to
`Q`, close GG, or prove four-agent/general additive EFX.
