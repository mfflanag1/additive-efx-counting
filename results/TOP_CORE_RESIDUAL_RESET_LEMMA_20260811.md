# Top-core residual-reset lemma

**Date:** 2026-08-11

**Status:** cap-free analytic factorization; terminal external response/Hall
termination remains open

## Setting

Use the critical reverse-order survivor of the top-core root exchange.  Write

\[
T_q=K_T\mathbin{\dot\cup}\overline K_T,
\qquad
T_r=P'\mathbin{\dot\cup}\overline P'.
\]

The live flower cell supplies

\[
v_r(T_q+f)>v_r(T_r+B_r),
\qquad v_r(B_r)\ge v_r(f), \tag{1}
\]

and the reverse-order wall is

\[
v_r(P')>v_r(K_T). \tag{2}
\]

The other mutual edge and the live bottom polarity give

\[
v_q(T_r+f)>v_q(T_q+B_q),
\qquad v_q(B_q)>v_q(f). \tag{3}
\]

## Complement reversal

Equations (1)--(2) force

\[
v_r(\overline K_T)>v_r(\overline P'). \tag{4}
\]

Indeed, (1) and `v_r(B_r)>=v_r(f)` imply
`v_r(T_q)>v_r(T_r)`.  Expanding both top packets and using (2) yields

\[
v_r(\overline K_T)+v_r(K_T)
>v_r(\overline P')+v_r(P')
>v_r(\overline P')+v_r(K_T),
\]

which proves (4).  Thus failure of the direct `P'`-for-`K_T` exchange is
not an unordered dead end: both the selected cores and their complements
have strict, opposite transfer orientations in `r`'s row.

Equation (3) similarly forces

\[
v_q(T_r)>v_q(T_q). \tag{5}
\]

Therefore the minimal-payment residual rotation applies.  Choose an
inclusion-minimal nonempty `L subseteq T_r` with

\[
v_q(L)>v_q(T_q),
\]

and form

\[
Z_r=T_q+f,
\qquad
Z_q=B_q+L,
\qquad
R=(T_r\setminus L)+B_r. \tag{6}
\]

Both mutual owners strictly improve, every owner dominates the residual
charity `R`, and the only possible EFX failure is strong envy of the evolved
`q` target `B_q+L`.  Hence the two-root residual-split response-Hall theorem
applies to every critical top-core reverse-order state.

## Factorization consequence

The critical top-core cell is not a fourth terminal obstruction.  It
canonically factors back into the same residual response-Hall boundary as
the ordinary minimal-payment rotation:

1. an EFX endpoint closes immediately;
2. an internal response SDR is a release-compatible PI edge set;
3. otherwise an external source or a minimal Hall-deficient target set is
   exposed.

The complement inequality (4) records information that must be retained if
the continuation later changes the root back to `r`.  Merely invoking (6),
however, does not by itself prove a strict global-potential increase: a
later response continuation could revisit another top-core exchange.

The scalar implications replay in
[`top_core_residual_reset_audit.json`](top_core_residual_reset_audit.json).

## Claim boundary

This lemma removes the critical reverse-order cell as an independent proof
architecture and routes it into the existing cap-free two-root component.
It does not eliminate a sink-capture wall, rule out a terminal all-owner
Hall deficiency, prove that repeated root changes cannot revisit a prior
state, close the `GG` flower, or prove four-agent additive EFX.
