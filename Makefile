PYTHON ?= python3
VERIFY_TMP ?= /tmp/additive-efx-counting-verify
ROW_MERGE_TOPOLOGY_TRACES := results/row_merge_q4_small_step_chain3_m9_cegar.json results/row_merge_q4_small_step_chain3_m9_graph1212_cap20_cegar.json results/row_merge_q4_small_step_chain3_m9_graph1212_cap20_ladder4.json results/row_merge_q4_small_step_chain3_m9_graph1212_cap20_pool60.json results/row_merge_q4_small_step_chain3_m9_graph1212_cap20_pool64.json results/row_merge_q4_cycle023_plus_base_cap20_gate.json results/row_merge_q4_cycle023_both_plus_base_cap20_gate.json results/row_merge_q4_path32_plus_base_cap20_gate.json results/row_merge_q4_path32_all_lengths_plus_base_cap20_gate.json results/row_merge_q4_all_three_cycles_plus_base_cap20_gate.json results/row_merge_q4_all_paths_start3_plus_base_cap20_gate.json results/row_merge_q4_min_topology_cover_plus_base_cap20_gate.json results/row_merge_q4_min_topology_cover_round2_plus_base_cap20_gate.json

.PHONY: install verify verify-paper verify-audit verify-parkability verify-single-wall verify-row-merge-q4-radius-boundary verify-row-merge-exchange-chain-gate verify-row-merge-topology-mining-gate verify-row-merge-ranked-path-gate verify-row-merge-adaptive-hall-path-gate verify-adaptive-first-agent-core verify-safe-floater-exchange verify-bundle-cycle-source verify-floater-substitution-cycle verify-partial-nash-substitution-census verify-partial-nash-local-trichotomy-refutation verify-partial-pareto-completion-refutation verify-partial-nash-completion-refutation verify-partial-nash-one-transfer-refutation verify-partial-nash-source-completion-refutation verify-partial-hall-radius-one verify-partial-hall-pair-extraction verify-rank1-core-shape-ladder verify-efx48-release paper

install:
	$(PYTHON) -m pip install -r requirements.txt

verify: verify-paper verify-audit

verify-efx48-release:
	test -n "$(EFX48_CERT_ROOT)"
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_cpc_formula_assumptions.py $(EFX48_CERT_ROOT) --output $(VERIFY_TMP)/efx48-cpc-formula-assumptions.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/replay_efx48_relocatable_cpc.py --root $(EFX48_CERT_ROOT) --output $(VERIFY_TMP)/efx48-relocatable-cpc-replay.json

verify-paper:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) repro/counting_witnesses/verify_all.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) artifacts/generalized_parking/verify_certificates.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) repro/countcegar_k4/test_sat_differential.py --result-out $(VERIFY_TMP)/sat-differential.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) repro/countcegar_k4/test_slot_boundary.py --result-out $(VERIFY_TMP)/slot-boundary.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) repro/countcegar_k4/verify_drat.py --hash-only

verify-audit:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) repro/countcegar_real/test_countcegar_real.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) repro/countcegar_real/validate_manifest.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) artifacts/efx_chambers/verify_radii.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) artifacts/efx_chambers/verify_radii_exact.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) artifacts/multifloater_parking/verify_small.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) supplement/test_build_release.py
	$(MAKE) verify-parkability

verify-row-merge-q4-radius-boundary:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_row_merge_q4_small_step_radius_boundary.py --seed results/row_merge_q4_small_step_radius2_m9_cegar_seed16.json --normalization results/row_merge_q4_small_step_radius2_m9_cegar_seed16.cvc5.normalization.json --cvc5 results/row_merge_q4_small_step_radius2_m9_cegar_seed16.cvc5.json --terminal results/row_merge_q4_small_step_radius2_m9_cegar_terminal37.json --output $(VERIFY_TMP)/row-merge-q4-small-step-radius2-m9-boundary-audit.json
	cmp results/row_merge_q4_small_step_radius2_m9_boundary_audit.json $(VERIFY_TMP)/row-merge-q4-small-step-radius2-m9-boundary-audit.json

verify-row-merge-exchange-chain-gate:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/analyze_row_merge_q4_distance3_exchange.py --source results/row_merge_q4_small_step_radius2_m9_cegar_terminal37.json --output $(VERIFY_TMP)/row-merge-q4-distance3-exchange-m9-analysis.json
	cmp results/row_merge_q4_distance3_exchange_m9_analysis.json $(VERIFY_TMP)/row-merge-q4-distance3-exchange-m9-analysis.json
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_row_merge_q4_exchange_chain_gate.py --analysis results/row_merge_q4_distance3_exchange_m9_analysis.json --cegar results/row_merge_q4_small_step_chain3_m9_cegar.json --normalization results/row_merge_q4_small_step_chain3_m9_cegar.cvc5.normalization.json --cvc5 results/row_merge_q4_small_step_chain3_m9_cegar.cvc5.json --fixed56 results/row_merge_q4_small_step_chain3_m9_graph1212_cegar.json --ladder8 results/row_merge_q4_small_step_chain3_m9_graph1212_ladder8.json --ladder4 results/row_merge_q4_small_step_chain3_m9_graph1212_ladder4.json --hall56 results/row_merge_q4_small_step_chain3_m9_graph1212_hall56.json --output $(VERIFY_TMP)/row-merge-q4-exchange-chain-gate-audit.json
	cmp results/row_merge_q4_exchange_chain_gate_audit.json $(VERIFY_TMP)/row-merge-q4-exchange-chain-gate-audit.json

verify-row-merge-topology-mining-gate:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/analyze_row_merge_q4_chain_trace.py $(foreach trace,$(ROW_MERGE_TOPOLOGY_TRACES),--trace $(trace)) --output $(VERIFY_TMP)/row-merge-q4-chain-topology-mining-final-analysis.json
	cmp results/row_merge_q4_chain_topology_mining_final_analysis.json $(VERIFY_TMP)/row-merge-q4-chain-topology-mining-final-analysis.json
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_row_merge_q4_topology_mining_gate.py --analysis results/row_merge_q4_chain_topology_mining_final_analysis.json --gate results/row_merge_q4_all_three_cycles_plus_base_cap20_gate.json --gate results/row_merge_q4_all_paths_start3_plus_base_cap20_gate.json --gate results/row_merge_q4_min_topology_cover_plus_base_cap20_gate.json --gate results/row_merge_q4_min_topology_cover_round2_plus_base_cap20_gate.json --output $(VERIFY_TMP)/row-merge-q4-topology-mining-gate-audit.json
	cmp results/row_merge_q4_topology_mining_gate_audit.json $(VERIFY_TMP)/row-merge-q4-topology-mining-gate-audit.json

verify-row-merge-ranked-path-gate:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/mine_row_merge_q4_valuation_selector.py --analysis results/row_merge_q4_chain_topology_mining_final_analysis.json --output $(VERIFY_TMP)/row-merge-q4-valuation-selector-mining-v2.json
	cmp results/row_merge_q4_valuation_selector_mining_v2.json $(VERIFY_TMP)/row-merge-q4-valuation-selector-mining-v2.json
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_row_merge_q4_ranked_path_gate.py --mining results/row_merge_q4_valuation_selector_mining_v2.json --refutation results/row_merge_q4_ranked_path_0003_generic_cap20_cegar.json --boundary results/row_merge_q4_ranked_path_trace_union_generic_cap20_cegar.json --output $(VERIFY_TMP)/row-merge-q4-ranked-path-gate-audit.json
	cmp results/row_merge_q4_ranked_path_gate_audit.json $(VERIFY_TMP)/row-merge-q4-ranked-path-gate-audit.json

verify-row-merge-adaptive-hall-path-gate:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/analyze_row_merge_q4_adaptive_hall_paths.py --analysis results/row_merge_q4_chain_topology_mining_final_analysis.json --ranked results/row_merge_q4_ranked_path_0003_generic_cap20_cegar.json --ranked results/row_merge_q4_ranked_path_trace_union_generic_cap20_cegar.json --output $(VERIFY_TMP)/row-merge-q4-adaptive-hall-path-analysis.json
	cmp results/row_merge_q4_adaptive_hall_path_analysis.json $(VERIFY_TMP)/row-merge-q4-adaptive-hall-path-analysis.json

verify-single-wall: verify-row-merge-q4-radius-boundary verify-row-merge-exchange-chain-gate verify-row-merge-topology-mining-gate verify-row-merge-ranked-path-gate verify-row-merge-adaptive-hall-path-gate
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_row_merge_single_wall_radius.py --source results/row_merge_single_wall_q2_radius2_refutation.json --source results/row_merge_single_wall_q3_radius2_refutation.json --source results/row_merge_single_wall_q4_radius1_refutation.json --unsat-source results/row_merge_single_wall_q4_radius2_m7_unsat.json --normalization results/row_merge_single_wall_q4_radius2_m7_unsat.cvc5.normalization.json --cvc5 results/row_merge_single_wall_q4_radius2_m7_unsat.cvc5.json --core results/row_merge_single_wall_q4_radius2_m7_core.json --core-normalization results/row_merge_single_wall_q4_radius2_m7_core.cvc5.normalization.json --core-cvc5 results/row_merge_single_wall_q4_radius2_m7_core.cvc5.json --genericity-core results/row_merge_single_wall_q4_radius2_m7_genericity_core.json --genericity-normalization results/row_merge_single_wall_q4_radius2_m7_genericity_core.cvc5.normalization.json --genericity-cvc5 results/row_merge_single_wall_q4_radius2_m7_genericity_core.cvc5.json --pair-pivot results/row_merge_q4_small_step_pair_m8.json --pair-pivot-normalization results/row_merge_q4_small_step_pair_m8.cvc5.normalization.json --pair-pivot-cvc5 results/row_merge_q4_small_step_pair_m8.cvc5.json --output $(VERIFY_TMP)/row-merge-single-wall-radius-refutations.json
	cmp results/row_merge_single_wall_radius_refutation_audit.json $(VERIFY_TMP)/row-merge-single-wall-radius-refutations.json

verify-adaptive-first-agent-core:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_adaptive_priority_first_agent_core.py --seed results/lexmax_all_orders_anneal_4x9_seed93.json --core results/adaptive_priority_first01_compact_core.json --raw-formula results/adaptive_priority_first01_compact_core.smt2 --normalized-formula results/adaptive_priority_first01_compact_core.cvc5.smt2 --normalization results/adaptive_priority_first01_compact_core.cvc5.normalization.json --cvc5 results/adaptive_priority_first01_compact_core.cvc5.json --inequality-core results/adaptive_priority_first01_inequality_core.json --inequality-raw-formula results/adaptive_priority_first01_inequality_core.smt2 --inequality-normalized-formula results/adaptive_priority_first01_inequality_core.cvc5.smt2 --inequality-normalization results/adaptive_priority_first01_inequality_core.cvc5.normalization.json --inequality-cvc5 results/adaptive_priority_first01_inequality_core.cvc5.json --output $(VERIFY_TMP)/adaptive-priority-first01-core-audit.json --time-limit 60
	cmp results/adaptive_priority_first01_compact_core_audit.json $(VERIFY_TMP)/adaptive-priority-first01-core-audit.json

verify-safe-floater-exchange:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_safe_floater_exchange_lemma.py --output $(VERIFY_TMP)/safe_floater_exchange_lemma_audit.json --weak-smt2 $(VERIFY_TMP)/safe_floater_exchange_lemma_weak.smt2 --strict-smt2 $(VERIFY_TMP)/safe_floater_exchange_lemma_strict.smt2
	cmp results/safe_floater_exchange_lemma_audit.json $(VERIFY_TMP)/safe_floater_exchange_lemma_audit.json
	cmp results/safe_floater_exchange_lemma_weak.smt2 $(VERIFY_TMP)/safe_floater_exchange_lemma_weak.smt2
	cmp results/safe_floater_exchange_lemma_strict.smt2 $(VERIFY_TMP)/safe_floater_exchange_lemma_strict.smt2

