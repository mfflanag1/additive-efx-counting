#!/usr/bin/env python3
"""Independent exact audit of the hardened weighted-Hall no-closure model."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

try:
    from .analyze_flexible_two_external_weighted_hall import run as census
    from .audit_flexible_lex_radius3_hardened_countermodel import subset_sum_count
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        validate_flower_master,
    )
    from .harden_flexible_lex_basic_pi_free_countermodel import basic_pi_free
    from .harden_flexible_lex_radius3_countermodel import live_polarity
except ImportError:
    from analyze_flexible_two_external_weighted_hall import run as census
    from audit_flexible_lex_radius3_hardened_countermodel import subset_sum_count
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        validate_flower_master,
    )
    from harden_flexible_lex_basic_pi_free_countermodel import basic_pi_free
    from harden_flexible_lex_radius3_countermodel import live_polarity


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(source_path: Path) -> dict:
    source = json.loads(source_path.read_text())
    if source.get("status") != "HARDENED_NO_CLOSURE":
        raise ValueError("source is not a hardened no-closure model")
    values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in source["values"].items()
    }
    old = validate_flower_master(values)
    assert live_polarity(values)
    assert basic_pi_free(values, old)
    expected_subsets = 1 << len(values[AGENTS[0]])
    subset_counts = {agent: subset_sum_count(values[agent]) for agent in AGENTS}
    assert set(subset_counts.values()) == {expected_subsets}

    exact_census = census(source_path)
    assert exact_census["status"] == "NO_CLOSURE_FOUND"
    assert exact_census["counts"].get("EFX", 0) == 0
    assert exact_census["counts"].get("INTERNAL_SDR", 0) == 0
    assert exact_census["counts"]["HALL_DEFICIENT"] == exact_census["partition_count"]
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "two-external-weighted-hall-hardened-countermodel-audit-v1",
        "status": "VERIFIED",
        "positive_additive": True,
        "flower_master_valid": True,
        "live_polarity_valid": True,
        "subset_sum_injective": True,
        "subset_sum_counts": subset_counts,
        "basic_pi_free": True,
        "minimal_payment_packets": exact_census["minimal_payment_packets"],
        "residual_partition_count": exact_census["partition_count"],
        "classification_counts": exact_census["counts"],
        "claim_boundary": (
            "solver-independent exact-Fraction verification of no EFX residual "
            "partition and no internal response SDR in a positive nondegenerate "
            "bounded flower; this refutes the two closure branches under the "
            "encoded local premises, but does not exclude a larger generalized "
            "PI component or decide the strict-polarity branch"
        ),
        "provenance": {
            "source": str(source_path.relative_to(root)),
            "source_sha256": sha256(source_path),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source.resolve())
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "partitions": result["residual_partition_count"],
        "counts": result["classification_counts"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
