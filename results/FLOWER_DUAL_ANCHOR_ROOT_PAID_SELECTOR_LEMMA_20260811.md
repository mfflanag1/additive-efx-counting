# Flower dual-anchor root-paid selector lemma

**Date:** 2026-08-11

**Status:** cap-free adaptive-root selector; termination of its critical
packet or aggregate-deficit branches remains open

## Dual permanent anchor

In the length-two `GG` flower, write

\[
 X_r=T_r\mathbin{\dot\cup}B_r,
 \qquad X_q=T_q\mathbin{\dot\cup}B_q.
\]

Besides the root-oriented pair used by the rank-two anchor lemma, the
opposite mutual edge and the opposite external bottom edge supply two
disjoint common-safe desired cores

\[
 D_q=T_r+f,
 \qquad A_a\subseteq T_q+B_r,                       \tag{1}
\]

with distinct response sources `q` and `a in {c,s}`.  Let `e` be the
fourth owner and put

\[
 P=\left(\mathop{\dot\bigcup}_{i\in N}X_i+f\right)
   \setminus(D_q\mathbin{\dot\cup}A_a).             \tag{2}
\]

Thus `P` contains every good not used by the two dual cores, including the
whole old bundle `X_e`.

The selector below uses only that the two cores are disjoint, common-safe,
strictly desired by distinct nonroot sources `q,a`, and that the other two
owners are `r,e`.  Hence the same proof applies verbatim to any replacement
cores with those properties, including a deletion of `D_q` and any
common-safe external response core in its complement.

## Root-payment feasibility

If

\[
 v_r(P)<v_r(X_r),                                    \tag{3}
\]

no allocation using both cores in (1) can keep the earlier root weakly
nonworse.  Equation (3) is the exact **dual-pool deficit**; it is retained
as a signed flower handoff rather than silently abandoning the dual root.

Suppose instead that

\[
 v_r(P)\ge v_r(X_r).                                 \tag{4}
\]

Among all oriented partitions `P=H dot union L` satisfying

\[
 v_r(H)\ge v_r(X_r),
 \qquad v_r(H)\ge v_r(L),                            \tag{5}
\]

choose one maximizing `v_e(L)`.  The family is nonempty: `H=P,L=empty`
is feasible by (4).  Give `H` to `r`, `L` to `e`, `D_q` to `q`, and
`A_a` to `a`.

The root is weakly nonworse and envy-free against the other residual cell.
Because both cores are common-safe, the root is also EFX against them.
Owners `q,a` strictly improve over their base bundles and therefore remain
EFX against both cores.

## Exact least-good dichotomy

The only possible mutual failure between the two residual owners is

\[
 v_e(L)<\tau_e(H).                                   \tag{6}
\]

If (6) holds, let `g` be a least-`e` good of `H`.  Then

\[
 v_e(L)<v_e(H-g).                                    \tag{7}
\]

Moving `g` from `H` to `L` strictly increases `e`'s selected cell.  By
maximality, at least one constraint in (5) must break.  Hence every failed
dual selector supplies the exact disjunction

\[
 v_r(H-g)<v_r(X_r)                                   \tag{8}
\]

or

\[
 v_r(H-g)<v_r(L+g).                                  \tag{9}

\]

Equivalently, `g` is critical either for root payment,

\[
 v_r(g)>v_r(H)-v_r(X_r),                             \tag{10}

or for root envy-freeness,

\[
 2v_r(g)>v_r(H)-v_r(L).                              \tag{11}

The two alternatives can hold simultaneously.  They are item-named strict
certificates and use no cardinality or value cap.

## Flower consequence

If (6) fails, the residual owners are mutually EFX.  Every other failure is
localized to a residual owner against a selected core or a represented
source against `H` or `L`, exactly the two-core/two-hole response boundary.
An EFX endpoint satisfies the required flower objective: `r` is weakly
nonworse and the later mutual owner `q` strictly improves.  A response SDR
is release-compatible because (1)--(2) partition the complete owner union
and charity good.

Consequently a canonical reset need not return immediately to the same
root-oriented pair.  It has the following cap-free adaptive alternative:

1. the dual pool is root-payable and yields an EFX improvement, a PI/Hall
   boundary, or the critical good (8)--(11); or
2. the dual pool is not root-payable and exposes the aggregate deficit
   (3).

The payment-critical alternative has the same one-good compensator shape as
the existing root frontier, but its benchmark is the old root bundle rather
than a selected root core; composing the two therefore remains an explicit
step.  The deficit branch identifies the precise additional payment that
must be extracted from one of the two dual cores before changing roots.

## Verification and claim boundary

[`flower_dual_anchor_root_paid_selector_audit.json`](flower_dual_anchor_root_paid_selector_audit.json)
checks disjoint support, feasibility, root safety, the least-good move, and
both critical-value rewrites.

This lemma supplies a priority-valid alternative to an idempotent fixed-
anchor reset.  It does not pay the root under (3), terminate the critical
packet produced by (8)--(11), eliminate later source-inactive response
walls, close `GG`, or prove four-agent/general additive EFX.
