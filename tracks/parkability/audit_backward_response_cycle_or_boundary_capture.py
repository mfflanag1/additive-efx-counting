#!/usr/bin/env python3
"""Exact audit of backward response cycles and boundary capture."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises: list[z3.BoolRef], conclusion: z3.BoolRef) -> bool:
    solver = z3.Solver()
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(root: Path) -> dict:
    A, remainder, overlap, compensation, floor = z3.Reals(
        "A remainder overlap compensation floor"
    )
    symbolic = {
        "boundary_failure_forces_overlap_capture": prove(
            [A == remainder + overlap, A > floor,
             remainder + compensation <= floor, compensation >= 0],
            overlap - compensation >= A - floor,
        ),
        "capture_is_strict": prove(
            [A == remainder + overlap, A > floor,
             remainder + compensation <= floor, compensation >= 0],
            overlap > compensation,
        ),
    }
    assert all(symbolic.values())

    owners = ("r", "q", "c", "s")
    paths = [
        path for path in itertools.permutations(owners)
        if any(path[index:index + 2] == ("r", "q") for index in range(3))
    ]
    records = []
    for path in paths:
        r_position = path.index("r")
        q_position = r_position + 1
        for source_position in range(1, 4):
            for target_position in range(source_position):
                if target_position == 0:
                    identity_class = "owner_hole_cycle"
                elif target_position == q_position:
                    identity_class = "nonhole_anchor_target_collision"
                elif source_position == r_position:
                    identity_class = "nonhole_anchor_source_release"
                else:
                    identity_class = "generic_nonhole_boundary_split"
                records.append({
                    "path": list(path),
                    "source_position": source_position,
                    "source": path[source_position],
                    "target_position": target_position,
                    "target": path[target_position],
                    "cycle_positions": list(range(target_position, source_position + 1)),
                    "boundary_source_position": target_position - 1 if target_position else None,
                    "identity_class": identity_class,
                })
    assert len(records) == 36
    counts = {
        identity_class: sum(
            record["identity_class"] == identity_class for record in records
        )
        for identity_class in sorted({record["identity_class"] for record in records})
    }
    assert counts == {
        "generic_nonhole_boundary_split": 10,
        "nonhole_anchor_source_release": 2,
        "nonhole_anchor_target_collision": 6,
        "owner_hole_cycle": 18,
    }

    script = Path(__file__).resolve()
    theorem = root / "results/BACKWARD_RESPONSE_CYCLE_OR_BOUNDARY_CAPTURE_LEMMA_20260813.md"
    dependency = root / "results/SIGNED_SURPLUS_PREFIX_RECRUITMENT_LEMMA_20260813.md"
    return {
        "schema": "backward-response-cycle-or-boundary-capture-audit-v1",
        "status": "BACKWARD_RESPONSE_REDUCED_TO_MIXED_CYCLE_PAYMENT",
        "symbolic_checks": symbolic,
        "anchored_path_count": len(paths),
        "backward_order_count": len(records),
        "identity_class_counts": counts,
        "records": records,
        "smallest_terminal": "supplier-saturated mixed-cycle observer payment",
        "claim_boundary": (
            "cap-free support classification only; mixed-cycle payment/root-q "
            "reverse inequality remains open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "dependency": str(dependency.relative_to(root)),
            "dependency_sha256": sha256(dependency),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "counts": result["identity_class_counts"],
    }, indent=2))


if __name__ == "__main__":
    main()
