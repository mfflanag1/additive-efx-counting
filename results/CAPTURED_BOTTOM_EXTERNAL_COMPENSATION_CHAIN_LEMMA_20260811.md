# Captured-bottom external-compensation chain lemma

**Date:** 2026-08-11

**Status:** cap-free finite realization of the `q -> a -> r` bottom-transfer
path; terminal top-switch/source-capture handoffs remain open

## Full-capture input

Use the full-`X_q` flower orientation

\[
 A_a=T_q+H,
 \qquad \varnothing\ne H\subseteq B_r,
\]

where external source `a in {c,s}` strictly desires the common-safe core
`A_a`.  Pair it with the disjoint dual mutual core

\[
 D_q=T_r+f.
\]

The complement of these cores is

\[
 P=(B_r\setminus H)+B_q+X_c+X_s.                   \tag{1}

Suppose the dual pool does not pay the earlier root and that a minimal
dual-core extraction reaches the pure captured-bottom branch

\[
 \varnothing\ne C\subseteq H.                       \tag{2}

Packets in `T_r+f` or `T_q` instead enter the already named top/floater
root-exchange handoff.

## Alternating compensation

For packets `C subseteq H` and `B subseteq B_q`, define

\[
 P(C,B)=P+C-B,
 \qquad A(C,B)=A_a-C+B.                              \tag{3}

These two targets still partition `P+A_a`; `D_q` is fixed.  The two payment
conditions are

\[
 v_r(P(C,B))\ge v_r(X_r),                            \tag{R}
\]

\[
 v_a(A(C,B))>v_a(X_a).                              \tag{A}
\]

Start with `B=empty` and an inclusion-minimal nonempty `C` restoring (R).
Repeat the following operations.

1. If (A) fails, enlarge `B` inclusion-minimally until it holds.  If even
   `B=B_q` does not restore (A), stop at **B-exhaustion**.
2. If (R) then fails, enlarge `C` inclusion-minimally until it holds.  If
   even `C=H` does not restore (R), stop at **C-exhaustion**.
3. If both conditions hold, stop successfully.

Every nonterminal round strictly enlarges `B` or `C`.  Hence the process
terminates after at most `|B_q|+|H|` additions.  This is the cap-free packet
lift of the empirical owner path: physically, `B` moves from `q` toward the
external source and `C` moves from the external core toward the root.

## Successful leaf

At success, `r` is weakly nonworse, while `q` retains the desired core
`D_q` and `a` strictly desires `A(C,B)`.  If `A(C,B)` is common-safe, the
two disjoint cores `D_q,A(C,B)` have root-payable complement `P(C,B)`, so
the dual-anchor root-paid selector applies.  It yields an EFX flower
improvement, a release-compatible response/Hall boundary, or a root-critical
least-good certificate.

If `A(C,B)` is not common-safe, an inclusion-minimal unsafe deletion names
a response augmentation.  Thus success never returns to an unnamed failed
bottom swap.

## C-exhaustion

At C-exhaustion,

\[
 v_r(P+H-B)<v_r(X_r).
\]

Using (1) and `X_r=T_r+B_r`, cancellation gives

\[
 v_r(T_r)>v_r((B_q\setminus B)+X_c+X_s).             \tag{4}

Thus failure to return enough captured bottom is an exact root-top
concentration certificate.  It enters a top-core/root-payment handoff; it
cannot repeat as a bottom-only compensation failure.

## B-exhaustion

Put

\[
 \mu_a=v_a(A_a)-v_a(X_a)>0.
\]

At B-exhaustion,

\[
 v_a(A_a-C+B_q)\le v_a(X_a),
\]

and therefore

\[
 v_a(C)-v_a(B_q)\ge\mu_a>0.                         \tag{5}

The live mutual-owner polarity gives

\[
 v_q(B_q)>v_q(B_r)\ge v_q(C).                       \tag{6}

Hence the same two packets have strict opposite order in rows `a` and `q`:
the external source needs `C`, while the later mutual owner strictly favors
`B_q`.  Equations (5)--(6) are the exact source-capture endpoint of the
bottom-transfer chain.

If the same external owner `a` supplies the other bottom-edge core

\[
 A_r=K+B_q,
 \qquad K\subseteq T_r,
\]

then `v_a(A_r)>v_a(X_a)` and B-exhaustion further imply

\[
 v_a(K)>v_a(A_a-C).                                  \tag{7}

This names the next top switch.  Moreover, either `D_q-K` remains desired
by `q`, in which case `D_q-K` and `A_r` are disjoint desired cores and the
root-paid/dual-pool-deficit dichotomy reapplies to their complement, or

\[
 v_q(K)\ge v_q(D_q)-v_q(X_q)>0,                      \tag{8}

so the switch packet captures `q`'s whole response margin.  Thus even the
same-source B-exhausted endpoint returns to an alternate two-core anchor or
exposes a new two-row top-capture packet; payment of the root at the
alternate anchor is not assumed.

## Verification and claim boundary

[`captured_bottom_external_compensation_chain_audit.json`](captured_bottom_external_compensation_chain_audit.json)
checks support conservation, both exhaustion cancellations, the opposite
packet order, and the same-source top-switch dichotomy.

This lemma finitely lifts the observed `q -> c -> r` transfer topology and
eliminates indefinite pure-bottom compensation.  It does not terminate the
C-exhausted root-top handoff, compensate the B-exhausted source-capture
packet in the opposite-source case, terminate the same-source top switch,
close `GG`, or prove four-agent/general additive EFX.
