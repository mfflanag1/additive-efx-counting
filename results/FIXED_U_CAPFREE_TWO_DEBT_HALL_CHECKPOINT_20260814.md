# Fixed-U cap-free two-debt/Hall checkpoint

**Date:** 2026-08-14

**Status:** dual-verified sharp root/sacrifice two-debt theorem and cap-free
reductions; universal four-edge conclusion remains open

## New headline

The allocated-`E` form-2 bounded theorem now guarantees more than complete
EFX. Under the complete generalized-PI exclusion pool, one of seven explicit
at-most-four-edge EFX endpoints has at most two base-payment holes.

This has now been sharpened: the same endpoint can always be chosen to pay
both represented owners `q` and `s`, so every hole belongs to `{r,d}`.  A
separate exact PI-free countermodel shows that one hole is insufficient while
retaining both payments.  Thus the two residual rows are canonical and sharp,
not an anonymous cardinality bound.  See
`ALLOCATED_E_QS_PAID_TWO_DEBT_SHARP_THEOREM_20260814.md`.

The producer restores 46,683 independently validated PI clauses and returns
UNSAT when all seven such endpoints are forbidden. Assumption-core extraction
reduces this to 1,966 PI clauses—638 three-owner and 1,328 four-owner clauses—
plus all seven endpoints. An independent encoding using nested tail minima,
direct deletion inequalities, direct payment counting, and a different seed
again returns UNSAT.

See `ALLOCATED_E_TWO_PAYMENT_HOLE_SEVEN_ENDPOINT_THEOREM_20260814.md`.

## Cap-free lift obtained

Two analytic reductions remove arbitrary packet size from the proof
interface.

1. **Hidden-minimum split.** Whenever a bundle is safe after compressed-atom
   deletion but unsafe after physical single-good deletion, its least physical
   good lies strictly inside a nonsingleton compressed atom and satisfies an
   exact strict margin inequality. There is no third cardinality-dependent
   failure mode.
2. **Physical Hall lift.** Every expanded three-/four-core compressed PI clause
   yields physical generalized PI, an outside-source response, or a Hall-
   deficient internal response graph. An inclusion-minimal deficiency has
   exactly one missing source and a near-perfect matching; for four owners it
   uses at most three response edges, leaving one charity edge within budget.

See `PHYSICAL_PACKET_COMPRESSION_HIDDEN_MINIMUM_LEMMA_20260814.md` and
`DISJOINT_COMPRESSED_CORE_PHYSICAL_HALL_LIFT_LEMMA_20260814.md`.

Payment depends only on packet totals and therefore survives physical
expansion exactly. For the selected two-hole endpoint, a failed EFX observer
who is not a payment-hole owner exposes an ordinary base-desired response by
globally minimal extraction. Hence physical endpoint failure is localized to
an ordinary response augmentation or at most two current/base debt rows. See
`TWO_HOLE_ENDPOINT_PHYSICAL_FAILURE_LOCALIZATION_LEMMA_20260814.md`.

## Computational physical-tail gate

The exact one/two-good-per-named-piece CEGAR was strengthened with complete
batch separation of self cores and up to 1,000 multi-owner families per
round. It restored 68 earlier cuts and learned 2,031 new cuts, for 2,099
replayable physical PI signatures. Its next check reached the declared
900-second limit and returned `UNKNOWN`:

- `allocated_e_form2_seven_endpoint_physical_pi_cegar_batchall_resume68.json`.

This is stronger negative-space evidence, not a bounded theorem or
countermodel. The cap-free analytic reductions above do not depend on a
terminal verdict from this search.

## Corrected payment shortcut

Profiles found against the minimized 425-clause core can force one, two, or
three payment holes in every EFX endpoint. Full PI auditing finds an omitted
generalized PI in every profile. They therefore refute only derivation of a
payment theorem from the minimized core, not the fully PI-free theorem. The
complete 46,683-cut decision resolves the valid two-hole question positively.

