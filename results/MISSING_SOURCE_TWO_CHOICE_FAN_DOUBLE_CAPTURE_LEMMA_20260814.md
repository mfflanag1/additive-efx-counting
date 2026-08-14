# Missing-source two-choice fan double-capture lemma

**Date:** 2026-08-14

**Status:** cap-free exact capture consequence of the corrected `3+1`
reservoir-fan defect; physical reversal remains open

## Rank-three fan

Let four pairwise-disjoint common-safe desired fan cores have exactly three
distinct sources.  Let `m` be the missing source and `a` the duplicated
source.  Denote the two cores desired by `a` by `D_1,D_2`, and the cores for
the other two represented sources by `U,V`.

Let `C` be any common-safe desired core for missing source `m`, with floor
`F_m` and strict response margin

\[
                         \mu=v_m(C)-F_m>0.        \tag{1}
\]

The two possible one-core-per-represented-source fan unions are

\[
                         G_j=U\cup V\cup D_j
                         \qquad(j=1,2).           \tag{2}
\]

## PI-free capture for both choices

If `C\setminus G_j` remained desired by `m`, choose an inclusion-minimal
desired subcore there.  Together with `U,V,D_j`, this gives four pairwise-
disjoint common-safe desired cores with four distinct sources.  The
surjective case of the corrected reservoir-fan lemma therefore gives
generalized PI.

Consequently, in a generalized-PI-free state,

\[
 v_m(C\setminus G_j)\le F_m,
 \qquad
 v_m(C\cap G_j)\ge\mu
 \qquad(j=1,2).                                  \tag{3}
\]

Put

\[
 H=C\cap(U\cup V),\qquad P_j=C\cap D_j.          \tag{4}
\]

The packets `H,P_1,P_2` are pairwise disjoint, and (3) becomes

\[
                         v_m(H)+v_m(P_j)\ge\mu
                         \qquad(j=1,2).           \tag{5}
\]

Thus exactly one of the following holds:

1. `v_m(H)>=mu`: the singly represented fan union already captures the
   missing source's complete strict response margin; or
2. with `eta=mu-v_m(H)>0`, both disjoint duplicate-source intersections
   satisfy

\[
                         v_m(P_1),v_m(P_2)\ge\eta.               \tag{6}
\]

This is a genuine double-capture certificate: the same positive residual
missing-source margin is covered independently inside two disjoint cores
desired by one duplicated represented source.

## Exact topology split

Among the 48 nonself four-target source maps with image size three, the
missing owner is one of the duplicated source's two target suppliers in 24
maps and is not in the other 24.  In the first class one packet `P_j` can be
retained by the missing owner without creating a transfer edge.  In the
second class both duplicate-source capture packets have foreign current
suppliers, so a reversal must cancel another owner edge or use a different
fan core.

## Claim boundary

Proved: both PI-free capture inequalities, the common-overlap/double-capture
dichotomy, disjointness of the two residual capture packets, and the exact
24/24 topology split.  Not proved: that either capture pays the missing
owner in the final allocation, edge-feasible reversal in the foreign-
supplier class, observer safety, the fixed-U theorem, or additive EFX.
