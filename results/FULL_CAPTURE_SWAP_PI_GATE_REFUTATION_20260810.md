# Full-capture immediate swap/PI gate refutation

**Date:** 2026-08-10

**Status:** exact bounded refutation of the immediate-closure mechanism;
the cap-free component-growth theorem remains open

## Refuted mechanism

In the full-`X_q` capture cell of the three-packet flower, consider every
priority-improving item swap between

\[
h\in A_q\cap B_r
\quad\text{and}\quad
b\in A_r\cap B_q=B_q.
\]

The proposed next lemma said that some such swap is EFX, or that the
generalized edge supplied by an external blocker immediately closes a BCFF
PI cycle with the existing flower edges. The second implication is false.

An external target-`r` blocker does give an edge

\[
i\xrightarrow{\{b\}\mid\{h\}}r.
\]

But this edge releases `h`, not its incoming good `b`. For example, pairing
it with the arm edge `r -f-> c` gives disjoint incoming sets `{b},{f}`, but
neither edge releases `b`: the blocker releases `h subseteq B_r`, while the
arm releases `B_c`. Hence BCFF Definition 3.4 is not satisfied. Edge
existence alone is not release compatibility.

## Exact surviving cell

The frozen two-good-per-component model has source/order key

\[
(h,a,\alpha,\beta;\pi)=(r,c,c,c;r,q,c,s)
\]

and full `X_q` capture. It simultaneously enforces:

1. positivity, base EFX, charity dominance, and the six displayed desired
   bundles;
2. failure of every lex-valid one-unpaid common-safe cover;
3. blockage of every EFX insertion of `f`;
4. blockage of every owner-improving `f`-for-item swap;
5. blockage of every priority-directed one-good transfer;
6. blockage of every priority-directed two-good exchange, both when the
   earlier owner's released good is discarded and when it is returned to
   the donor; and
7. blockage of all four bottom-crossing `r--q` swaps, while at least one
   pair is both `r`-improving and source-safe for `q`.

The cell is SAT. For each source-safe improving bottom swap, the model can
use `c` as an external target-`r` blocker. Thus neither ordinal alignment nor
radius-two exchange failure forces an immediate PI cycle.

The exact model is
[`three_nonsingleton_flower_full_capture_swap_gate.json`](three_nonsingleton_flower_full_capture_swap_gate.json).

## Smallest escape of the frozen model

Exact allocation optimization, now imposing owner-versus-charity dominance
as well as pairwise EFX, proves that the nearest partial and complete
lex-improving states both move three goods.

The nearest partial escape has one component on `q,c,charity`:

- `aq_tq_1` moves from `q` to charity;
- `ar_bq_1` moves from `q` to `c`; and
- `tc_0` moves from `c` to `q`.

Agents `r,s` are fixed and `q,c` improve; charity changes from `{f}` to
`{f,aq_tq_1}` and remains unenvied. The nearest complete escape moves
`ar_bq_1` from `q` to `c`, `bc_0` from `c` to `r`, and `f` to `s`.
Agent `r`, first in priority, improves; `q` loses one unit at the integer
scale; `c,s` improve. Both endpoints have item distance three.
See
[`three_nonsingleton_flower_full_capture_swap_gate_improvement.json`](three_nonsingleton_flower_full_capture_swap_gate_improvement.json).

## Corrected analytic target

The flower gate is therefore a **component-growth theorem**, not an
immediate swap/PI theorem. Start with an extremal bottom swap. Each failed
move supplies a signed generalized edge and a released good. Grow the
connected transfer component through the owner of the unsupplied incoming
good. Prove that growth either:

1. reaches an EFX allocation whose first changed owner improves;
2. closes a release-compatible PI edge set; or
3. revisits an owner with a strict cyclic item ordering, which is
   impossible.

The three-edge owner/charity component above is the smallest surviving motif
that this theorem must cover. A fixed item-radius bound is not part of the
target.

## Simple-path strengthening is also false

A second exact gate additionally blocks every three-good transfer whose
slot topology is a simple directed path through the four owners. It remains
SAT. Its nearest partial improvement still moves three goods, but its
connected transfer multigraph uses only the slots `q,charity`:

- `aq_tq_1` moves from `q` to charity;
- `ar_bq_1` moves from `q` to charity; and
- `f` moves from charity to `q`.

Thus one owner replaces two of her goods by `f`, with two parallel
`q--charity` releases and one return edge. It is not a simple path on
distinct owners and it changes charity cardinality from one to two. Its
nearest complete improvement moves seven goods in one component spanning all
five slots. The exact model and optimization are
[`three_nonsingleton_flower_full_capture_path_gate.json`](three_nonsingleton_flower_full_capture_path_gate.json)
and
[`three_nonsingleton_flower_full_capture_path_gate_improvement.json`](three_nonsingleton_flower_full_capture_path_gate_improvement.json).

Consequently the correct object is a connected transfer **multigraph** on
the four owner slots plus charity. The strengthened
[`GENERAL_TRANSFER_COMPONENT_HYBRID_WALL_LEMMA.md`](GENERAL_TRANSFER_COMPONENT_HYBRID_WALL_LEMMA.md)
now handles different charity cardinalities directly and proves that every
hybrid wall crosses to another slot component. What remains is not charity
balancing but endpoint construction: derive one globally feasible endpoint
multigraph from the flower's champion data rather than discovering it only
after solving a bounded model.

## Packet-selector strengthening is false

A third exact gate additionally blocks every owner-improving replacement of
an arbitrary nonempty owner packet by `f`, including failures caused by the
new charity packet. It remains SAT. Its nearest partial EFX-with-charity
improvement has one three-edge branching component on `r,c,s`:

- `r` sends `aq_br_0` to `s`;
- `r` sends `aq_br_1` to `c`; and
- `c` sends `tc_1` to `r`.

Owners `r,c,s` all improve and `q` is fixed. The nearest complete
improvement is the charity-side dual: `c` receives `f`, sends `bc_1` to `r`,
and sends `tc_1` to `s`. It also moves three goods and improves every changed
owner. The frozen model and optimization are
[`three_nonsingleton_flower_full_capture_packet_gate.json`](three_nonsingleton_flower_full_capture_packet_gate.json)
and
[`three_nonsingleton_flower_full_capture_packet_gate_improvement.json`](three_nonsingleton_flower_full_capture_packet_gate_improvement.json).

Thus the next primitive is a **hub-splitting component**: one slot receives
an incoming good or packet while releasing a packet partitioned among two or
more recipients. The cap-free
[`CHARITY_ROOTED_HUB_SPLIT_OBSTRUCTION_LEMMA_20260810.md`](CHARITY_ROOTED_HUB_SPLIT_OBSTRUCTION_LEMMA_20260810.md)
now converts every failed charity-rooted split into exact hub/leaf generalized
edges. The live remainder is selecting the split so that its wall graph
either closes a release-compatible directed cycle or cannot sustain its open
source/Hall-deficient component.
Linear paths and one-recipient packet replacements are both strictly too
narrow.

## Claim boundary

This is an exact countermodel to one proposed proof mechanism, not to EFX
existence. The modeled state is not asserted globally lexicographically
maximal, and the result neither proves nor disproves the three-nonsingleton
flower theorem.
