# Canonical root-response two-stage selector lemma

**Date:** 2026-08-11

**Status:** cap-free canonicalization of every common-safe root response at
one retained residual state; joint-packet and unsafe-response branches remain
open

## Root-response family

Fix the anchored residual state

\[
 D_r=T_q+f,
 \qquad W=B_q+L,
 \qquad \delta_q=v_q(W)-v_q(X_q)>0.
\]

Let `R(L)` be the finite family of all nonempty common-safe bundles

\[
 A\subseteq W
 \quad\text{such that}\quad
 v_r(A)>v_r(X_r).                                   \tag{1}
\]

If the root creates an evolved-target wall, global inclusion-minimization
of desired subsets produces a common-safe core.  Whenever its source is the
root, it belongs to this family even if its value lies below the temporary
anchor `D_r`.  For `A in R(L)`, write

\[
 K_A=A\cap B_q,
 \qquad J_A=A\cap L.
\]

## Stage one: maximize anchor-return payment

Choose

\[
 A_1\in\arg\min_{A\in R(L)}v_q(A).                 \tag{2}
\]

The anchor-return allocation gives `q` exact gain

\[
 \delta_q+v_q(D_r)-v_q(A).                          \tag{3}
\]

Therefore `A_1` maximizes `q`'s return gain over the entire root-response
family.  If

\[
 v_q(A_1)<v_q(D_r)+\delta_q,                        \tag{4}
\]

the anchor return pays both mutual owners and enters the EFX/one-wall
endpoint of the return-or-capture lemma.

If (4) fails, then for every `A in R(L)`,

\[
 v_q(A)\ge v_q(D_r)+\delta_q.                       \tag{5}
\]

Under nondegeneracy the comparison is strict.  Hence **every** common-safe
root response is in the capture branch; changing response cores cannot
restore anchor-return payment.

## Stage two: maximize floater substitution

Subject to the universal failure (5), choose

\[
 A_2\in\arg\max_{A\in R(L)}v_r(J_A+f).              \tag{6}
\]

If

\[
 v_r(J_{A_2}+f)\ge v_r(X_r),                        \tag{7}
\]

the floater-substitution lemma gives an EFX/lex endpoint or a single
evolved-target response augmentation.

If (7) fails, maximality gives, for every `A in R(L)`,

\[
 v_r(J_A+f)<v_r(X_r).                               \tag{8}
\]

In particular the selected `A_2=K+J` satisfies both universal capture (5)
and floater failure (8).  The two preceding lemmas then give

\[
 \begin{aligned}
 v_q(K)&>v_q(L\setminus J)+v_q(f),\\
 v_r(K)&>v_r(f)+v_r(A_2)-v_r(X_r),
 \end{aligned}                                      \tag{9}
\]

with `K` a nonempty subset of the original `B_q`.

## No fixed-state root-response cycling

At fixed `L`, the sequential selector is exhaustive:

1. some root response has a paying anchor return;
2. all anchor returns fail but some root response has a paying floater
   substitution; or
3. every common-safe root response fails both operations, and one canonical
   response exposes the joint packet (9).

Thus a response/Hall continuation cannot evade the packet certificate by
cycling among different common-safe root cores at the same retained state.
The choice is global over the finite response family and uses no item or
value cap.

## Verification and claim boundary

[`canonical_root_response_two_stage_selector_audit.json`](canonical_root_response_two_stage_selector_audit.json)
checks propagation of the stage-one minimum, propagation of the stage-two
maximum, and both selected capture inequalities under Z3 5.0.0.

This lemma canonicalizes the common-safe root-response family, including
root-sourced cores extracted from unsafe targets.  It does not classify the
non-root source cases of every unsafe target, terminate the joint packet
(9), prove that a subsequent response preserves `L`, close the remaining
Hall boundary, close `GG`, or prove four-agent/general additive EFX.
