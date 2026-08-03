# Three-of-Four Edge Full Favorite-Triple Cell Lemma

**Status:** cap-free analytic lemma; conditional selection route refuted  
**Scope:** four additive agents, nine goods, strict common favorite  
**Role:** edge-local sufficient form of the exact favorite-triple Hall gate

## Statement

Let \(f\) be a strict favorite of every agent and put
\(F_i=v_i(f)\). Choose residual goods \(a,b\), set

\[
T=\{f,a,b\},
\qquad
\theta_i=F_i+\max\{v_i(a),v_i(b)\},
\]

and let \(R\) be the other six goods. Suppose every pair
\(S\subseteq R\) is accepted by at least three of the four agents, where
agent \(i\) accepts \(S\) when

\[
v_i(S)\ge\theta_i. \tag{1}
\]

Then every one of the 15 perfect matchings of \(R\) into three pairs,
together with \(T\), supports a complete EFX allocation.

## Proof

Fix any three-pair perfect matching of \(R\). In its pair--agent graph,
each pair vertex has at least three neighbors. Every one-pair vertex set
therefore has at least one neighbor; every two-pair set has at least three
neighbors and hence at least two; and the three-pair set also has at least
three neighbors. Hall's conditions hold, so the three pairs can be matched
to three distinct agents. The
[favorite-triple Hall characterization](FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md)
then gives a complete EFX allocation. The argument applies to every perfect
matching of \(R\). \(\square\)

## Sharp relation to the failed fixed-agent lemma

It is sufficient that the same three agents accept every residual pair,
but it is not necessary. An exact integer boundary has no such fixed triple
of agents: its best third universal-acceptor slack is \(-1\). Nevertheless
every residual pair is accepted by at least three agents, with the identity
of the rejecter allowed to vary. Consequently all 15 pairings work.

## Refuted conditional selection target

The next stronger-than-necessary target is:

> In the universal-threshold distinct-representative branch, if all 840
> favorite-pair balanced states are Hall-obstructed, then some two residual
> goods leave six goods whose every pair is accepted by at least three
> agents at threshold (1).

This would close the branch through one full 15-pairing cell, but it is
false. The strict profile in
[efx49_distinct_half_two_core_boundary_audit.json](efx49_distinct_half_two_core_boundary_audit.json)
has no favorite-pair EFX partition and has all 15 favorite-triple pairings
in one cell, yet one residual edge has only two accepting agents. Thus no
parked pair satisfies the three-of-four hypothesis.

The surviving sufficient statement is the
[two-core/Tutte corollary](FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md): two
agents accept every residual edge, and the graph of edges rejected by both
outsiders has no perfect matching.
