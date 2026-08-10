# Three-nonsingleton cycle census and length-two flower reduction

**Date:** 2026-08-09

**Status:** cap-free structural reduction; it does not close the
three-nonsingleton branch

## Setting and notation

Work with four positive, nondegenerate additive agents at a PI-free,
globally lexicographically maximal one-charity partial EFX allocation. Three
allocated bundles are nonsingletons and the fourth is a singleton. Select
one incoming basic `f`-champion edge for each target, replacing a selected
edge by its parallel envy edge whenever its desired set discards `f`.

For a selected simple directed cycle write:

- `G` when the incoming edge of a nonsingleton target is a genuine selected
  `f`-champion edge;
- `L` when the incoming edge of a nonsingleton target is ordinary envy; and
- `S` when the incoming edge targets the unique singleton and is therefore
  ordinary envy.

Words are identified only up to cyclic rotation. Reflection is not used,
because the cycle is directed.

## Exhaustive eight-class census

A PI-free selected cycle contains at least two genuine edges. A genuine edge
cannot target the singleton, by the same charity-dominance argument used in
the exactly-two-nonsingleton composition. Direct enumeration gives exactly
the following eight classes:

| length | cycle word | external owners |
|---:|---|---|
| 2 | `GG` | one large, one singleton |
| 3 | `GGL` | singleton |
| 3 | `GGS` | one large |
| 3 | `GGG` | singleton |
| 4 | `GGLS` | none |
| 4 | `GGSL` | none |
| 4 | `GLGS` | none |
| 4 | `GGGS` | none |

The two adjacent words `GGLS` and `GGSL` are distinct directed classes;
they differ by the order of the large ordinary target and singleton target.
The exact enumeration is frozen in
[`three_nonsingleton_selected_cycle_census.json`](three_nonsingleton_selected_cycle_census.json).

None of these eight classes is literally covered by the four
exactly-two-nonsingleton cycle theorems. In `GG`, one external owner is now
large. In `GGS`, the external observer is large rather than singleton. In
`GGL`, the ordinary return targets a large bundle. The `GGG` and `GGGS`
classes have a third genuine edge, while every length-four class has only
one singleton target. Thus a contraction theorem, rather than a relabeling
of the old lemmas, is genuinely necessary.

## Length-two return-edge reduction

Consider the first class, with mutual genuine cycle

\[
r\xrightarrow f q\xrightarrow f r,
\]

external nonsingleton owner `c`, and singleton owner `s`. The two external
bottom-edge sources supplied by BCFF Theorem 3.16 lie in `{c,s}`.

> **Lemma 1 (return-edge reduction).** If both `c` and `s` have an incoming
> ordinary envy edge, the configuration contains a PI cycle and cannot be
> globally maximal.

**Proof.** The proof of the trapped-source length-two theorem uses
singletonness only to establish that each of the two external owners has an
incoming envy edge. Once those two edges are supplied, its distinct-source
and shared-source PI routings use only the two external bottom edges, one of
the two genuine `f`-edges, and ordinary envy edges. The same four-agent case
split therefore applies verbatim to external owners `c,s`. \(\square\)

The singleton `s` necessarily has an incoming envy edge: otherwise its
owner absorbs `f` and obtains a complete EFX allocation. Consequently:

> **Corollary 2.** Every surviving length-two three-nonsingleton state makes
> the external large owner `c` a source of the ordinary envy graph.

This source condition forces additional champion structure. BCFF
Observation 2.8 supplies an incoming basic `f`-champion of `c`. Its desired
set cannot discard `f`, because that would give an ordinary incoming envy
edge into `c`. Its source cannot be `c`, because a self-`f`-champion is a PI
cycle. Hence some `h in {r,q,s}` genuinely `f`-champions `c`. Its top and
bottom are both nonempty: an empty top would make `{f}` envied, while an
empty bottom would make `X_c+f` common-safe and would also make owner `c` a
self-champion.

