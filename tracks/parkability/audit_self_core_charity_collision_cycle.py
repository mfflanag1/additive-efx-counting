#!/usr/bin/env python3
"""Exact finite audit for the self-core to charity-collision cycle lemma."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]


def cycles(function):
    found = set()
    n = len(function)
    for start in range(n):
        order = []
        position = {}
        current = start
        while current not in position:
            position[current] = len(order)
            order.append(current)
            current = function[current]
        cycle = order[position[current]:]
        rotations = [tuple(cycle[i:] + cycle[:i]) for i in range(len(cycle))]
        found.add(min(rotations))
    return tuple(sorted(found))


def run(output: Path):
    function_counts = {}
    cycle_length_counts = {}
    overlap_cases = 0
    for n in range(2, 5):
        functions = 0
        lengths = {}
        for function in itertools.product(range(n), repeat=n):
            if any(function[i] == i for i in range(n)):
                continue
            functions += 1
            found = cycles(function)
            assert found
            for cycle in found:
                assert len(cycle) >= 2
                assert all(function[cycle[i]] == cycle[(i + 1) % len(cycle)]
                           for i in range(len(cycle)))
                lengths[len(cycle)] = lengths.get(len(cycle), 0) + 1

                # Each target has a private token and an arbitrary subset of
                # three shared-charity tokens. Any cross-target intersection
                # is therefore confined to charity.
                charity = {f"c{k}" for k in range(3)}
                choices = tuple(
                    set(combo)
                    for size in range(4)
                    for combo in itertools.combinations(charity, size)
                )
                for selected in itertools.product(choices, repeat=len(cycle)):
                    cores = [set(part) | {f"x{owner}"}
                             for owner, part in zip(cycle, selected)]
                    for left, right in itertools.combinations(cores, 2):
                        assert left & right <= charity
                        overlap_cases += 1
        function_counts[str(n)] = functions
        cycle_length_counts[str(n)] = {str(k): v for k, v in sorted(lengths.items())}

    pivotal_audit = {}
    for arity in range(1, 9):
        values = [z3.Real(f"pivotal_{arity}_{i}") for i in range(arity)]
        total = z3.Sum(*values)
        base = [value > 0 for value in values]
        base.append(total > 1)
        base.extend(total - value <= 1 for value in values)
        solver = z3.SolverFor("QF_LRA")
        solver.add(*base, z3.Or(*(value < total - 1 for value in values)))
        lower_status = solver.check()
        assert lower_status == z3.unsat
        solver = z3.SolverFor("QF_LRA")
        solver.add(*base, total - 1 <= 0)
        slack_status = solver.check()
        assert slack_status == z3.unsat
        pivotal_audit[str(arity)] = {
            "all_goods_cover_strict_desire_margin": str(lower_status),
            "strict_margin_positive": str(slack_status),
        }

    result = {
        "schema": "self-core-charity-collision-cycle-audit-v1",
        "status": "AUDIT_PASSED",
        "fixed_point_free_function_counts": function_counts,
        "cycle_length_counts": cycle_length_counts,
        "overlap_localization_cases": overlap_cases,
        "pivotal_minimality_audit": pivotal_audit,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Audits the finite functional-graph, private-support overlap, and "
            "minimal-core pivotality components. The existence and common safety "
            "of globally minimal desired cores are proved analytically."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
