# Radius-five three-rival certificate-cover target

## Candidate theorem

Fix the canonical positive-additive $4\times9$ cell

\[
X=(\{6,7\},\{1,2,3\},\{0,4\},\{5\});f=8.
\]

The live bounded theorem says: if $X$ is eligible partial EFX and every
radius-one completion is Hall-blocked, then there is an eligible one-floater
state at owner distance at most five with strictly larger normalized-
utilitarian potential.

An equivalent certificate-cover program selects a normalized-utilitarian
maximum and proves that every Hall-obstruction comparison cell admits one of:

1. an explicit complete radius-one allocation;
2. one eligible Pareto-dominating rival; or
3. a weighted cycle of at most three eligible rivals whose maximality
   inequalities contradict the cell walls.

This statement remains open. A proof is only for the fixed canonical cell;
lifting across bundle shapes and numbers of goods would still remain.

## Exact motif census

Six independently reached Hall-obstruction cells are now exact UNSAT under
normalized-potential maximality. Their deletion-irreducible cores have sizes
5, 8, 12, 13, 16, and 25. The exact census is
[`partial_hall_frozen_core_census.json`](partial_hall_frozen_core_census.json).

- Five cores contain one explicit rival. Exact agentwise queries prove that
  every one of those cells forces its rival to Pareto-dominate the base; see
  [`partial_hall_core_rival_dominance_audit.json`](partial_hall_core_rival_dominance_audit.json).
- The remaining Pareto-maximal cell needs three rivals and has the exact
  weighted-cycle certificate in
  [`PARTIAL_HALL_THREE_RIVAL_WEIGHTED_CYCLE.md`](PARTIAL_HALL_THREE_RIVAL_WEIGHTED_CYCLE.md).
- At radius five, no sampled core needs more than one rival; the radius-four
  terminal obstruction has a 16-constraint, one-rival distance-five core.

This is evidence for the cover target, not a finite cover.

## Solver strengthening

The six core clauses have been closed under the
$S_2\times S_3\times S_2$ stabilizer of the base bundles. Exact replay proves
every image infeasible under row normalization and strict positivity. After
deduplication, 126 sound theory clauses are injected into the 3,187-rival
double-factored master:

- source SHA-256:
  `e80bfbfe1bd31c98c503d91d075cdab0fd1d652569ade66481ba4de5557f2ebe`;
- strengthened SHA-256:
  `a6425621e7d80a57539bafa9c689bf811d0f56267fa94e473c9be4406e28341a`;
- manifest:
  [`partial_hall_utilitarian_local_r5_core_orbit_strengthened_manifest.json`](partial_hall_utilitarian_local_r5_core_orbit_strengthened_manifest.json).

`UNSAT` for this strengthened master would prove the fixed radius-five
theorem because the strengthening is satisfiability-preserving and the
master contains only a subset of all radius-five improvement blockers.
`SAT` would require exact enumeration of every omitted radius-five rival;
`UNKNOWN` would remain inconclusive.

## Hall reduction obtained after the frozen-core census

The obstruction side is now substantially narrower. The cap-free
[maximum-bundle neighbor lemma](PARTIAL_HALL_NONEMPTY_NEIGHBOR_LEMMA.md)
removes singleton deficient sets. The dual-verified
[pair-deficiency theorem](PARTIAL_HALL_PAIR_DEFICIENCY_THEOREM.md) forces a
two-agent, one-neighbor defect, and the stronger
[designated pair-trap theorem](PARTIAL_HALL_DESIGNATED_PAIR_TRAP_THEOREM.md)
locates it among 17 star moves and 102 labeled agent-pair cells. In each cell,
the designated bundle is the unique strict favorite of both trapped agents.

The cap-free
[star localization lemma](PARTIAL_HALL_STAR_LOCALIZATION_LEMMA.md) then splits
the cover target into 85 regular cells, where a trapped agent outside the
owner--source pair exposes a preferred residual of the enlarged bundle, and
17 owner--source exceptions. These two classes form an exact disjoint cover
of the designated traps. Their conditioned radius-five masters remain
solver-unknown, so this is a proof reduction rather than the desired
three-rival cover.

The exact nearest-improver ladder supports an augmenting-exchange
interpretation; see
[`partial_hall_improver_transfer_ladder.json`](partial_hall_improver_transfer_ladder.json).
The certified radius-two through radius-five boundary profiles require
respectively 2, 3, 4, and 5 ownership changes. Their transfers progress from
a two-bundle swap to a three-edge path, a four-good exchange, and a
floater-changing five-edge exchange. This is evidence that the preferred
residual must seed a bounded augmenting chain, not a one-good release.

## Next proof move

If the strengthened master remains unknown, prioritize the regular
preferred-residual conversion and the 17 owner--source exceptions. Use any
conditioned models to extract new deletion cores, close each under the
stabilizer, and iterate.
The stopping certificate is a finite UNSAT cover. The falsification
certificate is a SAT profile that survives exhaustive radius-five rival
enumeration and independent Hall replay.