We have therefore proved the following normal form.

> **Length-two flower reduction.** Every globally maximal obstruction in
> the `GG` class must contain three arbitrary-packet genuine edges
> \[
> r\xrightarrow f q,qquad q\xrightarrow f r,qquad
> h\xrightarrow f c,quad h\in\{r,q,s\},
> \]
> together with an ordinary edge `a -> s`, `a in {r,q,c}`, and the two
> external bottom edges of the mutual cycle, whose sources lie in `{c,s}`.

The flower has 36 source cells before priority is considered: three arm
sources, three singleton enviers, and four ordered choices of the two
bottom-edge sources. Across 24 fixed priority orders this gives 864 indexed
cells, but the intended proof target is a reservoir-order dichotomy rather
than an 864-row case proof.

## Direct flower swap

One arm/envy source pair closes without using either external bottom edge.

> **Lemma 3.** If `h=s` and `a=c`, the flower is not globally maximal.

**Proof.** Give `r,q` their original bundles, give `c` the singleton `{z}`,
and give `s` the arm's desired bundle `T_c+f`, leaving `B_c` unallocated:

\[
(Y_r,Y_q,Y_c,Y_s)=(X_r,X_q,\{z\},T_c+f).
\]

Every displayed bundle is common-safe at the base. Agents `r,q` are fixed,
while `c` strictly prefers `{z}` and `s` strictly prefers `T_c+f` by the two
source edges. The allocation is therefore EFX and Pareto improves the base,
contradicting global maximality. \(\square\)

The aggregate inequalities replay as QF_LRA-UNSAT in
[`three_nonsingleton_flower_direct_swap_audit.json`](three_nonsingleton_flower_direct_swap_audit.json).
Thus eight of the nine arm-source/singleton-envier pairs remain before the
two bottom-edge sources are considered.

## Four-source packet matching

Let `A_q` be the desired bundle supplied by the external
`(B_r|B_q)`-edge into `q`, and let `A_r` be the desired bundle supplied by
the external `(B_q|B_r)`-edge into `r`. Then

\[
A_q\subseteq T_q+B_r,qquad A_r\subseteq T_r+B_q.
\]

These two pools are disjoint from each other and from `T_c+f` and `{z}`.

> **Lemma 4.** If the arm source `h`, singleton envier `a`, and the two
> ordered bottom-edge sources are four distinct agents, the flower is not
> globally maximal.

**Proof.** Assign `T_c+f` to `h`, `{z}` to `a`, `A_q` to the source of the
first bottom edge, and `A_r` to the source of the second. The four bundles
are pairwise disjoint and common-safe, and every recipient strictly prefers
her assigned bundle. Hence the result is EFX and Pareto improves the base.
\(\square\)

Because the bottom sources lie in `{c,s}`, distinctness requires them to be
opposite and requires `(h,a)` to be either `(r,q)` or `(q,r)`. This closes
four additional source cells. Together Lemmas 3--4 close 8 of the 36 cells;
the exact grid
[`three_nonsingleton_flower_source_grid.json`](three_nonsingleton_flower_source_grid.json)
confirms that 28 source cells remain, or 672 source/priority cells before
order structure is compressed by these two initial allocations. The broader
cover theorem below supersedes that residual count.

## One-unpaid cover theorem

Include all three genuine desired bundles and the unchanged base bundles in
the common-safe support family:

| bundle | support | preferred recipient |
|---|---|---|
| `D_r` | `T_q+f` | `r` |
| `D_q` | `T_r+f` | `q` |
| `D_c` | `T_c+f` | arm source `h` |
| `Z` | `{z}` | envier `a` (or fixed owner `s`) |
| `A_q` | subset of `T_q+B_r` | left bottom-edge source |
| `A_r` | subset of `T_r+B_q` | right bottom-edge source |
| `X_r,X_q,X_c` | unchanged base supports | their owners |

Call a recipient **unpaid** when she receives a common-safe bundle that is
neither her old bundle nor one of the bundles she is known to desire.

