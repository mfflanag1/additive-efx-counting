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
  — source-valid reconstruction of the BCFF two-large length-three residual.
  It proves the singleton-absorption and easy-priority lemmas cap-free,
  proves all-source primal and rotated reservoir lemmas, closes every
  `r`-first order, and proves two three-promotion/payment reductions. The
  external singleton-source wall is closed; the remaining gate is the
  `q`-source handoff when `r` has earlier priority, together with a two-wall
  mixed-pool uncrossing. No two-large or general EFX closure is yet claimed.
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
  observer wall. Only the two `r`-before-`p,q` dual-base rows remain for
  this source type.
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
  for `x`. This is a reduction, not yet the full external-`q` theorem.
- [`LENGTH_THREE_PARALLEL_ROOT_PIVOT_REDUCTION.md`](LENGTH_THREE_PARALLEL_ROOT_PIVOT_REDUCTION.md)
  — cap-free safety closure of the remaining parallel-root recurrence. Returning
  the charity-swap pivot to a newly exposed `p`-root strictly improves the
  `p` coordinate; every augmentation failure containing the pivot is either
  an ordinary PI cycle or a champion handoff. Only a compatible residual
  payment remains.
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
