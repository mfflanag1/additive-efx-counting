#!/usr/bin/env python3
"""Find nearest EFX improvements for the full-X_q capture witness."""

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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def old_owner(good: str) -> str:
    if good == "f":
        return UNALLOCATED
    if good == "z":
        return "s"
    if good.startswith(("ar_tr", "tr_rest", "aq_br", "br_rest")):
        return "r"
    if good.startswith(("aq_tq", "tq_rest", "ar_bq", "bq_rest")):
        return "q"
    if good.startswith(("tc", "bc")):
        return "c"
    raise AssertionError(good)


def load_values(path: Path):
    payload = json.loads(path.read_text())
    fractions = {
        agent: {good: Fraction(raw) for good, raw in row.items()}
        for agent, row in payload["values"].items()
    }
    scale = math.lcm(*(
        amount.denominator for row in fractions.values() for amount in row.values()
    ))
    values = {
        agent: {good: int(amount * scale) for good, amount in row.items()}
        for agent, row in fractions.items()
    }
    return payload, values, scale


def solve(values: dict, complete: bool):
    goods = tuple(values[AGENTS[0]])
    recipients = AGENTS if complete else AGENTS + (UNALLOCATED,)
    recipient_index = {recipient: index for index, recipient in enumerate(recipients)}
    owner = {good: z3.Int(f"capture_{'c' if complete else 'p'}_{good}") for good in goods}
    solver = z3.Solver()
    for good in goods:
        solver.add(owner[good] >= 0, owner[good] < len(recipients))
    bundle_value = {
        (observer, recipient): z3.Sum(*(
            z3.If(owner[good] == recipient_index[recipient], values[observer][good], 0)
            for good in goods
        ))
        for observer in AGENTS for recipient in AGENTS
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
        agent: sum(values[agent][good] for good in goods if old_owner(good) == agent)
        for agent in AGENTS
    }
    solver.add(z3.Or(*(
        z3.And(
            *(bundle_value[earlier, earlier] == base[earlier] for earlier in AGENTS[:position]),
            bundle_value[agent, agent] > base[agent],
        )
        for position, agent in enumerate(AGENTS)
    )))
    moved_terms = []
    for good in goods:
        old = old_owner(good)
        moved_terms.append(
            z3.If(owner[good] == recipient_index[old], 0, 1)
            if old in recipient_index else z3.IntVal(1)
        )
    moved = z3.Sum(*moved_terms)
    for bound in range(len(goods) + 1):
        solver.push()
        solver.add(moved <= bound)
        checked = solver.check()
        if checked == z3.sat:
            model = solver.model()
            allocation = {
                recipient: sorted(
                    good for good in goods
                    if model.eval(owner[good]).as_long() == recipient_index[recipient]
                )
                for recipient in recipients
            }
            utilities = [model.eval(bundle_value[agent, agent]).as_long() for agent in AGENTS]
            solver.pop()
            return {
                "status": "SAT",
                "minimum_moved_goods": bound,
                "allocation": allocation,
                "base_utility_vector": [base[agent] for agent in AGENTS],
                "utility_vector": utilities,
            }
        solver.pop()
    return {"status": "UNSAT"}


def run(witness_path: Path) -> dict:
    witness_path = witness_path.resolve()
    witness, values, scale = load_values(witness_path)
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    return {
        "schema": "three-nonsingleton-flower-full-q-capture-improvement-v1",
        "status": "COMPLETE",
        "source_order_key": witness["source_order_key"],
        "integer_scale": scale,
        "nearest_partial_improvement": solve(values, False),
        "nearest_complete_improvement": solve(values, True),
        "claim_boundary": (
            "exact optimization on one bounded full-X_q capture witness; the resulting transfer component "
            "is proof-mining evidence and not a cap-free escape theorem"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "witness": str(witness_path.relative_to(root)),
            "witness_sha256": sha256(witness_path),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--witness", type=Path,
        default=root / "results" / "three_nonsingleton_flower_full_q_capture_witness.json",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.witness)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "partial": result["nearest_partial_improvement"],
        "complete": result["nearest_complete_improvement"],
    }, indent=2))


if __name__ == "__main__":
    main()
