# Three-nonsingleton contraction target

**Date:** 2026-08-09

**Status:** active general-EFX gate; the eight selected-cycle classes are
now exhaustive and the length-two class is reduced to a three-packet flower

## Target theorem

Let `X` be a globally lexicographically maximal noncomplete partial EFX
allocation for four positive, nondegenerate additive agents in the BCFF
one-charity normal form. Suppose exactly three allocated bundles are
nonsingletons.

Prove that the selected basic-cycle structure yields at least one of:

1. a complete EFX allocation;
2. a partial EFX allocation with strictly larger fixed-order lexicographic
   potential, preferably one with at most two nonsingleton bundles.

The first outcome proves existence for the instance, the second contradicts
global maximality. There is no separate equal-potential contraction outcome:
nondegeneracy makes every agent's bundle utility injective, so equality of
the full ordered utility vector forces every assigned bundle to remain the
same and cannot reduce the number of nonsingletons.

## Why this is the highest-leverage next gate

The exactly-two branch is now closed. The exactly-three branch is the
smallest state class not covered by that theorem and retains one singleton
anchor, so it is structurally closer to the successful reservoir arguments
than the all-four-nonsingleton branch. Its key task is not another fixed
priority table: it is to manufacture a second singleton, or to identify the
precise obstruction preventing that contraction.

## Required proof program

1. Select one incoming basic champion or parallel envy edge per bundle and
   classify simple cycles by the number and placement of genuine champion
   edges, allowing all extra graph edges.
2. For every surviving class, attempt a cap-free `top/bottom` rotation that
   empties one large owner's residual bundle while preserving EFX.
3. Route every failed rotation through an explicit generalized PI cycle or a
   strict lexicographic improvement. Do not assume chordlessness, unique
   champion decompositions, bounded packet sizes, or a fixed item cap.
4. Use exact arithmetic or SMT only to enumerate symbolic inequality cells,
   falsify candidate lemmas, and extract small cores. The final theorem must
   be an arbitrary-packet analytic argument with replayable audits.
5. Audit every BCFF interface directly against the published definitions,
   especially generalized-edge release sets and the treatment of internal
   bottom edges.

## First bounded milestone

The first milestone is complete. The exact census has eight directed classes,
and none is a direct instance of an exactly-two-nonsingleton theorem. The
length-two `GG` class now reduces cap-free to a three-packet flower: the
external large owner has no incoming ordinary envy edge and therefore has a
nonself genuine incoming `f`-champion arm. See
[`THREE_NONSINGLETON_CYCLE_CENSUS_AND_FLOWER_REDUCTION_20260809.md`](THREE_NONSINGLETON_CYCLE_CENSUS_AND_FLOWER_REDUCTION_20260809.md).

The length-two flower is now further reduced by an exhaustive common-safe
cover theorem. All 864 source/priority cells have either a direct improving
cover or a cover with one unpaid mutual-cycle owner placed after a strict
improver. A four-cover strict-cycle lemma closes another 148 cells, leaving
284 cells in which simultaneous failure is consistent only in the relaxed
independent-total/tail abstraction. A true-tail atomic audit reduces this to
116 bounded cells but supplies an exact two-good exchange witness after all
one-good transfers are blocked. This rules out continuing by fixed radius.
The second alternative has now occurred. An exact full-`X_q` model blocks
every priority-directed one- and two-good exchange, including a source-safe
improving bottom swap, while its nearest improving EFX allocation is a
three-good connected owner/charity multigraph. Moreover, the external swap-blocker edge need
not have its incoming good released by the apparent flower cycle. See
[`FULL_CAPTURE_SWAP_PI_GATE_REFUTATION_20260810.md`](FULL_CAPTURE_SWAP_PI_GATE_REFUTATION_20260810.md).

The next research output must therefore be a cap-free component-growth
lemma: follow the unsupplied incoming good of each blocker through successive
owners until the component yields a lex-improving EFX allocation, a
release-compatible PI edge set, or an impossible strict item-order cycle.
The component must be a slot multigraph and may involve charity: blocking
all simple three-good owner paths still leaves an exact model whose nearest
partial escape is a three-edge `q--charity` packet replacement.

The variable-charity hybrid-wall theorem now removes the cardinality
restriction, and the packet-for-charity replacement lemma supplies the exact
opposite-sign obstruction rule for a component incident to charity. The
remaining construction premise is to select the first improving packet or
exchange component from the flower data; once a feasible endpoint is named,
the distinguished lex-component corollary grows to it in finitely many slot
components.

An exact strengthening now blocks every one-recipient packet-for-charity
replacement as well. Its nearest partial and complete escapes are three-edge
hub-splitting components: one owner receives one good (or `f`) while sending
two goods to two distinct recipients. The selector must therefore range over
packet partitions at a hub, not just subsets sent to charity.

The charity-rooted hub-split obstruction lemma now classifies every failure
of such a split cap-free. A failed hub target supplies an incoming subset of
`{f}` while releasing the whole hub packet; every failed leaf target supplies
an incoming subset of its disjoint packet cell. Directed wall cycles are
therefore release-compatible PI edge sets. The exact remaining selector gate
is to choose the hub and partition so that an open wall source or a strict
Hall-deficient target set cannot persist under component growth.

## Claim boundary

Closing this target would eliminate the exactly-three-nonsingleton branch.
It would still not resolve general four-agent additive EFX until the
all-four-nonsingleton branch and the nonnegative/tie limiting wrapper are
closed and the full argument receives independent expert review.
