#!/usr/bin/env python3
"""Certify the canonical forced-singleton-swap handoff lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .lra_master import ParkabilityLRAMaster
    from .normalize_smt2_for_cvc5 import atomic_write
    from .run_lexmax_partial_cegar import (
        Base,
        bundles_of,
        rival_blocker_expression,
        subset_sum,
    )
except ImportError:
    from anneal import atomic_json
    from lra_master import ParkabilityLRAMaster
    from normalize_smt2_for_cvc5 import atomic_write
    from run_lexmax_partial_cegar import (
        Base,
        bundles_of,
        rival_blocker_expression,
        subset_sum,
    )


SCHEMA = "forced-singleton-swap-certificate-v1"
A: Base = (8, (2, 1, 1, 1, 2, 3, 0, 0, None))
B: Base = (3, (1, 1, 1, None, 3, 1, 2, 0, 3))
SWAP: Base = (3, (1, 1, 1, None, 3, 1, 0, 2, 3))
ORDER = (1, 0, 2, 3)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def add_weak_state(
    master: ParkabilityLRAMaster,
    state: Base,
    *,
    blocked_hosts: tuple[int, ...],
) -> tuple[z3.ArithRef, ...]:
    floater, base_owner = state
    bundles = bundles_of(base_owner, master.n)
    utilities = tuple(
        subset_sum(master, observer, bundles[observer])
        for observer in range(master.n)
    )
    for observer in range(master.n):
        master.solver.add(
            utilities[observer] >= master.values[observer][floater]
        )
        for target in range(master.n):
            if observer == target:
                continue
            for removed in bundles[target]:
                master.solver.add(
                    utilities[observer]
                    >= subset_sum(
                        master,
                        observer,
                        tuple(
                            good
                            for good in bundles[target]
                            if good != removed
                        ),
                    )
                )
    for host in blocked_hosts:
        enlarged = bundles[host] + (floater,)
        master.solver.add(
            z3.Or(
                *(
                    utilities[observer]
                    < subset_sum(
                        master,
                        observer,
                        tuple(
                            good
                            for good in enlarged
                            if good != removed
                        ),
                    )
                    for observer in range(master.n)
                    if observer != host
                    for removed in enlarged
                )
            )
        )
    return utilities


def build_premise() -> tuple[
    ParkabilityLRAMaster,
    tuple[z3.ArithRef, ...],
    tuple[z3.ArithRef, ...],
]:
    master = ParkabilityLRAMaster(4, 9)
    utility_a = add_weak_state(master, A, blocked_hosts=(3,))
    utility_b = add_weak_state(master, B, blocked_hosts=(0, 2))
    return master, utility_a, utility_b


def check_negated(
    master: ParkabilityLRAMaster,
    conclusion: z3.BoolRef,
) -> str:
    master.solver.push()
    master.solver.add(z3.Not(conclusion))
    status = str(master.solver.check())
    master.solver.pop()
    return status


def construct() -> tuple[dict, bytes]:
    master, _, utility_b = build_premise()
    premise = master.solve(time_limit_s=30)
    if premise.status != "SAT" or premise.values is None:
        raise AssertionError("forced-swap premises are not satisfiable")
    first_ordering = master.values[0][6] > master.values[0][7]
    second_ordering = master.values[2][7] > master.values[2][6]
    first_status = check_negated(master, first_ordering)
    second_status = check_negated(master, second_ordering)
    if first_status != "unsat" or second_status != "unsat":
        raise AssertionError("a forced singleton ordering was not proved")

    handoff_blocker = rival_blocker_expression(
        master,
        utility_b,
        B[1],
        SWAP,
        ORDER,
        "exact",
    )
    master.solver.push()
    master.solver.add(handoff_blocker)
    handoff_status = str(master.solver.check())
    master.solver.pop()
    if handoff_status != "unsat":
        raise AssertionError("swap state was not forced eligible and lex larger")

    frozen, _, frozen_utility_b = build_premise()
    frozen.solver.add(
        rival_blocker_expression(
            frozen,
            frozen_utility_b,
            B[1],
            SWAP,
            ORDER,
            "exact",
        )
    )
    if frozen.solve(time_limit_s=30).status != "UNSAT":
        raise AssertionError("frozen handoff formula is not UNSAT")
    formula = frozen.to_smt2().encode()

    def state_record(state: Base) -> dict:
        return {
            "floater": state[0],
            "base_owner": list(state[1]),
            "bundles": [
                list(bundle)
                for bundle in bundles_of(state[1], 4)
            ],
        }

    record = {
        "schema": SCHEMA,
        "status": "PROVED_CANONICAL_SYMBOLIC_LEMMA",
        "meaning": (
            "under weak EFX and weak floater-nonenvy, the three stated "
            "blocked hosts force the swap state to be eligible and strictly "
            "larger in order (1,0,2,3); item and agent relabeling gives the "
            "abstract forced-singleton-swap lemma"
        ),
        "n": 4,
        "m": 9,
        "strictly_positive_additive_values": True,
        "state_a": state_record(A),
        "state_b": state_record(B),
        "swap_state": state_record(SWAP),
        "blocked_hosts": {
            "state_a": [3],
            "state_b": [0, 2],
        },
        "agent_order": list(ORDER),
        "checks": {
            "premise_status": "sat",
            "premise_model": [list(row) for row in premise.values],
            "negated_v0_g6_gt_g7_status": first_status,
            "negated_v2_g7_gt_g6_status": second_status,
            "swap_ineligible_or_lex_lower_status": handoff_status,
            "frozen_formula_status": "unsat",
        },
        "solver": {
            "name": "z3",
            "version": z3.get_version_string(),
            "logic": "QF_LRA",
        },
        "smt2_sha256": sha256_bytes(formula),
    }
    return record, formula


def generate(record_path: Path, smt2_path: Path) -> dict:
    if record_path.exists() or smt2_path.exists():
        raise ValueError("generation requires new output paths")
    record, formula = construct()
    atomic_write(smt2_path, formula)
    record["smt2_path"] = str(smt2_path.resolve())
    atomic_json(record_path, record)
    return record


def verify(record_path: Path, smt2_path: Path) -> dict:
    observed = json.loads(record_path.read_text())
    expected, formula = construct()
    expected["smt2_path"] = str(smt2_path.resolve())
    if observed != expected:
        raise AssertionError("forced-swap certificate record changed")
    if smt2_path.read_bytes() != formula:
        raise AssertionError("forced-swap SMT formula changed")
    if observed["smt2_sha256"] != sha256(smt2_path):
        raise AssertionError("forced-swap formula hash mismatch")
    return {
        "status": "PASS",
        "record": str(record_path.resolve()),
        "smt2": str(smt2_path.resolve()),
        "smt2_sha256": observed["smt2_sha256"],
        "claim_scope": (
            "analytic local exchange lemma; not a proof of complete EFX"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--record",
        type=Path,
        default=Path("results/forced_singleton_swap_lemma.json"),
    )
    parser.add_argument(
        "--smt2",
        type=Path,
        default=Path("results/forced_singleton_swap_lemma.smt2"),
    )
    parser.add_argument("--generate", action="store_true")
    args = parser.parse_args()
    result = (
        generate(args.record, args.smt2)
        if args.generate
        else verify(args.record, args.smt2)
    )
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