See `SEVEN_ENDPOINT_PAYMENT_STRENGTHENING_NO_GO_20260814.md` for the correction
record.

## Exact remaining implication

At a single saturated physical root-facing rank-three fixed-`U` record, prove
that each of the two cap-free terminal forms activates an already excluded GG
continuation:

1. a minimal one-hole Hall-deficient physical response family; or
2. a non-EFX seven-endpoint expansion whose failed comparisons are confined
   to the exact root/sacrifice pair `{r,d}`, followed after root retention by
   either the existing sole `d` wall or the unique `Z6` `{d,q}`/`M` branch.

Retaining the current strict root converts such an endpoint into exact
compensation prices for the paid pair `{q,s}`.  A disjoint compatible packet
pair closes the reassembly; failure is an explicit two-creditor Hall cut.
See `ROOT_RETENTION_QS_COMPENSATION_HALL_REDUCTION_LEMMA_20260814.md`.

The 394-clause proof core uses only endpoints `Z1,Z2,Z3,Z4,Z6`. Exact
root-retention accounting collapses `Z1`--`Z4` to the already named single
`d`-wall branch: in `Z3` the apparently affected `s` bundle becomes exactly
`X_s`, so it remains paid. Only `Z6` has a genuine second creditor, namely
`q`, and it carries the explicit compensation packet `M`. An exact PI-free
rational countermodel shows that `M` need not pay `q`. See
`FIVE_CORE_ENDPOINT_ROOT_RETENTION_LEDGER_LEMMA_20260814.md`.

The remaining `Z6` root-fixed face has now been exhausted, not merely
sampled. An independently audited exact PI-free profile has no EFX allocation
among all 6,411 complete allocations retaining `A+H` and using at most four
support edges. Hence neither a larger one-target donation nor arbitrary
coordinated nonroot redistribution can close the theorem while the current
root bundle is fixed. See
`ENDPOINT6_ROOT_FIXED_FOUR_EDGE_COMPLETION_NO_GO_20260814.md`.

The companion EFX-2 track has reduced the canonical whole-retired-packet
current-response branch to five exact compensation paths and their path-Hall
cut, with strict root overpayment closed and equality collapsed to a unique
base-restoration exchange. The missing bridge is now to map the one-hole/
two-debt objects above into that exact physical supplier-path contract—or
produce a full-premise countermodel. Generic payment bounds, packet-size caps,
and fixed endpoint topologies are no longer the right targets.

The smallest remaining bridge is now root-changing: in the sole genuine
second-creditor `Z6` row, derive a root/anchor-changing operation, a
well-founded change of saturated record, or response-mediated progress whose
final root support differs from `A+H`. A proof confined to the root-fixed face
is exactly refuted.

## Verification

- 27 focused tests pass in 2.87 seconds in the current verifier environment.
- Hidden-minimum audit: all negated implications UNSAT for arities 1--12.
- Hall audit: all 3x3 and 4x4 nonempty incidence graphs classified; 14,218
  inclusion-minimal deficiencies verified in one-hole normal form.
- Sharp `q,s`-paid producer: UNSAT with 46,683 PI clauses and seven endpoints.
- Sharp independent replay: UNSAT with 394 PI clauses and five direct
  endpoint/payment formulas.
- One-hole sharpness: exact PI-free rational countermodel, independently
  audited over all seven endpoints.
- Endpoint-6 root-fixed exhaustion: exact PI-free rational countermodel with
  zero EFX allocations in the independently regenerated 6,411-member menu.

## Claim boundary

Proved: the exact twelve-atom sharp `q,s`-paid/two-debt endpoint theorem;
cap-free hidden-minimum, physical Hall-lift, minimal-deficiency one-hole,
root/sacrifice observer localization, and root-retention compensation
identities.

Not proved: elimination of the remaining supplier-compatible two-creditor
Hall cut,
the universal saturated fixed-`U` four-edge theorem, four-agent additive EFX,
or general additive EFX.
