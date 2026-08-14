# Generalized-PI canonical CEGAR gate

**Date:** 2026-08-13

**Status:** exact verifier and two-sided bounded search; old residual cell
eliminated, allocated-support repair in progress

## Canonical completeness

Fix a base allocation `X`.  A generalized champion edge from source `i` to
target `j` may be represented by its desired assigned core `A`.  Its incoming
and released packets have the canonical form

\[
 H=A\setminus X_j,\qquad S=X_j\setminus A.       \tag{1}
\]

It is enough to enumerate inclusion-minimal common-safe desired cores.  If
`B subseteq A` is an inclusion-minimal desired core, replacing `A` by `B`
shrinks `H` and enlarges `S`.  Thus it preserves pairwise disjointness of all
incoming packets and cannot destroy availability from base charity or from a
packet released by another selected edge.  Every generalized PI cycle
therefore has a canonical witness using inclusion-minimal cores.

For a fixed canonical witness, incoming disjointness and release coverage
are combinatorial. Its valuation-dependent content is exactly the
conjunction that each displayed core is common-safe and strictly desired by
its source.  Negating that conjunction is consequently a sound QF-LRA CEGAR
cut: it removes the witnessed PI cycle without excluding any profile in
which at least one of its champion edges is absent.

The closed disjoint-core characterization sharpens this further. A
generalized PI cycle exists exactly when some nonempty owner set has one
pairwise-disjoint minimal desired core per source and every good in those
cores is base-owned inside the set or by charity. Once the core family is
fixed, the cyclic target order is arbitrary. CEGAR signatures and cuts are
therefore deduplicated by `(source, desired core)` alone; retaining target
labels would install the same symbolic cut up to 24 times.

`find_generalized_pi_cycle.py` exhausts all minimal desired cores and all
owner cycles of lengths one through four.  The finder now takes the actual
base allocation as an argument; this is load-bearing because changing a good
from charity to an owner changes packet availability even when every value
is unchanged.  `run_generalized_pi_named_selector_cegar.py` and
`run_allocated_e_capture_rank_three_cegar.py` convert its witnesses into
exact symbolic cuts.

**Resume correction.** The allocated-support driver's historical resume
loader reads only witnesses embedded in the immediate source file; it does
not recursively traverse that file's own resume link. This is sound for an
individual run but can silently weaken a multi-generation continuation.
`flatten_allocated_e_cegar_resume.py` now verifies every linked SHA-256,
recursively collects the chain, deduplicates canonical signatures, and emits
one lossless resume payload. Applied to R3, it restored 23,847 distinct cuts,
444 more than the last run's one-hop effective set. No convergence claim may
use a chained resume without this flattening or an equivalent recursive
audit.

## Eliminated cell

In the former full-capture and two-bare cells, the required paid core
`E={e,l}` has `X_s={e,p}` and `l` in base charity.  It is already the
length-one PI cycle `s -- {l}|{p} --> s`.  Both forms are UNSAT after adding
only the negation of this edge.  Deletion-minimal core extraction returns
exactly that one assumption in each form.

This corrects the earlier ordinary-PI-free selector refutations: all four
counterprofiles have independently audited generalized self-PI witnesses.
The bounded selector becomes vacuously true in that cell because the cell is
not saturated.

## First nonvacuous repair

The allocated-`E` repair changes base provenance while keeping the physical
support state and rank-three response interface:

- `l`, the external part of `E`, is base-owned by sacrificed owner `d`;
- `j`, the external part needed by `d`'s `Q` response, is base-owned by `q`;
- only `gr` remains in base charity.

Hence neither required core is a charity-only self splice. Generalized PI
now depends on release of allocated support. Form R2 is exactly UNSAT after
14,249 effective higher-order cuts and an independent rebuild; its
higher-order contradiction compresses to a stable 32-family deletion-minimal
layer. Form R3 remains unresolved: after the original 30-round limit, a
losslessly flattened continuation reached its own 20-round limit with 28,820
distinct cuts and continued to expose fresh generalized-PI families. The
final lossless resume is
`allocated_e_capture_form2_pairlinear_flattened_resume_v2.json`. This is the
intended captured-support dependency gate rather than a false unallocated-
good countermodel; an iteration limit is not scientific convergence.

## Exact outcomes and boundary

For either repaired response form:

- `UNSAT` after exhaustive CEGAR convergence is a bounded-atom exclusion;
- `SAT_NO_GENERALIZED_PI` is a genuine generalized-PI-free profile for the
  declared necessary premises, but is not yet a saturated countermodel;
- an iteration limit or solver timeout is unresolved.

Even a converged bounded result does not prove the cap-free four-edge
theorem.  Its purpose is to expose the shortest release-dependency inequality
or exact profile that must be lifted into the full signed/saturation record.
