# Packet-replacement aggregate root-flip polarity lemma

**Date:** 2026-08-10

**Status:** cap-free analytic dichotomy; the two oriented survivor branches
remain open

## Setting

Use a strict core-capture survivor of the packet-replacement complement-
return lemma.  Thus an external owner `a` receives the desired bundle

\[
K+f,
\]

and, with

\[
O=X_q\setminus K,
\qquad
\Delta_a=v_q(K)-v_q(X_a)>0,
\]

the canonical compensated root flip chooses `P subseteq T_r` and
`H subseteq O` subject to

\[
v_r(H)\ge v_r(P),
\qquad
v_q(P)>\Delta_a+v_q(H). \tag{1}
\]

## Aggregate dichotomy

Take the full packets

\[
P=T_r,
\qquad
H=O. \tag{2}
\]

If

\[
v_r(O)\ge v_r(T_r)
\quad\hbox{and}\quad
v_q(X_a)\ge v_q(f), \tag{3}
\]

then (1) holds.  The first inequality is immediate.  For the second, the
flower bundle `T_r+f` is strictly desired by `q`, so

\[
v_q(T_r)+v_q(f)>v_q(X_q).
\]

Using `v_q(X_a)>=v_q(f)` gives

\[
v_q(T_r)>v_q(X_q)-v_q(X_a)
=\Delta_a+v_q(O). \tag{4}
\]

Consequently every failure of the aggregate root flip forces at least one
of the two strict polarities

\[
v_r(T_r)>v_r(O), \tag{R-wall}
\]

\[
v_q(f)>v_q(X_a). \tag{Q-wall}
\]

No cardinality or minimum-item assumption enters the argument.

## Complete aggregate flip

When (3) holds, formula (12) of the complement-return lemma becomes

\[
Y_a=K+f,
\qquad
Y_q=X_a+T_r,
\qquad
Y_r=B_r+O, \tag{5}
\]

with the fourth owner fixed.  This is a complete allocation: `K+O=X_q`
and `T_r+B_r=X_r`.  Agent `a` strictly improves by the selected response,
`q` strictly improves by (4), and `r` is weakly nonworse by (3).
The response-Hall support is exactly the already audited three-target root
flip with `P=T_r,H=O`.  Thus an EFX instance of (5) is the required later-
owner improvement, while an internal response SDR is PI.

## Composition with the maximal frontier

For a value-maximal replacement frontier, every core-capture survivor also
satisfies

\[
v_q(O)>v_q(f).
\]

Therefore a `Q-wall` has the strict three-level order

\[
v_q(O)>v_q(f)>v_q(X_a). \tag{6}
\]

An `R-wall` instead says that the earlier root ranks its payment reservoir
above the entire released complement.  These are the two signed states an
adaptive external-owner augmentation must transport.  They replace the
unstructured statement “the two-row knapsack failed” with an explicit
root/owner polarity, while still allowing smaller packets to satisfy (1).

The scalar implication replays in
[`packet_replacement_aggregate_root_flip_polarity_audit.json`](packet_replacement_aggregate_root_flip_polarity_audit.json).

## Claim boundary

This lemma closes the full-packet root flip unless the named `R-wall` or `Q-wall`
holds.  It does not rule out those walls, prove that a smaller
compensating pair exists, eliminate an external response-Hall defect, close
the `GG` flower, or prove four-agent additive EFX.
