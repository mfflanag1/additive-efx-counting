# All-owner Hall response-compression lemma

**Date:** 2026-08-11

**Status:** cap-free analytic terminal reduction; the missing-source residual
payment/recapture branch remains open

## Minimal all-owner defect

Let `Y=(Y_i)_{i in N}` be a complete proposed allocation for four owners,
with every intended owner strictly preferring `Y_i` to her base bundle
`X_i`.  For each target `Y_j`, let `C_j` be its nonempty set of most-envious
response sources relative to `X`.

Suppose the full target set `N` is an inclusion-minimal Hall-deficient set:

\[
\left|\bigcup_{j\in N}C_j\right|<4,
\]

while every proper nonempty `U subsetneq N` satisfies

\[
\left|\bigcup_{j\in U}C_j\right|\ge |U|. \tag{1}
\]

Put `S=union_j C_j`.  Removing any one target and applying (1) gives
`|S|>=3`, whereas deficiency gives `|S|<=3`.  Hence

\[
|S|=3. \tag{2}
\]

Thus every minimal all-owner defect has deficiency exactly one.  Hall's
theorem on any three-target deletion that admits the restriction supplies a
matching from the three sources in `S` to three distinct original targets.
Equivalently, one target can be omitted so that all three response sources
take disjoint targets.

More strongly, **every prescribed response edge extends to such a
three-edge matching**.  Fix `i in C_j`.  Match the proper target set
`N\setminus{j}` to all three sources `S`, which is possible by (1).  In that
matching source `i` is assigned to some target `k`.  Delete `i -> k`, insert
`i -> j`, and leave `k` unmatched.  The other two matching edges remain
disjoint.  This anchored form is what lets response compression retain a
specific sink-capturing edge rather than forgetting the dependency that
created the terminal state.

## Response compression

Choose such a matching.  For each source `i in S`, let `mu(i)` be its
matched target and choose the corresponding common-safe desired response
core

\[
A_i\subseteq Y_{\mu(i)},
\qquad v_i(A_i)>v_i(X_i). \tag{3}
\]

The three packets `A_i` are pairwise disjoint because their parent targets
are distinct.  Let `d` be the unique owner outside `S`, and consolidate all
unselected goods into

\[
W=\left(\mathop{\dot\bigcup}_{j\in N}Y_j\right)
\setminus\left(\mathop{\dot\bigcup}_{i\in S}A_i\right). \tag{4}
\]

Define

\[
Z_i=A_i\quad(i\in S),
\qquad Z_d=W. \tag{5}
\]

This is a complete allocation.  Every source in `S` strictly improves by
(3).  The sole remaining payment condition is

\[
v_d(W)>v_d(X_d). \tag{6}
\]

If (6) holds, all four owners strictly improve.  If `Z` is EFX, it closes
immediately.  If its recomputed response relation has an SDR, the incoming
packets are disjoint and internally supplied because (5) is a complete
reallocation of all four base bundles and the charity good, so the SDR is a
generalized PI edge set.

If (6) fails, nondegeneracy gives the exact aggregate capture certificate

\[
\sum_{i\in S}v_d(A_i)
>
v_d(f)+\sum_{k\ne d}v_d(X_k), \tag{7}
\]

where the displayed form uses that the pre-compression targets partition
all base goods together with `f`.  If (6) holds but neither EFX nor an SDR
results, every response source is still internal and the new obstruction is
a **missing-source recapture** of `W` or one of the three source-owned cores;
there is no longer an arbitrary four-target Hall defect.

## Anchored sink-capture corollary

Suppose the all-owner component was reached through a sink target `Y_a` and
a response source `b` with desired core `B subseteq Y_a`.  Anchor the edge
`b -> a` in the matching above and set `A_b=B`.  The unique residual bundle
`W` then has the exact anchored form

\[
W=(Y_a\setminus B)+
\mathop{\dot\bigcup}_{j\ne a}(Y_j\setminus A_{\sigma(j)}), \tag{8}
\]

where `A_{sigma(j)}` is empty for the one unmatched target.  Thus compression
retains the unused part of the captured sink target and pools it with every
unused part of all three other targets.  It need not contain the simple
pairwise return `Y_b+(Y_a\setminus B)`, because a response core may be carved
from `Y_b`; payment is a genuinely global comparison.  Failure is exactly
the aggregate certificate (7), not merely the original pairwise
sink-capture inequality.

## Consequence for the flower bridge

Together with the top-core residual-reset lemma, all three previously named
terminal branches now enter one response-compression endpoint:

1. top-core reverse order resets to the two-root response-Hall component;
2. successful outside-source rotations grow that component to all owners;
3. an inclusion-minimal all-owner Hall defect compresses to three disjoint
   desired cores and one missing-source residual.

The remaining analytic task is therefore to pay the unique residual owner,
use (7) to change the root, or show that a recapture rotation strictly
advances a well-founded potential.

The four-owner Hall statement, extension of every response edge, and packet
partition replay in
[`all_owner_hall_response_compression_audit.json`](all_owner_hall_response_compression_audit.json).

## Claim boundary

This lemma proves deficiency one and the canonical response compression. It
does not prove (6), show that every recomputed response relation has an SDR,
eliminate missing-source recapture, prohibit a return to an earlier root,
close the `GG` flower, or prove four-agent additive EFX.
