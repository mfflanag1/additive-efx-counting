#!/usr/bin/env python3
"""Symbolic and exact graph audit of the forward-chord split lemma."""

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
    A, remainder, overlap, freed, floor = z3.Reals(
        "A remainder overlap freed floor"
    )
    E, current, base, response_remainder, reservoir = z3.Reals(
        "E current base response_remainder reservoir"
    )
    symbolic = {
        "response_source_paid_without_old_core": prove(
            [E > current, current >= base], E > base
        ),
        "whole_core_failure_forces_capture": prove(
            [A == remainder + overlap, A > floor,
             remainder + freed <= floor, freed >= 0],
            overlap - freed >= A - floor,
        ),
        "capture_is_strict": prove(
            [A == remainder + overlap, A > floor,
             remainder + freed <= floor, freed >= 0],
            overlap > freed,
        ),
        "anchor_overlap_captures_current_response_margin": prove(
            [E == response_remainder + overlap, E > current,
             response_remainder <= current],
            overlap >= E - current,
        ),
        "whole_complete_residual_pool_failure_forces_anchor_source_capture": prove(
            [A == remainder + overlap, A > floor,
             remainder + reservoir <= floor, reservoir >= 0],
            overlap - reservoir >= A - floor,
        ),
    }
    assert all(symbolic.values())

    owners = ("r", "q", "c", "s")
    paths = [
        path for path in itertools.permutations(owners)
        if any(path[index:index + 2] == ("r", "q") for index in range(3))
    ]
    assert len(paths) == 6
    records = []
    for path in paths:
        r_position = path.index("r")
        q_position = r_position + 1
        for source_position in range(4):
            for target_position in range(source_position + 1, 4):
                adjacent = target_position == source_position + 1
                anchor_target = (
                    not adjacent and target_position == q_position
                )
                anchor_source = (
                    not adjacent and source_position == r_position
                )
                assert not (anchor_target and anchor_source)
                if adjacent:
                    identity_class = "adjacent_same_source_replacement"
                elif anchor_target:
                    identity_class = "nonadjacent_anchor_target_collision"
                elif anchor_source:
                    identity_class = "nonadjacent_anchor_source_release"
                else:
                    identity_class = "generic_nonadjacent_split"
                records.append({
                    "path": list(path),
                    "source_position": source_position,
                    "source": path[source_position],
                    "target_position": target_position,
                    "target": path[target_position],
                    "displaced_source_position": target_position - 1,
                    "displaced_source": path[target_position - 1],
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
        "adjacent_same_source_replacement": 18,
        "generic_nonadjacent_split": 6,
        "nonadjacent_anchor_source_release": 6,
        "nonadjacent_anchor_target_collision": 6,
    }

    script = Path(__file__).resolve()
    theorem = root / "results/FORWARD_CHORD_CORE_SPLIT_OR_ANCHOR_CAPTURE_LEMMA_20260813.md"
    dependency = root / "results/SIGNED_SURPLUS_PREFIX_RECRUITMENT_LEMMA_20260813.md"
    return {
        "schema": "forward-chord-core-split-or-anchor-capture-audit-v1",
        "status": "FORWARD_CHORD_REDUCED_TO_TWO_ANCHOR_INTERFACES",
        "symbolic_checks": symbolic,
        "anchored_path_count": len(paths),
        "forward_order_count": len(records),
        "identity_class_counts": counts,
        "records": records,
        "smallest_terminals": {
            "anchor_target": "nonempty response/anchor overlap hitting set",
            "anchor_source": "complete-residual-pool capture disjoint from protected anchor",
        },
        "claim_boundary": (
            "cap-free split/capture reduction only; full-pool capture "
            "and the backward GG decorated-head exchange remain open"
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
