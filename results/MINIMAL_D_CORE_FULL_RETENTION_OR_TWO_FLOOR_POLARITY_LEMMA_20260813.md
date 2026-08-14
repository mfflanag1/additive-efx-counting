# Minimal `d`-core full-retention or two-floor polarity lemma

**Date:** 2026-08-13

**Status:** cap-free scalar classification of the terminal backward-hole
capture; contradiction with both root walls remains open

## Input

Let `D` be an inclusion-minimal common-safe desired core for sacrificed owner
`d` at floor `F_d`:

\[
              v_d(D)>F_d,
 \qquad \mu_d=v_d(D)-F_d>0.                       \tag{1}
\]

Suppose backward hole pushing leaves a retained packet `H subseteq D` and
the terminal capture inequality

\[
              v_d(H)>\mu_d+v_d(Y_d)+\chi,         \tag{2}
\]

where `chi=0` when `d` is internal to the response path and
`chi=v_d(P)>0` when `d` is the unmatched target and keeps charity.

## Exact dichotomy

If `H=D`, the whole desired response is retained at its physical target. The
response transfer disappears, and the terminal payment condition is exactly

\[
                         v_d(Y_d)+\chi<F_d.        \tag{3}
\]

This is the full-retention/bare-deficit branch.

If `H` is a proper subset of `D`, deletion preserves common safety and
inclusion-minimality of `D` gives

\[
                         v_d(H)\le F_d.            \tag{4}
\]

Combining (2) and (4) yields

\[
              \mu_d+v_d(Y_d)+\chi<F_d,           \tag{5}
\]

or equivalently

\[
              v_d(D)+v_d(Y_d)+\chi<2F_d.         \tag{6}
\]

Thus every proper terminal repair lies in a strict two-floor band. No
additional response core can be extracted from `H`; its mathematical content
is instead the simultaneous fact that it is item-critical for the represented
target owner and captures more than `d`'s full response margin.

Equivalently, define the bare deficit after charity

\[
                 \rho_d=F_d-v_d(Y_d)-\chi.        \tag{7}
\]

Both branches force `rho_d>0`. In the proper branch, (5) is exactly

\[
                         \mu_d<\rho_d.             \tag{8}
\]

Thus the response's guaranteed strict margin—even though it is completely
captured by the selected union under generalized PI-freeness—is smaller than
the amount needed to repair `d`. Any successful reversal must use value
beyond the captured margin, combine the two response targets, or exploit a
signed residual/charity substitution.

## Fixed-U consequence

Apply the dichotomy unconditionally to the ordinary base-desired `d->q`
response. The exact R2 path has paid unmatched target `s` immediately before
internal `d`, so charity can remain at `d` while `s` keeps its current paid
bundle. R3 has `d` as target hole. Therefore both forms use `chi=v_d(P)` for
this `q`-target application. A saturated survivor must realize either
complete retention of the `d->q` core or the strengthened strict band (6),
while also satisfying:

- the root wall against `A`;
- the lower wall against the other response cores;
- generalized-PI full-margin capture by the selected union; and
- the represented target owner's item-critical repair inequalities.

The `d->r` strong-wall response may be only current-desired, so minimality at
the base floor and the generalized-PI capture argument do not automatically
apply there. The next analytic task is therefore two-part: exclude the
full/proper polarity at `q`, and either convert `d->r` to a base response or
close its mixed current/base signed-payment branch.

## Boundary

The dichotomy is cap-free and exact. It does not itself contradict the root
walls, establish disjointness or release compatibility of the two retained
packets, prove observer safety, or finish the fixed-U theorem.
