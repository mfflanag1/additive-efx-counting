# Root-facing exhaustion handoff lemma

**Date:** 2026-08-11

**Status:** cap-free root/top factorization; the f-only captured-bottom
handoff remains open

## Setting

Use a root-facing J-exhaustion from the source-inactive core/residual repair
lemma.  The exhausted core is the anchored root bundle

\[
A_r=D_r=T_q+f,
\]

the current residual is `W`, and the critical returned packet is a nonempty
set

\[
H\subseteq T_q+f.
\]

Writing

\[
\sigma_r=v_r(T_q+f)-v_r(X_r)>0,
\]

J-exhaustion gives

\[
v_r(H)-v_r(W)\ge\sigma_r.                            \tag{1}
\]

Put `K=H intersect T_q`.

## Top-containing branch

If `K` is nonempty, use `K` as the packet in the top-core root-exchange
lemma.  The other mutual flower edge gives

\[
v_q(T_r+f)>v_q(X_q)>v_q(K),                          \tag{2}
\]

where the second inequality follows from `K subseteq T_q` and nonempty
`B_q`.  Hence there is a deletion-minimal `P' subseteq T_r` with

\[
v_q(P'+f)>v_q(K).
\]

The root exchange either pays `r` and supplies the required two-owner
component, or has the critical reverse order `v_r(P')>v_r(K)`.  The
top-core residual-reset lemma factors that reverse order back into the
minimal-payment two-root response-Hall component.

Thus every root-facing exhaustion containing a top good is already routed
through proved cap-free operations.  It may revisit the response boundary,
but it is not a new terminal geometry.

## The f-only branch

If `K` is empty, nonemptiness of `H subseteq T_q+f` forces

\[
H=\{f\}.
\]

Substituting in (1) and expanding `sigma_r` gives

\[
v_r(X_r)\ge v_r(T_q)+v_r(W).                         \tag{3}

Since `T_q+f` is strictly desired by `r`, (3) forces

\[
v_r(f)>v_r(W).                                       \tag{4}

The live early-root polarity gives `v_r(B_r)>=v_r(f)`, and therefore

\[
v_r(B_r)>v_r(W).                                     \tag{5}

In particular `B_r` cannot be contained in `W`.  At least one root-bottom
good lies in a selected nonroot core:

\[
C=B_r\setminus W\ne\varnothing.                     \tag{6}

This is the exact next dependency.  The obstruction is no longer an
unnamed root wall: the root needs the charity good more than the entire
residual, while a nonroot desired core captures a nonempty part of the
root's bottom packet that is worth still more to `r`.

## Composition consequence

Root-facing J-exhaustion now has only two outcomes:

1. `H` contains a top good and enters the top-core exchange/reset; or
2. `H={f}` and exposes the captured-bottom handoff (4)--(6).

The remaining operation must return enough of `C` to the root while
compensating the nonroot core source from `W` or another released core.  A
successful compensation strictly raises the root/residual potential; a
failure must follow the captured bottom goods to their next owner, and a
revisit must be converted into a release-compatible PI cycle.

## Verification and claim boundary

[`root_facing_exhaustion_handoff_audit.json`](root_facing_exhaustion_handoff_audit.json)
checks the top-packet payment premise, the f-only cancellation, both strict
value consequences, and the captured-bottom support implication under Z3
5.0.0 and 4.15.3.

This lemma eliminates root-facing exhaustion as an arbitrary packet case.
It does not close a top-core revisit, perform the captured-bottom
compensation, eliminate the two-hole 2-by-2 Hall boundary, close `GG`, or
prove four-agent additive EFX.
