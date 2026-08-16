# Row-Merge Exchange-Topology Mining Gate

**Status:** four natural topology-compressed menus exactly refuted at integer
cap 20; the full exchange-chain candidate remains open  
**Scope:** four positive-additive agents, nine goods, wall partition

\[
01\mid23\mid45\mid678,
\]

and the fixed post-wall Hall graph

\[
\begin{pmatrix}
0&1&1&0\\
0&1&0&1\\
0&1&1&0\\
0&1&0&1
\end{pmatrix}.
\]

**Not claimed:** a refutation of the 515-partition exchange-chain menu,
row-merge continuation, or complete additive EFX

## Basic picture

The failed wall partition has four bundles. A simple exchange action moves one
good along a directed path or around a directed cycle of bundles. There are
515 distinct partitions obtainable using at most three moves.

The solver trace repeatedly suggested that only a few *shapes* of exchange
might be needed. Each suggested shape was therefore promoted to an exact
statement: block all 16 previously known pair pivots, block every good-level
realization of the selected shapes, and ask whether a positive additive wall
profile can still exist. At cap 20 the answer was SAT in every promoted case.
Each SAT model is an exact counterexample to that compressed menu, but still
has many complete EFX allocations and other simple-chain repairs.

## Exact refutations

All wall item values in the following profiles are integers in
\(\{1,\ldots,20\}\). The post-wall step increases only good 2 in row 0; that
entry may therefore exceed 20.

| selected exchange menu | selected partitions | with base pivots | surviving simple-chain partitions | complete EFX allocations |
|---|---:|---:|---:|---:|
| every directed three-cycle | 80 | 96 | 44 | 686 |
| every length-1--3 path starting at bundle 678 | 117 | 130 | 19 | 542 |
| first minimum two-topology trace cover | 14 | 30 | 37 | 513 |
| second minimum two-topology trace cover | 18 | 34 | 15 | 381 |

The first minimum cover consisted of the cycle \(0\to1\to2\to0\) and path
\(3\to0\to2\). After its exact refutation was added to the trace, the next
minimum cover changed to the cycle \(0\to2\to3\to0\) and the same path.
That cover was exactly refuted as well.

The solver-free aggregate audit reconstructs every wall premise, fixed Hall
graph, blocked menu, full 515-partition support count, and complete EFX census:
[row_merge_q4_topology_mining_gate_audit.json](row_merge_q4_topology_mining_gate_audit.json).

## What survived proof mining

The final trace contains 23 exact SAT models. No individual good-level action
and no individual partition supports EFX in every model. The smallest
topology cover still has two shapes, but its distinct good-level menu grew
from 14 to 18 and then to 24 partitions as two adversarial countermodels were
added. The 24-partition third cover is an untested trace fit, not a conjecture
or theorem.

One broad empirical pattern survives: every stored model has a length-three
path touching all four bundles. This is the 264-partition Hamiltonian-path
family. Its survival is evidence that long exchange propagation matters, but
it is not enough compression to explain *which goods* should move.

The final exact trace classification is
[row_merge_q4_chain_topology_mining_final_analysis.json](row_merge_q4_chain_topology_mining_final_analysis.json).

## Full-candidate boundary

The full 515-partition statement is not refuted. On the cap-20 grid, CEGAR
found exact SAT models through 76 learned cuts and accumulated an 80-cut pool;
the 80-cut solve was canceled at the stopping point and records `unknown`.
Every preceding model retained between 7 and 14 unblocked chain repairs. See
[row_merge_q4_small_step_chain3_m9_graph1212_cap20_pool64.json](row_merge_q4_small_step_chain3_m9_graph1212_cap20_pool64.json).

Thus the correct boundary is:

> Exchange topology alone does not select a short universal repair menu in
> this fixed cell. The full length-three exchange-chain candidate remains
> open and requires a valuation-aware selection rule or a global argument.

## Durable artifacts

- Trace motif and minimum-cover analyzer:
  [`analyze_row_merge_q4_chain_trace.py`](../tracks/parkability/analyze_row_merge_q4_chain_trace.py)
- Exact menu decision generator:
  [`decide_row_merge_q4_cycle023_gate.py`](../tracks/parkability/decide_row_merge_q4_cycle023_gate.py)
- Solver-free aggregate auditor:
  [`audit_row_merge_q4_topology_mining_gate.py`](../tracks/parkability/audit_row_merge_q4_topology_mining_gate.py)
- All-three-cycle refutation:
  [row_merge_q4_all_three_cycles_plus_base_cap20_gate.json](row_merge_q4_all_three_cycles_plus_base_cap20_gate.json)
- All-paths-from-678 refutation:
  [row_merge_q4_all_paths_start3_plus_base_cap20_gate.json](row_merge_q4_all_paths_start3_plus_base_cap20_gate.json)
- Successive minimum-cover refutations:
  [round 1](row_merge_q4_min_topology_cover_plus_base_cap20_gate.json) and
  [round 2](row_merge_q4_min_topology_cover_round2_plus_base_cap20_gate.json)

## Next analytic unit

Do not promote another topology-only cover from the same trace. Static
valuation ranks have now been tested as the first successor. Exactly three
source-wise minimum policies cover all 23 stored models, but the natural
policy ((0,0,0,3)) has a fresh generic-wall cap-20 refutation. The union of
all three remains undecided after 100 conditional cuts and a 60-second
timeout. See [ROW_MERGE_RANKED_PATH_GATE.md](ROW_MERGE_RANKED_PATH_GATE.md).

The first direct Hall-blocker rule has now been exactly replayed and fails on
five of 25 distinct generic frozen profiles: the current minimal blocker's
neighborhood alone does not identify a safe source. The next candidate needs
valuation-slack lookahead, a source outside that neighborhood, or a non-path
exchange. See
[ROW_MERGE_ADAPTIVE_HALL_PATH_GATE.md](ROW_MERGE_ADAPTIVE_HALL_PATH_GATE.md).
The frozen topology and ranked-path refutations remain the mandatory
falsification suite.
