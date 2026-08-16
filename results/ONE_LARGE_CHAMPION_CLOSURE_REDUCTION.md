# One-large generalized-champion closure reduction

**Status:** cap-free structural theorem and maximal-obstruction exclusion  
**Scope:** four nondegenerate positive-additive agents, arbitrary hub-bundle
size, one charity good  
**Boundary:** closes every singleton-target branch and reduces every
remaining `f`-cycle to one hub-bottom packet; it does not exhaust that packet

## Setup

Let

\[
X_h=A,\qquad X_j=\{s_j\}\quad(j\ne h)
\]

be an EFX allocation with one unallocated good `f`. Assume charity
dominance

\[
v_i(X_i)\geq v_i(f)\qquad(i\in N). \tag{1}
\]

For an `f`-champion edge \(i\xrightarrow{f}j\), fix its BCFF desired set
\(Q\subseteq X_j\cup\{f\}\): agent `i` strictly prefers `Q` to `X_i`, and
no agent strongly envies `Q`. Its corresponding discard is

\[
D=(X_j\cup\{f\})\setminus Q.
\]

## Singleton-target collapse

> **Singleton-target lemma.** If \(X_j=\{s_j\}\), every selected
> `f`-champion witness has exactly one of two forms:
>
> 1. \(Q=\{s_j\}\) and \(D=\{f\}\). Then `i` ordinarily envies `j`, so
>    the champion edge can be replaced by the clean envy edge `i -> j`.
> 2. \(Q=\{s_j,f\}\) and \(D=\varnothing\). Then `j` is itself a clean
>    self-`f`-champion, and assigning \(\{s_j,f\}\) to `j` completes EFX.

**Proof.** The desired set is a nonempty subset of \(\{s_j,f\}\). It
cannot be \(\{f\}\), because (1) says that the source does not strictly
prefer `f` to her own bundle. If it excludes `f`, it is exactly
\(\{s_j\}\), so the source envies `j`; a singleton is never strongly
envied after removal of a good, making the ordinary envy edge valid.

If the desired set includes `f`, it must be the full pair. Since no agent
strongly envies that pair and positive additivity makes owner `j` strictly
prefer it to \(\{s_j\}\), `j` is also a most-envious agent for the pair.
Giving the pair to `j` makes her better off, leaves all other own bundles
unchanged, and introduces a target block that no agent strongly envies.
The old EFX inequalities cover every unchanged target, proving complete
EFX. \(\square\)

The same final observation applies to any target: if an `f`-champion's
desired set is the entire \(X_j+f\), then owner `j` cleanly self-champions
and direct absorption completes. Thus every genuine unresolved `f`-edge
has a nonempty discard from its target bundle.

## Hub-target form

For an edge entering the hub, either `f` is discarded or retained.

- If `f` is discarded, the source envies a subset of `A` and hence envies
  `A`; replace the champion edge by the ordinary envy edge to `h`.
- If `f` is retained, write

  \[
  Q=T\mathbin{\dot\cup}\{f\},\qquad
  A=T\mathbin{\dot\cup}B. \tag{2}
  \]

  Charity dominance rules out \(T=\varnothing\). The edge inserts `f` and
  releases exactly the proper hub-bottom packet \(B\subsetneq A\). If
  \(B=\varnothing\), the full-target observation completes EFX.

## All cycle lengths collapse to the hub bottom

Choose one incoming `f`-champion for every target and take any simple
directed cycle `C` in the resulting four-vertex graph. Apply the two
replacements above to its edges.

If an edge into a singleton retains `f`, the singleton-target lemma already
completes EFX. Otherwise every singleton-target edge of `C` becomes an
ordinary envy edge. There are then only three possibilities:

1. `C` omits the hub, so every edge of `C` is an envy edge;
2. `C` contains the hub but its incoming edge discards `f`, so again every
   edge is an envy edge; or
3. `C` contains the hub, its incoming edge retains `f`, and this is the
   only edge of `C` that consumes `f`. Every other edge is an envy edge.

The first two cases are ordinary envy cycles. Rotating their bundles
preserves EFX and (1), strictly improves every cycle owner, and preserves
the one-large bundle-size shape. Repeating such rotations terminates because
only finitely many assignments of the same four blocks exist.

