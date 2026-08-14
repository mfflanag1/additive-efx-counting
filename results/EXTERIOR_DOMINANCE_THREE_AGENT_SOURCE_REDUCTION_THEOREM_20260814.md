# Exterior-dominance three-agent source reduction theorem

**Date:** 2026-08-14

**Supersession (2026-08-14):** the full anchored `GG` state cannot reach the
exterior-dominant input, by the old-root-core contradiction. The source
analysis below remains conditionally correct but is no longer needed for the
retired-packet collision theorem.

**Status:** cap-free elimination of the one- and three-source faces and
reduction of the two-source face to an exact root-threshold debt

**Composition update (2026-08-14).**  The exterior-dominance premise is now
an unconditional survivor of the admitted global-exterior sacrifice theorem.
Consequently the source topology below is part of the live root-held
collision reduction, not merely a conditional analysis of a proposed test
allocation.

## Input

Let `X=(X_r,X_1,X_2,X_3;{f})` be the positive, bundle-nondegenerate,
globally fixed-priority lexicographically maximal one-charity EFX base.  Put

\[
 O=G\setminus X_r=X_1\mathbin{\dot\cup}X_2
   \mathbin{\dot\cup}X_3\mathbin{\dot\cup}\{f\}. \tag{1}
\]

Assume the remaining retired packet is base-contained and exterior-dominant:

\[
 \varnothing\ne K\subseteq X_r,
 \qquad
 v_r(O)<v_r(g)\quad(g\in K).                     \tag{2}
\]

In particular,

\[
 v_r(P)<v_r(X_r)
 \qquad(P\subseteq O),                            \tag{3}
\]

so the base root does not even plainly envy any possible nonroot bundle
formed from the exterior.

## The restricted three-agent instance

Discard the root row temporarily and view

\[
 (X_1,X_2,X_3;\{f\})                             \tag{4}
\]

as a partial allocation of `O` among the three nonroot agents.  It is EFX,
because it is a restriction of the four-agent EFX base.  Moreover every
nonroot agent pays the fixed root threshold:

\[
 v_i(X_i)\ge\tau_i(X_r)\qquad(i=1,2,3).          \tag{5}
\]

Let `E` be the ordinary envy graph of (4).

## Acyclicity from global maximality

If `E` has a directed envy cycle, rotate the bundles on that cycle.  The
standard envy-cycle rotation preserves EFX because bundle contents are only
permuted, and every participant on the cycle strictly improves.  The root
and charity are unchanged.  Equation (5) remains true because participant
utilities rise, and the root's comparisons are unchanged.

The resulting four-agent partial allocation is therefore EFX and
lexicographically above `X`, contradicting global maximality.  Hence

\[
 E\text{ is acyclic}.                             \tag{6}
\]

It has at least one source.

## Three sources close the four-agent state

Chaudhury, Garg, and Mehlhorn prove that if a three-agent partial EFX envy
graph has three sources, their Lemma 15 produces a complete EFX allocation
Pareto-dominating the partial allocation.

See [*EFX Exists for Three Agents*, Lemma
15](https://arxiv.org/abs/2002.05119).

Suppose therefore that `E` has three sources, and let
`(Y_1,Y_2,Y_3)` be the resulting complete EFX allocation of `O`, with

\[
 v_i(Y_i)\ge v_i(X_i)\qquad(i=1,2,3).           \tag{7}
\]

Fix the root at `X_r`.  The allocation

\[
 (X_r,Y_1,Y_2,Y_3)                                \tag{8}
\]

is complete EFX:

1. the three nonroot owners are mutually EFX by construction;
2. (5) and (7) protect every nonroot owner against the unchanged root
   target; and
3. for each `i`, (2)--(3) give
   `v_r(X_r)>v_r(O)>=tau_r(Y_i)`, so the root is protected against every
   nonroot target.

At least one inequality in (7) is strict.  Otherwise bundle nondegeneracy
would force `Y_i=X_i` for all three agents, leaving the positive good `f`
unallocated, contrary to completeness.  Thus (8) is lexicographically above
`X`, a contradiction.

## One source also closes

CGM Corollary 7 states that a three-agent partial EFX allocation with an
unallocated good and a single envy-graph source admits a complete EFX
allocation that Pareto dominates the partial allocation, with the source
strictly improved. Apply it to (4) and the unallocated charity good `f`, and
let `Y` be the resulting complete allocation of `O`.

The identical cross-comparison proof used for (8) applies. Pareto domination
preserves every nonroot threshold (5), while (2)--(3) protect the unchanged
root from every bundle contained in `O`. At least the unique source strictly
improves. Therefore `(X_r,Y_1,Y_2,Y_3)` is a complete EFX allocation
lexicographically above `X`, a contradiction. Hence the one-source face is
also impossible.

## Two sources: lex completion or exact root-threshold debt

For two sources, CGM Lemma 19 proves a complete internally EFX allocation
which **dominates in their fixed lexicographic potential**. It is not stated
as Pareto domination in the final hard subcases; the paper's Section 5
explicitly shows why such a strengthening is false in general.

Choose CGM's agent order to agree with the fixed global order restricted to
the three nonroot agents, and let `Y` be their Lemma 19 output. If

\[
 v_i(Y_i)\ge\tau_i(X_r)
 \qquad(i=1,2,3),                                 \tag{9}
\]

then the identical cross-comparison proof for (8) applies. The root is equal
to base, and the nonroot utility vector is lexicographically higher in the
restricted global order, contradicting global maximality.

Therefore every surviving two-source state carries the exact debt

\[
 \exists i\in\{1,2,3\}:\quad
 v_i(Y_i)<\tau_i(X_r).                            \tag{10}
\]

This is a root-target observer debt, not a failure of three-agent EFX.

## Exact surviving source topology

Combining (6) with the preceding branches, an exterior-dominant terminal has
an acyclic nonroot envy graph with exactly two sources and the CGM completion
debt (10). Section 5 of the same paper explains why the two-source result
cannot simply be strengthened to Pareto domination.

For three labeled vertices, the surviving two-source DAG family has only
finitely many edge topologies. The next collision step must exploit source identity,
the owner incurring (10), the named retirement supplier/current response
source, or the stronger GG champion edges; plain three-agent existence alone
cannot close them.

## GG identity refinement

In the frozen length-two `GG` flower, the external large owner `c` is a
source of the full ordinary envy graph. It remains a source after restricting
to the nonroot owners. Before the one-source closure, the possible source sets
are `{c}`, `{c,q}`, and `{c,s}`. The first is now impossible, so the surviving
source sets are exactly

\[
 \{c,q\}\qquad\text{or}\qquad\{c,s\}.           \tag{11}
\]

Both must carry the root-threshold debt (10). Thus the final
exterior-dominant collision is no longer anonymous: it is indexed by whether
the retirement supplier/current response source is `c`, the other source, or
the unique non-source/debt owner.

## Claim boundary

This theorem proves acyclicity, closes the one- and three-source cases using
the exact published Pareto-dominating results, gives the exact two-source
debt (10), and derives the two surviving GG source sets (11). It does not
prove that Lemma 19 preserves all root thresholds, route the debt owner through the retirement
supplier, eliminate the exterior-dominant packet, close `T_{L,times}^*`, or
prove four-agent/general EFX.
