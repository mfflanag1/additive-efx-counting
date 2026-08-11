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

The August 3 anti-local-minimum checkpoint is
[`EFX_BREAKTHROUGH_ROUTE_AUDIT_20260803.md`](EFX_BREAKTHROUGH_ROUTE_AUDIT_20260803.md).
It freezes the diminishing-return completion-cut branch and promotes a
unified charity Hall-absorption target under explicit falsification and
proof-compression gates. The proved entry points are
[`CHARITY_HALL_ABSORPTION_EQUIVALENCE.md`](CHARITY_HALL_ABSORPTION_EQUIVALENCE.md),
[`PARTIAL_CHARITY_LEXICOGRAPHIC_BOTTLENECK_LEMMA.md`](PARTIAL_CHARITY_LEXICOGRAPHIC_BOTTLENECK_LEMMA.md),
[`PARTIAL_CHARITY_MATCHED_SLACK_EXCHANGE_LEMMA.md`](PARTIAL_CHARITY_MATCHED_SLACK_EXCHANGE_LEMMA.md),
[`PARTIAL_THRESHOLD_UNIQUE_DEFECT_HANDOFF_LEMMA.md`](PARTIAL_THRESHOLD_UNIQUE_DEFECT_HANDOFF_LEMMA.md),
[`PARTIAL_THRESHOLD_UNIQUE_DEFECT_HALL_TRICHOTOMY.md`](PARTIAL_THRESHOLD_UNIQUE_DEFECT_HALL_TRICHOTOMY.md),
[`PARTIAL_THRESHOLD_HOST_REDIRECTION_AUDIT.md`](PARTIAL_THRESHOLD_HOST_REDIRECTION_AUDIT.md),
[`PARTIAL_THRESHOLD_FULL_UNIQUE_DEFECT_COMPONENT_GATE.md`](PARTIAL_THRESHOLD_FULL_UNIQUE_DEFECT_COMPONENT_GATE.md),
[`GENERAL_TRANSFER_COMPONENT_HYBRID_WALL_LEMMA.md`](GENERAL_TRANSFER_COMPONENT_HYBRID_WALL_LEMMA.md),
[`UNIQUE_DEFECT_CHAMPION_BRIDGE_LEMMA.md`](UNIQUE_DEFECT_CHAMPION_BRIDGE_LEMMA.md),
[`HOST_INTERFERENCE_LOCALIZATION_LEMMA.md`](HOST_INTERFERENCE_LOCALIZATION_LEMMA.md),
[`MULTI_BOTTOM_CARDINALITY_GATE.md`](MULTI_BOTTOM_CARDINALITY_GATE.md),
[`RECIPROCAL_CHAMPION_THRESHOLD_GATE.md`](RECIPROCAL_CHAMPION_THRESHOLD_GATE.md),
[`PARTIAL_GENERAL_CHARITY_MINIMUM_SWAP_LEMMA.md`](PARTIAL_GENERAL_CHARITY_MINIMUM_SWAP_LEMMA.md),
[`PARTIAL_GENERAL_OWNER_EXCHANGE_PLATEAU_LEMMA.md`](PARTIAL_GENERAL_OWNER_EXCHANGE_PLATEAU_LEMMA.md),
and
[`PARTIAL_THRESHOLD_BOTTLENECK_HALL_CUT_LEMMA.md`](PARTIAL_THRESHOLD_BOTTLENECK_HALL_CUT_LEMMA.md).
The absorption-gradient lemma remains unproved, so neither four-agent nor
general additive EFX is claimed.

The host-redirection audit is a deliberate anti-local-minimum result. It
finds an exact four-agent witness refuting the corpus-suggested local
host--bad reduction while confirming that the witness itself absorbs through
another host. Thus future arguments must use global selector extremality and
must not elevate the 4,320/4,320 corpus pattern into a theorem.

The corrected two-source champion bridge makes that warning exact. The bad
agent need not champion the augmented host: the host can be the competing
most-envious source, as a frozen local \((4,8)\) counterexample demonstrates.
All 4,320 full-witness corpus states nevertheless lie in the bad-source branch
and have threshold-neutral, one-charity reciprocal champion cycles, but
separate exact local profiles refute reciprocity, champion-cycle
threshold nonnegativity, and their naive combination with a bad-owner minimum
swap. Every refuting state lies below absorbing global maxima. The proved
host-wall propagation lemma converts the remaining reciprocal wall into a
new host-minimum swap wall, while nonreciprocity redirects the incoming
champion edge through an external owner. Global wall cancellation remains the
unproved step.

The revised \((\Theta,U,\Lambda)\) selector is independently enumerated in
[`threshold_utility_tiebreak_corpus_audit.json`](threshold_utility_tiebreak_corpus_audit.json):
all 1,128 combinations of 47 hard profiles and 24 agent orders select an
absorbing state. The profiles include the Chaudhury lex-potential
counterexample. This is a finite-corpus result, not a general theorem.

Exact selector falsification is implemented by
`scan_charity_threshold_absorption.py`,
`search_charity_selector_anneal.py`, and
`exhaust_charity_threshold_selector.py`. The seven
`charity_threshold_selector_*_exhaustion.json` artifacts cover 811,315
row-normalized finite profiles without a negative selector margin. These are
finite-domain theorems and must not be cited as unrestricted EFX existence.

The earlier four-agent Hall-gradient branch removed the fixed off-host
edge profile and proved its first structural consequence in the full cyclic
pair-Hall cell: each owner's core good weakly dominates both the floater and
the preceding pair's token. Two cyclic cross-row clause families are also
proved; the residual pair-Hall cell remains open. See
[`PARTIAL_THRESHOLD_PAIR_HALL_CORE_DOMINANCE_LEMMA.md`](PARTIAL_THRESHOLD_PAIR_HALL_CORE_DOMINANCE_LEMMA.md)
and
[`PARTIAL_THRESHOLD_PAIR_HALL_CROSS_ROW_CLAUSES.md`](PARTIAL_THRESHOLD_PAIR_HALL_CROSS_ROW_CLAUSES.md).
The human
[`rotating-token lemma`](PARTIAL_THRESHOLD_ROTATING_TOKEN_LEMMA.md) supplies a
valid cyclic symmetry break; its canonical pool currently stands at
159/78/38 and remains open.

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
- [`SMALL_INTEGER_COUNTEREXAMPLE_BOUND.md`](SMALL_INTEGER_COUNTEREXAMPLE_BOUND.md).

The singleton-swap lemma is a genuine local exchange theorem, but no
covering argument currently shows that every hypothetical all-orders-blocked
family contains its pattern. It therefore does not resolve complete EFX.

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
  distances three, three, and two. One seven-good size-four/radius-two cell
  is independently UNSAT in Z3 and cvc5.
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
- [`ADAPTIVE_ROOT_ORDER_BRIDGE_REFUTATION_20260809.md`](ADAPTIVE_ROOT_ORDER_BRIDGE_REFUTATION_20260809.md)
  — exact alternating-atom obstruction to closing the two surviving orders
  by canonical root flip, half-turn, or priority relabeling alone. Both
  promoted rotations and three immediate two-good exchanges fail strictly;
  the unique minimum escape for `(s,p,q,r)` is a one-good anchored suffix
  transfer. This identifies why the suffix operation in the reservoir
  theorem is necessary; it does not refute the broader adaptive escape.
- [`ALTERNATING_RESERVOIR_EXCHANGE_LEMMA.md`](ALTERNATING_RESERVOIR_EXCHANGE_LEMMA.md)
  — cap-free analytic closure of the two surviving external-observer orders.
  A minimal `q`-threshold reservoir set is either common-safe or its unsafe
  deletion contains a desired `r`/`s` set paid by the original disjoint safe
  block. This proves the arbitrary-packet two-safe packing lemma and its
  half-turn. A subsequent dual-reservoir argument closes two of the four
  hard orders with refuted observer candidates; complete four-agent EFX
  remains open.
- [`ALTERNATING_DUAL_RESERVOIR_TRICHOTOMY.md`](ALTERNATING_DUAL_RESERVOIR_TRICHOTOMY.md)
  — cap-free analytic escape theorem for `(p,s,q,r)` and its half-turn.
  Minimal threshold extraction yields either a same-offer promotion, an
  anchored `q`-handoff, or an opposite-reservoir root promotion. Together
  with root flip and reservoir exchange this closes all eight hard
  alternating priority orders. The strict same-champion-offer refinement is
  open but unnecessary for the wider escape theorem.
- [`ALTERNATING_GLOBAL_LEX_CAPFREE_THEOREM.md`](ALTERNATING_GLOBAL_LEX_CAPFREE_THEOREM.md)
  — complete cap-free analytic cover of all 24 priority orders in the
  arbitrary-packet alternating topology: 16 easy singletonizations, two
  root flips, two reservoir exchanges, and four dual-reservoir escapes.
  This closes the alternating two-large residual, not general four-agent
  additive EFX.
- [`ALTERNATING_EXTENSION_OR_HANDOFF_REDUCTION.md`](ALTERNATING_EXTENSION_OR_HANDOFF_REDUCTION.md)
  — cap-free reduction of the stricter same-champion-offer refinement to one
  intersecting `r`-source wall, followed by its exact eight-good refutation.
  The audit exhausts all 390,625 allocations: zero anchored escapes, zero
  desired promotions from `X_r+f`, and 162 cross-face escapes. The smallest
  missing operation is an opposite-reservoir desired-root promotion, already
  covered by the broader alternating global-lex theorem.
- [`alternating_variable_extension_1121_refutation.json`](alternating_variable_extension_1121_refutation.json)
  and [`alternating_variable_extension_1121_refutation_audit.json`](alternating_variable_extension_1121_refutation_audit.json)
  — positive eight-good profile and independent exhaustive certificate
  refuting the strict anchored-or-original-offer bridge. This is not an EFX
  counterexample.