verify-bundle-cycle-source:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_bundle_cycle_source_lemma.py --output $(VERIFY_TMP)/bundle_cycle_source_lemma_audit.json --weak-smt2 $(VERIFY_TMP)/bundle_cycle_weak.smt2 --nash-smt2 $(VERIFY_TMP)/bundle_cycle_nash.smt2 --source-smt2 $(VERIFY_TMP)/bundle_cycle_source.smt2
	cmp results/bundle_cycle_source_lemma_audit.json $(VERIFY_TMP)/bundle_cycle_source_lemma_audit.json
	cmp results/bundle_cycle_weak.smt2 $(VERIFY_TMP)/bundle_cycle_weak.smt2
	cmp results/bundle_cycle_nash.smt2 $(VERIFY_TMP)/bundle_cycle_nash.smt2
	cmp results/bundle_cycle_source.smt2 $(VERIFY_TMP)/bundle_cycle_source.smt2

verify-floater-substitution-cycle:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_floater_substitution_cycle_lemma.py --output $(VERIFY_TMP)/floater_substitution_cycle_lemma_audit.json --weak-smt2 $(VERIFY_TMP)/floater_substitution_cycle_weak.smt2 --nash-smt2 $(VERIFY_TMP)/floater_substitution_cycle_nash.smt2
	cmp results/floater_substitution_cycle_lemma_audit.json $(VERIFY_TMP)/floater_substitution_cycle_lemma_audit.json
	cmp results/floater_substitution_cycle_weak.smt2 $(VERIFY_TMP)/floater_substitution_cycle_weak.smt2
	cmp results/floater_substitution_cycle_nash.smt2 $(VERIFY_TMP)/floater_substitution_cycle_nash.smt2

verify-partial-nash-substitution-census:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_partial_nash_substitution_census.py --output $(VERIFY_TMP)/partial_nash_substitution_census.json
	cmp results/partial_nash_substitution_census.json $(VERIFY_TMP)/partial_nash_substitution_census.json

verify-partial-nash-local-trichotomy-refutation:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_partial_nash_local_trichotomy_refutation.py --output $(VERIFY_TMP)/partial_nash_local_trichotomy_refutation_audit.json
	cmp results/partial_nash_local_trichotomy_refutation_audit.json $(VERIFY_TMP)/partial_nash_local_trichotomy_refutation_audit.json

verify-partial-pareto-completion-refutation:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_partial_pareto_completion_refutation.py --output $(VERIFY_TMP)/partial_pareto_completion_refutation_audit.json
	cmp results/partial_pareto_completion_refutation_audit.json $(VERIFY_TMP)/partial_pareto_completion_refutation_audit.json

verify-partial-nash-completion-refutation:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_partial_nash_completion_refutation.py --output $(VERIFY_TMP)/partial_nash_completion_refutation_audit.json
	cmp results/partial_nash_completion_refutation_audit.json $(VERIFY_TMP)/partial_nash_completion_refutation_audit.json

verify-partial-nash-one-transfer-refutation:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_partial_nash_one_transfer_refutation.py --output $(VERIFY_TMP)/partial_nash_one_transfer_refutation_audit.json
	cmp results/partial_nash_one_transfer_refutation_audit.json $(VERIFY_TMP)/partial_nash_one_transfer_refutation_audit.json

verify-partial-nash-source-completion-refutation:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_partial_nash_source_completion_refutation.py --output $(VERIFY_TMP)/partial_nash_source_completion_refutation_audit.json
	cmp results/partial_nash_source_completion_refutation_audit.json $(VERIFY_TMP)/partial_nash_source_completion_refutation_audit.json

verify-partial-hall-pair-extraction:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/search_partial_hall_pair_extraction.py results/partial_hall_two_positive_reroute_corpus_search.json --output $(VERIFY_TMP)/partial_hall_pair_extraction_corpus134.json
	cmp results/partial_hall_pair_extraction_corpus134.json $(VERIFY_TMP)/partial_hall_pair_extraction_corpus134.json
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_partial_hall_direct_pair_counterexample.py --source results/partial_hall_direct_pair_extraction_counterexample.json --output $(VERIFY_TMP)/partial_hall_direct_pair_extraction_counterexample_audit.json
	cmp results/partial_hall_direct_pair_extraction_counterexample_audit.json $(VERIFY_TMP)/partial_hall_direct_pair_extraction_counterexample_audit.json
	test "$$(z3 results/partial_hall_direct_pair_extraction_aggregate.smt2)" = "sat"
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_partial_hall_host_minimum_counterexample.py --source results/partial_hall_host_minimum_extraction_counterexample.json --output $(VERIFY_TMP)/partial_hall_host_minimum_extraction_counterexample_audit.json
	cmp results/partial_hall_host_minimum_extraction_counterexample_audit.json $(VERIFY_TMP)/partial_hall_host_minimum_extraction_counterexample_audit.json
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_partial_hall_owner_minimum_extraction_theorem.py --directory results --output $(VERIFY_TMP)/partial_hall_owner_minimum_extraction_theorem_audit.json
	cmp results/partial_hall_owner_minimum_extraction_theorem_audit.json $(VERIFY_TMP)/partial_hall_owner_minimum_extraction_theorem_audit.json
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_partial_hall_owner_minimum_substitution_counterexample.py --source results/partial_hall_owner_minimum_substitution_counterexample.json --output $(VERIFY_TMP)/partial_hall_owner_minimum_substitution_counterexample_audit.json
	cmp results/partial_hall_owner_minimum_substitution_counterexample_audit.json $(VERIFY_TMP)/partial_hall_owner_minimum_substitution_counterexample_audit.json
	test "$$(z3 results/partial_hall_owner_minimum_ties_extraction_aggregate.smt2)" = "unsat"
	test "$$(z3 results/partial_hall_owner_minimum_ties_singletons_01.smt2)" = "unsat"
	test "$$(z3 results/partial_hall_owner_minimum_ties_singletons_03.smt2)" = "unsat"
	test "$$(z3 results/partial_hall_owner_minimum_ties_singletons_07.smt2)" = "unsat"
	test "$$(z3 results/partial_hall_owner_minimum_ties_singletons_15.smt2)" = "unsat"

verify-partial-hall-radius-one:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_partial_hall_radius_one_model.py --source results/partial_hall_pareto_cegar_session1.json --output $(VERIFY_TMP)/partial_hall_pareto_cegar_model_audit.json
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_partial_hall_completion.py results/partial_hall_pareto_cegar_session1.json --output $(VERIFY_TMP)/partial_hall_pareto_cegar_completion_audit.json
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_partial_hall_radius_one_model.py --source results/partial_hall_utilitarian_local_cegar_session1.json --output $(VERIFY_TMP)/partial_hall_utilitarian_local_cegar_session1_audit.json
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_partial_hall_radius_one_model.py --source results/partial_hall_utilitarian_local_r3_cegar_session1.json --output $(VERIFY_TMP)/partial_hall_utilitarian_local_r3_cegar_session1_audit.json
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_partial_hall_radius_one_model.py --source results/partial_hall_utilitarian_local_r4_cegar_session1.json --output $(VERIFY_TMP)/partial_hall_utilitarian_local_r4_cegar_session1_audit.json
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_partial_hall_rival_factoring.py --checkpoint results/partial_hall_utilitarian_local_r5_cegar_session4_seed211.json --output $(VERIFY_TMP)/partial_hall_utilitarian_local_r5_double_factored_audit.json --timeout-seconds 300
	test "$$(z3 results/partial_hall_witness_encoding_audit.smt2)" = "unsat"
	test "$$(z3 results/partial_hall_nonempty_neighbor_audit.smt2)" = "unsat"
	test "$$(z3 results/partial_hall_pair_deficiency_compact_core.smt2)" = "unsat"
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/run_smt2_cvc5.py --source results/partial_hall_pair_deficiency_compact_core.cvc5.smt2 --output $(VERIFY_TMP)/partial_hall_pair_deficiency_compact_core_cvc5.json --timeout-seconds 60
	test "$$(jq -r .status $(VERIFY_TMP)/partial_hall_pair_deficiency_compact_core_cvc5.json)" = "UNSAT"
	test "$$(z3 results/partial_hall_designated_pair_trap.smt2)" = "unsat"
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/run_smt2_cvc5.py --source results/partial_hall_designated_pair_trap.cvc5.smt2 --output $(VERIFY_TMP)/partial_hall_designated_pair_trap_cvc5.json --timeout-seconds 60
	test "$$(jq -r .status $(VERIFY_TMP)/partial_hall_designated_pair_trap_cvc5.json)" = "UNSAT"
	test "$$(z3 results/partial_hall_utilitarian_frozen_cell_seed17_cont117_core.smt2)" = "unsat"
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/run_smt2_cvc5.py --source results/partial_hall_utilitarian_frozen_cell_seed17_cont117_core.cvc5.smt2 --output $(VERIFY_TMP)/partial_hall_utilitarian_frozen_cell_cvc5.json --timeout-seconds 60
	test "$$(jq -r .status $(VERIFY_TMP)/partial_hall_utilitarian_frozen_cell_cvc5.json)" = "UNSAT"
	test "$$(z3 results/partial_hall_completion_improvement_lemma_seed17.smt2)" = "unsat"
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/run_smt2_cvc5.py --source results/partial_hall_completion_improvement_lemma_seed17.cvc5.smt2 --output $(VERIFY_TMP)/partial_hall_completion_improvement_lemma_cvc5.json --timeout-seconds 60
	test "$$(jq -r .status $(VERIFY_TMP)/partial_hall_completion_improvement_lemma_cvc5.json)" = "UNSAT"
	test "$$(z3 results/partial_hall_two_wall_algebra.smt2)" = "unsat"
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/run_smt2_cvc5.py --source results/partial_hall_two_wall_algebra.smt2 --output $(VERIFY_TMP)/partial_hall_two_wall_algebra_cvc5.json --timeout-seconds 60
	test "$$(jq -r .status $(VERIFY_TMP)/partial_hall_two_wall_algebra_cvc5.json)" = "UNSAT"
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_partial_hall_two_wall_gates.py --source results/partial_hall_utilitarian_maximality_anneal_seed17_cont117.json --source results/partial_hall_utilitarian_maximality_anneal_seed23.json --source results/partial_hall_pareto_cegar_session1.json --source results/partial_hall_utilitarian_local_cegar_session1.json --source results/partial_hall_utilitarian_local_r3_cegar_session1.json --source results/partial_hall_utilitarian_local_r4_cegar_session1.json --output $(VERIFY_TMP)/partial_hall_two_wall_gate_corpus_audit.json
	cmp results/partial_hall_two_wall_gate_corpus_audit.json $(VERIFY_TMP)/partial_hall_two_wall_gate_corpus_audit.json
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_partial_hall_augmenting_exchange_topologies.py --input results/partial_hall_radius_one_2321_lra_compact.json --input results/partial_hall_utilitarian_maximality_anneal_seed17_cont117.json --input results/partial_hall_utilitarian_maximality_anneal_seed23.json --input results/partial_hall_pareto_cegar_session1.json --input results/partial_hall_utilitarian_local_cegar_session1.json --input results/partial_hall_utilitarian_local_r3_cegar_session1.json --input results/partial_hall_utilitarian_local_r4_cegar_session1.json --output $(VERIFY_TMP)/partial_hall_augmenting_exchange_topology_audit.json
	cmp results/partial_hall_augmenting_exchange_topology_audit.json $(VERIFY_TMP)/partial_hall_augmenting_exchange_topology_audit.json
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/search_partial_hall_two_positive_reroute.py --directory results --output $(VERIFY_TMP)/partial_hall_two_positive_reroute_corpus_search.json
	cmp results/partial_hall_two_positive_reroute_corpus_search.json $(VERIFY_TMP)/partial_hall_two_positive_reroute_corpus_search.json
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/mine_partial_hall_rival_set_cover.py --source results/partial_hall_two_positive_reroute_corpus_search.json --output $(VERIFY_TMP)/partial_hall_rival_set_cover_r5.json --radius 5
	cmp results/partial_hall_rival_set_cover_r5.json $(VERIFY_TMP)/partial_hall_rival_set_cover_r5.json
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_partial_hall_complementary_swaps.py --source results/partial_hall_two_positive_reroute_corpus_search.json --output $(VERIFY_TMP)/partial_hall_complementary_swap_audit.json
	cmp results/partial_hall_complementary_swap_audit.json $(VERIFY_TMP)/partial_hall_complementary_swap_audit.json
	test "$$(z3 results/partial_hall_opposite_third_pairing_algebra.smt2)" = "unsat"
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/run_smt2_cvc5.py --source results/partial_hall_opposite_third_pairing_algebra.smt2 --output $(VERIFY_TMP)/partial_hall_opposite_third_pairing_algebra_cvc5.json --timeout-seconds 60
	test "$$(jq -r .status $(VERIFY_TMP)/partial_hall_opposite_third_pairing_algebra_cvc5.json)" = "UNSAT"
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/extract_partial_hall_farkas_certificate.py --source results/partial_hall_complementary_swap_gate8_frozen_cell.json --output $(VERIFY_TMP)/partial_hall_complementary_swap_gate8_frozen_cell_farkas.json
	cmp results/partial_hall_complementary_swap_gate8_frozen_cell_farkas.json $(VERIFY_TMP)/partial_hall_complementary_swap_gate8_frozen_cell_farkas.json
	test "$$(z3 results/partial_hall_six_wall_algebra.smt2)" = "unsat"
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/run_smt2_cvc5.py --source results/partial_hall_six_wall_algebra.smt2 --output $(VERIFY_TMP)/partial_hall_six_wall_algebra_cvc5.json --timeout-seconds 60
	test "$$(jq -r .status $(VERIFY_TMP)/partial_hall_six_wall_algebra_cvc5.json)" = "UNSAT"
	test "$$(z3 results/partial_hall_utilitarian_frozen_cell_pareto_core.smt2)" = "unsat"
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/run_smt2_cvc5.py --source results/partial_hall_utilitarian_frozen_cell_pareto_core.cvc5.smt2 --output $(VERIFY_TMP)/partial_hall_utilitarian_frozen_cell_pareto_core_cvc5.json --timeout-seconds 60
	test "$$(jq -r .status $(VERIFY_TMP)/partial_hall_utilitarian_frozen_cell_pareto_core_cvc5.json)" = "UNSAT"
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/extract_partial_hall_farkas_certificate.py --source results/partial_hall_utilitarian_frozen_cell_pareto_core.json --output $(VERIFY_TMP)/partial_hall_utilitarian_frozen_cell_pareto_farkas.json
	cmp results/partial_hall_utilitarian_frozen_cell_pareto_farkas.json $(VERIFY_TMP)/partial_hall_utilitarian_frozen_cell_pareto_farkas.json
	cmp results/partial_hall_pareto_cegar_model_audit.json $(VERIFY_TMP)/partial_hall_pareto_cegar_model_audit.json
	cmp results/partial_hall_pareto_cegar_completion_audit.json $(VERIFY_TMP)/partial_hall_pareto_cegar_completion_audit.json
	cmp results/partial_hall_utilitarian_local_cegar_session1_audit.json $(VERIFY_TMP)/partial_hall_utilitarian_local_cegar_session1_audit.json
	cmp results/partial_hall_utilitarian_local_r3_cegar_session1_audit.json $(VERIFY_TMP)/partial_hall_utilitarian_local_r3_cegar_session1_audit.json
	cmp results/partial_hall_utilitarian_local_r4_cegar_session1_audit.json $(VERIFY_TMP)/partial_hall_utilitarian_local_r4_cegar_session1_audit.json
	cmp results/partial_hall_utilitarian_local_r5_double_factored_audit.json $(VERIFY_TMP)/partial_hall_utilitarian_local_r5_double_factored_audit.json

