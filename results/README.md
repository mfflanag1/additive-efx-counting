# Results directory

This directory contains both current evidence and historical campaign output.
Do not infer claim status from a filename alone.

Current paper evidence is exactly the subset referenced by:

- `repro/counting_witnesses/instances.json`
- `repro/countcegar_k4/MANIFEST.json`
- `artifacts/generalized_parking/certificates.json`
- `supplement/build_release.py`

The exact-real checkpoint inventory is separately pinned by
`repro/countcegar_real/MANIFEST.json`. It is reproducible research state, not a
paper theorem.

All other files should be treated as exploratory or historical unless a
current package README explicitly promotes them. In particular,
`CAMPAIGN_LOG.md`, `REPORT.md`, and `REVIEW.html` preserve superseded states and
corrections.

See `../ACCOMPLISHMENTS.md` for current claims and
`../docs/CAMPAIGN_ARCHIVE.md` for the archive map.

## Positive additive EFX at \(4\times8\)

The current internal proof and certification program for the new
four-agent/eight-good existence theorem is promoted through these entry
points:

- [`EFX48_PROOF_GUIDE.md`](EFX48_PROOF_GUIDE.md) — mathematical deduction
  chain and hybrid trust boundary;
- [`SESSION_REVIEW_CURRENT_20260729.md`](SESSION_REVIEW_CURRENT_20260729.md)
  — live status and research-level assessment;
- [`EFX_4X8_LRA_CERTIFICATE.md`](EFX_4X8_LRA_CERTIFICATE.md) — exact terminal
  systems and computational result;
- [`PUBLISHED_INPUT_AUDIT.md`](PUBLISHED_INPUT_AUDIT.md) — exact external
  theorem variants; and
- [`EXPERT_REVIEW_CHECKLIST.md`](EXPERT_REVIEW_CHECKLIST.md) — outstanding
  adversarial review gates;
- [`EFX48_REVIEWER_HANDOFF.md`](EFX48_REVIEWER_HANDOFF.md) — commands,
  responsibilities, and response template for independent reviewers; and
- [`../output/pdf/efx48-review-draft.pdf`](../output/pdf/efx48-review-draft.pdf)
  — the current eight-page technical manuscript.

The Lean entry point is [`../formal/efx48/EFX48.lean`](../formal/efx48/EFX48.lean).
The large frozen certificate bundle is outside this source directory at
`../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729`.
The final end-to-end manifest passes locally, and its frozen source archive
has been extracted, built, and audited in a new temporary project directory
on the original host. A genuinely independent second-machine or cross-platform
replay and external review still remain. Until they pass, describe the result
as an internally verified hybrid theorem rather than a peer-reviewed theorem.

## General additive-EFX research program

The general problem remains open. Current exact status and proof gates are
in [`GENERAL_EFX_GOAL_20260730.md`](GENERAL_EFX_GOAL_20260730.md).

The newest Hall-completion gate is
[`PARTIAL_HALL_UTILITARIAN_FROZEN_CELL_GATE.md`](PARTIAL_HALL_UTILITARIAN_FROZEN_CELL_GATE.md).
Two near-maximal obstruction cells are now exact UNSAT; the cleaner one has a
five-inequality human proof showing that a retained eligible rival strictly
Pareto-improves the changing agents. This is a local exclusion result. The
normalized-utilitarian selector, its lift beyond the fixed canonical cell,
and general additive EFX remain unresolved.
Its main analytic extraction is the cap-free
[`PARTIAL_HALL_TWO_WALL_CONVERSION_LEMMA.md`](PARTIAL_HALL_TWO_WALL_CONVERSION_LEMMA.md).
The second cell yields the complementary
[`PARTIAL_HALL_SIX_WALL_REPLACEMENT_LEMMA.md`](PARTIAL_HALL_SIX_WALL_REPLACEMENT_LEMMA.md).
The Pareto-maximal obstruction cell instead yields a fixed-cell
[`PARTIAL_HALL_THREE_RIVAL_WEIGHTED_CYCLE.md`](PARTIAL_HALL_THREE_RIVAL_WEIGHTED_CYCLE.md).
The newest exchange extraction is the cap-free algebraic
[`PARTIAL_HALL_COMPLEMENTARY_SWAP_IDENTITY.md`](PARTIAL_HALL_COMPLEMENTARY_SWAP_IDENTITY.md),
with its still-open finite repair test in
[`PARTIAL_HALL_COMPLEMENTARY_SWAP_GATE.md`](PARTIAL_HALL_COMPLEMENTARY_SWAP_GATE.md).
The identity is exact; the seven- and eight-rival conversions are refuted and
the nine-rival Hall conversion timed out, so none supplies the missing theorem.
One exact escape cell is now converted by the cap-free
[`PARTIAL_HALL_OPPOSITE_THIRD_PAIRING_LEMMA.md`](PARTIAL_HALL_OPPOSITE_THIRD_PAIRING_LEMMA.md),
whose nine-inequality algebra is independently UNSAT in Z3 and cvc5.

Both multiplicity-`2+2` bottom-pair branches are now proof-checked. Whether
the two repeated pairs are disjoint or share one good, they force either a
full selected Hall cell or one of their conversion allocations. cvc5
produced CPC proofs and Ethos returned `correct`:

- [`DISJOINT_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md`](DISJOINT_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md);
- [`efx49_disjoint_double_bottom_pair_conversion_audit.json`](efx49_disjoint_double_bottom_pair_conversion_audit.json);
- [`OVERLAP_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md`](OVERLAP_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md);
- [`efx49_overlap_double_bottom_pair_conversion_audit.json`](efx49_overlap_double_bottom_pair_conversion_audit.json); and
- the disjoint and overlapping orbit audits
  [`efx49_bottom_pattern6_conversion_orbit_audit.json`](efx49_bottom_pattern6_conversion_orbit_audit.json)
  and [`efx49_bottom_pattern0_conversion_orbit_audit.json`](efx49_bottom_pattern0_conversion_orbit_audit.json).

The fixed-order lexicographic completion strategy is refuted by a positive,
bundle-nondegenerate \(4\times9\) instance. Its adaptive-priority weakening
remains open. Five jointly feasible fixed candidate cells have been closed
by exact all-order CEGAR, and one minimal handoff has been converted into an
analytic lemma valid for arbitrary goods. A separate determinant argument
now supplies an explicit sufficient integer cap for any fixed cell:

- [`ADAPTIVE_PRIORITY_COMPLETION_TARGET.md`](ADAPTIVE_PRIORITY_COMPLETION_TARGET.md);
- [`FORCED_SINGLETON_SWAP_LEMMA.md`](FORCED_SINGLETON_SWAP_LEMMA.md);
- [`forced_singleton_swap_lemma.json`](forced_singleton_swap_lemma.json); and
- [`adaptive_priority_trace92_i5_dependency_core.json`](adaptive_priority_trace92_i5_dependency_core.json);
- [`adaptive_priority_exchange_motif_audit.json`](adaptive_priority_exchange_motif_audit.json); and
- [`adaptive_priority_first_agent_pair_gate.json`](adaptive_priority_first_agent_pair_gate.json)
  — the first two exact two-group probes, with one dual-solver 18-rival
  fixed-cell exclusion and one explicitly inconclusive endpoint; and
- [`SMALL_INTEGER_COUNTEREXAMPLE_BOUND.md`](SMALL_INTEGER_COUNTEREXAMPLE_BOUND.md).

The singleton-swap lemma is a genuine local exchange theorem, but no
covering argument currently shows that every hypothetical all-orders-blocked
family contains its pattern. It therefore does not resolve complete EFX.

The newest two-first-agent fixed-cell certificate, including its
distinctness-free 53-assumption inequality core, is rebuilt and checked with:

```bash
make verify-adaptive-first-agent-core
```

This command verifies only the frozen seed-derived cell. It is not a test of
the adaptive-priority conjecture over all candidate identities.

The attempted Hall conversion is summarized in
[`adaptive_priority_first01_hall_gate.json`](adaptive_priority_first01_hall_gate.json).
It closes the fixed witness-choice system exactly, but its 955-conflict
deletion-minimal cover is a diagnostic rather than a publishable lemma.

### New Borda-additive \(4\times9\) theorem candidate

The bounded-integer workbench now proves, in ten dual-encoded CP-SAT cells,
that every four-agent/nine-good instance whose item values in each row are a
permutation of \(1,\ldots,9\) has a complete EFX allocation of shape
\(3+2+2+2\). The five cells are exactly the five favorite-good multiplicity
orbits. They use no residual cuts or lexicographic stabilizers and share the
same 417-partition pool.

