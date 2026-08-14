# Paid-cycle charity-to-sacrificed lemma

**Date:** 2026-08-13

**Status:** cap-free three-/four-edge functional payment closure; only the
bare sacrificed-owner deficit and observer safety remain

## R2 two-cycle

Reverse the paid response cycle

\[
 r\to q\to r
\]

and give singleton charity `{p}` to `d`.  Owners `r` and `q` receive desired
cores and are strictly paid.  Owner `s` keeps all of its current paid bundle.
Owner `d` keeps all of `W` and receives `p`.

The transfer graph is

\[
 q\to r,\qquad r\to q,\qquad
 \mathrm{charity}\to d,                           \tag{1}
\]

so it is functional and uses only three edges.  No packet from `d` needs to
be sent to the already-paid owner `s`.

## R3 three-cycle

Reverse the complete paid response cycle

\[
 r\to q\to s\to r
\]

and again give `{p}` to `d`.  The three cycle owners receive desired cores,
and `d` keeps `W+p`.  The transfer graph is functional and uses four edges.

## Common exact separator

In both forms every represented owner is paid.  The only possible payment
failure is

\[
 v_d(W)+v_d(p)<v_d(X_d).                           \tag{2}
\]

Thus each exact response form has three canonical functional payment
candidates: two shortest sacrificed-source paths, whose respective endpoint
margins may fail, and the paid-cycle candidate, whose `d` margin may fail.
A proof must show that all three scalar failures force a saturated exit, or
switch to another flexible functional topology.

Once any candidate is paid, observer failure yields a complete decorated
current response by the paid-splice lemma.

## Verification and boundary

[`audit_paid_cycle_charity_to_sacrificed.py`](../tracks/parkability/audit_paid_cycle_charity_to_sacrificed.py)
checks both constructions, exact atom conservation, functionality, edge
counts, represented-owner payment, and the common `d` margin identity in
QF-LRA.

This lemma does not exclude (2), prove observer safety, or prove the
universal functional/four-edge theorem.
