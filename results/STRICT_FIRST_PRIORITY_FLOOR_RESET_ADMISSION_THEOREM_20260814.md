# Strict first-priority floor-reset admission theorem

**Date:** 2026-08-14

**Status:** cap-free admission of an explicitly recorded later-floor reset at
a strict first-priority root; the reset itself is not finite progress

## Exact priority input

Let `X` be the globally fixed-priority lexicographically maximal EFX base,
let `r` be its first-priority owner, and put

\[
 x=v_r(X_r).
\]

Let `Y` be any explicitly specified feasible allocation with exact current
suppliers and releases such that

\[
 v_r(Y_r)>x.                                     \tag{1}
\]

No EFX or old nonroot-floor premise is assumed for `Y`.

## Controlled floor reset

Recompute every EFX comparison at the actual allocation `Y` and replace the
auxiliary current floor vector by

\[
 F_i^Y=v_i(Y_i)\qquad(i\in N).                  \tag{2}
\]

Retain separately the immutable base certificate `(X,r,x)`, the complete
physical anchor label, the full signed transfer decoration, and every
retirement/collision record. If the physical root support changed in
forming `Y`, record that change rather than calling it the old anchor.

Equation (2) is an actual controlled reset, not an assertion that `Y`
preserves the previous floor vector. Every owner pays her new current floor
with equality, while (1) retains the only priority coordinate needed to
beat `X`: the first coordinate. The reset may lower any later auxiliary
floor, including to zero, but never lowers the protected root below `x`.

The state space remains finite. For a fixed finite instance each `F_i^Y` is
the value of one of finitely many bundles in row `i`; the allocation, anchor,
supplier, response, and ledger labels are also finite. A floor reset alone
is therefore not advertised as progress and may not be counted merely
because its numerical vector changed.

## Endpoint and response audit

If `Y` is EFX, (1) makes its fixed-priority utility vector lexicographically
larger than that of `X`, contradicting global maximality regardless of the
later owners' utilities.

If `Y` is not EFX, some source strongly envies a target. A one-good deletion
of that target is desired relative to the source's actual assigned bundle.
Choose, among every source and every desired subset of every target, a
nonempty subset `D` of globally minimum cardinality. Then `D` is safe at
`Y`: if an observer strongly envied `D`, deleting one good would give a
strictly smaller desired subset, contradicting minimality. Thus the reset
enters the ordinary exact-response interface with

\[
 v_i(D)>F_i^Y=v_i(Y_i)                           \tag{3}
\]

for its source `i`, and with all supplier, target, and release labels taken
from the actual allocation `Y`.

The reset does not claim that a response is progress. Progress must be
proved separately from physical support, a new response/anchor coordinate,
or another contracted potential. Every later transition in this strict-root
phase must either keep the root above `x` or explicitly execute a different
root/anchor outcome; lowering later floors cannot substitute for that test.

## Admissibility conclusion

The controlled reset is a valid extension of the exact signed-state
transition registry whenever all of the following are present:

1. a fully specified feasible allocation `Y`;
2. current suppliers and destinations for every moved good;
3. the strict first-priority certificate (1);
4. the recomputed floor vector (2) and all actual EFX comparisons; and
5. a separate physical progress argument for every non-EFX continuation.

This supplies precisely the operation left open by
`ROOT_GLOBAL_SUPPLIER_STAR_FLOOR_ADMISSIBILITY_GAP_20260814.md`. It does not
infer PI from a supplier star, erase a retirement label, or preserve an old
nonroot protected floor.

## Claim boundary

This theorem admits recorded later-floor sacrifice during a strict-root
phase. It does not by itself construct a strict allocation, prove packet
progress, close a supplier component, close `T_{L,times}^*`, GG, four-agent
EFX, or general additive EFX.
