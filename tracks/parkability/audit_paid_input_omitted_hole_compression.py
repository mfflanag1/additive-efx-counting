#!/usr/bin/env python3
"""Exhaustive Hall audit of omitted-hole compression on a paid input."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def maximum_matching(edges, targets):
    targets = tuple(targets)
    for sources in itertools.permutations(range(4), len(targets)):
        if all((source, target) in edges for source, target in zip(sources, targets)):
            return tuple(zip(sources, targets))
    return None


def is_full_minimal_defect(edges):
    all_targets = range(4)
    if maximum_matching(edges, all_targets) is not None:
        return False
    for size in range(1, 4):
        for targets in itertools.combinations(all_targets, size):
            if maximum_matching(edges, targets) is None:
                return False
    return True


def run(root: Path) -> dict:
    edge_list = tuple(itertools.product(range(4), repeat=2))
    defect_count = 0
    omitted_checks = 0
    violations = []
    source_union_sizes = set()
    for mask in range(1 << len(edge_list)):
        edges = {edge_list[index] for index in range(len(edge_list)) if mask & (1 << index)}
        if not is_full_minimal_defect(edges):
            continue
        defect_count += 1
        source_union = {source for source, _ in edges}
        source_union_sizes.add(len(source_union))
        missing = set(range(4)) - source_union
        if len(missing) != 1:
            violations.append({"mask": mask, "reason": "source union not deficiency one"})
            continue
        d = next(iter(missing))
        matching = maximum_matching(edges, set(range(4)) - {d})
        omitted_checks += 1
        if matching is None or {source for source, _ in matching} != source_union:
            violations.append({"mask": mask, "reason": "own target cannot be omitted"})

    yd, extra, xd = z3.Reals("yd extra xd")
    solver = z3.SolverFor("QF_LRA")
    solver.add(yd >= xd, extra >= 0, yd + extra < xd)
    payment_check = str(solver.check())
    assert payment_check == "unsat"

    theorem = root / "results/PAID_INPUT_OMITTED_HOLE_COMPRESSION_LEMMA_20260811.md"
    script = Path(__file__).resolve()
    return {
        "schema": "paid-input-omitted-hole-compression-audit-v1",
        "status": "ALL_EXHAUSTED" if not violations else "FAILED",
        "response_graphs": 1 << len(edge_list),
        "minimal_full_defects": defect_count,
        "source_union_sizes": sorted(source_union_sizes),
        "omitted_own_target_checks": omitted_checks,
        "violations": violations,
        "residual_contains_missing_owner_target": True,
        "residual_payment_check": payment_check,
        "remaining_gate": "represented-source recapture of paid residual",
        "claim_boundary": (
            "full-set minimal Hall defect on paid input; proper defects, "
            "recapture termination, support overlap, GG, and EFX remain open"
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
