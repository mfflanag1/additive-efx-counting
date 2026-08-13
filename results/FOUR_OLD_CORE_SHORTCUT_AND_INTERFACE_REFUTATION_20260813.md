# Four-old-core shortcut and interface refutation

**Date:** 2026-08-13

**Status:** cap-free contradiction to the stated paid-response splice normal
form; the actual mixed-edge GG import must be reconstructed

## Shortcut theorem

Let `X` be a partial EFX allocation of four agents.  Suppose there are four
pairwise-disjoint bundles `(A_i)_{i in N}` such that

\[
 v_i(A_i)>v_i(X_i)                                \tag{1}
\]

for every source `i`, and

\[
 \tau_h(A_i)\le v_h(X_h)                          \tag{2}
\]

for every observer `h` and target `i`.  Define the partial allocation

\[
 Y_i=A_i.                                         \tag{3}
\]

Physical disjointness makes (3) an allocation.  For `h != i`, equations
(1)--(2) give

\[
 v_h(Y_h)>v_h(X_h)\ge\tau_h(A_i)=\tau_h(Y_i).     \tag{4}
\]

Thus `Y` is EFX.  Equation (1) says that it Pareto dominates `X`, and hence
strictly improves every fixed lexicographic owner order.  Goods outside the
four cores may remain unallocated; the EFX inequalities compare owner
bundles, not their union with charity.

This is the same elementary implication stated for current-safe cores in
`CURRENT_SAFE_FULL_RESPONSE_MATCHING_ENDPOINT_LEMMA_20260811.md`, specialized
to base-common-safe cores.

## Conflict with the deletion-return normal form

The current deletion-return manuscript states simultaneously that:

1. the Hamiltonian path has one assigned core `A_i` for every source;
2. all four `A_i` are base-common-safe desired cores;
3. the matching places them in distinct physical targets; and
4. `X` is globally lexicographically maximal among partial EFX allocations.

Items 1--3 satisfy the shortcut theorem.  Its allocation `Y` contradicts
item 4 before the decorated hole response `D`, deletion remainder `P`, or
rank-completing splice is considered.  Consequently no globally realizable
GG state satisfies the stated local normal form.

The two positive-rational referee witnesses do satisfy items 1--3, and the
audit now explicitly constructs `Y`.  Both are EFX and improve every owner.
This is why they were correctly labeled local rather than globally maximal.

## Published-definition check

Berger--Cohen--Feldman--Fiat define a generalized champion's desired bundle
so that its source envies it while no agent strongly envies it.  Their
Lemma 3.4 uses compatible desired bundles on a PI component to construct a
Pareto-improving partial EFX allocation.  Their Definition 2.1 and Lemma 2.2
permit progress to any dominating partial EFX allocation; they do not impose
a one-good bound on the new charity during an individual improvement.

Therefore “one charity good at the base” does not rescue the four-old-core
normal form.  If all four cores are simultaneously physical and disjoint,
their unused complements can be unallocated in the shortcut allocation.

Primary source: Berger, Cohen, Feldman and Fiat, *Almost Full EFX Exists for
Four Agents*, AAAI 2022, Definitions 2.1 and 3.1 and Lemmas 2.2 and 3.4.

## Required interface correction

A genuine mixed-margin Hamiltonian terminal must drop at least one shortcut
premise.  The smallest plausible corrected import is:

- only three path edges have pairwise-disjoint base-common-safe desired
  cores; and
- the fourth edge is the recurrent core `D`, which is only current-safe and
  may carry positive base-safety debt.

Alternatively, if four generalized edges are retained, their incoming
packets are not simultaneously available/disjoint and the exact overlap and
release labels must replace the current target-partition assertion.

Until one corrected import is derived from the original GG flower, the
rank-completing paid-response splice is resolved **vacuously under its stated
premises** but cannot be used to claim GG closure.  The next necessary task
is not another packet selector: it is to reconstruct which path edge is
mixed, its actual physical support, and the three old cores that remain
simultaneously available.

## Claim boundary

This theorem refutes the consistency of the stated splice interface and
proves an immediate EFX/Pareto endpoint whenever its four-old-core premises
hold.  It does not prove that the actual GG derivation supplies those
premises, reconstruct the corrected mixed matching, close GG, or prove
four-agent/general additive EFX.
