#!/usr/bin/env python3
"""Additive packet relaxation for simultaneous flower-cover failure."""

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
        BUNDLE_SUPPORT,
        candidate_covers,
        run as run_cover,
    )
except ImportError:
    from decide_three_nonsingleton_flower_one_unpaid_cover import (
        AGENTS,
        BASE,
        BUNDLE_SUPPORT,
        candidate_covers,
        run as run_cover,
    )


COMPONENTS = (
    "aq_tq", "aq_br", "tq_rest", "br_rest",
    "ar_tr", "ar_bq", "tr_rest", "bq_rest",
    "tc", "bc", "z", "f",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_cell(index: int, key: dict) -> dict:
    order = tuple(key["priority_order"])
    arm = key["arm_source"]
    envier = key["singleton_envier"]
    left = key["left_bottom_source"]
    right = key["right_bottom_source"]
    covers = candidate_covers(arm, envier, left, right, order)
    one_unpaid = [cover for cover in covers if cover["unpaid_agent"] is not None]
    assert one_unpaid and not any(cover["unpaid_agent"] is None for cover in covers)

    base = {agent: z3.Real(f"a{index}_base_{agent}") for agent in AGENTS}
    component = {
        (name, agent): z3.Real(f"a{index}_{name}_{agent}")
        for name in COMPONENTS
        for agent in AGENTS
    }
    total = {}
    for agent in AGENTS:
        aq = component["aq_tq", agent] + component["aq_br", agent]
        ar = component["ar_tr", agent] + component["ar_bq", agent]
        tq = component["aq_tq", agent] + component["tq_rest", agent]
        br = component["aq_br", agent] + component["br_rest", agent]
        tr = component["ar_tr", agent] + component["tr_rest", agent]
        bq = component["ar_bq", agent] + component["bq_rest", agent]
        total.update({
            ("A_q", agent): aq,
            ("A_r", agent): ar,
            ("D_r", agent): tq + component["f", agent],
            ("D_q", agent): tr + component["f", agent],
            ("D_c", agent): component["tc", agent] + component["f", agent],
            ("X_r", agent): tr + br,
            ("X_q", agent): tq + bq,
            ("X_c", agent): component["tc", agent] + component["bc", agent],
            ("Z", agent): component["z", agent],
        })
    tail = {
        (name, agent): z3.Real(f"a{index}_{name}_tail_{agent}")
        for name in BUNDLE_SUPPORT
        for agent in AGENTS
    }
    solver = z3.SolverFor("QF_LRA")
    for agent in AGENTS:
        solver.add(base[agent] > 0)
        for name in COMPONENTS:
            solver.add(component[name, agent] >= 0)
        for name in ("tc", "bc", "z", "f"):
            solver.add(component[name, agent] > 0)
        for pair in (("aq_tq", "tq_rest"), ("aq_br", "br_rest"), ("ar_tr", "tr_rest"), ("ar_bq", "bq_rest")):
            solver.add(component[pair[0], agent] + component[pair[1], agent] > 0)
        for name in BUNDLE_SUPPORT:
            solver.add(total[name, agent] > 0)
            solver.add(tail[name, agent] >= 0)
            solver.add(tail[name, agent] < total[name, agent])
            solver.add(tail[name, agent] <= base[agent])
        solver.add(tail["Z", agent] == 0)
        solver.add(total[BASE[agent], agent] == base[agent])
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

    for cover in one_unpaid:
        unpaid = cover["unpaid_agent"]
        payment = cover["assignment"][unpaid]
        solver.add(z3.Or(*(
            total[payment, unpaid] < tail[cover["assignment"][target], unpaid]
            for target in AGENTS
            if target != unpaid
        )))

    checked = solver.check()
    return {
        **key,
        "cover_count": len(one_unpaid),
        "status": "IMPOSSIBLE" if checked == z3.unsat else str(checked),
    }


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
    records = [checked_cell(index, key) for index, key in enumerate(live_keys)]
    counts = {
        status: sum(record["status"] == status for record in records)
        for status in ("IMPOSSIBLE", "sat", "unknown")
    }
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    return {
        "schema": "three-nonsingleton-flower-additive-low-wall-v1",
        "status": "COMPLETE" if len(records) == 432 and not counts["unknown"] else "INCOMPLETE",
        "counts": counts,
        "records": records,
        "claim_boundary": (
            "sound additive packet relaxation linking A_q,A_r to the six top/bottom packets, with arbitrary "
            "common-safe tails; SAT models need not realize packet minima or a globally maximal EFX state"
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