- [`LENGTH_THREE_GLOBAL_LEX_TARGET.md`](LENGTH_THREE_GLOBAL_LEX_TARGET.md)
  — source-valid reconstruction and completed cap-free closure of the BCFF
  two-large length-three residual. The final reservoir-order theorem
  supersedes the retained extremal-pair and pivot-wall proof-mining history.
  This closes one residual topology, not general additive EFX.
- [`LENGTH_THREE_AP_CANONICAL_ESCAPE_LEMMA.md`](LENGTH_THREE_AP_CANONICAL_ESCAPE_LEMMA.md)
  — cap-free analytic closure of the sole external-`p` priority row
  `(s,p,r,q)`. A minimal-payment boundary sourced by `p` or `s` reverses
  directly; a `q` boundary is paid either by the singleton `x` or by the
  least-`r` suffix rotation `({x,h},E-h,F,{y})`. No maximizing bundle,
  packet-size cap, or anchor-safety case remains in this row.
- [`LENGTH_THREE_AR_TAIL_ESCAPE_LEMMA.md`](LENGTH_THREE_AR_TAIL_ESCAPE_LEMMA.md)
  — cap-free analytic closure of the external-`r` orders `(p,s,r,q)` and
  `(s,p,r,q)`. The same canonical minimal-payment dichotomy works because
  the edge `r -> s` rules out the suffix allocation's sole external
  observer wall. The later reservoir-order theorem closes the two formerly
  open dual-base rows as well.
- [`LENGTH_THREE_EARLY_R_DUAL_BASE_REDUCTION_20260809.md`](LENGTH_THREE_EARLY_R_DUAL_BASE_REDUCTION_20260809.md)
  — cap-free base-threshold extraction for the two remaining external-`r`
  orders. The atomic core `(T_r+f,B_r+T_q,{x},{y})` lifts to arbitrary
  packets unless an unsafe payment exposes a `p`- or `q`-desired set using
  both `B_r` and `T_q`. In the `q`-source branch its `B_r` part must exceed
  `B_q` for both `q` and `r`. This is a reduction, not a closure theorem.
- [`length_three_early_r_dual_base_scalar_audit.json`](length_three_early_r_dual_base_scalar_audit.json)
  — byte-replayable QF_LRA audit of the four additive implications used by
  the early-`r` reduction. Desired-set extraction and PI routing remain the
  analytic proof layer.
- [`LENGTH_THREE_AQ_ADAPTIVE_SINGLETON_REDUCTION.md`](LENGTH_THREE_AQ_ADAPTIVE_SINGLETON_REDUCTION.md)
  — cap-free reduction of all four external-`q` rows. Assigning the two
  singleton roots adaptively closes every minimal-payment source except two
  explicit cases where `y` is simultaneously too small to anchor `p` and
  to pay `r`; the remaining witness is one strict `s`- or `q`-preference
  for `x`. This remains a valid reduction but is superseded as a completion
  gate by the reservoir-order theorem.
- [`LENGTH_THREE_PARALLEL_ROOT_PIVOT_REDUCTION.md`](LENGTH_THREE_PARALLEL_ROOT_PIVOT_REDUCTION.md)
  — cap-free safety closure of the remaining parallel-root recurrence. Returning
  the charity-swap pivot to a newly exposed `p`-root strictly improves the
  `p` coordinate; every augmentation failure containing the pivot is either
  an ordinary PI cycle or a champion handoff. The later reservoir-order
  theorem bypasses the compatible-payment residual entirely.
- [`LENGTH_THREE_AUGMENTED_ROOT_PAYMENT_REDUCTION.md`](LENGTH_THREE_AUGMENTED_ROOT_PAYMENT_REDUCTION.md)
  — cap-free routing of every minimal-payment source for an externally safe
  augmented root. A `p` source closes directly; a `q` or `s` source uses
  the appropriate singleton plus the least-`p` root good to compensate
  `r`. The explicit compensation deficit is no longer a completion gate.
- [`length_three_augmented_root_payment_audit.json`](length_three_augmented_root_payment_audit.json)
  — exact five-case QF_LRA replay of the candidate-allocation algebra in
  the augmented-root payment reduction.
- [`LENGTH_THREE_RESERVOIR_ORDER_ESCAPE_THEOREM.md`](LENGTH_THREE_RESERVOIR_ORDER_ESCAPE_THEOREM.md)
  — cap-free analytic closure of all length-three priority/source types.
  The two reservoir orientations partition the 24 orders according to
  whether `q` or `r` comes first; low reversals in the second orientation
  can only be sourced by `r` or `s`.
- [`LENGTH_THREE_BCFF_COMPOSITION_AUDIT.md`](LENGTH_THREE_BCFF_COMPOSITION_AUDIT.md)
  — requirement-by-requirement proof that the BCFF length-three branch
  supplies every premise of the reservoir-order theorem, including packet
  nonemptiness, the external singleton edge, and the generalized PI source
  wall; no chordless or exact-graph assumption is used.
- [`length_three_reservoir_order_packet_audit.json`](length_three_reservoir_order_packet_audit.json)
  — exact 24-case QF_LRA replay of both reservoir orientations for all
  three external sources.
- [`length_three_parallel_pivot_scalar_audit.json`](length_three_parallel_pivot_scalar_audit.json)
  — exact QF_LRA replay of the owner/selected-edge top ordering, the failed-
  fallback charity-versus-pivot inequality, and the strict augmented-root
  improvement, and the fact that residual-capacity failure forces the pivot
  above the entire `q`-bottom packet. All four negated implications are
  UNSAT.
- [`length_three_global_lex_atomic_sweep.json`](length_three_global_lex_atomic_sweep.json)
  and [`length_three_global_lex_atomic_sweep_audit.json`](length_three_global_lex_atomic_sweep_audit.json)
  — exact motif audit of all 72 atomic external-source/priority cells. Every
  cell is UNSAT with a core of at most three allocations; this is explicitly
  proof-mining evidence, not a packet theorem.
- [`length_three_selected_residual_atomic_cores.json`](length_three_selected_residual_atomic_cores.json)
  and [`length_three_selected_residual_atomic_cores_audit.json`](length_three_selected_residual_atomic_cores_audit.json)
  — exact replay of the nine remaining atomic types after dropping every
  nonselected envy/champion exclusion. All remain UNSAT, showing that the
  chordless normalization is not carrying the atomic result; packet closure
  still requires the contested-top lemma.
- [`length_three_dual_mode_adversarial_audit.json`](length_three_dual_mode_adversarial_audit.json)
  — exact census of the adaptive `r`-payment/`s`-payment potential on 26
  adversarial profiles. All 25 profiles with a feasible mode have a direct
  EFX Pareto escape; the sole failure is the known Pareto-maximal `V*`, which
  lacks the length-three residual-capacity premise. This is corpus evidence,
  not a packet theorem.
- [`length_three_lex_tail_adversarial_audit.json`](length_three_lex_tail_adversarial_audit.json)
  — byte-replayable exact search using the weaker payment thresholds
  justified by the two surviving lexicographic orders. Both the `p`-first and
  `s`-then-`p` tail-payment families escape all 26 frozen adversarial
  profiles, including `V*`. This removes a corpus obstruction but is not a
  cap-free theorem.
- [`length_three_tail_extremal_adversarial_audit.json`](length_three_tail_extremal_adversarial_audit.json)
  — exact falsification audit for the one-mode extremal selector. Among 57
  Pareto-maximal `r`-tail pairs on 28 adversarial/length-three profiles, nine
  lack a direct payment; seven reverse through `s`, while two retain a
  `p/q` boundary blocker. This refutes only the abstract one-mode inference.
- [`length_three_hybrid_extremal_adversarial_audit.json`](length_three_hybrid_extremal_adversarial_audit.json)
  — byte-replayable exact audit of the asymmetric `r`-tail/`s`-base
  potential. Every one of 54 Pareto-maximal hybrid pairs has a direct EFX
  payment on the expanded 28-profile corpus, including the two exact
  length-three models. The canonically anchored subfamily (`f in P`,
  `x in Q`) likewise has zero failures across its 52 Pareto-maximal pairs.
  The fixed-`P`, maximizing-`Q` subfamily is structurally feasible on 24
  profiles and has zero failures at all 24 unique maxima.
  The corpus uses the `a=r` singleton-source pattern; this is adversarial
  evidence for that sub-tier, not a cap-free or all-source theorem.
- [`length_three_hybrid_atom_exact.json`](length_three_hybrid_atom_exact.json)
  — exact QF_LRA decisions for all singleton-source types in the seven-good
  length-three atom: 4,096 `R`-tail forms for `a=p`, 8,192
  `R`-tail/`S`-base forms for `a=r`, and 4,096 `R`-tail forms for `a=q`.
  Every formula is UNSAT, supporting the source-valid motif only; this is not
  an arbitrary-packet proof.
- [`length_three_ap_suffix_atom_exact.json`](length_three_ap_suffix_atom_exact.json)
  — exact 14-case QF_LRA audit of the trimmed suffix rotation in the atomic
  `a=p`, external-`q` source motif, including tied least-`r` pivots. Every
  case is UNSAT. This corroborates the cap-free packet proof's local algebra;
  it does not replace that proof. The later canonical dichotomy eliminates
  the former unsafe-payment wall for this source type.
- [`length_three_canonical_packet_audit.json`](length_three_canonical_packet_audit.json)
  — exact QF_LRA replay of all sixteen aggregate packet calculations in the
  external-`p` canonical lemma, external-`r` tail lemma, and both
  orientations of the external-`q` adaptive-singleton reduction. Every
  negated EFX conclusion is UNSAT. The audit verifies the local algebra;
  the structural derivation of its inequalities remains analytic.
- [`length_three_dual_mode_atom_exact.json`](length_three_dual_mode_atom_exact.json),
  [`length_three_dual_mode_atom_selected.json`](length_three_dual_mode_atom_selected.json),
  and [`length_three_dual_mode_split_refutation.json`](length_three_dual_mode_split_refutation.json)
  — targeted fixed-root falsification boundary. The exact chordless atom
  forces one of fourteen canonical payments, while the selected-edge atom
  and the exact `(2,2,2,2)` packet cell refute that fixed-root strengthening.
  The packet model's minimum unrestricted dual-mode escape is a three-good
  anchored suffix cycle. These decisions motivate the arbitrary compatible-
  pair potential and do not establish the cap-free length-three theorem.
