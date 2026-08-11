# Flower external-bottom-edge rank-two anchor lemma

**Date:** 2026-08-11

**Status:** cap-free exclusion of rank-one termination in the `GG` flower;
termination inside the canonical rank-two boundary remains open

## Two permanent disjoint targets

In the length-two `GG` flower, the mutual edge gives the anchored
common-safe desired root core

\[
 A_r=T_q+f                                             \tag{1}
\]

sourced by `r`.

BCFF's external `(B_q\mid B_r)` bottom edge into the root supplies another
common-safe desired core

\[
 A_b\subseteq T_r+B_q                                 \tag{2}
\]

whose source `b` lies in `{c,s}`.  In particular `b != r`.

The supports in (1),(2) are disjoint:

\[
 (T_q+f)\cap(T_r+B_q)=\varnothing.                    \tag{3}

\]

Thus the two response edges `r -> A_r` and `b -> A_b` always form a
rank-two matching with pairwise-disjoint common-safe desired cores.

## Canonical rank-two reset

Give `A_r` to `r`, give `A_b` to `b`, and pool every remaining good between
the other two owners.  Apply cut-and-choose to that pool.  The two residual
owners are mutually EFX, the root remains strictly above base, and every
remaining wall belongs to the exact two-core/two-hole response boundary.
Consequently the 2-by-2 normal form gives an EFX lex improvement, a
release-compatible PI component, or an empty-target/source-inactive repair
state.

This reset is available after any attempted second rank descent.  All goods
of `A_b` remain inside the complete owner union even if a preceding repair
or pivot distributed them among several temporary bundles.  Extracting the
fixed packet (2) and pooling its complement preserves completeness and
release support.

## Consequence for the rank-one normal form

The abstract one-core/three-hole external-star normal form is not a terminal
state of the `GG` flower.  Before invoking a general three-agent remainder
selector, reinsert the permanent external-bottom-edge core `A_b`.  The
response rank returns to two and the proof re-enters the already classified
two-hole boundary.

Likewise, the root-monopoly relation for the auxiliary target
`U=T_r+B_q` is impossible in the flower: equation (2) supplies a nonroot
response source for `U`.  The root-monopoly complement theorem remains a
valid generic fallback, but its terminal two-row branch is not needed for
this `GG` rank reset.

## Verification and claim boundary

[`flower_external_bottom_edge_rank_two_anchor_audit.json`](flower_external_bottom_edge_rank_two_anchor_audit.json)
checks source distinctness, packet disjointness, rank-two matching, reset
support, and all 16 two-hole response relations.

This lemma excludes rank-one termination cap-free.  It does not prove that
successive canonical rank-two resets strictly increase a global potential,
terminate source-inactive repair/reset recurrence, close captured-bottom or
unsafe-residual overlap, close `GG`, or prove four-agent/general additive
EFX.
