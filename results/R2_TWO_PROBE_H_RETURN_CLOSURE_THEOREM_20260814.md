# R2 two-probe `H`-return closure theorem

**Date:** 2026-08-14

**Status:** cap-free closure of the named-provenance proper-residual R2
branch, conditional on semantic acceptance of `T_{L,times}^*`; arbitrary
captured-support provenance remains open

## Input branch

Use the proper-residual named-provenance hypotheses of
`ROOT_FACING_TWO_EDGE_STRICT_PAYMENT_COMPLETION_LEMMA_20260813.md`:

- physical support `Y=(A+H,Q,W,E;P)` with nonempty `H,P`;
- strict represented cores `A,Q,E`;
- `Q=J+(K-J)+Q_0` with nonempty `Q_0`;
- `X_d=H+(K-J)+G_q`;
- `d(J+(K-J)+H)>d(X_d)`; and
- `d(W)>=tail_d(Q)`.

Those premises imply

\[
                         v_d(W+H)>v_d(X_d).        \tag{1}
\]

No packet-size or value bound is used.

## Two probes

Test, in order,

\[
\begin{aligned}
C_d&=(A,Q,W+H,E+P),\\
C_r&=(A+H,Q,W,E+P).
\end{aligned}                                    \tag{2}

Both are complete.  Relative to `Y`, their actual support edges are

\[
\begin{array}{c|c}
C_d&r\to d:H,\quad charity\to s:P,\\
C_r&charity\to s:P.
\end{array}                                      \tag{3}

Thus either EFX endpoint uses at most two edges.  Relative to `C_d`, the
second probe changes only

\[
                         H:d\longrightarrow r.    \tag{4}

\]

Cancelling (4) returns exactly `C_d`.

## Payment and one-hole admission

The two-edge strict-payment lemma makes every owner strict at `C_d`.
At `C_r`, owners `r,q,s` are strict: the root receives `A+H`, `q` receives
`Q`, and `s` receives `E+P`.  Only `d` can be below its base floor.

If `d` remains paid, `C_r` is another all-owner-paid probe.  If `d` is
unpaid, then

\[
\begin{aligned}
v_d(H)
 &=v_d((C_d)_d)-v_d((C_r)_d)\\
 &>v_d((C_d)_d)-v_d(X_d)\ge0.                   \tag{5}
\end{aligned}

Hence `H` strictly captures the entire payment deficit created by its
return.  The second probe is therefore an admissible priority-valid
one-hole candidate, not an untyped unpaid allocation.  If it is EFX, the
strict first-priority root beats the globally maximal base regardless of
`d`'s payment status.

## Retired-packet collision

If `C_d` is EFX, stop.  Otherwise its all-paid failure yields the exact
globally minimal current-safe decorated response.  The transition
`Y -> C_d` removes the nonempty packet `H` from the protected root, pays its
new holder `d`, and records `H` in the retired-support ledger.

Now test `C_r`.  Equation (4) is an active whole-packet return to the
protected root.  Its canonical cancellation restores precisely the already
failed paid probe `C_d` and its signed response.  If `C_r` is not EFX, then:

- a paid failure gives the normalization-bypass repeated-response branch;
- an unpaid `d` gives the protected-floor capture branch (5);
- a release or observer failure retains the same physical packet and signed
  candidate; and
- a first new response record is strict finite history progress, while its
  first exact repeat enters the same collision component.

At saturation these are exactly the root-holder/return cases of
`T_{L,times}^*`, not the parked subtype: the second declared probe consumes
the whole named retired packet and places it back at the root.  Commit
`34709c9ce22dbde23a5fa381a2ccea7898dfe1ca` closes that collision subtype by
the controlled first-priority floor reset, subject to its independent
semantic review.

Consequently, under that imported theorem, one of `C_d,C_r` is a complete
physical EFX allocation using at most two packet-transfer edges.

## Consequence and boundary

This closes R2 whenever the proper residual and provenance identity needed
for (1) hold.  It also explains the two-edge endpoints found in the enriched
twenty-one-role exact search: they are instances of the first probe.

It does not derive `Q-K!=empty`, align arbitrary captured `d` support with
`H+(K-J)+G_q`, handle `K=Q`, convert a dropped-owner/Hall capture from the
role-compression theorem, independently validate the controlled floor reset,
or prove the full fixed-`U` objective.
