# Root global supplier-star floor-admissibility gap

**Date:** 2026-08-14

**Historical verdict:** the proposed complete-current-exterior supplier-star
was not admissible while it silently retained the old positive nonroot
floors.

**Resolution update (2026-08-14).** The gap is now repaired by
`STRICT_FIRST_PRIORITY_FLOOR_RESET_ADMISSION_THEOREM_20260814.md`. It
explicitly resets every later auxiliary floor at the tested allocation,
retains the strict first-priority root certificate, recomputes every EFX
comparison, and does not count the reset itself as progress. The singleton
specialization in
`ROOT_SINGLETON_SUPPLIER_STAR_FLOOR_RESET_CLOSURE_THEOREM_20260814.md`
then gives strict packet progress and closes the root-holder branch. The old
unreset argument below remains invalid and is retained as correction
provenance.

## Exact mismatch

The frozen charge-or-anchor contract requires every tested candidate to
preserve its declared protected floors.  The supplier-star candidate assigns

\[
 Z'_r=G\setminus T,\qquad Z'_u=T,
\]

and gives every other nonroot owner the empty bundle.  Hence any sacrificed
owner `a` with declared floor `F_a>0` receives

\[
 v_a(Z'_a)=v_a(\varnothing)=0<F_a.
\]

Positive additivity makes the zero on the left exact.  Root strictness is
enough to make an **EFX endpoint** a lexicographic improvement, but it does
not by itself license a non-EFX intermediate allocation that violates the
frozen floor vector.  Nor does naming every physical supplier establish the
missing floor premise.

The current proof does not show that every sacrificed owner has zero typed
floor, and it does not identify an existing `G0--G10` operation that resets
those floors before adopting the supplier-star allocation and its extracted
response.  Therefore the assertion that every failed test strictly reduces
the live packet coordinate is not yet composed into the exact recurrent
state.

## What remains valid

Conditional on a valid controlled floor reset or a floor-paying supplier
star, the root theorem correctly derives complete-exterior dominance, and
the retained old root core gives the exact contradiction

\[
 v_r(k)>v_r(G\setminus X_r)\ge v_r(T_q+f)
 >v_r(X_r)\ge v_r(k).
\]

The nonroot desire-free envelope descent is unaffected.  The defect is only
the admission of the root-side operation that derives the first strict
inequality.

## Smallest missing operation, now supplied

Prove one of the following, without changing the frozen theorem:

1. a controlled lexicographic sacrifice/floor-reset operation that is an
   actual admissible signed-state transition and makes every later floor
   release explicit;
2. a supplier-closed compensation of every positive-floor donor while the
   root retains the strict margin and every resulting wall has proper
   retired-packet support; or
3. a different root/anchor exchange deriving the needed packet reduction or
   contradiction without emptying a positive-floor owner.

The new controlled floor-reset theorem supplies alternative 1. The reset is
recorded explicitly, and the singleton-star response geometry supplies the
separate strict progress required by that theorem.

## Subsequent localization

`ROOT_RETIRED_PACKET_OLD_ANCHOR_CRITICAL_LOCALIZATION_THEOREM_20260814.md`
first narrowed the gap without using the global supplier star. Its corrected
version uses a clean controlled release rather than a historical-source
return. The later floor-reset theorem closes even the residual cell

\[
 \varnothing\ne K\subseteq
 \{g\in D_r:v_r(D_r-g)<v_r(X_r)\}.
\]

so critical old-anchor payment is no longer a live `T_{L,times}^*` gate.
