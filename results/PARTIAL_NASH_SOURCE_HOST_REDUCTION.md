# Maximum-Nash Bundle Cycles and the Source-Host Reduction

**Status:** proved cap-free reduction; the subsequent floater-support chain is
open  
**Scope:** any positive-additive instance for which the eligible one-floater
family is nonempty  
**Role in the general goal:** applies in particular to the four-agent
almost-complete EFX state supplied by Berger--Cohen--Feldman--Fiat

Let \((X,f)\) be EFX with exactly one unallocated good \(f\), and assume

\[
v_i(X_i)\ge v_i(f)\qquad\text{for every agent }i.
\tag{E}
\]

Call such a state *eligible*. For positive valuations, all own-bundle
utilities in an eligible state are positive.

## Bundle-cycle improvement lemma

Let \(a_0,\ldots,a_{k-1}\) be distinct agents, with indices read modulo
\(k\). Suppose

\[
v_{a_t}(X_{a_{t+1}})\ge v_{a_t}(X_{a_t})
\qquad (t=0,\ldots,k-1).
\tag{1}
\]

Rotate the bundles backward around the cycle, so that agent \(a_t\) receives
\(X_{a_{t+1}}\), while every other agent keeps its bundle and \(f\) remains
unallocated.

> **Lemma.** The rotated state is eligible and EFX. If at least one inequality
> in (1) is strict, its Nash product of own-bundle utilities is strictly
> larger.

For an observer outside the cycle, the own bundle and the set of target
bundles are unchanged; only target labels are permuted. For an observer
\(a_t\), own utility weakly increases. Every target other than the old own
bundle and the newly received bundle was already an EFX target. The newly
received bundle no longer needs to be tested against itself. The only new
target is the old own bundle, and

\[
v_{a_t}(X_{a_{t+1}})
\ge v_{a_t}(X_{a_t})
\ge v_{a_t}(X_{a_t}\setminus\{g\})
\]

for every \(g\in X_{a_t}\). Thus EFX survives. Condition (E) survives because
cycle agents weakly improve and the others are unchanged. The Nash statement
follows because every factor is positive, no factor decreases, and at least
one factor increases.

The two-agent equality swap observed at the annealing wall is the \(k=2\),
all-equalities case of this lemma. It is therefore a general handoff, not an
accident of that matrix.

## Acyclic strict envy at a Nash maximizer

Direct an edge \(i\to j\) when agent \(i\) strictly prefers bundle \(X_j\) to
its own bundle. If this digraph contained a directed cycle, the bundle-cycle
lemma would strictly increase Nash welfare while retaining eligibility.
Therefore:

> **Corollary 1.** The strict-envy digraph of every maximum-Nash eligible
> state is acyclic.

Every finite acyclic digraph has a vertex of indegree zero. Consequently some
agent \(h\) owns a *source bundle*:

\[
v_i(X_i)\ge v_i(X_h)\qquad\text{for every }i\ne h.
\tag{2}
\]

This is stronger than ordinary EFX comparison with \(X_h\): nobody strictly
envies the complete source bundle.

## Source-host blocker theorem

Suppose the floater cannot be inserted into any bundle of a maximum-Nash
eligible state, and choose a source owner \(h\).

First, \(X_h\) cannot be a singleton. If \(X_h=\{r\}\), then after inserting
\(f\), every other observer \(i\) dominates both possible one-good
remainders: (E) gives \(v_i(X_i)\ge v_i(f)\), while (2) gives
\(v_i(X_i)\ge v_i(r)\). Hence insertion into \(h\) would be EFX.

Because insertion into the nonsingleton \(X_h\) is blocked, some observer
\(i\ne h\) and removed good \(q\in X_h\cup\{f\}\) satisfy

\[
v_i(X_i)
<v_i\bigl((X_h\cup\{f\})\setminus\{q\}\bigr).
\tag{3}
\]

The removed good cannot be \(f\), since then (3) would say
\(v_i(X_i)<v_i(X_h)\), contradicting (2). Thus \(q=r\in X_h\), and

\[
v_i(X_h)
\le v_i(X_i)
< v_i(X_h)-v_i(r)+v_i(f).
\tag{4}
\]

In particular,

\[
v_i(f)>v_i(r).
\tag{5}
\]

> **Corollary 2 (source-host reduction).** Every hypothetical blocked
> maximum-Nash state has a nonsingleton source bundle. Every witness blocking
> insertion into that source removes an old host good \(r\) and supplies an
> observer that strictly prefers the floater \(f\) to \(r\).

This converts an arbitrary all-host obstruction into a genuine
floater-support edge. It also explains why the safe floater-exchange lemma
does not immediately finish the proof: the blocking observer is precisely an
agent that vetoes the unanimous comparison needed for that safe exchange.

## Verification

The permanent audit is
[bundle_cycle_source_lemma_audit.json](bundle_cycle_source_lemma_audit.json).
It contains:

- QF_LRA checks of the EFX/floater and source-blocker scalar implications;
- a QF_NRA check of strict Nash improvement;
- literal exhaustion of all 4,096 three-agent, four-good profiles over values
  \(\{1,2\}\), exercising 79,872 bundle cycles, 38,400 of them strict; and
- all 4,096 irreflexive digraphs on four vertices, including all 543 acyclic
  digraphs, to audit the source step.

Reproduce it with:

```sh
make verify-bundle-cycle-source
```

## Remaining gate

Starting from the source host \(h\), select a blocker \((i,r)\) supplied by
(4). Replacing \(r\) by \(f\) makes \(r\) the next floater, but may violate
EFX exactly at agents that rank \(f\) above \(r\). The
[floater-substitution path lemma](PARTIAL_NASH_SUBSTITUTION_PATH_LEMMA.md)
closes the case of a unique supporter reachable through weak bundle
preferences.

The broader local closure is false: an exact state has no strict bundle cycle
and no improving rematching among all 192 source substitutions, while still
having 1,780 larger global rivals. Consequently the missing theorem must use
global Nash maximality to produce one of:

1. a safe floater exchange with a strict Nash gain;
2. a strict bundle-improvement cycle; or
3. an equality bundle cycle leading to an insertable Nash maximizer.

Neither a fixed transfer radius nor the complete one-source-substitution
family can substitute for this step. The required comparison may reorganize
goods across the full allocation.
