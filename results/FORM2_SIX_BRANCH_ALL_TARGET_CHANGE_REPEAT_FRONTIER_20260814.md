# Form-2 six-branch all-target-change repeat frontier

**Date:** 2026-08-14

**Status:** cap-free elimination of unchanged-current-support response
recurrence; exact old cross-state base-margin terminal remains open

## Every current target changes

Each of the six canonical form-2 branches has four nonempty physical packet
edges forming a spanning tree on charity and the four owners.  Let `Y` be the
current support allocation and `Z` one such branch allocation.

Every owner vertex is incident to the tree.  If owner `i` only receives, then
`Z_i` contains a positive packet disjoint from `Y_i`; if `i` only sends, a
nonempty subset of `Y_i` is absent from `Z_i`; and if `i` both sends and
receives, the incoming packet was held by another vertex and is disjoint from
`Y_i`, while the outgoing packet is a nonempty subset of `Y_i`.  Therefore

\[
                         Z_i\ne Y_i
                         \qquad(i=r,q,s,d).        \tag{1}
\]

Charity sends its nonempty singleton and receives nothing in these complete
branches, so its support changes as well.

The argument is purely physical and remains valid for arbitrary packet
cardinalities.

## Consequence for a paid non-EFX branch

Suppose `Z` pays all owners but is not EFX.  Global-minimum failed-response
extraction gives a current-common-safe desired core `D subseteq Z_t` and the
complete decorated record

\[
 (s,Z_t,D;(I_i,O_i)_{i\in N}),                    \tag{2}
\]

where `(I_i,O_i)` is the full signed decoration relative to the fixed GG
base `X`.

By (1), the physical target support `Z_t` differs from every same-owner
current target `Y_t`.  Thus (2) cannot be an unchanged-current-support replay
of a response recorded at `Y`.  Exactly one of the following occurs:

1. the source/core/target/release decoration (2) is new and permanently
   augments the finite response ledger; or
2. the complete decorated record occurred at an earlier cross-state probe.

In outcome 2, `FULL_SIGNED_TRANSFER_STATE_RECONSTRUCTION_LEMMA_20260811.md`
implies that the earlier allocation, all four bundles, charity, moved-good
graph, target supports, and response/release labels are exactly `Z`.  The
survivor is therefore an **exact paid four-edge record repeat**, not an
untyped old response and not merely repetition of a coarse response edge.

## Combined form-2 frontier

On the shared-target-disjoint branch, the six probes now give:

1. a complete four-edge EFX allocation;
2. a new decorated response/support record;
3. an exact paid four-edge decorated-record repeat; or
4. simultaneous owner-payment failure, equivalent to the three
   supplier-capture inequalities.

Shared-target failure remains the double-margin packet alternative.  At a
saturated state outcome 2 is excluded.  The response-rank question has
therefore been replaced by the sharper repeat question: show that outcome 3
enters the exact base-margin/direct-safety terminal of represented-component
charity extraction, or yields release-compatible PI/progress.

## Claim boundary

Proved: every owner target changes, a paid failure produces a
current-common-safe decorated response, and any non-new survivor repeats the
complete physical allocation/record exactly.

Not proved: closure of the exact repeat, the base-margin/direct-safety
interface, contradiction of supplier capture or double capture, the fixed-`U`
theorem, or general EFX.
