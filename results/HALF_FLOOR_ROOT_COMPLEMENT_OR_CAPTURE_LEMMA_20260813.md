# Half-floor root-complement-or-capture lemma

**Date:** 2026-08-13

**Status:** cap-free packet split for the current-only root wall; simultaneous
capture/edge compression remains

## Statement

Use the hypotheses and notation of the half-floor current-wall lift. In the
nonsingleton-`Q` branch,

\[
 \frac12F_d<v_d(W)<\tau_d(A).                    \tag{1}
\]

Let `C` be any nonempty packet of the root core `A` committed to another
response source, and put

\[
                         R=A\setminus C.          \tag{2}
\]

Then the following useful alternative holds:

1. **complement payment:** `v_d(W+R)>=F_d`; or
2. **strict capture:**

   \[
   v_d(C)>v_d(A)+v_d(W)-F_d>2v_d(W)-F_d>0.        \tag{3}
   \]

Indeed, failure of branch 1 gives

\[
 v_d(R)<F_d-v_d(W),
\]

and subtraction from `v_d(A)` gives the first inequality in (3). Since
`v_d(A)>tau_d(A)>v_d(W)`, the other inequalities follow.

## Observer safety of the complement

Because `C` is nonempty, `R` is a proper subset of `A`. For every observer
`i`, choose any removed good `c in C`. Then

\[
 v_i(R)\le v_i(A-c)\le\tau_i(A)\le F_i.          \tag{4}
\]

Thus the complete complement—not merely an inclusion-minimal response
core—is full-value base-safe for every observer. In branch 1 it may be sent
to `d` as one unrestricted packet while `d` retains `W`.

## Role in the four-edge proof

This turns overlap with the lifted `d->r` packet into a quantitative fork.
Whenever the packet already committed from the root does not prevent the
complement from paying `d`, owner payment and incoming-packet safety close.
Every survivor forces that committed packet to absorb more than the positive
half-floor slack `2v_d(W)-F_d`.

The lemma does not show that two supplier-recipient edges out of the root fit
the final four-edge topology, pay the owner receiving `C`, or make the
enlarged target `W+R` EFX-safe. Nor does (3) alone make `C` desired by `d`.
The remaining universal obligation is to combine this strict capture with
the `d->q` base-core capture and the saturated response/observer exits, or
to exhibit a full-premise countermodel realizing both captures.

[`audit_half_floor_root_complement_or_capture.py`](../tracks/parkability/audit_half_floor_root_complement_or_capture.py)
independently verifies the alternative and cross-observer safety in exact
QF-LRA.
