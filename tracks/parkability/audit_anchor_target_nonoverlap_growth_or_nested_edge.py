#!/usr/bin/env python3
"""Audit anchor-target nonoverlap growth and nested-edge conversion."""

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
    selected, support, base = z3.Reals("selected support base")
    response, current = z3.Reals("response current")
    tau_e, tau_anchor = z3.Reals("tau_e tau_anchor")
    symbolic = {
        "selected_core_plus_nonanchor_support_stays_paid": prove(
            [selected > base, support >= 0], selected + support > base
        ),
        "nonempty_positive_support_strictly_grows_source": prove(
            [support > 0], selected + support > selected
        ),
        "current_desire_implies_base_desire": prove(
            [response > current, current >= base], response > base
        ),
        "nested_core_inherits_base_safety": prove(
            [tau_e <= tau_anchor, tau_anchor <= base], tau_e <= base
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
        q_position = path.index("q")
        for source_position in range(4):
            if source_position == q_position or path[source_position] == "r":
                continue
            direction = "forward" if source_position < q_position else "backward"
            records.append({
                "path": list(path),
                "source": path[source_position],
                "source_position": source_position,
                "target": "q",
                "target_position": q_position,
                "direction": direction,
            })
    assert len(records) == 12
    direction_counts = {
        direction: sum(record["direction"] == direction for record in records)
        for direction in ("forward", "backward")
    }
    assert direction_counts == {"forward": 6, "backward": 6}

    script = Path(__file__).resolve()
    theorem = root / "results/ANCHOR_TARGET_NONOVERLAP_GROWTH_OR_NESTED_EDGE_LEMMA_20260813.md"
    dependencies = [
        root / "results/FORWARD_CHORD_CORE_SPLIT_OR_ANCHOR_CAPTURE_LEMMA_20260813.md",
        root / "results/BACKWARD_RESPONSE_CYCLE_OR_BOUNDARY_CAPTURE_LEMMA_20260813.md",
    ]
    return {
        "schema": "anchor-target-nonoverlap-growth-or-nested-edge-audit-v1",
        "status": "ANCHOR_TARGET_INEQUALITY_ELIMINATED_TO_NESTED_EDGE",
        "symbolic_checks": symbolic,
        "anchor_target_order_count": len(records),
        "direction_counts": direction_counts,
        "records": records,
        "smallest_terminal": "old nested root-facing response edge",
        "claim_boundary": (
            "q-target overlap eliminated as surplus inequality; root-facing "
            "handoff and root-sourced complete-pool capture remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "dependencies": [
                {"path": str(path.relative_to(root)), "sha256": sha256(path)}
                for path in dependencies
            ],
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
        "direction_counts": result["direction_counts"],
    }, indent=2))


if __name__ == "__main__":
    main()
