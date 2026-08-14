# External-Hall finite-decision nonvacuity gate

**Date:** 2026-08-14

**Status:** the exact star/fork menu is executable, but every existing
full-PI twelve-atom decision is vacuous or already excluded before the menu
is tested

## Exact menu now available

The `2x1` external Hall star and `3x2` fork classifications have now been
composed into a direct finite decision driver.  For each of the two surviving
rank-three response forms it permits every complete nonempty-owner allocation
supported by any edge-compatible star or fork topology, rather than fixing
the response packet contents.

The exact support counts are:

| form | star signatures | fork signatures | star topologies | fork topologies | union |
|---|---:|---:|---:|---:|---:|
| `R2` | 15 | 78 | 13 | 46 | 53 |
| `R3` | 15 | 78 | 15 | 60 | 60 |

Every topology has at most four original-supplier/recipient pairs, including
the charity edge.  The decision driver fails closed: it checks satisfiability
of the premise cell before negating a single EFX endpoint.

## Calibration failure of the legacy master

In both response forms, the legacy twelve-atom master is SAT after excluding
ordinary PI but becomes UNSAT immediately after generalized self-PI is
excluded.  No Hall endpoint is needed for the contradiction.  The cause is
the already documented forced self-edge

\[
                 s\xrightarrow{\{l\}\mid\{p\}}s.
\]

Consequently an UNSAT answer obtained by adding the Hall menu to that master
is vacuous: it does not prove that a saturated profile has a star/fork EFX
endpoint.  The new driver records `vacuous_premise_unsat` rather than
promoting such a result.

## Why the allocated-support repair does not decide this gate

The later allocated-`E` atomization removes the forced charity self-edge by
making `l` base-owned by the sacrificed owner.  It is nonvacuous at the first
PI layers, but it has already been eliminated independently:

- form `R3` is inconsistent at its repaired master layer; and
- form `R2` is UNSAT after the independently replayed 14,249 generalized-PI
  family cuts in
  `ALLOCATED_E_FORM_R2_GENERALIZED_PI_EXCLUSION_THEOREM_20260813.md`.

Those are useful bounded exclusions, but again no surviving saturated profile
remains on which the external Hall menu can be tested.  The existing
functional-cover and two-survivor solvers therefore cannot answer the live
universal question by being patched with the 156 fork signatures.

## Exact cap-free target exposed by the audit

The next proof must work before a fixed atomization kills the premise cell.
For an overflowing external Hall response, follow the base supplier of every
retained or proper-incoming part.  The required **alternating external-Hall
closure-or-cancellation lemma** is:

> At a saturated signed state, this supplier walk either introduces a new
> response/core/release coordinate, closes a pairwise-disjoint physical
> desired-core family and hence generalized PI, or reaches the unmatched
> owner with enough whole-packet exhaustion/return to satisfy one of the exact
> `2x1` or 156 `3x2` edge-cancellation signatures.

The first outcome is excluded by saturation, the second by PI-freeness, and
the third is the only route that can yield the desired four-edge endpoint.
The remaining load-bearing work is to prove that observer safety and the
first-priority root margin survive the supplier walk.  Merely showing that
owner labels repeat is insufficient; exact packet and release labels must
repeat or strictly refine.

## Claim boundary

Proved here: exact star/fork topology generation and a fail-closed
nonvacuity audit showing that the legacy full-PI finite decision cannot prove
the live Hall theorem.

Not proved: the alternating closure-or-cancellation lemma, a nonvacuous
full-saturation finite model, the rank-three fixed-`U` four-edge theorem, or
general additive EFX.
