#!/usr/bin/env python3
"""Replay the exact refutations of the response-derived topology selector."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import z3

try:
    from .audit_fixed_u_support_edge_three_no_go import complete_efx
    from .decide_fixed_u_rank_three_four_edge_complete_efx import (
        allocations_with_at_most_edges,
    )
    from .run_fixed_u_full_packet_terminal_cegar import (
        BASE, GOODS, OWNERS, RECIPIENTS, SUPPORT_STATE,
    )
    from .run_fixed_u_rank_three_relation_cegar import build_rank_three_master
    from .run_full_capture_rank_three_cegar import ordinary_pi_free_constraints
except ImportError:
    from audit_fixed_u_support_edge_three_no_go import complete_efx
    from decide_fixed_u_rank_three_four_edge_complete_efx import (
        allocations_with_at_most_edges,
    )
    from run_fixed_u_full_packet_terminal_cegar import (
        BASE, GOODS, OWNERS, RECIPIENTS, SUPPORT_STATE,
    )
    from run_fixed_u_rank_three_relation_cegar import build_rank_three_master
    from run_full_capture_rank_three_cegar import ordinary_pi_free_constraints


R2 = (
    (("d", "s"), ("r", "d"), ("q", "r"), ("charity", "q")),
    (("d", "s"), ("q", "d"), ("r", "q"), ("charity", "r")),
    (("q", "r"), ("r", "q"), ("r", "d"), ("charity", "s")),
    (("q", "r"), ("r", "q"), ("q", "d"), ("charity", "s")),
    (("q", "r"), ("r", "q"), ("d", "s"), ("charity", "d")),
)


CYCLE = (("r", "q"), ("q", "s"), ("s", "r"))


def reverse(responses, recipient):
    return tuple((target, source) for source, target in responses) + (
        ("charity", recipient),
    )


R3 = (
    (("r", "d"), ("q", "r"), ("s", "q"), ("charity", "s")),
    (("q", "d"), ("s", "q"), ("r", "s"), ("charity", "r")),
    *(reverse(
        tuple(edge for edge in CYCLE if edge[0] != omitted) + (("d", target),),
        omitted,
    ) for target in ("r", "q") for omitted in ("r", "q", "s")),
    (("q", "r"), ("s", "q"), ("r", "s"), ("charity", "d")),
)


def total(values, observer, goods):
    return sum((values[observer][good] for good in goods), Fraction())


def tail(values, observer, goods):
    goods = tuple(goods)
    return total(values, observer, goods) - min(
        (values[observer][good] for good in goods), default=Fraction()
    )


def response(values, source, target):
    current = {
        owner: total(values, owner, SUPPORT_STATE[owner]) for owner in OWNERS
    }
    goods = SUPPORT_STATE[target]
    for size in range(1, len(goods) + 1):
        for subset in itertools.combinations(goods, size):
            if total(values, source, subset) > 1 and all(
                tail(values, observer, subset) <= 1 for observer in OWNERS
            ):
                return True
            if total(values, source, subset) > current[source] and all(
                tail(values, observer, subset) <= current[observer]
                for observer in OWNERS
            ):
                return True
    return False


def exact_relation(values):
    targets = (*OWNERS, "charity")
    return {
        (source, target)
        for source in OWNERS for target in targets if source != target
        if response(values, source, target)
    }


def ordinary_relation(values):
    result = set()
    for source in OWNERS:
        for target in OWNERS:
            if source == target:
                continue
            for size in range(1, len(BASE[target]) + 1):
                for subset in itertools.combinations(BASE[target], size):
                    if total(values, source, subset) > 1 and all(
                        tail(values, observer, subset) <= 1 for observer in OWNERS
                    ):
                        result.add((source, target))
    return result


def ordinary_cycles(edges):
    result = []
    for length in range(2, len(OWNERS) + 1):
        for subset in itertools.combinations(OWNERS, length):
            anchor = min(subset)
            for tail_order in itertools.permutations(
                    tuple(owner for owner in subset if owner != anchor)):
                cycle = (anchor, *tail_order)
                if all((cycle[index], cycle[(index + 1) % length]) in edges
                       for index in range(length)):
                    result.append(cycle)
    return result


def named_allocations(topologies):
    supplier = {
        good: source for source, goods in SUPPORT_STATE.items() for good in goods
    }
    seen = set()
    for topology in topologies:
        options = []
        for good in GOODS:
            source = supplier[good]
            outgoing = tuple(
                target for edge_source, target in topology if edge_source == source
            )
            options.append(outgoing if source == "charity" else (source, *outgoing))
        for recipients in itertools.product(*options):
            allocation = {recipient: [] for recipient in RECIPIENTS}
            for good, recipient in zip(GOODS, recipients, strict=True):
                allocation[recipient].append(good)
            if any(not allocation[owner] for owner in OWNERS):
                continue
            key = tuple(tuple(allocation[recipient]) for recipient in RECIPIENTS)
            if key not in seen:
                seen.add(key)
                yield allocation


def replay(path):
    payload = json.loads(path.read_text())
    values = {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in payload["values"].items()
    }
    form_index = payload["form_index"]
    topologies = tuple(
        tuple(tuple(edge) for edge in topology)
        for topology in payload.get(
            "topologies", R2 if form_index == 0 else R3
        )
    )
    expected_relation = {
        0: {("r", "q"), ("q", "r"), ("s", "d"), ("d", "q"), ("d", "r")},
        2: {("r", "q"), ("q", "s"), ("s", "r"), ("d", "q"), ("d", "r")},
    }[form_index]

    named = tuple(named_allocations(topologies))
    named_efx = [allocation for allocation in named if complete_efx(values, allocation)]

    unrestricted = []
    for allocation in allocations_with_at_most_edges(4, SUPPORT_STATE):
        if any(not allocation[owner] for owner in OWNERS):
            continue
        if complete_efx(values, allocation):
            unrestricted.append(allocation)

    solver, variables = build_rank_three_master(
        exclude_self_responses=True,
        required_owner_cycle_form=True,
        exact_owner_cycle_response_relation=True,
        owner_cycle_form_index=form_index,
    )
    if payload.get("ordinary_pi_free"):
        solver.add(*ordinary_pi_free_constraints(variables, BASE))
    for owner in OWNERS:
        for good in GOODS:
            solver.add(variables[good, owner] == z3.RealVal(str(values[owner][good])))
    master_replay = solver.check()

    ordinary = ordinary_relation(values)
    return {
        "source": f"results/{path.name}",
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "form_index": form_index,
        "master_exact_value_replay": str(master_replay),
        "ordinary_pi_free_required": bool(payload.get("ordinary_pi_free")),
        "ordinary_response_relation": [list(edge) for edge in sorted(ordinary)],
        "ordinary_response_cycles": [list(cycle) for cycle in ordinary_cycles(ordinary)],
        "ordinary_pi_free_exact": not ordinary_cycles(ordinary),
        "exact_nonself_response_relation": [list(edge) for edge in sorted(exact_relation(values))],
        "exact_relation_matches_form": exact_relation(values) == expected_relation,
        "named_topology_count": len(topologies),
        "named_allocation_count": len(named),
        "decision_allocation_count": payload["distinct_allocation_count"],
        "named_allocation_count_matches": len(named) == payload["distinct_allocation_count"],
        "named_complete_efx_count": len(named_efx),
        "unrestricted_four_edge_complete_efx_count": len(unrestricted),
        "first_unrestricted_witness": unrestricted[0] if unrestricted else None,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    records = [replay(path) for path in args.source]
    result = {
        "schema": "two-survivor-named-topology-refutation-audit-v1",
        "verdict": (
            "NAMED_RESPONSE_TOPOLOGY_SELECTOR_REFUTED_UNRESTRICTED_FOUR_EDGE_SURVIVES"
        ),
        "records": records,
        "all_exact_relation_replays_match": all(
            record["master_exact_value_replay"] == "sat"
            and record["exact_relation_matches_form"]
            and record["named_allocation_count_matches"]
            for record in records
        ),
        "all_named_families_have_no_efx": all(
            record["named_complete_efx_count"] == 0 for record in records
        ),
        "all_profiles_have_unrestricted_four_edge_efx": all(
            record["unrestricted_four_edge_complete_efx_count"] > 0
            for record in records
        ),
        "claim_boundary": (
            "exact replay of two twelve-atom necessary-premise profiles. The "
            "result refutes the union of response-derived named topologies, not "
            "the unrestricted four-edge theorem and not the saturated theorem."
        ),
    }
    script = Path(__file__).resolve()
    result["provenance"] = {
        "script": str(script.relative_to(script.parents[2])),
        "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "verdict": result["verdict"],
        "all_exact_relation_replays_match": result["all_exact_relation_replays_match"],
        "all_named_families_have_no_efx": result["all_named_families_have_no_efx"],
        "all_profiles_have_unrestricted_four_edge_efx": result[
            "all_profiles_have_unrestricted_four_edge_efx"
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
