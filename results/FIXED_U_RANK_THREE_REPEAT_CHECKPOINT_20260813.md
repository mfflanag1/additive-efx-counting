# Fixed-U rank-three repeat checkpoint

**Date:** 2026-08-13

**Status:** the former termination claim has been withdrawn; one exact
rank-three, two-hole capture-return gate remains

## What is now proved

1. The uncompensated fourth donor can be restored to its whole desired core;
   only the external owner remains sacrifice-eligible. This removes the last
   fourth-donor payment separator but returns to response compression.
2. Saturated response components of sizes two through four are excluded
   **when** their response matching has rank equal to the component size and
   unchanged outsiders are directly safe.
3. Full physical owner coverage does not force that rank premise. Exhaustion
   of all 32,768 anchor-containing response graphs leaves 208 connected,
   owner-cycle-free, rank-three survivors, collapsing to three selected
   matchings and three owner-hole pairs.
4. Globally splitting the complete residual pool between the sacrificed
   owner and nonempty charity is cap-free and exact. A least-valued residual
   good is optimal over every charity subset. Failure is equivalent to one
   strict capture-or-parked-own-support inequality against a selected core.

## Why the previous proof did not close

The exact-history potential is finite, but finiteness alone only forces an
exact repeated state. The rank-four Hamiltonian charity-path theorem closes
a repeated full matching. A rank-three state has one unmatched owner and,
after charity is included, two unmatched targets. The unmatched owner can be
physically joined through its root-facing response into the permanent anchor
without becoming represented. Therefore exact reconstruction preserves a
two-hole obstruction rather than manufacturing the missing fourth edge.

The coarse composition audit previously represented `exact_repeat` as an
edge directly to saturated extraction. That edge was an assumption, not an
encoded consequence. Its status is now `RANK_THREE_REPEAT_GATE_OPEN`.

## Adversarial decision evidence

An eleven-good symbolic cell realizes the smallest rank-three wall pattern
with base EFX, positive additive values, a strict root and fourth owner, a
weakly paid protected owner, and one sacrificed owner. CEGAR repeatedly asks
whether the valuation profile admits any root-improving complete EFX
allocation with nonempty charity.

- The unrestricted full-lex run installed 163 exact allocation cuts before
  an interrupted/timeout checkpoint; it did not produce a countermodel.
- The root-coordinate minimum-move run installed 300 cuts. Every adversarial
  valuation encountered had an exact root-improving EFX escape moving two,
  three, four, or five goods: 6 at radius two, 130 at radius three, 162 at
  radius four, and 2 at radius five. Thus radius four is strongly dominant
  but not universal even in this atomization.
- A one-shot decision installed every one of the 90,332 allocations within
  radius four (44/864/10,128/79,296 by exact radius). Z3 timed out, so this is
  neither SAT nor UNSAT.

The minimum-move motifs consistently keep the strict fourth-owner packet and
most of the current root target, then use charity-to-`q`, `q`-to-sacrificed-
owner, and one compensating exchange through the root or fourth owner. This
is evidence for a connected charity-anchor replacement lemma, not its proof.

## Exact live theorem

Let `d` be the unmatched sacrifice-eligible owner, `A_r` the permanent root
core in the changed `q` target, and `P` the complete residual pool. After the
global residual split fails, prove that

\[
 v_d(C)+\chi>
 v_d(E)-\epsilon+v_d(X_d)-\tau_d(A_r)
\]

forces one of:

1. return of captured `d`-support while paying its selected-core source;
2. a charity-to-`q`, `q`-to-`d` connected replacement with root/fourth-owner
   compensation;
3. a release-compatible PI component;
4. strict retained/support/response progress; or
5. rank growth from three to four.

Otherwise produce a positive rational profile satisfying the complete
fixed-`U` bottom-tail, reassembly, global-root-maximal, PI-free, signed-state,
and response-saturation premises and exhibiting a genuine repeat.

This gate, not the already closed rank-four mixed-margin payment problem, is
the current boundary. The fixed-`U` branch, GG, four-agent additive EFX, and
general additive EFX remain open.

## Replay

```bash
/private/tmp/efx-charity-py/bin/python tracks/parkability/audit_rank_three_exact_repeat_gate.py --output results/rank_three_exact_repeat_gate_audit.json
/private/tmp/efx-charity-py/bin/python tracks/parkability/audit_rank_three_two_hole_global_residual_split.py --output results/rank_three_two_hole_global_residual_split_audit.json
/private/tmp/efx-charity-py/bin/pytest -q tracks/parkability/test_rank_three_exact_repeat_gate.py tracks/parkability/test_rank_three_two_hole_global_residual_split.py tracks/parkability/test_fixed_u_retained_support_termination.py
```
