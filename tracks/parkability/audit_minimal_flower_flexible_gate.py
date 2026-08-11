#!/usr/bin/env python3
"""Replay and minimize the minimal-flower flexible-completion gate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .run_minimal_flower_global_lex_cegar import (
        build_master,
        rival_blocker,
        tie_blocker,
    )
except ImportError:
    from run_minimal_flower_global_lex_cegar import (
        build_master,
        rival_blocker,
        tie_blocker,
    )


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_records(payload):
    ties = []
    rivals = []
    for record in payload["trace"]:
        if record["kind"] == "nondegeneracy":
            ties.extend(
                (entry["agent"], tuple(entry["signature"]))
                for entry in record["ties"]
            )
        elif record["kind"] == "rival":
            rivals.extend(
                {recipient: tuple(goods) for recipient, goods in allocation.items()}
                for allocation in record["allocations"]
            )
    return ties, rivals


def check(ties, rivals):
    solver, value, base = build_master()
    solver.add(*(tie_blocker(value, tie) for tie in ties))
    solver.add(*(
        rival_blocker(value, base, allocation, "flexible")
        for allocation in rivals
    ))
    return str(solver.check())


def minimize_rivals(ties, rivals):
    core = list(rivals)
    index = 0
    while index < len(core):
        trial = core[:index] + core[index + 1:]
        if check(ties, trial) == "unsat":
            core = trial
        else:
            index += 1
    return core


def topology(allocation):
    base_owner = {
        "tr": "r", "br": "r", "tq": "q", "bq": "q",
        "tc": "c", "bc": "c", "z": "s", "f": "_",
    }
    edges = sorted(
        f"{base_owner[good]}->{recipient}:{good}"
        for recipient, goods in allocation.items()
        for good in goods
        if base_owner[good] != recipient
    )
    return ";".join(edges)


def run(gate_path):
    payload = json.loads(gate_path.read_text())
    assert payload["status"] == "UNSAT_MINIMAL_FLOWER"
    assert payload["target"] == "flexible"
    ties, rivals = load_records(payload)
    full_status = check(ties, rivals)
    no_tie_status = check([], rivals)
    active_ties = [] if no_tie_status == "unsat" else ties
    core = minimize_rivals(active_ties, rivals)
    minimal_status = check(active_ties, core)
    deletion_checks = [
        check(active_ties, core[:index] + core[index + 1:])
        for index in range(len(core))
    ]
    return {
        "schema": "minimal-flower-flexible-completion-audit-v1",
        "status": (
            "DELETION_MINIMAL_UNSAT_CORE"
            if minimal_status == "unsat" and set(deletion_checks) == {"sat"}
            else "AUDIT_FAILED"
        ),
        "solver": f"Z3 {z3.get_version_string()}",
        "full_replay_status": full_status,
        "without_nondegeneracy_status": no_tie_status,
        "recorded_tie_count": len(ties),
        "recorded_rival_count": len(rivals),
        "core_rival_count": len(core),
        "core": [
            {
                "allocation": {
                    recipient: list(goods)
                    for recipient, goods in allocation.items()
                },
                "topology": topology(allocation),
            }
            for allocation in core
        ],
        "deletion_check_statuses": deletion_checks,
        "claim_boundary": (
            "exact QF_LRA replay and deletion-minimal allocation core for the "
            "eight-good representative full-capture flower; this is a bounded "
            "proof-mining certificate, not the cap-free flexible completion lemma"
        ),
        "provenance": {
            "gate": str(gate_path),
            "gate_sha256": sha256(gate_path),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.gate.resolve())
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "without_nondegeneracy_status": result["without_nondegeneracy_status"],
        "recorded_rivals": result["recorded_rival_count"],
        "core_rivals": result["core_rival_count"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