- [`ALTERNATING_EXTERNAL_OBSERVER_RESOLUTION_20260809.md`](ALTERNATING_EXTERNAL_OBSERVER_RESOLUTION_20260809.md)
  — the complete eight-order classification: two cap-free theorems and six
  exact strict countermodels, with the distinction between failure of the
  anchored candidate and availability of other rival forms made explicit.
- [`TRAPPED_SOURCE_RETURN_LENGTH_TWO_CLOSURE_THEOREM.md`](TRAPPED_SOURCE_RETURN_LENGTH_TWO_CLOSURE_THEOREM.md)
  — cap-free closure of the two-genuine-edge length-two cycle, including
  distinct and shared external bottom-edge sources. The artifact was
  recovered from the original research worktree and now makes its BCFF
  Theorem 3.16 internal-to-external reduction explicit.
- [`TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md`](TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md)
  — cap-free composition of the length-two, length-three, adjacent, and
  alternating selected-cycle classes. The four classes are exhaustive
  without assuming a chordless champion graph, so a globally lex-maximal
  noncomplete state cannot have exactly two nonsingleton bundles. This is a
  theorem for one branch of the BCFF normal form, not general additive EFX.
- [`THREE_NONSINGLETON_CYCLE_CENSUS_AND_FLOWER_REDUCTION_20260809.md`](THREE_NONSINGLETON_CYCLE_CENSUS_AND_FLOWER_REDUCTION_20260809.md)
  — exact eight-class census for selected cycles with three nonsingleton
  bundles, plus a cap-free reduction of the length-two class to a
  three-packet champion flower. An exact positive nondegenerate local profile
  shows why the singleton return lemma cannot be extended to the external
  large owner. An exhaustive 864-cell cover then closes half the cells
  directly and reduces every other cell to one low-payment wall for `r` or
  `q`. Four-cover strict-cycle menus close another 148 cells, leaving 284
  cap-free low-wall cells. A true-tail atomic audit leaves 116 bounded cells
  and extracts a two-good generalized exchange after all one-good transfers
  are blocked. A cap-free packet-total/minimum theorem then reduces all eight
  `a=c` source patterns to crossing desired sets and two explicit full-bundle
  capture alternatives. Later exact gates refute immediate swap/PI closure
  and simple owner-path closure, replacing them with the connected
  owner/charity multigraph target below. The flower remains open; this is not
  a general-EFX proof.
- [`BILATERAL_SWAP_OBSTRUCTION_LEMMA_20260810.md`](BILATERAL_SWAP_OBSTRUCTION_LEMMA_20260810.md)
  — cap-free classification of every failed priority-directed item swap.
  External target walls have one of two opposite item-order signs and yield
  the corresponding generalized exchange edge; a losing later owner is the
  sole source-wall case. This supplies the local edge conversion needed by
  the full-capture PI target but does not select a successful swap or close
  the flower.
- [`FULL_CAPTURE_SWAP_PI_GATE_REFUTATION_20260810.md`](FULL_CAPTURE_SWAP_PI_GATE_REFUTATION_20260810.md)
  — exact two-good-per-component refutation of the proposed immediate
  swap/PI closure. Even after every priority-directed one- and two-good
  exchange is blocked, a source-safe improving bottom swap can have an
  external wall whose generalized edge lacks release support. The frozen
  model's nearest improving EFX-with-charity allocation moves three goods in
  a connected owner/charity multigraph. This redirects the cap-free target from a
  fixed-radius swap lemma to component growth; it is not an EFX
  counterexample. A strengthened model blocks every simple three-good owner
  path and escapes through a connected owner/charity multigraph instead, so
  the target must allow repeated slots and charity-cardinality changes.
- [`PACKET_CHARITY_REPLACEMENT_OBSTRUCTION_LEMMA_20260810.md`](PACKET_CHARITY_REPLACEMENT_OBSTRUCTION_LEMMA_20260810.md)
  — cap-free classification of replacing an arbitrary owner packet by the
  charity good and releasing that packet into charity. A target wall forces
  the observer to rank the charity good above the whole packet; a charity
  wall forces the opposite strict ranking. With no wall the move is an EFX-
  with-charity lexicographic improvement. This supplies the charity-side
  signed dependency rule but does not select an improving packet.
  An exact strengthening blocks every such packet replacement and survives;
  its nearest escapes are three-edge hub-splitting components, identifying
  packet partition among multiple recipients as the next primitive.
- [`PACKET_REPLACEMENT_CHARITY_ABSORPTION_LEMMA_20260810.md`](PACKET_REPLACEMENT_CHARITY_ABSORPTION_LEMMA_20260810.md)
  — cap-free closure of an isolated charity wall. The wall owner absorbs the
  released common-safe packet and releases her old bundle; a `q`-sourced
  replacement is immediately PI, while every survivor is a new-owner edge
  or a Hall defect missing `q`.
- [`packet_replacement_charity_absorption_audit.json`](packet_replacement_charity_absorption_audit.json)
  — dual-solver symbolic replay of the absorption edge's packet support and
  strict-desire implication.
- [`PACKET_REPLACEMENT_COMPLEMENT_RETURN_LEMMA_20260810.md`](PACKET_REPLACEMENT_COMPLEMENT_RETURN_LEMMA_20260810.md)
  — cap-free return theorem for an external response `K+f` to the selected
  replacement. Returning the entire released complement closes PI; every
  survivor obeys `q(X_a)<q(K)<q(X_q)-q(f)` or names a Hall source. The other
  mutual owner is excluded analytically, leaving only `c,s`. The theorem
  also selects a `T_r` payment packet and reduces the root flip to one
  two-row compensation system with exact response-Hall support.
- [`packet_replacement_complement_return_audit.json`](packet_replacement_complement_return_audit.json)
  — dual-solver symbolic replay of the two-edge packet support and strict
  core-capture interval.
- [`MAXIMAL_REPLACEMENT_FRONTIER_EXCHANGE_LEMMA_20260810.md`](MAXIMAL_REPLACEMENT_FRONTIER_EXCHANGE_LEMMA_20260810.md)
  — cap-free global selection of a value-maximal packet below `f`. Every
  residual packet crosses the remaining `q`-slack, and every beneficial
  exchange across the frontier jumps a strict forbidden band. A surviving
  core capture therefore leaves a nonempty threshold-crossing pivot. This
  supplies a discrete potential for adaptive replacement growth but does
  not by itself solve the two-row compensation/Hall gate.
- [`maximal_replacement_frontier_exchange_audit.json`](maximal_replacement_frontier_exchange_audit.json)
  and [`maximal_replacement_frontier_profile_census.json`](maximal_replacement_frontier_profile_census.json)
  — dual-solver scalar replay plus an exact adversarial census of the seven
  frozen flower profiles. All four displayed external responses return or
  compensate; this is regression evidence, not a cap-free exhaustion.
- [`PACKET_REPLACEMENT_AGGREGATE_ROOT_FLIP_POLARITY_LEMMA_20260810.md`](PACKET_REPLACEMENT_AGGREGATE_ROOT_FLIP_POLARITY_LEMMA_20260810.md)
  — cap-free full-packet instance of the canonical root flip. It closes
  whenever the earlier root accepts the entire released complement and the
  external bundle is worth at least `f` to `q`; failure forces a named
  `R-wall` or `Q-wall`. With a maximal frontier, the latter becomes the
  strict order `q(O)>q(f)>q(X_a)`.
- [`packet_replacement_aggregate_root_flip_polarity_audit.json`](packet_replacement_aggregate_root_flip_polarity_audit.json)
  — dual-solver scalar replay of the aggregate payment implication.
- [`ALTERNATING_PAYMENT_COMPENSATION_CHAIN_LEMMA_20260810.md`](ALTERNATING_PAYMENT_COMPENSATION_CHAIN_LEMMA_20260810.md)
  — cap-free adaptive solution of the packet-selection search. Minimal
  `q`-payment and `r`-compensation repairs alternately enlarge two disjoint
  packets, so every repair branch terminates. A successful leaf is the
  canonical root flip; exhaustion forces either an explicit root wall or
  `q(O)>q(f)>q(X_a)`, with every inserted packet deletion-critical.
- [`alternating_payment_compensation_chain_audit.json`](alternating_payment_compensation_chain_audit.json)
  — dual-solver replay of both exhaustion implications. The frozen strict-
  capture profile has a three-state repair tree with one successful leaf,
  confirming that minimal-repair ties must remain adaptive.
- [`CHARITY_ROOTED_TRANSFER_TREE_RESPONSE_HALL_LEMMA_20260810.md`](CHARITY_ROOTED_TRANSFER_TREE_RESPONSE_HALL_LEMMA_20260810.md)
  — cap-free component theorem covering every charity-rooted packet tree,
  including stars, paths, and hubs whose leaves donate onward. If the
  selected endpoint is not already EFX, every internal response SDR is PI;
  otherwise an open source or minimal Hall defect is named. This lifts both
  hardened radius-four escape topologies to arbitrary packets.
- [`charity_rooted_transfer_tree_release_audit.json`](charity_rooted_transfer_tree_release_audit.json)
  — exact release-support replay of all 405 labeled rooted-tree/internal-
  response-permutation pairs through four owners.
- [`Q_EXHAUSTION_ROOT_SWITCH_LEMMA_20260810.md`](Q_EXHAUSTION_ROOT_SWITCH_LEMMA_20260810.md)
  — converts every Q-exhausted compensation leaf into a canonical complete
  transfer tree. If `E` is the uncompensated released remainder, exhaustion
  forces `q(f)>q(E)+q(X_a)`; root `q` replaces `E` by `f` and sends `E` to
  the external owner. Thus Q-exhaustion now ends only at an EFX endpoint,
  PI matching, open source, or named Hall defect.
