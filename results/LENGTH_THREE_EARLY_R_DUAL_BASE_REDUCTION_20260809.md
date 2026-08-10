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

## Joint-suffix escape

The split-profile escape has an arbitrary-packet formulation.  Fix any
good `j in T_r` and any partition

\[
J=J_q\mathbin{\dot\cup}J_r.
\tag{11}
\]

Define

\[
\begin{aligned}
P_j&=\{x,j\},\\
Q_j&=H+J_q+B_q,\\
R_j&=(T_r\setminus\{j\})+J_r+(T_q\setminus H).
\end{aligned}
\tag{12}
\]

These three bundles and `{y}` are pairwise disjoint.  Suppose `Q_j` and
`R_j` are common-safe and

\[
v_q(Q_j)\ge v_q(x),\qquad v_r(R_j)\ge b_r.
\tag{13}
\]

Then

\[
(Y_p,Y_r,Y_q,Y_s)=(P_j,R_j,Q_j,\{y\})
\tag{14}
\]

is EFX and lexicographically improves both orders in (2).

To prove this, positivity gives `v_p(P_j)>v_p(x)=b_p`.  Every deletion of
`P_j` leaves `{x}` or `{j}`.  Agent `q` is protected by the first inequality
in (13), and `v_q(j)<=b_q<v_q(x)` by base EFX.  Agent `r` cannot envy `{x}`:
otherwise `r -> p -f-> r` is a PI cycle.  Agent `s` cannot envy `{x}`:
otherwise `s -> p -f-> r -> s` is a PI cycle.  Both agents value `{j}` at
most their base utilities by base EFX.  Thus `P_j` is safe for every new
recipient.  Common safety of `Q_j,R_j`, together with (13), protects all
remaining comparisons.  Agent `s` is fixed, `r` is weakly preserved, and
`p` strictly improves, proving the lexicographic claim.

Ignoring the common-safety selector for the moment, the two recipient
conditions in (13) are exactly a two-demand partition of `J`.  Put

\[
\delta_q^j=v_q(x)-v_q(H+B_q),\qquad
\delta_r^j=b_r-v_r((T_r\setminus\{j\})+(T_q\setminus H)).
\tag{15}
\]

Then (13) is equivalent to

\[
v_q(J_q)\ge\delta_q^j,
\qquad
v_r(J_r)\ge\delta_r^j.
\tag{16}
\]

For each `j`, fractional knapsack decides (16) with at most one split good.
Thus failure of the joint-suffix escape has only two possible sources: a
scalar `q/r` price separator on `J`, or one indivisible boundary good,
together with failure of common safety after the corresponding rounding.
It is not an unrestricted three-bundle packing problem.

The minimum escape in the frozen `(2,2,2,2)` dual-mode counterprofile is an
instance of (14): `j=tr1`, `J_q={br1}`, `J_r={br0}`, and `H={tq1}`.  This
explains that counterprofile but is not used as evidence that (16) always
has an integral solution.

## Sharper `q`-source bottleneck

Suppose `A=J+H` is sourced by `q`.  Since `v_q(A)>b_q`, additivity yields

\[
v_q(J)>v_q(B_q)+v_q(T_q\setminus H)>v_q(B_q).
\tag{17}
\]

Moreover global maximality forces

\[
v_r(J)\ge v_r(B_q).
\tag{18}
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
impossible, proving (18).

## Exact theorem boundary

The two orders in (2) are closed unless base-threshold extraction produces
one of exactly two objects:

1. a `p`-desired cross-packet set `A=J+H` satisfying (7), with nonempty
   `J subseteq B_r` and `H subseteq T_q`; or
2. a `q`-desired cross-packet set with the same geometry and the joint
   bottleneck (17)--(18).

This reduction does not route those two objects.  In particular, it does
not claim the early-`r` orders or the full length-three topology are closed.
It supplies two exact interfaces for a dual-base operation: find the
joint-suffix partition (16), preserving `s` and `r` before improving `p`,
or transfer `{y}` to `r` while compensating `s`, using a cross-packet
boundary whose `r`-value is strictly below `b_r`.

The displayed scalar implications are replayed independently in
[`length_three_early_r_dual_base_scalar_audit.json`](length_three_early_r_dual_base_scalar_audit.json).
The replay checks the additive algebra; desired-set extraction and PI-cycle
routing are the analytic parts of the proof.
