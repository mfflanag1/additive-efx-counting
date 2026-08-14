#!/usr/bin/env python3
"""Independent exact audit of the endpoint-6 one-packet repair no-go."""

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
from .run_allocated_e_endpoint6_one_packet_repair_cegar import repair_allocations
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


ROOT = Path(__file__).resolve().parents[2]


def run(source: Path, output: Path):
    source = source.resolve()
    payload = json.loads(source.read_text())
    assert payload["status"] == "SAT_PI_FREE_NO_ONE_PACKET_REPAIR"
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

    repair_diagnostics = []
    for donor, packet, allocation in repair_allocations():
        is_efx = complete_efx(values, allocation)
        assert not is_efx
        repair_diagnostics.append({
            "donor": donor,
            "packet": list(packet),
            "is_efx": is_efx,
        })
    assert len(repair_diagnostics) == payload["repair_count"] == 17

    result = {
        "schema": "allocated-e-endpoint6-one-packet-repair-countermodel-audit-v1",
        "status": "AUDIT_PASSED",
        "source": str(source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "master_fixed_profile_status": str(master_status),
        "full_generalized_pi_found": False,
        "full_minimal_core_counts": {
            owner: len(cores) for owner, cores in minimal.items()
        },
        "endpoint6_is_efx": True,
        "repair_count": len(repair_diagnostics),
        "all_repairs_non_efx": True,
        "repair_diagnostics": repair_diagnostics,
        "audit_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact bounded countermodel to the 17 declared one-target-to-q "
            "repairs. It does not refute coordinated or cap-free GG operations."
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
