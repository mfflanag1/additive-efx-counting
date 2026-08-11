# Reused-top canonical-core selector lemma

**Date:** 2026-08-11

**Status:** cap-free elimination of fixed-source/fixed-bottom reused-top
cycling; source or core-shape changes remain open

## Fixed removed support

Let the later mutual owner hold the desired core

\[
 D(U)=(T_r\setminus U)+f,
 \qquad U\subseteq T_r.
\]

Fix an external source `a` and the nonempty finite family

\[
 \mathcal K(U)=\{K\subseteq U:
 K+B_q\text{ is common-safe and desired by }a\}.     \tag{1}

Choose

\[
 K^*\in\arg\min_{K\in\mathcal K(U)}v_r(K),           \tag{2}

with deterministic tie-breaking. Let `P(K)` be the complement of `D(U)`
and `K+B_q` in the complete owner union plus `f`.

## Root-pool maximization

For any two members (K,K'\in\mathcal K(U)), cancellation gives

\[
 v_r(P(K'))-v_r(P(K))=v_r(K)-v_r(K').                \tag{3}

Therefore

\[
 v_r(P(K^*))\ge v_r(P(K))
 \qquad(K\in\mathcal K(U)).                          \tag{4}

If `P(K^*)` pays `r`'s base utility, the root-paid dual selector applies.
If it does not, (4) shows that every reused-top core in the same family
underpays the root. Switching among them cannot help and is discarded.

Any continuation must instead enlarge `U` with a fresh top good, repartition
`B_q`, change the response source or core shape, use an unsafe augmentation,
or expose the existing capture certificate.

## Well-founded consequence

Combine (2)--(4) with fresh-switch margin descent. A fresh switch strictly
enlarges `U` and decreases `q`'s positive response margin. At fixed `U`,
one canonical core maximizes root payment and no reused-support switch is
useful. Since `T_r` is finite, the fixed-source full-`B_q` branch cannot
cycle. No item or value cap is used.

## Verification and claim boundary

[`reused_top_canonical_core_selector_audit.json`](reused_top_canonical_core_selector_audit.json)
checks complement cancellation, root-pool maximality, and propagation of a
canonical deficit.

This lemma does not eliminate a change of source, a proper-bottom or unsafe
core, later return through another target family, close `GG`, or prove
four-agent/general additive EFX.
