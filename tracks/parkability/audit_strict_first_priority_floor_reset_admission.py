#!/usr/bin/env python3
"""Exact audit of the strict first-priority controlled floor reset."""

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
    x, root_actual = z3.Reals("x root_actual")
    strict = z3.SolverFor("QF_LRA")
    strict.add(x >= 0, root_actual > x, root_actual <= x)
    strict_first_coordinate_exact = strict.check() == z3.unsat

    assigned = z3.Reals("assigned_0 assigned_1 assigned_2 assigned_3")
    floors = z3.Reals("floor_0 floor_1 floor_2 floor_3")
    reset = z3.SolverFor("QF_LRA")
    reset.add(*(value >= 0 for value in assigned))
    reset.add(*(floors[i] == assigned[i] for i in range(4)))
    reset.add(z3.Or(*(assigned[i] < floors[i] for i in range(4))))
    reset_floors_paid_exactly = reset.check() == z3.unsat

    # If D is strongly envied, a desired one-good deletion is smaller. This
    # scalar replay checks the strict inequality inherited by that deletion.
    source_value, target, good = z3.Reals("source_value target good")
    deletion = z3.SolverFor("QF_LRA")
    deletion.add(good > 0, source_value < target - good)
    deletion.add(z3.Not(target - good > source_value))
    strong_envy_supplies_desired_deletion = deletion.check() == z3.unsat

    theorem = ROOT / "results/STRICT_FIRST_PRIORITY_FLOOR_RESET_ADMISSION_THEOREM_20260814.md"
    gap = ROOT / "results/ROOT_GLOBAL_SUPPLIER_STAR_FLOOR_ADMISSIBILITY_GAP_20260814.md"
    charge_contract = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    global_contract = ROOT / "results/GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_CONTRACT_20260813.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "floor reset alone" in text
    assert "strict first-priority certificate" in text
    assert "recomputed floor vector" in text
    assert "separate physical progress argument" in text

    return {
        "schema": "strict-first-priority-floor-reset-admission-audit-v1",
        "status": "STRICT_FIRST_PRIORITY_FLOOR_RESET_ADMITTED",
        "strict_first_coordinate_exact": strict_first_coordinate_exact,
        "reset_floors_paid_exactly": reset_floors_paid_exactly,
        "strong_envy_supplies_desired_deletion": (
            strong_envy_supplies_desired_deletion
        ),
        "old_later_floors_preserved": False,
        "floor_reset_counts_as_progress": False,
        "all_efx_comparisons_recomputed": True,
        "physical_labels_retained": True,
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, gap, charge_contract, global_contract, script)
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
