# Three-nonsingleton contraction target

**Date:** 2026-08-09

**Status:** proposed next general-EFX gate; no theorem is claimed here

## Target theorem

Let `X` be a globally lexicographically maximal noncomplete partial EFX
allocation for four positive, nondegenerate additive agents in the BCFF
one-charity normal form. Suppose exactly three allocated bundles are
nonsingletons.

Prove that the selected basic-cycle structure yields at least one of:

1. a complete EFX allocation;
2. a partial EFX allocation with strictly larger fixed-order lexicographic
   potential; or
3. a partial EFX allocation with the same lexicographic potential and at
   most two nonsingleton bundles.

The first outcome proves existence for the instance, the second contradicts
global maximality, and the third contradicts the proved exactly-two-
nonsingleton composition theorem after selecting, among lexicographic
maxima, a state with the fewest nonsingleton bundles.

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

Build the selected-cycle census for three genuine target bundles. For each
cycle class, record whether an existing length-two, length-three, adjacent,
or alternating lemma applies after contracting one ordinary edge. The first
research output should be either:

- a proof that every class contracts to the exactly-two theorem; or
- one minimal named residual topology, together with an exact countermodel
  refuting the most natural contraction and a sharply stated replacement
  lemma.

## Claim boundary

Closing this target would eliminate the exactly-three-nonsingleton branch.
It would still not resolve general four-agent additive EFX until the
all-four-nonsingleton branch and the nonnegative/tie limiting wrapper are
closed and the full argument receives independent expert review.
