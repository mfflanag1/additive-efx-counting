# Closed base-block cross-response merger lemma

**Date:** 2026-08-14

**Status:** cap-free elimination of outsider safety as an independent
base-cancellation gate; internal response rank remains open

## Closed blocks after a paid branch

Let `X` be the fixed base allocation and let `Z` be a complete allocation
that weakly base-pays every owner. Partition the owners together with the
base-charity vertex into the connected components of the net `X -> Z`
transfer graph. By the closed-union theorem, every block `K` satisfies

```text
X(K) = Z(K)
```

as an equality of physical good sets.

Suppose an owner `i` in one block is not EFX-safe against an owner target
`j` in another block. Among all failed owner/target subbundles, choose a
globally inclusion-minimal current-desired core `D subseteq Z_j` for `i`.
Then

```text
v_i(D) > v_i(Z_i)
tau_h(D) <= v_h(Z_h) for every owner h.
```

Thus `D` is a current-safe decorated response from target `j` to source
`i`. Since `X(K)=Z(K)`, every good in `Z_j` has base origin in the target
block, while the response source lies in a different block.

## Quotient merger

Contract every closed base block to one vertex. Record an undirected
quotient edge whenever an exact decorated response has target in one block
and source in another. A cross-block EFX failure has exactly two outcomes:

1. its full source, target support, core, release, and signed compensation
   record is new, giving response augmentation; or
2. that exact record is already present, in which case its quotient edge
   joins the two blocks inside one represented-response component.

Adding a response whose endpoints lie in different current quotient
components strictly reduces their number. Therefore at most `b-1` such
component mergers can occur from a partition with `b` blocks.

At a saturated record, new response labels and represented-component growth
are both excluded. Consequently no EFX failure crosses two distinct
maximal represented-response components of the closed-block quotient.
Equivalently, each maximal union of blocks is outsider-safe against every
other such union.

## Consequence for cancellation

When a four-edge current-support branch becomes disconnected after exact
composition with the older base record, cancellation yields closed aggregate
blocks, not a new terminal. Close those blocks under already recorded
cross-block responses. Saturation then gives an exact dichotomy:

1. the closure recruits every owner into one full represented component; or
2. it is a proper represented component whose outside-owner comparisons are
   safe.

This supplies the outsider-safety interface required by the saturated
represented-component extraction theorem. The remaining admission
condition is response rank inside the resulting component, together with
the required signed base-margin and release hypotheses.

## Verification boundary

The finite audit enumerates all 52 partitions of the five physical vertices
and every quotient graph on their blocks. It checks 1,769 additions of an
owner-to-owner cross-component response and verifies that each reduces the
component count by exactly one. Current-safe core extraction is inherited
from the independently audited paid-splice observer-failure lemma; it is not
re-encoded as a second valuation solver here.

## Claim boundary

Proved: physical localization of a cross-block core, current-safe response
extraction, strict quotient-component merger, finite termination of mergers,
and outsider safety at saturation. Not proved: rank equal to component
size, the component-wide base-margin separator, release compatibility,
charity-target safety, the fixed-`U` theorem, or additive EFX.
