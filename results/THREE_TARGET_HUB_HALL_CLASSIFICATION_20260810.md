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

Any directed internal cycle containing `h` is PI.  The hub edge releases the
union of the two disjoint leaf packets, while `{f}` is unallocated, so both a
hub--leaf two-cycle and an internal three-cycle meet BCFF Definition 3.4.
A PI-free state contains neither.

## Exact Hall alternatives

Hall's theorem leaves a nonempty target set `W` with

\[
\left|\bigcup_{j\in W}N(j)\right|<|W|.
\]

Choose `W` inclusion-minimal.  The 64 possible self-loop-free internal wall
graphs split exactly as follows.

1. Thirty-two graphs contain a directed cycle through `h` and are PI.
2. Twenty-nine PI-free graphs have some target `j` with `N(j)=emptyset`.
   Such a target is either already wall-free or can be blocked only from the
   fourth owner.  It is therefore a terminal or open boundary for component
   growth, not a closed internal obstruction.
3. Exactly three PI-free graphs have every `N(j)` nonempty.  They form the
   single leaf-mutual family

   \[
   N(r)=\{s\},\qquad N(s)=\{r\},\qquad
   \varnothing\ne N(h)\subseteq\{r,s\},
   \tag{1}
   \]

   with `h` absent as an internal wall source.  Two members have an
   inclusion-minimal Hall witness of size two and the third has one of size
   three.  The leaf two-cycle alone is not declared PI: it does not contain
   the hub edge that releases its incoming packets.

The exact counts are `32,29,2,1` for PI closure and minimum Hall-witness
sizes `1,2,3`, respectively.  The complete census replays in
[`three_target_hub_hall_pattern_audit.json`](three_target_hub_hall_pattern_audit.json).

## Consequence for the selector

The hub-split selector no longer has an unstructured Hall remainder.  Unless
the wall graph is already PI, it has a terminal/open target or belongs to
the three-member leaf-mutual family (1).  The latter is the only fully
internally blocked three-target trap and is now the highest-value analytic
case: varying the hub or repartitioning its packet must either create a hub
cycle, expose a terminal/open target, or contradict flower-specific
champion identities.

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
