# Alternating external-observer classification

**Date:** 2026-08-09

**Status:** all eight hard orders classified; surviving pair proved cap-free


*Cancelable-class repair 2026-08-16, third pass* (S3 of
[`CANCELABLE_CLASS_SWEEP_20260816.md`](CANCELABLE_CLASS_SWEEP_20260816.md)).
**Convention.** Throughout, `tau_i(Z)=max_{g in Z} v_i(Z\{g})` (max deletion),
and a set `Z` is *common-safe* when `tau_i(Z)<=b_i` for every agent `i`, where
`b_i=v_i(X_i)`. This is the definition stated in
[`ALTERNATING_RESERVOIR_EXCHANGE_LEMMA.md`](ALTERNATING_RESERVOIR_EXCHANGE_LEMMA.md)
and used uniformly across the in-closure files; it is recorded here so that no
file uses the symbol without a resolvable definition.

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
closes `(p,s,q,r)` and `(p,q,s,r)` using either a selected-offer promotion,
an anchored `q`-handoff, or an opposite-reservoir root promotion.  Its
half-turn closes `(s,p,r,q)` and `(s,r,p,q)`. Thus all eight hard orders are
closed cap-free by the three component constructions, even though six of
the narrower anchored candidates remain exactly refuted.

Thus this classification completes the stated external-observer research
goal and removes one genuine arbitrary-packet gate, but it is not a proof
of general four-agent additive EFX.