- [`q_exhaustion_root_switch_audit.json`](q_exhaustion_root_switch_audit.json)
  — dual-solver scalar and release-support replay of the root switch.
- [`RELEASED_OWNER_COMPENSATION_CHAIN_LEMMA_20260810.md`](RELEASED_OWNER_COMPENSATION_CHAIN_LEMMA_20260810.md)
  — expands the alternating compensation reservoir from `X_q-K` to
  `(X_q-K)+X_a`, using the entire bundle released when the responder receives
  `K+f`. Successful leaves are release-compatible components; Q-exhaustion
  still root-switches, and only the sharper wall `r((X_q-K)+X_a)<r(P)`
  survives.
- [`released_owner_compensation_chain_audit.json`](released_owner_compensation_chain_audit.json)
  — dual-solver exhaustion and packet-support replay for the expanded chain.
- [`OPEN_LEAF_SOURCE_ROTATION_LEMMA_20260810.md`](OPEN_LEAF_SOURCE_ROTATION_LEMMA_20260810.md)
  — cap-free growth step for a new source `b` responding to leaf `X_a+E`.
  Rotate its desired subset to `b` and the complement plus `X_b` back to
  `a`; either the improving component gains an owner or an exact strict
  capture wall is forced. The hardened adversary grows from `q,s` to
  `q,c,s` and then exposes `r`.
- [`open_leaf_source_rotation_audit.json`](open_leaf_source_rotation_audit.json)
  — dual-solver scalar and release-support replay of the source rotation.
- [`OUTSIDE_SOURCE_SINK_AUGMENTATION_LEMMA_20260810.md`](OUTSIDE_SOURCE_SINK_AUGMENTATION_LEMMA_20260810.md)
  — general cap-free induction behind repeated source rotations. An outside
  source takes a desired subset of the current sink target and the sink gets
  its complement plus the source's old bundle. Either the represented owner
  set grows, or the sink values the captured subset above the source bundle
  plus its entire accumulated improvement margin. Release compatibility is
  preserved at every successful step.
- [`outside_source_sink_augmentation_audit.json`](outside_source_sink_augmentation_audit.json)
  — dual-solver capture and abstract support-preservation replay.
- [`hardened_q_wall_sink_augmentation_pi_audit.json`](hardened_q_wall_sink_augmentation_pi_audit.json)
  — solver-free exact end-to-end closure of the hardened Q-wall profile.
  Two successful augmentations represent all four owners; the final response
  relation has matching `q<-s,c<-c,r<-r,s<-q`, whose disjoint incoming
  packets are internally supplied. This is a generalized PI certificate,
  not merely a nearby EFX witness.
- [`FULL_RESERVOIR_R_WALL_TOP_CAPTURE_LEMMA_20260810.md`](FULL_RESERVOIR_R_WALL_TOP_CAPTURE_LEMMA_20260810.md)
  — localizes the only compensation wall not converted to a component.
  Combining full-reservoir failure with `r`'s desired `T_q+f` bundle forces
  the response core's top portion to dominate the omitted bottom plus the
  external owner's entire bundle in `r`'s row. Bottom-only cores—used by all
  current strict-capture adversaries—cannot realize this wall.
- [`full_reservoir_r_wall_top_capture_audit.json`](full_reservoir_r_wall_top_capture_audit.json)
  — dual-solver scalar replay of the strict top-capture implication.
- [`TOP_CORE_ROOT_EXCHANGE_LEMMA_20260810.md`](TOP_CORE_ROOT_EXCHANGE_LEMMA_20260810.md)
  — adaptive root/order flip for the remaining top core. Transfer `K_T` to
  `r`, give `f` to `q`, and return a deletion-minimal `q`-payment packet
  from `T_r`. The exchange closes unless `r` has the critical reverse order
  `r(P')>r(K_T)>r(B_q-K_B)+r(X_a)`.
- [`top_core_root_exchange_audit.json`](top_core_root_exchange_audit.json)
  — dual-solver payment-existence and two-edge release-support replay.
- [`FLOWER_LATER_OWNER_SINGLE_REPLACEMENT_SELECTOR_LEMMA_20260810.md`](FLOWER_LATER_OWNER_SINGLE_REPLACEMENT_SELECTOR_LEMMA_20260810.md)
  — cap-free analytic selection of a first improving packet-for-charity
  operation in every hard three-nonsingleton flower cell. The later owner on
  the mutual champion cycle must value `f` above some good of her bundle;
  otherwise three lex-valid common-safe cover walls form an impossible
  strict cycle. An exact packet-total/minimum replay checks all 1,020 hard
  source/support/order cells under two Z3 versions. This closes first-packet
  selection, but the target/charity wall dependency still needs a termination
  theorem before the `GG` flower is closed. A location census forces the
  selected good into the later owner's bottom packet in 754 cells; the other
  266 retain a top/bottom disjunction.
- [`FIXED_REPLACEMENT_LEX_COMPLETION_REFUTATIONS_20260810.md`](FIXED_REPLACEMENT_LEX_COMPLETION_REFUTATIONS_20260810.md)
  — dual-solver exact refutations of two natural ways to freeze the selected
  later-owner operation. Neither a fixed singleton replacement nor a fixed
  inclusion-maximal low packet must admit an EFX completion preserving the
  earlier owner. Both witnesses still have a two-good flexible EFX lex
  escape, so the corrected `GG` target must allow the distinguished bundle
  to evolve during dependency growth.
- [`FLOWER_DUAL_FULL_CAPTURE_ESCAPE_LEMMA_20260810.md`](FLOWER_DUAL_FULL_CAPTURE_ESCAPE_LEMMA_20260810.md)
  — cap-free flexible-completion theorem when the external bottom edge into
  the earlier mutual owner retains her entire top packet. Either the later
  owner replaces her bottom by `f`, or a dual rotation strictly improves
  both mutual owners. An exact symbolic gate reduces to precisely these two
  allocations without nondegeneracy assumptions. The surviving general
  gate is now a nonempty residual top packet whose reinsertion can recreate
  the original generalized edge instead of making monotone progress.
- [`FLOWER_THREE_ROTATION_POLARITY_LEMMA_20260810.md`](FLOWER_THREE_ROTATION_POLARITY_LEMMA_20260810.md)
  — cap-free three-allocation reduction valid before choosing an external
  bottom edge. If none is a flexible EFX escape, the mutual owners must rank
  `f` versus `B_q` in opposite directions, and the later owner must rank
  `T_r>T_q` and `B_q>B_r`. This confines the residual-recapture problem to
  one aggregate orientation; it does not yet contradict that orientation.
- [`FLOWER_EARLY_ROOT_CHARITY_ROTATION_LEMMA_20260810.md`](FLOWER_EARLY_ROOT_CHARITY_ROTATION_LEMMA_20260810.md)
  — cap-free fourth rotation showing that global lex maximality additionally
  forces `r(B_r)>=r(f)>r(B_q)`. Together with the later-owner polarity this
  makes the two mutual owners rank `B_r,B_q` in strict opposite orders.
- [`LEX_ROOTED_OWNER_CHARITY_DONATION_OBSTRUCTION_LEMMA_20260810.md`](LEX_ROOTED_OWNER_CHARITY_DONATION_OBSTRUCTION_LEMMA_20260810.md)
  — cap-free wall classification for the newly isolated operation in which
  the earlier root receives one donor good, the later donor may lose, and one
  root good joins charity. External root walls supply a generalized exchange
  edge; external charity walls must consume the released root good. The exact
  nondegenerate profile and solver-free replay are
  [`residual_flower_packet_countermodel.json`](residual_flower_packet_countermodel.json)
  and
  [`residual_flower_packet_countermodel_audit.json`](residual_flower_packet_countermodel_audit.json).
- [`residual_flower_global_lex_gate_audit.json`](residual_flower_global_lex_gate_audit.json)
  — dual-solver deletion-minimal five-allocation UNSAT core for the exact
  nine-good residual cell. This is proof-mining evidence, not an
  arbitrary-packet theorem; the packet countermodel above explains the exact
  failure of that lift.
- [`MECHANISM_INDEPENDENT_RADIUS3_GATE_20260810.md`](MECHANISM_INDEPENDENT_RADIUS3_GATE_20260810.md)
  — exact refutation of the local three-good endpoint target on the bounded
  representative live-polarity flower master. The first profile has a self
  PI edge; a second hardened positive subset-sum-injective profile survives
  exclusion of self champions, ordinary envy cycles, and one-genuine PI
  cycles while retaining zero EFX lex endpoints among all 41,394 connected
  allocations through radius three. Its first radius-four response has a
  Hall defect. Generalized multi-genuine PI-freeness and global maximality
  remain open, so the literal hard-state theorem is not refuted.
- [`FLOWER_MINIMAL_PAYMENT_RESIDUAL_ROTATION_LEMMA_20260810.md`](FLOWER_MINIMAL_PAYMENT_RESIDUAL_ROTATION_LEMMA_20260810.md)
  — cap-free selector using an inclusion-minimal `q`-paying packet from
  `T_r`. Both mutual owners improve, the entire complement is safe charity,
  and every failure is localized to one evolved-target wall.
- [`FLOWER_TWO_ROOT_RESIDUAL_SPLIT_RESPONSE_HALL_LEMMA_20260810.md`](FLOWER_TWO_ROOT_RESIDUAL_SPLIT_RESPONSE_HALL_LEMMA_20260810.md)
  — cap-free response-Hall composition for partitioning the released
  residual among the root and up to two external leaves. The two root edges
  release each other's incoming packets and supply every leaf cell, so all
  2, 6, and 24 internal response permutations are PI-compatible. Its
  return-response corollary closes an external wall whenever `q` responds to
  one augmented blocker bundle. The exact 16-partition census in
  [`residual_flower_two_root_partition_census.json`](residual_flower_two_root_partition_census.json)
  finds three such SDRs and closes the nondegenerate packet-lift adversary.
