# Permanent-anchor hitting recurrence: frozen contract

**Date:** 2026-08-13

**Status:** exact campaign statement and interface audit; resolved by the
minimal-response peel-or-reselect theorem

## State

Fix a positive, nondegenerate four-agent additive instance and a partial EFX
base allocation `X` that is globally maximal in a fixed priority beginning
with root `r`. A post-recruitment state consists of:

1. the complete current allocation and charity;
2. its full signed decoration relative to `X`;
3. a supplier-closed selected response component;
4. a permanent old root core `K_r`, with its original q-target provenance,
   currently assigned to `r`;
5. a disjoint recruited root response `E`, also assigned to `r`, which was
   current-safe at extraction and satisfies
   `v_r(E)>p:=v_r(Y_r^pre)>=v_r(X_r)`, where `p` pays every target left
   unchanged by the sacrifice handoff; and
6. every selected response/core/target/release label and the current matching
   and hole labels.

Thus the enlarged root target is

\[
 B=K_r\mathbin{\dot\cup}E.                       \tag{1}
\]

`Permanent anchor` here means the physical core and its signed provenance
are retained. It does **not** mean that `K_r` remains inside the current
q-owned bundle after it has been assigned to its response source.

## Exact recurrence

An exact recurrence repeats the entire finite record above, not merely the
root, hole, matching rank, or scalar utilities. Full signed-state
reconstruction then forces the same owner bundles, charity, physical target
supports, packet suppliers, response cores, and release labels.

Any changed record is finite augmentation only if it is permanently entered
in the monotone record ledger. Merely constructing a different candidate is
not by itself a strict transition.

## Mixed hitting response

If `B` is unsafe, choose an agent/subset pair of globally minimum cardinality
among all subsets desired over the agent's assigned bundle. Let its source be
`i` and its core be `D`. Then `D` is safe relative to the complete current
allocation and every good of `D` is critical in row `i`. The live mixed case
has

\[
 H=D\cap K_r\ne\varnothing,
 \qquad J=D\cap E\ne\varnothing.                 \tag{2}
\]

All support comparisons use current ownership and base provenance
separately. Self-returned goods are not counted twice as incoming release
packets.

## Permitted closing outcomes

The theorem is proved only if every exact recurrent state with (2) yields:

1. an explicit EFX allocation lexicographically above `X`;
2. pairwise-disjoint desired cores with internally supplied net incoming
   packets, forming a release-compatible PI cycle;
3. a declared finite coordinate that changes strictly and cannot later be
   reset without a different declared coordinate changing first;
4. a root core that is safe relative to the exact allocation at which it is
   selected, strictly desired by `r` over `X_r`, physically disjoint from
   retained targets after the exchange, and accompanied by a valid signed
   release record; or
5. entry into recapture/hole-pivot/two-hole machinery together with a proved
   well-founded termination argument, not merely a reference to an open
   boundary of that machinery.

The associated source-inactive loss band must satisfy the same standard.

## Counterexample standard

A disproof must give one exact positive-additive instance satisfying:

- base EFX and global fixed-priority lexicographic maximality against every
  partial EFX allocation;
- the complete GG flower and post-recruitment entry premises;
- permanent-anchor validity and signed supplier closure;
- a repeated complete state record;
- a mixed response (2); and
- failure of all five outcomes above.

A local scalar model, bounded null search, or candidate transition system
without global maximality does not refute the theorem.

## Current interface verdict

The prior archive supplies exact-state reconstruction, head-Hall reduction,
root-sourced sacrifice, response support localization, aligned recapture,
hole pivots, source-inactive repair, and two-hole Hall normalization. The
minimal-response peel-or-reselect theorem now supplies a permanent retired-
support ledger preventing restoration of a peeled root packet under the same
anchor label.

The contract is resolved by
[`PERMANENT_ANCHOR_MINIMAL_RESPONSE_PEEL_OR_RESELECT_THEOREM_20260813.md`](PERMANENT_ANCHOR_MINIMAL_RESPONSE_PEEL_OR_RESELECT_THEOREM_20260813.md):
a root-high safe response is reselected as the current anchor, while a
root-low response is paid out of the old anchor surplus and permanently
entered in the retired root-support ledger.
