# Three-Agent-Bottom Pairing Conversion Theorem

**Status:** cap-free, proof-checked computer-assisted theorem  
**Scope:** four additive agents, nine goods, a strict common favorite, and
universal owner-threshold failure  
**Not claimed:** the full four-agent/nine-good branch, complete EFX for all
four-agent instances, or general additive EFX

## The theorem

Let $f$ be a strict favorite of all four agents. For each agent $i$, sort the
other eight singleton values as

\[
x_{i1}\ge\cdots\ge x_{i8},\qquad F_i=v_i(f),
\]

and assume

\[
x_{i5}+x_{i6}+x_{i7}>F_i,
\qquad
x_{i3}+x_{i7}>F_i\ \text{or}\ x_{i4}+x_{i5}>F_i. \tag{1}
\]

Suppose two residual goods $a,b$ are jointly bottom-two for any three of the
four agents. Thus, for some three-agent set $A$,

\[
\max\{v_i(a),v_i(b)\}
\le \min_{g\notin\{f,a,b\}}v_i(g)
\qquad(i\in A).                                        \tag{2}
\]

No order condition is imposed on the fourth agent. Fix any perfect pairing
$M=\{E,P,Q\}$ of the other six goods. At the favorite-triple threshold

\[
F_i+\max\{v_i(a),v_i(b)\},
\]

one of the following holds:

1. $M$ has a Hall matching to three distinct agents, so
   $\{f,a,b\}\mid E\mid P\mid Q$ supports EFX; or
2. at least one of the six converted partitions

   \[
   \{f,h\}\mid(R\cup\{\ell\})\mid S\mid T             \tag{3}
   \]

   supports EFX, where $(h,\ell)$ is either $(a,b)$ or $(b,a)$, $R$ is one
   edge of $M$, and $S,T$ are the other two edges.

The result strictly strengthens the common-bottom theorem: the fourth
agent may rank either low good anywhere below the common favorite.

## Counting consequence

Let $H_{a,b}$ be the number of Hall-valid perfect pairings in this
favorite-triple cell, and let $P_f$ be the total number of EFX-supporting
balanced partitions with $f$ in a pair. The same reconstruction injection
as in the common-bottom proof gives

\[
P_f+H_{a,b}\ge 15.                                    \tag{4}
\]

Every failed pairing has a converted repair, and a converted partition
uniquely reconstructs its source pairing. Hence, if $P_f=0$, all 15
pairings are Hall-valid and the cell is full. In particular, the entire
subbranch in which some pair is bottom-two for at least three agents is
closed.

## Exact proof structure

Goods symmetry fixes $(a,b)=(7,8)$ and
$M=\{\{1,2\},\{3,4\},\{5,6\}\}$. Agent symmetry fixes the three agents in
(2) as $0,1,2$. Hall failure has three canonical forms:

1. one edge has zero neighboring agents;
2. two edges have at most one common neighboring agent; or
3. all three edges have at most two common neighboring agents.

For the latter two forms, the omitted fourth agent can lie inside or outside
the canonical neighbor set. Five exact role cells therefore exhaust all
possibilities. Z3 returns `unsat` in every cell. More compactly, both the
sorting-free cardinal encoding and an independent sorting-network encoding
return `unsat` on the unsplit 21-witness formula with only the 36 order
inequalities in (2). Pinned cvc5 1.3.3 independently returns `unsat` on the
normalized sorting-network formula. It emits an 18,975,836-byte CPC proof
with 233,949 proof steps, and the separate Ethos 0.2.3 checker accepts the
proof as `correct`.

Primary records:

- [cardinal unsplit result](efx49_three_agent_bottom_pairing_conversion_cardinal_z3.json);
- [sorting-network unsplit result](efx49_three_agent_bottom_pairing_conversion_sorting_z3.json);
- [independent cvc5 replay](efx49_three_agent_bottom_pairing_conversion_sorting_cvc5.json);
- [CPC/Ethos certificate](efx49_three_agent_bottom_pairing_conversion_sorting_cpc_ethos.json);
- [checked CPC proof](efx49_three_agent_bottom_pairing_conversion_sorting.cpc);
- [zero-neighbor role cell](efx49_three_agent_bottom_zero_neighbor_z3.json);
- [two-edge, omitted nonneighbor](efx49_three_agent_bottom_two_edges_one_neighbor_z3.json);
- [two-edge, omitted neighbor](efx49_three_agent_bottom_omit_neighbor_two_edges_one_neighbor_z3.json);
- [three-edge, omitted nonneighbor](efx49_three_agent_bottom_three_edges_two_neighbors_z3.json); and
- [three-edge, omitted neighbor](efx49_three_agent_bottom_omit_neighbor_three_edges_two_neighbors_z3.json).

The proof-mining core
[efx49_common_bottom_conversion_zero_neighbor_order_core.json](efx49_common_bottom_conversion_zero_neighbor_order_core.json)
deletes all 12 order inequalities for one agent and retains all 36 for the
other three. Deleting any one of those retained inequalities makes that
canonical zero-neighbor formula satisfiable. A separate exact model with
only two bottom-order agents blocks all six local conversions:
[efx49_two_agent_bottom_zero_neighbor_conversion_boundary_z3.json](efx49_two_agent_bottom_zero_neighbor_conversion_boundary_z3.json).
Thus the three-agent hypothesis is sharp for this six-conversion lemma,
although the two-agent boundary may have EFX elsewhere.

The reconstructing generator is
[decide_common_bottom_pairing_conversion.py](../tracks/parkability/decide_common_bottom_pairing_conversion.py).
The hash-pinned aggregate audit is
[efx49_three_agent_bottom_pairing_conversion_audit.json](efx49_three_agent_bottom_pairing_conversion_audit.json).

## Remaining branch

It now suffices to handle profiles in which no residual pair is bottom-two
for three agents. After selecting one bottom pair per agent, the multiplicity
pattern is one of

1. $2+2$;
2. $2+1+1$; or
3. $1+1+1+1$.

The next analytic target is a role-aware Hall-witness lemma for pairs shared
by two agents. A proof need only force a favorite-pair repair or one full
favorite-triple Hall cell. This is the smallest surviving gate exposed by
the conversion analysis.