- [`FLOWER_RESIDUAL_WALL_PAYMENT_POLARITY_LEMMA_20260810.md`](FLOWER_RESIDUAL_WALL_PAYMENT_POLARITY_LEMMA_20260810.md)
  — cap-free proof that the earlier root can always be paid from the released
  residual. Any observer unpayable even by the whole residual must rank
  `B_q` above that residual, leaving only the two external-owner payment/Hall
  deficiency or a polarity-driven root flip.
- [`FLOWER_EXTERNAL_RETURN_AUGMENTATION_LEMMA_20260810.md`](FLOWER_EXTERNAL_RETURN_AUGMENTATION_LEMMA_20260810.md)
  — cap-free finite-growth theorem for an external response source. An
  ordinary or residual return from `q` closes PI; otherwise the process
  produces a low-return inequality or one named non-`q` source. With four
  owners only one genuinely new external augmentation is possible, leaving
  a closed Hall defect rather than an indefinite blocker chain.
- [`FLOWER_COMPLEMENT_RETURN_AUGMENTATION_LEMMA_20260810.md`](FLOWER_COMPLEMENT_RETURN_AUGMENTATION_LEMMA_20260810.md)
  — cap-free strengthening that routes the unused part of the blocked
  `q` target back with the external owner's base bundle and the residual.
  The resulting three incoming sets are disjoint and internally supplied;
  every surviving low-return branch obeys a strict deep-capture inequality.
- [`flower_complement_return_augmentation_audit.json`](flower_complement_return_augmentation_audit.json)
  — dual-solver symbolic replay of complement-return release support and
  both scalar capture implications.
- [`OWNER_ROOTED_HUB_SPLIT_RESPONSE_HALL_LEMMA_20260810.md`](OWNER_ROOTED_HUB_SPLIT_RESPONSE_HALL_LEMMA_20260810.md)
  — cap-free response-Hall theorem for an owner-supplied exchange star. The
  hub receives a donor packet and partitions its own released packet among
  that donor and other leaves. The donor and hub release each other's
  incoming sets, so every internal response SDR is a BCFF PI edge set. This
  adds the repeated-owner primitive missing from the charity-rooted lemma;
  flower-specific packet selection and deficient/open responses remain.
- [`CHARITY_ROOTED_HUB_SPLIT_OBSTRUCTION_LEMMA_20260810.md`](CHARITY_ROOTED_HUB_SPLIT_OBSTRUCTION_LEMMA_20260810.md)
  — cap-free classification of every EFX failure after an improving owner
  replaces a packet by the charity good and partitions the released packet
  among several recipients. Hub walls and leaf walls yield exact generalized
  edges with disjoint incoming packets. A directed closure is a BCFF PI edge
  set; otherwise the obstruction exposes an open source or a strict Hall
  deficiency. The lemma does not yet select a split or eliminate those two
  component-growth remainders.
- [`THREE_TARGET_HUB_HALL_CLASSIFICATION_20260810.md`](THREE_TARGET_HUB_HALL_CLASSIFICATION_20260810.md)
  — exhaustive 64-graph classification of the internal wall-source relation
  for one hub and two leaves. Thirty-two graphs contain a PI cycle through
  the hub, 29 expose a target with no internal wall, and the remaining three
  form one leaf-mutual family: the leaves block each other, at least one
  blocks the hub, and the hub never blocks a leaf. This isolates the only
  fully internally blocked analytic case.
- [`LEAF_MUTUAL_TRAP_SCALAR_GATE_REFUTATION_20260810.md`](LEAF_MUTUAL_TRAP_SCALAR_GATE_REFUTATION_20260810.md)
  — positive cap-six additive realization of the sole closed three-target
  Hall trap. Base EFX, charity dominance, hub improvement, both mutual leaf
  walls, both leaf-to-hub walls, and absence of hub-to-leaf walls coexist.
  Therefore the trap cannot be eliminated by summing local wall signs; the
  next proof must use flower champion identities or an alternate hub.
- [`ARM_OWNER_HUB_SELECTOR_REFUTATION_20260810.md`](ARM_OWNER_HUB_SELECTOR_REFUTATION_20260810.md)
  — exact full-capture model surviving blockage of every improving two-leaf
  split from the external arm owner, in addition to all earlier exchange,
  path, and packet gates. None of its arm-owner splits is itself EFX, but two
  have full most-envious response matchings and are PI; two are open and two
  Hall deficient. This preserves the corrected EFX-or-response-Hall selector
  while rejecting a one-star EFX endpoint.
- [`HUB_SPLIT_RESPONSE_HALL_LEMMA_20260810.md`](HUB_SPLIT_RESPONSE_HALL_LEMMA_20260810.md)
  — cap-free conversion of each proposed hub/leaf target into its exact set
  of most-envious generalized-edge sources relative to the base allocation.
  A hub self-source is PI, and any internal system of distinct representatives
  is a release-compatible PI edge set. This corrects the invalid shortcut of
  treating strong-envy observers as edge sources.
- [`ARM_RESPONSE_SELECTOR_GATE_REFUTATION_20260810.md`](ARM_RESPONSE_SELECTOR_GATE_REFUTATION_20260810.md)
  — exact full-capture model in which the external arm owner has no eligible
  two-leaf split, so every arm-rooted EFX/response-matching implication is
  vacuous. A mutual-cycle owner nevertheless has an outright EFX split. This
  replaces the fixed-arm selector by an alternate-hub eligibility dichotomy.
- [`ADJACENT_LARGE_GLOBAL_LEX_TARGET_20260809.md`](ADJACENT_LARGE_GLOBAL_LEX_TARGET_20260809.md)
  — analytic cap-free closure of all 24 priority orders in the adjacent-large
  length-four residual. The final five `p`-first types are closed by an
  endogenous safe-repartition theorem on `X_r+X_q+f`: reservoir extraction
  either pays `q` for `D_r`, or returns an arbitrary `r`-desired bundle for
  which `D_r` pays `q`. This proves the adjacent residual lemma, not complete
  four-agent EFX.
- [`adjacent_large_safe_repartition_cells_audit.json`](adjacent_large_safe_repartition_cells_audit.json)
  and [`adjacent_large_safe_repartition_core_2222.json`](adjacent_large_safe_repartition_core_2222.json)
  — exact corroboration of the safe-repartition theorem in the atom, all four
  one-packet splits, and the full binary cell, plus a 28-rival
  binary solver core. The exact cells are diagnostics; the cap-free result is
  the analytic theorem above.
- [`TOP_CORE_RESIDUAL_RESET_LEMMA_20260811.md`](TOP_CORE_RESIDUAL_RESET_LEMMA_20260811.md)
  — cap-free factorization of the critical top-core reverse-order leaf into
  the existing minimal-payment two-root response-Hall component. The strict
  complementary top-packet order and residual-rotation payment are
  dual-version QF_LRA audited; response termination and prevention of a
  later revisit remain open.
- [`ALL_OWNER_HALL_RESPONSE_COMPRESSION_LEMMA_20260811.md`](ALL_OWNER_HALL_RESPONSE_COMPRESSION_LEMMA_20260811.md)
  — cap-free deficiency-one reduction for a minimal all-owner response Hall
  defect. Three sources take disjoint desired cores and the unique missing
  source receives every residual good, reducing the endpoint to one payment
  or recapture certificate. All 50,625 nonempty four-by-four response
  relations are exhaustively audited; residual payment is not asserted.
- [`WEIGHTED_RESPONSE_COMPRESSION_DUAL_LEMMA_20260811.md`](WEIGHTED_RESPONSE_COMPRESSION_DUAL_LEMMA_20260811.md)
  — cap-free minimum-cost selector for the compressed Hall endpoint. A paid
  matching leaves at most one residual wall; failure has an exact weighted
  assignment-dual certificate. The associated core recapture preserves the
  one-wall normal form and has one exact margin inequality. The scalar and
  weak-duality implications replay under two Z3 versions; elimination of the
  dual certificate remains open.
- [`LEX_SACRIFICED_RESPONSE_COMPRESSION_LEMMA_20260811.md`](LEX_SACRIFICED_RESPONSE_COMPRESSION_LEMMA_20260811.md)
  — exact priority-sensitive interpretation of an unpaid compression. Its
  cores capture part of the missing owner's base bundle above all unused
  external goods. For a non-`r` missing source, the resulting allocation is
  still a valid flexible/lex candidate and every EFX failure lies in one
  two-sided wall star; the singleton case captures its unique good.
- [`ROOT_ANCHORED_COMPRESSION_STAR_LEMMA_20260811.md`](ROOT_ANCHORED_COMPRESSION_STAR_LEMMA_20260811.md)
  — proves that `r` is always a response source through the contained
  common-safe root core `T_q+f`, so the missing source is never the earlier
  root. An aligned residual-response/core-wall pair strictly increases a
  finite recapture potential. A maximal obstruction must therefore be a
  disjoint cross-star with one strict four-level value order; eliminating
  that cross-star remains open.
- [`CROSS_STAR_HOLE_PIVOT_LEMMA_20260811.md`](CROSS_STAR_HOLE_PIVOT_LEMMA_20260811.md)
  — gives the cap-free alternating-matching pivot for a disjoint cross-star
  whose missing owner is also a base-response source for the envied core.
  The pivot preserves all goods, moves the unique residual hole, and
  localizes every new EFX failure to the same two-sided-star form. When the
  wall is not a base response, positivity and nondegeneracy instead force a
  strict source-inactive loss band. Root-facing stars and hole recurrence
  remain the analytic termination boundary.
- [`cross_star_hole_pivot_audit.json`](cross_star_hole_pivot_audit.json)
  — dual-version replay of the pivot's set partition, wall localization,
  priority split, and source-inactive loss band.
- [`COMMON_SAFE_TARGET_RESPONSE_RIGIDITY_LEMMA_20260811.md`](COMMON_SAFE_TARGET_RESPONSE_RIGIDITY_LEMMA_20260811.md)
  — proves that every strict base-response contained in a common-safe target
  is the whole target. Consequently a cross-star pivot moves its core side
  intact; all proper-subset support evolution occurs on the residual side.
