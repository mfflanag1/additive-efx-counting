#!/usr/bin/env python3
"""Exact owner-set audit of four-owner decorated-component exhaustion."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


OWNERS = frozenset(("r", "q", "c", "s"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def powerset(values):
    values = tuple(values)
    for mask in range(1 << len(values)):
        yield frozenset(values[index] for index in range(len(values)) if mask & (1 << index))


def run(root: Path) -> dict:
    cases = 0
    violations = []
    union_sizes = {}
    for target, source, observer in itertools.permutations(OWNERS, 3):
        for target_component in powerset(OWNERS):
            if not {target, source} <= target_component:
                continue
            for observer_component in powerset(OWNERS):
                if observer not in observer_component:
                    continue
                if target_component & observer_component:
                    continue
                cases += 1
                represented = target_component | observer_component
                outside = OWNERS - represented
                union_sizes[str(len(represented))] = union_sizes.get(str(len(represented)), 0) + 1
                if len(represented) < 3 or len(outside) > 1:
                    violations.append({
                        "target": target,
                        "source": source,
                        "observer": observer,
                        "target_component": sorted(target_component),
                        "observer_component": sorted(observer_component),
                    })
                if outside and len(represented | {next(iter(outside))}) != 4:
                    violations.append({"outside_recruitment_failed": sorted(outside)})

    script = Path(__file__).resolve()
    theorem = root / "results/FOUR_OWNER_DECORATED_COMPONENT_EXHAUSTION_LEMMA_20260811.md"
    return {
        "schema": "four-owner-decorated-component-exhaustion-audit-v1",
        "status": "ALL_EXHAUSTED" if not violations else "FAILED",
        "owner_count": len(OWNERS),
        "component_cases": cases,
        "represented_union_size_counts": union_sizes,
        "violations": violations,
        "maximum_outside_owners_before_recruitment": 1,
        "outside_recruitments_before_full_union": 1,
        "remaining_gate": (
            "full-owner repeated decorated response with base-margin separator and "
            "failed sacrificed-source direct safety"
        ),
        "claim_boundary": (
            "four-owner component-union exhaustion; saturated packet inequalities, "
            "globally maximal GG countermodel, and EFX remain open"
        ),
        "provenance": {
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
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