- [`BORDA_EFX_4X9_THEOREM.md`](BORDA_EFX_4X9_THEOREM.md) — theorem,
  reduction, basic explanation, and trust boundary;
- [`efx49_borda_shape3222_dual_encoding_audit.json`](efx49_borda_shape3222_dual_encoding_audit.json)
  — hash-pinned ten-cell manifest; and
- [`efx49_borda_shape3222_favorites211_core17_cpc_ethos.json`](efx49_borda_shape3222_favorites211_core17_cpc_ethos.json)
  — the 17-partition \(2+1+1\) core independently proved by cvc5 and
  proof-checked by Ethos.

This is a rigid valuation subclass, not the general additive theorem. The
other four favorite-orbit cells still lack external proof logs, so the
combined result is conservatively labeled a computer-assisted theorem
candidate.

### Rank-gap boundary beyond Borda

The fixed \(3+2+2+2\) conclusion survives when every agent chooses any nine
distinct integer scores from \(1,\ldots,10\) or \(1,\ldots,11\), according
to exact CP-SAT orbit closures. It is sharp at cap 12: a frozen
common-favorite profile has 838 complete EFX allocations but none of that
shape. Every one instead isolates the common favorite as a singleton.

- [`RANK_GAP_EFX_4X9.md`](RANK_GAP_EFX_4X9.md) — ladder, sharpness matrix,
  census, and resulting singleton-completion target; and
- [`COMMON_FAVORITE_SINGLETON_REDUCTION.md`](COMMON_FAVORITE_SINGLETON_REDUCTION.md)
  — exact analytic reduction of a singleton completion to one threshold;
  and
- [`efx49_rankgap12_shape_boundary_audit.json`](efx49_rankgap12_shape_boundary_audit.json)
  — independently regenerated literal and partition census.
- [`efx49_rankgap12_sparse_common_audit.json`](efx49_rankgap12_sparse_common_audit.json)
  — dual-encoding audit of the 424 balanced partitions plus only two
  canonical singleton repairs.

The complete-EFX closure now reaches cap 12: the common-favorite cell closes
after adding the 48 singleton repairs to the 424 balanced partitions. These
rank-gap cells now close under both matching-clause and Hall-selector
encodings:

- [`efx49_rankgap12_dual_encoding_audit.json`](efx49_rankgap12_dual_encoding_audit.json)
  — hash-pinned ten-cell theorem audit.

Both encodings still use CP-SAT and lack external proof logs, so the result
remains a computer-assisted theorem candidate.

The strongest dual-encoded result now reaches cap 13. All five
matching-clause cells and all five Hall-selector cells close with the
broader structural conclusion “balanced or isolate a designated favorite.”
The hard common-favorite orbit uses the same sparse 446-partition pool in
both encodings.

- [`efx49_rankgap13_theorem_audit.json`](efx49_rankgap13_theorem_audit.json)
  — hash-pinned five-orbit, ten-cell dual-encoding audit; and
- [`efx49_rankgap13_shape_boundaries_audit.json`](efx49_rankgap13_shape_boundaries_audit.json)
  — literal \(3+1\) and \(2+2\) shape-failure/repair censuses.
- [`efx49_common_favorite_real_frontier_audit.json`](efx49_common_favorite_real_frontier_audit.json)
  — exhaustive audit of the first unrestricted-real profile outside the
  sparse cap-13 pool: it still has 104 EFX allocations, all supported by
  common-favorite-singleton partitions.
- [`efx49_common_favorite_real_balanced_boundary_audit.json`](efx49_common_favorite_real_balanced_boundary_audit.json)
  — the converse boundary: 2,231 EFX allocations, all balanced and none
  with a singleton. The two structural branches are independently
  necessary.
- [`efx49_common_favorite_second_orbits_audit.json`](efx49_common_favorite_second_orbits_audit.json)
  — exact reduction of all 4,096 strict second-favorite vectors in the
  common-favorite cell to five multiplicity orbits.
- [`OWNER_THRESHOLD_SHAPE_ENVELOPE.md`](OWNER_THRESHOLD_SHAPE_ENVELOPE.md)
  — exact \(3+3+2\) and \(4+2+2\) owner-threshold optima, yielding a
  complete two-inequality characterization of universal threshold failure.
- [`DISTINCT_HALF_FAVORITE_GATE.md`](DISTINCT_HALF_FAVORITE_GATE.md)
  — strict generic boundaries for two false completion shortcuts, the
  analytic owner-floor closure, and the remaining
  triple-host exchange step.
- [`DISTINCT_HALF_DENSITY_FLOOR_LEMMA.md`](DISTINCT_HALF_DENSITY_FLOOR_LEMMA.md)
  — cap-free three-set proof of the favorite-pair owner-floor allocation;
  the dual 840-partition formulas are now independent corroboration.
- [`COMMON_LOW_FAVORITE_TRIPLE_LEMMA.md`](COMMON_LOW_FAVORITE_TRIPLE_LEMMA.md)
  — cap-free EFX repair when two common low goods join the favorite and the
  remaining six goods admit three observer-safe pairs; includes the
  replacement dichotomy left open by the refuted favorite-pair rank route.
- [`FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md`](FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md)
  — exact cap-free equivalence: a favorite-triple balanced partition is
  EFX-supporting precisely when its three pair bundles have a Hall matching
  to three agents at the favorite-triple deletion threshold; includes the
  surviving two-core/Tutte sufficient lemma and its exact three-case
  specialization on six vertices.
- [`efx49_six_vertex_tutte_classification_audit.json`](efx49_six_vertex_tutte_classification_audit.json)
  — exhaustive check of that specialization over all \(2^{15}\) labeled
  outsider-rejection graphs.
- [`THREE_OBSERVER_FULL_TRIPLE_CELL_LEMMA.md`](THREE_OBSERVER_FULL_TRIPLE_CELL_LEMMA.md)
  and
  [`THREE_OF_FOUR_EDGE_FULL_TRIPLE_CELL_LEMMA.md`](THREE_OF_FOUR_EDGE_FULL_TRIPLE_CELL_LEMMA.md)
  — valid sufficient full-cell lemmas whose proposed conditional selection
  routes are now exactly refuted.
- [`efx49_distinct_half_favorite_triple_boundary_audit.json`](efx49_distinct_half_favorite_triple_boundary_audit.json)
  — strict reverse boundary with zero favorite-triple EFX partitions but
  356 favorite-pair EFX partitions, proving both sides of the surviving
  dichotomy are necessary.
- [`efx49_distinct_half_two_core_boundary_audit.json`](efx49_distinct_half_two_core_boundary_audit.json)
  — strict boundary showing that three universal pair acceptors are not
  forced; the surviving two-agent core and one-edge outsider-rejection graph
  make all 15 favorite-triple pairings pass Hall.
- [`efx49_distinct_half_canonical_two_core_boundary_audit.json`](efx49_distinct_half_canonical_two_core_boundary_audit.json)
  — strict zero-favorite-pair boundary refuting the six-cell shortcut that
  lows are representatives and core agents are their complement; its unique
  unrestricted witness uses nonrepresentative lows 5 and 6.
- [`efx49_distinct_half_two_core_decision_boundary_audit.json`](efx49_distinct_half_two_core_decision_boundary_audit.json)
  — deterministic replay of the 40-cut matching CEGAR, 24-cut Hall CEGAR,
  55-cut direct complement CEGAR, 183-cut reified complement CEGAR, and
  cap-20 CP-SAT boundaries for the surviving two-core target; the last
  bounded model has only 20 favorite-pair repairs, no two-core witness, and
  one full 15-pairing favorite-triple Hall cell, while the final 331-cut
  continuation remained `UNKNOWN` after 900 seconds.
- [`efx49_distinct_half_full_cell_encoding_audit.json`](efx49_distinct_half_full_cell_encoding_audit.json)
  — both-polarity semantic audit for directly forbidding every full
  favorite-triple Hall cell.
- [`efx49_distinct_half_full_cell_decision_boundary_audit.json`](efx49_distinct_half_full_cell_decision_boundary_audit.json)
  — exact replay of the first no-full-cell real CEGAR profile and its
  183-cut `UNKNOWN` boundary, plus the cap-20 CP-SAT trace and its 412-cut,
  600-second `UNKNOWN` continuation.
- [`efx49_distinct_half_full_cell_cpsat_cegar_cap20_session3.json`](efx49_distinct_half_full_cell_cpsat_cegar_cap20_session3.json)
  — bounded no-full-cell CEGAR endpoint with 357 surviving favorite-pair
  repairs; the matching 21-megabyte model is hash-pinned by the audit.
