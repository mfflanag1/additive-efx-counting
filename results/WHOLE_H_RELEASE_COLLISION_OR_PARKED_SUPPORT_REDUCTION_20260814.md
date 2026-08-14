# Whole-`H` release collision-or-parked-support reduction

**Date:** 2026-08-14

**Status:** cap-free composition reduction; the parked-support terminal
`T_{L,perp}^*` remains open

**Subsequent endpoint-6 update:** the displayed parked-support alternative is
not terminal in this chart.  The second explicit probe `C_s` necessarily
reactivates `H`; see
`ENDPOINT6_TWO_PROBE_H_RELAY_CLOSURE_THEOREM_20260814.md`.  Generic
`T_{L,perp}^*` outside this endpoint-6 chart remains open.

## Input

Use the saturated physical allocated-`E` endpoint-6 state and the all-paid
complete candidate

\[
C_d=(A,Q,H+L+W,(E-L)+P).                         \tag{1}
\]

The current support state before (1) is

\[
Y=(A+H,Q,W,E;P).                                 \tag{2}
\]

Every named physical packet is nonempty.  Thus testing (1) releases the
nonempty packet `H` from the protected root `r` to the nonroot holder `d`.
Record each physical good of `H` in the monotone retired-support ledger with
its root/anchor label and the actual supplier edge `r->d`.

The all-paid decorated-response lemma says that (1) is complete EFX through
three edges, or its failure extracts a globally inclusion-minimal physical
core

\[
D\subseteq H+L+W                                  \tag{3}
\]

that is desired and common-safe at the actual allocation (1).

## Exact ledger dichotomy

Continue the deterministic fixed-`U` selector while retaining the full
signed record of (1).  Exactly one of the following occurs.

1. **Closing/progress outcome.** An EFX/lex endpoint, release-compatible PI,
   strict response/support/current-utility progress, or a valid anchor-label
   transition occurs.
2. **Retired-support collision.** Some extracted/tested response or failed
   normalized selector has support meeting `H`.  Its nonempty intersection
   with `H`, together with the recorded `r->d` retirement, current holder,
   recipient/source, floors, and failed realization, is the collision
   certificate required by `T_{L,times}^*`.
3. **Parked support.** Every member of the complete active selector/release
   pool is disjoint from `H`.  Because the ledger is nonempty, the exact
   repeat is `T_{L,perp}^*`, not the empty-ledger terminal `T_0^*`.

This is exhaustive.  If the first response (3) meets `H`, it supplies the
collision support immediately; if it is a new signed response, history grows
once, and an exact saturated repeat supplies the collision certificate.  If
it avoids `H`, inspect the remaining finite active pool.  A later hit enters
alternative 2; absence of every hit is exactly alternative 3 by definition.

## Composition with the collision theorem

The companion EFX-2 track proves `T_{L,times}^*` closed under the frozen GG
contract in commit
`34709c9ce22dbde23a5fa381a2ccea7898dfe1ca`.  Its new controlled
first-priority floor reset is load-bearing and still requires external
semantic review.  Subject to that review, alternative 2 cannot survive at a
saturated record.

Consequently the endpoint-6 whole-`H` release branch now has only one typed
recurrent obstruction:

\[
T_{L,perp}^*.                                     \tag{4}
\]

The earlier empty-ledger terminal is impossible in this branch because (1)
has already retired the nonempty packet `H`.  The broad repeated-response
gate has therefore been reduced to collision-free parked support.

## Why this does not yet prove the active theorem

The collision theorem eliminates a signed recurrent state; it does not by
itself certify that every intermediate endpoint is a complete EFX allocation
using the original three or four support edges.  More importantly, a
complete active pool may avoid `H` forever while operating on `L+W` and on
replacement bundles.  That is precisely `T_{L,perp}^*`.

To close the universal fixed-`U` theorem one must now prove, in this
endpoint-6 chart, that parked `H` can be activated or projected away without
losing payment, EFX safety, the fixed priority root, or the four-edge budget;
or produce a full-premise positive-additive countermodel to that assertion.

## Verification and claim boundary

`audit_whole_h_release_collision_or_parked_support.py` independently checks
the nonempty-ledger classification over every abstract active support family
on a finite universe, verifies that collision and parked alternatives are
disjoint and exhaustive, and records the exact imported collision-theorem
commit.

Proved: a cap-free, definition-faithful reduction of every saturated
endpoint-6 whole-`H` release recurrence to closing/progress,
`T_{L,times}^*`, or `T_{L,perp}^*`; exclusion of `T_0^*`; and, conditional on
the separately proved collision theorem, localization to `T_{L,perp}^*`.

Not proved: closure of `T_{L,perp}^*`, a complete EFX endpoint in every
physical branch, the universal rank-three fixed-`U` four-edge theorem, or
general additive EFX.
