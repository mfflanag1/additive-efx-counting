# Charity-augmented five-target hole-pivot cycle lemma

**Date:** 2026-08-11

**Status:** cap-free matching-level closure of every exact repeated charity
hole by an alternating cycle; persistence of physical edge labels across a
changing target remains the final interface

## Five targets and four sources

At a paid repeated-support splice, regard the four owner targets together
with the current charity packet as five pairwise-disjoint physical targets.
Let the four owners be response sources.  Select a rank-four response matching

\[
 M:S\longrightarrow T\setminus\{H\},             \tag{1}

\]

where `H` is the unique unmatched **charity hole**.  Each selected edge carries
a common-safe desired core and its exact physical release label.  The matching
is chosen by the existing root-anchor/full-priority selector whenever that
anchor is present.

## One hole pivot

Suppose source `i` has a response edge into the hole `H`.  Write

\[
 K=M(i).                                           \tag{2}

\]

Replace edge `(i,K)` by `(i,H)`.  Cardinality remains four, every source stays
represented, and the unique unmatched target becomes `K`.  Thus a charity or
owner-target response into the hole changes only the unmatched physical
target; it cannot reduce response rank or owner coverage.

If `(i,H)` is a new exact physical response label, recording it is permanent
response augmentation.  Otherwise the pivot is the canonical continuation
of an already recorded decorated response.

## Repeated-hole cycle

Consider successive old-edge pivots at one exact decorated physical state.
Write the holes

\[
 H_0,H_1,\ldots                                    \tag{3}

\]

and pivot sources `i_0,i_1,...`, where before pivot `t`, source `i_t` is
matched to `H_{t+1}` and moves to `H_t`.

There are only five targets.  If no response augmentation or physical-state
change occurs, some hole repeats among `H_0,...,H_5`.  At the first repeat

\[
 H_b=H_a,\qquad a<b,                               \tag{4}

\]

the intermediate holes are pairwise distinct.  Moreover, the source of the
closing pivot is the source of the pivot that first left `H_a`; the sources
of the intervening pivots together with that closing source are pairwise
distinct.  The edges

\[
 i_t\longrightarrow H_t
 \quad(a<t<b)                                     \tag{5}


form an alternating cycle, where the closing source `i_{b-1}=i_a` supplies
the final edge.  Immediately before the segment, these sources were matched
cyclically to the next targets.  Applying all edges in (5) simultaneously
preserves matching cardinality and agrees with the old matching outside the
cycle.

## Physical release consequence

The five current targets are disjoint.  Hence desired cores chosen from the
cycle targets are pairwise disjoint.  If their recorded incoming/release
labels are unchanged across the exact repeated decorated state, every core
released by one cycle source supplies the next cycle target, including the
charity-to-owner and owner-to-charity exchange at the hole boundary.  The
cycle is then a release-compatible generalized PI component.  If a label has
changed, its new exact support is permanent response augmentation or retained-
support progress rather than recurrence.

After the component payment and charity-exchange endpoint checks:

1. an observer-safe cycle is an EFX/lex or Pareto-improving endpoint;
2. an internal desired-core cycle is a release-compatible PI contradiction;
3. a failed target produces the surplus-decorated response continuation; and
4. a changed edge label gives permanent response/support augmentation.

Thus an exact full-owner state cannot repeat solely by moving the charity
hole among old response edges.

## Verification and boundary

[`charity_augmented_five_target_hole_pivot_cycle_audit.json`](charity_augmented_five_target_hole_pivot_cycle_audit.json)
exhausts all 120 rank-four matchings of four labeled sources into five targets
and every pivot sequence through the first repeated hole.  It verifies rank
preservation, unique-hole evolution, distinctness before first repetition,
cycle rotation, and invariance outside the cycle.

This lemma assumes an exact repeated decorated physical response state and
stable edge labels.  It does not prove that every dynamic GG reset preserves
those labels, force observer-safe payment of every extracted cycle, close the
universal repeated-support theorem, close GG, or prove four-agent/general
additive EFX.
