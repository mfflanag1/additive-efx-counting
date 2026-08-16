# Connected augmenting-exchange target

## Candidate fixed-cell theorem

Fix the canonical positive-additive partial allocation

\[
X=(\{6,7\},\{1,2,3\},\{0,4\},\{5\}),\qquad f=8.
\]

Assume that $X$ is EFX, every owner weakly prefers its bundle to $f$, and
all 91 partitions obtained by assigning $f$ and moving at most one old good
are Hall-blocked. Then there is another eligible one-floater EFX allocation
$Y$ with strictly larger normalized-utilitarian potential such that:

1. at most five goods change owner, counting a change to or from the floater
   position; and
2. the transfer multigraph of those changed goods is weakly connected on the
   four owners and the floater vertex.

This candidate is stronger than the unresolved radius-five improvement
lemma. Proving it would close the canonical cell only. It would not by itself
lift to other bundle shapes or prove complete EFX existence.

## Why connectedness is the current analytic target

A connected transfer graph is the smallest formulation that contains every
known exact boundary witness. Requiring a simple path or cycle is already too
narrow: the distance-four and distance-five witnesses have branching degree
two. Connectedness still permits the multi-bundle interaction demanded by
the failed one-good-release audit, while excluding unrelated simultaneous
exchanges that provide no natural Hall-augmentation narrative.

## Exact finite-profile evidence

[`partial_hall_augmenting_exchange_topology_audit.json`](partial_hall_augmenting_exchange_topology_audit.json)
enumerates every eligible one-floater EFX state for seven independently found
Hall-obstruction profiles and compares normalized-utilitarian potential
exactly.

- All seven profiles have a connected improving exchange.
- The nearest connected distances are $2,3,2,2,3,4,5$.
- There are 3,638 improving states in total; 3,535 have a connected transfer
  graph.
- In every profile, a nearest unrestricted improver is already connected.

Potential gain is additive across weak transfer components, but eligibility
does not decompose with it. Among the 103 disconnected improving states, only
69 contain a component that is itself an eligible positive-gain state. The
remaining 34 exactly refute the naive component-isolation lemma. In the first
recorded refutation, both components have positive potential gain when
applied separately, but neither component state is EFX; their union is EFX.
Thus the proof must construct a connected rival directly or use a weighted
combination that accounts for cross-component eligibility walls.
The cap-free
[dependency-cycle lemma](PARTIAL_EFX_TRANSFER_COMPONENT_DEPENDENCY_LEMMA.md)
now shows that universal component failure forces those walls into a directed
cycle; the unresolved step is to combine the cycle inequalities with the
component potential gains.

These counts are exhaustive for the six displayed integer profiles, but they
are not a symbolic cover of the valuation cell.

## Decision status

The connected radius-five template set contains 34,370 allocations, versus
37,501 unrestricted radius-five templates. A first factored master timed out
before producing a model. An unfactored CEGAR run produced one Hall-obstructed
valuation with 158 connected improvers, then timed out after adding the first
128 improver types and their symmetry images. This is `UNKNOWN`, not a
counterexample or proof.

A projected-seed master then retained 605 connected rivals from the existing
radius-five trace and expanded them to 3,485 symmetry-closed blockers. Z3
again returned `UNKNOWN (TIMEOUT)` after 300 seconds without producing a
valuation. Additional monolithic runtime is therefore not the current proof
strategy.

The next proof move is therefore analytic: use the designated pair trap and
star localization to seed a connected exchange, and show that either it
terminates in an eligible improving state within five transfers or yields a
weighted cycle of eligible rivals contradicting potential maximality. The 17
owner--source exceptions remain a separate finite case family.

## Claim boundary

No connected-exchange theorem is claimed. The verified content is the exact
seven-profile census and the already proved designated pair-trap and
star-localization and
[transfer-component decomposition](PARTIAL_EFX_TRANSFER_COMPONENT_DECOMPOSITION_LEMMA.md)
lemmas. A `SAT` result is a refutation only after its
valuation is independently audited against all 34,370 connected templates;
an `UNSAT` result requires independent replay of the final master.
