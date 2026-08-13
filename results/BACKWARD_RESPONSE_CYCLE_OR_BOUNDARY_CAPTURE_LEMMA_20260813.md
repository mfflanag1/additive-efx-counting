# Backward-response cycle or boundary-capture lemma

**Date:** 2026-08-13

**Status:** cap-free physical classification of every full-prefix backward
response; generic supplier-saturated payment is refuted and the stronger GG
decorated-head exchange remains open

## Geometry

Let

\[
 h_0\to h_1\to h_2\to h_3\to c
\]

be the genuine selected path, and let source `b=h_k` have a globally minimal
current response `E subseteq Y_{h_l}` with `k>l`.

### Response into the owner hole

If `l=0`, the cores

\[
 E,K_0,K_1,\ldots,K_{k-1}                       \tag{1}
\]

lie in distinct targets and form the directed owner cycle

\[
 h_0\to h_1\to\cdots\to h_k\to h_0.            \tag{2}
\]

Every incoming support is physically disjoint. If an incoming signed packet
is supplied outside the cycle, adjoining its supplier strictly grows the
owner component. At supplier saturation, (2) is release-compatible. Its only
remaining issue is mixed observer payment: old selected cores are base-safe,
whereas `E` and the decorated selected cores may spend realized current
surplus.

The permanent root anchor is preserved. If the response source is the root,
its anchor core lies in the next target outside (2) and can remain with the
root alongside `E`; no boundary core is displaced.

### Response into a matched prefix target

Suppose `l>0`. The target already contains the selected boundary core

\[
 A=K_{l-1}\quad\text{for source }a=h_{l-1}.      \tag{3}
\]

Put `J=E intersect A`. If `J` is empty, the response cycle (2) and the
boundary core coexist physically. If `J` is nonempty, source `b` can release
its old selected core `K_k`; for `L subseteq K_k`, give

\[
 Z_b=E,\qquad Z_a=(A\setminus J)+L.              \tag{4}
\]

If some `L` preserves `a`'s priority-valid floor `F_a`, the response is a
paid boundary split. If even the whole `K_k` fails, then

\[
 v_a(J)-v_a(K_k)\ge v_a(A)-F_a>0.                \tag{5}
\]

Thus all local subpacket choices are exhausted by one exact overlap-capture
inequality.

## Anchored identity classes

Across the six paths containing adjacent `r -> q`, the 36 backward orders
split into:

| class | count |
|---|---:|
| response into the owner hole | 18 |
| nonhole response colliding with the q-target anchor | 6 |
| nonhole response sourced by the anchored root | 2 |
| generic nonhole boundary split | 10 |

For an anchor-target collision, delete `J=E intersect K_r`. If `E-J` remains
current-desired, the exact anchor survives; otherwise `J` is simultaneously
response-critical and anchor-consuming. For a nonhole root-sourced response,
retain `K_r`. The complete physical compensation pool is

\[
 \mathcal R_E=(\mathop{\dot\bigcup}_{i\in N}R_i)\setminus E,
\]

not only the released q-target residual `R_q=Y_q-K_r`. Complete-pool failure
gives

\[
 v_a(J)-v_a(\mathcal R_E)\ge v_a(A)-F_a>0.       \tag{6}
\]

These are the same two physical root/q interfaces as in the forward-chord
lemma. Direction changes the graph outcome—cycle versus chord—but not the
support obstruction.

## Exact remaining backward gate

After disjoint completion, boundary compensation, or component growth, the
backward branch is a supplier-saturated mixed cycle. Applying residual return
to an underfunded old cycle source either pays its decorated debts or makes
the incoming cycle core strictly better than its outgoing selected core in
that source's row. Supplier saturation alone does not force the first branch:
the exact anchored countermodel in
[`SUPPLIER_SATURATION_DOES_NOT_FORCE_MIXED_CYCLE_PAYMENT_20260813.md`](SUPPLIER_SATURATION_DOES_NOT_FORCE_MIXED_CYCLE_PAYMENT_20260813.md)
survives all 625 residual assignments. Failure localizes at the head of a
decorated edge. The stronger unresolved GG operation is therefore a
decorated-head exchange together with the full-pool capture above.

## Claim boundary

This lemma proves the cycle/boundary geometry, disjointness, component-growth
alternative, overlap-capture inequalities, and anchored identity counts. It
also records the exact refutation of generic supplier-saturated payment. It
does not derive the decorated-head exchange from global GG recurrence,
reverse (5)--(6), close GG, or prove four-agent/general additive EFX.