- [`common_safe_target_response_rigidity_audit.json`](common_safe_target_response_rigidity_audit.json)
  — dual-version replay of the proper-subset contradiction and simplified
  five-case pivot support partition.
- [`WHOLE_CORE_RETURN_TWO_HOLE_DESCENT_LEMMA_20260811.md`](WHOLE_CORE_RETURN_TWO_HOLE_DESCENT_LEMMA_20260811.md)
  — replaces every priority-valid base-active nonroot core pivot by cap-free
  rank descent. Releasing the whole core with the residual gives two holes,
  strictly improves the old hole, and enters the fully classified 2-by-2
  response boundary. Core-side hole recurrence is thereby eliminated.
- [`whole_core_return_two_hole_descent_audit.json`](whole_core_return_two_hole_descent_audit.json)
  — dual-version replay of response rigidity, strict inherited gain,
  priority preservation, support partition, and the 16-relation continuation.
- [`ONE_CORE_THREE_HOLE_EXTERNAL_STAR_NORMAL_FORM_20260811.md`](ONE_CORE_THREE_HOLE_EXTERNAL_STAR_NORMAL_FORM_20260811.md)
  — applies three-agent EFX existence after a second rank descent and
  localizes every remaining failure to a root-centered signed star.
  Base-active reciprocal signs close by a two-owner PI component or
  unsafe-core augmentation; inactive reciprocal signs carry an exact loss
  band. The 64 signs split into 27 nonreciprocal and 37
  reciprocal-containing patterns.
- [`one_core_three_hole_external_star_normal_form_audit.json`](one_core_three_hole_external_star_normal_form_audit.json)
  — dual-version replay of wall localization, rigidity/loss-band polarity,
  reciprocal release support, and the complete 64-pattern split.
- [`FLOWER_RANK_ONE_ROOT_MONOPOLY_HANDOFF_LEMMA_20260811.md`](FLOWER_RANK_ONE_ROOT_MONOPOLY_HANDOFF_LEMMA_20260811.md)
  — uses the live mutual-edge payment polarity to produce a second target
  `T_r+B_q`. Any nonroot response source restores rank two; the unique
  rank-one response defect makes the root capture a nonempty packet of
  `B_q`. Thus the generic three-hole selector is replaced by an explicit
  flower bottom-capture handoff.
- [`flower_rank_one_root_monopoly_handoff_audit.json`](flower_rank_one_root_monopoly_handoff_audit.json)
  — dual-version replay of the live target inequality, all 15 nonempty
  response-source relations, disjoint target support, and forced bottom
  capture.
- [`ROOT_MONOPOLY_COMPLEMENT_ESCAPE_LEMMA_20260811.md`](ROOT_MONOPOLY_COMPLEMENT_ESCAPE_LEMMA_20260811.md)
  — terminates repeated root monopoly after one complement check. A desired
  complement cannot again be sourced by the root because two disjoint
  root-desired cores contradict base EFX; otherwise the first core captures
  all of `q`'s target surplus and its `B_q` packet dominates the root's
  omitted top plus whole bottom.
- [`root_monopoly_complement_escape_audit.json`](root_monopoly_complement_escape_audit.json)
  — dual-version replay of the root-row cancellation, twice-base exclusion,
  forced nonroot complement source, and terminal `q`-surplus capture.
- [`FLOWER_EXTERNAL_BOTTOM_EDGE_RANK_TWO_ANCHOR_LEMMA_20260811.md`](FLOWER_EXTERNAL_BOTTOM_EDGE_RANK_TWO_ANCHOR_LEMMA_20260811.md)
  — excludes rank-one termination in `GG`. The anchored root core and the
  known external bottom-edge core have disjoint support and distinct
  sources, so every attempted second descent resets canonically to the
  classified two-core/two-hole boundary.
- [`flower_external_bottom_edge_rank_two_anchor_audit.json`](flower_external_bottom_edge_rank_two_anchor_audit.json)
  — solver-independent replay of permanent matching, packet disjointness,
  complete reset support, and all 16 two-hole response relations.
- [`FLOWER_DUAL_ANCHOR_ROOT_PAID_SELECTOR_LEMMA_20260811.md`](FLOWER_DUAL_ANCHOR_ROOT_PAID_SELECTOR_LEMMA_20260811.md)
  — replaces an idempotent fixed-anchor reset by the opposite mutual/bottom
  anchor whenever its complement can pay the earlier root. A maximal
  root-safe partition either reaches the two-hole response boundary or
  exposes an item-named root-payment/root-envy critical good; infeasibility
  is the exact aggregate dual-pool deficit.
- [`flower_dual_anchor_root_paid_selector_audit.json`](flower_dual_anchor_root_paid_selector_audit.json)
  — symbolic replay of dual-root feasibility, root safety, the least-good
  move, and both critical-value rewrites.
- [`DUAL_POOL_MINIMAL_CORE_EXTRACTION_LEMMA_20260811.md`](DUAL_POOL_MINIMAL_CORE_EXTRACTION_LEMMA_20260811.md)
  — converts failure to pay the earlier root from the dual-anchor complement
  into an inclusion-minimal packet extracted from the two dual cores. If
  both sources survive the deletion the root-paid selector applies; otherwise
  the same packet captures a source's full strict response margin. In the
  full-capture cell the deficit cancels to a root-top/captured-bottom order.
- [`dual_pool_minimal_core_extraction_audit.json`](dual_pool_minimal_core_extraction_audit.json)
  — symbolic replay of minimality, root criticality, source-margin capture,
  and the full-capture support cancellation.
- [`CAPTURED_BOTTOM_EXTERNAL_COMPENSATION_CHAIN_LEMMA_20260811.md`](CAPTURED_BOTTOM_EXTERNAL_COMPENSATION_CHAIN_LEMMA_20260811.md)
  — lifts the strict full-capture `q -> external -> r` owner path to an
  arbitrary-packet alternating chain. It terminates in a root-payable dual
  selector, a root-top concentration certificate, or an opposite-order
  external-source capture; a same-source capture switches to the other
  bottom core or captures the later mutual owner's response margin.
- [`captured_bottom_external_compensation_chain_audit.json`](captured_bottom_external_compensation_chain_audit.json)
  — symbolic replay of support conservation, both exhaustion identities,
  opposite packet order, and the same-source top-switch dichotomy.
- [`FULL_CAPTURE_SOURCE_SAFE_HUB_ELIGIBILITY_LEMMA_20260810.md`](FULL_CAPTURE_SOURCE_SAFE_HUB_ELIGIBILITY_LEMMA_20260810.md)
  — splits the representative full-capture cell cap-free. A source-safe
  bottom pair forces a later-owner hub split or an immediate cover; the
  complementary strict-separated order is the input to the captured-bottom
  external-compensation chain.
- [`full_capture_source_safe_hub_eligibility_audit.json`](full_capture_source_safe_hub_eligibility_audit.json)
  — symbolic replay of the source-safe payment and failed-cover
  contradiction.
- [`dual_anchor_strict_separated_profile_audit.json`](dual_anchor_strict_separated_profile_audit.json)
  — exact-Fraction adversarial replay on the frozen strict-separated
  full-capture profile. Its dual root-paid selector is not EFX, but all four
  intended owners improve and its response relation has a release-supported
  internal matching, so the profile closes by generalized PI.
- [`dual_anchor_frozen_profile_census.json`](dual_anchor_frozen_profile_census.json)
  — repeats the dual selector on ten hardened full-capture profiles. All ten
  complement pools pay the earlier root and all ten selected allocations
  have release-supported internal response matchings; five profiles realize
  the strict-separated `q` order. This is bounded adversarial evidence, not
  the cap-free response theorem.
- [`SAME_SOURCE_TOP_SWITCH_MARGIN_DESCENT_LEMMA_20260811.md`](SAME_SOURCE_TOP_SWITCH_MARGIN_DESCENT_LEMMA_20260811.md)
  — gives the same-source top switch a genuine global potential. Every
  switch using a fresh root-top good strictly enlarges removed support and
  decreases the later mutual owner's positive response margin; failure
  captures that whole margin. Only reuse of already removed top support can
  recur.
- [`same_source_top_switch_margin_descent_audit.json`](same_source_top_switch_margin_descent_audit.json)
  — symbolic replay of the margin identity, strict fresh-support descent,
  and the capture alternative.
- [`REUSED_TOP_CANONICAL_CORE_SELECTOR_LEMMA_20260811.md`](REUSED_TOP_CANONICAL_CORE_SELECTOR_LEMMA_20260811.md)
  — canonicalizes every common-safe external core disjoint from the current
  mutual core, across both external sources, both bottom families, proper
  cores, and residual responses. The core minimizing root value maximizes
  the root's complement; a continuation must remove fresh mutual-core
  support, become unsafe, or change to a root-sourced response.
- [`reused_top_canonical_core_selector_audit.json`](reused_top_canonical_core_selector_audit.json)
  — symbolic replay of complement cancellation, root-pool maximality, and
  propagation of the canonical deficit.
- [`FLOWER_REMOVED_TOP_RETENTION_POTENTIAL_LEMMA_20260811.md`](FLOWER_REMOVED_TOP_RETENTION_POTENTIAL_LEMMA_20260811.md)
  — makes removed root-top support persistent across q-oriented and
  root-oriented resets. Every fresh removal strictly grows that support and
  lowers the later mutual owner's positive response margin; failure captures
  the whole original margin. Together with global external-core
  canonicalization, this rules out reset cycling while the reduced mutual
  core remains desired.
- [`flower_removed_top_retention_potential_audit.json`](flower_removed_top_retention_potential_audit.json)
  — symbolic replay of the persistent margin identity, strict fresh-packet
  descent, and terminal capture.
- [`CAPTURED_Q_MARGIN_ANCHORED_RESIDUAL_ROTATION_LEMMA_20260811.md`](CAPTURED_Q_MARGIN_ANCHORED_RESIDUAL_ROTATION_LEMMA_20260811.md)
  — converts terminal failure of the reduced q-core without resetting the
  support potential. Extend the retained packet only enough to replace
  `T_q`, rotate to `T_q+f` and `B_q+L`, and park the unused root goods. Both
  mutual owners improve and every failure is the existing evolved-target
  response/Hall boundary.
