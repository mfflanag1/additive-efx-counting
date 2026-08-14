#!/usr/bin/env python3
"""Independent exact audit of the endpoint-6 root-fixed completion no-go."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

from .audit_allocated_e_paid_strengthening_counterprofile import complete_efx
from .find_generalized_pi_cycle import find_closed_core_families
from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE, build_master
from .run_allocated_e_endpoint6_root_fixed_completion_cegar import root_fixed_menu
from .run_allocated_e_root_retention_new_debt_cegar import RETAINED
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


ROOT = Path(__file__).resolve().parents[2]


def run(source: Path, output: Path):
    source = source.resolve()
    payload = json.loads(source.read_text())
    assert payload["status"] == "SAT_PI_FREE_NO_ROOT_FIXED_FOUR_EDGE_EFX"
    endpoint_source = ROOT / payload["endpoint_source"]
    endpoint6 = json.loads(endpoint_source.read_text())["allocations"][5]
    values = {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in payload["values"].items()
    }

    solver, symbolic = build_master(2)
    for owner in OWNERS:
        for good in GOODS:
            solver.add(symbolic[good, owner] == z3.RealVal(str(values[owner][good])))
    master_status = solver.check()
    assert master_status == z3.sat
    witnesses, minimal = find_closed_core_families(
        values, ALLOCATED_E_BASE, maximum=1,
    )
    assert not witnesses
    assert complete_efx(values, endpoint6)

    def utility(owner, bundle):
        return sum((values[owner][good] for good in bundle), Fraction(0))

    assert utility("q", endpoint6["q"]) >= 1
    assert utility("s", endpoint6["s"]) >= 1
    assert utility("q", RETAINED[6]["q"]) < 1

    menu = root_fixed_menu()
    efx = []
    for allocation, edges in menu:
        if complete_efx(values, allocation):
            efx.append({
                "allocation": allocation,
                "edges": [list(edge) for edge in sorted(edges)],
            })
    assert len(menu) == payload["root_fixed_allocation_count"] == 6411
    assert not efx

    result = {
        "schema": "allocated-e-endpoint6-root-fixed-completion-countermodel-audit-v1",
        "status": "AUDIT_PASSED",
        "source": str(source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "master_fixed_profile_status": str(master_status),
        "full_generalized_pi_found": False,
        "full_minimal_core_counts": {
            owner: len(cores) for owner, cores in minimal.items()
        },
        "endpoint6_is_efx": True,
        "root_fixed_allocation_count": len(menu),
        "root_fixed_efx_count": len(efx),
        "audit_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact bounded countermodel to every complete four-edge allocation "
            "retaining the current root bundle. Root-changing GG operations remain open."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
