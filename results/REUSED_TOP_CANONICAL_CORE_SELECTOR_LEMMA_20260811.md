# Reused-top canonical-core selector lemma

**Date:** 2026-08-11

**Status:** cap-free canonicalization of every common-safe external response
disjoint from the current mutual core; fresh mutual-core removal, unsafe
augmentation, and root-sourced responses remain open

## Fixed removed support

Let the later mutual owner hold the desired core

\[
 D(U)=(T_r\setminus U)+f,
 \qquad U\subseteq T_r.
\]

Let `C(U)` be the full complement of `D(U)` in the complete owner union plus
`f`.  Define the nonempty finite response family

\[
 \mathcal A(U)=\{(a,A):a\in\{c,s\},
 \ \varnothing\ne A\subseteq C(U),
 A\text{ is common-safe and desired by }a\}.         \tag{1}
\]

The known external bottom edge makes the family nonempty.  It includes both
external sources, full- and proper-bottom cores, the opposite `T_q+B_r`
family, residual-response cores, and every other common-safe external core
disjoint from `D(U)`.

Choose

\[
 (a^*,A^*)\in\arg\min_{(a,A)\in\mathcal A(U)}v_r(A).\tag{2}
\]

Use deterministic tie-breaking. Let `P(A)` be the complement of `D(U)` and
`A` in the complete owner union plus `f`.

## Root-pool maximization

For any two response cores $A,A'\in\mathcal A(U)$, cancellation gives

\[
 v_r(P(A'))-v_r(P(A))=v_r(A)-v_r(A').                \tag{3}
\]

Therefore

\[
 v_r(P(A^*))\ge v_r(P(A))
 \qquad((a,A)\in\mathcal A(U)).                     \tag{4}
\]

If `P(A^*)` pays `r`'s base utility, the root-paid dual selector applies.
If it does not, (4) shows that every common-safe external core disjoint from
`D(U)` underpays the root. Switching source, bottom packet, residual target,
or opposite-bottom family cannot help and is discarded simultaneously.

Any continuation must instead enlarge `U` with a fresh top good, leave the
external-source family by using the root as source, use an unsafe
augmentation, or expose the existing capture certificate.

## Well-founded consequence

Combine (2)--(4) with fresh-switch margin descent. A fresh switch strictly
enlarges `U` and decreases `q`'s positive response margin. At fixed `U`,
one canonical response core maximizes root payment across every common-safe
external response disjoint from `D(U)`. Since `T_r` is finite, the external
rank-two repair/reset branch cannot cycle while removed support is retained.
No item or value cap is used.

## Verification and claim boundary

[`reused_top_canonical_core_selector_audit.json`](reused_top_canonical_core_selector_audit.json)
checks complement cancellation, root-pool maximality, and propagation of a
canonical deficit.

This lemma does not prove that every later operation retains `U`, eliminate
an unsafe or root-sourced core, terminate the fresh-packet `q`-capture
handoff, close `GG`, or prove four-agent/general additive EFX.
