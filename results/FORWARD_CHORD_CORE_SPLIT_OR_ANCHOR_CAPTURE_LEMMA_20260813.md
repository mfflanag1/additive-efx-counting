# Forward-chord core split or anchor-capture lemma

**Date:** 2026-08-13

**Status:** cap-free reduction of every full-prefix forward response to a
same-source replacement, a paid two-core split, or one of two exact
root-anchor capture interfaces; the former `R_q`-only reservoir is corrected
to the complete signed residual pool

## Forward response geometry

Use the genuine selected path

\[
 h_0\to h_1\to h_2\to h_3\to c,                 \tag{1}
\]

with selected source core `K_i` lying in target `Y_{h_{i+1}}`.  At the
full-prefix state, let source `b=h_k` have a globally minimal current
response

\[
 E\subseteq Y_{h_l},\qquad k<l.                  \tag{2}
\]

The selected core already occupying that target is

\[
 A=K_{l-1},\qquad a=h_{l-1}.                     \tag{3}
\]

Put `J=E intersect A`.  The response core `E` and remainder `A-J` are
physically disjoint.

## Adjacent forward response

If `l=k+1`, then `a=b` and `A=K_k`: the new response and the selected core
belong to the same source. Replacing `A` by `E` creates no displaced source
and no target-rank loss. Because `E` is current-desired, its source is paid
strictly above `Y_b`; because it is globally minimal, it is current-safe.
The complete core/target/release label is either new finite augmentation or
an exact same-source recurrent replacement.

This includes the adjacent root response into q. The old physical anchor
core remains recorded inside the same q target even when the selected root
core is replaced by the newer current response.

## Nonadjacent response and generic compensation

Assume `l>=k+2`, so `a!=b`.  Let `F_a` be the priority-valid protected floor
of displaced source `a`, and suppose

\[
 v_a(A)>F_a.                                      \tag{4}
\]

Source `b` no longer needs its former selected core `K_k`, because `E` alone
is worth strictly more than `Y_b`.  For every `L subseteq K_k`, consider

\[
 Z_b=E,
 \qquad Z_a=(A\setminus J)+L.                    \tag{5}

All other selected cores remain unchanged.  The bundles in (5) are
disjoint. If some `L` satisfies `v_a(Z_a)>F_a`, choose an inclusion-minimal
one. Both affected sources are paid, and any unsafe enlarged target `Z_a`
produces a new labeled current/base response. Thus a successful `L` is a
paid forward-chord conversion, not a matching-label reset.

If even `L=K_k` fails, additivity and (4) give the exact capture inequality

\[
 v_a(J)-v_a(K_k)
 \ge v_a(A)-F_a>0.                                \tag{6}

The response overlap captures the displaced source's entire strict selected-
core margin even after crediting the whole freed source core. No proper
subpacket selector inside `K_k` can repair this branch.

## Permanent-anchor exceptions

Assume the selected path contains the permanent edge `r -> q`.

1. **Anchor-target collision.** If `h_l=q`, then `A=K_r` is the permanent
   anchor core. Put `R_q=Y_q-K_r`. When `J` is empty, (2) is disjoint from
   the anchor and the two cores coexist. When `J` is nonempty, first delete
   the complete overlap. If `E-J` remains current-desired, it is a disjoint
   response and the exact anchor survives. Otherwise `J` captures the
   response source's complete strict current margin:
   \[
    v_b(J)\ge v_b(E)-v_b(Y_b)>0.                  \tag{7}
   \]
   Since `E-J subseteq R_q`, exact retention of both `E` and `K_r` is then
   physically impossible. The terminal is the simultaneous response/anchor
   hitting set `J`; the smallest operation is a replacement response in
   `R_q`, or explicit anchor release and reconstruction.
2. **Anchor-source release.** If `b=r` and `l>position(q)`, then the freed
   core `K_k=K_r` is the permanent anchor. Retain it with the root response.
   In the selected-core allocation every target residual is unallocated, so
   the physical compensation family is not just `R_q`. After removing any
   residual atoms consumed by `E`, put
   \[
    \mathcal R_E=(\mathop{\dot\bigcup}_{i\in N}R_i)\setminus E.
   \]
   It is disjoint from the anchor, response, and retained selected cores and
   contains `R_q`. Run the compensation selector over
   `L subseteq mathcal R_E`. If no `L` pays `a`, complete-pool failure is
   \[
    v_a(J)-v_a(\mathcal R_E)\ge v_a(A)-F_a>0.     \tag{8}
   \]
   The `R_q`-only formulation is strictly false: another target residual can
   repair a collision that `R_q` cannot. Thus the remaining obligation is
   full-pool capture, not a q-only reverse inequality.

These are the only anchor exceptions. Across the six Hamiltonian paths
containing adjacent `r -> q`, the 36 forward source/target orders split as:

| class | count |
|---|---:|
| adjacent same-source replacement | 18 |
| nonadjacent anchor-target collision | 6 |
| nonadjacent anchor-source release | 6 |
| generic nonadjacent split | 6 |

Thus the forward-chord problem no longer requires an anonymous adaptive
root/order theorem. Its only unresolved inputs are the response/anchor
hitting set and the complete-residual-pool capture.

## Claim boundary

This lemma proves the path indexing, disjoint split, source/displaced-owner
payment identities, whole-core and complete-residual-pool failure
inequalities, and exhaustive anchored identity classification. It does not
force a compensation packet to exist, eliminate the two anchor exceptions
with GG maximality, pay every external observer of the changed target, close
the backward-cycle branch, close GG, or prove four-agent/general additive
EFX. See
[`ROOT_SOURCED_COMPLETE_SIGNED_RESIDUAL_COMPENSATION_LEMMA_20260813.md`](ROOT_SOURCED_COMPLETE_SIGNED_RESIDUAL_COMPENSATION_LEMMA_20260813.md).
