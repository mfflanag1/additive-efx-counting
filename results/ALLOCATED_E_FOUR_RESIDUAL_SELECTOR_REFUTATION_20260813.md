# Allocated-E four-residual selector refutation

**Date:** 2026-08-13

**Status:** exact bounded no-go; generalized PI and unrestricted four-edge
escapes remain

## Refuted selector

In the allocated-support repair of response form R3, retain the represented
cores `A,Q,E` and the sacrificed bundle `W`. Consider the four simplest
complete placements of residual packet `H` and charity token `p`:

1. retain `H` at `r`, give `p` to `d`;
2. give both `H,p` to `d`;
3. give `H` to `s` and `p` to `d`;
4. give `H` to `d` and `p` to `s`.

There is an exact positive-rational profile satisfying the repaired
twelve-good rank-three premises, every generalized self-PI exclusion, all
110 fixed-core-anchored exclusions, and all 11,298 closed two-owner core
exclusions, in which none of these four allocations is EFX.

Therefore complete self-/pair-PI-freeness does not reduce simultaneous
capture to one residual placement inequality.

## What survives

The profile is not a saturated countermodel:

- it has 3,233 closed disjoint desired-core families, 151 on three owners
  and 3,082 on all four owners;
- it has 197 complete EFX allocations within four support edges—22 using
  three edges and 175 using four; and
- its three-edge escapes use dynamic bilateral `d`/represented-owner
  exchanges or a short compensation path, rather than the four frozen
  residual endpoints.

Thus the no-go points in the same direction as the cap-free crossed-import
lemma: the remaining selector must follow the contested support dependency,
not assign `H,p` independently of it.

## Verification and boundary

`audit_allocated_e_four_residual_refutation.py` independently re-evaluates
the exact rational profile, verifies base normalization/EFX, proves all four
endpoints non-EFX by explicit observer/target witnesses, exhausts canonical
closed core families, and enumerates every complete allocation within four
support edges.

This is a bounded selector counterexample. It is not generalized-PI-free,
not a full saturated-state countermodel, and not a counterexample to the
four-edge theorem or additive EFX.
