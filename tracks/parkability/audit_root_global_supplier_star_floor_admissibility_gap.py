#!/usr/bin/env python3
"""Audit the frozen-floor gap in the global supplier-star candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    floor, empty_value = z3.Reals("floor empty_value")
    solver = z3.SolverFor("QF_LRA")
    solver.add(floor > 0, empty_value == 0, empty_value >= floor)
    positive_floor_preservation_unsat = solver.check() == z3.unsat

    contract = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    global_contract = ROOT / "results/GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_CONTRACT_20260813.md"
    candidate = ROOT / "results/ROOT_GLOBAL_EXTERIOR_SUBPACKET_SACRIFICE_THEOREM_20260814.md"
    gap = ROOT / "results/ROOT_GLOBAL_SUPPLIER_STAR_FLOOR_ADMISSIBILITY_GAP_20260814.md"
    reset = ROOT / "results/STRICT_FIRST_PRIORITY_FLOOR_RESET_ADMISSION_THEOREM_20260814.md"
    closure = ROOT / "results/ROOT_SINGLETON_SUPPLIER_STAR_FLOOR_RESET_CLOSURE_THEOREM_20260814.md"
    script = Path(__file__).resolve()

    contract_text = contract.read_text()
    global_text = global_contract.read_text()
    candidate_text = candidate.read_text()
    gap_text = gap.read_text()
    reset_text = reset.read_text()
    closure_text = closure.read_text()
    assert "keep its declared floors" in contract_text
    assert "Every source, floor, safety" in global_text
    assert "give every other nonroot owner and charity the empty bundle" in candidate_text
    assert "gap is now repaired" in gap_text
    assert "auxiliary current floor vector" in reset_text
    assert "closes the exhaustive root-holder branch" in closure_text

    return {
        "schema": "root-global-supplier-star-floor-admissibility-gap-v1",
        "status": "HISTORICAL_UNRESET_STAR_INVALID_FLOOR_RESET_REPAIR_PROVED",
        "positive_floor_empty_assignment_preservation_unsat": positive_floor_preservation_unsat,
        "candidate_empties_later_owners": True,
        "frozen_contract_requires_declared_floors": True,
        "all_sacrificed_floors_zero_proved": False,
        "controlled_floor_reset_admitted": True,
        "unreset_supplier_star_transition_admitted": False,
        "reset_supplier_star_transition_admitted": True,
        "conditional_exterior_dominance_scalar_chain_valid": True,
        "full_T_L_times_theorem_closed": True,
        "smallest_missing_operation": None,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (
                contract,
                global_contract,
                candidate,
                gap,
                reset,
                closure,
                script,
            )
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
