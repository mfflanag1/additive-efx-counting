# Base-crossing reference-floor rigidity lemma

**Date:** 2026-08-14

**Status:** cap-free exclusion of the base-floor equality face and physical
localization of every other equality-paid recipient floor

## Input

Let `X` be the globally fixed base allocation, let `r` be the protected root,
and let `s != r` be the colliding recipient.  Assume the additive row `v_s`
is bundle-nondegenerate:

\[
 P\ne Q\quad\Longrightarrow\quad v_s(P)\ne v_s(Q).             \tag{1}
\]

The root currently holds a nonempty retired packet `K`, while the original
recipient candidate is

\[
 A=B\mathbin{\dot\cup}K,
 \qquad v_s(A)=F_s+\mu.                           \tag{2}
\]

For a split `K=T dot-union U`, with `T` transferred to `s`, let `R_s` be a
top-up packet disjoint from `K`.  The resulting recipient target is

\[
 Q_s=B\mathbin{\dot\cup}T\mathbin{\dot\cup}R_s.  \tag{3}
\]

## Reference-floor rigidity

Suppose a typed recipient floor is the value of a named physical reference
bundle `W_s`:

\[
 F_s=v_s(W_s).                                    \tag{4}
\]

If the recipient is paid exactly, then (1) forces physical identity:

\[
 v_s(Q_s)=F_s\quad\Longrightarrow\quad Q_s=W_s.  \tag{5}
\]

Consequently every genuinely transferred good belongs to the reference
support:

\[
 T\subseteq W_s.                                  \tag{6}
\]

This converts an equality-price statement into an exact support constraint;
it is not merely a scalar tie.

## Current-floor payment is strict

If `W_s=Y_s`, the recipient's bundle immediately before the operation, then
the root-held packet is disjoint from `Y_s`.  Hence any nonempty transferred
`T subseteq K` satisfies `T cap Y_s=empty`, contradicting (6).  Therefore

\[
 v_s(Q_s)\ge v_s(Y_s),\quad T\ne\varnothing
 \quad\Longrightarrow\quad
 v_s(Q_s)>v_s(Y_s).                               \tag{7}
\]

Thus a current-floor top-up crossing is automatically a strict recipient
improvement.  At an exact root base restoration, this strictness can replace
the root's lost surplus for fixed-priority routing whenever every owner
preceding `s` remains at her base floor; owners after `s` may then be treated
by the existing decorated-head sacrifice machinery.

## Base-floor equality capture is impossible at the surviving root cut

Now suppose the original collision is equality-critical at the recipient's
base floor:

\[
 \mu=0,
 \qquad F_s=v_s(X_s).                             \tag{8}
\]

Equations (1), (2), and (8) force

\[
 A=X_s,
 \qquad K\subseteq X_s.                          \tag{9}
\]

The nondegenerate root equality/base-restoration lemma and strict
full-packet underpayment force the surviving root packet to cross the base
root support:

\[
 \varnothing\ne U=K\cap X_r.                     \tag{10}
\]

But base bundles are disjoint, so (9) gives

\[
 K\cap X_r\subseteq X_s\cap X_r=\varnothing,     \tag{11}
\]

contradicting (10).  Therefore the protected-root base-crossing
equality-Hall terminal cannot simultaneously be an equality-critical
recipient collision at the base floor.

## Remaining typed faces

After this exclusion, a root base-restoration cut must lie in one of:

1. strict recipient capture;
2. an equality-critical recipient floor represented by a physical bundle
   other than `X_s`, with (6) recording the required support inclusion;
3. root-payment deficiency before equality restoration is available; or
4. an already routed EFX, PI, rank, collision-support, or anchor outcome.

For a current-floor reference, branch 2 is impossible for every nonempty
root-to-recipient transfer by (7).  The only equality floors still requiring
separate treatment are lower/base-debt or target-threshold references whose
physical support actually contains `T`.

## Claim boundary

This lemma proves the exact physical consequences (5)--(11).  It does not
force a compatible root-return packet, resolve overlap between a strict
recipient top-up and the unique root restoration packet, justify sacrificing
an owner preceding `s`, eliminate root-payment deficiency, close
`T_{L,times}^*`, or prove four-agent/general EFX.
