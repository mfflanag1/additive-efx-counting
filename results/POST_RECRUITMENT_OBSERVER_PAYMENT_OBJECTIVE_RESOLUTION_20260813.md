# Post-recruitment observer-payment objective resolution

**Date:** 2026-08-13

**Verdict:** **exactly refuted.** Supplier saturation does not force mixed-
cycle observer payment, and the alleged `R_q`-only anchor-preserving
compensation case is false. Complete-pool payment is a valid optional
shortcut but is not a necessary premise after the priority-valid sacrifice
handoff.

## Frozen objective

The objective was to prove or exactly refute the post-recruitment theorem
asserting observer payment for a supplier-saturated mixed response cycle,
including the root-sourced collision in which the permanent old root anchor
is retained and the displaced source is compensated from the q-target
residual.

The archived post-recruitment statement uses these premises:

1. four owners lie on a directed cycle of pairwise-disjoint selected cores;
2. at least one core is current-desired/current-safe and the remaining cores
   are old base-desired/base-common-safe;
3. the signed supplier closure of the selected packets is all four owners;
4. old sources may receive released residual goods; and
5. the permanent old edge `r -> q` and its root anchor are retained.

The claimed conclusion was that these facts force every observer debt to be
paid. They do not.

## Requirement-by-requirement resolution

| Requirement | Exact evidence | Verdict |
|---|---|---|
| Supplier-saturated mixed cycle | Positive rational four-owner witness with cycle `r -> q -> a -> b -> r`, three old cores, and one decorated core | satisfied |
| Internal physical supply | Supplier closure is exactly all four owners | satisfied |
| Permanent root anchor | `K_r` remains assigned to the root in every audited residual return | satisfied |
| Observer payment | The blocked row has value `11.4` even with the entire four-residual pool, below decorated threshold `12` | false |
| Exhaust residual assignments | All `5^4=625` assignments of the four residual goods to four owners or charity are enumerated; none is EFX while all owners remain above base | false conclusion independently replayed |
| `R_q`-only root compensation | A second exact positive witness has `a(A-J+R_q)=5<10` but `a(A-J+R_q+R_r)=11>10` | exactly refuted |
| Anchor retained during root response | The root response is disjoint from `K_r`; both remain with the root | satisfied |
| Complete-pool failure as terminal | The root may take `K_r+E`, the unaffected sources retain protected cores, and the displaced later owner receives the exact complement | superseded by a priority-valid sacrifice handoff |

The first countermodel and its independent implementation establish the
negative answer without relying on solver failure or bounded-value
extrapolation. The 625 cases are the entire residual-assignment family in
the frozen implication. The second witness is a structural counterexample
to the assertion that `R_q` is the complete anchor-preserving compensation
reservoir.

## Exact corrected theorem

What remains true is the following narrower statement.

1. For a root-sourced collision, the complete physically available residual
   pool is
   \[
   \mathcal R_E=(\dot\bigcup_i R_i)\setminus E.
   \]
2. If even this pool cannot pay displaced source `a`, then
   \[
   v_a(J)-v_a(\mathcal R_E)\ge v_a(A)-F_a>0.
   \]
3. This inequality diagnoses failed paid completion, but does not prevent a
   lexicographically valid move: retain the anchor, give `K_r+E` to the
   first-priority root, and sacrifice the displaced later source.
4. Every subsequent failure is an explicitly labeled sacrificed-owner,
   residual, or enlarged-root-target response. A minimal response to the
   enlarged root target is response-side, anchor-side, or a mixed permanent-
   anchor hitting set.

Thus the payment theorem is not repairable by replacing `R_q` with a larger
unnamed reservoir. Its correct replacement is a response-compression
transition.

## Scope boundary

This resolution does **not** prove four-agent additive EFX and does not
resolve the stronger globally recurrent/maximal GG closure theorem. The
source manuscripts explicitly distinguish that strengthening from the
generic post-recruitment payment implication. The surviving GG problem is
to terminate a mixed permanent-anchor hitting-set recurrence or show that
anchor release/reselection is forced.

That remaining problem does not change the verdict on this objective: the
stated observer-payment implication and its `R_q`-only anchor case are
exactly false.

## Reproducible evidence

- [`SUPPLIER_SATURATION_DOES_NOT_FORCE_MIXED_CYCLE_PAYMENT_20260813.md`](SUPPLIER_SATURATION_DOES_NOT_FORCE_MIXED_CYCLE_PAYMENT_20260813.md)
- [`supplier_saturation_does_not_force_mixed_cycle_payment_audit.json`](supplier_saturation_does_not_force_mixed_cycle_payment_audit.json)
- [`supplier_saturated_payment_refutation_independent_audit.json`](supplier_saturated_payment_refutation_independent_audit.json)
- [`ROOT_SOURCED_COMPLETE_SIGNED_RESIDUAL_COMPENSATION_LEMMA_20260813.md`](ROOT_SOURCED_COMPLETE_SIGNED_RESIDUAL_COMPENSATION_LEMMA_20260813.md)
- [`root_sourced_complete_signed_residual_compensation_audit.json`](root_sourced_complete_signed_residual_compensation_audit.json)
- [`ROOT_SOURCED_ANCHOR_RETAINING_SACRIFICE_HANDOFF_LEMMA_20260813.md`](ROOT_SOURCED_ANCHOR_RETAINING_SACRIFICE_HANDOFF_LEMMA_20260813.md)
- [`ENLARGED_ROOT_TARGET_ANCHOR_HITTING_TRICHOTOMY_20260813.md`](ENLARGED_ROOT_TARGET_ANCHOR_HITTING_TRICHOTOMY_20260813.md)
- [`post_recruitment_observer_payment_resolution_independent_audit.json`](post_recruitment_observer_payment_resolution_independent_audit.json)

