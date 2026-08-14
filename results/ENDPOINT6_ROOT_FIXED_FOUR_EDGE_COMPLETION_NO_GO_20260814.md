# Endpoint-6 root-fixed four-edge completion no-go

**Date:** 2026-08-14

**Status:** independently audited exact PI-free bounded countermodel; every
root-retaining completion is excluded in the declared cell

## Exhaustive selector

Fix the current protected root bundle `A+H`.  Assign every remaining one of
the nine named atoms to `q,d,s`, require empty charity, and retain exactly the
allocations whose directed supplier-to-recipient support set has size at most
four.  This produces 6,411 complete allocations.

The menu contains arbitrary coordinated redistribution among all three
nonroot owners.  It strictly contains the seventeen one-target-to-`q` repairs
and is not restricted to trees, single packets, or a moved-good radius.

The tested strengthening was:

> If endpoint `Z6` is EFX and pays `q,s`, but exact current-root retention
> leaves `q` below base, then either there is a generalized PI or some one of
> the 6,411 root-fixed four-edge allocations is EFX.

## Exact countermodel

The allocation/PI CEGAR starts with 46,683 valid generalized-PI exclusions.
It adds 160 newly discovered PI-family cuts and five lazy allocation cuts,
then terminates at an exact positive-rational profile with:

1. the complete allocated-`E` form-2 premises;
2. no generalized PI under the exact complete oracle;
3. endpoint `Z6` complete EFX and paying `q,s`;
4. the root-retained `q` target below base; and
5. zero EFX allocations in the entire 6,411-member root-fixed menu.

The producer is `allocated_e_form2_endpoint6_root_fixed_completion_cegar.json`.
`audit_allocated_e_endpoint6_root_fixed_completion_countermodel.py`
independently fixes the rational master, reruns the complete generalized-PI
oracle, reconstructs all 6,411 allocations from the support ledger, and
checks each allocation by direct Fraction arithmetic.  The audit is
`allocated_e_form2_endpoint6_root_fixed_completion_cegar_audit.json`.

## Consequence

The final universal operation cannot preserve the exact current root bundle.
It must instead do at least one of:

1. change or release the root/anchor packet;
2. move first to a different saturated GG record with a well-founded label
   decrease; or
3. use a response-mediated construction whose final root support is not
   `A+H`.

This converts the companion EFX-2 root-anchor work from an optional repair
into a logically necessary ingredient.  More enumeration inside the
root-fixed face cannot close the theorem.

## Claim boundary

Refuted: every complete at-most-four-edge endpoint that retains the current
root bundle in the exact twelve-atom endpoint-6 cell.

Not refuted: a root-changing/anchor-changing completion, a different GG
record, the cap-free physical theorem, four-agent EFX, or general EFX.
