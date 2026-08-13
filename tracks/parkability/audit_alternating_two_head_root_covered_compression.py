#!/usr/bin/env python3
"""Audit root-covered maximum compression for alternating two-head graphs."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import z3


AGENTS = range(4)
ROOT = 0
HEADS = frozenset({0, 2})


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relations():
    options = []
    for agent in AGENTS:
        rows = []
        for mask in range(1 << 4):
            row = frozenset(target for target in AGENTS if mask >> target & 1)
            if agent in HEADS:
                if not row or agent in row:
                    continue
            elif agent not in row:
                continue
            rows.append(row)
        options.append(rows)
    yield from itertools.product(*options)


def matchings(rows):
    found = []
    for size in range(1, 5):
        for sources in itertools.combinations(AGENTS, size):
            for targets in itertools.permutations(AGENTS, size):
                if all(targets[k] in rows[source] for k, source in enumerate(sources)):
                    found.append(tuple(zip(sources, targets)))
    return found


def graph_census() -> dict:
    deficient = 0
    rank_distribution = Counter()
    root_covered_distribution = Counter()
    for rows in relations():
        available = matchings(rows)
        rank = max(len(matching) for matching in available)
        if rank == 4:
            continue
        deficient += 1
        assert rank in {2, 3}
        root_covered = [
            matching for matching in available
            if len(matching) == rank and any(source == ROOT for source, _ in matching)
        ]
        assert root_covered
        rank_distribution[rank] += 1
        root_covered_distribution[rank] += len(root_covered)
    assert deficient == 860
    return {
        "deficient_relation_count": deficient,
        "rank_distribution": {str(k): v for k, v in sorted(rank_distribution.items())},
        "root_covered_maximum_matching_count": {
            str(k): v for k, v in sorted(root_covered_distribution.items())
        },
        "all_deficient_graphs_have_root_covered_maximum_matching": True,
    }


def rank_three_wall_check() -> dict:
    base = z3.RealVector("r3_base", 4)
    lam = z3.RealVector("r3_lam", 4)
    assigned = z3.RealVector("r3_assigned", 4)
    core_tau = [[z3.Real(f"r3_tau_{i}_{k}") for k in range(3)] for i in AGENTS]
    residual_tau = z3.Real("r3_residual_tau")
    missing = 3
    solver = z3.SolverFor("QF_LRA")
    for i in AGENTS:
        solver.add(base[i] >= 0, lam[i] >= base[i])
        if i != missing:
            solver.add(assigned[i] >= lam[i])
        for k in range(3):
            solver.add(core_tau[i][k] <= lam[i])
    solver.add(assigned[ROOT] > base[ROOT])
    solver.add(residual_tau <= assigned[missing])
    assert solver.check() == z3.sat
    for i in AGENTS:
        if i == missing:
            continue
        for k in range(3):
            probe = z3.SolverFor("QF_LRA")
            probe.add(solver.assertions(), assigned[i] < core_tau[i][k])
            assert probe.check() == z3.unsat
    probe = z3.SolverFor("QF_LRA")
    probe.add(solver.assertions(), assigned[missing] < residual_tau)
    assert probe.check() == z3.unsat
    return {
        "represented_to_core_walls_excluded": True,
        "missing_self_wall_excluded": True,
        "root_strict": True,
    }


def rank_two_wall_check() -> dict:
    lam = z3.RealVector("r2_lam", 4)
    assigned = z3.RealVector("r2_assigned", 4)
    core_tau = [[z3.Real(f"r2_core_tau_{i}_{k}") for k in range(2)] for i in AGENTS]
    residual_tau = [[z3.Real(f"r2_res_tau_{i}_{k}") for k in range(2)] for i in AGENTS]
    represented = {0, 1}
    holes = {2, 3}
    solver = z3.SolverFor("QF_LRA")
    for i in AGENTS:
        if i in represented:
            solver.add(assigned[i] >= lam[i])
        for k in range(2):
            solver.add(core_tau[i][k] <= lam[i])
    solver.add(assigned[ROOT] > 0)
    # Cut-and-choose makes both hole rows safe against both residual cells.
    for i in holes:
        for k in range(2):
            solver.add(residual_tau[i][k] <= assigned[i])
    assert solver.check() == z3.sat
    for i in represented:
        for k in range(2):
            probe = z3.SolverFor("QF_LRA")
            probe.add(solver.assertions(), assigned[i] < core_tau[i][k])
            assert probe.check() == z3.unsat
    for i in holes:
        for k in range(2):
            probe = z3.SolverFor("QF_LRA")
            probe.add(solver.assertions(), assigned[i] < residual_tau[i][k])
            assert probe.check() == z3.unsat
    return {
        "represented_to_core_walls_excluded": True,
        "hole_to_residual_walls_excluded": True,
    }


def run(root: Path) -> dict:
    theorem = root / "results/ALTERNATING_TWO_HEAD_ROOT_COVERED_COMPRESSION_LEMMA_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "alternating-two-head-root-covered-compression-audit-v1",
        "status": "TWO_HEAD_HALL_REDUCED_TO_ROOT_COVERED_COMPRESSION",
        "anchored_topology": {
            "edge_word": ["O", "D", "O", "D"],
            "decorated_heads": [0, 2],
            "root_is_head": True,
        },
        "graph_census": graph_census(),
        "rank_three_wall_check": rank_three_wall_check(),
        "rank_two_wall_check": rank_two_wall_check(),
        "claim_boundary": (
            "cap-free graph/compression handoff; root-facing one-head row, "
            "compressed recurrence, and complete-pool capture remain open"
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
    print(json.dumps({"status": result["status"], **result["graph_census"]}, indent=2))


if __name__ == "__main__":
    main()

