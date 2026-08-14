#!/usr/bin/env python3
"""Audit charity-response exclusion and the forced rank-three owner cycle."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import z3


OWNERS = ("r", "q", "d", "s")
ANCHOR = ("r", "q")
ROOT_EDGE = ("d", "q")
STRONG_WALL_EDGE = ("d", "r")


def prove(premises, conclusion):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def directed_cycles(edges):
    edge_set = set(edges)
    cycles = set()
    for size in (2, 3, 4):
        for cycle in itertools.permutations(OWNERS, size):
            if cycle[0] != min(cycle):
                continue
            if all(
                (cycle[index], cycle[(index + 1) % size]) in edge_set
                for index in range(size)
            ):
                cycles.add(frozenset(cycle))
    return cycles


def rank_three_forms():
    records = []
    for q_target in OWNERS:
        if q_target == "q":
            continue
        for s_target in OWNERS:
            if s_target in ("s", "q", q_target):
                continue
            matching = (ANCHOR, ("q", q_target), ("s", s_target))
            edges = tuple(sorted((*matching, ROOT_EDGE, STRONG_WALL_EDGE)))
            cycles = directed_cycles(edges)
            assert cycles
            records.append({
                "selected_matching": [list(edge) for edge in sorted(matching)],
                "root_facing_edge": list(ROOT_EDGE),
                "strong_wall_response_edge": list(STRONG_WALL_EDGE),
                "all_edges": [list(edge) for edge in edges],
                "owner_cycles": [sorted(cycle) for cycle in sorted(
                    cycles, key=lambda item: sorted(item)
                )],
                "shortest_cycle_length": min(map(len, cycles)),
            })
    assert len(records) == 4
    return records


def run(root: Path):
    p, base, current = z3.Reals("p base current")
    charity_exclusion = prove(
        [p > 0, p <= base, base <= current],
        z3.And(z3.Not(p > base), z3.Not(p > current)),
    )
    records = rank_three_forms()
    histogram = Counter(record["shortest_cycle_length"] for record in records)
    assert histogram == {2: 2, 3: 2}
    script = Path(__file__).resolve()
    theorem = root / "results/PAID_SINGLETON_CHARITY_RANK_THREE_OWNER_CYCLE_LEMMA_20260813.md"
    return {
        "schema": "paid-singleton-charity-rank-three-owner-cycle-v1",
        "status": "PAID_SOURCE_CHARITY_RESPONSE_EXCLUDED_AND_FIVE_EDGE_CYCLE_FORCED",
        "checks": {
            "base_safe_singleton_not_base_or_current_desired_by_paid_source": charity_exclusion,
            "rank_three_matching_forms_checked": len(records),
            "every_form_contains_owner_cycle": all(record["owner_cycles"] for record in records),
            "cycle_length_histogram": {
                str(length): count for length, count in sorted(histogram.items())
            },
        },
        "records": records,
        "exact_remaining_gate": (
            "make one forced two- or three-owner cycle release-compatible; "
            "the only cap-free obstruction is physical core overlap/full-margin "
            "capture or an outside supplier label"
        ),
        "claim_boundary": (
            "cap-free scalar and graph lemma conditional on a base-safe singleton "
            "charity token and paid represented sources; it does not constrain a "
            "sacrificed source below base and does not prove disjoint "
            "release packets or finish the four-edge complete-EFX theorem"
        ),
        "provenance": {
            "z3_version": z3.get_version_string(),
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "forms": result["checks"]["rank_three_matching_forms_checked"],
        "cycle_lengths": result["checks"]["cycle_length_histogram"],
    }, indent=2))


if __name__ == "__main__":
    main()
