# Anchor-constrained q-priority matching lemma

**Date:** 2026-08-11

**Status:** cap-free elimination of response-active sacrificed `q` whenever
the permanent root anchor preserves maximum rank; anchor-gap release and the
source-inactive reset recurrence remain open

## Anchored response relation

Use the complete charity path after the root-monopoly handoff.  Let

\[
 h=Y_q=(X_q\setminus K)+f
\]

be the changed later-owner target.  It contains the permanent common-safe
root core `T_q+f`, so the response relation has the fixed edge

\[
 r\longrightarrow h.                               \tag{1}
\]

In the live sacrificed branch,

\[
 v_q(h)<v_q(X_q).                                   \tag{2}

By positivity, every subset of `h` has value at most `v_q(h)`.  Thus `q`
has no desired response into its own changed target:

\[
 q\not\longrightarrow h.                           \tag{3}

Let `nu` be the maximum rank of the full response relation.  Let `nu_h` be
the maximum rank among matchings required to contain (1).

## Matching dichotomy

Exactly one of the following holds.

1. **Anchor gap:** `nu_h<nu`.  The symmetric difference between an
   unrestricted maximum matching and an anchor-constrained maximum matching
   contains an alternating path through (1).  This is the exact response
   path whose physical release support must be composed with the permanent
   `B_q` release.
2. **Anchor-compatible maximum rank:** `nu_h=nu`.  Among maximum matchings
   containing (1), first prefer a matching that represents `q`.  If one
   exists, `q` is not the residual owner.  If none exists, then `q` has no
   response edge to any active target.

For the last assertion, let `M` be an anchored maximum matching leaving `q`
unmatched.  A `q` edge to an unmatched target would augment `M`.  A `q` edge
to a target matched by an external source could replace that one edge,
preserving rank and (1) while representing `q`.  The target matched by `r`
is `h`, and (3) forbids the remaining case.  Hence

\[
 \deg(q)=0.                                         \tag{4}
\]

No item cardinality or value cap is used.

## Consequence for the reset potential

The sacrificed-`q` Hall boundary no longer requires comparisons between
different missing owners.

- If `q` is response-active and the anchor is rank-compatible, select a
  maximum matching representing `q`; sacrifice an external owner instead.
- If the anchor costs rank, retain the named anchor-gap alternating path.
- Otherwise `q` is genuinely source-inactive against every active target.
  During any fixed-state repair phase, the core/residual repair and two-hole
  descent therefore compare residual progress in `q`'s row only.  If `q`
  later becomes response-active, the first branch applies.

On the exact four-state plateau that refutes the historical ledger, take
`h=A_r`.  Requiring `r -> A_r` removes the two states rooted at `W`, and
prioritizing `q -> A_c` removes the state that represents `c` instead.  Thus
the four matching labels collapse to the single deterministic choice

\[
 (A_r,q,c,W).
\]

The plateau therefore refutes historical maxima, but not this current-state
selector.  Recurrence through different physical response cores remains an
analytic issue.

This is the graph operation missing from the raw potential: maximize rank
subject to the permanent release anchor and then maximize representation of
the protected sacrificed owner.  It prevents a gratuitous change of the
missing-owner valuation row.

## Exact audit and boundary

[`anchor_constrained_q_priority_matching_audit.json`](anchor_constrained_q_priority_matching_audit.json)
exhausts all `2^14` response relations on four sources and four targets with
(1) forced and (3) forbidden.  Every relation is classified as an anchor
rank gap, an anchor-compatible matching representing `q`, or an
anchor-compatible state in which `q` has degree zero.

The lemma does not prove that the anchor-gap alternating path is
release-compatible, show that every source-inactive rank-two reset preserves
the improved `q` cell, close fixed-support/floater recurrence, close `GG`, or
prove four-agent/general additive EFX.