- [`DISTINCT_HALF_FULL_CELL_CAP5_THEOREM.md`](DISTINCT_HALF_FULL_CELL_CAP5_THEOREM.md)
  — independently corroborated finite-domain theorem: in the exact
  distinct-half structural branch, strictly positive item values at most
  five force either a favorite-pair EFX state or a full favorite-triple
  Hall cell. CP-SAT closes a 416-partition pool, Z3 closes a 330-partition
  QF_LIA core and shrinks it to 193 partitions, and an independent
  threshold-CNF/CaDiCaL replay shrinks further to a deletion-minimal
  17-partition core. Its 702,820-clause formula and binary DRAT proof are
  independently checked; this is not a real-valued or general EFX theorem.
- [`efx49_distinct_half_full_cell_cap5_audit.json`](efx49_distinct_half_full_cell_cap5_audit.json)
  — deterministic hash-pinned reconstruction of the three-encoding cap-5
  evidence chain and its explicit trust boundary.
- [`efx49_distinct_half_full_cell_cap5_core17_drat_verification.json`](efx49_distinct_half_full_cell_cap5_core17_drat_verification.json)
  — proof-generator and checker hashes, certificate census, and the exact
  `drat-trim` `VERIFIED` transcript.
- [`DISTINCT_HALF_FULL_CELL_CAP6_THEOREM.md`](DISTINCT_HALF_FULL_CELL_CAP6_THEOREM.md)
  — proof-certified extension of the same structural branch to positive
  integer values at most six. CP-SAT, QF_LIA, and threshold CNF converge to
  a verified deletion-minimal 21-partition core; the final 1,145,090-clause
  CNF has an independently accepted binary DRAT proof.
- [`efx49_distinct_half_full_cell_cap6_audit.json`](efx49_distinct_half_full_cell_cap6_audit.json)
  — deterministic semantic manifest binding the cap-6 CEGAR pool, nested
  cores, threshold CNF, and checked proof object.
- [`efx49_distinct_half_full_cell_cap6_core21_drat_verification.json`](efx49_distinct_half_full_cell_cap6_core21_drat_verification.json)
  — exact cap-6 proof-generator/checker hashes and the `s VERIFIED`
  transcript.
- [`efx49_distinct_half_full_cell_cap6_hall_witness_census.json`](efx49_distinct_half_full_cell_cap6_hall_witness_census.json)
  — deterministic proof-mining census of all 588 low-pair cells in the 21
  deletion boundaries. Size-one Hall witnesses cover 572 cells, including
  all 126 representative-pair cells. In 17 of 21 profiles one fixed
  unrepresented edge witnesses all six representative-pair cells; the
  frequency is descriptive, not a cap-free theorem.
- [`DISTINCT_HALF_FULL_CELL_ORBIT_GATE.md`](DISTINCT_HALF_FULL_CELL_ORBIT_GATE.md)
  — symmetry-aware proof-mining of the 17-partition cap-5 certificate. The
  core occupies six of ten representative/unmatched-good orbits, but the
  resulting 624-partition selection candidate is refuted by an exact
  cap-20 profile whose 45 repairs all lie in two omitted orbits.
- [`efx49_distinct_half_full_cell_orbit_gate_audit.json`](efx49_distinct_half_full_cell_orbit_gate_audit.json)
  — semantic replay of the ten-orbit census, all 17 deletion boundaries,
  the cap-6 literal-core escape, the corrected annealing profile, and the
  exact-real six-orbit CEGAR trace, plus the exact 900-allocation
  refutation of the proposed selector and the 780-partition eight-orbit
  cap-20 and 173-cut exact-real `UNKNOWN` boundaries. The eight-orbit
  family is exactly the states whose triple is not all representatives.
- [`efx49_distinct_half_six_orbit_refutation_profile.json`](efx49_distinct_half_six_orbit_refutation_profile.json)
  — compact positive-EFX valuation profile refuting both the six-orbit and
  representative-partner selection candidates; it is not an EFX
  counterexample.
- [`DISTINCT_HALF_RR_HALL_SPLIT_GATE.md`](DISTINCT_HALF_RR_HALL_SPLIT_GATE.md)
  — exhaustive split of every hypothetical eight-orbit counterexample into
  an all-RR-singleton branch or a canonical RR-nonsingleton branch. Both
  exact-real formulas remain `unknown`. The RR-singleton data further split
  into a common-unrepresented-edge branch, expressible by four order-
  statistic inequalities, and its complement; the note also records exact
  counterexamples to the tempting one-swap terminal exchange lemma.
- [`DISTINCT_HALF_COMMON_UU_SPLIT_GATE.md`](DISTINCT_HALF_COMMON_UU_SPLIT_GATE.md)
  — the equivalent two-lemma formulation: a dense unmatched-edge branch and
  one canonical common-witness branch, plus the current three-repair
  boundary.
- [`efx49_distinct_half_rr_hall_split_gate_audit.json`](efx49_distinct_half_rr_hall_split_gate_audit.json)
  — deterministic replay of the 19 order-statistic orbits, the 708-pool
  exact-real common/complementary boundaries, and the cap-20 optimization
  checkpoint with 30 eight-orbit repairs and 684 complete EFX allocations.
- [`ZERO_NEIGHBOR_FAVORITE_TRIPLE_CONVERSION_LEMMA.md`](ZERO_NEIGHBOR_FAVORITE_TRIPLE_CONVERSION_LEMMA.md)
  — cap-free conversion of a shared zero-neighbor Hall edge into a
  favorite-pair EFX partition. Two independent three-repair profiles reduce
  exactly to a 12-valid-plus-3-converted Hall cell.
- [`efx49_zero_neighbor_favorite_triple_conversion_audit.json`](efx49_zero_neighbor_favorite_triple_conversion_audit.json)
  — deterministic full-partition replay of both profiles and two negative
  controls, plus a symbolic QF_LRA UNSAT check of the conversion implication.
- [`COMMON_BOTTOM_PAIRING_CONVERSION_THEOREM.md`](COMMON_BOTTOM_PAIRING_CONVERSION_THEOREM.md)
  — cap-free closure of the common-bottom-pair subbranch: each failed Hall
  pairing injects into a distinct favorite-pair EFX conversion, so
  (P_f+H_{a,b}\ge15). Its cvc5 CPC proof is accepted by Ethos.
- [`efx49_common_bottom_pairing_conversion_audit.json`](efx49_common_bottom_pairing_conversion_audit.json)
  — hash-pinned replay of both Z3 encodings, independent cvc5, the checked
  218,320-step proof, all three Hall-witness cells, and the 15-to-90
  injection census.
- [`THREE_AGENT_BOTTOM_PAIRING_CONVERSION_THEOREM.md`](THREE_AGENT_BOTTOM_PAIRING_CONVERSION_THEOREM.md)
  — strict strengthening of the common-bottom theorem: the same conversion
  and $P_f+H_{a,b}\ge15$ injection need the pair to be bottom-two for only
  three agents. The remaining bottom-pair multiplicity patterns are $2+2$,
  $2+1+1$, and $1+1+1+1$.
- [`efx49_three_agent_bottom_pairing_conversion_audit.json`](efx49_three_agent_bottom_pairing_conversion_audit.json)
  — hash-pinned cardinal/sorting Z3 records, independent cvc5 and checked
  CPC proof, five canonical Hall-role cells, the deletion-minimal 36-order
  core, the two-agent sharpness boundary, and the 15-to-90 injection census.
- [`BOTTOM_PAIR_MULTIPLICITY_GATE.md`](BOTTOM_PAIR_MULTIPLICITY_GATE.md)
  — exhaustive successor gate after the three-agent-bottom theorem. The four
  selected bottom pairs reduce to 20 unlabeled multigraph patterns; the first
  two are the overlapping and disjoint `2+2` cases, refined into 4 and 9
  relative matching orbits. The complete 165- and 180-conversion closures
  are proof-checked for those two cases; local boundaries and historical
  global zero-repair solver stalls retain their narrower status.
- [`DISJOINT_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md`](DISJOINT_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md)
  — proof-checked cap-free closure of the disjoint `2+2` pattern. Either one
  selected favorite-triple Hall cell is full or one of 180 conversions
  supports EFX. A 72-partition sufficient pool and its 19-partition core have
  independent cvc5 CPC proofs accepted by Ethos.
- [`efx49_disjoint_double_bottom_pair_conversion_audit.json`](efx49_disjoint_double_bottom_pair_conversion_audit.json)
  — hash-pinned aggregate of cardinal/sorting Z3, cvc5, CPC/Ethos, the four
  conversion orbits, and the certified 19-partition core.
