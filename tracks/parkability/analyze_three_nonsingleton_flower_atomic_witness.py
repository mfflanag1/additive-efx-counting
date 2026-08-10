#!/usr/bin/env python3
"""Find nearest EFX improvements outside the frozen flower cover family."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import z3


AGENTS = ("r", "q", "c", "s")
UNALLOCATED = "_"
OLD_OWNER = {
    "ar_tr": "r", "tr_rest": "r", "aq_br": "r", "br_rest": "r",
    "aq_tq": "q", "tq_rest": "q", "ar_bq": "q", "bq_rest": "q",
    "tc": "c", "bc": "c", "z": "s", "f": UNALLOCATED,
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_witness(path: Path):
    payload = json.loads(path.read_text())
    record = next(record for record in payload["records"] if "component_values" in record)
    fractions = {
        agent: {good: Fraction(raw) for good, raw in values.items()}
        for agent, values in record["component_values"].items()
    }
    scale = math.lcm(*(
        amount.denominator
        for values in fractions.values()
        for amount in values.values()
    ))
    integer = {
        agent: {good: int(amount * scale) for good, amount in values.items()}
        for agent, values in fractions.items()
    }
    return record, integer, scale


def solve(values: dict, complete: bool):
    goods = tuple(OLD_OWNER)
    recipients = AGENTS if complete else AGENTS + (UNALLOCATED,)
    recipient_index = {recipient: index for index, recipient in enumerate(recipients)}
    owner = {good: z3.Int(f"owner_{'complete' if complete else 'partial'}_{good}") for good in goods}
    solver = z3.Solver()
    for good in goods:
        solver.add(owner[good] >= 0, owner[good] < len(recipients))

    bundle_value = {
        (observer, recipient): z3.Sum(*(
            z3.If(owner[good] == recipient_index[recipient], values[observer][good], 0)
            for good in goods
        ))
        for observer in AGENTS
        for recipient in AGENTS
    }
    for observer in AGENTS:
        own = bundle_value[observer, observer]
        for target in AGENTS:
            target_total = bundle_value[observer, target]
            for good in goods:
                solver.add(z3.Implies(
                    owner[good] == recipient_index[target],
                    own >= target_total - values[observer][good],
                ))

    base = {
        agent: sum(values[agent][good] for good, old in OLD_OWNER.items() if old == agent)
        for agent in AGENTS
    }
    lex_terms = []
    for position, agent in enumerate(AGENTS):
        lex_terms.append(z3.And(
            *(bundle_value[earlier, earlier] == base[earlier] for earlier in AGENTS[:position]),
            bundle_value[agent, agent] > base[agent],
        ))
    solver.add(z3.Or(*lex_terms))

    moved_terms = []
    for good in goods:
        if OLD_OWNER[good] in recipient_index:
            moved_terms.append(z3.If(owner[good] == recipient_index[OLD_OWNER[good]], 0, 1))
        else:
            moved_terms.append(z3.IntVal(1))
    moved = z3.Sum(*moved_terms)
    for bound in range(len(goods) + 1):
        solver.push()
        solver.add(moved <= bound)
        checked = solver.check()
        if checked == z3.sat:
            model = solver.model()
            allocation = {
                recipient: sorted(
                    good
                    for good in goods
                    if model.eval(owner[good]).as_long() == recipient_index[recipient]
                )
                for recipient in recipients
            }
            utilities = {
                agent: model.eval(bundle_value[agent, agent]).as_long()
                for agent in AGENTS
            }
            solver.pop()
            return {
                "status": "SAT",
                "minimum_moved_goods": bound,
                "allocation": allocation,
                "utility_vector": [utilities[agent] for agent in AGENTS],
                "base_utility_vector": [base[agent] for agent in AGENTS],
            }
        solver.pop()
    return {"status": "UNSAT"}


def run(witness_path: Path) -> dict:
    witness, values, scale = load_witness(witness_path)
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    try:
        witness_label = str(witness_path.relative_to(root))
    except ValueError:
        witness_label = str(witness_path)
    return {
        "schema": "three-nonsingleton-flower-atomic-witness-improvement-v1",
        "status": "COMPLETE",
        "source_order_key": {
            field: witness[field]
            for field in (
                "arm_source", "singleton_envier", "left_bottom_source",
                "right_bottom_source", "priority_order",
            )
        },
        "integer_scale": scale,
        "values": values,
        "nearest_partial_improvement": solve(values, complete=False),
        "nearest_complete_improvement": solve(values, complete=True),
        "claim_boundary": (
            "exact optimization on the frozen 12-good atomic witness; improvements show only that a new "
            "allocation family exists outside the current common-safe cover menu"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "witness": witness_label,
            "witness_sha256": sha256(witness_path),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--witness",
        type=Path,
        default=root / "results" / "three_nonsingleton_flower_atomic_low_wall_audit.json",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.witness)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "partial": result["nearest_partial_improvement"]["status"],
        "complete": result["nearest_complete_improvement"]["status"],
    }, indent=2))


if __name__ == "__main__":
    main()
