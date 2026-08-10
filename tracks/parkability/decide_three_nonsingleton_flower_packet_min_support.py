#!/usr/bin/env python3
"""Cap-free packet-total/minimum audit of the same-source flower cell."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .decide_three_nonsingleton_flower_one_unpaid_cover import AGENTS, BASE, candidate_covers
    from .decide_three_nonsingleton_flower_support_mask_audit import RESTS, valid
except ImportError:
    from decide_three_nonsingleton_flower_one_unpaid_cover import AGENTS, BASE, candidate_covers
    from decide_three_nonsingleton_flower_support_mask_audit import RESTS, valid


COMPONENT_BUNDLES = {
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
COMPONENTS = tuple(dict.fromkeys(
    component for components in COMPONENT_BUNDLES.values() for component in components
))
def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def minimum(values):
    result = values[0]
    for value in values[1:]:
        result = z3.If(result <= value, result, value)
    return result


def present_components(aq_support: str, ar_support: str, empty_rest: tuple[str, ...]):
    present = set(COMPONENTS) - set(empty_rest)
    if aq_support == "tq":
        present.remove("aq_br")
    elif aq_support == "br":
        present.remove("aq_tq")
    if ar_support == "tr":
        present.remove("ar_bq")
    elif ar_support == "bq":
        present.remove("ar_tr")
    return present


def checked_mask(
    index: int,
    arm_source: str,
    left_bottom_source: str,
    right_bottom_source: str,
    order: tuple[str, ...],
    aq_support: str,
    ar_support: str,
    empty_rest: tuple[str, ...],
    forbid_single_replacement_owner: str | None = None,
):
    present = present_components(aq_support, ar_support, empty_rest)
    total_component = {
        (component, agent): z3.Real(f"pm{index}_{component}_{agent}")
        for component in present
        for agent in AGENTS
    }
    minimum_component = {
        (component, agent): z3.Real(f"pm{index}_{component}_min_{agent}")
        for component in present
        for agent in AGENTS
    }
    bundle_parts = {
        bundle: tuple(component for component in components if component in present)
        for bundle, components in COMPONENT_BUNDLES.items()
    }
    total = {
        (bundle, agent): z3.Sum(*(total_component[component, agent] for component in parts))
        for bundle, parts in bundle_parts.items()
        for agent in AGENTS
    }
    tail = {
        (bundle, agent): (
            z3.RealVal(0)
            if bundle == "Z"
            else total[bundle, agent] - minimum([
                minimum_component[component, agent] for component in parts
            ])
        )
        for bundle, parts in bundle_parts.items()
        for agent in AGENTS
    }
    base = {agent: total[BASE[agent], agent] for agent in AGENTS}
    solver = z3.SolverFor("QF_LRA")
    for component in present:
        for agent in AGENTS:
            solver.add(total_component[component, agent] > 0)
            if component in ("f", "z"):
                solver.add(minimum_component[component, agent] == total_component[component, agent])
            else:
                solver.add(minimum_component[component, agent] > 0)
                solver.add(minimum_component[component, agent] <= total_component[component, agent])
    for agent in AGENTS:
        for bundle in bundle_parts:
            solver.add(tail[bundle, agent] <= base[agent])
        solver.add(total_component["f", agent] <= base[agent])
        solver.add(total["X_c", agent] <= base[agent])

    desired = {
        "D_r": "r", "D_q": "q", "D_c": arm_source,
        "Z": "c", "A_q": left_bottom_source, "A_r": right_bottom_source,
    }
    for bundle, source in desired.items():
        solver.add(total[bundle, source] > base[source])

    if forbid_single_replacement_owner is not None:
        owners = AGENTS if forbid_single_replacement_owner == "all" else (forbid_single_replacement_owner,)
        for owner in owners:
            solver.add(
                total_component["f", owner]
                <= minimum([
                    minimum_component[component, owner]
                    for component in bundle_parts[BASE[owner]]
                ])
            )

    covers = candidate_covers(
        arm_source, "c", left_bottom_source, right_bottom_source, order
    )
    one_unpaid = [cover for cover in covers if cover["unpaid_agent"] is not None]
    for cover in one_unpaid:
        unpaid = cover["unpaid_agent"]
        payment = cover["assignment"][unpaid]
        solver.add(z3.Or(*(
            total[payment, unpaid] < tail[cover["assignment"][target], unpaid]
            for target in AGENTS if target != unpaid
        )))
    checked = solver.check()
    return {
        "priority_order": list(order),
        "aq_support": aq_support,
        "ar_support": ar_support,
        "empty_rest": list(empty_rest),
        "forbid_single_replacement_owner": forbid_single_replacement_owner,
        "status": "IMPOSSIBLE" if checked == z3.unsat else str(checked),
    }


def run(
    arm_source: str = "r",
    left_bottom_source: str = "c",
    right_bottom_source: str = "c",
) -> dict:
    records = []
    index = 0
    for order in itertools.permutations(AGENTS):
        for aq_support, ar_support in itertools.product(("tq", "br", "both"), ("tr", "bq", "both")):
            for mask in range(1 << len(RESTS)):
                empty_rest = tuple(rest for bit, rest in enumerate(RESTS) if mask & (1 << bit))
                if not valid(aq_support, ar_support, empty_rest):
                    continue
                records.append(checked_mask(
                    index,
                    arm_source,
                    left_bottom_source,
                    right_bottom_source,
                    order,
                    aq_support,
                    ar_support,
                    empty_rest,
                ))
                index += 1
    counts = {
        status: sum(record["status"] == status for record in records)
        for status in ("IMPOSSIBLE", "sat", "unknown")
    }
    survivors = [record for record in records if record["status"] == "sat"]
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    return {
        "schema": "three-nonsingleton-flower-packet-min-support-v1",
        "status": "COMPLETE" if len(records) == 1536 and not counts["unknown"] else "INCOMPLETE",
        "source_pattern": {
            "arm_source": arm_source,
            "singleton_envier": "c",
            "left_bottom_source": left_bottom_source,
            "right_bottom_source": right_bottom_source,
        },
        "mask_count": len(records),
        "counts": counts,
        "survivors": survivors,
        "records": records,
        "claim_boundary": (
            "cap-free QF_LRA packet abstraction: every nonempty component has arbitrary total and exact "
            "minimum, so each displayed bundle tail is exact for arbitrary packet cardinality; it proves "
            "the UNSAT support/order cells only for the named source pattern"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arm-source", choices=("r", "q", "s"), default="r")
    parser.add_argument("--left-bottom-source", choices=("c", "s"), default="c")
    parser.add_argument("--right-bottom-source", choices=("c", "s"), default="c")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.arm_source, args.left_bottom_source, args.right_bottom_source)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "counts": result["counts"]}, indent=2))


if __name__ == "__main__":
    main()
