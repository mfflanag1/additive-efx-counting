# Root-critical compensator dichotomy

**Date:** 2026-08-11

**Status:** cap-free analytic reduction; the compensator dependency is
terminated by the alternating-frontier lemma

## Setting

Use the failed root-preserving two-hole selector.  The released pool has two
partitions

\[
 P=A\mathbin{\dot\cup}W=H\mathbin{\dot\cup}L,
\]

where `A` is the old common-safe desired root core, `W` is the old residual,
and the selected orientation gives `H` to the root `r` and `L` to the other
hole `d`.  Put

\[
 \delta=v_r(H)-v_r(A)=v_r(W)-v_r(L)\ge 0.             \tag{1}
\]

Let `g` be the least-`d` good of `H`.  Failure of the selector gives

\[
 v_d(L)<v_d(H-g),                                    \tag{2}
\]

and root criticality gives

\[
 v_r(g)>\delta.                                      \tag{3}
\]

The partition `H,L` maximizes `v_d(L)` among all oriented partitions whose
root cell has value at least `v_r(A)`.

## Compensator dichotomy

Call `K subseteq L` a **root compensator** for `g` when

\[
 v_r(K)\ge v_r(g)-\delta.                            \tag{4}
\]

Exactly one of the following alternatives applies.

### 1. A compensator exists

For every root compensator `K`, maximality of the selected partition forces

\[
 v_d(K)\ge v_d(g).                                   \tag{5}
\]

Indeed, exchange `g` and `K`:

\[
 H'=(H-g)+K,
 \qquad
 L'=(L-K)+g.                                         \tag{6}
\]

Equation (4) and (1) give `v_r(H')>=v_r(A)`.  Hence `(H',L')` is another
feasible oriented partition.  Optimality of `L` gives

\[
 v_d(L)+v_d(g)-v_d(K)=v_d(L')\le v_d(L),
\]

which is (5).  In the nondegenerate normal form the disjoint bundles `K`
and `{g}` are distinct, so (5) is strict:

\[
 v_d(K)>v_d(g).                                      \tag{7}
\]

Choose an inclusion-minimal compensator.  Then every `k in K` is
root-critical inside the packet:

\[
 v_r(K-k)<v_r(g)-\delta.                             \tag{8}

Thus failure has become a named alternating dependency: the root needs the
packet `K` to release `g`, while the other hole strictly ranks that same
packet above `g`.  The packet is retained for the next owner/charity
component rather than being hidden inside the two-hole partition.  The
root-critical alternating-frontier lemma grows this dependency finitely
until it exposes an old-core packet dominating the residual complement.

### 2. No compensator exists

Taking `K=L` in the failure of (4) gives

\[
 v_r(L)<v_r(g)-\delta.
\]

Using (1),

\[
 v_r(g)>v_r(L)+\delta=v_r(W).                        \tag{9}
\]

Positivity now proves that `g` did not originate in `W`: every good of `W`
has value at most `v_r(W)`.  Consequently

\[
 g\in A.                                             \tag{10}
\]

This support conclusion is cap-free and is stronger than the scalar
root-critical polarity alone.

## Flower routing

For the anchored `GG` flower, `A=T_q+f`.  In the no-compensator branch,
(10) gives exactly two possibilities.

1. If `g in T_q`, use the singleton packet `{g}` in the top-core root
   exchange.  The critical reverse orientation factors through the proved
   top-core residual reset into the two-root response-Hall component.
2. If `g=f`, equation (9) gives `v_r(f)>v_r(W)`.  The early-root polarity
   `v_r(B_r)>=v_r(f)` then yields `v_r(B_r)>v_r(W)`, so
   `B_r\setminus W` is nonempty and the captured-bottom handoff applies.

Therefore an unstructured root-critical selector failure no longer
survives.  It either exposes the strict compensator dependency (7)--(8),
enters the top exchange/reset, or enters the captured-bottom handoff.

## Verification and claim boundary

[`root_critical_compensator_dichotomy_audit.json`](root_critical_compensator_dichotomy_audit.json)
checks the support identity, compensator feasibility, forced opposite-row
order, no-compensator residual domination, and old-core membership under Z3
5.0.0 and 4.15.3.

Together with the alternating-frontier lemma, the compensator chain
terminates in a top-core or captured-bottom handoff.  These lemmas do not
close a later top-core or captured-bottom revisit, close `GG`, or prove
four-agent/general additive EFX.
