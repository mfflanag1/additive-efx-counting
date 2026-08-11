#!/usr/bin/env python3
"""Replay and minimize the residual-flower global-lex gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import z3

try:
    from . import run_residual_flower_global_lex_cegar as residual
except ImportError:
    import run_residual_flower_global_lex_cegar as residual


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
    solver, value, base = residual.base_cegar.build_master()
    solver.add(*(residual.base_cegar.tie_blocker(value, tie) for tie in ties))
    solver.add(*(
        residual.base_cegar.rival_blocker(
            value, base, allocation, "global-lex"
        )
        for allocation in rivals
    ))
    return str(solver.check())


def minimize(ties, rivals):
    core = list(rivals)
    chunk = 1
    while chunk * 2 <= len(core):
        chunk *= 2
    while chunk:
        index = 0
        while index < len(core):
            trial = core[:index] + core[index + chunk:]
            if trial and check(ties, trial) == "unsat":
                core = trial
            else:
                index += chunk
        chunk //= 2
    return core


def topology(allocation):
    base_owner = {
        good: agent
        for agent, goods in residual.base_cegar.BASE_BUNDLES.items()
        for good in goods
    }
    base_owner["f"] = "_"
    return ";".join(sorted(
        f"{base_owner[good]}->{recipient}:{good}"
        for recipient, goods in allocation.items()
        for good in goods
        if base_owner[good] != recipient
    ))


def run(gate_path):
    payload = json.loads(gate_path.read_text())
    assert payload["status"] == "UNSAT_MINIMAL_FLOWER"
    assert payload["target"] == "global-lex"
    residual.configure_residual_cell()
    residual.install_live_master()
    ties, rivals = load_records(payload)
    full_status = check(ties, rivals)
    no_tie_status = check([], rivals)
    active_ties = [] if no_tie_status == "unsat" else ties
    core = minimize(active_ties, rivals)
    deletion_checks = [
        check(active_ties, core[:index] + core[index + 1:])
        for index in range(len(core))
    ]
    return {
        "schema": "residual-flower-global-lex-gate-audit-v1",
        "status": (
            "DELETION_MINIMAL_UNSAT_CORE"
            if check(active_ties, core) == "unsat"
            and set(deletion_checks) == {"sat"}
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
            "nine-good residual-top flower cell; UNSAT is proof-mining evidence, "
            "not the cap-free flower theorem"
        ),
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
