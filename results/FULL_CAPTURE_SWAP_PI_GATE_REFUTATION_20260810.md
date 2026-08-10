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

Exact allocation optimization proves that the nearest partial and complete
lex-improving EFX allocations both move three goods.

The nearest partial escape leaves `f` unallocated and forms the chain

\[
q\longrightarrow c\longrightarrow r\longrightarrow s:
\]

- `ar_bq_1` moves from `q` to `c`;
- `tc_1` moves from `c` to `r`; and
- `tr_rest_1` moves from `r` to `s`.

Agent `r`, first in priority, improves; `q` loses one unit at the integer
scale; `c,s` improve. The nearest complete escape swaps `tc_1` and
`aq_br_1` between `c,r` and gives `f` to `s`. Both have item distance three.
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

The three-good chain above is the smallest surviving motif that this theorem
must cover. A fixed item-radius bound is not part of the target.

## Claim boundary

This is an exact countermodel to one proposed proof mechanism, not to EFX
existence. The modeled state is not asserted globally lexicographically
maximal, and the result neither proves nor disproves the three-nonsingleton
flower theorem.
