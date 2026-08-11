# Same-source top-switch margin-descent lemma

**Date:** 2026-08-11

**Status:** cap-free potential for fresh same-source switches; reused-top
response recurrence remains open

## Setting

Use the B-exhausted same-source endpoint of the captured-bottom external-
compensation chain.  The later mutual owner `q` holds a desired deletion of

\[
 D_q=T_r+f.
\]

Write the currently removed top support as `U subseteq T_r` and the current
mutual core as

\[
 D(U)=(T_r\setminus U)+f.
\]

Its strict `q`-response margin is

\[
 \mu(U)=v_q(D(U))-v_q(X_q)>0.                        \tag{1}

The external source switches to a crossing bottom core `K+B_q`, with
nonempty `K subseteq T_r`.

## Fresh-switch descent

Put

\[
 K^{\rm new}=K\setminus U.
\]

To keep the two selected cores disjoint, every good of `K^{new}` must be
removed from `D(U)`.  If the reduced mutual core remains desired, then

\[
 \mu(U+K^{\rm new})
 =\mu(U)-v_q(K^{\rm new})>0.                         \tag{2}

Whenever `K^{new}` is nonempty, positivity gives the strict potential drop

\[
 0<\mu(U+K^{\rm new})<\mu(U),                        \tag{3}

and the removed support strictly grows:

\[
 U\subsetneq U+K^{\rm new}.                         \tag{4}

If the reduced core is not desired, the removed packet captures the whole
current response margin:

\[
 v_q(K^{\rm new})\ge\mu(U).                         \tag{5}

Thus a fresh top switch either strictly descends the mutual-owner margin or
exposes the exact `q`-capture handoff.

## Finite consequence

Along switches whose external top packets always contain a fresh good,
`U` grows strictly.  There can be at most `|T_r|` such switches.  The scalar
margin (1) decreases by the value of the newly removed disjoint packet at
each successful step; no infinitesimal argument or value cap is used.

The only switch not covered by strict descent satisfies

\[
 K\subseteq U.                                       \tag{6}

It reuses top support already removed from the mutual core.  This is not a
new knapsack leaf: it is the precise dynamic-response recurrence in which
an earlier external target reclaims a previously selected physical packet.
The recurrence must close through common release support/PI, supplier
growth, or the existing overlap hitting-set polarity.  Equation (6) is the
sole remaining same-source revisit form.

## Verification and claim boundary

[`same_source_top_switch_margin_descent_audit.json`](same_source_top_switch_margin_descent_audit.json)
checks the margin identity, strict fresh-support descent, and the failure-
captures-margin alternative.

This lemma proves that fresh same-source top switches cannot cycle.  It does
not eliminate a reused packet satisfying (6), prove release compatibility
across every historical target, terminate the opposite-source capture
branch, close `GG`, or prove four-agent/general additive EFX.
