# Fixed-U liquidated-root three-placement response frontier

**Date:** 2026-08-14

**Status:** cap-free direct-response frontier; singleton-hit descent,
p-augmented root capture, and exact decorated recurrence remain

## Three liquidation probes

Start from the frozen current allocation `(Y,{p})`, permanent anchor

\[
 A\subseteq Y_q,\qquad v_r(A)>v_r(X_r),
\]

and the nonempty original-root cell `Y_r` certified by
`FIXED_U_ROOT_RESIDUAL_NONEMPTY_LIQUIDATION_REDUCTION_LEMMA_20260814.md`.
Fix a nonroot residual holder `k`.  Move `A` to the root, move all of `Y_r`
to `k`, and place `p` in turn at each nonroot owner `h`.  Call the resulting
complete allocation `Z^{k,h}`.

Every probe has root bundle exactly `A`, so the root is strictly above its
base coordinate.  Relative to `Y`, its only possible nonself transfer pairs
are

\[
 q\to r:A,\qquad r\to k:Y_r,\qquad charity\to h:p.             \tag{1}
\]

Hence every probe uses at most three edges.

Assume all three probes for the fixed `k` are non-EFX.  Choose a response of
globally minimum cardinality over them.  If it contains `p`, it enters the
nonroot singleton-hit safe-envelope descent.  Suppose henceforth that its
core `E` is disjoint from `p`, with source `i` and target `t`.

The pairwise minimum-response argument applies to the three probes because
only the singleton holder changes.  Thus `E` is safe at all three probes and
is desired at every placement except possibly `h=i`.  Choose a placement
with `h!=i`.  At that allocation,

\[
                         v_i(E)>v_i(Z^{k,h}_i).                  \tag{2}
\]

## Direct transfer for a nonroot target

If `t` is nonroot and `t!=k`, transfer `E` to `i` and leave all other goods
where they are.  The target has only its original supplier cell, so together
with (1) the result uses at most four pairs.  The root stays at `A`, and the
source strictly improves by (2).

If `t=k`, its target may mix its original cell with `Y_r`.  Transfer to `i`
both `E` and **all** of `Y_r`, counting their union once.  The only possible
pairs are

\[
 q\to r:A,\qquad r\to i:Y_r,\qquad
 k\to i:E\cap(Y_k\setminus A),\qquad charity\to h:p.          \tag{3}
\]

The third pair is absent if that intersection is empty, and self-pairs are
deleted.  Thus (3) also uses at most four edges.  The source receives a
superset of `E` in addition to its retained original support and therefore
strictly improves.  This whole-cell completion removes the unique five-edge
mixed-target signature rather than treating it as an obstruction.

## Direct transfer for the pure anchor target

If `t=r`, then `E subseteq A`; the liquidated root target has only the
anchor-supplier cell.  Transfer `E` to its source, return all of `Y_r` to the
root, and give `p` to the root.  The final root bundle is

\[
                         A\setminus E+Y_r+p.                    \tag{4}
\]

The only possible nonself pairs are

\[
 q\to r:A\setminus E,\qquad q\to i:E,\qquad charity\to r:p.  \tag{5}
\]

so the allocation uses at most three edges.  If `i=k`, inequality (2) says
that `E` alone is worth more to `i` than its entire probe bundle containing
`Y_r`; hence returning `Y_r` still leaves `i` strictly improved.

Put

\[
 \delta_r=v_r(Y_r+A)-v_r(X_r)>0.
\]

The root in (4) remains strictly above base exactly when

\[
                         v_r(E)<\delta_r+v_r(p).                \tag{6}
\]

Failure is the exact p-augmented capture wall

\[
                         v_r(E)\ge\delta_r+v_r(p).              \tag{7}
\]

## Consequence

For each fixed residual holder, simultaneous failure of the three complete
liquidation probes yields exactly one of:

1. a nonroot singleton-hit envelope continuation;
2. a complete priority-valid allocation through at most four edges which,
   if EFX, proves the desired endpoint and, if non-EFX, supplies the next
   exact decorated response;
3. a root-target common-safe desired core satisfying (7).

There is no remaining packet-size, mixed-supplier, or fifth-edge branch.
Unlike the two-edge charity-relay collision argument, this frontier does not
use a controlled floor reset, retirement label, or imported collision
closure.

## Exact claim boundary

Proved: response transport across the three nonroot singleton placements,
the complete at-most-four-edge execution of every singleton-disjoint
nonroot-target response, and the exact root alternative (6)--(7).  Not
proved: termination of the changed-state singleton-hit chain within the
original probes, contradiction of (7), closure of a non-EFX transfer's
decorated recurrence, the saturated fixed-U theorem, or additive EFX.
