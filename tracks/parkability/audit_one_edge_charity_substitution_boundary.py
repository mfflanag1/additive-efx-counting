#!/usr/bin/env python3
"""Independently audit the smallest corrected-form substitution boundary."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

from .analyze_rank_three_one_edge_charity_substitution import profile_analysis
from .audit_fixed_u_support_edge_three_no_go import complete_efx
from .analyze_fixed_u_four_edge_topology_cover import topology
from .decide_fixed_u_rank_three_four_edge_complete_efx import allocations_with_at_most_edges
from .run_fixed_u_full_packet_terminal_cegar import SUPPORT_STATE
from .run_fixed_u_rank_three_relation_cegar import build_rank_three_master


def run(root: Path):
    source = root / "results/fixed_u_rank_three_corrected_owner_cycle_unseeded_cegar.json"
    payload = json.loads(source.read_text())
    record = next(item for item in payload["rounds"] if item.get("values"))
    values = {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in record["values"].items()
    }

    solver, symbolic = build_rank_three_master(
        exclude_self_responses=True,
        required_owner_cycle_form=True,
    )
    for (good, observer), variable in symbolic.items():
        solver.add(variable == z3.RealVal(str(values[observer][good])))
    assert solver.check() == z3.sat

    selector = profile_analysis(record)
    assert selector["selector_candidate_count"] == 12
    assert selector["efx_witness_count"] == 0

    counts = {edge_count: 0 for edge_count in range(5)}
    topologies = set()
    for allocation in allocations_with_at_most_edges(4, SUPPORT_STATE):
        if complete_efx(values, allocation):
            graph = topology(allocation)
            counts[len(graph)] += 1
            topologies.add(graph)
    assert counts == {0: 0, 1: 0, 2: 0, 3: 0, 4: 20}
    assert len(topologies) == 11

    canonical = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    script = Path(__file__).resolve()
    theorem = root / "results/ONE_EDGE_CHARITY_SUBSTITUTION_BOUNDARY_20260813.md"
    return {
        "schema": "one-edge-charity-substitution-boundary-v1",
        "status": "RESPONSE_CORE_SUBSTITUTION_REFUTED_GENERAL_FOUR_EDGE_SURVIVES",
        "source": f"results/{source.name}",
        "source_iteration": record["iteration"],
        "source_record_sha256": hashlib.sha256(canonical).hexdigest(),
        "checks": {
            "corrected_nonself_owner_cycle_master_satisfied": True,
            "one_edge_substitution_candidate_count": selector["selector_candidate_count"],
            "one_edge_substitution_efx_count": selector["efx_witness_count"],
            "complete_efx_count_by_support_edges": {
                str(key): value for key, value in counts.items()
            },
            "four_edge_topology_count": len(topologies),
        },
        "claim_boundary": (
            "exact twelve-atom positive-rational boundary satisfying the corrected "
            "packet and nonself owner-cycle gates. It refutes only the selector "
            "that reverses three recorded response cores and replaces the fourth "
            "by charity. It has twenty complete EFX allocations on eleven other "
            "four-edge topologies, so it is not a four-edge or EFX countermodel. "
            "Full signed saturation remains unencoded."
        ),
        "provenance": {
            "z3_version": z3.get_version_string(),
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], **result["checks"]}, indent=2))


if __name__ == "__main__":
    main()
