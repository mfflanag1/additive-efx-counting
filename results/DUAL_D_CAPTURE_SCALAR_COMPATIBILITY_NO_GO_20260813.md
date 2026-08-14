# Dual-`d` capture scalar-compatibility no-go

**Date:** 2026-08-13

**Status:** exact cap-free no-go for a purely `d`-row contradiction; this is
not a full state or EFX countermodel

## Tempting but false route

The base `d->q` backward walk and the current `d->r` backward walk can each
terminate with a retained packet capturing the missing owner's payment
margin. It is tempting to add those two inequalities and seek a contradiction
using only `d`'s row. No such contradiction follows.

Normalize `F_d=1` and take the exact values

\[
 v_d(W)=\frac35,qquad v_d(P)=\frac1{10}.         \tag{1}
\]

Let the ordinary `q` core have two goods of value `3/5` each. Then

\[
 v_d(Q)=\frac65>1,qquad \tau_d(Q)=\frac35=v_d(W).
                                                               \tag{2}
\]

Retaining all of `Q` gives `H_q=Q` and satisfies the base-core terminal
capture

\[
 v_d(H_q)=\frac65>
 (v_d(Q)-1)+v_d(W)+v_d(P)=\frac9{10}.             \tag{3}
\]

Let a minimal current root core have value `v_d(D)=7/10` and retain a
subpacket `H_r` of value `1/2`. Then

\[
 v_d(W)+v_d(D-H_r)+v_d(P)=\frac9{10}<1,           \tag{4}
\]

equivalently

\[
 v_d(H_r)=\frac12>
 v_d(W)+v_d(D)+v_d(P)-1=\frac25.                 \tag{5}
\]

All values are positive, `W>1/2`, and `D>W`, so the half-floor premises and
both exact terminal capture inequalities coexist.

## Consequence

The dual-capture branch cannot be closed by a scalar inequality involving
only

\[
 F_d, v_d(W), v_d(P), v_d(Q), v_d(D),
 v_d(H_q), v_d(H_r).
\]

The next proof must use information discarded by this projection: another
owner's item-critical payment inequality, full observer safety, crossed base
support, generalized-PI closure, or the four-edge physical graph. This is a
route refutation, not evidence against the universal four-edge theorem.

[`audit_dual_d_capture_scalar_compatibility.py`](../tracks/parkability/audit_dual_d_capture_scalar_compatibility.py)
checks every displayed equality and strict inequality in exact rational
arithmetic and independently confirms QF-LRA satisfiability.
