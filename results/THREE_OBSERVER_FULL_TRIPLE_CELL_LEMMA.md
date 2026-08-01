# Three-Observer Full Favorite-Triple Cell Lemma

**Status:** cap-free analytic lemma; conditional selection route refuted  
**Scope:** four additive agents, nine goods, strict common favorite  
**Role:** scalar sufficient form of the exact favorite-triple Hall gate

## Statement

Let \(f\) be a strict favorite of every agent and put
\(F_i=v_i(f)\). Choose residual goods \(a,b\), set

\[
T=\{f,a,b\},
\qquad
\theta_i=F_i+\max\{v_i(a),v_i(b)\},
\]

and let \(R\) be the other six goods. Suppose three distinct agents
\(C\) satisfy

\[
v_i(\{g,h\})\ge\theta_i
\tag{1}
\]

for every \(i\in C\) and every pair \(\{g,h\}\subseteq R\).
Then every one of the 15 perfect matchings of \(R\) into three pairs,
together with \(T\), supports a complete EFX allocation. Assign the three
pairs bijectively to the agents in \(C\) and assign \(T\) to the fourth
agent.

## Proof

For any perfect matching of \(R\), (1) makes each of its three pair
vertices adjacent to all three agents in \(C\) at the exact threshold
\(\theta_i\). Hence the pair--agent graph has a matching saturating the
three pairs. The
[favorite-triple Hall characterization](FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md)
then gives a complete EFX allocation. The argument is independent of the
chosen perfect matching, so all 15 work. \(\square\)

## Scalar common-bottom form

For one of the three agents, sort the eight residual values as

\[
x_1\ge\cdots\ge x_8.
\]

If \(a,b\) are that agent's bottom two goods, then (1) for every pair of
the remaining six goods is equivalent to

\[
x_5+x_6\ge F+x_7. \tag{2}
\]

Indeed, \(x_5+x_6\) is the least pair value among the top six goods and
\(F+x_7\) is the favorite-triple threshold. Thus a common bottom pair and
three rows satisfying (2) produce a full 15-pairing EFX cell.

## Boundary evidence and refuted conditional route

The first two branch-valid profiles with zero favorite-pair EFX states have
the same stronger structure: goods \(1,2\) are a common bottom pair, agents
\(0,2,3\) accept every pair of the other six goods, and therefore all 15
pairings of the favorite triple \(\{0,1,2\}\) are EFX-supporting. The
independent census is
[efx49_three_observer_full_triple_cell_audit.json](efx49_three_observer_full_triple_cell_audit.json).

This motivates—but does not prove—the following conditional selection
conjecture:

> In the universal-threshold distinct-representative branch, if all 840
> favorite-pair balanced states are Hall-obstructed, then some two residual
> goods satisfy the three-observer hypothesis above.

This is stronger than necessary. The exact gate only asks for one
favorite-triple pairing whose three edge labels satisfy Hall. A refutation
of the conditional selection conjecture would therefore retire this scalar
shortcut without refuting the exact balanced conversion gate.

That refutation has now been found in strict generic position. The exact
branch-valid profile audited in
[efx49_distinct_half_two_core_boundary_audit.json](efx49_distinct_half_two_core_boundary_audit.json)
has zero favorite-pair EFX partitions and 15 favorite-triple EFX
partitions, but its best possible third universal-acceptor slack is
\(-7\). Thus no fixed three agents satisfy (1). Literal enumeration still
finds 270 complete EFX allocations, all using \(\{0,1,2\}\) as the favorite
triple.

The replacement motif is edge-local: every pair of the other six goods is
accepted by at least three agents, though the rejecting agent can depend on
the pair. That weaker sufficient statement is proved in
[THREE_OF_FOUR_EDGE_FULL_TRIPLE_CELL_LEMMA.md](THREE_OF_FOUR_EDGE_FULL_TRIPLE_CELL_LEMMA.md).
Its conditional selection claim is also refuted by a later strict boundary.
The sharpest surviving sufficient target is now the two-core/Tutte
corollary in
[FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md](FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md).
