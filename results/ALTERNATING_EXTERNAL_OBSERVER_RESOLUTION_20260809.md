# Alternating external-observer classification

**Date:** 2026-08-09

**Status:** all eight hard orders classified; surviving pair proved cap-free

## Complete classification

For the anchored, external-observer-safe three-agent improvement candidate,
the eight hard alternating priority orders split as follows.

| Priority order | Candidate status | Evidence |
|---|---|---|
| `(p,s,r,q)` | cap-free theorem | reservoir-exchange lemma |
| `(s,p,q,r)` | cap-free theorem | half-turn of reservoir-exchange lemma |
| `(p,s,q,r)` | exactly refuted | strict seven-good countermodel |
| `(p,q,r,s)` | exactly refuted | strict seven-good countermodel |
| `(p,q,s,r)` | exactly refuted | strict seven-good countermodel |
| `(s,p,r,q)` | exactly refuted | strict seven-good countermodel |
| `(s,r,p,q)` | exactly refuted | strict seven-good countermodel |
| `(s,r,q,p)` | exactly refuted | strict seven-good countermodel |

The six exact countermodels and the two atomic UNSAT decisions are replayed
by [`alternating_anchored_or_promoted_atomic_audit.json`](alternating_anchored_or_promoted_atomic_audit.json)
and its generator.  “Refuted” applies to the anchored external-observer
candidate, not to the existence of some other EFX lexicographic escape.

## Cap-free surviving theorem

For `(p,s,r,q)`, let `D=T_q+f` and `U=X_r+B_q`.  The
[`reservoir-exchange lemma`](ALTERNATING_RESERVOIR_EXCHANGE_LEMMA.md)
constructs disjoint common-safe bundles `A,Q`, with `A` desired by `r` or
`s` and `v_q(Q)>=tau_q(A)`.  The
[`two-safe-bundle reduction`](ALTERNATING_TWO_SAFE_BUNDLE_REDUCTION.md)
turns them into the required EFX lexicographic improvement.  The proof is
independent of packet cardinalities.  Half-turn relabeling proves
`(s,p,q,r)`.

The constructive audit
[`alternating_reservoir_exchange_audit.json`](alternating_reservoir_exchange_audit.json)
replays all three proof branches on the 18 frozen exact adversarial
profiles.  It is corroboration; the theorem is analytic.

## Relation to the wider alternating program

The external-observer candidate is now fully resolved, but the alternating
topology is not.  The cap-free root-flip lemma closes `(p,q,r,s)` and
`(s,r,q,p)` using a different rival form despite their anchored-candidate
countermodels.  The cap-free
[`dual-reservoir trichotomy`](ALTERNATING_DUAL_RESERVOIR_TRICHOTOMY.md)
closes `(p,s,q,r)` and `(s,p,r,q)` using either a selected-offer promotion,
an anchored `q`-handoff, or an opposite-reservoir root promotion.  Two hard
priority orders remain:

\[
(p,q,s,r),\quad(s,r,p,q).
\]

Thus this classification completes the stated external-observer research
goal and removes one genuine arbitrary-packet gate, but it is not a proof
of general four-agent additive EFX.
