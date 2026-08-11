# Permanent-anchor q-activity dichotomy lemma

**Date:** 2026-08-11

**Status:** cap-free elimination of every response-active sacrificed-`q`
matching state, with no maximum-rank compatibility assumption; the resulting
degree-zero source-inactive recurrence remains open

## Protected anchor

Let `G` be the bipartite response graph between owner sources and active
targets.  The changed later-owner target `h` has the permanent root response
edge

\[
 e=(r,h).                                            \tag{1}
\]

Because the live branch sacrifices `q` below her base utility while every
subset of `h` is no more valuable to `q` than `h` itself,

\[
 (q,h)\notin E(G).                                  \tag{2}
\]

Choose a maximum-cardinality matching among those required to contain `e`.
Subject to that cardinality and anchor constraint, prefer a matching that
represents `q`.

## Theorem

Exactly one of the following holds.

1. The selected anchor-constrained maximum matching represents `q`.
2. `q` has response degree zero in the full active relation:
   \[
   \deg_G(q)=0.                                     \tag{3}
   \]

This conclusion is independent of the unrestricted maximum rank.  In
particular, it remains true when forcing the permanent anchor lowers rank.

## Proof

Suppose the selected matching leaves `q` unmatched and `q` has an edge to a
target `t`.  Equation (2) gives `t != h`.

- If `t` is unmatched, adding `(q,t)` increases the cardinality while
  retaining the anchor, contradicting constrained maximality.
- If `t` is matched, let `(a,t)` be its matching edge.  Since `r` is already
  matched to `h`, we have `a != r`.  Replace `(a,t)` by `(q,t)`.  The new
  matching has the same cardinality, still contains `(r,h)`, and represents
  `q`, contradicting the secondary choice.

Therefore no such `t` exists and (3) holds.  No item cardinality, valuation
cap, equality assumption between constrained and unrestricted rank, or
alternating-path analysis is used.  \(\square\)

## Flower consequence

The root-anchored sacrificed-`q` boundary no longer permits repeated changes
of the missing-owner valuation row merely because the unrestricted matching
has higher rank.

- Whenever `q` responds to any active target, select an anchor-constrained
  maximum matching representing `q`; an external owner may be left in a
  residual cell, but `q` receives a desired common-safe core.
- Whenever `q` is sacrificed while retaining the anchor, she is genuinely
  source-inactive against **every** active target.

Thus the raw and historical cross-owner residual potentials are unnecessary
for the protected later owner.  The remaining fixed-`U` theorem is narrower:
starting from a degree-zero `q`, prove that core/residual repair either makes
`q` response-active, constructs a surplus-budgeted connected component, or
forces the retained-support/hitting-set contradiction.  The instant `q`
becomes active, the first branch above removes her as a hole without dropping
the permanent root anchor.

An anchor-rank gap may still create an additional external residual cell.
That is a two-hole partition problem, not a reason to sacrifice active `q`.

## Exact verification and boundary

[`permanent_anchor_q_activity_dichotomy_audit.json`](permanent_anchor_q_activity_dichotomy_audit.json)
exhausts all `2^14` four-source/four-target response relations with (1)
forced and (2) forbidden.  In every one of the 14,336 relations where `q`
is active, an anchor-constrained maximum matching represents `q`; the other
2,048 relations have degree-zero `q`.

The lemma is a response-graph theorem.  It does not pay the remaining
external residual cells, prove that a degree-zero `q` becomes active, close
the source-inactive/hitting-set recurrence, establish physical release
support for every subsequent repair, close `GG`, or prove four-agent/general
additive EFX.
