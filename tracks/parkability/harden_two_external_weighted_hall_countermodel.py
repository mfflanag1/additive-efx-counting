#!/usr/bin/env python3
"""Harden the bounded two-external weighted-Hall no-closure model."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

try:
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        validate_flower_master,
    )
    from .harden_flexible_lex_basic_pi_free_countermodel import (
        basic_pi_free,
        perturb,
    )
    from .harden_flexible_lex_radius3_countermodel import live_polarity, sha256
    from .run_two_external_weighted_hall_cegar import find_closure
except ImportError:
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        validate_flower_master,
    )
    from harden_flexible_lex_basic_pi_free_countermodel import basic_pi_free, perturb
    from harden_flexible_lex_radius3_countermodel import live_polarity, sha256
    from run_two_external_weighted_hall_cegar import find_closure


def run(source_path: Path, maximum_seed: int) -> dict:
    source = json.loads(source_path.read_text())
    if source.get("status") != "sat_no_closure":
        raise ValueError("source is not a SAT no-closure result")
    source_values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in source["values"].items()
    }
    old = validate_flower_master(source_values)
    common_denominator = math.lcm(*(
        amount.denominator
        for row in source_values.values() for amount in row.values()
    ))
    atom_count = len(source_values[AGENTS[0]])
    delta_power = common_denominator.bit_length() + atom_count + 2
    delta = Fraction(1, 1 << delta_power)
    assert delta * ((1 << atom_count) - 1) < Fraction(1, 2 * common_denominator)

    for seed in range(maximum_seed):
        values = perturb(source_values, seed, delta)
        try:
            validate_flower_master(values)
        except AssertionError:
            continue
        if not live_polarity(values) or not basic_pi_free(values, old):
            continue
        closure = find_closure(values, old)
        if closure["kind"] != "NONE":
            continue
        script = Path(__file__).resolve()
        root = script.parents[2]
        return {
            "schema": "two-external-weighted-hall-hardened-countermodel-v1",
            "status": "HARDENED_NO_CLOSURE",
            "seed": seed,
            "delta": str(delta),
            "source_common_denominator": common_denominator,
            "atom_count": atom_count,
            "positive": True,
            "subset_sum_injective": True,
            "flower_master_valid": True,
            "live_polarity_valid": True,
            "basic_pi_free": True,
            "minimal_payment_packets": [
                list(packet) for packet in closure["minimal_payment_packets"]
            ],
            "examined_residual_partitions": closure["examined_partitions"],
            "response_offer_cache_size": closure["response_offer_cache_size"],
            "efx_residual_partition_count": 0,
            "internal_response_sdr_count": 0,
            "values": {
                agent: {good: str(amount) for good, amount in row.items()}
                for agent, row in values.items()
            },
            "claim_boundary": (
                "positive subset-sum-injective bounded representative flower "
                "satisfying the live polarity and basic PI-free constraints, "
                "with no EFX residual partition or internal response SDR for "
                "any minimal payment packet; generalized PI-freeness and the "
                "claimed strict-polarity contradiction are not decided"
            ),
            "provenance": {
                "source": str(source_path.relative_to(root)),
                "source_sha256": sha256(source_path),
                "script": str(script.relative_to(root)),
                "script_sha256": sha256(script),
            },
        }
    return {
        "schema": "two-external-weighted-hall-hardened-countermodel-v1",
        "status": "NO_HARDENING_FOUND",
        "maximum_seed": maximum_seed,
        "delta": str(delta),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-seed", type=int, default=10000)
    args = parser.parse_args()
    result = run(args.source.resolve(), args.maximum_seed)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "seed": result.get("seed"),
        "partitions": result.get("examined_residual_partitions"),
    }, indent=2))


if __name__ == "__main__":
    main()
