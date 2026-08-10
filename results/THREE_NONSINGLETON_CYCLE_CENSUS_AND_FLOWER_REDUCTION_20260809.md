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

At the level of a single selected cover, this low-payment family is the
remaining gate. Comparing alternative covers closes part of it immediately.

## Four-cover strict-cycle lemma

The one-unpaid theorem selected one cover per cell, but many cells admit
several covers with the same unpaid recipient. Those alternatives close a
further 148 source/order cells without any additive packet identity.

> **Lemma 7 (payment menu).** Fix an agent `u` and a finite menu of
> lex-valid one-unpaid covers, all with unpaid recipient `u`. If, for every
> strict ordering of the non-singleton bundles appearing in the menu, some
> cover assigns `u` a bundle maximal among that cover's assigned bundles,
> then at least one cover is EFX and lexicographically improving.

**Proof.** Suppose every cover fails EFX. All fixed or improving recipients
meet every tail because the assigned bundles are common-safe, so only `u`
can fail. If `P` is her payment in a failed cover, then

\[
v_u(P)<\tau_u(W)<v_u(W)
\]

for some other nonsingleton bundle `W` in that cover; a singleton has zero
tail and cannot witness failure. Thus every menu row forces its payment
strictly below another displayed bundle. But in the row whose payment is
maximal under the actual strict `u`-ordering, no such inequality is
possible. \(\square\)

The exact low-wall audit asserts simultaneous failure of every lex-valid
one-unpaid cover. It finds 148 UNSAT and 284 SAT cells in the deliberately
relaxed independent-total/tail abstraction. Every UNSAT cell has a
deletion-minimal four-cover payment menu, and the 148 certificates reduce to
only six canonical clause types, with deterministic multiplicities
`44,44,18,18,12,12`.
See
[`three_nonsingleton_flower_abstract_low_wall_audit.json`](three_nonsingleton_flower_abstract_low_wall_audit.json)
and
[`three_nonsingleton_flower_payment_menu_audit.json`](three_nonsingleton_flower_payment_menu_audit.json).

Combining Theorem 5 and Lemma 7 closes 580 of the 864 flower source/priority
cells. The remaining 284 cells admit an abstract simultaneous-wall model.
Those models are not asserted additively realizable, so they refute no EFX
claim; they identify exactly where packet additivity or generalized PI
routing must enter.

## Additive and true-tail boundary

Linking `A_q,A_r` additively to the six top/bottom packets, while retaining
arbitrary common-safe tail variables, does not close another cell. This
remains true after imposing the cap-free lower bound that the tail of a
bundle split into two nonempty packets dominates either entire packet: the
sound relaxation again returns 148 impossible and 284 satisfiable cells.
See
[`three_nonsingleton_flower_additive_low_wall_audit.json`](three_nonsingleton_flower_additive_low_wall_audit.json).
Thus bundle-total additivity alone is not the missing invariant.

### Cap-free packet-minimum support theorem

The exact minimum of a union of nonempty packets is the minimum of their
packet minima. Introducing one arbitrary total and one arbitrary positive
minimum per nonempty packet therefore represents every displayed EFX tail
exactly, without bounding packet cardinality.

Write

\[
A_q=(A_q\cap T_q)\mathbin{\dot\cup}(A_q\cap B_r),\qquad
A_r=(A_r\cap T_r)\mathbin{\dot\cup}(A_r\cap B_q),
\]

and call a desired bundle **crossing** when both intersections are nonempty.
Say the pair **fully captures `X_q`** when
`T_q subseteq A_q` and `B_q subseteq A_r`, and **fully captures `X_r`**
when `B_r subseteq A_q` and `T_r subseteq A_r`.

> **Theorem 8 (packet-minimum normal form).** In the flower family with arm
> source `r` and singleton envier `c`, simultaneous failure of every
> lex-valid common-safe cover has the following necessary form.
>
> 1. If the two bottom-edge sources are opposite (`c,s` or `s,c`), both
>    `A_q` and `A_r` are crossing.
> 2. If both bottom edges are sourced by `c`, both bundles are crossing and
>    either they fully capture `X_q`, or `c` precedes `r` and they fully
>    capture `X_r`.
> 3. If both bottom edges are sourced by `s`, both bundles are crossing and
>    either they fully capture `X_q`, or `s` precedes both `r,c` and they
>    fully capture `X_r`.
>
> Swapping `r,q` gives the four arm-source-`q` statements.

The proof exhausts the nine possible nonempty support types of `A_q,A_r`,
all feasible empty/nonempty residual masks, and all 24 priorities. Each cell
uses arbitrary packet totals and exact packet minima. Across the four
arm-source-`r` patterns, 5,124 of 6,144 support/order cells are QF_LRA-UNSAT;
the remaining 1,020 agree exactly with the three clauses above. The compact
replay is
[`three_nonsingleton_flower_packet_min_family_audit.json`](three_nonsingleton_flower_packet_min_family_audit.json).

