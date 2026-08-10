#!/usr/bin/env python3
"""Exact one-good-per-component flower cell with true EFX tails."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .decide_three_nonsingleton_flower_one_unpaid_cover import (
        AGENTS,
        BASE,
        candidate_covers,
        run as run_cover,
    )
except ImportError:
    from decide_three_nonsingleton_flower_one_unpaid_cover import (
        AGENTS,
        BASE,
        candidate_covers,
        run as run_cover,
    )


BUNDLE_COMPONENTS = {
    "A_q": ("aq_tq", "aq_br"),
    "A_r": ("ar_tr", "ar_bq"),
    "D_r": ("aq_tq", "tq_rest", "f"),
    "D_q": ("ar_tr", "tr_rest", "f"),
    "D_c": ("tc", "f"),
    "X_r": ("ar_tr", "tr_rest", "aq_br", "br_rest"),
    "X_q": ("aq_tq", "tq_rest", "ar_bq", "bq_rest"),
    "X_c": ("tc", "bc"),
    "Z": ("z",),
}
OWNER_COMPONENTS = {
    "r": ("ar_tr", "tr_rest", "aq_br", "br_rest"),
    "q": ("aq_tq", "tq_rest", "ar_bq", "bq_rest"),
    "c": ("tc", "bc"),
    "s": ("z",),
}
COMPONENTS = tuple(dict.fromkeys(
    component for components in BUNDLE_COMPONENTS.values() for component in components
))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def minimum(values):
    result = values[0]
    for value in values[1:]:
        result = z3.If(result <= value, result, value)
    return result


def true_tail(values):
    if len(values) <= 1:
        return z3.RealVal(0)
    return z3.Sum(*values) - minimum(values)


def checked_cell(index: int, key: dict, include_model: bool = False) -> dict:
    order = tuple(key["priority_order"])
    arm = key["arm_source"]
    envier = key["singleton_envier"]
    left = key["left_bottom_source"]
    right = key["right_bottom_source"]
    covers = candidate_covers(arm, envier, left, right, order)
    one_unpaid = [cover for cover in covers if cover["unpaid_agent"] is not None]
    assert one_unpaid and not any(cover["unpaid_agent"] is None for cover in covers)

    component = {
        (name, agent): z3.Real(f"t{index}_{name}_{agent}")
        for name in COMPONENTS
        for agent in AGENTS
    }
    total = {
        (name, agent): z3.Sum(*(component[part, agent] for part in parts))
        for name, parts in BUNDLE_COMPONENTS.items()
        for agent in AGENTS
    }
    tail = {
        (name, agent): (
            true_tail([component[part, agent] for part in parts])
        )
        for name, parts in BUNDLE_COMPONENTS.items()
        for agent in AGENTS
    }
    base = {agent: total[BASE[agent], agent] for agent in AGENTS}
    solver = z3.SolverFor("QF_LRA")
    for agent in AGENTS:
        for name in COMPONENTS:
            solver.add(component[name, agent] > 0)
        for name in BUNDLE_COMPONENTS:
            solver.add(tail[name, agent] <= base[agent])
        solver.add(component["f", agent] <= base[agent])
        solver.add(total["X_c", agent] <= base[agent])

    desired = {
        "D_r": "r",
        "D_q": "q",
        "D_c": arm,
        "Z": envier,
        "A_q": left,
        "A_r": right,
    }
    for name, source in desired.items():
        solver.add(total[name, source] > base[source])

    for owner_agent, old_parts in OWNER_COMPONENTS.items():
        if owner_agent == "s":
            continue
        for released in old_parts:
            new_parts = tuple(part for part in old_parts if part != released) + ("f",)
            blockers = []
            for observer in AGENTS:
                if observer == owner_agent:
                    continue
                values = [component[part, observer] for part in new_parts]
                blockers.append(z3.Sum(*values) - minimum(values) > base[observer])
            solver.add(z3.Or(
                component["f", owner_agent] <= component[released, owner_agent],
                *blockers,
            ))

    for receiver in AGENTS:
        for source in AGENTS:
            if order.index(receiver) >= order.index(source):
                continue
            for transferred in OWNER_COMPONENTS[source]:
                new_parts = dict(OWNER_COMPONENTS)
                new_parts[receiver] = OWNER_COMPONENTS[receiver] + (transferred,)
                new_parts[source] = tuple(
                    part for part in OWNER_COMPONENTS[source] if part != transferred
                )
                failure_terms = []
                for observer in AGENTS:
                    own_values = [component[part, observer] for part in new_parts[observer]]
                    own_total = z3.Sum(*own_values) if own_values else z3.RealVal(0)
                    for target in AGENTS:
                        target_values = [component[part, observer] for part in new_parts[target]]
                        failure_terms.append(own_total < true_tail(target_values))
                solver.add(z3.Or(*failure_terms))

    for cover in one_unpaid:
        unpaid = cover["unpaid_agent"]
        payment = cover["assignment"][unpaid]
        solver.add(z3.Or(*(
            total[payment, unpaid] < tail[cover["assignment"][target], unpaid]
            for target in AGENTS
            if target != unpaid
        )))

    checked = solver.check()
    record = {
        **key,
        "cover_count": len(one_unpaid),
        "status": "IMPOSSIBLE" if checked == z3.unsat else str(checked),
    }
    if include_model and checked == z3.sat:
        model = solver.model()
        record["component_values"] = {
            agent: {
                name: str(model.eval(component[name, agent], model_completion=True))
                for name in COMPONENTS
            }
            for agent in AGENTS
        }
        record["bundle_totals"] = {
            agent: {
                name: str(model.eval(total[name, agent], model_completion=True))
                for name in BUNDLE_COMPONENTS
            }
            for agent in AGENTS
        }
        record["bundle_tails"] = {
            agent: {
                name: str(model.eval(tail[name, agent], model_completion=True))
                for name in BUNDLE_COMPONENTS
            }
            for agent in AGENTS
        }
    return record


def run() -> dict:
    cover = run_cover()
    live_keys = [
        {
            field: record[field]
            for field in (
                "arm_source",
                "singleton_envier",
                "left_bottom_source",
                "right_bottom_source",
                "priority_order",
            )
        }
        for record in cover["records"]
        if record["status"] == "ONE_UNPAID"
    ]
    witness_key = {
        "arm_source": "r",
        "singleton_envier": "c",
        "left_bottom_source": "c",
        "right_bottom_source": "s",
        "priority_order": ["r", "q", "c", "s"],
    }
    records = [
        checked_cell(index, key, include_model=key == witness_key)
        for index, key in enumerate(live_keys)
    ]
    counts = {
        status: sum(record["status"] == status for record in records)
        for status in ("IMPOSSIBLE", "sat", "unknown")
    }
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    return {
        "schema": "three-nonsingleton-flower-atomic-low-wall-v3",
        "status": "COMPLETE" if len(records) == 432 and not counts["unknown"] else "INCOMPLETE",
        "counts": counts,
        "records": records,
        "claim_boundary": (
            "exact one-positive-good-per-displayed-component cell with true additive minimum-good tails "
            "and blockage of every owner-improving one-floater swap and every priority-directed "
            "one-good transfer; "
            "UNSAT is bounded-cell evidence and SAT refutes only universal sufficiency of the current cover family"
        ),
        "provenance": {
            "cover_script_sha256": cover["provenance"]["script_sha256"],
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "counts": result["counts"]}, indent=2))


if __name__ == "__main__":
    main()
