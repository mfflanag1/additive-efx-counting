#!/usr/bin/env python3
"""Extract/replay a PI-cut core for the widened form-2 response menu."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

from .run_allocated_e_capture_rank_three_cegar import build_master
from .run_fixed_u_full_packet_terminal_cegar import allocation_formula
from .run_generalized_pi_named_selector_cegar import (
    cycle_signature, generalized_pi_cut,
)


OWNERS = ("r", "q", "d", "s")
CURRENT = {
    "r": ("a0", "a1", "h"),
    "q": ("j", "k", "q0"),
    "d": ("m", "gq", "gr"),
    "s": ("l", "e"),
    "charity": ("p",),
}
MENU = (
    (("charity", "r"), ("r", "d"), ("r", "s")),
    (("charity", "r"), ("q", "d"), ("r", "d"), ("r", "q")),
    (("charity", "q"), ("d", "q"), ("q", "d"), ("r", "s")),
    (("charity", "r"), ("s", "q"), ("r", "s"), ("r", "d")),
    (("charity", "q"), ("q", "r"), ("r", "s"), ("r", "d")),
    (("charity", "s"), ("q", "r"), ("s", "q"), ("r", "d")),
    (("charity", "r"), ("s", "q"), ("r", "s"), ("q", "d")),
    (("charity", "q"), ("q", "r"), ("r", "s"), ("q", "d")),
    (("charity", "s"), ("q", "r"), ("s", "q"), ("q", "d")),
)


def canonical(allocation):
    return tuple(
        (owner, tuple(sorted(goods)))
        for owner, goods in sorted(allocation.items())
    )


def independent_allocations_for_topology(topology):
    outgoing = {supplier: [] for supplier in CURRENT}
    charity_target = None
    for supplier, recipient in topology:
        if supplier == "charity":
            assert charity_target is None
            charity_target = recipient
        else:
            outgoing[supplier].append(recipient)
    assert charity_target is not None

    routing_rows = []
    for supplier in OWNERS:
        recipients = outgoing[supplier]
        destinations = (supplier, *recipients)
        rows = []
        for assignment in itertools.product(
                destinations, repeat=len(CURRENT[supplier])):
            if any(recipient not in assignment for recipient in recipients):
                continue
            rows.append(dict(zip(CURRENT[supplier], assignment, strict=True)))
        routing_rows.append(rows)

    allocations = []
    for selected in itertools.product(*routing_rows):
        allocation = {owner: [] for owner in OWNERS}
        allocation[charity_target].append("p")
        for routing in selected:
            for good, owner in routing.items():
                allocation[owner].append(good)
        allocation["charity"] = []
        allocations.append(allocation)
    return allocations


def independent_menu_allocations():
    rows = {}
    for topology in MENU:
        for allocation in independent_allocations_for_topology(topology):
            rows.setdefault(canonical(allocation), allocation)
    result = list(rows.values())
    assert [len(independent_allocations_for_topology(row)) for row in MENU] == [
        12, 84, 343, 36, 84, 147, 147, 84, 36,
    ]
    assert len(result) == 973
    return result


def add_menu_negations(solver, value):
    allocations = independent_menu_allocations()
    for allocation in allocations:
        solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))
    return len(allocations)


def load_witnesses(sources):
    witnesses = {}
    source_rows = []
    for source in sources:
        raw = source.read_bytes()
        payload = json.loads(raw)
        assert payload["form_index"] == 2
        before = len(witnesses)
        for iteration in payload.get("iterations", ()):
            for witness in iteration.get("pi_witnesses") or ():
                witnesses.setdefault(cycle_signature(witness), witness)
        source_rows.append({
            "source": str(source),
            "source_sha256": hashlib.sha256(raw).hexdigest(),
            "new_cut_count": len(witnesses) - before,
            "cumulative_cut_count": len(witnesses),
        })
    return witnesses, source_rows


def run(sources: list[Path], output: Path, timeout_seconds: int):
    witnesses, source_rows = load_witnesses(sources)
    solver, value = build_master(2)
    allocation_count = add_menu_negations(solver, value)
    labels = {}
    for index, (signature, witness) in enumerate(sorted(witnesses.items())):
        label = z3.Bool(f"form2_pi_cut_{index}")
        solver.assert_and_track(generalized_pi_cut(value, witness), label)
        labels[str(label)] = (signature, witness)
    solver.set(timeout=timeout_seconds * 1000)
    status = solver.check()
    if status != z3.unsat:
        raise RuntimeError(f"tracked replay did not prove UNSAT: {status}")
    core_names = {str(label) for label in solver.unsat_core()}
    core = [labels[name] for name in sorted(core_names)]

    replay, replay_value = build_master(2)
    replay_allocation_count = add_menu_negations(replay, replay_value)
    assert replay_allocation_count == allocation_count
    for _, witness in core:
        replay.add(generalized_pi_cut(replay_value, witness))
    replay.set(timeout=timeout_seconds * 1000)
    replay_status = replay.check()
    if replay_status != z3.unsat:
        raise RuntimeError(f"core-only replay did not prove UNSAT: {replay_status}")

    cycle_lengths = {}
    for _, witness in core:
        length = str(len(witness["cycle"]))
        cycle_lengths[length] = cycle_lengths.get(length, 0) + 1
    result = {
        "schema": "allocated-e-form2-response-branch-menu-unsat-core-v1",
        "status": "UNSAT_REPLAYED",
        "solver": f"Z3 {z3.get_version_string()}",
        "topology_count": len(MENU),
        "allocation_count": allocation_count,
        "cut_sources": source_rows,
        "input_cut_count": len(witnesses),
        "core_cut_count": len(core),
        "core_cycle_length_counts": cycle_lengths,
        "core_witnesses": [witness for _, witness in core],
        "tracked_replay_status": str(status),
        "core_only_replay_status": str(replay_status),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Tracked/core-only replay of the exact twelve-atom form-2 "
            "nine-topology master. The algebraic master is shared with the "
            "primary encoding and the result is not cap-free."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    args = parser.parse_args()
    result = run(args.source, args.output, args.timeout_seconds)
    print(json.dumps({
        "status": result["status"],
        "input_cut_count": result["input_cut_count"],
        "core_cut_count": result["core_cut_count"],
        "core_only_replay_status": result["core_only_replay_status"],
    }, indent=2))


if __name__ == "__main__":
    main()
