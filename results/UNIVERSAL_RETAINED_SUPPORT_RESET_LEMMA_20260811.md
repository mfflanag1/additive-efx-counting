# Universal retained-support reset lemma

**Date:** 2026-08-11

**Status:** cap-free monotonicity of every top-only q-core reset; fixed-support
rank recurrence and floater-consuming retained cores remain open

## Current retained support

Let

\[
 D(U)=(T_r\setminus U)+f,
 \qquad U\subseteq T_r,
\]

be the currently retained `q`-oriented mutual core, with positive response
margin

\[
 \mu(U)=v_q(D(U))-v_q(X_q)>0.                       \tag{1}
\]

Suppose a root-oriented Hall/recapture detour has selected a pairwise-
disjoint family of common-safe desired cores `A_1,...,A_m` that should be
retained when the proof returns to a `q`-oriented state.  Assume none of
these retained cores consumes `f`; an `f`-consuming core belongs to the
separate floater/root handoff.

## Canonical overlap update

Let

\[
 K=\left(\bigcup_{h=1}^m A_h\right)
   \cap(T_r\setminus U),                             \tag{2}
\]

and update

\[
 U'=U+K.                                             \tag{3}
\]

Then

\[
 D(U')=(T_r\setminus(U+K))+f                        \tag{4}
\]

is disjoint from every retained core.  No previously removed good is
restored: `U subseteq U'`.  Its exact response margin is

\[
 \mu(U')=\mu(U)-v_q(K).                             \tag{5}
\]

Exactly one of the following holds.

1. **Preserved reset.** `K` is empty.  Then `U'=U`, the old core `D(U)` is
   already disjoint from every retained core, and the reset preserves the
   outer support coordinate exactly.
2. **Fresh-support reset.** `K` is nonempty and `mu(U')>0`.  Then `D(U')`
   remains common-safe and desired by `q`, while
   \[
   U\subsetneq U',\qquad 0<\mu(U')<\mu(U).           \tag{6}
   \]
3. **Captured-margin handoff.** `mu(U')<=0`.  Then
   \[
   v_q(K)\ge\mu(U)>0,                               \tag{7}
   \]
   so the fresh overlap captures the entire remaining `q` response margin.
   Invoke the captured-q-margin anchored residual rotation with retained
   support `U'`; the proof does not restore the old mutual core.

Deletion preserves common safety, so no unsafe-core branch is introduced by
the reset itself.  The argument is independent of the number or sizes of
the retained cores.

## Global-potential consequence

Every top-only return from a root-anchored sacrificed-`q` Hall detour can be
normalized by (2)--(4).  Therefore no such reset decreases the retained
support coordinate.  A reset that physically conflicts with the old mutual
core either strictly enlarges `U` or enters the already named captured-
margin response boundary.

At fixed `U`, the reused-top canonical-core selector chooses one external
response maximizing the root residual across the entire common-safe family;
the maximum-matching, recapture, two-hole, and recurrence lemmas then govern
the inner coordinates.  Thus the only resets not covered by this theorem
are:

1. a retained core consuming the shared floater `f`; or
2. a fixed-support inner recurrence that neither changes the retained core
   nor consumes fresh top support.

These are now separate, explicit terminals rather than an arbitrary
rank-lowering reset.

## Claim boundary

This lemma proves monotone retained-top support for every reset whose
retained cores avoid `f`.  It does not eliminate floater-consuming cores,
terminate every fixed-`U` source-inactive/hitting-set recurrence, prove the
full lexicographic potential, close `GG`, or prove four-agent/general
additive EFX.