The third case is a BCFF basic Pareto-improvable cycle: it has one
`f`-champion edge and otherwise envy edges. Lemma 3.5 assigns its desired
blocks, producing a partial EFX allocation that strictly Pareto dominates
`X`. Its exact unallocated set is the hub bottom `B` from (2). In the
closed-hyperflow notation,

\[
\mathop{\dot\bigcup}H_e=\{f\},\qquad
\mathop{\dot\bigcup}L_e=B.
\]

Thus this basic cycle is a closed/no-discard certificate exactly when
\(B=\varnothing\). If `B` is nonempty, its closure defect is exactly `B`;
there are no singleton-bottom packets.

The four possible cycle lengths now have no separate valuation cases:

| cycle length | vertices after excluding direct completion | result |
|---:|---|---|
| 1 | singleton | clean self-absorption |
| 1 | hub | self-`f` edge releasing `B` |
| 2 | two singletons | envy-cycle rotation |
| 2 | hub plus one singleton | one hub `f` edge, one envy edge, residue `B` |
| 3 | three singletons | envy-cycle rotation |
| 3 | hub plus two singletons | one hub `f` edge, two envy edges, residue `B` |
| 4 | hub plus three singletons | one hub `f` edge, three envy edges, residue `B` |

This proves the cap-free reduction:

> **One-large champion reduction.** From every state satisfying the setup,
> either direct absorption completes EFX, an eligible envy-cycle rotation
> gives strict one-large progress, or a one-`f` basic PI cycle gives strict
> Pareto progress and leaves exactly one proper nonempty subset
> \(B\subsetneq A\) unallocated.

## Extra structure of the residual packet

After eliminating envy cycles, let `p` be the source of the genuine hub
edge. If the cycle is a self-loop, `p=h`; otherwise the absence of a
parallel envy edge gives

\[
v_p(X_p)\geq v_p(A).
\]

In both cases championship of \(T+f\) yields

\[
v_p(T)+v_p(f)>v_p(X_p)\geq v_p(T)+v_p(B),
\]

and hence

\[
v_p(f)>v_p(B). \tag{3}
\]

The PI endpoint is itself EFX with collective charity dominance over `B`.
Choose any \(t\in T\). Original EFX against the hub gives, for every
nonhub observer `q`,

\[
v_q(X_q)\geq v_q(A\setminus\{t\})\geq v_q(B),
\]

while the hub trivially values `A` at least as much as `B`. Every owner
weakly improves on the PI cycle, so each terminal own bundle also weakly
dominates `B`. The residual is therefore not arbitrary: it is a proper
hub packet, is collectively charity-dominated, and lies strictly below `f`
in the root champion's row.

If \(|B|=1\), the PI endpoint remains a one-large allocation with one
charity good: the large target loses one good and gains `f`, and all other
targets remain singleton. It also strictly Pareto dominates the previous
state. Consequently, finite repetition gives either complete EFX or a
residual with \(|B|\geq2\). In particular, the setup is complete whenever
\(|A|\leq2\).

The exact remaining **hub-bottom exhaustion gate** is to consume all of
`B` through compatible incoming-clean generalized-champion edges while
routing every later release. In the notation of
[`CLOSED_CHAMPION_HYPERFLOW_GATE.md`](CLOSED_CHAMPION_HYPERFLOW_GATE.md),
one must extend or replace the basic cycle until

\[
\mathop{\dot\bigcup}H_e=\{f\}\mathbin{\dot\cup}
\mathop{\dot\bigcup}L_e.
\]

The singleton analysis removes three independent bottom packets from this
gate; only descendants of one subset of the hub bundle remain.

## Consequence for a globally maximal obstruction

Fix an agent order and choose a lexicographically maximal partial EFX
allocation among all partial EFX allocations of a four-agent instance. In a
hypothetical instance with no complete EFX allocation, BCFF Theorem 5.1
implies that this maximum has at most one unallocated good: two or more
would admit a strictly dominating EFX allocation. It has exactly one good
`f`, and no agent envies it. Otherwise the minimal-envied-subset move in
BCFF Lemma 2.4 gives a Pareto-dominating partial EFX allocation. Thus (1)
holds.

