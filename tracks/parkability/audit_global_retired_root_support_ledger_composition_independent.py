#!/usr/bin/env python3
"""Independent finite signed-state replay of global ledger normalization.

This implementation imports neither the primary composition audit nor the
collision audit. It exhausts all allocations of three labeled goods among
four owners and charity and every proposed reassignment/ledger mask.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


OWNERS = range(4)
CHARITY = 4
GOODS = range(3)
LOCATIONS = range(5)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def masks(allocation: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sum(1 << g for g in GOODS if allocation[g] == owner)
        for owner in OWNERS
    )


def value(owner: int, mask: int) -> int:
    return sum((owner + 2) * (g + 1) + g * g + 1 for g in GOODS if mask >> g & 1)


def run(repo: Path) -> dict:
    allocations = list(itertools.product(LOCATIONS, repeat=len(tuple(GOODS))))

    reconstruction_pairs = 0
    seen: dict[tuple[tuple[int, ...], tuple[tuple[int, int], ...]], tuple[int, ...]] = {}
    for base in allocations:
        base_masks = masks(base)
        for current in allocations:
            current_masks = masks(current)
            signed = tuple(
                (current_masks[i] & ~base_masks[i], base_masks[i] & ~current_masks[i])
                for i in OWNERS
            )
            rebuilt = tuple((base_masks[i] & ~signed[i][1]) | signed[i][0] for i in OWNERS)
            assert rebuilt == current_masks
            charity = sum(1 << g for g in GOODS if current[g] == CHARITY)
            assert charity == ((1 << len(tuple(GOODS))) - 1) & ~sum(rebuilt)
            key = (base, signed)
            if key in seen:
                assert seen[key] == current
            seen[key] = current
            reconstruction_pairs += 1

    normalization_cases = 0
    collision_cases = 0
    capture_cases = 0
    equality_critical_cases = 0
    for current in allocations:
        current_masks = masks(current)
        for proposed in allocations:
            proposed_masks = masks(proposed)
            for ledger_mask in range(1 << len(tuple(GOODS))):
                normalized = list(proposed)
                for g in GOODS:
                    if ledger_mask >> g & 1 and proposed[g] != current[g]:
                        normalized[g] = current[g]
                normalized_tuple = tuple(normalized)
                assert len(normalized_tuple) == len(tuple(GOODS))
                assert all(location in LOCATIONS for location in normalized_tuple)
                normalized_masks = masks(normalized_tuple)
                normalization_cases += 1

                for recipient in OWNERS:
                    moved_in = proposed_masks[recipient] & ledger_mask & ~current_masks[recipient]
                    if moved_in == 0:
                        continue
                    collision_cases += 1
                    original_value = value(recipient, proposed_masks[recipient])
                    reduced_value = value(recipient, normalized_masks[recipient])
                    floor = value(recipient, current_masks[recipient])
                    if reduced_value < original_value:
                        # Independently instantiate the weak protected floor
                        # at the original cell value. Cancellation makes this
                        # cell strictly underpaid without creating a strict
                        # response above that floor.
                        equality_critical_cases += 1
                        all_removed = proposed_masks[recipient] & ~normalized_masks[recipient]
                        assert value(recipient, all_removed) > 0
                    if original_value > floor and reduced_value <= floor:
                        capture_cases += 1
                        moved_value = value(recipient, moved_in)
                        # The recipient can simultaneously regain a ledger
                        # good that the proposal moved out. Hence removed
                        # incoming value need only dominate, not equal, the
                        # net cell-value loss.
                        all_removed = proposed_masks[recipient] & ~normalized_masks[recipient]
                        assert value(recipient, all_removed) >= original_value - reduced_value
                        assert value(recipient, all_removed) >= original_value - floor
                        assert moved_value > 0

    theorem = repo / "results/GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_COMPOSITION_THEOREM_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "global-retired-root-support-ledger-composition-independent-audit-v1",
        "status": "INDEPENDENT_SIGNED_STATE_AND_NORMALIZATION_REPLAY_PASSED",
        "goods": len(tuple(GOODS)),
        "owners": len(tuple(OWNERS)),
        "allocations": len(allocations),
        "signed_reconstruction_pairs": reconstruction_pairs,
        "normalization_cases": normalization_cases,
        "retired_transfer_collision_cases": collision_cases,
        "failed_floor_capture_cases": capture_cases,
        "weak_floor_equality_critical_cases": equality_critical_cases,
        "physical_conservation": True,
        "signed_reconstruction_injective": True,
        "semantic_note": (
            "finite labeled-good replay independently validates state identity, "
            "cancellation conservation, and capture accounting; the cap-free "
            "G0-G10 composition is the manuscript argument"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    result = run(repo)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "normalization_cases": result["normalization_cases"],
        "capture_cases": result["failed_floor_capture_cases"],
    }, indent=2))


if __name__ == "__main__":
    main()
