# Sacrificed-`H` relay admission lemma

**Date:** 2026-08-14

**Status:** cap-free admission of the second endpoint-6 probe into the
paid/sacrificed fixed-`U` candidate phase

## Setting

Let the first complete probe be

\[
C_d=(A,Q,H+L+W,X_s),                              \tag{1}
\]

where `A` is strict for the first-priority root `r`, `Q` pays protected owner
`q`, `X_s` pays `s`, and all four owners—including `d`—are weakly base-paid.
The packet `H` is nonempty and valuations are positive.

Move only `H` from `d` to `s`:

\[
C_s=(A,Q,L+W,H+X_s).                              \tag{2}
\]

The incremental operation is the single physical edge `d->s:H`.

## Theorem

Allocation (2) is a complete priority-valid candidate.  Owners `r,q` keep
their bundles, `s` strictly improves, and only the sacrifice-eligible owner
`d` can lose utility.  Exactly one of the following holds.

1. `C_s` is complete EFX.  It is then the required lexicographic endpoint.
2. `d` remains base-paid.  Then all four owners are paid at `C_s`, and every
   non-EFX failure enters the ordinary paid-splice current-response theorem.
3. `d` is below base at `C_s`.  The transferred packet strictly captures the
   entire loss of the earlier paid state above the base floor:

   \[
   v_d(H)>v_d((C_d)_d)-v_d(X_d)\ge0.              \tag{3}
   \]

   Thus (2) carries an exact protected-floor retired-packet capture, not an
   untyped unpaid candidate.

## Proof

Completeness is unchanged by transferring `H`.  The first two owners are
unchanged and

\[
v_s((C_s)_s)=v_s(X_s)+v_s(H)>v_s(X_s)             \tag{4}
\]

by positivity.  Hence the strict earlier root certificate survives, `q`
stays paid, `s` is strict, and `d` is the unique possible payment hole.  An
EFX instance therefore strictly beats the globally maximal base even if `d`
is below base.

If `d` remains paid, branch 2 is immediate.  Otherwise

\[
v_d((C_s)_d)<v_d(X_d)
\]

and the identity

\[
v_d(H)=v_d((C_d)_d)-v_d((C_s)_d)                  \tag{5}
\]

gives (3) strictly.  These two payment cases are disjoint and exhaustive.

## Endpoint-6 ledger consequence

After `C_d` records `H` as retired at its paid holder `d`, the admitted
candidate (2) is precisely a later attempted consumption of `H`.  Canonical
cancellation of its only incremental edge restores `C_d`.  Therefore:

- branch 2 plus non-EFX gives the repeated paid-state
  normalization-bypass certificate;
- branch 3 gives the protected-floor capture certificate; and
- both are typed `T_{L,times}^*` inputs after exact response/state
  saturation.

This proves the admission fact left open in the two-probe premise audit.  It
does not independently close `T_{L,times}^*`, audit the whole fixed-`U`
dependency graph, or prove general EFX.

## Verification

`audit_sacrificed_h_relay_admission.py` checks conservation and the one-edge
support identity, and independently negates (3) in QF_LRA under the unpaid
branch.  Every negation is UNSAT.