- [`captured_q_margin_anchored_residual_rotation_audit.json`](captured_q_margin_anchored_residual_rotation_audit.json)
  — symbolic replay of both-owner payment, charity containment, strict
  support growth, and relative minimality.
- [`ROOT_SOURCED_EVOLVED_TARGET_RETURN_OR_CAPTURE_LEMMA_20260811.md`](ROOT_SOURCED_EVOLVED_TARGET_RETURN_OR_CAPTURE_LEMMA_20260811.md)
  — converts a common-safe root response to the evolved `q` target into an
  anchor-return allocation. Either that return pays both mutual owners and
  leaves only one response wall, or the root core contains a nonempty
  `B_q` packet dominating the omitted retained packet plus `f` in `q`'s
  row.
- [`root_sourced_evolved_target_return_or_capture_audit.json`](root_sourced_evolved_target_return_or_capture_audit.json)
  — symbolic replay of the return-payment identity, strict capture
  cancellation, nonempty packet support, and charity containment.
- [`ROOT_RESPONSE_FLOATER_SUBSTITUTION_DICHOTOMY_LEMMA_20260811.md`](ROOT_RESPONSE_FLOATER_SUBSTITUTION_DICHOTOMY_LEMMA_20260811.md)
  — substitutes `f` into a captured root response while returning its
  `B_q` packet and `T_q` to the later owner. Success closes or leaves one
  evolved wall; failure makes the same nonempty `B_q` packet strictly
  margin-critical for both mutual owners.
- [`root_response_floater_substitution_dichotomy_audit.json`](root_response_floater_substitution_dichotomy_audit.json)
  — symbolic replay of support conservation, mutual-owner payment, and the
  two-row joint-capture certificate.
- [`CANONICAL_ROOT_RESPONSE_TWO_STAGE_SELECTOR_LEMMA_20260811.md`](CANONICAL_ROOT_RESPONSE_TWO_STAGE_SELECTOR_LEMMA_20260811.md)
  — globally selects over every common-safe root response at a fixed
  retained state: first maximize anchor-return payment, then maximize
  floater substitution. If neither operation succeeds, all root responses
  fail both tests and one canonical nonempty `B_q` packet is critical in
  both mutual-owner rows.
- [`canonical_root_response_two_stage_selector_audit.json`](canonical_root_response_two_stage_selector_audit.json)
  — symbolic replay of both extremal-propagation implications and the
  selected joint-capture inequalities.
- [`EVOLVED_TARGET_MINIMAL_SOURCE_TRICHOTOMY_LEMMA_20260811.md`](EVOLVED_TARGET_MINIMAL_SOURCE_TRICHOTOMY_LEMMA_20260811.md)
  — globally minimizes any unsafe desired subset of the evolved target to
  obtain a common-safe core. Its source is exhaustively `q` (immediate PI),
  external (return/Hall augmentation), or `r` (the canonical two-stage root
  selector), so an unnamed unsafe evolved-target branch no longer remains.
- [`evolved_target_minimal_source_trichotomy_audit.json`](evolved_target_minimal_source_trichotomy_audit.json)
  — symbolic replay of minimal-core safety and exhaustive source routing;
  physical release support is inherited from the prior two-root audit.
- [`JOINT_PACKET_MAXIMAL_LEX_DONATION_FRONTIER_LEMMA_20260811.md`](JOINT_PACKET_MAXIMAL_LEX_DONATION_FRONTIER_LEMMA_20260811.md)
  — turns the canonical joint `B_q` packet into a connected lexicographic
  transfer beginning `q -> r` and extending to charity when its maximal
  root donation is nonempty, while allowing the later donor to lose. The
  frontier leaves only donor, root-target, or charity blockers and makes
  every unused root good payment-critical.
- [`joint_packet_maximal_lex_donation_frontier_audit.json`](joint_packet_maximal_lex_donation_frontier_audit.json)
  — symbolic replay of root gain, maximal-donation criticality, and the
  external target/charity blocker polarities.
- [`JOINT_PACKET_BILATERAL_OR_LEX_DONATION_SELECTOR_LEMMA_20260811.md`](JOINT_PACKET_BILATERAL_OR_LEX_DONATION_SELECTOR_LEMMA_20260811.md)
  — first maximizes `q`-payment over every root-affordable packet. Either a
  bilateral swap pays both mutual owners, or every root-improving exchange
  has the same strict order in both rows, proving that the later-owner loss
  in the connected lex donation is structurally necessary.
- [`joint_packet_bilateral_or_lex_donation_selector_audit.json`](joint_packet_bilateral_or_lex_donation_selector_audit.json)
  — symbolic replay of bilateral payment and global maximum-failure
  propagation.
- [`JOINT_PACKET_EXTERNAL_SINK_REROUTING_LEMMA_20260811.md`](JOINT_PACKET_EXTERNAL_SINK_REROUTING_LEMMA_20260811.md)
  — reroutes a nonempty root-affordable packet to either external owner,
  producing the cap-free connected path `q -> r -> external` required by
  the hardened profiles. Every non-donor wall is localized to the root or
  sink target and enters sacrificed-owner response compression.
- [`joint_packet_external_sink_rerouting_audit.json`](joint_packet_external_sink_rerouting_audit.json)
  — symbolic replay of connected support, root/sink improvement, and both
  target-threshold polarities.
- [`JOINT_PACKET_CHARITY_COMPLETED_TRANSFER_PATH_LEMMA_20260811.md`](JOINT_PACKET_CHARITY_COMPLETED_TRANSFER_PATH_LEMMA_20260811.md)
  — assigns `f` to the losing later owner, sends the joint packet to the
  root, and optionally sends a root packet to an external sink. This always
  gives a complete connected path `charity -> q -> r (-> external)` and
  reduces failure to a release-supported sacrificed-owner Hall boundary.
- [`joint_packet_charity_completed_transfer_path_audit.json`](joint_packet_charity_completed_transfer_path_audit.json)
  — symbolic replay of complete support, root payment, the exact donor loss,
  and all changed-target polarities.
- [`CHARITY_COMPLETED_PATH_ROOT_RESPONSE_ANCHOR_LEMMA_20260811.md`](CHARITY_COMPLETED_PATH_ROOT_RESPONSE_ANCHOR_LEMMA_20260811.md)
  — observes that the completed `q` target still contains the original
  common-safe root core `T_q+f`, whose response edge releases all of `B_q`
  and supplies the joint packet consumed by the root target. A `q` source
  closes PI, an external source grows a root-anchored matching, and the only
  survivor is an explicit two-target root-monopoly defect.
- [`charity_completed_path_root_response_anchor_audit.json`](charity_completed_path_root_response_anchor_audit.json)
  — exact support and source-label replay for the permanent root edge.
- [`GG_RETAINED_SUPPORT_CONNECTED_PATH_COMPOSITION_CHECKPOINT_20260811.md`](GG_RETAINED_SUPPORT_CONNECTED_PATH_COMPOSITION_CHECKPOINT_20260811.md)
  — composes retained-support capture, exhaustive evolved-target source
  routing, the canonical root selector, joint-packet bilateral exhaustion,
  and the complete connected path. Subsequent handoffs eliminate the root-
  monopoly pair and preserve or capture every top/floater reset. The sole
  remaining terminal is the fixed-`U`, root-anchored sacrificed-`q` Hall
  recurrence; its rank-lowering resets still need one global potential or
  connected-component extraction.
- [`gg_retained_support_connected_path_composition_audit.json`](gg_retained_support_connected_path_composition_audit.json)
  — integrity/replay manifest for twenty-two cap-free dependencies and the
  focused 51-test dependency suite; it is not a proof of the corrected global reset
  potential.
- [`GG_RANK_RESET_RAW_POTENTIAL_REFUTATION_20260811.md`](GG_RANK_RESET_RAW_POTENTIAL_REFUTATION_20260811.md)
  ([exact audit](gg_rank_reset_raw_potential_refutation_audit.json))
  — exactly refutes the raw `missing-owner residual value` coordinate across
  hole changes. A positive subset-sum-injective additive witness preserves
  retained support, maximum response rank, owner-union size, and the entire
  response relation while a row rescaling reverses the residual comparison.
  The corrected target uses an owner-indexed normalized residual ledger and
  historical rank/supplier support; GG closure remains open.
- [`gg_rank_reset_raw_potential_globality_gap_audit.json`](gg_rank_reset_raw_potential_globality_gap_audit.json)
  — complete exact `5^9` allocation census of the raw-coordinate witness.
  Its base is not globally lex maximal under any of the 24 priority orders,
  so the witness refutes the coordinate but cannot serve as a counterexample
  to the full GG bridge.
- [`GG_HISTORICAL_SUPPORT_LEDGER_STAGNATION_REFUTATION_20260811.md`](GG_HISTORICAL_SUPPORT_LEDGER_STAGNATION_REFUTATION_20260811.md)
  ([exact audit](gg_historical_support_ledger_stagnation_audit.json))
  — shows that the corrected historical ledger is nondecreasing but not a
  strict termination potential. Four distinct non-EFX rank-three
  compressions share the same saturated rank, owner union, normalized
  per-hole residual maxima, and used-support history. This does not prove a
  particular deterministic repair rule cycles; it forces either a new
  current-state invariant or direct component extraction.
- [`PERMANENT_ANCHOR_Q_ACTIVITY_DICHOTOMY_LEMMA_20260811.md`](PERMANENT_ANCHOR_Q_ACTIVITY_DICHOTOMY_LEMMA_20260811.md)
  ([exact audit](permanent_anchor_q_activity_dichotomy_audit.json))
  — removes the response-active sacrificed-`q` recurrence without assuming
  that the permanent anchor preserves unrestricted maximum rank. Among all
  anchor-constrained maximum matchings, an active `q` can always be
  represented by one edge replacement; hence a sacrificed `q` has degree
  zero against every active target. All `2^14` four-by-four response graphs
  replay exactly. The remaining gate is the genuinely source-inactive
  degree-zero repair.
