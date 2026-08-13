#!/usr/bin/env python3
"""Audit the one-head nonroot compression-star handoff."""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path

import z3


AGENTS = ("r", "q", "a", "b")
ROOT = "r"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def nonempty_subsets(items):
    for size in range(1, len(items) + 1):
        yield from combinations(items, size)


def graph_census() -> dict:
    records = []
    for head in AGENTS:
        targets = tuple(agent for agent in AGENTS if agent != head)
        for row in nonempty_subsets(targets):
            nonroot = tuple(target for target in row if target != ROOT)
            handoff = bool(nonroot)
            root_facing = head != ROOT and row == (ROOT,)
            assert handoff != root_facing
            records.append({
                "head": head,
                "accepted_targets": list(row),
                "nonroot_handoff": handoff,
                "root_facing": root_facing,
            })
    assert len(records) == 28
    assert sum(record["nonroot_handoff"] for record in records) == 25
    assert sum(record["root_facing"] for record in records) == 3
    return {
        "row_count": len(records),
        "nonroot_handoff_count": sum(record["nonroot_handoff"] for record in records),
        "root_facing_count": sum(record["root_facing"] for record in records),
        "root_facing_rows": [record for record in records if record["root_facing"]],
    }


def symbolic_checks() -> dict:
    checked = 0
    for head in AGENTS:
        for target in AGENTS:
            if target in {head, ROOT}:
                continue

            base = {i: z3.Real(f"base_{head}_{target}_{i}") for i in AGENTS}
            own = {i: z3.Real(f"own_{head}_{target}_{i}") for i in AGENTS}
            lam = {i: z3.Real(f"lam_{head}_{target}_{i}") for i in AGENTS}
            assigned = {i: z3.Real(f"assigned_{head}_{target}_{i}") for i in AGENTS}
            residual = z3.Real(f"residual_{head}_{target}")
            residual_tau = z3.Real(f"residual_tau_{head}_{target}")
            core_tau = {
                (i, k): z3.Real(f"tau_{head}_{target}_{i}_{k}")
                for i in AGENTS for k in range(3)
            }

            solver = z3.SolverFor("QF_LRA")
            for i in AGENTS:
                solver.add(base[i] >= 0, own[i] > base[i], lam[i] >= base[i])
                if i == head:
                    solver.add(lam[i] > own[i], assigned[i] >= lam[i])
                elif i == target:
                    solver.add(own[i] >= lam[i], assigned[i] == residual)
                else:
                    solver.add(own[i] >= lam[i], assigned[i] == own[i])
                for k in range(3):
                    solver.add(core_tau[i, k] <= lam[i])
            solver.add(residual_tau <= residual)
            assert solver.check() == z3.sat

            represented = tuple(i for i in AGENTS if i != target)
            # No represented owner can fail against a selected core.
            for i in represented:
                for k in range(3):
                    probe = z3.SolverFor("QF_LRA")
                    probe.add(solver.assertions(), assigned[i] < core_tau[i, k])
                    assert probe.check() == z3.unsat
            # The missing owner cannot fail against her own residual.
            probe = z3.SolverFor("QF_LRA")
            probe.add(solver.assertions(), assigned[target] < residual_tau)
            assert probe.check() == z3.unsat
            # The root is represented and strictly above the base.
            assert ROOT != target
            probe = z3.SolverFor("QF_LRA")
            probe.add(solver.assertions(), z3.Not(assigned[ROOT] > base[ROOT]))
            assert probe.check() == z3.unsat
            checked += 1
    assert checked == 9
    return {
        "head_target_interfaces": checked,
        "represented_core_wall_excluded": True,
        "missing_self_residual_wall_excluded": True,
        "root_strictly_improved": True,
    }


def run(root: Path) -> dict:
    theorem = root / "results/ONE_HEAD_NONROOT_COMPRESSION_STAR_HANDOFF_LEMMA_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "one-head-nonroot-compression-star-handoff-audit-v1",
        "status": "ONE_HEAD_REDUCED_TO_ROOT_FACING_OR_COMPRESSION_STAR",
        "graph_census": graph_census(),
        "symbolic_checks": symbolic_checks(),
        "claim_boundary": (
            "cap-free one-head handoff; compressed-star recurrence, root-facing "
            "row, two-head Hall cut, and complete-pool capture remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
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
        **result["graph_census"],
    }, indent=2))


if __name__ == "__main__":
    main()

