# Row-Merge Three-Exchange Chain Gate

**Status:** full candidate remains open; selected topology compressions are
exactly refuted at cap 20, and the latest bounded CEGAR pool has 80 cuts  
**Scope:** four positive-additive agents, nine goods, wall shape
(2+2+2+3), and a Hall-size-four small-step crossing  
**Not claimed:** a local pivot theorem, row-merge continuation, or general
complete EFX

## Candidate

Start from the wall partition

\[
01\mid23\mid45\mid678.
\]

A simple exchange chain chooses a directed simple path or cycle on the four
bundles, of length at most three, and moves one good from each source bundle
along its outgoing edge. A path is admitted only when its terminal source
bundle remains nonempty. Canonicalizing the resulting partitions gives 515
distinct candidates. This menu is much smaller than the full 1,889-partition
transfer-radius-three ball and has a direct cap-free definition, although its
maximum length is still fixed.

The candidate statement is that at least one of these 515 partitions supports
a complete EFX matching after the small wall step.

## Exact motif extraction

The terminal radius-two refutation profile has 123 EFX-supporting partitions
and 206 complete EFX allocations. Exactly 20 supporting partitions are nearest
to the failed wall partition, all at transfer distance three. Eight of those
20 are simple exchange chains in the menu above. Thus the first unbalanced
boundary is repaired by the intended motif, but one profile cannot prove the
candidate.

The complete alignment, transfer-edge, and EFX-matching census is frozen in
[row_merge_q4_distance3_exchange_m9_analysis.json](row_merge_q4_distance3_exchange_m9_analysis.json).

## Exact CEGAR boundary

The first master blocked the 16 earlier bundle pivots and the eight repairs
from the terminal profile. This 24-cut formula is SAT. Its exact model retains
48 simple-chain repairs. Blocking 32 of them creates a 56-cut formula on which
Z3 returned `unknown`; pinned cvc5 1.3.3 independently reached its 300-second
limit without a verdict. Hence neither solver proved or refuted the 515-state
candidate.

The first SAT model has the post-wall feasibility graph

\[
\begin{pmatrix}
0&1&1&0\\
0&1&0&1\\
0&1&1&0\\
0&1&0&1
\end{pmatrix}.
\]

Fixing this graph removes the graph-choice disjunction. At 32 cuts the branch
is SAT and has nine remaining exchange-chain repairs. The 36-, 40-, and
56-cut matching-clause rungs returned `unknown` at their stated limits. A
second 56-cut encoding using explicit Hall-witness selectors also returned
`unknown` after 180 seconds. An exhaustive differential over all 50,625
four-by-four graphs with nonempty rows confirms that the matching-clause and
Hall-selector obstruction encodings are equivalent.

These timeouts are not evidence of UNSAT. The exact status is therefore:

> The simple length-three exchange-chain candidate is neither proved nor
> refuted, even in this fixed nine-good Hall graph cell.

## Durable chain

- Motif classification:
  [row_merge_q4_distance3_exchange_m9_analysis.json](row_merge_q4_distance3_exchange_m9_analysis.json)
- 24-to-56 matching-clause CEGAR:
  [row_merge_q4_small_step_chain3_m9_cegar.json](row_merge_q4_small_step_chain3_m9_cegar.json)
- Normalized 56-cut formula and independent replay:
  [row_merge_q4_small_step_chain3_m9_cegar.cvc5.normalization.json](row_merge_q4_small_step_chain3_m9_cegar.cvc5.normalization.json)
  and
  [row_merge_q4_small_step_chain3_m9_cegar.cvc5.json](row_merge_q4_small_step_chain3_m9_cegar.cvc5.json)
- Fixed-graph 32-to-40 and 32-to-36 ladders:
  [row_merge_q4_small_step_chain3_m9_graph1212_ladder8.json](row_merge_q4_small_step_chain3_m9_graph1212_ladder8.json)
  and
  [row_merge_q4_small_step_chain3_m9_graph1212_ladder4.json](row_merge_q4_small_step_chain3_m9_graph1212_ladder4.json)
- Fixed-graph 56-cut matching and Hall encodings:
  [row_merge_q4_small_step_chain3_m9_graph1212_cegar.json](row_merge_q4_small_step_chain3_m9_graph1212_cegar.json)
  and
  [row_merge_q4_small_step_chain3_m9_graph1212_hall56.json](row_merge_q4_small_step_chain3_m9_graph1212_hall56.json)
- Solver-free aggregate audit:
  [row_merge_q4_exchange_chain_gate_audit.json](row_merge_q4_exchange_chain_gate_audit.json)

Reproduce the classifications and all semantic checks with:

```bash
make verify-row-merge-exchange-chain-gate
```

## Later cap-20 and topology boundary

Exact integer CEGAR at wall cap 20 produced SAT models through 76 cuts and
learned an 80-cut pool. The 80-cut solve ended `unknown/canceled`; it is not a
theorem verdict. Attempts to compress the surviving repairs by bundle-level
topology were then exactly falsified: all directed three-cycles, all simple
paths starting at the three-good bundle, and two successive minimum
two-topology covers can all fail even when combined with the 16 base pivots.
Each refuting profile still has complete EFX allocations and other simple
exchange-chain repairs.

The exact scope, models, and solver-free audit are in
[ROW_MERGE_TOPOLOGY_MINING_GATE.md](ROW_MERGE_TOPOLOGY_MINING_GATE.md).

## Next analytic unit

Topology-only selection is exhausted as a short explanation in this fixed
cell. A first valuation-aware compression using source-wise item minima is
also insufficient: the natural ((0,0,0,3)) rule is exactly refuted at cap
20 in the generic one-edge wall cell. The union of all three rules that
survive the 23-model trace remains undecided at a 100-cut boundary. See
[ROW_MERGE_RANKED_PATH_GATE.md](ROW_MERGE_RANKED_PATH_GATE.md).

The first direct adaptive version is also insufficient: filling the current
hole from the neighborhood of a recomputed minimal Hall blocker fails on five
of 25 distinct generic frozen models. A viable successor needs valuation-
slack lookahead, a source outside that neighborhood, or a non-path exchange.
See
[ROW_MERGE_ADAPTIVE_HALL_PATH_GATE.md](ROW_MERGE_ADAPTIVE_HALL_PATH_GATE.md).
