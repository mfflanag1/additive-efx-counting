#!/usr/bin/env python3
"""Independent exact audit of the four-residual selector counterprofile."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from .audit_fixed_u_support_edge_three_no_go import complete_efx
from .decide_allocated_e_four_residual_endpoints import ENDPOINTS
from .decide_fixed_u_rank_three_four_edge_complete_efx import allocations_with_at_most_edges
from .find_generalized_pi_cycle import find_closed_core_families
from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "results" / "allocated_e_form2_four_residual_endpoint_decision.json"
DOCUMENT = ROOT / "results" / "ALLOCATED_E_FOUR_RESIDUAL_SELECTOR_REFUTATION_20260813.md"


def total(values, owner, goods):
    return sum((values[owner][good] for good in goods), Fraction())


def tail(values, owner, goods):
    rows = [values[owner][good] for good in goods]
    return sum(rows, Fraction()) - min(rows, default=Fraction())


def failure_witness(values, allocation):
    for observer in OWNERS:
        own = total(values, observer, allocation[observer])
        for target in OWNERS:
            if observer != target and own < tail(values, observer, allocation[target]):
                return {
                    "observer": observer,
                    "target": target,
                    "own": str(own),
                    "target_tail": str(tail(values, observer, allocation[target])),
                }
    return None


def audit():
    source = json.loads(SOURCE.read_text())
    assert source["status"] == "sat" and source["form_index"] == 2
    values = {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in source["values"].items()
    }
    assert all(values[owner][good] > 0 for owner in OWNERS for good in GOODS)
    for owner in OWNERS:
        assert total(values, owner, ALLOCATED_E_BASE[owner]) == 1
        assert total(values, owner, ALLOCATED_E_BASE["charity"]) <= 1
        for target in OWNERS:
            if target != owner:
                assert tail(values, owner, ALLOCATED_E_BASE[target]) <= 1

    endpoint_records = []
    for index, allocation in enumerate(ENDPOINTS):
        witness = failure_witness(values, allocation)
        assert witness is not None
        endpoint_records.append({"endpoint": index, "failure": witness})

    families, minimal = find_closed_core_families(
        values, ALLOCATED_E_BASE, maximum=None,
    )
    family_sizes = Counter(len(witness["cycle"]) for witness in families)
    assert not family_sizes[1] and not family_sizes[2]

    holder = {
        good: supplier for supplier, goods in SUPPORT_STATE.items() for good in goods
    }
    efx_counts = Counter()
    topology_counts = Counter()
    for allocation in allocations_with_at_most_edges(4, SUPPORT_STATE):
        if any(not allocation[owner] for owner in OWNERS):
            continue
        if not complete_efx(values, allocation):
            continue
        edges = tuple(sorted({
            (holder[good], target)
            for target, goods in allocation.items() for good in goods
            if holder[good] != target
        }))
        efx_counts[len(edges)] += 1
        topology_counts[edges] += 1
    assert efx_counts == Counter({3: 22, 4: 175})

    return {
        "schema": "allocated-e-four-residual-refutation-audit-v1",
        "status": "FOUR_RESIDUAL_ENDPOINTS_REFUTED_WITH_HIGHER_PI_AND_EFX_ESCAPES",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "document_sha256": hashlib.sha256(DOCUMENT.read_bytes()).hexdigest(),
        "endpoint_failures": endpoint_records,
        "minimal_desired_core_counts": {owner: len(rows) for owner, rows in minimal.items()},
        "closed_family_counts_by_size": {
            str(size): count for size, count in sorted(family_sizes.items())
        },
        "complete_efx_counts_by_edge": {
            str(size): count for size, count in sorted(efx_counts.items())
        },
        "three_edge_topology_count": sum(len(edges) == 3 for edges in topology_counts),
        "claim_boundary": (
            "Exact bounded selector refutation. The profile has higher-order "
            "generalized PI families and many unrestricted <=4-edge EFX escapes."
        ),
    }


def main():
    output = ROOT / "results" / "allocated_e_four_residual_refutation_audit.json"
    result = audit()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "families": result["closed_family_counts_by_size"],
        "efx": result["complete_efx_counts_by_edge"],
    }, indent=2))


if __name__ == "__main__":
    main()
