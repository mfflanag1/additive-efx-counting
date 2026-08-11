# Flower minimal-payment residual rotation lemma

**Date:** 2026-08-10

**Status:** cap-free analytic one-wall reduction; termination of the remaining
target dependency is open

## Statement

Let `(X,{f})` be a positive additive EFX-with-charity allocation.  Write

\[
X_r=T_r\mathbin{\dot\cup}B_r,
\qquad
X_q=T_q\mathbin{\dot\cup}B_q,
\]

with all four packets nonempty.  Suppose

\[
D_r=T_q+f
\]

is common-safe and strictly desired by `r`, and suppose

\[
v_q(T_r)>v_q(T_q). \tag{1}
\]

Choose an inclusion-minimal nonempty packet `L subseteq T_r` satisfying

\[
v_q(L)>v_q(T_q), \tag{2}
\]

and put

\[
R=(T_r\setminus L)+B_r.
\]

Then the allocation

\[
Y=(T_q+f,\ B_q+L,\ X_c,\ X_s;\ R) \tag{3}
\]

strictly improves both `r` and `q`.  Its charity packet is dominated by
every owner.  Every assigned target other than `B_q+L` is already safe.
Consequently exactly one of the following occurs:

1. `Y` is EFX with charity and is the required flexible improvement; or
2. some observer `i in {r,c,s}` strongly envies `B_q+L`.

In the second case, define the insertion charge into a nonempty core `C` by

\[
\kappa_i(C,P)
=v_i(P)+m_i(C)-\min\{m_i(C),m_i(P)\}. \tag{4}
\]

The wall forces

\[
\kappa_i(B_q,L)>\kappa_i(B_q,T_q). \tag{5}
\]

Taking an inclusion-minimal envied subset of `B_q+L` supplies a generalized
`(L|T_q)` response into the evolved `q` slot, with any additional discard
also released.

## Proof

Existence of `L` follows from (1) and finiteness; delete goods from `T_r`
while (2) remains true.  Agent `r` strictly improves because she receives
the desired bundle `D_r`.  Agent `q` strictly improves because

\[
v_q(B_q+L)>v_q(B_q+T_q)=v_q(X_q).
\]

The charity packet is automatically safe.  Fix any `ell in L`.  For every
observer `i`, base EFX against `X_r` gives

\[
v_i(X_i)\ge v_i(X_r-\{\ell\})\ge v_i(R).
\]

Owners `r,q` only improve and owners `c,s` are fixed, so all four dominate
`R` in (3).

The target `D_r` is common-safe.  The targets `X_c,X_s` are unchanged base
bundles.  Thus every observer is safe against those three targets.  Agent
`q` cannot fail against any target because her own utility strictly rises;
in particular her comparison with her own new bundle is automatic.  The
only possible failures are therefore external comparisons against
`B_q+L`, proving the dichotomy.

For an external observer, her new utility is at least her base utility, and
base EFX gives safety against `B_q+T_q=X_q`.  Hence a strict wall against
`B_q+L` forces its threshold to exceed the old threshold.  Since

\[
\tau_i(C+P)=\tau_i(C)+\kappa_i(C,P)
\]

for disjoint nonempty packets, this is exactly (5).  Inclusion-minimality of
an envied subset supplies the generalized response edge. \(\square\)

## Minimality information

The selected packet also satisfies

\[
v_q(L-\{\ell\})\le v_q(T_q)
\qquad(\ell\in L). \tag{6}
\]

Thus every good of `L` is payment-critical.  The adaptive continuation may
delete or redirect one such good, but doing so reopens a quantified `q`
payment deficit rather than an unstructured loss.  This is the natural
one-defect state for the lex-rooted donation and response-Hall lemmas.

The scalar threshold implication replays in
[`flower_minimal_payment_residual_rotation_audit.json`](flower_minimal_payment_residual_rotation_audit.json).

## Claim boundary

This lemma always selects a two-owner improving residual rotation and
reduces every failure to one evolved-target wall.  It does not eliminate
that wall, prove its response source is internal, terminate the resulting
one-defect component, close `GG`, or prove four-agent additive EFX.
