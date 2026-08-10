#!/usr/bin/env python3
"""Test all one-unpaid flower covers in the independent-tail abstraction."""

from __future__ import annotations

import argparse
import hashlib
import itertools
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

    base = {agent: z3.Real(f"w{index}_base_{agent}") for agent in AGENTS}
    total = {
        (name, agent): z3.Real(f"w{index}_{name}_{agent}")
        for name in BUNDLE_SUPPORT
        for agent in AGENTS
    }
    tail = {
        (name, agent): z3.Real(f"w{index}_{name}_tail_{agent}")
        for name in BUNDLE_SUPPORT
        for agent in AGENTS
    }
    solver = z3.SolverFor("QF_LRA")
    for agent in AGENTS:
        solver.add(base[agent] > 0)
        for name in BUNDLE_SUPPORT:
            solver.add(total[name, agent] > 0)
            solver.add(tail[name, agent] >= 0)
            solver.add(tail[name, agent] < total[name, agent])
            solver.add(tail[name, agent] <= base[agent])
        solver.add(tail["Z", agent] == 0)
        solver.add(total[BASE[agent], agent] == base[agent])

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
        failure = z3.Or(*(
            total[payment, unpaid] < tail[cover["assignment"][target], unpaid]
            for target in AGENTS
            if target != unpaid
        ))
        solver.add(failure)

    checked = solver.check()
    record = {
        **key,
        "cover_count": len(one_unpaid),
        "status": "IMPOSSIBLE" if checked == z3.unsat else str(checked),
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
    records = [checked_cell(index, key) for index, key in enumerate(live_keys)]
    counts = {
        status: sum(record["status"] == status for record in records)
        for status in ("IMPOSSIBLE", "sat", "unknown")
    }
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    return {
        "schema": "three-nonsingleton-flower-abstract-low-wall-v1",
        "status": "COMPLETE" if len(records) == 432 and not counts["unknown"] else "INCOMPLETE",
        "counts": counts,
        "records": records,
        "claim_boundary": (
            "independent-total/tail abstraction for simultaneous failure of every lex-valid one-unpaid cover; "
            "SAT models need not be additively realizable and refute no EFX theorem"
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
