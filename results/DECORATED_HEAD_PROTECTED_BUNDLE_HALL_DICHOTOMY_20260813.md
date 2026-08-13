# Decorated-head protected-bundle Hall dichotomy

**Date:** 2026-08-13

**Status:** cap-free reduction of the one-/two-head mixed-cycle exchange to a
deficiency-one whole-bundle Hall witness

## Protected acceptance graph

Let `Z=(Z_i)_{i in N}` be the paid residual-completed mixed-cycle allocation.
Every owner is strictly above the globally maximal base `X`. Let `H` be the
decorated-head blocker set after old-incoming self-response progress has been
excluded. The localization theorem gives

\[
 1\le |H|\le2.                                   \tag{1}
\]

For each agent define the complete protected threshold

\[
 \lambda_i=
 \max\left\{v_i(X_i),\ \max_{j\in N}\tau_i(Z_j)\right\}.             \tag{2}
\]

Construct a bipartite graph from agents to the four whole candidate bundles:

\[
 i\sim j\quad\Longleftrightarrow\quad
 v_i(Z_j)\ge\lambda_i.                           \tag{3}

An edge means that assigning the intact bundle `Z_j` to `i` preserves her
base floor and pays every EFX comparison against every intact candidate
bundle.

## Forced edges

Every non-head `i notin H` accepts her own bundle. Indeed she is not a
blocker, so

\[
 v_i(Z_i)\ge\max_j\tau_i(Z_j),
\]

and the paid candidate gives `v_i(Z_i)>v_i(X_i)`. Thus

\[
 i\sim i\qquad(i\notin H).                       \tag{4}

Every head has a nonempty acceptance row. Choose `j*` maximizing the total
value `v_i(Z_j)`. Since `i` blocks some target `Z_k`,

\[
 v_i(Z_{j^*})\ge v_i(Z_k)>	au_i(Z_k)>v_i(Z_i)>v_i(X_i).             \tag{5}

Moreover `v_i(Z_{j^*})` is at least every target total and hence every
deletion threshold. Therefore `i sim j*`. Since `i` blocks something,
`i` does not accept its own bundle at threshold (2); every accepted head
edge used below is nonidentity.

## Matching branch

If (3) has a perfect matching `pi`, assign `Z_{pi(i)}` to agent `i`. Whole
bundles are merely permuted, so feasibility and physical release support are
unchanged. Equations (2)--(3) give EFX and weak base payment for every owner.
Every head receives utility strictly above its old paid candidate utility by
(5), so at least one owner is strict. This is an EFX Pareto—and therefore
lexicographic—improvement over `X`, contradicting global maximality.

## Hall branch

If no perfect matching exists, take an inclusion-minimal Hall-deficient
source set `S`. Every subset containing only non-heads has their distinct
identity targets in its neighborhood by (4). Hence

\[
 S\cap H\ne\varnothing.                          \tag{6}

Minimality gives Hall's condition on every proper deletion of `S`, so

\[
 |N(S)|=|S|-1.                                   \tag{7}

Thus failure is not an unstructured payment wall. It is a deficiency-one
protected-bundle Hall witness containing at least one decorated head.

For one head, the witness is a closed alternating set containing that head:
the head accepts only bundles already claimed by the non-head identity rows
inside the set, and no whole-bundle permutation can free a bundle for it.
For two heads, the same statement holds with one or both heads in the
witness. The exhaustive graph audit checks every admissible labeled relation
and classifies minimal witnesses by size and head content.

## Consequence

The generic instruction “pay the supplier-saturated mixed cycle” is replaced
by an exact dichotomy:

1. permute the four intact paid bundles using a protected perfect matching,
   obtaining an EFX lexicographic contradiction; or
2. enter a deficiency-one Hall witness containing a decorated head.

In the second branch every whole-bundle operation is exhausted. The smallest
missing operation must split a bundle inside the witness, release a selected
core, use charity, or change a protected floor. The alternating minimal-
response lemma supplies candidate-safe head-sourced subcores for precisely
this packet-level continuation.

## Claim boundary

This lemma proves the protected graph construction, forced identity/head
edges, matching endpoint, head-containing deficiency-one Hall certificate,
and exhaustive four-owner graph classification. It does not prove that every
Hall witness admits a packet split, eliminate the one-head closed star or
two-head witness, compose the root full-pool capture, close GG, or prove
four-agent/general additive EFX.
