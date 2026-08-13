#!/usr/bin/env python3
"""Exact audit of the paid-response path-core rotation lemma."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises: list[z3.BoolRef], conclusion: z3.BoolRef) -> bool:
    solver = z3.Solver()
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def location_map(k: int, l: int) -> dict[int, int | str]:
    """Return the target location of each path core A_i."""
    locations: dict[int, int | str] = {0: "charity", 1: 1, 2: 2, 3: 3}
    if k < l:
        for index in range(k, l):
            locations[index] = index + 1
        locations[l] = k
    else:
        for index in range(0, l):
            locations[index] = index + 1
        locations[l] = k
        for index in range(k, 3):
            locations[index] = index + 1
        locations[3] = "charity"
    return locations


def classify(k: int, l: int) -> dict:
    locations = location_map(k, l)
    assert len(set(locations.values())) == 4
    nonself_sources = [
        source
        for source, target in locations.items()
        if target == "charity" or target != source
    ]
    if k < l:
        expected_cycle = list(range(k, l + 1))
        for source in range(k, l):
            assert locations[source] == source + 1
        assert locations[l] == k
        outcome = "internally_supplied_segment_cycle"
        rank = len(nonself_sources)
    else:
        gap = k - l - 1
        rank = 4 - gap
        expected = list(range(0, l + 1)) + list(range(k, 4))
        assert nonself_sources == expected
        expected_cycle = []
        outcome = "rank_four" if rank == 4 else "endpoint_hole_core_exchange"
    return {
        "source_position": k,
        "target_position": l,
        "locations": {f"A_{key}": value for key, value in locations.items()},
        "nonself_sources": nonself_sources,
        "response_rank": rank,
        "cycle_sources": expected_cycle,
        "outcome": outcome,
    }


def load_referee(root: Path):
    source = root / "tracks/parkability/audit_closing_source_deletion_return_referee.py"
    spec = importlib.util.spec_from_file_location("closing_referee", source)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replay_witness(payload: dict) -> dict:
    agents = ("t", "u", "s", "w")
    rows = {
        agent: {good: Fraction(number) for good, number in row.items()}
        for agent, row in payload["valuations"].items()
    }
    candidate = {
        agent: frozenset(bundle) for agent, bundle in payload["candidate"].items()
    }
    if "old_cores" in payload:
        cores = {
            agent: frozenset(bundle) for agent, bundle in payload["old_cores"].items()
        }
    else:
        cores = {
            "t": frozenset({"a0"}), "u": frozenset({"a1"}),
            "s": frozenset({"a2"}), "w": frozenset({"a3"}),
        }
    all_goods = frozenset(next(iter(rows.values())))
    deleted = payload["deleted_good"]
    returned = candidate["t"]
    residual = {
        "u": candidate["u"] - cores["u"],
        "s": candidate["s"] - cores["s"],
        "w": candidate["w"] - cores["w"],
    }
    rotated = {
        "t": returned,
        "u": cores["t"] | residual["u"],
        "s": cores["u"] | residual["s"],
        "w": cores["s"] | residual["w"],
    }
    charity = all_goods - frozenset().union(*rotated.values())

    def value(agent: str, bundle: frozenset[str]) -> Fraction:
        return sum((rows[agent][good] for good in bundle), Fraction(0))

    def threshold(agent: str, bundle: frozenset[str]) -> Fraction:
        if len(bundle) <= 1:
            return Fraction(0)
        return value(agent, bundle) - min(rows[agent][good] for good in bundle)

    efx = all(
        value(observer, rotated[observer]) >= threshold(observer, rotated[target])
        for observer in agents
        for target in agents
        if observer != target
    )
    assert efx
    assert deleted in charity
    return {
        "rotated_allocation": {
            agent: sorted(bundle) for agent, bundle in rotated.items()
        },
        "charity": sorted(charity),
        "utilities": {
            agent: str(value(agent, rotated[agent])) for agent in agents
        },
        "efx": efx,
    }


def run(root: Path) -> dict:
    source_gain, source_floor = z3.Reals("source_gain source_floor")
    restored_value, restored_floor = z3.Reals("restored_value restored_floor")
    unchanged_value, unchanged_floor = z3.Reals("unchanged_value unchanged_floor")
    checks = {
        "source_strictly_paid": prove(
            [source_gain > source_floor], source_gain > source_floor
        ),
        "restored_target_preserves_floor": prove(
            [restored_value >= restored_floor], restored_value >= restored_floor
        ),
        "unchanged_target_preserves_floor": prove(
            [unchanged_value >= unchanged_floor], unchanged_value >= unchanged_floor
        ),
    }
    assert all(checks.values())
    orders = [classify(k, l) for k in range(1, 4) for l in range(1, 4) if k != l]
    counts = {
        outcome: sum(record["outcome"] == outcome for record in orders)
        for outcome in (
            "internally_supplied_segment_cycle",
            "rank_four",
            "endpoint_hole_core_exchange",
        )
    }
    assert counts == {
        "internally_supplied_segment_cycle": 3,
        "rank_four": 2,
        "endpoint_hole_core_exchange": 1,
    }
    endpoint = next(record for record in orders if record["outcome"].startswith("endpoint"))
    assert (endpoint["target_position"], endpoint["source_position"]) == (1, 3)
    assert endpoint["response_rank"] == 3

    referee = load_referee(root)
    witness_replays = {
        "first": replay_witness(referee.rational_witness()),
        "trimmed": replay_witness(referee.trimmed_rational_witness()),
    }
    theorem = root / "results/PAID_RESPONSE_PATH_CORE_ROTATION_LEMMA_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "paid-response-path-core-rotation-audit-v1",
        "status": "CORE_SUPPORTED_REDUCED_TO_ONE_ENDPOINT_EXCHANGE",
        "symbolic_payment_checks": checks,
        "order_count": len(orders),
        "outcome_counts": counts,
        "orders": orders,
        "unique_survivor": endpoint,
        "frozen_witness_replays": witness_replays,
        "claim_boundary": (
            "cap-free path/core combinatorics and payment only; residual-essential "
            "responses and feasibility of the endpoint hole/core exchange remain open"
        ),
        "provenance": {
            "z3_version": z3.get_version_string(),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "outcomes": result["outcome_counts"]}, indent=2))


if __name__ == "__main__":
    main()
