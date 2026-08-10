# Cap-free alternating global-lex theorem

**Date:** 2026-08-09

**Status:** cap-free analytic theorem under the normalized positive
alternating premises

## Theorem

Let `X` be a partial EFX allocation of four agents with one unallocated good
`f` and alternating champion topology

\[
p\xrightarrow f r\longrightarrow s
\xrightarrow f q\longrightarrow p,
\]

where `X_p={x}`, `X_s={y}`, and `X_r,X_q` are arbitrary nonempty bundles.
For a fixed lexicographic priority order, suppose either a compatible
generalized champion family is present or all four compatible cross-bottom
families are absent. Then `X` is not globally lexicographically maximal
among partial EFX allocations.

No bound is imposed on the number of goods in any top or bottom packet.

## Adaptive-root/order formulation

For a fixed priority order, the proof gives the requested adaptive escape:

1. a compatible desired family gives its standard PI-cycle EFX
   improvement immediately;
2. otherwise, choose the root orientation from the priority order.  A root
   flip or half-turn reduces the applicable hard orbit to the reservoir
   orders `(p,s,r,q)` or `(s,p,q,r)`, preserving common safety, packet
   disjointness, the two champion decompositions, and the two ordinary-envy
   edges; or
3. the root-flip or dual-reservoir allocation itself is an explicit EFX
   lexicographic improvement, with the external observer checked inside the
   corresponding lemma.

No literal change of the fixed lexicographic priority is needed or used.
Such a change would not contradict maximality for the original order.  The
"priority change" is instead a proof-level choice of the root/half-turn
normal form determined by that original order.

## Proof by exhaustive analytic order cover

There are 24 priority orders.

1. The
   [`easy-priority escape lemma`](ALTERNATING_EASY_PRIORITY_ESCAPE_LEMMA.md)
   closes the 16 orders beginning with `r` or `q`, with `p,r`, or with
   `s,q`. Its allocations have only singleton bundles and are automatically
   EFX.
2. The [`root-flip lemma`](ALTERNATING_ROOT_FLIP_LEMMA.md) closes
   `(p,q,r,s)` and, by half-turn, `(s,r,q,p)`.
3. The
   [`reservoir-exchange lemma`](ALTERNATING_RESERVOIR_EXCHANGE_LEMMA.md)
   closes `(p,s,r,q)` and, by half-turn, `(s,p,q,r)`.
4. The
   [`dual-reservoir trichotomy`](ALTERNATING_DUAL_RESERVOIR_TRICHOTOMY.md)
   has three possible outputs for a `p`-rooted state. Two strictly improve
   `p`. The third fixes `p` and `s` and strictly improves `q`. Consequently
   the same trichotomy closes **both** `(p,s,q,r)` and `(p,q,s,r)`. Its
   half-turn either improves `s`, or fixes `s,p` and improves `r`, so it
   closes both `(s,p,r,q)` and `(s,r,p,q)`.

These sets are disjoint and contain all 24 orders. If a compatible family is
present, its standard PI cycle gives an EFX Pareto improvement and hence a
lexicographic improvement in every order. If all compatible families are
absent, items 1--4 apply. Thus no alternating state satisfying the stated
premises is globally lexicographically maximal. \(\square\)

## Consequence and boundary

This proves the priority-sensitive alternating escape lemma for arbitrary
packet sizes. It closes the alternating length-four residual topology in the
two-nonsingleton BCFF reduction.

It does **not** yet prove complete four-agent additive EFX. The length-three
and adjacent-large length-four residual topologies in the two-large reduction
still require cap-free closure. After those, the three- and four-nonsingleton
cases and the nonnegative/tie limit wrapper remain. The strict refinement
that every `p`-rooted escape must anchor `p` or promote it within its original
champion offer is also open, but is no longer needed for the alternating
global-lex theorem: opposite-reservoir promotion is itself a valid EFX
lexicographic escape.

## Verification boundary

The proof is analytic. The exact computations were used to discover and
adversarially test its component lemmas, not to extrapolate from a finite
cell. The 24-order coverage is regression-tested by
[`test_alternating_capfree_order_coverage.py`](../tracks/parkability/test_alternating_capfree_order_coverage.py).
The constructive dual-reservoir audit replays 18 frozen eleven-good profiles
and is byte-reproducible.  The six strict hard-order countermodels and the
augmented-`q`-face models refute the narrower fixed anchored candidate, not
this adaptive theorem: in each case one of the root-flip, reservoir, or
dual-reservoir rival forms survives.  The exact boundary is catalogued in
[`ALTERNATING_EXTERNAL_OBSERVER_RESOLUTION_20260809.md`](ALTERNATING_EXTERNAL_OBSERVER_RESOLUTION_20260809.md).
