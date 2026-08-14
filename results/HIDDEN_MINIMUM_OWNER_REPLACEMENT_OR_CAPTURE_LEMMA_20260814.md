# Hidden-minimum owner replacement-or-capture lemma

**Date:** 2026-08-14

**Status:** cap-free last-unsafe-core lemma; simultaneous unsafe-core
collisions and conversion of the captured owner packet remain open

## Setup

Let `X` be the base allocation and let `V` be a nonempty owner set.  Suppose
contracted cores

\[
                         (D_i)_{i\in V}            \tag{1}
\]

are nonempty, pairwise disjoint, desired by their indexed sources, common
safe in the contracted instance, and closed under base ownership in
`V union {charity}`.  Expand the cores to their physical goods.

Assume every expanded `D_j` with `j!=i` is already physically common safe,
while `D_i` is not.  Then some observer `a` and
physical good `g in D_i` satisfy

\[
                         v_a(D_i-g)>v_a(X_a).       \tag{2}
\]

This is exactly the hidden-minimum failure produced by response-role
compression.

## Globally minimal replacement

Among every pair `(b,F)` such that

\[
                 \varnothing\ne F\subseteq D_i-g,
                 \qquad v_b(F)>v_b(X_b),           \tag{3}
\]

choose one with minimum cardinality.  Such a pair exists by (2).  The
bundle `F` is physically common safe.  Otherwise some observer `c` strongly
envies `F`; deleting the witnessing good gives a desired bundle for `c` of
strictly smaller cardinality, contradicting the choice in (3).

If `b=i`, replace `D_i` by `F`.  The resulting family is still pairwise
disjoint and closed on `V`, so it is a physical generalized PI family.

## Owner replacement

Now suppose `b!=i`.  Put

\[
                         W=(V\setminus\{i\})\cup\{b\}.          \tag{4}
\]

Use `F` as the core of source `b`; discard both `D_i` and the old `D_b` when
`b in V`; and retain `D_j` for every

\[
                         j\in V\setminus\{i,b\}.                \tag{5}
\]

The displayed replacement cores are nonempty, physically common safe,
desired by distinct sources, and pairwise disjoint: `F subset D_i`, while
every retained core was disjoint from `D_i` in (1).

Every selected good originally had base owner in `V` or charity.  The only
old owner absent from `W` is `i`:

\[
       (V\cup\{\mathrm{charity}\})
       \setminus(W\cup\{\mathrm{charity}\})=\{i\}.             \tag{6}

Hence exactly one of the following occurs.

1. The replacement family contains no good base-owned by `i`.  It is closed
   on `W`, and therefore gives a physical generalized PI family.
2. Its union contains a good base-owned by `i`.  The failed physical lift
   has produced an exact **owner-`i` capture certificate** in a disjoint
   desired-core family after source `i` was deleted.

No value bound, packet-cardinality bound, or fixed atomization is used.

## Alternating interpretation

At a PI-free state with exactly one remaining unsafe expanded core, the
failure must take outcome 2.  Thus the final hidden-minimum repair replaces
source `i` by a globally minimal physical response source `b` while
retaining a packet of base-`i` support.  A sequential lift can use this as
its terminal step; if two or more cores remain unsafe, their replacement
sources must first be uncrossed or treated as a simultaneous-source
collision.

For four owners the owner labels alone cannot grow indefinitely.  What is
not yet proved is that repetition of a label supplies the exact physical
return and observer-surplus inequalities required by the retired-packet
collision theorem.  Equality of labels is not equality of packets or signed
states.

## Claim boundary

Proved: when all other cores have already lifted physically, the last
hidden-minimum obstruction either yields physical generalized PI or produces
a precise deleted-owner support capture in another disjoint physical
desired-core family.

Not proved: uncrossing two or more simultaneously unsafe cores, distinctness
of their replacement sources, that the captured packet is held by the
required collision recipient, that it is returned whole, that all
owner-payment and observer-surplus rows survive its transfer, or that the
active four-edge fixed-`U` theorem follows.