- [`OVERLAP_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md`](OVERLAP_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md)
  — proof-checked cap-free closure of the overlapping `2+2` pattern using
  the full 165-conversion family and a theorem-preserving 960-element
  canonicalization. Together with the disjoint theorem this closes both
  `2+2` patterns.
- [`efx49_overlap_double_bottom_pair_conversion_audit.json`](efx49_overlap_double_bottom_pair_conversion_audit.json)
  — hash-pinned aggregate of cardinal Z3, fresh-process Z3, independent
  sorting-network Z3, cvc5, the checked 68.75 MB CPC proof, and the exact
  symmetry/orbit audits.
- [`TRIANGLE_REPEATED_BOTTOM_PAIR_CONVERSION_THEOREM.md`](TRIANGLE_REPEATED_BOTTOM_PAIR_CONVERSION_THEOREM.md)
  — proof-checked cap-free closure of the first `2+1+1` pattern, whose
  selected bottom pairs form a triangle with one doubled edge. The complete
  225-conversion family uses a theorem-preserving 480-element canonicalization.
- [`efx49_triangle_repeated_bottom_pair_conversion_audit.json`](efx49_triangle_repeated_bottom_pair_conversion_audit.json)
  — hash-pinned aggregate of cardinal Z3, fresh-process Z3, independent
  sorting-network Z3, cvc5, the checked 35.86 MB CPC proof, and exact
  symmetry/orbit audits.
- [`STAR_REPEATED_BOTTOM_PAIR_CONVERSION_THEOREM.md`](STAR_REPEATED_BOTTOM_PAIR_CONVERSION_THEOREM.md)
  — proof-checked cap-free closure of the second `2+1+1` pattern, whose
  selected bottom pairs form a three-leaf star with one doubled edge. The
  complete 228-conversion family and a theorem-preserving 96-element
  canonicalization close this cell.
- [`efx49_star_repeated_bottom_pair_conversion_audit.json`](efx49_star_repeated_bottom_pair_conversion_audit.json)
  — hash-pinned aggregate of cardinal Z3, fresh-process Z3, independent
  sorting-network Z3, cvc5, the checked 51.30 MB CPC proof, and exact
  symmetry/orbit audits.
- [`PATH_REPEATED_BOTTOM_PAIR_CONVERSION_THEOREMS.md`](PATH_REPEATED_BOTTOM_PAIR_CONVERSION_THEOREMS.md)
  — proof-checked cap-free closure of both four-vertex-path `2+1+1`
  patterns, according to whether the doubled edge is central or terminal.
  Each complete conversion family has 240 partitions.
- [`efx49_bottom_pattern3_conversion_audit.json`](efx49_bottom_pattern3_conversion_audit.json)
  and [`efx49_bottom_pattern4_conversion_audit.json`](efx49_bottom_pattern4_conversion_audit.json)
  — hash-pinned solver, CPC/Ethos, symmetry, and conversion-orbit aggregates
  for the two path theorems.
- [`REPEATED_BOTTOM_PAIR_EXCLUSION_THEOREM.md`](REPEATED_BOTTOM_PAIR_EXCLUSION_THEOREM.md)
  — class-level cap-free theorem combining the earlier three-agent-bottom
  result, both `2+2` cases, and all seven `2+1+1` cases. In the residual
  no-repair/no-full-cell branch, the four selected bottom pairs must be
  pairwise distinct.
- [`efx49_all_repeated_bottom_pair_conversions_audit.json`](efx49_all_repeated_bottom_pair_conversions_audit.json)
  — hash-pinned seven-case aggregate: 1,713 case-partitions, 217.43 MB of
  checked CPC proofs, 2,512,561 proof steps, and Ethos `correct` throughout.
- [`efx49_bottom_pair_pattern_census_audit.json`](efx49_bottom_pair_pattern_census_audit.json)
  — deterministic exhaustive reduction of 30,681 labeled edge multisets to
  20 canonical patterns: 2 of type `2+2`, 7 of type `2+1+1`, and 11 of type
  `1+1+1+1`.
- [`efx49_all_distinct_dual_z3_candidates_audit.json`](efx49_all_distinct_dual_z3_candidates_audit.json)
  — historical hash-pinned candidate aggregate for all eleven all-distinct
  patterns under both cardinal and sorting-network Z3 encodings.
- [`efx49_all_distinct_bottom_pair_conversions_audit.json`](efx49_all_distinct_bottom_pair_conversions_audit.json)
  — promoted eleven-case aggregate: 3,486 case-partitions, 383,418,002
  bytes and 4,603,008 steps of CPC proofs, with cardinal Z3, fresh Z3,
  sorting-network Z3, pinned cvc5, and Ethos `correct` throughout.
- [`COMMON_FAVORITE_UNIVERSAL_THRESHOLD_EFX_THEOREM.md`](COMMON_FAVORITE_UNIVERSAL_THRESHOLD_EFX_THEOREM.md)
  — cap-free complete-EFX theorem for four agents and nine goods throughout
  the strict-common-favorite/universal-owner-threshold-failure branch.
- [`efx49_common_favorite_universal_threshold_efx_audit.json`](efx49_common_favorite_universal_threshold_efx_audit.json)
  — top-level hash-pinned case audit covering the three-agent-bottom branch
  and all 20 multiplicity-at-most-two graph patterns; its component proofs
  total 723,786,758 bytes and 8,552,082 proof steps, all accepted by Ethos.
- [`MIXED_THRESHOLD_HALL_GATE.md`](MIXED_THRESHOLD_HALL_GATE.md)
  — exact formulation of the remaining common-favorite branch and two
  positive boundaries showing that an owner-threshold pass need not yield
  any Hall-valid favorite-singleton allocation; all complete EFX support in
  both boundaries is balanced.
- [`efx49_common_favorite_mixed_hall_boundaries_audit.json`](efx49_common_favorite_mixed_hall_boundaries_audit.json)
  and
  [`efx49_common_favorite_mixed_hall_local6_boundary_audit.json`](efx49_common_favorite_mixed_hall_local6_boundary_audit.json)
  — independently regenerated Hall, partition, allocation, and transfer
  censuses; the second refutes all six one-transfer repairs of a fixed
  threshold-passing \(3+3+2\) partition.
- [`efx49_common_favorite_mixed_hall_radius2_gate_audit.json`](efx49_common_favorite_mixed_hall_radius2_gate_audit.json)
  — open radius-two successor: 63 balanced repairs are blocked; direct caps
  6 and 20 and a cap-6 CEGAR master with 488 learned singleton obstructions
  all end `UNKNOWN`.
- [`efx49_common_favorite_mixed_selection_gate_audit.json`](efx49_common_favorite_mixed_selection_gate_audit.json)
  — historical rank-selection frontier: all three early mixed profiles have
  rank-two threshold passes with zero-neighbor witnesses, while the first
  bounded cap-20 searches decided neither selector.
- [`efx49_common_favorite_mixed_selection_gate_audit_v2.json`](efx49_common_favorite_mixed_selection_gate_audit_v2.json)
  — resumed symmetry-reduced frontier: the rank-two pool grows from 66 to
  119 motifs and the zero-neighbor pool from 49 to 69, with every trace model
  and learned-count transition independently reconstructed.
- [`efx49_common_favorite_rank2_selection_refutation_audit.json`](efx49_common_favorite_rank2_selection_refutation_audit.json)
  — exact cap-4 refutation of both selectors: a two-type profile has exactly
  three threshold passes, all with resident rank one, no favorite-singleton
  EFX partition, but 195 balanced supporting partitions and 3,690 complete
  allocations.
- [`efx49_common_favorite_fourtype_rank2_frontier_audit.json`](efx49_common_favorite_fourtype_rank2_frontier_audit.json)
  — repaired cap-4 frontier with four pairwise nonproportional rows: 12 exact
  trace profiles grow the cumulative rank-two obstruction pool from 29 to
  77 motifs; both sessions end at iteration limits.
- [`efx49_common_favorite_fourtype_rank2_refutation_audit.json`](efx49_common_favorite_fourtype_rank2_refutation_audit.json)
  — exact refutation of the repaired selector: four pairwise
  bundle-order-inequivalent rows, three rank-one threshold passes, no
  favorite-singleton EFX partition, 599 balanced supporting partitions,
  and 3,878 complete allocations.
- [`ROW_MERGE_CONTINUATION_GATE.md`](ROW_MERGE_CONTINUATION_GATE.md) and
  [`tight49_row_merge_interpolation_audit.json`](tight49_row_merge_interpolation_audit.json)
  — cap-free reduction of four-agent EFX to continuation away from a safe
  three-valuation boundary, plus the resident-extension lemma reducing a
  fixed bundle partition to at most four intervals. Its ordinal-chamber
  corollary closes every profile with at most three bundle-order types.
