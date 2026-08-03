# Residual-Threshold Matching Lemma

**Status:** exact analytic equivalence  
**Scope:** arbitrary nonnegative additive valuations  
**Not claimed:** that a suitable residual set always exists

## Lemma

Let \(N\) be a set of \(n\) agents and let the goods be partitioned as

\[
M=S\mathbin{\dot\cup}R,
\qquad |S|=n-1,
\qquad R\ne\varnothing.
\]

For each agent \(i\), define the residual threshold

\[
\rho_i(R)=v_i(R)-\min_{r\in R}v_i(r).
\]

Construct a bipartite graph \(G_R\) with agents on the left and the
singleton candidates \(S\) on the right. Put an edge \(i\sim g\) exactly
when

\[
v_i(g)\ge \rho_i(R).
\]

Then the partition

\[
\bigl\{\{g\}:g\in S\bigr\}\cup\{R\}
\]

supports a complete EFX allocation if and only if \(G_R\) has a matching
that saturates all \(n-1\) goods in \(S\).

Equivalently, by Hall's theorem, it supports EFX exactly when

\[
|N_{G_R}(Q)|\ge |Q|
\qquad\text{for every }Q\subseteq S.
\]

## Proof

Suppose first that \(G_R\) has a matching saturating \(S\). Give every
matched agent its matched singleton and give \(R\) to the one unmatched
agent.

An agent owning a singleton \(\{g\}\) cannot strongly envy another
singleton: removing that singleton's only good leaves the empty bundle.
Its comparisons against \(R\) hold because

\[
v_i(g)\ge \rho_i(R)
=\max_{r\in R}v_i(R\setminus\{r\}).
\]

The owner of \(R\) cannot strongly envy a singleton for the same
empty-bundle reason. These are all ordered comparisons, so the allocation
is EFX.

Conversely, suppose an EFX allocation is supported on this partition.
Every singleton good \(g\in S\) is owned by a distinct agent. If agent
\(i\) owns \(\{g\}\), its EFX comparisons against \(R\) imply

\[
v_i(g)\ge
\max_{r\in R}v_i(R\setminus\{r\})
=\rho_i(R).
\]

Thus every singleton-owner pair is an edge of \(G_R\), and those pairs form
a matching saturating \(S\). \(\square\)

## Four-agent, nine-good form

For four agents and nine goods, choose any six-good residual set \(R\).
The other three goods are singleton candidates. A complete EFX allocation
of shape

\[
6+1+1+1
\]

exists exactly when the resulting \(4\times3\) residual-threshold graph has
matching number three.

This is materially simpler than checking all EFX comparisons or all
agent--bundle permutations. Failure has only the three Hall forms:

1. some singleton candidate has no eligible agent;
2. some two singleton candidates collectively have at most one eligible
   agent; or
3. all three singleton candidates collectively have at most two eligible
   agents.

If one singleton candidate is a common favorite \(f\), every successful
matching isolates \(f\). The common-favorite condition is not needed for
the equivalence itself.

## Relation to the favorite-singleton reduction

The [favorite-singleton reduction](COMMON_FAVORITE_SINGLETON_REDUCTION.md)
removes a selected singleton owner and leaves a general three-agent EFX
selection problem. The present lemma chooses a particularly transparent
three-agent allocation: two more singleton bundles and one residual
bundle. All remaining selection conditions then collapse to one Hall
matching.

The new tight common-favorite search profile has exactly 18 complete EFX
allocations, supported by only two unlabeled partitions. One of those
partitions has shape \(6+1+1+1\), so this lemma explains its most extreme
repair branch exactly.

The tempting two-shape covering statement

\[
\text{balanced }(3,2,2,2)
\quad\text{or}\quad
\text{residual }(6,1,1,1)
\]

is false, even in the rank-distinct cap-13 common-favorite cell. The
identical-row profile

\[
(13,12,7,6,5,4,3,2,1)
\]

for all four agents has no EFX allocation of either shape. It nevertheless
has 480 complete EFX allocations on 20 unlabeled partitions: 12 of shape
\(3+3+2+1\), 5 of shape \(4+2+2+1\), and 3 of shape \(4+3+1+1\), all
isolating the common favorite.

Thus the residual-threshold lemma is an exact extreme-branch tool, not a
two-shape covering theorem. The broader balanced-or-favorite-singleton
conjecture survives this falsification.
