# Row-Merge Valuation-Ranked Path Gate

**Status:** one natural source-wise minimum selector exactly refuted at cap
20; the union of all three trace-surviving selectors remains undecided  
**Scope:** four positive-additive agents, nine goods, the generic one-edge
wall

\[
01\mid23\mid45\mid678,
\]

with wall and post-wall feasibility graphs

\[
G^-=
\begin{pmatrix}
1&1&1&0\\
0&1&0&1\\
0&1&1&0\\
0&1&0&1
\end{pmatrix},
\qquad
G^+=
\begin{pmatrix}
0&1&1&0\\
0&1&0&1\\
0&1&1&0\\
0&1&0&1
\end{pmatrix}.
\]

**Not claimed:** a refutation of all adaptive Hall-blocker paths, the full
515-partition exchange-chain candidate, row-merge continuation, or complete
additive EFX

## Candidate selector

A source-wise minimum policy is a tuple

\[
(a_0,a_1,a_2,a_3).
\]

For each of the 24 oriented Hamiltonian paths through the four bundles, move
from source bundle (s) a good minimizing agent (a_s)'s value within that
source. All tied minima are admitted. This turns the 264 good-level
Hamiltonian-path actions into a small, valuation-dependent menu.

Exact mining over 23 stored wall models tested global, source-only,
target-only, and directed-edge policies using row minima, row extrema, and
row-sum extrema. No global or target-only row-minimum rule covers the trace.
Exactly three source-only row-minimum policies use the minimum possible two
distinct criteria and cover all 23 models:

\[
(0,0,0,1),\qquad (0,1,0,1),\qquad (0,0,0,3).
\]

This classification is exact for the frozen trace, not a theorem about all
wall profiles. It is reproduced by
[row_merge_q4_valuation_selector_mining_v2.json](row_merge_q4_valuation_selector_mining_v2.json).

## Exact generic-wall refutation

The most natural policy ((0,0,0,3)) asks agent 0 to choose the least-valued
good in each two-good source and agent 3 to choose the least-valued good in
the three-good source. A conditional QF_LIA CEGAR master found the following
generic-wall cap-20 refutation after three SAT rounds and 11 learned action
conditions:

\[
V^-=
\begin{pmatrix}
1&19&20&11&19&2&3&3&11\\
3&1&16&6&5&10&1&2&20\\
1&16&1&20&18&2&5&7&3\\
4&1&6&17&1&11&3&3&20
\end{pmatrix}.
\]

The post-wall matrix changes only entry ((0,2)), from 20 to 21. The
feasibility graph changes only edge ((0,0)), from present to absent. All 16
base pivots fail. Ties generate 42 selected Hamiltonian actions, and every
one fails. Nevertheless, 17 other simple-chain partitions support EFX, and
the profile has 428 complete EFX allocations across 281 partitions.

Thus the result refutes a repair selector, not EFX existence. The frozen
model and formula are
[row_merge_q4_ranked_path_0003_generic_cap20_cegar.json](row_merge_q4_ranked_path_0003_generic_cap20_cegar.json)
and
[row_merge_q4_ranked_path_0003_generic_cap20_cegar.smt2](row_merge_q4_ranked_path_0003_generic_cap20_cegar.smt2).

## Three-policy union boundary

The union of all three trace-surviving policies is harder and is not
refuted. Its generic-wall cap-20 CEGAR run completed 12 SAT rounds and learned
100 conditional action obstructions. The next master returned `unknown`
after its configured 60-second limit. The last exact SAT model still had two
selected supporting actions, 26 supporting simple-chain partitions, and 417
complete EFX allocations.

The exact endpoint is
[row_merge_q4_ranked_path_trace_union_generic_cap20_cegar.json](row_merge_q4_ranked_path_trace_union_generic_cap20_cegar.json).
The timeout is neither evidence for nor against the union selector.

## Correction provenance

The first exploratory runs fixed only (G^+). Their decoded profiles crossed
a second feasibility edge at the same step, so they were not evidence for a
generic single wall. Those JSON files are retained with explicit
`SUPERSEDED_NONGENERIC_TWO_EDGE_REFUTATION` status. The promoted runs
hash-bind and constrain both (G^-) and (G^+); the solver-free audit checks
that the unique graph change is ((0,0):1\to0).

The aggregate audit is
[row_merge_q4_ranked_path_gate_audit.json](row_merge_q4_ranked_path_gate_audit.json).

## Consequence for the proof strategy

The natural static source-rank rule is not enough to determine the exchange
goods, even after the topology has been expanded to every Hamiltonian path.
The three-policy union is still a live bounded possibility, but it has not
produced a theorem. A first adaptive successor has also now been tested:
recompute a minimal Hall blocker, fill the current hole from its neighborhood,
and repeat along a simple path. Exact solver-free replay finds five failures
among 25 distinct generic frozen profiles. See
[ROW_MERGE_ADAPTIVE_HALL_PATH_GATE.md](ROW_MERGE_ADAPTIVE_HALL_PATH_GATE.md).

Thus even adaptivity needs more than the current blocker's bundle incidence.
A next cap-free rule would need valuation-slack lookahead, a source outside the
current Hall neighborhood, or a non-path exchange, together with a
well-founded potential. The frozen refutations remain the mandatory
falsification suite.
