# Reused-top canonical-core selector lemma

**Date:** 2026-08-11

**Status:** cap-free elimination of every common-safe reused-top response
inside the removed-top/bottom reservoir; opposite-support and unsafe changes
remain open

## Fixed removed support

Let the later mutual owner hold the desired core

\[
 D(U)=(T_r\setminus U)+f,
 \qquad U\subseteq T_r.
\]

Let the nonempty finite response family be

\[
 \mathcal A(U)=\{(a,A):a\in\{c,s\},
 \ \varnothing\ne A\subseteq U+B_q,
 A\text{ is common-safe and desired by }a\}.         \tag{1}
\]

It includes full-`B_q`, proper-bottom, and changed-external-source cores.
Every member is disjoint from `D(U)`.

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
If it does not, (4) shows that every reused-top core in the same family
underpays the root. Switching among them cannot help and is discarded.

Any continuation must instead enlarge `U` with a fresh top good, leave the
support reservoir `U+B_q`, use an unsafe augmentation, or expose the
existing capture certificate.

## Well-founded consequence

Combine (2)--(4) with fresh-switch margin descent. A fresh switch strictly
enlarges `U` and decreases `q`'s positive response margin. At fixed `U`,
one canonical response core maximizes root payment across both external
sources and every common-safe subcore of `U+B_q`. Since `T_r` is finite,
this whole reused-reservoir branch cannot cycle. No item or value cap is
used.

## Verification and claim boundary

[`reused_top_canonical_core_selector_audit.json`](reused_top_canonical_core_selector_audit.json)
checks complement cancellation, root-pool maximality, and propagation of a
canonical deficit.

This lemma does not eliminate an unsafe core, a target supported outside
`U+B_q`, later return through the opposite `T_q+B_r` family, close `GG`, or
prove four-agent/general additive EFX.