For the open regime with at least five positive goods, all four allocated
bundles are nonempty. If one were empty, EFX and positivity would force
every other allocated bundle to be a singleton, leaving at least two goods
unallocated, contrary to maximality.

If this global maximum had at most one nonsingleton allocated bundle, the
one-large champion reduction would give either a complete EFX allocation or
a strictly dominating partial EFX allocation. Both contradict the assumed
noncomplete global maximum. Therefore:

> **Maximal-obstruction theorem.** In a positive-goods instance with at
> least five goods, every globally lexicographically maximal noncomplete
> four-agent partial EFX allocation has exactly one unenvied charity good
> and at least two nonsingleton allocated bundles.

This is a genuine cap-free exclusion of the entire one-large obstruction
shape. It is not a proof of complete four-agent EFX: after a multi-good
bottom is released, BCFF can make further lexicographic progress, but its
return to one charity need not preserve the one-large shape.

## Exactly two nonsingleton bundles

The same argument gives a sharp description of the next maximal shape.
Suppose a globally maximal noncomplete state has exactly two nonsingleton
targets. Fix one incoming `f`-champion witness per target. Then every cycle
in that selected graph satisfies:

- every edge entering a singleton is an ordinary envy edge, since retaining
  `f` there would complete;
- a nonsingleton-target edge that discards `f` is likewise replaceable by
  an envy edge; and
- a cycle with zero genuine `f` edges is an envy cycle, while a cycle with
  exactly one genuine `f` edge is a basic PI cycle.

Either kind of cycle strictly dominates the global maximum. Hence every
selected `f`-cycle must contain both nonsingleton targets, and both incoming
edges must genuinely retain `f`. Neither has a parallel envy edge, and both
release nonempty bottom packets; an empty bottom would give clean direct
absorption. The only possible cycle lengths are therefore 2, 3, and 4,
with respectively zero, one, and two replaceable singleton envy edges.

This names the next residual as the **two-genuine-edge recycling gate**:
two target edges request the same sole charity good, so one must be replaced
by generalized championship using packet released by the other.

BCFF Theorem 3.16 applies directly only to the length-two subcase. There are
no self-`f` champions at a noncomplete maximum, and the two genuine cycle
edges have no parallel envy edges. On two vertices these facts verify every
clause of BCFF Definition 3.9, so the two nonsingleton agents form a good
`f`-cycle. For bottom `B_a`, an internal good edge has the forced orientation
`a --B_a--> b`; together with the opposite edge `b --f--> a`, which releases
`B_a`, it is a PI two-cycle. Maximality therefore forces the source of each
bottom edge supplied by Theorem 3.16 to lie among the two external singleton
agents. The two edges need not have distinct sources. For lengths three and
four,
the singleton-target edges discard `f` and have parallel envy edges. Those
cycles are not good cycles under BCFF Definition 3.9, so Theorem 3.16 cannot
be invoked on them. Treating their singleton bottoms as empty
`f`-decompositions would be a quantifier error: an edge that discards `f`
does not induce an `f`-decomposition at all.

Thus current edge discovery does not yet reduce all maximal two-large
obstructions to the length-two pattern. The remaining theorem must either
replace the singleton envy segments before applying good-cycle discovery or
discover a clean cross-bottom edge without assuming a good `f`-cycle.

## Primary source

Berger, Cohen, Feldman, and Fiat,
[*Almost Full EFX Exists for Four Agents (and Beyond)*](https://arxiv.org/abs/2102.10654),
Sections 2.3 and 3 for championship, Lemma 2.4 for the minimal-envied-subset
move, and Theorem 5.1 for strict progress from at least two unallocated
goods.

The state-level maximality and champion-graph statements above use BCFF's
nondegenerate convention. Their Appendix A perturbation is sufficient for
existence theorems but does not automatically preserve a designated tied
maximal state or its selected champion graph. Extending this structural
normal form verbatim to tied nonnegative profiles therefore requires an
explicit state-preserving tie wrapper; no such extension is claimed here.

