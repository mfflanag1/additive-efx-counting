# Early-`r` dual-base reduction

**Date:** 2026-08-09

**Status:** cap-free analytic reduction of the two early-`r` length-three
orders to two cross-packet source walls; not a closure theorem

## Normal form

Let

\[
X_p=\{x\},\qquad X_r=T_r\mathbin{\dot\cup}B_r,\qquad
X_q=T_q\mathbin{\dot\cup}B_q,\qquad X_s=\{y\},
\]

and let `f` be the charity good.  The selected basic cycle and external
envy edge are

\[
p\xrightarrow f r\xrightarrow f q\longrightarrow p,
\qquad r\longrightarrow s.
\tag{1}
\]

Write `b_i=v_i(X_i)` and `D_p=T_r+f`.  The only priority orders considered
here are

\[
(s,r,p,q)\qquad\hbox{and}\qquad(s,r,q,p).
\tag{2}
\]

The selected desired sets `D_p`, `T_q+f`, `{x}`, and `{y}` are common-safe
at the base.  Absence of a self-`f`-champion at `r` gives

\[
v_r(T_q)>v_r(T_r).
\tag{3}
\]

## Base-threshold extraction

Put

\[
V=B_r+T_q.
\tag{4}
\]

Equation (3) implies

\[
v_r(V)>v_r(B_r+T_r)=b_r.
\tag{5}
\]

Choose an inclusion-minimal `R subseteq V` with `v_r(R)>=b_r`.  If `R` is
common-safe, then

\[
(Y_p,Y_r,Y_q,Y_s)=(D_p,R,\{x\},\{y\})
\tag{6}
\]

is EFX and Pareto improves the base.  Every displayed bundle is
common-safe, and every recipient receives at least her base utility; `p`,
`q`, and `r` improve strictly.

Suppose `R` is not common-safe.  In an unsafe deletion `R-h`, choose an
inclusion-minimal set `A` crossing any agent's base threshold.  Then `A` is
desired by its source, is common-safe, and minimality of `R` gives

\[
v_r(A)\le v_r(R-h)<b_r.
\tag{7}
\]

Thus `r` cannot source `A`.  Source `s` also closes immediately:

\[
(D_p,\{y\},\{x\},A)
\tag{8}
\]

is EFX and Pareto improving, because `r` desires `{y}` and `s` desires
`A`.  Consequently every surviving early-`r` state produces a desired set

\[
A\subseteq B_r+T_q,qquad v_r(A)<b_r,
\tag{9}
\]

whose source is `p` or `q`.

## Both packets are essential

Write

\[
J=A\cap B_r,\qquad H=A\cap T_q.
\tag{10}
\]

Both `J` and `H` are nonempty.

If `A` is sourced by `p` and `H` is empty, then `p` envies `X_r`; the
ordinary edge `p -> r`, followed by `r -f-> q -> p`, is a PI cycle.  If
`J` is empty, the ordinary envy edges `p -> q -> p` form a PI cycle.

If `A` is sourced by `q` and `H` is empty, then `q -> r -f-> q` is a PI
cycle.  If `J` is empty, additivity gives
`v_q(A)<=v_q(T_q)<v_q(X_q)=b_q`, contradicting that `A` is desired by
`q`.

Hence neither surviving wall is a diffuse observer failure: it is a
genuinely cross-packet desired set using goods from both large bundles.

## Sharper `q`-source bottleneck

Suppose `A=J+H` is sourced by `q`.  Since `v_q(A)>b_q`, additivity yields

\[
v_q(J)>v_q(B_q)+v_q(T_q\setminus H)>v_q(B_q).
\tag{11}
\]

Moreover global maximality forces

\[
v_r(J)\ge v_r(B_q).
\tag{12}
\]

Indeed, if `v_r(B_q)>v_r(J)`, the set

\[
L=(X_r\setminus J)+B_q
\]

is disjoint from `A` and has `r`-value strictly above `b_r`.  Extract a
desired set `E subseteq L`.  If its source is `r`, use
`({x},E,A,{y})`; if its source is `s`, use `({x},{y},A,E)`.  Both are EFX
Pareto improvements.  Sources `p` and `q` give, respectively, the
PI-compatible generalized cycles

\[
p\xrightarrow{B_q\mid J}r\xrightarrow f q\longrightarrow p,
\qquad
q\xrightarrow{B_q\mid J}r\xrightarrow f q.
\]

The incoming sets `B_q` and `{f}` are disjoint, and `B_q` is released by
the selected edge into `q`.  Every possible source is therefore
impossible, proving (12).

## Exact theorem boundary

The two orders in (2) are closed unless base-threshold extraction produces
one of exactly two objects:

1. a `p`-desired cross-packet set `A=J+H` satisfying (7), with nonempty
   `J subseteq B_r` and `H subseteq T_q`; or
2. a `q`-desired cross-packet set with the same geometry and the joint
   bottleneck (11)--(12).

This reduction does not route those two objects.  In particular, it does
not claim the early-`r` orders or the full length-three topology are closed.
It supplies the exact interface for a dual-base operation: preserve `s` at
`{y}` and pay `r` at `b_r`, or transfer `{y}` to `r` while compensating
`s`, using a cross-packet boundary whose `r`-value is strictly below
`b_r`.

The displayed scalar implications are replayed independently in
[`length_three_early_r_dual_base_scalar_audit.json`](length_three_early_r_dual_base_scalar_audit.json).
The replay checks the additive algebra; desired-set extraction and PI-cycle
routing are the analytic parts of the proof.
