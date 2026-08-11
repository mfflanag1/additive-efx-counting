# Anchor-constrained full-priority matching lemma

**Date:** 2026-08-11

**Status:** cap-free triangularization of every sacrificed-source response
boundary under the permanent root anchor

## Selector

Let `G` be the bipartite response graph between four sources and four active
targets. Fix the permanent root edge

\[
 e=(r,h)
\]

and a priority order

\[
 i_1\prec i_2\prec i_3
\]

on the three nonroot sources. Among all matchings containing `e`, first
maximize cardinality and then lexicographically maximize the represented-
source indicator

\[
 (\mathbf 1[i_1\text{ represented}],
  \mathbf 1[i_2\text{ represented}],
  \mathbf 1[i_3\text{ represented}]).              \tag{1}
\]

Use any deterministic physical-core tie-break only after (1).

## Triangular blocker theorem

If `i_k` is unmatched by the selected matching, every response neighbor of
`i_k` is either:

1. the anchored target `h`; or
2. a target matched to some strictly earlier source `i_l` with `l<k`.

In particular, an unmatched source has no edge to an unmatched target and no
edge to a target occupied by a later-priority source.

## Proof

Let `t` be a neighbor of unmatched `i_k`.

- If `t` is unmatched, adjoining `(i_k,t)` increases cardinality while
  retaining `e`, contradicting the first selection criterion.
- If `t=h`, the edge cannot replace the forced anchor and is the first named
  alternative.
- Otherwise `t` is matched to a nonroot source `i_l`. If `l>k`, replace
  `(i_l,t)` by `(i_k,t)`. Cardinality and the anchor are unchanged, while the
  first changed coordinate of (1) goes from zero to one. This contradicts
  the secondary selector.

Therefore `l<k`, proving the theorem. \(\square\)

## Acyclic response consequence

Orient a blocker arc from an unmatched source to the source occupying each
of its response targets. Every non-anchor arc strictly decreases the fixed
priority index. Hence blocker chains cannot cycle: after at most three
nonroot steps they reach the permanent root anchor.

This is stronger than prioritizing only `q`. It identifies the entire
represented priority prefix and prevents a sacrificed external owner from
starting an arbitrary `c`/`s` hole cycle at the matching level.

## Reset persistence

Every selected nonroot response core is disjoint from the anchored root core,
which contains the unique charity good `f`; hence each selected nonroot core
is floater-free. On a top-only orientation reset, apply universal retained
support simultaneously to all selected nonroot cores. Exactly one of the
following occurs:

1. all selected coverage indicators in (1) are preserved;
2. retained top support `U` grows strictly; or
3. the remaining `q` margin is captured and enters the anchored residual
   rotation.

Thus a top-only reset cannot reduce the protected priority prefix at fixed
`U`. A floater-consuming response is routed separately by its named source.
The only operation that can sacrifice an earlier covered source is therefore
an explicit core release/J-exhaustion, not matching recompression.

## Interaction with the root-budget frontier

When a captured external source is response-active away from `h`, the
selector represents it unless doing so would displace an earlier protected
source. Following such blockers is strictly priority-decreasing and reaches
the root-facing handoff. When it has only the anchor neighbor, its collision
is already root-facing. When it has no response edge, its same-row residual
can be globally maximized before source-inactive repair.

Consequently the third-owner continuation from an exchange-stable two-row cut
has only three structural destinations: protected owner-union growth, an
acyclic handoff to the root-facing frontier, or a genuinely response-silent
source-inactive residual. It cannot create a free matching-label cycle.

## Verification and boundary

[`anchor_constrained_full_priority_matching_audit.json`](anchor_constrained_full_priority_matching_audit.json)
exhausts all `2^15` response graphs containing the anchor. Every selected
matching and every unmatched-source neighbor obeys the triangular blocker
theorem.

This lemma proves graph-level triangularity and top-reset persistence. It
does not physically close an anchor-only collision, terminate an explicit
J-exhaustion, reverse an unsafe residual hitting set, select the final
surplus-budgeted fork, close `GG`, or prove four-agent/general additive EFX.