- [`row_merge_essential_edge_hall_audit.json`](row_merge_essential_edge_hall_audit.json)
  — exact graph census for the single-wall gate: 4,929 labeled
  essential-edge graphs, 213 symmetry orbits, and exactly four minimal Hall
  witness sizes.
- [`SINGLE_WALL_PIVOT_GATE.md`](SINGLE_WALL_PIVOT_GATE.md) and
  [`row_merge_single_wall_radius_refutation_audit.json`](row_merge_single_wall_radius_refutation_audit.json)
  — generic-wall no-go boundary: Hall sizes two and three can defeat every
  partition within two good transfers, and Hall size four can defeat every
  one-transfer partition. The post-wall profiles remain EFX-positive at
  distances three, three, and two. The seven-good size-four cell has a
  deletion-minimal seven-pivot/two-comparison core. In the balanced
  eight-good size-four cell, one of an explicit 11 pair pivots must support
  EFX for a sufficiently small step; Z3 and cvc5 independently prove the
  frozen formula UNSAT. This is sharp at the next enlargement: a nine-good
  \(2+2+2+3\) size-four wall blocks all 319 radius-two partitions but has
  206 complete EFX allocations beginning at distance three.
- [`ROW_MERGE_EXCHANGE_CHAIN_GATE.md`](ROW_MERGE_EXCHANGE_CHAIN_GATE.md) and
  [`row_merge_q4_exchange_chain_gate_audit.json`](row_merge_q4_exchange_chain_gate_audit.json)
  — exact distance-three proof-mining boundary. Simple transfer paths and
  cycles give a 515-partition menu; the terminal profile has eight such
  repairs. A 24-cut model retains 48 repairs and a fixed-graph 32-cut model
  retains nine. Later cap-20 CEGAR found exact repair models through 76 cuts,
  learned an 80-cut pool, and ended `unknown/canceled` at the 80-cut solve.
  The full candidate is open, not a pivot theorem.
- [`ROW_MERGE_TOPOLOGY_MINING_GATE.md`](ROW_MERGE_TOPOLOGY_MINING_GATE.md) and
  [`row_merge_q4_topology_mining_gate_audit.json`](row_merge_q4_topology_mining_gate_audit.json)
  — solver-free audited no-go boundary for short topology summaries in the
  fixed nine-good cell. Exact cap-20 profiles refute all 80 directed
  three-cycle partitions, all 117 paths starting at the three-good bundle,
  and two successive minimum two-topology trace covers, each combined with
  the 16 base pivots. The profiles retain 15--44 other chain repairs and
  381--686 complete EFX allocations. This refutes only the listed compressed
  menus, not the full 515-partition candidate.
- [`ROW_MERGE_RANKED_PATH_GATE.md`](ROW_MERGE_RANKED_PATH_GATE.md) and
  [`row_merge_q4_ranked_path_gate_audit.json`](row_merge_q4_ranked_path_gate_audit.json)
  — exact valuation-selector boundary in the same generic one-edge wall
  cell. Three source-wise minimum policies cover all 23 frozen trace models,
  but the natural ((0,0,0,3)) policy has a cap-20 refutation with 17 other
  chain repairs and 428 complete EFX allocations. The union of all three is
  still open after 12 SAT rounds, 100 conditional cuts, and a final
  60-second timeout. This retires only one static rank rule; broader adaptive
  selectors and the full chain candidate remain open.
- [`ROW_MERGE_ADAPTIVE_HALL_PATH_GATE.md`](ROW_MERGE_ADAPTIVE_HALL_PATH_GATE.md)
  and
  [`row_merge_q4_adaptive_hall_path_analysis.json`](row_merge_q4_adaptive_hall_path_analysis.json)
  — solver-free exact negative gate for the first adaptive Hall rule. Filling
  the current hole from the neighborhood of a recomputed minimal Hall blocker
  repairs 20 of 25 distinct generic frozen models but fails on five, after
  exhausting 19--35 permitted states per failure. This retires only that
  local Hall-neighborhood selector; sources outside the current neighborhood,
  cycles, valuation-slack lookahead, and the full chain candidate remain open.
