# Current-wall backward-hole capture lemma

**Date:** 2026-08-13

**Status:** cap-free extension of backward hole pushing to the nonsingleton
current-only `d->r` wall; capture uncrossing remains

## Current-wall packet

Use the R3 near-perfect matching path beginning at target hole `d`.  Write
`W=Y_d`, let `P` be singleton charity, and normalize the base floor to
`F_d`.  Suppose the ordinary `d->q` core `Q` is nonsingleton.  By the
half-floor lift,

\[
 v_d(W)>\frac12F_d,
 \qquad v_d(T)=\tau_d(A)>v_d(W),                  \tag{1}
\]

where `T=A-g` and `g` is a least-`d` good of the root core `A`. Choose an
inclusion-minimal `D subseteq T` with `v_d(D)>v_d(W)`. Then
`tau_d(D)<=v_d(W)`, while `v_i(D)<=F_i` for every other observer `i`.
Thus `D` is an exact current-safe desired response core for `d`, and

\[
                         v_d(W+D)>F_d.            \tag{2}
\]

## Backward repair

Reverse the three path responses and initially give `P` to the unmatched
source.  Apply the same backward hole-pushing operation as in
`BACKWARD_HOLE_PUSHING_D_CAPTURE_LEMMA_20260813.md`: a target that would be
underpaid retains an inclusion-minimal part of its outgoing core, and
charity moves to the predecessor.  Retention creates no new transfer edge,
so the construction always uses the same three owner pairs and one charity
pair.

Every represented owner before `d` is repaired exactly as in that lemma.
When the hole reaches target-hole `d`, let `H subseteq D` be the part retained
by the physical root target.  The final `d` bundle is

\[
                         W+(D\setminus H)+P.       \tag{3}
\]

If (3) reaches `F_d`, every owner is paid.  Otherwise exact rearrangement
gives

\[
 v_d(H)>v_d(W)+v_d(D)+v_d(P)-F_d
       >2v_d(W)+v_d(P)-F_d
       >v_d(P)\ge0.                               \tag{4}
\]

Thus the current-only branch has the same terminating form as the ordinary
base branch: either an all-owner-paid four-edge candidate or one retained,
item-critical root packet with a strict quantitative capture certificate.
Unlike the earlier conditional statement, no conversion of `D` into a
base-desired core is required.

If `Q` is a singleton, it is itself an ordinary base-paying response packet,
so the original `d->q` backward-hole lemma applies.  Hence the singleton and
nonsingleton cases exhaust the payment status of the mixed wall.

## Exact remaining boundary

This theorem closes termination and owner payment, not complete EFX.  In the
paid branch an enlarged target may still violate an observer threshold and
must be converted to a saturated decorated-response exit.  In the capture
branch, (4) must be uncrossed with the generalized-PI full-margin capture of
the `d->q` core, or compressed into a different four-edge packet graph.

[`audit_current_wall_backward_hole_capture.py`](../tracks/parkability/audit_current_wall_backward_hole_capture.py)
independently verifies full-packet payment, the exact terminal identity, and
the strict positive capture implication in QF-LRA.
