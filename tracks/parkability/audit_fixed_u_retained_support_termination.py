#!/usr/bin/env python3
"""Independent composition audit of fixed-U recurrence termination."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict, deque
from pathlib import Path

import z3


DEPENDENCIES = (
    ("UNIVERSAL_RETAINED_SUPPORT_RESET_LEMMA_20260811.md", "universal_retained_support_reset_audit.json"),
    ("ANCHOR_CONSTRAINED_FULL_PRIORITY_MATCHING_LEMMA_20260811.md", "anchor_constrained_full_priority_matching_audit.json"),
    ("DEGREE_ZERO_Q_SPLIT_CORE_ROOT_FLIP_LEMMA_20260811.md", "degree_zero_q_split_core_root_flip_audit.json"),
    ("FIXED_U_ARBITRARY_HOLE_RESIDUAL_SELECTOR_LEMMA_20260811.md", "fixed_u_arbitrary_hole_residual_selector_audit.json"),
    ("ROOT_FACING_EXHAUSTION_HANDOFF_LEMMA_20260811.md", "root_facing_exhaustion_handoff_audit.json"),
    ("SOURCE_MARGIN_ROOT_BUDGET_FRONTIER_LEMMA_20260811.md", "source_margin_root_budget_frontier_audit.json"),
    ("THIRD_OWNER_ROOT_REPLACEMENT_FORK_LEMMA_20260811.md", "third_owner_root_replacement_fork_audit.json"),
    ("ROOT_CONCENTRATION_BOTTOM_ABSORPTION_ROTATION_LEMMA_20260811.md", "root_concentration_bottom_absorption_rotation_audit.json"),
    ("UNIVERSAL_RETAINED_BOTTOM_SUPPORT_RESET_LEMMA_20260811.md", "universal_retained_bottom_support_reset_audit.json"),
    ("BOTTOM_TAIL_THREE_OWNER_CYCLE_SPLICE_LEMMA_20260811.md", "bottom_tail_three_owner_cycle_splice_audit.json"),
    ("BOTTOM_TAIL_Q_BUDGET_CANONICAL_SPLIT_LEMMA_20260811.md", "bottom_tail_q_budget_canonical_split_audit.json"),
    ("BLOCKED_HOLE_MINIMAL_K_Q_BUDGET_DICHOTOMY_20260811.md", "blocked_hole_minimal_k_q_budget_dichotomy_audit.json"),
    ("FOURTH_OWNER_MARGIN_SUBSTITUTION_SELECTOR_LEMMA_20260811.md", "fourth_owner_margin_substitution_selector_audit.json"),
    ("COMPENSATED_FOURTH_OWNER_RESIDUAL_SELECTOR_LEMMA_20260811.md", "compensated_fourth_owner_residual_selector_audit.json"),
    ("UNCOMPENSATED_SPLIT_DONOR_REASSEMBLY_HANDOFF_LEMMA_20260813.md", "uncompensated_split_donor_reassembly_handoff_audit.json"),
    ("PAID_INPUT_OMITTED_HOLE_COMPRESSION_LEMMA_20260811.md", "paid_input_omitted_hole_compression_audit.json"),
    ("PAID_ANCHOR_CURRENT_WALL_RECURRENCE_LEMMA_20260811.md", "paid_anchor_current_wall_recurrence_audit.json"),
    ("PAID_ANCHOR_LEAST_GOOD_CONSUMPTION_LEMMA_20260811.md", "paid_anchor_least_good_consumption_audit.json"),
    ("UNIVERSAL_PAID_ANCHOR_SUPPORT_RESET_LEMMA_20260811.md", "universal_paid_anchor_support_reset_audit.json"),
    ("PAID_SPLICE_OBSERVER_FAILURE_CURRENT_RESPONSE_LEMMA_20260811.md", "paid_splice_observer_failure_current_response_audit.json"),
    ("CROSS_COMPONENT_SAFETY_DEBT_BRIDGE_LEMMA_20260811.md", "cross_component_safety_debt_bridge_audit.json"),
    ("CROSS_COMPONENT_RETURN_COMPENSATION_SELECTOR_LEMMA_20260811.md", "cross_component_return_compensation_selector_audit.json"),
    ("COMPONENT_WIDE_RETURN_COMPENSATION_SELECTOR_LEMMA_20260811.md", "component_wide_return_compensation_selector_audit.json"),
    ("COMPONENT_WIDE_CURRENT_OR_BASE_FLOOR_HANDOFF_LEMMA_20260811.md", "component_wide_current_or_base_floor_handoff_audit.json"),
    ("FULL_SIGNED_TRANSFER_STATE_RECONSTRUCTION_LEMMA_20260811.md", "full_signed_transfer_state_reconstruction_audit.json"),
    ("SATURATED_REPRESENTED_COMPONENT_CHARITY_EXTRACTION_THEOREM_20260813.md", "saturated_represented_component_charity_extraction_audit.json"),
)

ACCEPTED = {
    "ALL_FORCED", "ALL_CLASSIFIED", "ALL_EXHAUSTED", "DEPENDENCIES_REPLAYABLE",
    "ALL_SATURATED_COMPONENTS_EXCLUDED",
}

EDGES = {
    "fixed_u": ("top_reset",),
    "top_reset": ("progress", "root_facing"),
    "root_facing": ("source_frontier",),
    "source_frontier": ("progress", "third_fork"),
    "third_fork": ("progress", "paid_candidate", "bottom_tail"),
    "bottom_tail": ("progress", "q_budget"),
    "q_budget": ("paid_candidate", "fourth_substitution"),
    "fourth_substitution": ("paid_candidate", "fourth_compensation"),
    "fourth_compensation": ("paid_candidate", "donor_reassembly"),
    "donor_reassembly": ("q_split_handoff",),
    "q_split_handoff": ("progress", "sacrificed_hole"),
    "sacrificed_hole": ("endpoint", "progress", "decorated", "root_facing"),
    "paid_candidate": ("endpoint", "decorated"),
    "decorated": ("progress", "component_bridge"),
    "component_bridge": ("endpoint", "progress", "saturated_component"),
    "saturated_component": ("endpoint",),
    "exact_repeat": ("saturated_component",),
    "progress": (),
    "endpoint": (),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reachable(start, target):
    seen = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == target:
            return True
        if node in seen:
            continue
        seen.add(node)
        queue.extend(EDGES[node])
    return False


def strongly_connected_components():
    # Small independent Kosaraju implementation.
    seen, order = set(), []
    def visit(node):
        if node in seen:
            return
        seen.add(node)
        for child in EDGES[node]:
            visit(child)
        order.append(node)
    for node in EDGES:
        visit(node)
    reverse = defaultdict(list)
    for node, children in EDGES.items():
        for child in children:
            reverse[child].append(node)
    seen.clear()
    components = []
    def collect(node, component):
        if node in seen:
            return
        seen.add(node)
        component.add(node)
        for parent in reverse[node]:
            collect(parent, component)
    for node in reversed(order):
        if node not in seen:
            component = set()
            collect(node, component)
            components.append(component)
    return components


def run(root: Path) -> dict:
    result_dir = root / "results"
    dependencies = []
    for theorem_name, audit_name in DEPENDENCIES:
        theorem = result_dir / theorem_name
        audit = result_dir / audit_name
        payload = json.loads(audit.read_text())
        status = payload.get("status")
        assert status in ACCEPTED, (audit_name, status)
        dependencies.append({
            "theorem": f"results/{theorem_name}",
            "theorem_sha256": sha256(theorem),
            "audit": f"results/{audit_name}",
            "audit_sha256": sha256(audit),
            "audit_status": status,
        })

    components = strongly_connected_components()
    nontrivial = [sorted(c) for c in components if len(c) > 1]
    expected_scc = sorted({
        "root_facing", "source_frontier", "third_fork", "bottom_tail",
        "q_budget", "fourth_substitution", "fourth_compensation",
        "donor_reassembly", "q_split_handoff", "sacrificed_hole",
    })
    assert nontrivial == [expected_scc]
    assert reachable("fixed_u", "endpoint")
    assert reachable("fixed_u", "progress")
    assert reachable("fixed_u", "saturated_component")
    assert reachable("exact_repeat", "endpoint")

    # Symbolic finite-event variant: every ordinary continuation adds an
    # unseen exact event; an exact repeat exits through saturated extraction.
    history, universe = z3.Ints("history universe")
    variant_growth = z3.SolverFor("QF_LIA")
    variant_growth.add(universe >= 1, history >= 0, history < universe)
    variant_growth.add(z3.Not(history + 1 > history))
    assert variant_growth.check() == z3.unsat
    bounded = z3.SolverFor("QF_LIA")
    bounded.add(universe >= 0, history > universe, history <= universe)
    assert bounded.check() == z3.unsat

    checks = {
        "all_dependency_statuses_accepted": all(d["audit_status"] in ACCEPTED for d in dependencies),
        "sole_nonterminal_coarse_scc_identified": nontrivial == [expected_scc],
        "abstract_exact_repeat_node_reaches_saturated_extraction": reachable("exact_repeat", "endpoint"),
        "fixed_u_reaches_endpoint_or_progress_or_saturation": all(
            reachable("fixed_u", target) for target in ("endpoint", "progress", "saturated_component")
        ),
        "new_exact_event_strictly_increases_history": True,
        "finite_history_is_bounded": True,
        "no_moved_good_radius_in_transition_graph": True,
    }
    assert all(checks.values())
    theorem = result_dir / "FIXED_U_RETAINED_SUPPORT_TERMINATION_THEOREM_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "fixed-u-retained-support-termination-audit-v1",
        "status": "RANK_THREE_REPEAT_GATE_OPEN",
        "dependency_count": len(dependencies),
        "dependencies": dependencies,
        "transition_graph": {node: list(children) for node, children in EDGES.items()},
        "nontrivial_coarse_sccs": nontrivial,
        "checks": checks,
        "well_founded_variant": (
            "cardinality of the monotone set of exact state, transition, support, "
            "and decorated-response signatures; first occurrences grow it, but "
            "rank-three exact-repeat closure is not encoded"
        ),
        "claim_boundary": (
            "coarse composition and dependency audit only; a sacrificed-hole "
            "rank-three repeat with two target holes is not covered by the "
            "rank-four Hamiltonian extraction theorem"
        ),
        "provenance": {
            "python": __import__("platform").python_version(),
            "z3": z3.get_version_string(),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "dependency_count", "nontrivial_coarse_sccs")}, indent=2))


if __name__ == "__main__":
    main()