This is a cap-free computer-assisted structural theorem, subject to an
independent encoding audit. It does not close the crossing/capture normal
forms. Those forms are now the analytic exchange-component gate; arbitrary
desired subsets outside them are eliminated.

### Full-capture exchange witness

A frozen positive two-good-per-component realization of the universal
full-`X_q` capture case survives every allocation in the common-safe cover
menu. Exact optimization nevertheless finds a lex-improving EFX allocation
at distance two. It swaps one good

\[
h\in A_q\cap B_r
\]

from `r` with one good

\[
b\in A_r\cap B_q=B_q
\]

from `q`; `c,s` remain fixed and `f` remains unallocated. For priority
`r,q,c,s`, agent `r` improves and `q` loses slightly. The transfer graph is
one connected `r--q` component, exactly aligned with the two external bottom
edges. See
[`three_nonsingleton_flower_full_q_capture_witness.json`](three_nonsingleton_flower_full_q_capture_witness.json)
and
[`three_nonsingleton_flower_full_q_capture_improvement.json`](three_nonsingleton_flower_full_q_capture_improvement.json).

This bounded witness does not prove that a two-good swap always succeeds.
The initially proposed analytic statement—either some priority-directed
bottom-crossing swap is EFX, or its blockers immediately close a PI
cycle—is now exactly refuted. A source-safe improving swap can have an
external blocker whose generalized edge lacks release support.

The exact one-good-per-displayed-component cell adds the true
minimum-good formula for every tail. In that bounded cell 316 of the 432
one-unpaid cases are impossible and 116 remain satisfiable. The surviving
cases occupy only eight source patterns. Ninety-six of them have
`a=c`, arm source `r` or `q`, and opposite bottom-edge sources; the other 20
are smaller same-source or singleton-arm boundary families.

The atomic master also blocks every owner-improving one-floater swap and
every priority-directed one-good transfer. These extra maximality constraints
do not change the `316/116` split. Therefore the 116 models are not artifacts
of omitting either local move. The frozen audit is
[`three_nonsingleton_flower_atomic_low_wall_audit.json`](three_nonsingleton_flower_atomic_low_wall_audit.json).
This is bounded proof-mining evidence, not a cap-free theorem.

One representative SAT model has source/order key

\[
(h,a,\alpha,\beta;\pi)=(r,c,c,s; r,q,c,s).
\]

Exhaustive exact optimization finds its nearest lex-improving EFX move at
distance two: transfer the atomic good `tq_rest` from `q` to `r`, release
`aq_br` from `r`, keep `f` unallocated, and leave `c,s` fixed. Agent `r`
improves before the losing agent `q`. This move lies outside the common-safe
cover menu and is a generalized one-in/one-out exchange, not another
one-good transfer. See
[`three_nonsingleton_flower_atomic_witness_improvement.json`](three_nonsingleton_flower_atomic_witness_improvement.json).

This witness is the stopping rule against a fixed-radius search. Blocking
radius one merely exposes a radius-two exchange, just as the earlier general
campaign found larger connected transfer components. The correct next
object is the component or generalized-edge structure of the exchange.

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

Prove a **component-growth lemma** for full-`X_q` capture. For the earlier
mutual-cycle owner, begin with swaps between goods in
`A_q intersect B_r` and `B_q` (and the symmetric pair when `q` is earlier),
but treat every blocker edge as a dependency whose incoming good still needs
release support. Follow that dependency across owners until the connected
component yields a lex-improving EFX allocation, a release-compatible PI
edge set, or an impossible strict item-order cycle. Then lift the same
argument to the priority-restricted full-`X_r` dual and the opposite-source
crossing case. The proof must allow arbitrary packet sizes and component
length; no fixed item radius is claimed.

For components incident to charity, the packet-for-charity replacement
lemma gives the required signed step: replacing `R subseteq X_q` by `f`
either improves EFX with charity, produces a target edge with
`v_i(f)>v_i(R)`, or produces a charity wall with the reverse inequality.
Together with the variable-charity hybrid-wall theorem, this reduces the
live gap to selecting a first improving packet/component from the flower's
champion data.

The exact model and nearest three-good escape establishing this correction
are documented in
[`FULL_CAPTURE_SWAP_PI_GATE_REFUTATION_20260810.md`](FULL_CAPTURE_SWAP_PI_GATE_REFUTATION_20260810.md).

Closing the flower settles only the `GG` row of the eight-class census. It
does not by itself eliminate the other seven three-nonsingleton classes.

Primary interfaces: BCFF Observation 2.8, Definition 3.4, Corollary 3.6,
and Theorem 3.16, [arXiv:2102.10654](https://arxiv.org/abs/2102.10654).
