# Fourth-owner margin-substitution selector lemma

**Date:** 2026-08-11

**Status:** cap-free exact selector for the fourth-owner operation forced by
the minimal-K/q-budget separator; compensated-donor and observer-safety
branches remain open

## Strict separator and fourth core

Use the blocked-hole separator with

\[
 \nu_d=v_d(K+H)-v_d(X_d)>0                         \tag{1}
\]

and

\[
 \theta_q=v_q(K)-\mu_q-v_q(W)>0.                  \tag{2}
\]

Thus returning a packet `J subseteq K` to protected `q` makes the remaining
hole transfer q-admissible exactly when

\[
 v_q(J)\ge\theta_q.                                \tag{3}
\]

Let the fourth represented owner `s` hold a disjoint common-safe desired
core `E`, with margin

\[
 \mu_s=v_s(E)-v_s(X_s)>0.                          \tag{4}
\]

A packet `L subseteq E` can be donated without compensation while keeping
`s` weakly paid exactly when

\[
 v_s(L)\le\mu_s.                                   \tag{5}
\]

## Two independent selectors

Choose

\[
 J^*\in\arg\min\{v_d(J):J\subseteq K,
                         v_q(J)\ge\theta_q\},       \tag{6}
\]

and

\[
 L^*\in\arg\max\{v_d(L):L\subseteq E,
                         v_s(L)\le\mu_s\}.          \tag{7}
\]

Both families are nonempty: `J=K` satisfies (3), because
`theta_q< v_q(K)`, and `L=empty` satisfies (5). Finite support gives both
optima.

## Exact dichotomy

Exactly one of the following holds.

1. **Fourth-owner substitution succeeds.** If
   \[
   \nu_d+v_d(L^*)-v_d(J^*)>0,                      \tag{8}
   \]
   send `K\setminus J^*` to `d`, keep `J^*` with `q`, and send `L^*` from
   `s` to `d`. Then
   \[
   v_d((K\setminus J^*)+H+L^*)>v_d(X_d),           \tag{9}
   \]
   while (3) makes `K\setminus J^*` q-admissible and (5) keeps `s` weakly
   paid. Apply the canonical residual split to pay `q`; the desired root
   core pays the root strictly. Hence all four owners are weakly paid and at
   least root and hole are strict before observer-safety checking. A
   surplus-budgeted leaf is an EFX lexicographic endpoint; a failed threshold
   gives the named response augmentation.
2. **Uncompensated fourth-owner separation.** If (8) fails, then for every
   q-sufficient `J subseteq K` and every s-affordable `L subseteq E`,
   \[
   v_d(J)-v_d(L)\ge\nu_d.                           \tag{10}
   \]
   Indeed (6) minimizes `d(J)` and (7) maximizes `d(L)`, so every other pair
   is weakly worse for the hole. Thus no uncompensated donation from `E` can
   replace enough of the q-expensive packet.

The failure (10) is an exact two-knapsack certificate. It identifies the
smallest remaining operation: compensate `s` from the residual/root surplus
so that the affordability bound (5) can be relaxed, or use the failed target
as a response augmentation. Repeating an uncompensated donor choice cannot
help.

## Verification and boundary

[`fourth_owner_margin_substitution_selector_audit.json`](fourth_owner_margin_substitution_selector_audit.json)
checks nonemptiness, the q-admissibility cancellation, all four payment
identities, and the global separation implication from the two extrema.

This lemma does not force (8), discharge observer-target surplus budgets,
construct the compensated-`s` continuation after (10), handle a response-
silent fourth owner, close GG, or prove four-agent/general additive EFX.