- [`FIXED_U_Q_RESIDUAL_GLOBAL_MAX_SELECTOR_LEMMA_20260811.md`](FIXED_U_Q_RESIDUAL_GLOBAL_MAX_SELECTOR_LEMMA_20260811.md)
  ([composition audit](fixed_u_q_residual_global_max_selector_audit.json))
  — globally maximizes the degree-zero hole's residual in `q`'s own row over
  every fixed-`U`, root-anchored response rank. A successful source-inactive
  repair or nonroot J-exhaustion strictly raises that same quantity, so it
  must instead activate `q`, augment through an unsafe core, close by EFX/PI,
  or contradict the selector. Only the root-facing and unsafe/hitting-set
  handoffs remain.
- [`PROTECTED_Q_RESPONSE_RETENTION_LEMMA_20260811.md`](PROTECTED_Q_RESPONSE_RETENTION_LEMMA_20260811.md)
  ([exact audit](protected_q_response_retention_audit.json))
  — shows that once the permanent-anchor selector represents `q`, the
  selected `q` core is floater-free. A later top-only orientation reset must
  preserve `q` coverage, strictly enlarge retained support, or capture the
  remaining `q` margin; it cannot silently sacrifice `q` again at the same
  retained state.
- [`DEGREE_ZERO_Q_SPLIT_CORE_ROOT_FLIP_LEMMA_20260811.md`](DEGREE_ZERO_Q_SPLIT_CORE_ROOT_FLIP_LEMMA_20260811.md)
  ([composition audit](degree_zero_q_split_core_root_flip_audit.json))
  — removes degree-zero `q` as an untyped one-target Hall terminal. The known
  desired mutual core remains a split-support response across the connected
  path; reassembling it yields protected `q` coverage, retained-support
  growth, captured-margin rotation, or a named source-margin packet. The
  latter packet and unsafe/root-critical handoffs remain open.
- [`ANCHOR_CONSTRAINED_Q_PRIORITY_MATCHING_LEMMA_20260811.md`](ANCHOR_CONSTRAINED_Q_PRIORITY_MATCHING_LEMMA_20260811.md)
  ([exact graph audit](anchor_constrained_q_priority_matching_audit.json))
  — supplies that current-state invariant at the response-graph level. Force
  the permanent root anchor, maximize rank, and then prioritize `q`. Across
  all `2^14` four-owner response relations, either the anchor costs rank,
  `q` is represented, or unmatched `q` has degree zero. It collapses the
  exact four-state ledger plateau to one matching label; physical-core
  recurrence and anchor-gap release remain open.
- [`SURPLUS_BUDGETED_CONNECTED_COMPONENT_TRANSFER_LEMMA_20260811.md`](SURPLUS_BUDGETED_CONNECTED_COMPONENT_TRANSFER_LEMMA_20260811.md)
  ([exact audit](surplus_budgeted_connected_component_transfer_audit.json))
  — lifts the externally-safe path endpoint to arbitrary connected packet
  graphs and lets each observer's realized gain pay for changed-target
  threshold overshoot. The exact four-owner branching repair
  `charity->r, r->{q,c}, c->s` has five positive threshold overshoots but all
  are covered by the corresponding owner surplus. Packet extraction from
  every terminal Hall polarity remains open.
- [`SOURCE_INACTIVE_CORE_RESIDUAL_REPAIR_LEMMA_20260811.md`](SOURCE_INACTIVE_CORE_RESIDUAL_REPAIR_LEMMA_20260811.md)
  — cap-free alternating packet repair for a sacrificed-owner wall that is
  not a base response. Core-to-residual and residual-to-core packets grow
  monotonically; every successful common-safe repair strictly increases the
  missing owner's residual potential. The only exhaustion is an exact
  two-row orientation in which one critical core packet dominates the
  entire residual by the core source's improvement margin.
- [`source_inactive_core_residual_repair_audit.json`](source_inactive_core_residual_repair_audit.json)
  — dual-version support and scalar replay of repair existence, residual
  advance, old-wall preservation, and the exhaustion margin.
- [`TWO_HOLE_CUT_AND_CHOOSE_RESPONSE_HALL_LEMMA_20260811.md`](TWO_HOLE_CUT_AND_CHOOSE_RESPONSE_HALL_LEMMA_20260811.md)
  — converts every non-root J-exhaustion into a cap-free two-hole component.
  A maximin divider and chooser make the two residual cells mutually EFX;
  because the old hole strongly envied the exhausted core, both cells are
  strictly more valuable to that hole than its previous residual. The only
  remainder is a localized two-core/two-residual response-Hall boundary.
- [`two_hole_cut_and_choose_response_hall_audit.json`](two_hole_cut_and_choose_response_hall_audit.json)
  — dual-version scalar and exhaustive 2-by-2 response replay, including the
  strict inherited maximin-potential gain.
- [`NONROOT_UNCONDITIONAL_RECAPTURE_LEMMA_20260811.md`](NONROOT_UNCONDITIONAL_RECAPTURE_LEMMA_20260811.md)
  — observes that a rank-three flower recapture need not preserve the
  missing owner's base payment. Root anchoring excludes `r` as the hole, so
  an unpaid recapture remains priority-valid and enters the sacrificed-owner
  star machinery. This removes the strict unpayable-recapture polarity as a
  separate terminal case.
- [`nonroot_unconditional_recapture_audit.json`](nonroot_unconditional_recapture_audit.json)
  — dual-version replay of recapture support, the exact payment identity,
  priority validity, and paid/unpaid wall localization.
- [`ROOT_FACING_EXHAUSTION_HANDOFF_LEMMA_20260811.md`](ROOT_FACING_EXHAUSTION_HANDOFF_LEMMA_20260811.md)
  — splits the priority-invalid root-facing exhaustion. Any critical packet
  containing a top good enters the existing top-core exchange/reset. The
  only new survivor has critical packet `{f}`; it forces the charity and
  the root's entire bottom packet above the residual, hence exposes a
  nonempty root-bottom packet captured in a nonroot desired core.
- [`root_facing_exhaustion_handoff_audit.json`](root_facing_exhaustion_handoff_audit.json)
  — dual-version replay of the top/root factorization, f-only cancellation,
  strict bottom polarity, and captured-bottom support.
- [`ROOT_PRESERVING_TWO_HOLE_SELECTOR_LEMMA_20260811.md`](ROOT_PRESERVING_TWO_HOLE_SELECTOR_LEMMA_20260811.md)
  — removes the root-facing priority exception without an item cap. A
  root-constrained partition either makes the two holes mutually EFX or
  identifies one least good with an exact root-critical deficit polarity.
- [`root_preserving_two_hole_selector_audit.json`](root_preserving_two_hole_selector_audit.json)
  — dual-version replay of root envy-freeness, selector criticality, and the
  exact residual-deficit identity.
- [`ROOT_CRITICAL_COMPENSATOR_DICHOTOMY_LEMMA_20260811.md`](ROOT_CRITICAL_COMPENSATOR_DICHOTOMY_LEMMA_20260811.md)
  — splits a failed root-preserving selector cap-free. Any residual packet
  that can compensate the root for its critical good is forced by selector
  maximality to have a strict opposite-row value order. If no such packet
  exists, the critical good lies in the original flower root core and routes
  to either the top-core exchange/reset or captured-bottom handoff.
- [`root_critical_compensator_dichotomy_audit.json`](root_critical_compensator_dichotomy_audit.json)
  — dual-version replay of the compensator exchange, forced packet order,
  residual-domination inequality, and old-core support conclusion.
- [`ROOT_CRITICAL_ALTERNATING_FRONTIER_LEMMA_20260811.md`](ROOT_CRITICAL_ALTERNATING_FRONTIER_LEMMA_20260811.md)
  — terminates the strict root-compensator dependency cap-free. Alternating
  minimal packets grow on both sides until a root-side packet exceeds the
  entire old residual; its old-core portion then dominates the exact
  residual complement and routes to a top exchange/reset or an enlarged
  captured-bottom handoff.
- [`root_critical_alternating_frontier_audit.json`](root_critical_alternating_frontier_audit.json)
  — dual-version replay of alternating packet growth, forced termination,
  and the terminal support cancellation.
- [`TWO_BY_TWO_RESPONSE_HALL_NORMAL_FORM_20260811.md`](TWO_BY_TWO_RESPONSE_HALL_NORMAL_FORM_20260811.md)
  — classifies both residual 2-by-2 response blocks cap-free. If neither
  block has an empty target, then either both match or their cross-block
  edges contain a release-compatible two-owner PI cycle. Consequently the
  only PI-free survivor is an empty-target/source-inactive wall followed by
  a lower-dimensional pivot or repair recurrence.
- [`two_by_two_response_hall_normal_form_audit.json`](two_by_two_response_hall_normal_form_audit.json)
  — exhaustive replay of all 16 labeled 2-by-2 relations and all 256 paired
  blocks; every pair is classified as a full SDR, cross-block two-cycle, or
  empty-target survivor.
- [`MINIMAL_HALL_OWNER_UNION_COMPRESSION_LEMMA_20260811.md`](MINIMAL_HALL_OWNER_UNION_COMPRESSION_LEMMA_20260811.md)
  — generalizes deficiency-one response compression from the all-owner case
  to every inclusion-minimal two-, three-, or four-target Hall defect. All
  50,625 nonempty four-by-four relations, 64,272 response edges, and every
  minimal defect replay exactly. A two-target/one-outside-source defect
  reduces cap-free to one two-way residual-pool partition.
- [`owner_union_compression_hardened_profile_audit.json`](owner_union_compression_hardened_profile_audit.json)
  — solver-independent replay of a positive subset-sum-injective flower
  profile whose local residual partitions end in `{q,s}->{c}`. Giving `c`
  its desired singleton core `{z}` and repartitioning the `q,s,c` owner union
  yields a complete EFX lex improvement. This closes the adversary, not the
  universal two-way partition gate.
