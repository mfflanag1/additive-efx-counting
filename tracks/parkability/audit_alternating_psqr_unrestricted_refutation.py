#!/usr/bin/env python3
"""Dual audit of the unrestricted psqr extension-or-handoff refutation."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .decide_alternating_two_safe_bundle_gate import numeric_desired
    from .run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        make_cell,
        numeric_efx,
        numeric_utilities,
        structural_solver,
    )
except ImportError:
    from decide_alternating_two_safe_bundle_gate import numeric_desired
    from run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        make_cell,
        numeric_efx,
        numeric_utilities,
        structural_solver,
    )


SCHEMA = "alternating-psqr-unrestricted-refutation-audit-v1"
PRIMARY_SIZES = (1, 1, 2, 1)
PRIMARY_ORDER = (0, 2, 3, 1)
PRIMARY_VALUES = (
    (281, 265, 32, 40, 273, 554, 546, 281),
    (283, 8, 243, 24, 12, 4, 554, 8),
    (22, 4, 10, 16, 28, 2, 255, 231),
    (6, 2, 18, 3, 28, 192, 16, 19),
)
HALF_SIZES = (2, 1, 1, 1)
HALF_ORDER = (2, 0, 1, 3)
HALF_VALUES = (
    (10, 16, 28, 22, 4, 255, 2, 231),
    (18, 3, 28, 6, 2, 16, 192, 19),
    (32, 40, 273, 281, 265, 546, 554, 281),
    (243, 24, 12, 283, 8, 554, 4, 8),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def role_data(cell, root):
    if root == 0:
        return cell["x"], cell["base_bundles"][1] + (cell["floater"],)
    if root == 2:
        return cell["y"], cell["base_bundles"][3] + (cell["floater"],)
    raise ValueError(root)


def owner_record(cell, owner):
    return {
        "allocation": {
            AGENTS[agent]: [
                cell["goods"][good]
                for good, assigned in enumerate(owner)
                if assigned == agent
            ]
            for agent in range(4)
        },
        "charity": [
            cell["goods"][good]
            for good, assigned in enumerate(owner)
            if assigned is None
        ],
    }


def pin_structural(values, cell):
    solver, symbolic, _own = structural_solver(cell)
    row_sums = tuple(sum(row) for row in values)
    solver.add(
        *(
            symbolic[agent][good] * row_sums[agent] == values[agent][good]
            for agent in range(4)
            for good in range(cell["m"])
        )
    )
    return str(solver.check())


def exhaustive_audit(values, cell, root, order):
    singleton, offer = role_data(cell, root)
    offer_set = set(offer)
    base = numeric_utilities(values, cell["base_owner"])
    base_key = tuple(base[agent] for agent in order)
    counts = {
        "allocation_count": 0,
        "unrestricted_efx_count": 0,
        "unrestricted_lex_improving_efx_count": 0,
        "anchored_candidate_count": 0,
        "anchored_efx_count": 0,
        "anchored_lex_improving_efx_count": 0,
        "desired_promoted_candidate_count": 0,
        "desired_promoted_efx_count": 0,
    }
    desired_bundles = set()
    unrestricted_examples = []
    for assignment in itertools.product(range(5), repeat=cell["m"]):
        owner = tuple(None if destination == 4 else destination for destination in assignment)
        counts["allocation_count"] += 1
        utilities = numeric_utilities(values, owner)
        efx = numeric_efx(values, owner)
        lex_improving = tuple(utilities[agent] for agent in order) > base_key
        if efx:
            counts["unrestricted_efx_count"] += 1
        if efx and lex_improving:
            counts["unrestricted_lex_improving_efx_count"] += 1
            if len(unrestricted_examples) < 3:
                unrestricted_examples.append(owner_record(cell, owner))

        root_bundle = tuple(
            good for good, assigned in enumerate(owner) if assigned == root
        )
        if root_bundle == (singleton,):
            counts["anchored_candidate_count"] += 1
            if efx:
                counts["anchored_efx_count"] += 1
            if efx and lex_improving:
                counts["anchored_lex_improving_efx_count"] += 1
        elif (
            root_bundle
            and set(root_bundle).issubset(offer_set)
            and numeric_desired(values, base, root, root_bundle)
        ):
            desired_bundles.add(root_bundle)
            counts["desired_promoted_candidate_count"] += 1
            if efx:
                counts["desired_promoted_efx_count"] += 1

    if counts["anchored_lex_improving_efx_count"] != 0:
        raise AssertionError("profile has an anchored lexicographic escape")
    if counts["desired_promoted_efx_count"] != 0:
        raise AssertionError("profile has a desired promoted-root EFX allocation")
    if counts["unrestricted_lex_improving_efx_count"] == 0:
        raise AssertionError("profile accidentally refutes unrestricted EFX improvement")
    return {
        "base_utilities": list(base),
        **counts,
        "desired_root_bundles": [
            [cell["goods"][good] for good in bundle]
            for bundle in sorted(desired_bundles)
        ],
        "unrestricted_examples": unrestricted_examples,
    }


def fixed_value_smt(values, cell, root, order):
    singleton, offer = role_data(cell, root)
    offer_set = set(offer)
    m = cell["m"]
    owner = tuple(z3.Int(f"owner_{root}_{good}") for good in range(m))
    solver = z3.SolverFor("QF_LIA")
    solver.add(*(z3.And(variable >= 0, variable <= 4) for variable in owner))
    utilities = tuple(
        z3.Sum(
            *(z3.If(owner[good] == agent, values[agent][good], 0) for good in range(m))
        )
        for agent in range(4)
    )
    bundle_values = tuple(
        tuple(
            z3.Sum(
                *(z3.If(owner[good] == target, values[observer][good], 0) for good in range(m))
            )
            for target in range(4)
        )
        for observer in range(4)
    )
    base = numeric_utilities(values, cell["base_owner"])
    anchored = z3.And(
        owner[singleton] == root,
        *(owner[good] != root for good in range(m) if good != singleton),
    )
    promoted = z3.And(
        *(owner[good] != root for good in range(m) if good not in offer_set),
        utilities[root] > base[root],
        *(
            z3.Implies(
                owner[removed] == root,
                bundle_values[observer][root] - values[observer][removed]
                <= base[observer],
            )
            for observer in range(4)
            for removed in offer
        ),
    )
    solver.add(z3.Or(anchored, promoted))
    solver.add(
        *(
            z3.Implies(
                owner[removed] == target,
                utilities[observer]
                >= bundle_values[observer][target] - values[observer][removed],
            )
            for observer in range(4)
            for target in range(4)
            for removed in range(m)
        )
    )
    solver.add(
        z3.Or(
            *(
                z3.And(
                    *(utilities[order[prefix]] == base[order[prefix]] for prefix in range(index)),
                    utilities[agent] > base[agent],
                )
                for index, agent in enumerate(order)
            )
        )
    )
    return str(solver.check())


def rotate_primary():
    agent_map = (2, 3, 0, 1)
    good_map = (2, 3, 4, 0, 1, 6, 5, 7)
    return tuple(
        tuple(PRIMARY_VALUES[agent_map[agent]][good_map[good]] for good in range(8))
        for agent in range(4)
    )


def audit():
    if rotate_primary() != HALF_VALUES:
        raise AssertionError("half-turn profile is not the exact role/good rotation")
    profiles = []
    for label, sizes, order, values in (
        ("psqr", PRIMARY_SIZES, PRIMARY_ORDER, PRIMARY_VALUES),
        ("half_turn_sprq", HALF_SIZES, HALF_ORDER, HALF_VALUES),
    ):
        cell = make_cell(sizes)
        root = order[0]
        structural_status = pin_structural(values, cell)
        if structural_status != "sat":
            raise AssertionError((label, "outside structural cell", structural_status))
        exhaustive = exhaustive_audit(values, cell, root, order)
        smt_status = fixed_value_smt(values, cell, root, order)
        if smt_status != "unsat":
            raise AssertionError((label, "SMT target finder", smt_status))
        profiles.append(
            {
                "label": label,
                "packet_sizes": list(sizes),
                "goods": list(cell["goods"]),
                "agent_order": list(order),
                "agent_order_names": [AGENTS[agent] for agent in order],
                "root": root,
                "root_name": AGENTS[root],
                "values": [list(row) for row in values],
                "structural_qf_lra_status": structural_status,
                "target_qf_lia_status": smt_status,
                "exhaustive": exhaustive,
            }
        )
    script = Path(__file__).resolve()
    return {
        "schema": SCHEMA,
        "status": "UNRESTRICTED_EXTENSION_OR_HANDOFF_REFUTED_BOTH_HALF_TURNS",
        "profiles": profiles,
        "claim_boundary": {
            "refuted": "the cap-free anchored-or-any-desired extension lemma for (p,s,q,r) and its half-turn",
            "not_refuted": "existence of EFX allocations, existence of unrestricted lexicographic EFX improvements, or complete additive EFX",
        },
        "verification": {
            "enumeration": "all 5^8 partial allocations with exact integer arithmetic",
            "independent_target_solver": "QF_LIA owner encoding",
            "structural_membership": "QF_LRA with each integer row pinned up to positive scaling",
        },
        "solver": {
            "name": "z3",
            "version": z3.get_version_string(),
        },
        "provenance": {
            "script": str(script.relative_to(script.parents[2])),
            "script_sha256": sha256(script),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        temporary = args.output.with_suffix(args.output.suffix + ".tmp")
        temporary.write_text(payload)
        temporary.replace(args.output)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
