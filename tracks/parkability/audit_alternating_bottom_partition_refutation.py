#!/usr/bin/env python3
"""Audit the full-binary refutation of the structured bottom-partition menu."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .decide_alternating_any_cross_subset_dichotomy import menu as all_cross_menu
    from .decide_alternating_any_root_subset_dichotomy import menu as repaired_menu
    from .decide_alternating_bottom_partition_dichotomy import ORDER, SIZES, menu as original_menu
    from .run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        bundles,
        make_cell,
        numeric_efx,
        numeric_utilities,
        structural_solver,
    )
except ImportError:
    from decide_alternating_any_cross_subset_dichotomy import menu as all_cross_menu
    from decide_alternating_any_root_subset_dichotomy import menu as repaired_menu
    from decide_alternating_bottom_partition_dichotomy import ORDER, SIZES, menu as original_menu
    from run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        bundles,
        make_cell,
        numeric_efx,
        numeric_utilities,
        structural_solver,
    )


SCHEMA = "alternating-structured-menu-refutation-audit-v2"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def lex_dominates(values, cell, owner) -> bool:
    base = numeric_utilities(values, cell["base_owner"])
    rival = numeric_utilities(values, owner)
    return tuple(rival[agent] for agent in ORDER) > tuple(base[agent] for agent in ORDER)


def rooted_owners(cell):
    root_good = cell["x"]
    remaining = tuple(good for good in range(cell["m"]) if good != root_good)
    destinations = (1, 2, 3, None)
    for assignment in itertools.product(destinations, repeat=len(remaining)):
        owner = [None] * cell["m"]
        owner[root_good] = 0
        for good, destination in zip(remaining, assignment):
            owner[good] = destination
        yield tuple(owner)


def support_size(owner) -> int:
    return sum(assigned is not None for assigned in owner)


def audit(source: Path) -> dict:
    source_data = json.loads(source.read_text())
    if source_data["status"] not in {
        "ALL_CROSS_DICHOTOMY_REFUTED",
        "STRUCTURED_DICHOTOMY_REFUTED",
        "REPAIRED_DICHOTOMY_REFUTED",
    }:
        raise AssertionError("source is not a SAT refutation")
    values = tuple(tuple(row) for row in source_data["values"])
    cell = make_cell(SIZES)

    solver, symbolic, _ = structural_solver(cell)
    solver.add(
        *(
            symbolic[agent][good] * sum(values[agent]) == values[agent][good]
            for agent in range(4)
            for good in range(cell["m"])
        )
    )
    if solver.check() != z3.sat:
        raise AssertionError("integerized profile is outside the structural cell")

    if source_data["status"] == "STRUCTURED_DICHOTOMY_REFUTED":
        structured = original_menu(cell)
    elif source_data["status"] == "REPAIRED_DICHOTOMY_REFUTED":
        structured = repaired_menu(cell)
    else:
        structured = all_cross_menu(cell)
    structured_escapes = [
        allocation
        for _, allocation in structured
        if numeric_efx(values, allocation) and lex_dominates(values, cell, allocation)
    ]
    if structured_escapes:
        raise AssertionError(("structured escape", structured_escapes[0]))

    rooted_efx_count = 0
    rooted_dominating_count = 0
    best_support = None
    minimum_support_escapes = []
    menu_allocations = {allocation for _, allocation in structured}
    outside_menu_count = 0
    return_r_y_count = 0
    anchor_s_y_count = 0
    singleton_return_union_count = 0
    for allocation in rooted_owners(cell):
        if not numeric_efx(values, allocation):
            continue
        rooted_efx_count += 1
        if not lex_dominates(values, cell, allocation):
            continue
        rooted_dominating_count += 1
        if allocation not in menu_allocations:
            outside_menu_count += 1
        assigned = bundles(allocation)
        return_r_y = assigned[1] == (cell["y"],)
        anchor_s_y = assigned[2] == (cell["y"],)
        return_r_y_count += int(return_r_y)
        anchor_s_y_count += int(anchor_s_y)
        singleton_return_union_count += int(return_r_y or anchor_s_y)
        size = support_size(allocation)
        if best_support is None or size < best_support:
            best_support = size
            minimum_support_escapes = [allocation]
        elif size == best_support and len(minimum_support_escapes) < 32:
            minimum_support_escapes.append(allocation)

    script = Path(__file__).resolve()
    return {
        "schema": SCHEMA,
        "status": "STRUCTURED_MENU_REFUTED_BUT_ROOTED_ESCAPES_EXIST"
        if rooted_dominating_count
        else "EXTERNAL_OBSERVER_LEMMA_REFUTED_FULL_BINARY_CELL",
        "packet_sizes": list(SIZES),
        "goods": list(cell["goods"]),
        "agent_order": list(ORDER),
        "agent_order_names": [AGENTS[agent] for agent in ORDER],
        "values": [list(row) for row in values],
        "structured_menu_size": len(structured),
        "structured_efx_lex_escape_count": 0,
        "rooted_candidate_count": 4 ** (cell["m"] - 1),
        "rooted_efx_count": rooted_efx_count,
        "rooted_lex_escape_count": rooted_dominating_count,
        "rooted_lex_escapes_outside_menu": outside_menu_count,
        "rooted_escapes_returning_r_to_y": return_r_y_count,
        "rooted_escapes_anchoring_s_at_y": anchor_s_y_count,
        "rooted_escapes_in_singleton_return_union": singleton_return_union_count,
        "minimum_allocated_good_count": best_support,
        "minimum_support_escapes": [
            {
                "owner_by_good": list(allocation),
                "bundles": {
                    AGENTS[agent]: [cell["goods"][good] for good in assigned]
                    for agent, assigned in enumerate(bundles(allocation))
                },
                "utilities": list(numeric_utilities(values, allocation)),
            }
            for allocation in minimum_support_escapes
        ],
        "claim_boundary": {
            "proved": "the frozen profile refutes the 112-allocation structured menu",
            "not_refuted": "the full rooted external-observer lemma when rooted escapes exist",
        },
        "solver": {
            "name": "z3",
            "version": z3.get_version_string(),
            "logic": "QF_LRA",
        },
        "provenance": {
            "script": str(script.relative_to(script.parents[2])),
            "script_sha256": sha256(script),
            "source": str(source),
            "source_sha256": sha256(source),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.source)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(args.output)
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "status",
                    "rooted_efx_count",
                    "rooted_lex_escape_count",
                    "minimum_allocated_good_count",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