verify-rank1-core-shape-ladder:
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_common_favorite_rank1_core_shape_ladder.py --cap4-core results/efx49_common_favorite_rank1_extended_bridge_collision12_cap4_hall_core6.json --cap5-matching-core results/efx49_common_favorite_rank1_extended_bridge_collision12_cap5_shapeaware_matching_core1.json --cap5-hall-replay results/efx49_common_favorite_rank1_extended_bridge_collision12_cap5_matching_core112_hall_replay.json --cap6-stage results/efx49_common_favorite_rank1_extended_bridge_collision12_cap6_core112_probe.json --cap6-stage results/efx49_common_favorite_rank1_extended_bridge_collision12_cap6_shape_ladder_cegar2.json --cap6-stage results/efx49_common_favorite_rank1_extended_bridge_collision12_cap6_shape_ladder_cegar3.json --cap6-stage results/efx49_common_favorite_rank1_extended_bridge_collision12_cap6_shape_ladder_cegar4.json --output $(VERIFY_TMP)/efx49-common-favorite-rank1-core-shape-ladder-audit.json
	cmp results/efx49_common_favorite_rank1_core_shape_ladder_audit.json $(VERIFY_TMP)/efx49-common-favorite-rank1-core-shape-ladder-audit.json

verify-parkability: verify-adaptive-first-agent-core verify-safe-floater-exchange verify-bundle-cycle-source verify-floater-substitution-cycle verify-partial-nash-substitution-census verify-partial-nash-local-trichotomy-refutation verify-partial-pareto-completion-refutation
	mkdir -p $(VERIFY_TMP)
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/test_parkability.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_lexmax_counterexample.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_forced_singleton_swap_lemma.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_favorite_singleton_hall_lemma.py --output $(VERIFY_TMP)/favorite-singleton-hall-lemma.json
	cmp results/favorite_singleton_hall_lemma_audit.json $(VERIFY_TMP)/favorite-singleton-hall-lemma.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_borda_shape_theorem.py --results-dir results --output $(VERIFY_TMP)/borda-shape-theorem.json
	cmp results/efx49_borda_shape3222_dual_encoding_audit.json $(VERIFY_TMP)/borda-shape-theorem.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_rank_gap_boundary.py --output $(VERIFY_TMP)/rank-gap-boundary.json
	cmp results/efx49_rankgap12_shape_boundary_audit.json $(VERIFY_TMP)/rank-gap-boundary.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_rank_gap12_theorem.py --results-dir results --output $(VERIFY_TMP)/rank-gap12-theorem.json
	cmp results/efx49_rankgap12_dual_encoding_audit.json $(VERIFY_TMP)/rank-gap12-theorem.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_rank_gap13_boundaries.py --results-dir results --output $(VERIFY_TMP)/rank-gap13-boundaries.json
	cmp results/efx49_rankgap13_shape_boundaries_audit.json $(VERIFY_TMP)/rank-gap13-boundaries.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_rank_gap13_theorem.py --results-dir results --output $(VERIFY_TMP)/rank-gap13-theorem.json
	cmp results/efx49_rankgap13_theorem_audit.json $(VERIFY_TMP)/rank-gap13-theorem.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_rank_gap14_favorites211_boundary.py --results-dir results --output $(VERIFY_TMP)/rank-gap14-favorites211-boundary.json
	cmp results/efx49_rankgap14_favorites211_boundary_audit.json $(VERIFY_TMP)/rank-gap14-favorites211-boundary.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_rank_gap12_sparse_common.py --results-dir results --output $(VERIFY_TMP)/rank-gap12-sparse-common.json
	cmp results/efx49_rankgap12_sparse_common_audit.json $(VERIFY_TMP)/rank-gap12-sparse-common.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_real_common_frontier.py --source results/efx49_common_favorite_real_sparse_session1.json --output $(VERIFY_TMP)/real-common-frontier.json
	cmp results/efx49_common_favorite_real_frontier_audit.json $(VERIFY_TMP)/real-common-frontier.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_balanced_boundary.py --source results/efx49_common_favorite_real_shape6111_session1.json --output $(VERIFY_TMP)/real-common-balanced-boundary.json
	cmp results/efx49_common_favorite_real_balanced_boundary_audit.json $(VERIFY_TMP)/real-common-balanced-boundary.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_favorite_singleton_hall_boundaries.py --output $(VERIFY_TMP)/real-common-hall-boundaries.json
	cmp results/efx49_common_favorite_hall_boundaries_audit.json $(VERIFY_TMP)/real-common-hall-boundaries.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_mixed_hall_boundaries.py --source results/efx49_common_favorite_threshold_pass_hall_611_cap20_cpsat_session1.json --source results/efx49_common_favorite_threshold_pass_hall_332_cap20_cpsat_session1.json --output $(VERIFY_TMP)/common-favorite-mixed-hall-boundaries.json
	cmp results/efx49_common_favorite_mixed_hall_boundaries_audit.json $(VERIFY_TMP)/common-favorite-mixed-hall-boundaries.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_mixed_hall_local6_boundary.py --source results/efx49_common_favorite_threshold_pass_hall_332_no_local6_cap20_cpsat_session1.json --output $(VERIFY_TMP)/common-favorite-mixed-hall-local6-boundary.json
	cmp results/efx49_common_favorite_mixed_hall_local6_boundary_audit.json $(VERIFY_TMP)/common-favorite-mixed-hall-local6-boundary.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_mixed_hall_radius2_gate.py --cap6 results/efx49_common_favorite_threshold_pass_hall_332_no_radius2_cap6_cpsat_session1.json --cap20 results/efx49_common_favorite_threshold_pass_hall_332_no_radius2_cap20_cpsat_session1.json --cegar results/efx49_common_favorite_threshold_pass_hall_332_no_radius2_cap6_cpsat_cegar_session1.json --output $(VERIFY_TMP)/common-favorite-mixed-hall-radius2-gate.json
	cmp results/efx49_common_favorite_mixed_hall_radius2_gate_audit.json $(VERIFY_TMP)/common-favorite-mixed-hall-radius2-gate.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_mixed_selection_gate.py --profile results/efx49_common_favorite_threshold_pass_hall_611_cap20_cpsat_session1.json --profile results/efx49_common_favorite_threshold_pass_hall_332_cap20_cpsat_session1.json --profile results/efx49_common_favorite_threshold_pass_hall_332_no_local6_cap20_cpsat_session1.json --zero-search results/efx49_common_favorite_mixed_zero_neighbor_332_cap20_cegar_session1.json --rank-search results/efx49_common_favorite_mixed_rank2_332_cap20_cegar_session1.json --output $(VERIFY_TMP)/common-favorite-mixed-selection-gate.json
	cmp results/efx49_common_favorite_mixed_selection_gate_audit.json $(VERIFY_TMP)/common-favorite-mixed-selection-gate.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_mixed_selection_gate.py --profile results/efx49_common_favorite_threshold_pass_hall_611_cap20_cpsat_session1.json --profile results/efx49_common_favorite_threshold_pass_hall_332_cap20_cpsat_session1.json --profile results/efx49_common_favorite_threshold_pass_hall_332_no_local6_cap20_cpsat_session1.json --zero-search results/efx49_common_favorite_mixed_zero_neighbor_332_cap20_sym_cegar_session2.json --rank-search results/efx49_common_favorite_mixed_rank2_332_cap20_sym_cegar_session2.json --output $(VERIFY_TMP)/common-favorite-mixed-selection-gate-v2.json
	cmp results/efx49_common_favorite_mixed_selection_gate_audit_v2.json $(VERIFY_TMP)/common-favorite-mixed-selection-gate-v2.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_rank2_selection_refutation.py --source results/efx49_common_favorite_mixed_rank2_332_cap4_sym_cegar_session2.json --output $(VERIFY_TMP)/common-favorite-rank2-selection-refutation.json
	cmp results/efx49_common_favorite_rank2_selection_refutation_audit.json $(VERIFY_TMP)/common-favorite-rank2-selection-refutation.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_fourtype_rank2_frontier.py --source results/efx49_common_favorite_mixed_rank2_332_cap4_fourtype_sym_cegar_session1.json --source results/efx49_common_favorite_mixed_rank2_332_cap4_fourtype_sym_cegar_session2.json --output $(VERIFY_TMP)/common-favorite-fourtype-rank2-frontier.json
	cmp results/efx49_common_favorite_fourtype_rank2_frontier_audit.json $(VERIFY_TMP)/common-favorite-fourtype-rank2-frontier.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_rank2_selection_refutation.py --profile fourtype --source results/efx49_common_favorite_mixed_rank2_332_cap4_fourtype_sym_cegar_session3.json --output $(VERIFY_TMP)/common-favorite-fourtype-rank2-refutation.json
	cmp results/efx49_common_favorite_fourtype_rank2_refutation_audit.json $(VERIFY_TMP)/common-favorite-fourtype-rank2-refutation.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_row_merge_interpolation.py --source results/t47.json --result $(VERIFY_TMP)/t47-row-merge-interpolation.json
	cmp results/t47_row_merge_interpolation_audit.json $(VERIFY_TMP)/t47-row-merge-interpolation.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_row_merge_interpolation.py --source results/tb4.json --result $(VERIFY_TMP)/tb4-row-merge-interpolation.json
	cmp results/tb4_row_merge_interpolation_audit.json $(VERIFY_TMP)/tb4-row-merge-interpolation.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_row_merge_interpolation.py --source results/tight49_witness.json --result $(VERIFY_TMP)/tight49-row-merge-interpolation.json
	cmp results/tight49_row_merge_interpolation_audit.json $(VERIFY_TMP)/tight49-row-merge-interpolation.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_row_merge_interpolation.py --source results/tight410_witness.json --result $(VERIFY_TMP)/tight410-row-merge-interpolation.json
	cmp results/tight410_row_merge_interpolation_audit.json $(VERIFY_TMP)/tight410-row-merge-interpolation.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_row_merge_essential_edge_hall.py --output $(VERIFY_TMP)/row-merge-essential-edge-hall.json
	cmp results/row_merge_essential_edge_hall_audit.json $(VERIFY_TMP)/row-merge-essential-edge-hall.json
	PYTHONDONTWRITEBYTECODE=1 python tracks/parkability/audit_row_merge_single_wall_radius.py --source results/row_merge_single_wall_q2_radius2_refutation.json --source results/row_merge_single_wall_q3_radius2_refutation.json --source results/row_merge_single_wall_q4_radius1_refutation.json --unsat-source results/row_merge_single_wall_q4_radius2_m7_unsat.json --normalization results/row_merge_single_wall_q4_radius2_m7_unsat.cvc5.normalization.json --cvc5 results/row_merge_single_wall_q4_radius2_m7_unsat.cvc5.json --core results/row_merge_single_wall_q4_radius2_m7_core.json --core-normalization results/row_merge_single_wall_q4_radius2_m7_core.cvc5.normalization.json --core-cvc5 results/row_merge_single_wall_q4_radius2_m7_core.cvc5.json --genericity-core results/row_merge_single_wall_q4_radius2_m7_genericity_core.json --genericity-normalization results/row_merge_single_wall_q4_radius2_m7_genericity_core.cvc5.normalization.json --genericity-cvc5 results/row_merge_single_wall_q4_radius2_m7_genericity_core.cvc5.json --pair-pivot results/row_merge_q4_small_step_pair_m8.json --pair-pivot-normalization results/row_merge_q4_small_step_pair_m8.cvc5.normalization.json --pair-pivot-cvc5 results/row_merge_q4_small_step_pair_m8.cvc5.json --output $(VERIFY_TMP)/row-merge-single-wall-radius-refutations.json
	cmp results/row_merge_single_wall_radius_refutation_audit.json $(VERIFY_TMP)/row-merge-single-wall-radius-refutations.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_row_merge_interpolation.py --source results/efx49_common_favorite_threshold_pass_hall_611_cap20_cpsat_session1.json --result $(VERIFY_TMP)/common-favorite-threshold-pass-hall-611-row-merge-interpolation.json
	cmp results/efx49_common_favorite_threshold_pass_hall_611_row_merge_interpolation_audit.json $(VERIFY_TMP)/common-favorite-threshold-pass-hall-611-row-merge-interpolation.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_row_merge_interpolation.py --source results/efx49_common_favorite_threshold_pass_hall_332_cap20_cpsat_session1.json --result $(VERIFY_TMP)/common-favorite-threshold-pass-hall-332-row-merge-interpolation.json
	cmp results/efx49_common_favorite_threshold_pass_hall_332_row_merge_interpolation_audit.json $(VERIFY_TMP)/common-favorite-threshold-pass-hall-332-row-merge-interpolation.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_rank1_triple_gate.py --dense results/efx49_common_favorite_rank1_triple_conversion_lra_session1.json --cegar results/efx49_common_favorite_rank1_triple_conversion_cegar_session1.json --normalization results/efx49_common_favorite_rank1_triple_conversion_cegar_session1.cvc5.normalization.json --output $(VERIFY_TMP)/common-favorite-rank1-triple-gate.json
	cmp results/efx49_common_favorite_rank1_triple_gate_audit.json $(VERIFY_TMP)/common-favorite-rank1-triple-gate.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_rank1_local6_boundary.py --local6 results/efx49_common_favorite_rank1_triple_fixed_conversion_cap20_cpsat_cegar_session1.json --radius2 results/efx49_common_favorite_rank1_triple_no_radius2_cap20_cpsat_cegar_session1.json --output $(VERIFY_TMP)/common-favorite-rank1-local6-boundary.json
	cmp results/efx49_common_favorite_rank1_local6_boundary_audit.json $(VERIFY_TMP)/common-favorite-rank1-local6-boundary.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_rank1_radius2_orbits.py --local6 results/efx49_common_favorite_rank1_triple_fixed_conversion_cap20_cpsat_cegar_session1.json --contested results/efx49_common_favorite_rank1_triple_no_contested_radius2_cap20_cpsat_cegar_session1.json --output $(VERIFY_TMP)/common-favorite-rank1-radius2-orbits.json
	cmp results/efx49_common_favorite_rank1_radius2_orbits_audit.json $(VERIFY_TMP)/common-favorite-rank1-radius2-orbits.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_rank1_contested_refutation.py --session1 results/efx49_common_favorite_rank1_triple_zero_neighbor_contested_cap6_sym_cpsat_cegar_session1.json --session2 results/efx49_common_favorite_rank1_triple_zero_neighbor_contested_cap6_sym_cpsat_cegar_session2.json --bridge-boundary results/efx49_common_favorite_rank1_triple_no_radius2_bridge_cap6_sym_cpsat_cegar_session1.json --output $(VERIFY_TMP)/common-favorite-rank1-contested-refutation.json
	cmp results/efx49_common_favorite_rank1_contested_refutation_audit.json $(VERIFY_TMP)/common-favorite-rank1-contested-refutation.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_rank1_bridge_checkpoint.py --source results/efx49_common_favorite_rank1_bridge_checkpoint_profile.json --output $(VERIFY_TMP)/common-favorite-rank1-bridge-checkpoint.json
	cmp results/efx49_common_favorite_rank1_bridge_checkpoint_audit.json $(VERIFY_TMP)/common-favorite-rank1-bridge-checkpoint.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_rank1_bridge_refutation.py --source results/efx49_common_favorite_rank1_bridge_singleton_cap6_sym_cpsat_cegar_session1.json --output $(VERIFY_TMP)/common-favorite-rank1-bridge-refutation.json
	cmp results/efx49_common_favorite_rank1_bridge_refutation_audit.json $(VERIFY_TMP)/common-favorite-rank1-bridge-refutation.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_rank1_extended_bridge_checkpoint.py --source results/efx49_common_favorite_rank1_extended_bridge_checkpoint_profile.json --output $(VERIFY_TMP)/common-favorite-rank1-extended-bridge-checkpoint.json
	cmp results/efx49_common_favorite_rank1_extended_bridge_checkpoint_audit.json $(VERIFY_TMP)/common-favorite-rank1-extended-bridge-checkpoint.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/search_common_favorite_rank1_bridge_singletons_local.py --source results/efx49_common_favorite_rank1_extended_bridge_checkpoint_profile.json --repair-family bridge45 --upper 6 --hamming-two --output $(VERIFY_TMP)/common-favorite-rank1-extended-bridge-local.json
	cmp results/efx49_common_favorite_rank1_extended_bridge_checkpoint_local_audit.json $(VERIFY_TMP)/common-favorite-rank1-extended-bridge-local.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_rank1_extended_bridge_identical.py --matching results/efx49_common_favorite_rank1_extended_bridge_identical_cap6_matching_session1.json --hall results/efx49_common_favorite_rank1_extended_bridge_identical_cap6_hall_session1.json --checkpoint results/efx49_common_favorite_rank1_extended_bridge_checkpoint_profile.json --output $(VERIFY_TMP)/common-favorite-rank1-extended-bridge-identical.json
	cmp results/efx49_common_favorite_rank1_extended_bridge_identical_audit.json $(VERIFY_TMP)/common-favorite-rank1-extended-bridge-identical.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_rank1_extended_bridge_collision_cap4.py --matching12 results/efx49_common_favorite_rank1_extended_bridge_collision12_cap4_duplicate_matching_session1.json --matching23 results/efx49_common_favorite_rank1_extended_bridge_collision23_cap4_duplicate_matching_session1.json --hall12 results/efx49_common_favorite_rank1_extended_bridge_collision12_cap4_duplicate_hall_session1.json --hall23 results/efx49_common_favorite_rank1_extended_bridge_collision23_cap4_duplicate_hall_session1.json --output $(VERIFY_TMP)/common-favorite-rank1-extended-bridge-collision-cap4.json
	cmp results/efx49_common_favorite_rank1_extended_bridge_collision_cap4_audit.json $(VERIFY_TMP)/common-favorite-rank1-extended-bridge-collision-cap4.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_rank1_extended_bridge_collision_cap4.py --upper 5 --matching12 results/efx49_common_favorite_rank1_extended_bridge_collision12_cap5_duplicate_matching_session1.json --matching23 results/efx49_common_favorite_rank1_extended_bridge_collision23_cap5_duplicate_matching_session1.json --hall12 results/efx49_common_favorite_rank1_extended_bridge_collision12_cap5_duplicate_hall_session1.json --hall23 results/efx49_common_favorite_rank1_extended_bridge_collision23_cap5_duplicate_hall_session1.json --output $(VERIFY_TMP)/common-favorite-rank1-extended-bridge-collision-cap5.json
	cmp results/efx49_common_favorite_rank1_extended_bridge_collision_cap5_audit.json $(VERIFY_TMP)/common-favorite-rank1-extended-bridge-collision-cap5.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_owner_threshold_shape_envelope.py --output $(VERIFY_TMP)/owner-threshold-shape-envelope.json
	cmp results/efx49_owner_threshold_shape_envelope_audit.json $(VERIFY_TMP)/owner-threshold-shape-envelope.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_owner_threshold_pair_degree_encoding.py --output $(VERIFY_TMP)/owner-threshold-pair-degree-encoding.json
	cmp results/efx49_owner_threshold_pair_degree_encoding_audit.json $(VERIFY_TMP)/owner-threshold-pair-degree-encoding.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_normal_form_boundaries.py --output $(VERIFY_TMP)/distinct-half-normal-form-boundaries.json
	cmp results/efx49_distinct_half_normal_form_boundaries_audit.json $(VERIFY_TMP)/distinct-half-normal-form-boundaries.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_fixed_host_lex_boundary.py --output $(VERIFY_TMP)/distinct-half-fixed-host-lex-boundary.json
	cmp results/efx49_distinct_half_fixed_host_lex_boundary_audit.json $(VERIFY_TMP)/distinct-half-fixed-host-lex-boundary.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_structured_floor_boundary.py --output $(VERIFY_TMP)/distinct-half-structured-floor-boundary.json
	cmp results/efx49_distinct_half_structured_floor_boundary_audit.json $(VERIFY_TMP)/distinct-half-structured-floor-boundary.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_three_lex_parking.py --output $(VERIFY_TMP)/common-three-lex-parking.json
	cmp results/efx49_common_three_lex_parking_audit.json $(VERIFY_TMP)/common-three-lex-parking.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_three_theorem.py --results-dir results --output $(VERIFY_TMP)/common-three-theorem.json
	cmp results/efx49_common_three_dual_encoding_audit.json $(VERIFY_TMP)/common-three-theorem.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_floor_theorem.py --results-dir results --output $(VERIFY_TMP)/distinct-half-floor-theorem.json
	cmp results/efx49_distinct_half_floor_dual_encoding_audit.json $(VERIFY_TMP)/distinct-half-floor-theorem.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_density_floor_lemma.py --output $(VERIFY_TMP)/distinct-half-density-floor-lemma.json
	cmp results/efx49_distinct_half_density_floor_lemma_audit.json $(VERIFY_TMP)/distinct-half-density-floor-lemma.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_rank_augmentation.py --results-dir results --output $(VERIFY_TMP)/distinct-half-rank-augmentation.json
	cmp results/efx49_distinct_half_rank_augmentation_audit.json $(VERIFY_TMP)/distinct-half-rank-augmentation.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_rank_radius_boundary.py --output $(VERIFY_TMP)/distinct-half-rank-radius-boundary.json
	cmp results/efx49_distinct_half_rank_radius_boundary_audit.json $(VERIFY_TMP)/distinct-half-rank-radius-boundary.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_favorite_pair_rank_boundary.py --output $(VERIFY_TMP)/distinct-half-favorite-pair-rank-boundary.json
	cmp results/efx49_distinct_half_favorite_pair_rank_boundary_audit.json $(VERIFY_TMP)/distinct-half-favorite-pair-rank-boundary.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_one_defect_favorite_triple_conversion.py --output $(VERIFY_TMP)/one-defect-favorite-triple-conversion.json
	cmp results/efx49_one_defect_favorite_triple_conversion_audit.json $(VERIFY_TMP)/one-defect-favorite-triple-conversion.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_favorite_triple_hall_characterization.py --output $(VERIFY_TMP)/favorite-triple-hall-characterization.json
	cmp results/efx49_favorite_triple_hall_characterization_audit.json $(VERIFY_TMP)/favorite-triple-hall-characterization.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_six_vertex_tutte_classification.py --output $(VERIFY_TMP)/six-vertex-tutte-classification.json
	cmp results/efx49_six_vertex_tutte_classification_audit.json $(VERIFY_TMP)/six-vertex-tutte-classification.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_favorite_triple_boundary.py --output $(VERIFY_TMP)/distinct-half-favorite-triple-boundary.json
	cmp results/efx49_distinct_half_favorite_triple_boundary_audit.json $(VERIFY_TMP)/distinct-half-favorite-triple-boundary.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_two_core_boundary.py --output $(VERIFY_TMP)/distinct-half-two-core-boundary.json
	cmp results/efx49_distinct_half_two_core_boundary_audit.json $(VERIFY_TMP)/distinct-half-two-core-boundary.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_canonical_two_core_boundary.py --output $(VERIFY_TMP)/distinct-half-canonical-two-core-boundary.json
	cmp results/efx49_distinct_half_canonical_two_core_boundary_audit.json $(VERIFY_TMP)/distinct-half-canonical-two-core-boundary.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_two_core_decision_boundary.py --matching results/efx49_distinct_half_two_core_cegar_matching_session1.json --hall results/efx49_distinct_half_two_core_cegar_hall_session1.json --complement results/efx49_distinct_half_two_core_complement_cegar_session1.json --reified-complement results/efx49_distinct_half_two_core_reified_complement_cegar_session1.json --cpsat results/efx49_distinct_half_two_core_cpsat_cap20_session1.json --cpsat-cegar results/efx49_distinct_half_two_core_cpsat_cegar_cap20_session3.json --output $(VERIFY_TMP)/distinct-half-two-core-decision-boundary.json
	cmp results/efx49_distinct_half_two_core_decision_boundary_audit.json $(VERIFY_TMP)/distinct-half-two-core-decision-boundary.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_two_core_encoding.py --output $(VERIFY_TMP)/distinct-half-two-core-encoding.json
	cmp results/efx49_distinct_half_two_core_encoding_audit.json $(VERIFY_TMP)/distinct-half-two-core-encoding.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_full_cell_encoding.py --output $(VERIFY_TMP)/distinct-half-full-cell-encoding.json
	cmp results/efx49_distinct_half_full_cell_encoding_audit.json $(VERIFY_TMP)/distinct-half-full-cell-encoding.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_full_cell_decision_boundary.py --result results/efx49_distinct_half_full_cell_complement_cegar_session1.json --cpsat-cegar results/efx49_distinct_half_full_cell_cpsat_cegar_cap20_session3.json --output $(VERIFY_TMP)/distinct-half-full-cell-decision-boundary.json
	cmp results/efx49_distinct_half_full_cell_decision_boundary_audit.json $(VERIFY_TMP)/distinct-half-full-cell-decision-boundary.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/select_distinct_half_full_cell_orbit_pool.py --family eight_orbit --output $(VERIFY_TMP)/distinct-half-full-cell-eight-orbit-pool.json
	cmp results/efx49_distinct_half_full_cell_eight_orbit_pool.json $(VERIFY_TMP)/distinct-half-full-cell-eight-orbit-pool.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/select_distinct_half_full_cell_orbit_pool.py --family six_orbit --output $(VERIFY_TMP)/distinct-half-full-cell-six-orbit-pool.json
	cmp results/efx49_distinct_half_full_cell_six_orbit_pool.json $(VERIFY_TMP)/distinct-half-full-cell-six-orbit-pool.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/verify_distinct_half_full_cell_cnf_minimal_core.py --parent results/efx49_distinct_half_full_cell_lia_cap5_core3.json --candidate results/efx49_distinct_half_full_cell_cap5_minimal_core.json --cap 5 --output $(VERIFY_TMP)/distinct-half-full-cell-cap5-minimal-core.json
	cmp results/efx49_distinct_half_full_cell_cap5_minimal_core.json $(VERIFY_TMP)/distinct-half-full-cell-cap5-minimal-core.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_full_cell_cap5.py --source results/efx49_distinct_half_full_cell_cpsat_cegar_cap5_session1.json --core results/efx49_distinct_half_full_cell_cpsat_cap5_core1.json --replay results/efx49_distinct_half_full_cell_lia_cap5_core1_session1.json --smt2 results/efx49_distinct_half_full_cell_lia_cap5_core1_session1.smt2 --lia-core2 results/efx49_distinct_half_full_cell_lia_cap5_core2.json --lia-core3 results/efx49_distinct_half_full_cell_lia_cap5_core3.json --minimal-core results/efx49_distinct_half_full_cell_cap5_minimal_core.json --cnf-result results/efx49_distinct_half_full_cell_cap5_core17_cadical.json --cnf results/efx49_distinct_half_full_cell_cap5_core17.cnf --drat-result results/efx49_distinct_half_full_cell_cap5_core17_drat_verification.json --compressed-proof output/cap5-certification/efx49_distinct_half_full_cell_cap5_core17.drat.xz --output $(VERIFY_TMP)/distinct-half-full-cell-cap5.json
	cmp results/efx49_distinct_half_full_cell_cap5_audit.json $(VERIFY_TMP)/distinct-half-full-cell-cap5.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/verify_distinct_half_full_cell_cnf_minimal_core.py --parent results/efx49_distinct_half_full_cell_cap6_cnf_core13.json --candidate results/efx49_distinct_half_full_cell_cap6_minimal_core.json --cap 6 --output $(VERIFY_TMP)/distinct-half-full-cell-cap6-minimal-core.json
	cmp results/efx49_distinct_half_full_cell_cap6_minimal_core_verified.json $(VERIFY_TMP)/distinct-half-full-cell-cap6-minimal-core.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_full_cell_cap6.py --source results/efx49_distinct_half_full_cell_cpsat_cegar_cap6_session1.json --core results/efx49_distinct_half_full_cell_cpsat_cap6_core1.json --replay results/efx49_distinct_half_full_cell_lia_cap6_core1_session1.json --smt2 results/efx49_distinct_half_full_cell_lia_cap6_core1_session1.smt2 --lia-core results/efx49_distinct_half_full_cell_lia_cap6_core2.json --minimal-core results/efx49_distinct_half_full_cell_cap6_minimal_core_verified.json --cnf-result results/efx49_distinct_half_full_cell_cap6_core21_cadical.json --cnf results/efx49_distinct_half_full_cell_cap6_core21.cnf --drat-result results/efx49_distinct_half_full_cell_cap6_core21_drat_verification.json --compressed-proof output/cap6-certification/efx49_distinct_half_full_cell_cap6_core21.drat.xz --output $(VERIFY_TMP)/distinct-half-full-cell-cap6.json
	cmp results/efx49_distinct_half_full_cell_cap6_audit.json $(VERIFY_TMP)/distinct-half-full-cell-cap6.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/analyze_distinct_half_full_cell_hall_witnesses.py --source results/efx49_distinct_half_full_cell_cap6_minimal_core_verified.json --output $(VERIFY_TMP)/distinct-half-full-cell-cap6-hall-witnesses.json
	cmp results/efx49_distinct_half_full_cell_cap6_hall_witness_census.json $(VERIFY_TMP)/distinct-half-full-cell-cap6-hall-witnesses.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_rr_hall_split_gate.py --output $(VERIFY_TMP)/distinct-half-rr-hall-split-gate.json
	cmp results/efx49_distinct_half_rr_hall_split_gate_audit.json $(VERIFY_TMP)/distinct-half-rr-hall-split-gate.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_zero_neighbor_favorite_triple_conversion.py --input results/efx49_distinct_half_eight_minus_six_anneal_seed27_session1.json --input results/efx49_distinct_half_eight_orbit_anneal_seed27_session2.json --negative-control results/efx49_distinct_half_eight_minus_six_anneal_seed30_session2.json --negative-control results/efx49_distinct_half_eight_orbit_anneal_seed30_session1.json --conditional-optimizer results/efx49_distinct_half_three_pairing_cell_cpsat_cap100_session1.json --output $(VERIFY_TMP)/zero-neighbor-favorite-triple-conversion.json --smt2 $(VERIFY_TMP)/zero-neighbor-favorite-triple-conversion.smt2
	cmp results/efx49_zero_neighbor_favorite_triple_conversion_audit.json $(VERIFY_TMP)/zero-neighbor-favorite-triple-conversion.json
	cmp results/efx49_zero_neighbor_favorite_triple_conversion.smt2 $(VERIFY_TMP)/zero-neighbor-favorite-triple-conversion.smt2
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_bottom_pairing_conversion.py --cardinal results/efx49_common_bottom_pairing_conversion_z3.json --sorting results/efx49_common_bottom_pairing_conversion_sorting_z3.json --cvc5 results/efx49_common_bottom_pairing_conversion_sorting_cvc5.json --cpc results/efx49_common_bottom_pairing_conversion_sorting_cpc_ethos.json --normalization results/efx49_common_bottom_pairing_conversion_sorting_cvc5.normalization.json --split results/efx49_common_bottom_pairing_conversion_zero_neighbor_sorting_z3.json --split results/efx49_common_bottom_pairing_conversion_two_edges_one_neighbor_sorting_z3.json --split results/efx49_common_bottom_pairing_conversion_three_edges_two_neighbors_sorting_z3.json --output $(VERIFY_TMP)/common-bottom-pairing-conversion.json
	cmp results/efx49_common_bottom_pairing_conversion_audit.json $(VERIFY_TMP)/common-bottom-pairing-conversion.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_three_agent_bottom_pairing_conversion.py --cardinal results/efx49_three_agent_bottom_pairing_conversion_cardinal_z3.json --sorting results/efx49_three_agent_bottom_pairing_conversion_sorting_z3.json --cvc5 results/efx49_three_agent_bottom_pairing_conversion_sorting_cvc5.json --cpc results/efx49_three_agent_bottom_pairing_conversion_sorting_cpc_ethos.json --normalization results/efx49_three_agent_bottom_pairing_conversion_sorting_cvc5.normalization.json --split results/efx49_three_agent_bottom_zero_neighbor_z3.json --split results/efx49_three_agent_bottom_two_edges_one_neighbor_z3.json --split results/efx49_three_agent_bottom_omit_neighbor_two_edges_one_neighbor_z3.json --split results/efx49_three_agent_bottom_three_edges_two_neighbors_z3.json --split results/efx49_three_agent_bottom_omit_neighbor_three_edges_two_neighbors_z3.json --order-core results/efx49_common_bottom_conversion_zero_neighbor_order_core.json --two-agent-boundary results/efx49_two_agent_bottom_zero_neighbor_conversion_boundary_z3.json --output $(VERIFY_TMP)/three-agent-bottom-pairing-conversion.json
	cmp results/efx49_three_agent_bottom_pairing_conversion_audit.json $(VERIFY_TMP)/three-agent-bottom-pairing-conversion.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_bottom_pair_pattern_census.py --output $(VERIFY_TMP)/bottom-pair-pattern-census.json
	cmp results/efx49_bottom_pair_pattern_census_audit.json $(VERIFY_TMP)/bottom-pair-pattern-census.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_bottom_pattern_conversion_orbits.py --pattern-index 0 --output $(VERIFY_TMP)/bottom-pattern0-conversion-orbits.json
	cmp results/efx49_bottom_pattern0_conversion_orbit_audit.json $(VERIFY_TMP)/bottom-pattern0-conversion-orbits.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_bottom_pattern_conversion_orbits.py --pattern-index 1 --output $(VERIFY_TMP)/bottom-pattern1-conversion-orbits.json
	cmp results/efx49_bottom_pattern1_conversion_orbit_audit.json $(VERIFY_TMP)/bottom-pattern1-conversion-orbits.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_bottom_pattern_conversion_orbits.py --pattern-index 2 --output $(VERIFY_TMP)/bottom-pattern2-conversion-orbits.json
	cmp results/efx49_bottom_pattern2_conversion_orbit_audit.json $(VERIFY_TMP)/bottom-pattern2-conversion-orbits.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_bottom_pattern_conversion_orbits.py --pattern-index 3 --output $(VERIFY_TMP)/bottom-pattern3-conversion-orbits.json
	cmp results/efx49_bottom_pattern3_conversion_orbit_audit.json $(VERIFY_TMP)/bottom-pattern3-conversion-orbits.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_bottom_pattern_conversion_orbits.py --pattern-index 4 --output $(VERIFY_TMP)/bottom-pattern4-conversion-orbits.json
	cmp results/efx49_bottom_pattern4_conversion_orbit_audit.json $(VERIFY_TMP)/bottom-pattern4-conversion-orbits.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_bottom_pattern_conversion_orbits.py --pattern-index 5 --output $(VERIFY_TMP)/bottom-pattern5-conversion-orbits.json
	cmp results/efx49_bottom_pattern5_conversion_orbit_audit.json $(VERIFY_TMP)/bottom-pattern5-conversion-orbits.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_bottom_pattern_conversion_orbits.py --pattern-index 6 --output $(VERIFY_TMP)/bottom-pattern6-conversion-orbits.json
	cmp results/efx49_bottom_pattern6_conversion_orbit_audit.json $(VERIFY_TMP)/bottom-pattern6-conversion-orbits.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_bottom_pattern_conversion_orbits.py --pattern-index 7 --output $(VERIFY_TMP)/bottom-pattern7-conversion-orbits.json
	cmp results/efx49_bottom_pattern7_conversion_orbit_audit.json $(VERIFY_TMP)/bottom-pattern7-conversion-orbits.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_bottom_pattern_conversion_orbits.py --pattern-index 8 --output $(VERIFY_TMP)/bottom-pattern8-conversion-orbits.json
	cmp results/efx49_bottom_pattern8_conversion_orbit_audit.json $(VERIFY_TMP)/bottom-pattern8-conversion-orbits.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_bottom_pattern_conversion_orbits.py --pattern-index 14 --output $(VERIFY_TMP)/bottom-pattern14-conversion-orbits.json
	cmp results/efx49_bottom_pattern14_conversion_orbit_audit.json $(VERIFY_TMP)/bottom-pattern14-conversion-orbits.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_bottom_pattern_conversion_orbits.py --pattern-index 19 --output $(VERIFY_TMP)/bottom-pattern19-conversion-orbits.json
	cmp results/efx49_bottom_pattern19_conversion_orbit_audit.json $(VERIFY_TMP)/bottom-pattern19-conversion-orbits.json
	for index in 9 10 11 12 13 15 16 17 18; do PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_bottom_pattern_conversion_orbits.py --pattern-index $$index --output $(VERIFY_TMP)/bottom-pattern$$index-conversion-orbits.json; cmp results/efx49_bottom_pattern$${index}_conversion_orbit_audit.json $(VERIFY_TMP)/bottom-pattern$$index-conversion-orbits.json; done
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_disjoint_double_bottom_pair_conversion.py --cardinal results/efx49_bottom_pattern6_conversion_selector_cegar_session1.json --sorting results/efx49_bottom_pattern6_conversion_selector_sorting_z3.json --cvc5 results/efx49_bottom_pattern6_conversion_selector_sorting_cvc5.json --normalization results/efx49_bottom_pattern6_conversion_selector_sorting_cvc5.normalization.json --cpc results/efx49_bottom_pattern6_conversion_selector_sorting_cpc_ethos.json --core results/efx49_bottom_pattern6_conversion_selector_sorting_core1.json --core-analysis results/efx49_bottom_pattern6_conversion_selector_sorting_core1_analysis.json --core-cvc5 results/efx49_bottom_pattern6_conversion_selector_sorting_core1_cvc5.json --core-normalization results/efx49_bottom_pattern6_conversion_selector_sorting_core1_cvc5.normalization.json --core-cpc results/efx49_bottom_pattern6_conversion_selector_sorting_core1_cpc_ethos.json --orbit-audit results/efx49_bottom_pattern6_conversion_orbit_audit.json --output $(VERIFY_TMP)/disjoint-double-bottom-conversion.json
	cmp results/efx49_disjoint_double_bottom_pair_conversion_audit.json $(VERIFY_TMP)/disjoint-double-bottom-conversion.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/analyze_bottom_pattern_conversion_core.py --source results/efx49_bottom_pattern6_conversion_selector_sorting_core1.json --output $(VERIFY_TMP)/bottom-pattern6-conversion-core1-analysis.json
	cmp results/efx49_bottom_pattern6_conversion_selector_sorting_core1_analysis.json $(VERIFY_TMP)/bottom-pattern6-conversion-core1-analysis.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_overlap22_three_repair_motif.py --source results/efx49_overlap22_bottom_pattern_anneal_session2.json --source results/efx49_overlap22_bottom_pattern_anneal_session3.json --source results/efx49_overlap22_bottom_pattern_anneal_session4.json --source results/efx49_overlap22_full_selector_cpsat_cap100_session1.json --output $(VERIFY_TMP)/overlap22-three-repair-motif.json
	cmp results/efx49_overlap22_three_repair_motif_audit.json $(VERIFY_TMP)/overlap22-three-repair-motif.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_overlap_orbit1_shared_active.py --cardinal results/efx49_two_pair_bottom_cross_overlap_orbit1_shared_active_cegar_session1.json --external-z3 results/efx49_two_pair_bottom_cross_overlap_orbit1_shared_active_external_z3.json --cvc5 results/efx49_two_pair_bottom_cross_overlap_orbit1_shared_active_cvc5.json --normalization results/efx49_two_pair_bottom_cross_overlap_orbit1_shared_active_cvc5.normalization.json --cpc results/efx49_two_pair_bottom_cross_overlap_orbit1_shared_active_cpc_ethos.json --proof results/efx49_two_pair_bottom_cross_overlap_orbit1_shared_active.cpc --output $(VERIFY_TMP)/overlap-orbit1-shared-active.json
	cmp results/efx49_overlap_orbit1_shared_active_audit.json $(VERIFY_TMP)/overlap-orbit1-shared-active.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_overlap_pattern_symmetry.py --source results/efx49_overlap22_bottom_pattern_anneal_session2.json --source results/efx49_overlap22_bottom_pattern_anneal_session3.json --source results/efx49_overlap22_bottom_pattern_anneal_session4.json --source results/efx49_overlap22_full_selector_cpsat_cap100_session1.json --output $(VERIFY_TMP)/overlap22-pattern-symmetry.json
	cmp results/efx49_overlap22_pattern_symmetry_audit.json $(VERIFY_TMP)/overlap22-pattern-symmetry.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_overlap_double_bottom_pair_conversion.py --cardinal results/efx49_bottom_pattern0_conversion_selector_symmetric_cardinal_session1.json --external-z3 results/efx49_bottom_pattern0_conversion_selector_symmetric_cardinal_external_z3.json --sorting results/efx49_bottom_pattern0_conversion_selector_symmetric_sorting_session1.json --cvc5 results/efx49_bottom_pattern0_conversion_selector_symmetric_sorting_cvc5.json --normalization results/efx49_bottom_pattern0_conversion_selector_symmetric_sorting_cvc5.normalization.json --cpc results/efx49_bottom_pattern0_conversion_selector_symmetric_sorting_cpc_ethos.json --proof results/efx49_bottom_pattern0_conversion_selector_symmetric_sorting.cpc --symmetry-audit results/efx49_overlap22_pattern_symmetry_audit.json --orbit-audit results/efx49_bottom_pattern0_conversion_orbit_audit.json --output $(VERIFY_TMP)/overlap-double-bottom-conversion.json
	cmp results/efx49_overlap_double_bottom_pair_conversion_audit.json $(VERIFY_TMP)/overlap-double-bottom-conversion.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_star_repeated_pattern_symmetry.py --output $(VERIFY_TMP)/star-repeated-pattern-symmetry.json
	cmp results/efx49_star_repeated_pattern_symmetry_audit.json $(VERIFY_TMP)/star-repeated-pattern-symmetry.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_star_repeated_bottom_pair_conversion.py --cardinal results/efx49_bottom_pattern1_conversion_selector_symmetric_cardinal_session1.json --external-z3 results/efx49_bottom_pattern1_conversion_selector_symmetric_cardinal_external_z3.json --sorting results/efx49_bottom_pattern1_conversion_selector_symmetric_sorting_session1.json --cvc5 results/efx49_bottom_pattern1_conversion_selector_symmetric_sorting_cvc5.json --normalization results/efx49_bottom_pattern1_conversion_selector_symmetric_sorting_cvc5.normalization.json --cpc results/efx49_bottom_pattern1_conversion_selector_symmetric_sorting_cpc_ethos.json --proof results/efx49_bottom_pattern1_conversion_selector_symmetric_sorting.cpc --symmetry-audit results/efx49_star_repeated_pattern_symmetry_audit.json --orbit-audit results/efx49_bottom_pattern1_conversion_orbit_audit.json --output $(VERIFY_TMP)/star-repeated-bottom-conversion.json
	cmp results/efx49_star_repeated_bottom_pair_conversion_audit.json $(VERIFY_TMP)/star-repeated-bottom-conversion.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_triangle_repeated_pattern_symmetry.py --output $(VERIFY_TMP)/triangle-repeated-pattern-symmetry.json
	cmp results/efx49_triangle_repeated_pattern_symmetry_audit.json $(VERIFY_TMP)/triangle-repeated-pattern-symmetry.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_triangle_repeated_bottom_pair_conversion.py --cardinal results/efx49_bottom_pattern2_conversion_selector_symmetric_cardinal_session1.json --external-z3 results/efx49_bottom_pattern2_conversion_selector_symmetric_cardinal_external_z3.json --sorting results/efx49_bottom_pattern2_conversion_selector_symmetric_sorting_session1.json --cvc5 results/efx49_bottom_pattern2_conversion_selector_symmetric_sorting_cvc5.json --normalization results/efx49_bottom_pattern2_conversion_selector_symmetric_sorting_cvc5.normalization.json --cpc results/efx49_bottom_pattern2_conversion_selector_symmetric_sorting_cpc_ethos.json --proof results/efx49_bottom_pattern2_conversion_selector_symmetric_sorting.cpc --symmetry-audit results/efx49_triangle_repeated_pattern_symmetry_audit.json --orbit-audit results/efx49_bottom_pattern2_conversion_orbit_audit.json --output $(VERIFY_TMP)/triangle-repeated-bottom-conversion.json
	cmp results/efx49_triangle_repeated_bottom_pair_conversion_audit.json $(VERIFY_TMP)/triangle-repeated-bottom-conversion.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_path_repeated_pattern_symmetry.py --output $(VERIFY_TMP)/path-repeated-pattern-symmetry.json
	cmp results/efx49_path_repeated_pattern_symmetry_audit.json $(VERIFY_TMP)/path-repeated-pattern-symmetry.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_repeated_bottom_pair_conversion.py --pattern-index 3 --cardinal results/efx49_bottom_pattern3_conversion_selector_symmetric_cardinal_session1.json --external-z3 results/efx49_bottom_pattern3_conversion_selector_symmetric_cardinal_external_z3.json --sorting results/efx49_bottom_pattern3_conversion_selector_symmetric_sorting_session1.json --cvc5 results/efx49_bottom_pattern3_conversion_selector_symmetric_sorting_cvc5.json --normalization results/efx49_bottom_pattern3_conversion_selector_symmetric_sorting_cvc5.normalization.json --cpc results/efx49_bottom_pattern3_conversion_selector_symmetric_sorting_cpc_ethos.json --proof results/efx49_bottom_pattern3_conversion_selector_symmetric_sorting.cpc --symmetry-audit results/efx49_path_repeated_pattern_symmetry_audit.json --orbit-audit results/efx49_bottom_pattern3_conversion_orbit_audit.json --output $(VERIFY_TMP)/bottom-pattern3-conversion.json
	cmp results/efx49_bottom_pattern3_conversion_audit.json $(VERIFY_TMP)/bottom-pattern3-conversion.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_remaining_repeated_pattern_symmetry.py --pattern-index 4 --output $(VERIFY_TMP)/end-repeated-path-pattern-symmetry.json
	cmp results/efx49_end_repeated_path_pattern_symmetry_audit.json $(VERIFY_TMP)/end-repeated-path-pattern-symmetry.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_repeated_bottom_pair_conversion.py --pattern-index 4 --cardinal results/efx49_bottom_pattern4_conversion_selector_symmetric_cardinal_session1.json --external-z3 results/efx49_bottom_pattern4_conversion_selector_symmetric_cardinal_external_z3.json --sorting results/efx49_bottom_pattern4_conversion_selector_symmetric_sorting_session1.json --cvc5 results/efx49_bottom_pattern4_conversion_selector_symmetric_sorting_cvc5.json --normalization results/efx49_bottom_pattern4_conversion_selector_symmetric_sorting_cvc5.normalization.json --cpc results/efx49_bottom_pattern4_conversion_selector_symmetric_sorting_cpc_ethos.json --proof results/efx49_bottom_pattern4_conversion_selector_symmetric_sorting.cpc --symmetry-audit results/efx49_end_repeated_path_pattern_symmetry_audit.json --orbit-audit results/efx49_bottom_pattern4_conversion_orbit_audit.json --output $(VERIFY_TMP)/bottom-pattern4-conversion.json
	cmp results/efx49_bottom_pattern4_conversion_audit.json $(VERIFY_TMP)/bottom-pattern4-conversion.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_remaining_repeated_pattern_symmetry.py --pattern-index 5 --output $(VERIFY_TMP)/detached-edge-repeated-pattern-symmetry.json
	cmp results/efx49_detached_edge_repeated_pattern_symmetry_audit.json $(VERIFY_TMP)/detached-edge-repeated-pattern-symmetry.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_repeated_bottom_pair_conversion.py --pattern-index 5 --cardinal results/efx49_bottom_pattern5_conversion_selector_symmetric_cardinal_session1.json --external-z3 results/efx49_bottom_pattern5_conversion_selector_symmetric_cardinal_external_z3.json --sorting results/efx49_bottom_pattern5_conversion_selector_symmetric_sorting_session1.json --cvc5 results/efx49_bottom_pattern5_conversion_selector_symmetric_sorting_cvc5.json --normalization results/efx49_bottom_pattern5_conversion_selector_symmetric_sorting_cvc5.normalization.json --cpc results/efx49_bottom_pattern5_conversion_selector_symmetric_sorting_cpc_ethos.json --proof results/efx49_bottom_pattern5_conversion_selector_symmetric_sorting.cpc --symmetry-audit results/efx49_detached_edge_repeated_pattern_symmetry_audit.json --orbit-audit results/efx49_bottom_pattern5_conversion_orbit_audit.json --output $(VERIFY_TMP)/bottom-pattern5-conversion.json
	cmp results/efx49_bottom_pattern5_conversion_audit.json $(VERIFY_TMP)/bottom-pattern5-conversion.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_remaining_repeated_pattern_symmetry.py --pattern-index 7 --output $(VERIFY_TMP)/disconnected-fork-repeated-pattern-symmetry.json
	cmp results/efx49_disconnected_fork_repeated_pattern_symmetry_audit.json $(VERIFY_TMP)/disconnected-fork-repeated-pattern-symmetry.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_repeated_bottom_pair_conversion.py --pattern-index 7 --cardinal results/efx49_bottom_pattern7_conversion_selector_symmetric_cardinal_session1.json --external-z3 results/efx49_bottom_pattern7_conversion_selector_symmetric_cardinal_external_z3.json --sorting results/efx49_bottom_pattern7_conversion_selector_symmetric_sorting_session1.json --cvc5 results/efx49_bottom_pattern7_conversion_selector_symmetric_sorting_cvc5.json --normalization results/efx49_bottom_pattern7_conversion_selector_symmetric_sorting_cvc5.normalization.json --cpc results/efx49_bottom_pattern7_conversion_selector_symmetric_sorting_cpc_ethos.json --proof results/efx49_bottom_pattern7_conversion_selector_symmetric_sorting.cpc --symmetry-audit results/efx49_disconnected_fork_repeated_pattern_symmetry_audit.json --orbit-audit results/efx49_bottom_pattern7_conversion_orbit_audit.json --output $(VERIFY_TMP)/bottom-pattern7-conversion.json
	cmp results/efx49_bottom_pattern7_conversion_audit.json $(VERIFY_TMP)/bottom-pattern7-conversion.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_remaining_repeated_pattern_symmetry.py --pattern-index 8 --output $(VERIFY_TMP)/three-disconnected-edges-pattern-symmetry.json
	cmp results/efx49_three_disconnected_edges_pattern_symmetry_audit.json $(VERIFY_TMP)/three-disconnected-edges-pattern-symmetry.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_repeated_bottom_pair_conversion.py --pattern-index 8 --cardinal results/efx49_bottom_pattern8_conversion_selector_symmetric_cardinal_session1.json --external-z3 results/efx49_bottom_pattern8_conversion_selector_symmetric_cardinal_external_z3.json --sorting results/efx49_bottom_pattern8_conversion_selector_symmetric_sorting_session1.json --cvc5 results/efx49_bottom_pattern8_conversion_selector_symmetric_sorting_cvc5.json --normalization results/efx49_bottom_pattern8_conversion_selector_symmetric_sorting_cvc5.normalization.json --cpc results/efx49_bottom_pattern8_conversion_selector_symmetric_sorting_cpc_ethos.json --proof results/efx49_bottom_pattern8_conversion_selector_symmetric_sorting.cpc --symmetry-audit results/efx49_three_disconnected_edges_pattern_symmetry_audit.json --orbit-audit results/efx49_bottom_pattern8_conversion_orbit_audit.json --output $(VERIFY_TMP)/bottom-pattern8-conversion.json
	cmp results/efx49_bottom_pattern8_conversion_audit.json $(VERIFY_TMP)/bottom-pattern8-conversion.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_all_repeated_bottom_pair_conversions.py --census results/efx49_bottom_pair_pattern_census_audit.json --audit results/efx49_star_repeated_bottom_pair_conversion_audit.json --audit results/efx49_triangle_repeated_bottom_pair_conversion_audit.json --audit results/efx49_bottom_pattern3_conversion_audit.json --audit results/efx49_bottom_pattern4_conversion_audit.json --audit results/efx49_bottom_pattern5_conversion_audit.json --audit results/efx49_bottom_pattern7_conversion_audit.json --audit results/efx49_bottom_pattern8_conversion_audit.json --output $(VERIFY_TMP)/all-repeated-bottom-pair-conversions.json
	cmp results/efx49_all_repeated_bottom_pair_conversions_audit.json $(VERIFY_TMP)/all-repeated-bottom-pair-conversions.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_remaining_repeated_pattern_symmetry.py --pattern-index 14 --output $(VERIFY_TMP)/four-cycle-pattern-symmetry.json
	cmp results/efx49_four_cycle_pattern_symmetry_audit.json $(VERIFY_TMP)/four-cycle-pattern-symmetry.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_all_distinct_bottom_pair_conversion.py --pattern-index 14 --symmetry-breaking four_cycle_canonical --cardinal results/efx49_bottom_pattern14_conversion_selector_symmetric_cardinal_session1.json --external-z3 results/efx49_bottom_pattern14_conversion_selector_symmetric_cardinal_external_z3.json --sorting results/efx49_bottom_pattern14_conversion_selector_symmetric_sorting_session1.json --cvc5 results/efx49_bottom_pattern14_conversion_selector_symmetric_sorting_cvc5.json --normalization results/efx49_bottom_pattern14_conversion_selector_symmetric_sorting_cvc5.normalization.json --cpc results/efx49_bottom_pattern14_conversion_selector_symmetric_sorting_cpc_ethos.json --proof results/efx49_bottom_pattern14_conversion_selector_symmetric_sorting.cpc --symmetry-audit results/efx49_four_cycle_pattern_symmetry_audit.json --orbit-audit results/efx49_bottom_pattern14_conversion_orbit_audit.json --output $(VERIFY_TMP)/bottom-pattern14-conversion.json
	cmp results/efx49_bottom_pattern14_conversion_audit.json $(VERIFY_TMP)/bottom-pattern14-conversion.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_remaining_repeated_pattern_symmetry.py --pattern-index 19 --output $(VERIFY_TMP)/four-disconnected-edges-pattern-symmetry.json
	cmp results/efx49_four_disconnected_edges_pattern_symmetry_audit.json $(VERIFY_TMP)/four-disconnected-edges-pattern-symmetry.json
	for index in 9 10 11 12 13 15 16 17 18; do PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_all_distinct_pattern_symmetry.py --pattern-index $$index --output $(VERIFY_TMP)/bottom-pattern$$index-generic-symmetry.json; cmp results/efx49_bottom_pattern$${index}_generic_symmetry_audit.json $(VERIFY_TMP)/bottom-pattern$$index-generic-symmetry.json; done
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_all_distinct_bottom_pair_conversion.py --pattern-index 19 --symmetry-breaking four_disconnected_edges_canonical --cardinal results/efx49_bottom_pattern19_conversion_selector_symmetric_cardinal_session1.json --external-z3 results/efx49_bottom_pattern19_conversion_selector_symmetric_sorting_external_z3.json --sorting results/efx49_bottom_pattern19_conversion_selector_symmetric_sorting_session1.json --cvc5 results/efx49_bottom_pattern19_conversion_selector_symmetric_sorting_cvc5.json --normalization results/efx49_bottom_pattern19_conversion_selector_symmetric_sorting_cvc5.normalization.json --cpc results/efx49_bottom_pattern19_conversion_selector_symmetric_sorting_cpc_ethos.json --proof results/efx49_bottom_pattern19_conversion_selector_symmetric_sorting.cpc --symmetry-audit results/efx49_four_disconnected_edges_pattern_symmetry_audit.json --orbit-audit results/efx49_bottom_pattern19_conversion_orbit_audit.json --output $(VERIFY_TMP)/bottom-pattern19-conversion.json
	cmp results/efx49_bottom_pattern19_conversion_audit.json $(VERIFY_TMP)/bottom-pattern19-conversion.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_all_distinct_z3_candidates.py --census results/efx49_bottom_pair_pattern_census_audit.json $(foreach index,9 10 11 12 13 15 16 17 18,--cardinal results/efx49_bottom_pattern$(index)_conversion_selector_generic_cardinal_session1.json --sorting results/efx49_bottom_pattern$(index)_conversion_selector_generic_sorting_session1.json) --cardinal results/efx49_bottom_pattern14_conversion_selector_symmetric_cardinal_session1.json --sorting results/efx49_bottom_pattern14_conversion_selector_symmetric_sorting_session1.json --cardinal results/efx49_bottom_pattern19_conversion_selector_symmetric_cardinal_session1.json --sorting results/efx49_bottom_pattern19_conversion_selector_symmetric_sorting_session1.json --output $(VERIFY_TMP)/all-distinct-dual-z3-candidates.json
	cmp results/efx49_all_distinct_dual_z3_candidates_audit.json $(VERIFY_TMP)/all-distinct-dual-z3-candidates.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_four_disconnected_six_conversion_core.py --core results/efx49_bottom_pattern19_conversion_selector_sorting_core1.json --minimized-core results/efx49_bottom_pattern19_conversion_selector_sorting_core2_minimized.json --analysis results/efx49_bottom_pattern19_conversion_selector_sorting_core1_analysis.json --cvc5 results/efx49_bottom_pattern19_conversion_selector_sorting_core1_cvc5.json --normalization results/efx49_bottom_pattern19_conversion_selector_sorting_core1_cvc5.normalization.json --cpc results/efx49_bottom_pattern19_conversion_selector_sorting_core1_cpc_ethos.json --proof results/efx49_bottom_pattern19_conversion_selector_sorting_core1.cpc --without-symmetry results/efx49_bottom_pattern19_conversion_selector_sorting_core1_without_symmetry.json --minimality results/efx49_bottom_pattern19_conversion_selector_sorting_core2_minimality_audit.json --output $(VERIFY_TMP)/bottom-pattern19-six-conversion-core.json
	cmp results/efx49_bottom_pattern19_six_conversion_core_audit.json $(VERIFY_TMP)/bottom-pattern19-six-conversion-core.json
	for index in 9 10 11 12 13 15 16 17 18; do PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_all_distinct_bottom_pair_conversion.py --pattern-index $$index --symmetry-breaking all_distinct_canonical --cardinal results/efx49_bottom_pattern$${index}_conversion_selector_generic_cardinal_session1.json --external-z3 results/efx49_bottom_pattern$${index}_conversion_selector_generic_cardinal_external_z3.json --sorting results/efx49_bottom_pattern$${index}_conversion_selector_generic_sorting_session1.json --cvc5 results/efx49_bottom_pattern$${index}_conversion_selector_generic_sorting_cvc5.json --normalization results/efx49_bottom_pattern$${index}_conversion_selector_generic_sorting_cvc5.normalization.json --cpc results/efx49_bottom_pattern$${index}_conversion_selector_generic_sorting_cpc_ethos.json --proof results/efx49_bottom_pattern$${index}_conversion_selector_generic_sorting.cpc --symmetry-audit results/efx49_bottom_pattern$${index}_generic_symmetry_audit.json --orbit-audit results/efx49_bottom_pattern$${index}_conversion_orbit_audit.json --output $(VERIFY_TMP)/bottom-pattern$$index-conversion.json; cmp results/efx49_bottom_pattern$${index}_conversion_audit.json $(VERIFY_TMP)/bottom-pattern$$index-conversion.json; done
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_all_distinct_bottom_pair_conversions.py --census results/efx49_bottom_pair_pattern_census_audit.json $(foreach index,9 10 11 12 13 14 15 16 17 18 19,--audit results/efx49_bottom_pattern$(index)_conversion_audit.json) --output $(VERIFY_TMP)/all-distinct-bottom-pair-conversions.json
	cmp results/efx49_all_distinct_bottom_pair_conversions_audit.json $(VERIFY_TMP)/all-distinct-bottom-pair-conversions.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_universal_threshold_existence.py --owner-threshold-audit results/efx49_owner_threshold_shape_envelope_audit.json --hall-characterization-audit results/efx49_favorite_triple_hall_characterization_audit.json --census results/efx49_bottom_pair_pattern_census_audit.json --three-agent results/efx49_three_agent_bottom_pairing_conversion_audit.json --double-bottom results/efx49_overlap_double_bottom_pair_conversion_audit.json --double-bottom results/efx49_disjoint_double_bottom_pair_conversion_audit.json --repeated results/efx49_all_repeated_bottom_pair_conversions_audit.json --all-distinct results/efx49_all_distinct_bottom_pair_conversions_audit.json --output $(VERIFY_TMP)/common-favorite-universal-threshold-efx.json
	cmp results/efx49_common_favorite_universal_threshold_efx_audit.json $(VERIFY_TMP)/common-favorite-universal-threshold-efx.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/analyze_bottom_pattern_conversion_core.py --source results/efx49_bottom_pattern0_conversion_selector_symmetric_cardinal_core1.json --output $(VERIFY_TMP)/bottom-pattern0-conversion-core1-analysis.json
	cmp results/efx49_bottom_pattern0_conversion_selector_symmetric_cardinal_core1_analysis.json $(VERIFY_TMP)/bottom-pattern0-conversion-core1-analysis.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_full_cell_orbit_gate.py --minimal-core results/efx49_distinct_half_full_cell_cap5_minimal_core.json --cap6-escape results/efx49_distinct_half_full_cell_integer_core17_cap6.json --anneal results/efx49_distinct_half_six_orbit_anneal_session1.json --cegar results/efx49_distinct_half_six_orbit_cegar_session1.json --refutation results/efx49_distinct_half_six_orbit_refutation_profile.json --eight-pool results/efx49_distinct_half_full_cell_eight_orbit_pool.json --eight-cpsat results/efx49_distinct_half_full_cell_eight_orbit_cpsat_cap20_session1.json --eight-cegar results/efx49_distinct_half_eight_orbit_cegar_session2.json --output $(VERIFY_TMP)/distinct-half-full-cell-orbit-gate.json
	cmp results/efx49_distinct_half_full_cell_orbit_gate_audit.json $(VERIFY_TMP)/distinct-half-full-cell-orbit-gate.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_terminal_exchange_gate.py --output $(VERIFY_TMP)/distinct-half-terminal-exchange-gate.json
	cmp results/efx49_distinct_half_terminal_exchange_gate_audit.json $(VERIFY_TMP)/distinct-half-terminal-exchange-gate.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_full_cell_cnf_encoding.py --source results/efx49_distinct_half_full_cell_cpsat_cegar_cap5_session1.json --output $(VERIFY_TMP)/distinct-half-full-cell-cnf-encoding.json
	cmp results/efx49_distinct_half_full_cell_cnf_encoding_audit.json $(VERIFY_TMP)/distinct-half-full-cell-cnf-encoding.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/analyze_distinct_half_two_core_seed_pool.py --seed results/efx49_distinct_half_favorite_triple_boundary_audit.json --seed results/efx49_distinct_half_structured_floor_boundary_audit.json --seed results/efx49_distinct_half_fixed_host_lex_boundary_audit.json --seed results/efx49_distinct_half_rank_radius_boundary_audit.json --seed results/efx49_universal_threshold_distinct_reps_cegar_session1.json --output $(VERIFY_TMP)/distinct-half-two-core-seed-pool.json
	cmp results/efx49_distinct_half_two_core_seed_pool_analysis.json $(VERIFY_TMP)/distinct-half-two-core-seed-pool.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_nash_floor_candidate.py --output $(VERIFY_TMP)/nash-floor-candidate.json --random-profiles 1000
	cmp results/efx49_nash_floor_candidate_audit.json $(VERIFY_TMP)/nash-floor-candidate.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/analyze_distinct_half_conversion_dichotomy_pool.py --result results/efx49_distinct_half_conversion_dichotomy_cegar_session4.json --seed results/efx49_distinct_half_favorite_pair_rank_boundary_audit.json --add-partitions 8 --add-repairs 8 --selection diverse --output $(VERIFY_TMP)/distinct-half-conversion-dichotomy-pool.json
	cmp results/efx49_distinct_half_conversion_dichotomy_pool_analysis.json $(VERIFY_TMP)/distinct-half-conversion-dichotomy-pool.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_conversion_dichotomy_boundary.py --output $(VERIFY_TMP)/distinct-half-conversion-dichotomy-boundary.json
	cmp results/efx49_distinct_half_conversion_dichotomy_boundary_audit.json $(VERIFY_TMP)/distinct-half-conversion-dichotomy-boundary.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_three_observer_full_triple_cell.py --source results/efx49_distinct_half_favorite_pair_rank_boundary_audit.json --source results/efx49_distinct_half_conversion_dichotomy_boundary_audit.json --output $(VERIFY_TMP)/three-observer-full-triple-cell.json
	cmp results/efx49_three_observer_full_triple_cell_audit.json $(VERIFY_TMP)/three-observer-full-triple-cell.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_distinct_half_floor_core.py --core results/efx49_distinct_half_floor_minimized_core.json --theorem-audit results/efx49_distinct_half_floor_dual_encoding_audit.json --output $(VERIFY_TMP)/distinct-half-floor-core.json
	cmp results/efx49_distinct_half_floor_minimized_core_audit.json $(VERIFY_TMP)/distinct-half-floor-core.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_universal_pair_floor_lex_parking.py --output $(VERIFY_TMP)/universal-pair-floor-lex-parking.json
	cmp results/universal_pair_floor_lex_parking_audit.json $(VERIFY_TMP)/universal-pair-floor-lex-parking.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_second_orbits.py --output $(VERIFY_TMP)/real-common-second-orbits.json
	cmp results/efx49_common_favorite_second_orbits_audit.json $(VERIFY_TMP)/real-common-second-orbits.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_boundaries.py --results-dir results --output $(VERIFY_TMP)/common-favorite-boundaries.json
	cmp results/efx49_common_favorite_boundaries_audit.json $(VERIFY_TMP)/common-favorite-boundaries.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/audit_common_favorite_sufficient_cap.py --results-dir results --output $(VERIFY_TMP)/common-favorite-sufficient-cap.json
	cmp results/efx49_common_favorite_sufficient_cap_audit.json $(VERIFY_TMP)/common-favorite-sufficient-cap.json
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/test_terminal_cnf.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tracks/parkability/test_durable_campaign.py

paper:
	cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
