# Alternating payment-compensation chain lemma

**Date:** 2026-08-10

**Status:** cap-free finite adaptive selector; the two exhaustion walls
remain open

## Setting

Use a strict external core-capture survivor of the packet-replacement
complement-return lemma.  Put

\[
O=X_q\setminus K,
\qquad
\Delta_a=v_q(K)-v_q(X_a)>0.
\]

The flower payment reservoir satisfies

\[
v_q(T_r)>\Delta_a. \tag{1}
\]

For packets `P subseteq T_r` and `H subseteq O`, the canonical root flip is
paid exactly when

\[
v_q(P)>\Delta_a+v_q(H), \tag{Q}
\]

\[
v_r(H)\ge v_r(P). \tag{R}
\]

## Adaptive chain

Choose an inclusion-minimal nonempty `P subseteq T_r` satisfying (Q) with
`H=emptyset`.  It exists by (1).  Starting from `(P,emptyset)`, repeat:

1. If (R) fails and `v_r(O)>=v_r(P)`, enlarge `H` by an inclusion-minimal
   nonempty packet from `O-H` that restores (R).  If even all of `O` is
   insufficient, stop at an **R-exhausted wall**.
2. If (Q) then fails and `v_q(T_r)>Delta_a+v_q(H)`, enlarge `P` by an
   inclusion-minimal nonempty packet from `T_r-P` that restores (Q).  If
   even all of `T_r` is insufficient, stop at a **Q-exhausted wall**.
3. If both (Q) and (R) hold, stop successfully.

Every repair strictly enlarges one of `P,H`, and neither packet ever
shrinks.  Therefore the chain terminates after at most

\[
|T_r|+|O|
\]

strict repair steps.  This is a cap-free termination statement: the proof
uses finiteness but assumes no fixed bound on either packet.

When an inclusion-minimal repair is not unique, retain every choice as a
branch of a finite repair tree.  Every root-to-leaf path has the same
monotone termination property.  If any leaf is successful the root flip is
selected; only if every leaf is exhausted must the continuation analyze the
signed terminal walls.

Minimality makes every newly inserted repair packet critical.  If `D` is
the packet added in a Q-repair, deleting any `d in D` restores failure of
(Q) with the preceding `P,H`; the analogous statement holds in `r`'s row
for every R-repair.  Thus the chain records the exact blocker goods needed
for a subsequent component or item-order argument.

## Successful terminal state

If both inequalities hold, form

\[
Y_a=K+f,
\qquad
Y_q=(O\setminus H)+X_a+P,
\qquad
Y_r=(X_r\setminus P)+H, \tag{2}
\]

fixing the fourth owner.  This is the canonical complete root flip.  Agent
`a` strictly improves by the selected response, `q` strictly improves by
(Q), and `r` is weakly nonworse by (R).  The three response targets have
pairwise-disjoint incoming packets and internally supplied releases, as
already checked by the complement-return audit.  Hence an EFX instance of
(2) is the required improvement, while an internal response SDR is PI.

## Exact exhaustion alternatives

If an R-repair is impossible, then

\[
v_r(O)<v_r(P)\le v_r(T_r). \tag{R*}

This is stronger than the aggregate `R-wall`: it identifies the current
payment-critical subpacket that the entire released complement cannot pay.

If a Q-repair is impossible, then

\[
v_q(T_r)\le\Delta_a+v_q(H)\le\Delta_a+v_q(O).
\]

Since `Delta_a+v_q(O)=v_q(X_q)-v_q(X_a)` and `q` strictly desires
`T_r+f`, subtraction forces

\[
v_q(X_a)<v_q(f). \tag{Q*}

At a value-maximal replacement frontier, `v_q(O)>v_q(f)`, so the terminal
Q-wall has the strict orientation

\[
v_q(O)>v_q(f)>v_q(X_a). \tag{3}

Thus the adaptive chain never ends in an unnamed two-row failure.  It
either selects a working root flip or produces one of the explicit signed
states (R*) and (Q*), together with the full history of critical repair
packets.

The scalar exhaustion implications replay in
[`alternating_payment_compensation_chain_audit.json`](alternating_payment_compensation_chain_audit.json).
On the sole strict-capture response among the seven frozen frontier
profiles, the exact repair tree has three states: one successful leaf and
one Q-exhausted leaf.  This both validates the construction and shows that
ties between minimal repairs must remain adaptive rather than be frozen.

## Claim boundary

This lemma proves finite adaptive selection and eliminates blind search over
`(P,H)`.  It does not eliminate the R-exhausted or Q-exhausted wall, prove
that their blocker history yields an augmenting owner component, close the
remaining external Hall defect, close the `GG` flower, or prove four-agent
additive EFX.
