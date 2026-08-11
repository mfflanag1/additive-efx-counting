# Packet-replacement charity-absorption lemma

**Date:** 2026-08-10

**Status:** cap-free analytic closure of the isolated charity-wall branch;
the simultaneous missing-`q` response boundary remains open

## Setting

Let `(X,{f})` be EFX with unenvied charity, let
`empty != R subseteq X_q`, put `C=X_q\R`, and suppose

\[
v_q(f)>v_q(R).
\]

The packet replacement proposes

\[
Y_q=C+f,
\qquad P_Y=R,
\]

with every other owner fixed.  The packet-for-charity obstruction lemma
shows that every failure is a target wall against `C+f`, a charity wall
against `R`, or both.

## Absorption theorem

Suppose owner `i != q` has a charity wall,

\[
v_i(R)>v_i(X_i). \tag{1}
\]

Then `R` is a common-safe desired bundle for `i`.  Consequently:

1. if `q` is a most-envious response source for `C+f`, the replacement edge
   into `q` and the absorption edge into `i` form a release-compatible PI
   edge set;
2. otherwise every most-envious source for `C+f` is external to `q`.  Adding
   the absorption target `R` either exposes an owner outside `{q,i}`, or the
   two-target relation is Hall deficient and its missing source is `q`.

Thus an isolated charity wall cannot survive in a PI-free state.  Every
surviving charity wall must coexist with a non-`q` target response and is
already part of the same finite response-Hall component.

## Proof

First, every subset of an allocated EFX bundle is common-safe at the base.
Indeed, for any observer `j`, any `g in R`, and `|R|>=2`,

\[
v_j(R-g)\le v_j(X_q-g)\le v_j(X_j).
\]

For a singleton `R` the EFX tail is zero.  Hence `R` is common-safe for all
observers.  Inequality (1) makes it desired by `i`, so `i` is a most-envious
source for the replacement target `R` at slot `i`.  Its full edge label is

\[
I_i=R,
\qquad O_i=X_i. \tag{2}
\]

The proposed target at slot `q` has label

\[
I_q=\{f\},
\qquad O_q=R. \tag{3}
\]

If `q` is one of its most-envious sources, select the two self-edges
`q -> q` and `i -> i`.  Their incoming sets `{f}` and `R` are disjoint;
`f` is initially unallocated and (3) releases all of `R`.  They are therefore
a BCFF PI edge set.

If `q` is not a response source for `C+f`, choose any actual most-envious
source `a != q`.  Notice also that `C` is nonempty: otherwise
`q(f)>q(X_q)`, contradicting base charity dominance.  Positivity therefore
gives `q(R)<q(X_q)`, so `q` cannot source the absorption target either.  If
some source `a` lies outside `{q,i}`, it is an explicit growth edge.  If all
sources of `C+f` are internal, they equal `i`; both targets then have only
the internal source `i`, so `{q,i}` is Hall deficient and its missing source
is exactly `q`. \(\square\)

## Interaction with the flower selector

The flower selector always supplies a good `g in X_q` with `q(f)>q(g)`, so
the theorem applies with `R={g}`.  A charity wall then says that some owner
values `g` above her entire old bundle; that owner can absorb `g` while
releasing her whole bundle into the adaptive component.  The operation is
not bounded by one-good exchanges after this first step: the released bundle
may be partitioned by the owner-rooted hub and complement-return lemmas.

The exact support and scalar implications replay in
[`packet_replacement_charity_absorption_audit.json`](packet_replacement_charity_absorption_audit.json).

## Claim boundary

This lemma removes a charity-only terminal branch and converts every
simultaneous charity/target failure into the same finite missing-`q`
response-Hall problem.  It does not eliminate that Hall defect, close `GG`,
or prove four-agent additive EFX.