> **Theorem 5 (one-unpaid cover).** For every one of the 36 flower source
> cells and every one of the 24 fixed priority orders, there is a disjoint
> four-bundle allocation from the table with one of the following forms:
>
> 1. every recipient is fixed or strictly improved; or
> 2. exactly one recipient is unpaid, that recipient is `r` or `q`, she
>    receives `A_q` or `A_r`, and a strictly improving recipient precedes
>    her in the fixed priority.

**Proof.** Enumerate assignments of four table rows to the four agents,
discard every assignment whose displayed packet supports overlap, and label
each recipient fixed, improving, or unpaid from the source cell. Select an
all-fixed-or-improving cover when available; otherwise select a one-unpaid
cover whose first improver precedes the unpaid recipient. The exact directed
enumeration checks all `36*24=864` cells. It finds 432 covers of each form
and no uncovered cell. In every one-unpaid cover the preferred selection
makes the unpaid recipient one of `r,q` and her assigned bundle one of
`A_q,A_r`. The enumeration is frozen in
[`three_nonsingleton_flower_one_unpaid_cover.json`](three_nonsingleton_flower_one_unpaid_cover.json).
\(\square\)

For a selected cover let

\[
\theta_u=\max_j\tau_u(Y_j)
\]

be the largest `u`-tail among its four assigned bundles.

> **Corollary 6 (high-payment escape).** Every all-fixed-or-improving cover
> contradicts global maximality. A one-unpaid cover also contradicts global
> maximality whenever `v_u(Y_u)>=theta_u`.

All assigned bundles are common-safe, so fixed or improving recipients meet
every tail at their old utility. The displayed inequality makes the unpaid
recipient EFX. The first changed recipient in priority is a strict improver,
so the allocation is lexicographically better. The 864 aggregate
implications replay as QF_LRA-UNSAT in
[`three_nonsingleton_flower_one_unpaid_lra_audit.json`](three_nonsingleton_flower_one_unpaid_lra_audit.json).

Consequently 18 complete source cells close for all orders immediately. The
other 18 source cells reduce, order by order, to a single strict wall

\[
v_u(A)<\theta_u,
\qquad u\in\{r,q\},\quad A\in\{A_q,A_r\}.
\]

This is the only remaining gate in the length-two flower topology. The
finite cover does not prove that the wall is impossible; that requires a
cap-free desired-subset extraction and an explicit generalized PI routing.

## Exact wall witness

The frozen profile
[`three_nonsingleton_length_two_return_wall.json`](three_nonsingleton_length_two_return_wall.json)
is positive and nondegenerate and its displayed partial allocation is EFX
with unenvied charity. It realizes:

- the mutual genuine cycle `r -f-> q -f-> r`;
- the third genuine arm `r -f-> c`;
- both external bottom edges sourced by `c`;
- `c -> s` as the singleton's sole incoming envy; and
- no incoming ordinary envy edge into `c`.

This exactly refutes the shortcut that the external large owner must satisfy
the singleton return lemma. The profile is not asserted globally maximal
and is not an EFX counterexample; it validates the necessity of using the
third champion arm in any cap-free proof.

## Next analytic gate

Close the strict low-payment wall in Corollary 6. Extract a minimal desired
subset from the union of the unpaid external bundle and the tail attaining
`theta_u`, then route every possible source through an explicit generalized
PI cycle or a second one-unpaid cover. The argument must allow extra graph
edges and arbitrary packet sizes. An equal-vector contraction is unavailable
under nondegeneracy: equality of every owner's utility forces every assigned
bundle to be unchanged.

Closing the flower settles only the `GG` row of the eight-class census. It
does not by itself eliminate the other seven three-nonsingleton classes.

Primary interfaces: BCFF Observation 2.8, Definition 3.4, Corollary 3.6,
and Theorem 3.16, [arXiv:2102.10654](https://arxiv.org/abs/2102.10654).
