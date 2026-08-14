#!/usr/bin/env python3
"""Independent exact audit of the R3 PI-free payment-menu counterprofile."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import z3

from .decide_fixed_u_rank_three_four_edge_complete_efx import (
    allocations_with_at_most_edges, provenance_holder,
)
from .decide_three_candidate_functional_payment_skeleton import TOPOLOGIES
from .decide_two_survivor_named_topology_family import allocations_supported_by, canonical
from .find_generalized_pi_cycle import find_closed_core_families
from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE, build_master
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "results/allocated_e_form2_pi_payment_atom_cegar_continuation.json"
OUTPUT = ROOT / "results/allocated_e_pi_free_payment_counterprofile_audit.json"


def parse_values(payload):
    return {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in payload["values"].items()
    }


def total(values, observer, goods):
    return sum((values[observer][good] for good in goods), Fraction(0))


def complete_efx(values, allocation):
    for observer in OWNERS:
        own = total(values, observer, allocation[observer])
        for target in OWNERS:
            if target == observer:
                continue
            entries = [values[observer][good] for good in allocation[target]]
            if entries and own < sum(entries, Fraction(0)) - min(entries):
                return False
    return True


def run(output: Path = OUTPUT):
    payload = json.loads(SOURCE.read_text())
    if payload["status"] != "SAT_PI_FREE_NO_PAID_MATCHING":
        raise AssertionError(payload["status"])
    values = parse_values(payload)

    # Independent fixed-model replay of every declared master assertion.
    solver, symbolic = build_master(2)
    for owner in OWNERS:
        for good in GOODS:
            amount = values[owner][good]
            solver.add(symbolic[good, owner] == z3.RealVal(
                f"{amount.numerator}/{amount.denominator}"
            ))
    master_status = solver.check()
    if master_status != z3.sat:
        raise AssertionError(f"fixed profile fails master: {master_status}")

    pi_witnesses, minimal = find_closed_core_families(
        values, ALLOCATED_E_BASE, maximum=None,
    )
    if pi_witnesses:
        raise AssertionError(f"profile has {len(pi_witnesses)} generalized PI families")

    paid_allocations = {}
    for topology in TOPOLOGIES[2]:
        for allocation in allocations_supported_by(topology):
            paid_allocations.setdefault(canonical(allocation), allocation)
    paid_witnesses = []
    for allocation in paid_allocations.values():
        if all(total(values, owner, allocation[owner]) >= 1 for owner in OWNERS):
            paid_witnesses.append(allocation)
    if paid_witnesses:
        raise AssertionError("canonical paid matching family is not empty")

    supplier = provenance_holder(SUPPORT_STATE)
    checked = 0
    efx_witnesses = []
    topology_counts = Counter()
    edge_counts = Counter()
    for allocation in allocations_with_at_most_edges(4, SUPPORT_STATE):
        if any(not allocation[owner] for owner in OWNERS):
            continue
        checked += 1
        if not complete_efx(values, allocation):
            continue
        edges = tuple(sorted({
            (supplier[good], owner)
            for owner in OWNERS for good in allocation[owner]
            if supplier[good] != owner
        }))
        topology_counts[edges] += 1
        edge_counts[len(edges)] += 1
        if len(efx_witnesses) < 12:
            efx_witnesses.append({
                "edge_count": len(edges),
                "edges": [list(edge) for edge in edges],
                "allocation": {
                    owner: list(allocation[owner]) for owner in OWNERS
                },
                "utilities": {
                    owner: str(total(values, owner, allocation[owner]))
                    for owner in OWNERS
                },
            })

    efx_count = sum(topology_counts.values())
    if checked != 93480 or efx_count != 78 or min(edge_counts) != 2:
        raise AssertionError((checked, efx_count, edge_counts))

    result = {
        "schema": "allocated-e-pi-free-payment-counterprofile-audit-v1",
        "status": "PAYMENT_MENU_REFUTED_FOUR_EDGE_EFX_SURVIVES",
        "solver": f"Z3 {z3.get_version_string()}",
        "fixed_master_replay": str(master_status),
        "generalized_pi_family_count": len(pi_witnesses),
        "minimal_core_counts": {owner: len(rows) for owner, rows in minimal.items()},
        "paid_matching_allocation_count_checked": len(paid_allocations),
        "paid_matching_witness_count": len(paid_witnesses),
        "unrestricted_allocation_count_checked": checked,
        "unrestricted_efx_witness_count": efx_count,
        "efx_count_by_edge_count": {
            str(count): edge_counts[count] for count in sorted(edge_counts)
        },
        "minimum_efx_edge_count": min(edge_counts),
        "distinct_efx_topology_count": len(topology_counts),
        "sample_efx_witnesses": efx_witnesses,
        "claim_boundary": (
            "Exact twelve-good R3 profile satisfying the declared allocated-E "
            "master and full generalized-PI-freeness. It refutes only the three "
            "canonical all-owner-base-payment topologies. It has 78 complete EFX "
            "allocations through at most four support edges, including two-edge "
            "witnesses, and is not a four-edge theorem countermodel."
        ),
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "audit_source": str(Path(__file__).resolve().relative_to(ROOT)),
        "audit_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
