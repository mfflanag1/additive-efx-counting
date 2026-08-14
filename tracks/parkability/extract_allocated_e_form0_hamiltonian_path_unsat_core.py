#!/usr/bin/env python3
"""Extract and replay a PI-cut UNSAT core for the form-0 path theorem."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

from .run_allocated_e_capture_rank_three_cegar import build_master
from .run_fixed_u_full_packet_terminal_cegar import allocation_formula
from .run_generalized_pi_named_selector_cegar import cycle_signature, generalized_pi_cut


CURRENT = {
    "r": ("a0", "a1", "h"),
    "q": ("j", "k", "q0"),
    "d": ("m", "gq", "gr"),
    "s": ("l", "e"),
    "charity": ("p",),
}
PATH = {"r": "q", "q": "d", "d": "s"}


def independent_path_allocations():
    rows = []
    move_sets = {
        supplier: tuple(
            frozenset(combination)
            for size in range(1, len(CURRENT[supplier]) + 1)
            for combination in itertools.combinations(CURRENT[supplier], size)
        )
        for supplier in PATH
    }
    for selected in itertools.product(*(move_sets[supplier] for supplier in PATH)):
        moved = dict(zip(PATH, selected, strict=True))
        allocation = {owner: [] for owner in ("r", "q", "d", "s")}
        allocation["r"].append("p")
        allocation["s"].extend(CURRENT["s"])
        for supplier, recipient in PATH.items():
            for good in CURRENT[supplier]:
                allocation[recipient if good in moved[supplier] else supplier].append(good)
        allocation["charity"] = []
        rows.append(allocation)
    assert len(rows) == 343
    return rows


def add_path_negations(solver, value):
    for allocation in independent_path_allocations():
        solver.add(z3.Not(allocation_formula(allocation, value, "complete_efx")))


def run(source: Path, output: Path, timeout_seconds: int):
    payload = json.loads(source.read_text())
    assert payload["status"] == "UNSAT"
    witnesses = {}
    for iteration in payload["iterations"]:
        for witness in iteration.get("pi_witnesses", ()):
            witnesses.setdefault(cycle_signature(witness), witness)
    assert len(witnesses) == payload["generalized_pi_cut_count"]

    solver, value = build_master(0)
    add_path_negations(solver, value)
    labels = {}
    for index, (signature, witness) in enumerate(sorted(witnesses.items())):
        label = z3.Bool(f"pi_cut_{index}")
        solver.assert_and_track(generalized_pi_cut(value, witness), label)
        labels[str(label)] = (signature, witness)
    solver.set(timeout=timeout_seconds * 1000)
    status = solver.check()
    if status != z3.unsat:
        raise RuntimeError(f"tracked replay did not prove UNSAT: {status}")
    core_names = {str(label) for label in solver.unsat_core()}
    core = [labels[name] for name in sorted(core_names)]

    replay, replay_value = build_master(0)
    add_path_negations(replay, replay_value)
    for _, witness in core:
        replay.add(generalized_pi_cut(replay_value, witness))
    replay.set(timeout=timeout_seconds * 1000)
    replay_status = replay.check()
    if replay_status != z3.unsat:
        raise RuntimeError(f"core-only replay did not prove UNSAT: {replay_status}")

    result = {
        "schema": "allocated-e-form0-hamiltonian-path-unsat-core-v1",
        "status": "UNSAT_REPLAYED",
        "solver": f"Z3 {z3.get_version_string()}",
        "path_edges": [
            ["charity", "r"], ["r", "q"], ["q", "d"], ["d", "s"]
        ],
        "allocation_count": 343,
        "input_cut_count": len(witnesses),
        "core_cut_count": len(core),
        "core_witnesses": [witness for _, witness in core],
        "tracked_replay_status": str(status),
        "core_only_replay_status": str(replay_status),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Certificate replay and PI-cut core reduction for the exact "
            "twelve-atom form-0 master; not an independent master encoding "
            "and not a cap-free theorem."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=900)
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
