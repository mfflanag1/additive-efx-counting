# Two-external weighted-Hall boundary diagnosis

**Date:** 2026-08-11

**Status:** cap-free subset-polarity theorem proved; the proposed universal
closure theorem is not proved by the present local premises

## Exact cap-free theorem

Use the minimal-payment flower rotation

\[
Y_r=T_q+f,\qquad Y_q=W=B_q+L,\qquad
R=(T_r\setminus L)+B_r.
\]

Let `i` be any observer and let `S subseteq R`.  If assigning `S` to `i`
still does not pay the wall against `W`,

\[
v_i(Y_i)+v_i(S)<\tau_i(W), \tag{1}
\]

then

\[
v_i(B_q)>v_i(S). \tag{2}
\]

Indeed, intended owners weakly improve, and base EFX against
`X_r=L+R` gives

\[
v_i(Y_i)\ge v_i(L)+v_i(R)-m_i(L+R). \tag{3}
\]

Combining (1) and (3) with

\[
\tau_i(W)=v_i(B_q)+v_i(L)-m_i(B_q+L)
\]

yields

\[
v_i(B_q)>
v_i(R)+v_i(S)-m_i(L+R)+m_i(B_q+L)>v_i(S),
\]

because `R` is nonempty, `m_i(L+R)<=v_i(R)`, and all goods have positive
value.  The implication is independent of packet cardinality and is checked
by `flower_weighted_residual_complement_polarity_audit.json`.

For two external walls this gives the exact complement boundary.  Either
there is a packet `P subseteq R` that pays `c` while `R\P` pays `s`, or every
packet paying `c` has a complement satisfying

\[
v_s(B_q)>v_s(R\setminus P). \tag{4}
\]

The symmetric statement holds after exchanging `c,s`.  Thus a failed
two-owner payment split always supplies named strict complement polarities.

## Why this is not yet the requested contradiction

The strict inequalities in (2)--(4) concern different valuation rows.  They
are compatible; they do not algebraically cancel into a contradiction.
Moreover, paying all scalar demands is not sufficient for a response SDR.
The refreshed exact no-closure model has 79 residual partitions that pay all
three scalar demands, while every one of its 1,024 partitions is
response-Hall deficient.

This is not a degeneracy artifact.  The deterministic seed-2 perturbation in
`two_external_weighted_hall_hardened_countermodel.json` is positive and
subset-sum injective, satisfies the complete encoded flower master, live
polarity, and basic PI-free conditions, and still has:

- one inclusion-minimal payment packet;
- 1,024 exact residual partitions;
- zero EFX residual partitions; and
- zero internal response SDRs.

The independent exact-Fraction replay is
`two_external_weighted_hall_hardened_countermodel_audit.json`.

Consequently the first two branches of the proposed closure theorem are
false under the currently encoded local premises.  A third branch cannot be
called a *polarity contradiction* merely because it outputs (2): the
hardened valuation realizes those signs consistently.

## The missing global branch

The first hardened local survivor is not globally maximal.  It has a
one-good connected lexicographic EFX transfer

\[
c\to r:bc_0.
\]

Its exact response audit has no internal SDR, so this is specifically a
global-maximality contradiction rather than a local PI cycle.

After incrementally excluding every connected one- and two-good lex escape,
a second positive subset-sum-injective survivor remains locally deficient.
Its first connected lexicographic EFX contradiction has three goods and
topology

\[
q\to r:1,\qquad r\to c:2.
\]

This endpoint is EFX but has no internal response SDR, so it belongs to the
global lexicographic/maximality branch rather than the local PI branch.

The radius-three separation run installed 42 exact alternatives before a
deliberate pause: 31 internal SDRs, six EFX residual partitions, and five
global lex escapes of radius at most three.  It had not produced a new
countermodel after the first radius-three escape was cut.  The final solver
check was canceled, so this is a frontier record, not an UNSAT theorem.

## Correct breakthrough target

The supported cap-free statement is therefore:

> Every deficient minimal-payment response boundary either closes by an EFX
> residual split or a release-compatible PI component, or produces named
> strict residual-complement polarities.  To turn those polarities into a
> contradiction, one must construct a connected lexicographic EFX transfer
> component (or invoke an equivalent global-maximality consequence).

The remaining proof obligation is not another scalar weighted-Hall lemma.
It is a **polarity-to-connected-component conversion theorem**.  The bounded
data identify its first necessary topology as the cap-free lift of
`q -> r -> c`; a valid proof must allow arbitrary payment packets and then
apply the transfer-component hybrid lemma to contradict global lexicographic
maximality.

## Claim boundary

This note proves the arbitrary-subset polarity implication and independently
verifies two nondegenerate bounded local obstructions.  It does not prove
that every strict polarity certificate constructs the required connected
endpoint, establish full generalized PI-freeness of either obstruction,
close the flower `GG` case, or prove four-agent/general additive EFX.
