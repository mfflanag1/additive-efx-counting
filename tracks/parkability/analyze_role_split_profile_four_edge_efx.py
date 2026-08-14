#!/usr/bin/env python3
"""Enumerate exact four-edge complete-EFX endpoints for a saved profile."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from .run_allocated_e_form0_role_split_pi_cegar import (
    find_complete_efx_four_edge_endpoints, verify_complete_efx_endpoint,
)


def run(source, maximum):
    payload = json.loads(source.read_text())
    raw_values = payload.get("last_values") or payload.get("values")
    active = payload.get("last_active_goods") or payload.get("active_goods")
    if raw_values is None or active is None:
        raise ValueError("source does not contain a saved exact profile")
    values = {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in raw_values.items()
    }
    endpoints = find_complete_efx_four_edge_endpoints(
        values, active, maximum=maximum
    )
    assert all(
        verify_complete_efx_endpoint(values, active, endpoint)
        for endpoint in endpoints
    )
    edge_count_distribution = Counter(
        len(endpoint["transfer_edges"]) for endpoint in endpoints
    )
    edge_set_distribution = Counter(
        tuple(endpoint["transfer_edges"]) for endpoint in endpoints
    )
    return {
        "schema": "role-split-profile-four-edge-efx-analysis-v1",
        "status": (
            "FOUR_EDGE_COMPLETE_EFX_ENDPOINTS_FOUND"
            if endpoints else "NO_FOUR_EDGE_COMPLETE_EFX_ENDPOINT_FOUND"
        ),
        "source": f"results/{source.name}",
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "active_good_count": len(active),
        "maximum_endpoints": maximum,
        "endpoint_count": len(endpoints),
        "enumeration_truncated": len(endpoints) == maximum,
        "edge_count_distribution": {
            str(count): frequency
            for count, frequency in sorted(edge_count_distribution.items())
        },
        "edge_set_distribution": [
            {
                "edges": [list(edge) for edge in edge_set],
                "count": count,
            }
            for edge_set, count in edge_set_distribution.most_common()
        ],
        "endpoints": [
            {
                "allocation": {
                    owner: list(goods)
                    for owner, goods in endpoint["allocation"].items()
                },
                "transfer_edges": [
                    list(edge) for edge in endpoint["transfer_edges"]
                ],
            }
            for endpoint in endpoints
        ],
        "claim_boundary": (
            "Exact endpoint census for one saved rational role-split profile. "
            "A positive result excludes that profile as a countermodel but "
            "does not prove the universal role-split or cap-free theorem."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum", type=int, default=1000)
    args = parser.parse_args()
    result = run(args.source, args.maximum)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "endpoint_count": result["endpoint_count"],
        "edge_count_distribution": result["edge_count_distribution"],
        "truncated": result["enumeration_truncated"],
    }, indent=2))


if __name__ == "__main__":
    main()
