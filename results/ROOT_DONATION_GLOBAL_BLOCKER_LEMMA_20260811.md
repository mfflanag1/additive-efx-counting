# Root-donation global-blocker lemma

**Date:** 2026-08-11

**Status:** cap-free global-maximality dependency lemma; termination of the
resulting backward repair path remains open

## One-edge candidate

Let `(X,P)` be an EFX-with-charity allocation with first-priority owner `r`.
Choose another owner `a` and a nonempty packet `K subseteq X_a`.  Define

\[
Y_r=X_r+K,
\qquad
Y_a=X_a\setminus K,                                  \tag{1}
\]

and leave every other owner and charity fixed.  Positivity makes `r`
strictly better, so `(Y,P)` lexicographically dominates `(X,P)` whenever it
is EFX.  Its transfer graph is the one-edge connected component `a -> r`.

## Exact blocker localization

If `(Y,P)` is not EFX with charity, every failed comparison has one of only
two forms:

1. the donor `a` fails against an owner target other than herself or against
   charity; or
2. an unchanged observer `i notin {r,a}` fails against the enlarged root
   target `X_r+K`.

The root cannot fail: her own value strictly increases while every target
other than her own is unchanged or shrinks.  An unchanged observer cannot
newly fail against an unchanged target or against the shrunken donor target,
because EFX thresholds are monotone under deleting goods.  The donor is
automatically safe against her own shrunken bundle.  These observations
exhaust all ordered comparisons.

Consequently, at a globally lexicographically maximal state, **every**
nonempty root donation has a named blocker of type 1 or 2.

## Exact blocker polarities

If an unchanged observer `i` blocks the enlarged root target, base EFX and
the new failure give

\[
 \tau_i(X_r+K)>v_i(X_i)\ge\tau_i(X_r).               \tag{2}
\]

Thus the packet causes a strict root-threshold increase in row `i`.

If the donor blocks on an unchanged owner target `X_j`, then

\[
 v_a(X_a)-v_a(K)<\tau_a(X_j)\le v_a(X_a),
\]

so the donation exhausts the donor's entire base slack:

\[
 v_a(K)>v_a(X_a)-\tau_a(X_j)\ge0.                   \tag{3}
\]

For an unchanged charity target the identical argument gives

\[
 v_a(K)>v_a(X_a)-v_a(P)\ge0.                        \tag{4}
\]

A donor wall against the enlarged root target remains explicitly coupled:

\[
 v_a(X_a)-v_a(K)<\tau_a(X_r+K).                     \tag{5}
\]

Equations (2)--(5) are strict dependency polarities, not generic EFX
failures.

## Backward-path interpretation

A type-1 blocker on `X_j` asks for compensation from owner `j`, extending a
candidate path backward as

\[
 j\longrightarrow a\longrightarrow r.
\]

A type-2 blocker says that observer `i` must either join the enlarged-root
component or force the packet `K` to be replaced.  If the extension produces
externally common-safe changed targets, pays every nonsource owner, and
leaves the final path source directly EFX, the externally-safe connected
path-transfer lemma gives the global maximality contradiction.

This is exactly what happens in the two hardened weighted-Hall profiles:
the first donation `c -> r` closes immediately, while the second requires
the length-two component `q -> r -> c`.

## Claim boundary

This lemma proves the exhaustive blocker set and its strict polarities for
every root donation.  It does not show that a terminal weighted-Hall packet
is currently owned by a later donor, choose the compensating packet from a
blocker target, terminate the backward path, close `GG`, or prove
four-agent/general additive EFX.
