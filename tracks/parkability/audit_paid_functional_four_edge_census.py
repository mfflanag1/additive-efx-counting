#!/usr/bin/env python3
"""Exact census of paid functional four-edge EFX witnesses."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from .audit_fixed_u_support_edge_three_no_go import complete_efx
from .decide_fixed_u_rank_three_four_edge_complete_efx import (
    allocations_with_at_most_edges,
)
from .run_fixed_u_full_packet_terminal_cegar import OWNERS, SUPPORT_STATE
from .run_fixed_u_rank_three_relation_cegar import functional_transfer


def total(values, owner, goods):
    return sum((values[owner][good] for good in goods), Fraction())


def edge_count(allocation):
    supplier = {
        good: source for source, goods in SUPPORT_STATE.items() for good in goods
    }
    return len({
        (supplier[good], recipient)
        for recipient, goods in allocation.items() if recipient != "charity"
        for good in goods if supplier[good] != recipient
    })


def analyze(source):
    payload = json.loads(source.read_text())
    menu = tuple(
        allocation for allocation in allocations_with_at_most_edges(4, SUPPORT_STATE)
        if all(allocation[owner] for owner in OWNERS)
        and functional_transfer(allocation, SUPPORT_STATE)
    )
    records = []
    for round_record in payload["rounds"]:
        if "values" not in round_record:
            continue
        values = {
            owner: {good: Fraction(amount) for good, amount in row.items()}
            for owner, row in round_record["values"].items()
        }
        functional = []
        paid = []
        for allocation in menu:
            if not complete_efx(values, allocation):
                continue
            functional.append(allocation)
            if all(total(values, owner, allocation[owner]) >= 1 for owner in OWNERS):
                paid.append(allocation)
        records.append({
            "iteration": round_record["iteration"],
            "functional_complete_efx_count": len(functional),
            "paid_functional_complete_efx_count": len(paid),
            "minimum_functional_edge_count": min(map(edge_count, functional)),
            "minimum_paid_functional_edge_count": min(map(edge_count, paid)),
            "first_paid_witness": paid[0],
        })
    return {
        "schema": "paid-functional-four-edge-exact-response-census-v1",
        "source": f"results/{source.name}",
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "profile_count": len(records),
        "functional_allocation_menu_count": len(menu),
        "all_profiles_have_paid_functional_witness": bool(records) and all(
            record["paid_functional_complete_efx_count"] > 0 for record in records
        ),
        "minimum_paid_edge_histogram": dict(sorted(Counter(
            record["minimum_paid_functional_edge_count"] for record in records
        ).items())),
        "records": records,
        "claim_boundary": (
            "exact census of recorded twelve-atom corrected-response profiles; "
            "universal success on this finite adversarial corpus is evidence, "
            "not a bounded universal theorem or a cap-free theorem"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = analyze(args.source)
    script = Path(__file__).resolve()
    result["provenance"] = {
        "script": str(script.relative_to(script.parents[2])),
        "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in (
        "profile_count", "functional_allocation_menu_count",
        "all_profiles_have_paid_functional_witness",
        "minimum_paid_edge_histogram",
    )}, indent=2))


if __name__ == "__main__":
    main()
