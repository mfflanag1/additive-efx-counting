# Three-target hub Hall classification

**Date:** 2026-08-10

**Status:** exact finite combinatorial lemma; flower selector remains open

## Setting

Consider a charity-rooted hub split with hub `h` and two leaves `r,s`.  For
each changed target `j in {h,r,s}`, let `N(j)` be the set of *internal*
owners in `{h,r,s}` that can source a wall edge into `j`.  Self walls are
impossible, so `j notin N(j)`.  Sources outside this three-owner component
are deliberately omitted from `N(j)` and constitute open component-growth
edges.

If the three sets `N(j)` have a system of distinct representatives, the
selected source-to-target edges are a derangement of three vertices and
hence one directed three-cycle.  Because that cycle contains the hub edge,
the hub releases the union of the two disjoint leaf packets, while `{f}` is
unallocated.  The hub-split obstruction lemma therefore makes this a BCFF
PI cycle.  A PI-free state cannot have such a matching.

## Exact Hall alternatives

Hall's theorem leaves a nonempty target set `W` with

\[
\left|\bigcup_{j\in W}N(j)\right|<|W|.
\]

Choose `W` inclusion-minimal.  There are exactly three structural sizes.

1. `|W|=1`: one changed target has no internal blocker.  Every wall for
   that target is an open edge from the fourth owner.
2. `|W|=2`: the two targets have a single internal neighbor in total.  By
   self-wall exclusion, that neighbor is the third target.  Both deficient
   targets therefore point back to the same internal source, apart from any
   open fourth-owner walls.
3. `|W|=3`: every singleton and pair satisfies Hall, but the full target set
   has only two internal sources.  Up to the identity of the missing source,
   the graph is forced.  The two nonmissing sources form a directed
   two-cycle.  If either is the hub, this two-cycle contains the hub edge and
   is already PI.  Thus the unique PI-free full-set remainder is

   \[
   N(r)=\{s\},\qquad N(s)=\{r\},\qquad
   N(h)=\{r,s\},
   \tag{1}
   \]

   with `h` absent as an internal wall source.  The leaf two-cycle alone is
   not declared PI: it does not contain the hub edge that releases its
   incoming packets.

The exact 64-graph census and the three full-set patterns replay in
[`three_target_hub_hall_pattern_audit.json`](three_target_hub_hall_pattern_audit.json).

## Consequence for the selector

The hub-split selector no longer has an unstructured Hall remainder.  For a
two-leaf split, every PI-free failure must expose one of:

- a target with only the fourth owner available as blocker;
- two targets sharing the third target as their sole internal blocker; or
- the leaf-mutual pattern (1), in which the hub never blocks internally.

The first two cases identify a forced component-growth direction.  The third
is the only closed three-target trap and is now the highest-value analytic
case: varying the hub or repartitioning its packet must either make the hub a
wall source, reverse one leaf wall, or contradict the strict leaf overload
inequalities.

The last alternative cannot follow from the local star inequalities alone.
[`LEAF_MUTUAL_TRAP_SCALAR_GATE_REFUTATION_20260810.md`](LEAF_MUTUAL_TRAP_SCALAR_GATE_REFUTATION_20260810.md)
gives a positive cap-six additive model satisfying base EFX, charity
dominance, hub improvement, and all four strict walls.  Thus flower-specific
champion identities or an alternate hub/partition are essential.

## Claim boundary

This is a cap-free graph-theoretic classification once a two-leaf improving
hub split has been selected.  It neither proves that the flower supplies
such a split nor eliminates the leaf-mutual trap.  It therefore does not
close the three-packet flower or general additive EFX.
