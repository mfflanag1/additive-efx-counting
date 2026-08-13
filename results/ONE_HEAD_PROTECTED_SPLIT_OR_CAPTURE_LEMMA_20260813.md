# One-head protected split-or-capture lemma

**Date:** 2026-08-13

**Status:** cap-free exhaustion of every two-bundle repair of a one-head
protected Hall witness

## One-head paid candidate

Let `Z=(Z_i)_{i in N}` be the paid residual-completed cycle and suppose `h`
is its sole terminal blocker. Define

\[
 \lambda_i=
 \max\left\{v_i(X_i),\ \max_{j\in N}\tau_i(Z_j)\right\}.             \tag{1}
\]

Every non-head owns an accepted bundle:

\[
 v_i(Z_i)\ge\lambda_i\qquad(i\ne h).              \tag{2}

The head has at least one accepted nonidentity target. Let `a != h` be any
owner with

\[
 v_h(Z_a)\ge\lambda_h.                            \tag{3}

Choose an inclusion-minimal packet

\[
 P\subseteq Z_a,
 \qquad v_h(P)\ge\lambda_h.                       \tag{4}

Minimality gives

\[
 \tau_h(P)<\lambda_h                              \tag{5}

under nondegeneracy, with the weak inequality sufficient in general.

## Protected split

Swap the head into `P` and give the displaced owner the complete return

\[
 Z'_h=P,
 \qquad
 Z'_a=(Z_a\setminus P)+Z_h.                       \tag{6}

Every other owner keeps `Z_i`. The bundles remain pairwise disjoint and the
same total physical pool is used.

If

\[
 v_a(Z'_a)\ge\lambda_a,                           \tag{7}

then every owner meets her base floor and every comparison against an old
target. The new head target `P` is harmless: for every observer `i`,

\[
 \tau_i(P)\le\tau_i(Z_a)\le\lambda_i
 \le v_i(Z'_i),                                   \tag{8}

where the last inequality uses (4), (7), or the unchanged identity payment.
Thus the only target not already certified safe is the enlarged return
`Z'_a`.

If `Z'_a` is safe, (6) is EFX and weakly improves every owner over the base;
the head is strict because she blocked an old target, so
`lambda_h>v_h(Z_h)>v_h(X_h)`. Hence (6) contradicts global lexicographic
maximality. If `Z'_a` is unsafe, globally minimal extraction gives a fully
labeled response from the sole new target.

## Exact capture

If (7) fails, additivity gives

\[
 v_a(P)>
 v_a(Z_a)+v_a(Z_h)-\lambda_a.                    \tag{9}

Writing the protected slack as

\[
 \sigma_a=v_a(Z_a)-\lambda_a\ge0,
\]

equation (9) becomes

\[
 v_a(P)>v_a(Z_h)+\sigma_a.                       \tag{10}

Thus the packet needed by the head is worth more to the displaced owner than
the head's entire released bundle plus the displaced owner's complete
protected slack. No smaller head-paying packet can improve the return.

Globally maximize the displaced-owner return over every accepted target `a`
and every head-minimal packet (4). Exactly one of the following occurs:

1. a protected split (6) paid in both rows, followed by EFX or one new-target
   response; or
2. every accepted head packet satisfies the capture inequality (10).

The second branch is the exact one-head packet separator. The smallest move
outside this selector must recruit a third bundle, lower a later-priority
floor, replace the response, or use the root/anchor complete-residual pool.

The audit derives an exact positive one-head stress profile from the generic
supplier-saturation witness by paying its two ordinary old-incoming
self-response rows. The head then needs the whole decorated core and the
two-bundle return fails. More strongly, after retaining the permanent root
anchor and releasing every residual from the other owners, the decorated
source receives value `7/5` against direct EFX floor `7`. Thus the
complete-residual pool also fails in this local profile. The next operation
must split/release a selected core, alter the response source, or use a
priority-valid sacrifice. This is not asserted to be a globally recurrent
GG countermodel.

## Claim boundary

This lemma proves the complete two-bundle selector, old-target safety, unique
new wall, and exact capture inequality without an item or value cap. It does
not contradict simultaneous capture across every accepted target, force the
new response to be novel, solve the two-head topology, eliminate root
full-pool capture, close GG, or prove four-agent/general additive EFX.