- [\`row_merge_no_stable_partition_m7_audit.json\`](row_merge_no_stable_partition_m7_audit.json)
  — exact refutation of fixed-partition row-merge continuation: the endpoint
  partition sets are disjoint even though two overlapping allocation
  intervals cover the entire path.
- [\`row_merge_deficient_block_restart_refutation_m7_q3_audit.json\`](row_merge_deficient_block_restart_refutation_m7_q3_audit.json)
  — all 150 delete-and-repartition states confined to the minimal Hall block
  fail; the nearest partial EFX repair must touch an outside bundle.
- [\`row_merge_global_partial_restart_m7_audit.json\`](row_merge_global_partial_restart_m7_audit.json)
  — dual-solver seven-good lemma for Hall sizes two, three, and four: one of
  81 global delete-one/move-at-most-one partitions supports partial EFX.
- [\`row_merge_global_partial_radius1_m8_uplus_refutation.json\`](row_merge_global_partial_radius1_m8_uplus_refutation.json)
  — exact eight-good boundary: all 126 radius-one global partial restarts
  fail in an isolated Hall-size-three wall, while 218 complete EFX
  allocations remain elsewhere.
- [`t47_row_merge_interpolation_audit.json`](t47_row_merge_interpolation_audit.json),
  [`tb4_row_merge_interpolation_audit.json`](tb4_row_merge_interpolation_audit.json),
  and
  [`tight410_row_merge_interpolation_audit.json`](tight410_row_merge_interpolation_audit.json)
  — together with the \((4,9)\) audit, exact stable-partition checks for all
  48 ordered row paths of the count-four witnesses from \((4,7)\) through
  \((4,10)\); 17 paths have exactly one stable partition.
- [`efx49_common_favorite_threshold_pass_hall_611_row_merge_interpolation_audit.json`](efx49_common_favorite_threshold_pass_hall_611_row_merge_interpolation_audit.json)
  and
  [`efx49_common_favorite_threshold_pass_hall_332_row_merge_interpolation_audit.json`](efx49_common_favorite_threshold_pass_hall_332_row_merge_interpolation_audit.json)
  — exact continuation audits for the two hostile mixed-Hall profiles; every
  one of their 24 ordered row paths is covered by a single fixed assignment.
  Across all six row-merge audits, all 72 paths have a stable partition; 63
  use one assignment and nine use two assignments of the same bundles.
- [`RANK_ONE_COMMON_COLUMN_NORMAL_FORM.md`](RANK_ONE_COMMON_COLUMN_NORMAL_FORM.md)
  and [`efx49_common_favorite_rank1_triple_gate_audit.json`](efx49_common_favorite_rank1_triple_gate_audit.json)
  — proved analytic normal form for rank-one resident graphs, exact
  owner-switch reduction, and the superseded early triple-conversion gate.
- [`efx49_common_favorite_rank1_local6_boundary_audit.json`](efx49_common_favorite_rank1_local6_boundary_audit.json)
  — exact no-singleton rank-one profile blocking all six one-good transfers;
  all 366 supporting partitions are balanced, the nearest 15 are distance
  two, and the 63-partition radius-two successor remains open.
- [`efx49_common_favorite_rank1_radius2_orbits_audit.json`](efx49_common_favorite_rank1_radius2_orbits_audit.json)
  — exact nine-orbit decomposition of the radius-two neighborhood and the
  superseded 302-cut boundary for the former 21-state target.
- [`RANK_ONE_RADIUS_TWO_BRIDGE_GATE.md`](RANK_ONE_RADIUS_TWO_BRIDGE_GATE.md)
  and [`efx49_common_favorite_rank1_contested_refutation_audit.json`](efx49_common_favorite_rank1_contested_refutation_audit.json)
  — exact cap-6 refutation of that 21-state implication, including zero
  singleton repairs and one zero-neighbor bundle in every blocked state;
  all nine nearest repairs form one missing bridge orbit.
- [`efx49_common_favorite_rank1_bridge_checkpoint_audit.json`](efx49_common_favorite_rank1_bridge_checkpoint_audit.json)
  — superseded target-zero seed blocking all 30 contested-or-bridge states while
  retaining 30 favorite-singleton repairs; its six balanced radius-two
  repairs occupy one outside orbit.
- [`efx49_common_favorite_rank1_bridge_refutation_audit.json`](efx49_common_favorite_rank1_bridge_refutation_audit.json)
  — exact refutation of the 30-state bridge implication: zero of 966
  singleton partitions and zero target repairs work, although 264 other
  partitions yield 2,790 complete allocations. Its 15 nearest repairs add
  two origin orbits, giving the open 45-state successor; the first bounded
  campaign reaches a six-singleton Hamming-two local minimum.
- [`efx49_common_favorite_rank1_extended_bridge_identical_audit.json`](efx49_common_favorite_rank1_extended_bridge_identical_audit.json)
  — dual-encoded cap-6 theorem candidate for the subcell with three identical
  resident rows: the same 392 singleton partitions and 45 repairs close in
  matching-clause and Hall-selector CP-SAT. Unequal residents remain open.
- [`efx49_common_favorite_rank1_extended_bridge_collision_cap5_audit.json`](efx49_common_favorite_rank1_extended_bridge_collision_cap5_audit.json)
  — dual-encoded cap-5 extension to any repeated resident row. The two
  adjacent equality cases share the 392-partition pool and close under both
  a 12-matching quotient and a seven-case Hall quotient; all 4,096 compressed
  neighborhood graphs are checked against literal matching. Cap 6 is open;
  the separately retained cap-4 audit records the preceding rung.
- [`RANK_ONE_CORE_SHAPE_LADDER_GATE.md`](RANK_ONE_CORE_SHAPE_LADDER_GATE.md)
  and
  [`efx49_common_favorite_rank1_core_shape_ladder_audit.json`](efx49_common_favorite_rank1_core_shape_ladder_audit.json)
  — compression of the row-1=row-2 cap-5 theorem to one shared
  112-partition menu under both quotient encodings. Its balanced layer is
  exactly a 29-partition cap-4 Hall core; the remaining layers have residual
  shapes (4+2+2) and (4+3+1). The menu is not cap-free: four independently
  enumerated cap-6 trace models remain SAT through 196 cuts and generate an
  unsolved 211-cut pool. The audit checks all singleton-support and bridge
  censuses literally and pins every source and proto hash.
- [`FOUR_DISCONNECTED_BOTTOM_PAIRS_CONVERSION_THEOREM.md`](FOUR_DISCONNECTED_BOTTOM_PAIRS_CONVERSION_THEOREM.md)
  — first proof-checked all-distinct case: the four selected bottom pairs
  are disjoint and cover all eight residual goods. The complete
  360-conversion family closes under the branch assumptions.
- [`efx49_bottom_pattern19_conversion_audit.json`](efx49_bottom_pattern19_conversion_audit.json)
  — hash-pinned aggregate of two Z3 encodings, fresh-process replay, pinned
  cvc5, a 27.79 MB CPC proof accepted by Ethos, and the exact 384-action
  symmetry and four-orbit censuses.
- [`efx49_bottom_pattern19_conversion_selector_sorting_core2_minimized.json`](efx49_bottom_pattern19_conversion_selector_sorting_core2_minimized.json)
  — minimized six-partition canonical core for the perfect-matching case.
  The compact formula is also independently `unsat` in cvc5, with an
  8.86 MB CPC proof accepted by Ethos.
- [`efx49_bottom_pattern19_six_conversion_core_audit.json`](efx49_bottom_pattern19_six_conversion_core_audit.json)
  — single hash-pinned aggregate for the six-case core: two Z3 core checks,
  unguarded replay, independent cvc5, CPC/Ethos, exact orbit analysis,
  deletion-minimality, and the satisfiable no-symmetry boundary.
- [`FOUR_CYCLE_BOTTOM_PAIRS_CONVERSION_THEOREM.md`](FOUR_CYCLE_BOTTOM_PAIRS_CONVERSION_THEOREM.md)
  — second proof-checked all-distinct case, closing the four-cycle selected
  bottom-pair geometry with a 300-partition conversion family.
- [`efx49_bottom_pattern14_conversion_audit.json`](efx49_bottom_pattern14_conversion_audit.json)
  — hash-pinned aggregate of two Z3 encodings, fresh-process replay, pinned
  cvc5, a 58.69 MB CPC proof accepted by Ethos, and the exact 192-action
  symmetry and five-orbit censuses.
- [`efx49_overlap22_three_repair_motif_audit.json`](efx49_overlap22_three_repair_motif_audit.json)
  — four distinct overlap-`2+2` profiles (three annealed and one CP-SAT) at
  the exact three-repair boundary. Every profile has the same `12+3` Hall
  split, one common failed edge, and repairs exactly equal to the three
  failed-pairing conversions.
- [`efx49_overlap_orbit1_shared_active_audit.json`](efx49_overlap_orbit1_shared_active_audit.json)
  — proof-checked closure of relative matching orbit 1 for the 420-state
  shared-low-active family: fresh-process Z3 and independent cvc5 `unsat`, a
  52.15 MB CPC proof, and Ethos `correct`. This is one of four overlap
  matching orbits, not the whole overlap pattern.
- [`efx49_overlap22_pattern_symmetry_audit.json`](efx49_overlap22_pattern_symmetry_audit.json)
  — deterministic audit of the 960-element overlap-pattern relabeling group.
  All four exact three-repair boundaries have canonical representatives, and
  all twelve sharp repairs lie in the same size-60 conversion orbit.
- [`DISTINCT_HALF_TERMINAL_EXCHANGE_GATE.md`](DISTINCT_HALF_TERMINAL_EXCHANGE_GATE.md)
  — a sharp finite/local boundary: across all seven canonical
  terminal/matching cells, CP-SAT and Z3 QF_LIA prove that cap-5 terminal
  EFX forces an eight-orbit EFX repair within two swaps, without a
  full-Hall-cell assumption. The nonvacuous
  bounded theorem does not extend the certified existence ladder, and its
  unrestricted analogue is false by cap 20. The decisive profile has no full
  Hall cell, zero repairs in all 138 radius-two states, 336 favorite-pair EFX
  partitions elsewhere, and 1,439 complete EFX allocations. The nearest
  eight-orbit repair is at distance three; see
  [`TERMINAL_RADIUS_TWO_EXCHANGE_CANDIDATE.md`](TERMINAL_RADIUS_TWO_EXCHANGE_CANDIDATE.md).
- [`efx49_distinct_half_terminal_exchange_gate_audit.json`](efx49_distinct_half_terminal_exchange_gate_audit.json)
  — deterministic symmetry census, nonvacuity witness, target-family
  reconstruction, hash manifest for the fourteen finite-cap formulas, and
  independent semantic replay of the cap-20 radius-two refutation.
- [`ONE_DEFECT_FAVORITE_TRIPLE_CONVERSION_LEMMA.md`](ONE_DEFECT_FAVORITE_TRIPLE_CONVERSION_LEMMA.md)
  — optional cap-free conversion back to a favorite-pair allocation; the
  favorite-triple Hall theorem shows that its one-defect premise already
  suffices for EFX existence without an exchange.
- [`DISTINCT_HALF_CONVERSION_DICHOTOMY_GATE.md`](DISTINCT_HALF_CONVERSION_DICHOTOMY_GATE.md)
  — consolidated statement, strict boundary, exact solver limits, and the
  remaining conditional Hall-to-Tutte selection unit.
- [`DISTINCT_HALF_RANK_AUGMENTATION_GATE.md`](DISTINCT_HALF_RANK_AUGMENTATION_GATE.md)
  — exact strict boundaries refuting both favorite-pair plateau augmentation
  and its former radius-two strengthening.
- [`COMMON_THREE_LEXICOGRAPHIC_PARKING_LEMMA.md`](COMMON_THREE_LEXICOGRAPHIC_PARKING_LEMMA.md)
  — cap-free exchange proof closing the common-three side of the resulting
  half-favorite dichotomy, with dual exact-real UNSAT corroboration.
- [`UNIVERSAL_THRESHOLD_BALANCED_GATE.md`](UNIVERSAL_THRESHOLD_BALANCED_GATE.md)
  — exact statement and computational boundary for the remaining
  four-distinct-half-favorite-representatives branch.
- [`UNIVERSAL_PAIR_FLOOR_LEX_PARKING_LEMMA.md`](UNIVERSAL_PAIR_FLOOR_LEX_PARKING_LEMMA.md)
  — general \(n\)-agent, \(2n+1\)-good completion theorem when every
  residual pair clears the common-favorite floor.
- [`RESIDUAL_THRESHOLD_MATCHING_LEMMA.md`](RESIDUAL_THRESHOLD_MATCHING_LEMMA.md)
  — exact Hall characterization of a
  singleton--singleton--singleton--residual EFX partition.
- [`efx49_common_favorite_boundaries_audit.json`](efx49_common_favorite_boundaries_audit.json)
  — exhaustive audit of the 18-allocation common-favorite search boundary
  and the cap-13 profile refuting the narrower “balanced or
  \(6+1+1+1\)” cover.
- [`COMMON_FAVORITE_SUFFICIENT_CAP_GATE.md`](COMMON_FAVORITE_SUFFICIENT_CAP_GATE.md)
  — exact scope, safe reductions, sufficient integer cap, learned pool,
  and current trust boundary for the unrestricted common-favorite cell.
- [`efx49_common_favorite_sufficient_cap_audit.json`](efx49_common_favorite_sufficient_cap_audit.json)
  — independently reconstructed 485→811 CEGAR chain and hash-bound
  matching/Hall residual timeouts; explicitly no theorem verdict.
- [`adaptive_priority_first01_template_quotient_gate.json`](adaptive_priority_first01_template_quotient_gate.json)
  — exact negative compression gate for the fixed first-agent-0/1 cell:
  926 row-local minimal Hall conflicts occupy 397 colored-graph templates,
  with 29 additional mixed-row conflicts; explicitly no general EFX claim.
- [`PARTIAL_NASH_COMPLETION_TARGET.md`](PARTIAL_NASH_COMPLETION_TARGET.md),
  [`partial_nash_potential_gate.json`](partial_nash_potential_gate.json), and
  [`PARTIAL_NASH_COMPLETION_REFUTATION.md`](PARTIAL_NASH_COMPLETION_REFUTATION.md)
  — the maximum-Nash direct-insertion selector is exactly refuted. The fixed
  $4\times9$ profile has a unique blocked maximum among 290 eligible states;
  three independent partial-state enumerators agree. It also has 83 complete
  EFX allocations, so the general existence problem remains open.
- [`partial_nash_completion_refutation_audit.json`](partial_nash_completion_refutation_audit.json)
  — exhaustive audit over all 589,824 partial assignments and 262,144
  complete assignments, including all eligible states, insertion witnesses,
  and the exact complete-allocation hash. The profile/audit/seed-211/script
  SHA-256 values are `928029ffcd6d4171e1733999fe6f6f0abf0d0d5ab6ffe1c7c0a3702215155981`,
  `20f8804f932534242b196db6acbbca6d3c0434563ef3cdfed910e2babd412df6`,
  `c70870d3965621d5b60044ebd3adf7a2058af9a6c2446b414ef5790c6a867211`,
  and `fb666b2cd888e28f2bb104877b95f561f65d0006ea6304b4ebfd24d0c4a30e52`.
  A fresh 2026-08-02 replay passed byte-for-byte.
- [`PARTIAL_NASH_LOCAL_COMPLETION_REFUTATION.md`](PARTIAL_NASH_LOCAL_COMPLETION_REFUTATION.md)
  and
  [`partial_nash_one_transfer_refutation_audit.json`](partial_nash_one_transfer_refutation_audit.json)
  — exact refutation of the same-floater local repair. The unique blocked
  maximum-Nash state is the only eligible state among all 25 owner vectors at
  distance at most one, no insertable eligible state exists through distance
  three, and the nearest seven occur at distance four. The profile has 128
  complete EFX allocations, so this still refutes only a proof route.
- [`PARTIAL_NASH_SOURCE_COMPLETION_REFUTATION.md`](PARTIAL_NASH_SOURCE_COMPLETION_REFUTATION.md)
  and
  [`partial_nash_source_completion_refutation_audit.json`](partial_nash_source_completion_refutation_audit.json)
  — exact refutation of the strongest one-source-substitution repair. The
  unique blocked maximum-Nash state has two source bundles, but every one of
  the 120 source-good substitutions and arbitrary bundle rematchings fails
  partial EFX. The same profile has 87 complete EFX allocations. The paired
  corpus scan covers 159 distinct profiles and identifies this as the sole
  failure among three profiles with blocked maximum-Nash states.
- [`PARTIAL_NASH_SOURCE_HOST_REDUCTION.md`](PARTIAL_NASH_SOURCE_HOST_REDUCTION.md)
  and [`bundle_cycle_source_lemma_audit.json`](bundle_cycle_source_lemma_audit.json)
  — proved cap-free bundle-cycle improvement and source-host reduction. A
  blocked maximum-Nash state must expose a nonsingleton unenvied host and a
  blocker that ranks the floater above the removed host good; closing the
  resulting support chain remains open.
- [`PARTIAL_NASH_SUBSTITUTION_PATH_LEMMA.md`](PARTIAL_NASH_SUBSTITUTION_PATH_LEMMA.md)
  — proved cap-free floater-substitution improvement along a weak bundle
  preference path. The broader local cycle-or-source-substitution closure is
  exactly false; see
  [`partial_nash_local_trichotomy_gate.json`](partial_nash_local_trichotomy_gate.json).
  Its refuting state has 1,780 larger global rivals. The later exact
  maximum-Nash refutation shows why extending this local lemma cannot prove
  direct completion from global maximality.
- [`PARTIAL_PARETO_COMPLETION_GATE.md`](PARTIAL_PARETO_COMPLETION_GATE.md)
  and
  [`partial_pareto_completion_refutation_audit.json`](partial_pareto_completion_refutation_audit.json)
  — exact refutation of the simpler Pareto-maximal selector. The frozen
  blocked frontier vector is locally isolated from all higher-product states.
  This obstruction supplied the search objective that subsequently refuted
  maximum-Nash direct completion itself.
- [`MAX_NASH_RADIUS_ONE_HALL_COMPLETION_TARGET.md`](MAX_NASH_RADIUS_ONE_HALL_COMPLETION_TARGET.md),
  [`partial_hall_pareto_cegar_session1.json`](partial_hall_pareto_cegar_session1.json),
  and
  [`partial_hall_pareto_cegar_model_audit.json`](partial_hall_pareto_cegar_model_audit.json)
  — exact refutation of the stronger Pareto-maximal radius-one Hall selector.
  The canonical $2+3+2+1$ base is eligible and has no Pareto dominator among
  992 eligible states, yet all 91 one-old-good-move partitions and all 2,184
  partition--matching pairs fail. This refutes only that completion selector,
  not complete additive EFX.
- [`partial_hall_utilitarian_corpus_scan.json`](partial_hall_utilitarian_corpus_scan.json)
  — exact finite scan of the replacement normalized-utilitarian selector on
  208 distinct stored profiles through ten goods. Eight maximizing states
  fail radius-zero Hall completion; every maximizing state has a radius-one
  completion. This is falsification evidence, not a theorem.
- [`partial_hall_utilitarian_local_cegar_session1.json`](partial_hall_utilitarian_local_cegar_session1.json),
  [`partial_hall_utilitarian_local_r3_cegar_session1.json`](partial_hall_utilitarian_local_r3_cegar_session1.json),
  and
  [`partial_hall_utilitarian_local_r4_cegar_session1.json`](partial_hall_utilitarian_local_r4_cegar_session1.json)
  — exact normalized-utilitarian obstruction ladder. Radius-one Hall-blocked
  canonical states can exclude every larger-potential eligible state through
  owner distances two, three, and four; in each certified profile the nearest
  improvement occurs at the next distance. The global utilitarian selector
  remains unrefuted.
- [`partial_hall_utilitarian_local_r5_orbit_seed_build.json`](partial_hall_utilitarian_local_r5_orbit_seed_build.json)
  and
  [`partial_hall_utilitarian_local_r5_orbit_seed_cubes_d3.json`](partial_hall_utilitarian_local_r5_orbit_seed_cubes_d3.json)
  — the exact radius-five decision boundary after factored Hall encoding,
  sound 24-fold within-bundle good symmetry, and orbit closure of 416 learned
  rivals to 3,187 distinct exclusions. The eight cubes exactly cover the
  frozen master. This is a solver reduction, not a SAT/UNSAT verdict.
- [`partial_hall_utilitarian_local_r5_orbit_seed_cubes_d5.json`](partial_hall_utilitarian_local_r5_orbit_seed_cubes_d5.json)
  — hash-audited composition of the eight parent cubes with four children
  each, yielding a 32-leaf exact cover of the same frozen master.
- [`partial_hall_utilitarian_local_r5_double_factored_audit.json`](partial_hall_utilitarian_local_r5_double_factored_audit.json)
  and
  [`partial_hall_utilitarian_local_r5_double_factored_seed_cubes_d3.json`](partial_hall_utilitarian_local_r5_double_factored_seed_cubes_d3.json)
  — exact symbolic equivalence audit for sharing the 3,187 rival blockers'
  repeated eligibility comparisons, plus an eight-branch cover of the
  resulting 4,065-comparison master. This remains a decision encoding, not a
  radius-five theorem verdict.
- [`partial_hall_witness_encoding_audit.json`](partial_hall_witness_encoding_audit.json)
  and
  [`partial_hall_utilitarian_local_r5_hall_witness_core_orbit_strengthened_manifest.json`](partial_hall_utilitarian_local_r5_hall_witness_core_orbit_strengthened_manifest.json)
  — exact replacement of the 24 failed-matching clauses for each candidate
  completion by 56 minimal deficient-set Hall witnesses. An independent
  Boolean replay proves the encodings equivalent for every $4\times4$ graph;
  the new strengthened master retains the same 3,187 rival blockers and 126
  sound frozen-core clauses. This is a structural decision encoding, not yet
  a radius-five verdict.
- [`PARTIAL_HALL_NONEMPTY_NEIGHBOR_LEMMA.md`](PARTIAL_HALL_NONEMPTY_NEIGHBOR_LEMMA.md)
  and [`PARTIAL_HALL_PAIR_DEFICIENCY_THEOREM.md`](PARTIAL_HALL_PAIR_DEFICIENCY_THEOREM.md)
  — a cap-free maximum-bundle argument eliminates singleton Hall defects for
  any additive EFX acceptability graph. Exact QF_LRA then proves that every
  eligible radius-one obstruction in the fixed canonical cell exposes a
  two-agent, one-neighbor defect in at least one of its 91 candidate moves.
  This sharply narrows the exchange lemma still needed; it does not prove
  completion or EFX existence.
- [`PARTIAL_HALL_DIAGONAL_OR_HOST_LEMMA.md`](PARTIAL_HALL_DIAGONAL_OR_HOST_LEMMA.md)
  — cap-free analytic structure for direct floater insertion. Every agent
  accepts either its original bundle or the enlarged host; losing a diagonal
  edge forces the host edge. This reduces the possible four-row Hall graphs,
  but a new exact positive instance proves the condition alone still permits
  larger defects and that a one-good transfer is genuinely necessary.
- [`PARTIAL_HALL_PAIR_EXTRACTION_TARGET.md`](PARTIAL_HALL_PAIR_EXTRACTION_TARGET.md)
  and
  [`partial_hall_pair_extraction_corpus134.json`](partial_hall_pair_extraction_corpus134.json)
  — the cap-free generalization now chosen as the leading theorem target.
  Exact enumeration over 134 positive $4\times9$ profiles checks 128,131
  arbitrary-shape eligible states and 11,988,061 radius-one candidate
  partitions. All 674 states with no completion still expose a two-agent,
  one-neighbor Hall witness. Restricting transfers to owner-minimum goods still
  decides all states: 127,081 complete and 1,050 expose a pair. Direct
  insertion alone is exactly refuted by a separate positive $4\times9$
  profile, which an owner-minimum transfer completes. This is strong finite
  evidence across all five bundle-size shapes, not a proof over arbitrary
  valuations or goods.
- [`PARTIAL_HALL_OWNER_MINIMUM_EXTRACTION_THEOREM.md`](PARTIAL_HALL_OWNER_MINIMUM_EXTRACTION_THEOREM.md)
  and
  [`partial_hall_owner_minimum_extraction_theorem_audit.json`](partial_hall_owner_minimum_extraction_theorem_audit.json)
  — cap-free closure of pair-extraction gate 1. For arbitrary positive values
  and bundle sizes, direct insertion plus one of four selected owner-minimum
  goods either yields an EFX perfect matching or forces a two-agent,
  one-neighbor Hall trap. Z3 proves all 16 singleton patterns UNSAT; cvc5
  independently confirms the five symmetry representatives. Pair-trap
  conversion remains necessary before this can imply complete EFX.
- [`PARTIAL_HALL_PAIR_TRAP_CONVERSION_GATE.md`](PARTIAL_HALL_PAIR_TRAP_CONVERSION_GATE.md)
  and
  [`partial_hall_owner_minimum_substitution_counterexample_audit.json`](partial_hall_owner_minimum_substitution_counterexample_audit.json)
  — exact boundary of the next gate. One owner-minimum substitution is
  insufficient even in a positive $4\times9$ instance with a forced pair
  trap. The base is not globally selector-maximal: its nearest improvement is
  a two-good swap with exact normalized gain $11/1072$. Hence the live
  cap-free target is a trap-witness two-good exchange lemma.
- [`PARTIAL_HALL_DESIGNATED_PAIR_TRAP_THEOREM.md`](PARTIAL_HALL_DESIGNATED_PAIR_TRAP_THEOREM.md)
  — dual-verified strengthening of the pair-deficiency theorem. Among only 17
  explicit star moves, every fixed-cell obstruction creates two agents whose
  sole acceptable bundle is the enlarged host or the evacuated singleton's
  destination. Hence the obstruction contains a common strict-favorite
  collision. This is the current analytic conversion frontier.
- [`PARTIAL_HALL_STAR_LOCALIZATION_LEMMA.md`](PARTIAL_HALL_STAR_LOCALIZATION_LEMMA.md)
  — cap-free analytic localization: outside the source and host, an unchanged
  bundle can lose its EFX edge after a star move only to a residual of the
  enlarged designated bundle. The 102 designated pair traps therefore reduce
  to one regular preferred-residual motif and 17 labeled owner--source
  exceptions. The natural remove-one-good/rematch successor is sharply false:
  only 18 of 359 observed traps yield a parked higher-potential release, so a
  multi-bundle or weighted-cycle conversion is genuinely necessary.
- [`partial_hall_improver_transfer_ladder.json`](partial_hall_improver_transfer_ladder.json)
  — exact ownership-transfer graphs for the radius-two-through-five
  obstruction ladder. The nearest improving rivals use exactly 2, 3, 4, and
  5 changed goods, progressing from a swap through an augmenting path to a
  floater-changing exchange. This motivates the next bounded-chain lemma.
- [`PARTIAL_HALL_CONNECTED_EXCHANGE_TARGET.md`](PARTIAL_HALL_CONNECTED_EXCHANGE_TARGET.md)
  and
  [`partial_hall_augmenting_exchange_topology_audit.json`](partial_hall_augmenting_exchange_topology_audit.json)
  — sharpen the bounded-chain target to a weakly connected transfer
  multigraph. Exact exhaustive enumeration of seven obstruction profiles finds
  3,535 connected improvers among 3,638 improvers overall; every profile has
  a nearest connected improver at distance at most five. This is finite-corpus
  evidence, not a symbolic cover. The audit also refutes naive decomposition:
  34 of 103 disconnected improvers have no independently eligible positive
  component. Initial factored and unfactored connected-rival masters remain
  solver-unknown; a 3,485-blocker projected-seed master likewise timed out at
  300 seconds.
- [`PARTIAL_EFX_TRANSFER_COMPONENT_DECOMPOSITION_LEMMA.md`](PARTIAL_EFX_TRANSFER_COMPONENT_DECOMPOSITION_LEMMA.md)
  — cap-free decomposition theorem: every transfer component defines a valid
  one-floater allocation and normalized-utilitarian gain is the exact sum of
  its component gains. Hence some component of every improving rival has
  positive raw gain. The topology audit verifies the identity exhaustively
  and shows the sharp limitation: cross-component EFX eligibility can be
  essential.
- [`PARTIAL_EFX_TRANSFER_COMPONENT_DEPENDENCY_LEMMA.md`](PARTIAL_EFX_TRANSFER_COMPONENT_DEPENDENCY_LEMMA.md)
  — cap-free localization of that eligibility coupling. Any EFX failure of a
  component allocation crosses to another nontrivial transfer component; if
  every component fails, the resulting dependency digraph contains a directed
  cycle. In the exact corpus, all 82 ineligible positive components fail only
  EFX rather than floater parking, and all 22 all-component failures exhibit
  the predicted cycle. Every observed cycle is a mutual two-component cycle;
  21 of 22 have positive gain in both components.
- [`PARTIAL_HALL_TWO_COMPONENT_REROUTE_GATE.md`](PARTIAL_HALL_TWO_COMPONENT_REROUTE_GATE.md)
  and
  [`partial_hall_two_positive_reroute_corpus_search.json`](partial_hall_two_positive_reroute_corpus_search.json)
  — exact refutation of the tempting one-good splice. Among 25 qualifying
  two-positive rivals across 21 row-scale-distinct canonical Hall
  obstructions, one profile supplies four distance-five rivals with no
  connected eligible improving one-good reroute. Each has a successful
  connected bridge at distance two. This redirects the proof toward using
  the disconnected dependency-cycle union directly.
