# Allocated-E two-payment-hole seven-endpoint theorem

**Date:** 2026-08-14

**Status:** dual-verified exact bounded theorem

**Sharpening.**  `ALLOCATED_E_QS_PAID_TWO_DEBT_SHARP_THEOREM_20260814.md`
proves that the endpoint can always be chosen to pay both `q` and `s`, so
the two possible holes are exactly localized to `{r,d}`.  It also gives an
independently audited exact PI-free countermodel to reducing this to one
hole while retaining both payments.

## Theorem

In the exact twelve-atom allocated-`E` form-2 master, every profile satisfying
the complete recorded pool of 46,683 generalized-PI exclusions has one of the
seven explicit complete EFX endpoints at which at least two of the four
owners weakly retain their normalized base utility. Equivalently, the EFX
endpoint has at most two payment holes.

In particular, every fully generalized-PI-free profile in the declared cell
has such an endpoint, because it satisfies every valid PI exclusion in the
recorded pool.

## Producer

`allocated_e_form2_seven_endpoint_two_hole_full_pi_decision.json` rebuilds the
allocated-`E` form-2 master, restores all 46,683 closed disjoint-core clauses
from the independently validated all-allocation CEGAR chain, and negates the
seven conjunctions

\[
\text{complete EFX}(Z_k)\ \wedge\
\#\{i:v_i((Z_k)_i)\ge v_i(X_i)\}\ge2.
\]

Z3 5.0.0 returns UNSAT in 42.8 seconds.

The producer SHA-256 is
`9ca94dfd651b730ad193d14fecfab8357d8d593bdafd59f9de9dbaab1b9b9845`.

## Interpretation

The minimized 425-clause core is insufficient for this strengthening and
admits exact profiles with three payment holes. Every such profile contains
another generalized PI. Restoring the complete PI pool eliminates the
shortcut models and proves that two holes suffice in the fully PI-free
bounded cell.

This interfaces directly with the cap-free two-hole residual-split and
matching-hole machinery. It does not by itself show that the physical
expansion of the selected endpoint is EFX, or that its two payment holes can
always be repaired without changing the endpoint.

`TWO_HOLE_ENDPOINT_PHYSICAL_FAILURE_LOCALIZATION_LEMMA_20260814.md` supplies
the exact cap-free next step: after physical expansion, either the endpoint
is EFX, a paid observer failure exposes an ordinary base response, or every
unsafe comparison is sourced by the at-most-two payment-hole owners.

## Core extraction and independent replay

The direct full independent replay of all 46,683 nested-minimum predicates
reached its declared 900-second limit with `UNKNOWN`. Assumption-core
extraction then reduced the producer certificate to 1,966 PI clauses while
retaining all seven endpoints:

- 638 three-owner clauses: 353 on `{d,q,r}`, 129 on `{d,q,s}`, 107 on
  `{d,r,s}`, and 49 on `{q,r,s}`;
- 1,328 four-owner clauses.

The core is
`results/allocated_e_form2_two_hole_unsat_core.json`, SHA-256
`162fe57973b85a7098415e482895ba543d64ffe784c494725864fdf417f29e67`.

`tracks/parkability/audit_allocated_e_two_hole_endpoint_unsat.py` independently
rebuilt those 1,966 PI predicates with literal tail minima, encoded endpoint
EFX through direct deletion inequalities, and counted owner payments directly.
With a different seed it returned UNSAT. The audit record is
`results/allocated_e_form2_seven_endpoint_two_hole_compact_core_audit.json`,
SHA-256
`04526ab39d6ae8d0cad656c496a6717343c7b6ead124eb475325968d19420835`.

## Claim boundary

Proved with two exact formula encodings: the two-payment-hole strengthening in
the exact twelve-atom form-2 cell.

Not proved: the same strengthening for arbitrary physical packet sizes,
repair of both holes within four physical supplier edges, the universal
fixed-`U` theorem, four-agent EFX, or general EFX.
