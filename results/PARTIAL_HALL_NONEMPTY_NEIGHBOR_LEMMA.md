# Maximum-bundle neighbor lemma

## Statement

Let an agent have a nonnegative additive valuation over a partition
$B_1,\ldots,B_n$ of goods. Form the EFX acceptability graph in which the
agent is adjacent to bundle $B_j$ when

\[
v(B_j)\ge v(B_k\setminus\{g\})
\quad\text{for every }k\ne j\text{ and }g\in B_k.
\]

Then the agent has at least one neighbor. Consequently, a Hall-deficient set
in an EFX bundle graph has at least two agents.

This holds for every number of agents and goods. It does not require that a
starting allocation be EFX, that valuations be strictly positive, or that
there be only one unallocated good.

## Proof

Choose a bundle $B_j$ maximizing the agent's value. For every other bundle
$B_k$ and every $g\in B_k$, nonnegativity and maximality give

\[
v(B_k\setminus\{g\})\le v(B_k)\le v(B_j).
\]

Thus $B_j$ is adjacent to the agent.

## Role in the completion program

The exact four-agent Hall obstruction therefore needs only deficient-set
sizes two, three, and four. The original 56 minimal Boolean Hall witnesses
split as $4+24+24+4$ by deficient-set size; the first four are impossible
for additive EFX acceptability graphs, leaving 52.

[`partial_hall_nonempty_neighbor_audit.json`](partial_hall_nonempty_neighbor_audit.json)
independently checks the generic four-bundle contradiction: if no bundle were
safe, every bundle would be strictly below another bundle. The mathematical
proof above is the cap-free result.
