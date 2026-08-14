#!/usr/bin/env python3
"""Audit the exact R3 counterprofile to the mined functional cover."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

from .audit_fixed_u_support_edge_three_no_go import complete_efx
from .audit_two_survivor_named_topology_refutation import (
    exact_relation, named_allocations,
)
from .decide_exact_response_functional_cover_family import (
    FUNCTIONAL_COVER_TOPOLOGIES,
)
from .decide_fixed_u_rank_three_four_edge_complete_efx import (
    allocations_with_at_most_edges,
)
from .run_fixed_u_full_packet_terminal_cegar import (
    GOODS, OWNERS, SUPPORT_STATE,
)
from .run_fixed_u_rank_three_relation_cegar import build_rank_three_master


R3_RELATION = {
    ("r", "q"), ("q", "s"), ("s", "r"), ("d", "q"), ("d", "r")
}


def run(source):
    payload = json.loads(source.read_text())
    values = {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in payload["values"].items()
    }
    menu = tuple(named_allocations(FUNCTIONAL_COVER_TOPOLOGIES))
    menu_efx = sum(complete_efx(values, allocation) for allocation in menu)
    unrestricted = []
    for allocation in allocations_with_at_most_edges(4, SUPPORT_STATE):
        if any(not allocation[owner] for owner in OWNERS):
            continue
        if complete_efx(values, allocation):
            unrestricted.append(allocation)

    solver, variables = build_rank_three_master(
        exclude_self_responses=True,
        required_owner_cycle_form=True,
        exact_owner_cycle_response_relation=True,
        owner_cycle_form_index=2,
    )
    for owner in OWNERS:
        for good in GOODS:
            solver.add(variables[good, owner] == z3.RealVal(str(values[owner][good])))
    master_status = solver.check()
    relation = exact_relation(values)
    return {
        "schema": "exact-response-functional-cover-boundary-audit-v1",
        "verdict": "FOUR_TOPOLOGY_FUNCTIONAL_COVER_REFUTED_IN_R3",
        "source": f"results/{source.name}",
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "master_exact_value_replay": str(master_status),
        "exact_relation_matches_r3": relation == R3_RELATION,
        "functional_topology_count": len(FUNCTIONAL_COVER_TOPOLOGIES),
        "functional_menu_allocation_count": len(menu),
        "decision_allocation_count": payload["distinct_allocation_count"],
        "allocation_count_matches": len(menu) == payload["distinct_allocation_count"],
        "functional_menu_complete_efx_count": menu_efx,
        "unrestricted_four_edge_complete_efx_count": len(unrestricted),
        "first_unrestricted_witness": unrestricted[0] if unrestricted else None,
        "claim_boundary": (
            "exact bounded refutation of the four-topology menu mined from the "
            "25-profile census. It does not refute a dynamically enlarged "
            "topology selector, the unrestricted four-edge theorem, or the full "
            "saturated-state theorem."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source)
    script = Path(__file__).resolve()
    result["provenance"] = {
        "script": str(script.relative_to(script.parents[2])),
        "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in (
        "verdict", "master_exact_value_replay", "exact_relation_matches_r3",
        "functional_menu_complete_efx_count",
        "unrestricted_four_edge_complete_efx_count",
    )}, indent=2))


if __name__ == "__main__":
    main()
