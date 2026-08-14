#!/usr/bin/env python3
"""Independent exact audit of a root-retention new-creditor countermodel."""

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
from .run_allocated_e_root_retention_new_debt_cegar import RETAINED
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


ROOT = Path(__file__).resolve().parents[2]


def run(source: Path, output: Path):
    source = source.resolve()
    payload = json.loads(source.read_text())
    assert payload["status"] == "SAT_PI_FREE_NEW_CREDITOR_DEBT"
    endpoint_source = ROOT / payload["endpoint_source"]
    endpoints = json.loads(endpoint_source.read_text())["allocations"]
    endpoint_index = payload["endpoint_index"]
    endpoint = endpoints[endpoint_index - 1]
    retained = RETAINED[endpoint_index]
    creditor = payload["creditor"]
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
    assert complete_efx(values, endpoint)

    def utility(owner, bundle):
        return sum((values[owner][good] for good in bundle), Fraction(0))

    endpoint_utilities = {owner: utility(owner, endpoint[owner]) for owner in OWNERS}
    retained_creditor_utility = utility(creditor, retained[creditor])
    assert endpoint_utilities["q"] >= 1
    assert endpoint_utilities["s"] >= 1
    assert retained_creditor_utility < 1

    result = {
        "schema": "allocated-e-root-retention-new-debt-countermodel-audit-v1",
        "status": "AUDIT_PASSED",
        "source": str(source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "endpoint_index": endpoint_index,
        "creditor": creditor,
        "master_fixed_profile_status": str(master_status),
        "full_generalized_pi_found": False,
        "full_minimal_core_counts": {
            owner: len(cores) for owner, cores in minimal.items()
        },
        "endpoint_is_efx": True,
        "endpoint_utilities": {
            owner: str(amount) for owner, amount in endpoint_utilities.items()
        },
        "retained_creditor_utility": str(retained_creditor_utility),
        "audit_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact countermodel to automatic creditor payment after root "
            "retention in the named bounded endpoint only. Complete EFX is not refuted."
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
