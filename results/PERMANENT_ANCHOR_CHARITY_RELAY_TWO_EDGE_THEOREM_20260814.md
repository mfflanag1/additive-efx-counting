# Permanent-anchor charity-relay two-edge theorem

**Date:** 2026-08-14

**Status:** candidate cap-free reduction of the frozen saturated target to a
two-edge charity relay; the imported complete collision closure has an
unproved nonroot normalization-bypass branch

## Input

Use the current physical allocation `(Y,{p})` of a saturated root-facing
fixed-`U` state.  Let `r` be the first-priority root, `q` the permanent
anchor target, and

\[
 A\subseteq Y_q,
 \qquad v_r(A)>v_r(X_r)                           \tag{1}
\]

the permanent physical ordinary common-safe desired core on the anchor edge
`r->q`.  The singleton charity good `p` is positive.  Choose any nonroot
owner `d` (in the rank-three target, use its unique sacrifice-eligible
unmatched source).

No payment, response, residual, provenance, packet-size, or matching-rank
premise is imposed on the other owners.

## The two complete allocations

Move the anchor core from its current supplier `q` to its source `r`, retain
every other owner good at its current holder, and place `p` in turn at `r`
and `d`:

\[
\begin{array}{c|cccc}
 &r&q&d&j\\ \hline
R&Y_r+A+p&Y_q-A&Y_d&Y_j,\\
D&Y_r+A&Y_q-A&Y_d+p&Y_j.
\end{array}                                      \tag{2}
\]

Here `j` is the fourth owner; if `q=d`, the obvious union/difference in that
single row is used.  Both rows of (2) partition all goods and have empty
charity.  Relative to the original physical support state, their edge sets
are

\[
\begin{array}{c|c}
R&q\to r:A,\quad charity\to r:p,\\
D&q\to r:A,\quad charity\to d:p.
\end{array}                                      \tag{3}
\]

If `q=d`, these remain two distinct supplier-recipient pairs.  Thus either
endpoint uses exactly two edges and packet sizes are unrestricted.  By
positivity and (1),

\[
 v_r(R_r)>v_r(D_r)\ge v_r(A)>v_r(X_r).           \tag{4}
\]

## Stage, retire, and return

Test `R` first.  If it is EFX, (3)--(4) give the conclusion.  Otherwise use
the controlled first-priority reset at the actual allocation `R`, preserving
the immutable base, permanent anchor `A`, signed suppliers, and its globally
minimal failed response.

Now move only `p` from the staged root to `d`, obtaining `D`.  If `D` is
EFX, stop.  Otherwise reset at `D`, adopt its globally minimal failed
response, and record `r->d:p` as a retirement under the unchanged physical
anchor `A`.  The retirement-time reset floor of `d` is

\[
                         F_d=v_d(Y_d+p),          \tag{5}
\]

with `Y_d` in (5) interpreted as `Y_q-A` as well when `q=d`.

Retest `R` by returning the whole retired singleton from `d` to `r`.  The
root remains strict, all owners other than `d` weakly preserve their reset
bundles, and the unique reset-floor deficit is captured exactly:

\[
                         F_d-v_d(D_d-p)=v_d(p)>0. \tag{6}
\]

Canonical cancellation of that return leaves `p` at `d` and restores the
already failed allocation `D` and its adopted response.  The returned
allocation `R` is itself already known non-EFX from the first test.  At an
exact saturated repeat this supplies every datum of the
normalization-bypass/protected-floor `T_{L,times}^*` collision: the same
anchor, named packet, retirement supplier and holder, exact capture (6),
failed colliding selector, failed canonical normalization, and repeated
signed response.

Commit `34709c9ce22dbde23a5fa381a2ccea7898dfe1ca` claims to close that
subtype using the controlled reset.  The audit in
`NONROOT_NORMALIZATION_BYPASS_COLLISION_GAP_20260814.md` shows that its cited
dependencies do not cover the present possibility that `d` is the current
holder and the repeated normalized response avoids `{p}`.  Consequently the
last implication is not yet available: simultaneous non-EFX of `R,D`
reduces the target to that exact normalization-bypass gate.

## Consequence

Every state in the active frozen target has `(Y,{p})` and the permanent
ordinary root anchor (1).  The rank-three matching, hidden-minimum, Hall,
captured-support, R2/R3, and packet-compression branches are unnecessary for
this conditional closure.  They remain useful independent structural
results and fallback routes if the controlled reset is rejected.

## Verification and exact boundary

`audit_permanent_anchor_charity_relay_two_edge.py` checks both cases `q!=d`
and `q=d`, physical conservation, exact provenance edges, root strictness,
reset payment, deficit capture, and canonical cancellation.  It cannot
decide the proof-language question whether an arbitrary strict-root reset
allocation is an admitted `G0--G10` transition.  That question is exactly
the claim made by
`STRICT_FIRST_PRIORITY_FLOOR_RESET_ADMISSION_THEOREM_20260814.md` and is now
load-bearing for the active objective.

If the missing nonroot normalization-bypass branch is closed, this proves
the requested saturated root-facing rank-three fixed-`U` four-edge theorem,
in fact with two edges.  At present it is a sharp reduction, not a closure.
It does not prove the floor-reset extension, validate the BCFF-to-GG import,
close that bypass, prove all four-agent additive instances, or prove general
additive EFX.
