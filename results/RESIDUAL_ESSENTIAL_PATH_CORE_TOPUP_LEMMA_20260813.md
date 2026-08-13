# Residual-essential path-core top-up lemma

**Date:** 2026-08-13

**Status:** cap-free reduction of every mixed core/residual response to one
target-owner compensation inequality

## Mixed response

Use the path and paid deletion-return notation of the path-core rotation
lemma.  Let source `h_k` have an inclusion-minimal current-safe response

\[
 E\subseteq Z_l=A_l\mathbin{\dot\cup}R_l,
 \qquad v_k(E)>v_k(Z_k).                          \tag{1}
\]

Put

\[
 E_A=E\cap A_l,
 \qquad J=E\cap R_l.                             \tag{2}
\]

Replace the core-supported source bundle in the deterministic path rotation
by

\[
 W_k=A_l+J+R_k.                                   \tag{3}
\]

Because `E_A subseteq A_l`, positivity and (1) give

\[
 v_k(W_k)\ge v_k(E)+v_k(R_k)>v_k(Z_k).           \tag{4}
\]

Thus every mixed response, including a residual-essential one, has a
cap-free source-paying rotation.  No assumption `v_k(A_l)>v_k(Z_k)` is
needed.

## The only displaced floor

Remove `J` from the restored target owner:

\[
 W_l=(A_{l-1}+R_l)\setminus J=Y_l\setminus J.    \tag{5}

All other bundles and core locations are exactly those of the path-core
rotation.  Hence physical disjointness is preserved, the response source
strictly improves, and every changed owner except `h_l` receives either an
old protected target or an unchanged deletion-return bundle.

Let `b_l` be the complete protected floor of `h_l`.  Exactly one of the
following occurs.

1. **Paid top-up rotation:** `v_l(Y_l-J)>=b_l`.  The order classification of
   the path-core rotation lemma applies unchanged: three forward orders
   expose an internally supplied segment cycle, two adjacent backward orders
   reach rank four, and only `(l,k)=(1,3)` reaches the endpoint hole/core
   exchange.
2. **Residual-top-up separator:** `v_l(Y_l-J)<b_l`.  Since the old target
   paid `b_l`, cancellation gives the exact captured-surplus inequality

   \[
   v_l(J)>v_l(Y_l)-b_l.                            \tag{6}
   \]

   The residual packet needed to pay the response source consumes more than
   the restored target owner's entire protected surplus.

One may minimize `J subseteq R_l` subject to (4).  Then every `g in J` is
source-critical:

\[
 v_k(A_l+(J\setminus\{g\})+R_k)\le v_k(Z_k).     \tag{7}

The remaining operation is therefore exact: compensate `h_l` for the named
critical packet `J`, change the response/core, or use a priority-valid
reduction of `b_l`.

## Relationship to the old terminal

The former terminal distinguished “core-supported” and
“residual-essential” responses.  Equations (2)--(6) show that this is not a
fundamental split.  Every response enters the same path-core rotation; the
only extra separator is payment for its residual part.  When `J` is empty,
the theorem reduces to the path-core rotation lemma.

The endpoint order may therefore carry two coupled exchanges: compensation
for `J` at target `h_1`, followed by the hole/middle exchange involving
`P` and `A_2`.  A complete proof must optimize these jointly rather than
run either packet transfer greedily.

## Verification and claim boundary

The exact audit proves (4) and (6) over linear rational arithmetic and
replays all six path orders.  Both frozen referee witnesses have `J=empty`
and reach EFX under the core rotation.

This lemma does not compensate (6), jointly optimize the endpoint's two
packet exchanges, derive the required reverse inequality from the GG
root/q flower, produce a globally maximal GG countermodel, close GG, or
prove four-agent/general additive EFX.
