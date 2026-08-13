# Root-sourced complete signed-residual compensation lemma

**Date:** 2026-08-13

**Status:** cap-free correction of the alleged `R_q`-only anchor gate; the
complete signed residual pool is the minimal physical compensation family

**Supersession note (2026-08-13):** complete-pool compensation remains a
valid paid shortcut, but it is no longer a prerequisite. The
root-sourced anchor-retaining sacrifice handoff keeps the first-priority root
strictly improved, retains the permanent anchor, and sends full-pool failure
to an explicit sacrificed-owner/root-target response boundary.

## Root-sourced collision

Use a selected Hamiltonian matching containing the permanent root anchor

\[
 K_r\subseteq Y_q.                                 \tag{1}
\]

Let the root have a current response `E` in a different target `Y_l`. The
selected core occupying that target is `A=K_a` for displaced source `a`.
Write

\[
 J=E\cap A,
 \qquad A^-=A\setminus J.                         \tag{2}
\]

The anchor-target overlap branch was eliminated separately, so `E` and
`K_r` are disjoint. Give both to the root. Every other undisplaced source
keeps its selected core.

## Complete available residual pool

For each owner target write

\[
 Y_i=C_i\mathbin{\dot\cup}R_i,                    \tag{3}
\]

where `C_i` is the selected incoming core, if any. In the selected-core
allocation every `R_i` is unallocated. The response `E` may consume part of
one or more residual atoms in its own target, so the complete residual pool
still available after assigning `E` is

\[
 \mathcal R_E=
 \left(\mathop{\dot\bigcup}_{i\in N}R_i\right)
 \setminus E.                                     \tag{4}

It is disjoint from `E`, the permanent anchor, `A^-`, and every retained
selected core. In particular

\[
 R_q=Y_q\setminus K_r\subseteq\mathcal R_E,       \tag{5}

but normally `R_q` is only one summand. The root's own target residual and
all other unused target residuals are also physically available. Omitting
them is not implied by anchor preservation or internal release supply.

## Global compensation selector

Let `F_a` be the priority-valid floor for displaced source `a`. Globally
choose

\[
 L\subseteq\mathcal R_E                           \tag{6}

maximizing `v_a(L)` subject to every other residual recipient's already
protected floor, allowing the unused complement to remain in charity. Give

\[
 Z_a=A^-+L.                                       \tag{7}

If `v_a(Z_a)>F_a`, the displaced source is paid without cutting the anchor.
Any observer failure against the enlarged target (7) gives a globally
minimal labeled response; if every target is safe, the resulting allocation
is an EFX lexicographic improvement.

If even the complete residual pool cannot pay `a`, then

\[
 v_a(A^-)+v_a(\mathcal R_E)\le F_a.               \tag{8}

Since `v_a(A)>F_a`, cancellation gives the exact full-pool capture

\[
 v_a(J)-v_a(\mathcal R_E)
 \ge v_a(A)-F_a>0.                                \tag{9}

Equation (9), not the stronger inequality with `R_q` alone, is the genuine
anchor-preserving separator. It proves that no redistribution using only
currently unused residual goods can restore the displaced source. The next
operation must split/replace the response, release another selected core, or
invoke a third-owner component exchange that changes a protected floor.

## Strictness of the correction

The audit supplies positive rational data satisfying:

\[
 v_a(A)>F_a,
 \qquad v_a(A^-+R_q)<F_a,
 \qquad v_a(A^-+R_q+R_r)>F_a.                     \tag{10}

It also makes `E` current-desired/current-safe for the root and keeps `K_r`
disjoint. Thus the formerly advertised `R_q` failure can occur while the
complete signed residual pool immediately repairs the collision. This is a
structural counterexample to the claim that root-sourced compensation has a
sole `R_q` gate; it is not a globally maximal GG countermodel.

## Claim boundary

This lemma proves the complete residual accounting, physical disjointness,
global selector, exact failure inequality, and strict incompleteness of the
`R_q`-only test. It does not force (7) to be paid in every GG state, eliminate
the full-pool capture (9), pay a supplier-saturated mixed cycle, close GG, or
prove four-agent/general additive EFX.
