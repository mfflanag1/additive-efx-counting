# Source-margin root-budget frontier lemma

**Date:** 2026-08-11

**Status:** cap-free global two-row selector for every captured-source packet;
only a third-owner connected fork can cross the terminal exchange-stable cut

## Setting

Let `A` be a common-safe desired core for source `a`, with strict margin

\[
 \mu=v_a(A)-v_a(X_a)>0.
\]

Let `P` contain the current root-side pool together with every packet already
fixed on the root side from the other selected core. Assume there is some
`C_0 subseteq A` such that

\[
 v_r(P+C_0)\ge v_r(X_r).                            \tag{1}
\]

Minimal dual-pool extraction supplies such a packet whenever the source-`a`
part of the extraction is being compensated. Its captured-margin branch
additionally has `v_a(C_0)>=mu`, but the selector below does not freeze that
particular extraction.

## Global two-row selector

Consider every pair

\[
 C\subseteq A,
 \qquad B\subseteq P                                \tag{2}
\]

whose exchange

\[
 P'=P-B+C,
 \qquad A'=A-C+B                                    \tag{3}
\]

pays the root:

\[
 v_r(P')\ge v_r(X_r).                               \tag{4}
\]

The finite feasible family is nonempty by (1). Choose a pair `(C,B)`
maximizing `v_a(A')`. Put

\[
 \sigma=v_r(P')-v_r(X_r)\ge0                       \tag{5}
\]

for the selected root surplus.

Exactly one of the following holds.

1. **Source restored.** If `v_a(A')>v_a(X_a)`, both rows are paid. If `A'`
   is common-safe, the root-paid selector reapplies. If it is unsafe, a
   globally minimal desired deletion supplies the existing response
   augmentation.
2. **Exchange-stable blockade.** If `v_a(A')<=v_a(X_a)`, the source remains
   captured, but the selected cut satisfies all three exact properties
   below.

### Every boundary good is root-critical

For every `c in C`, returning `c` to its original source would improve row
`a`. Optimality therefore forces

\[
 v_r(c)>\sigma.                                     \tag{6}
\]

Likewise, for every unused root-pool good `g in P-B`, giving `g` to `a`
would improve row `a`, so

\[
 v_r(g)>\sigma.                                     \tag{7}
\]

Otherwise the corresponding one-good move preserves (4) and strictly raises
the selected objective by positivity.

### Every root-affordable swap has the opposite source order

For `c in C` and `b in B`, returning `c` to `a` while returning `b` to the
root changes root value by `v_r(b)-v_r(c)`. Hence

\[
 v_r(b)\ge v_r(c)\quad\Longrightarrow\quad
 v_a(b)\ge v_a(c).                                  \tag{8}
\]

For `h in A-C` and `g in P-B`, moving `h` to the root and `g` to `a` gives
the second cut inequality

\[
 v_r(h)\ge v_r(g)\quad\Longrightarrow\quad
 v_a(h)\ge v_a(g).                                  \tag{9}
\]

Indeed, violating either conclusion produces another root-paid pair in (2)
with strictly higher `a`-utility.

## Consequence

The selector already ranges over every split, enlargement, reduction, and
one-for-one replacement of the original extraction inside `A+P`. Thus a
terminal source-margin capture is no longer repairable by changing the
two-row packet choice. It is an exchange-stable cut with:

1. every directly movable boundary good larger than the entire root slack;
2. both directions of every root-affordable swap weakly aligned against a
   source improvement; and
3. the source still at or below base.

The smallest operation not represented in this family is a transfer through
a third owner. Such an owner may accept a root-expensive good while releasing
a different packet to the captured source, producing the branching topology

\[
 \mathrm{charity}\to r,
 \qquad r\to\{q,a\},
 \qquad a\to b.
\]

That is exactly the four-owner repair found in the frozen adversarial profile
and accepted by the surplus-budgeted connected-component endpoint theorem.

## Scale and support compatibility

All feasibility comparisons use row `r`, and all objective comparisons use
row `a`. Independent positive scaling preserves the selected frontier and
(6)--(9). Equation (3) conserves physical support and connects the old source
core to the root pool. Any third-owner continuation therefore joins the same
physical transfer component.

## Verification and boundary

[`source_margin_root_budget_frontier_audit.json`](source_margin_root_budget_frontier_audit.json)
checks the payment identities and all four one-good/swap changes symbolically;
the maximality implications are the finite-selector argument above.

This lemma supplies the strongest deterministic operation available within
the two affected valuation rows. It does not select the third-owner fork in
every exchange-stable blockade, prove its surplus inequalities from the GG
premises, close unsafe/hitting-set recurrence, close `GG`, or prove four-agent/
general additive EFX.
