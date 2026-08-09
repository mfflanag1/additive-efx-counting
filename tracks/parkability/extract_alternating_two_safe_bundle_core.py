#!/usr/bin/env python3
"""Extract a tracked pair-blocker core for an alternating safe-pair gate."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import z3

try:
    from .decide_alternating_two_safe_bundle_gate import (
        desired_bundles,
        pair_expression,
        powerset,
    )
    from .decide_alternating_safe_pair_schema import schema_records
    from .run_alternating_variable_packet_rooted_cegar import AGENTS, make_cell, structural_solver
except ImportError:
    from decide_alternating_two_safe_bundle_gate import (
        desired_bundles,
        pair_expression,
        powerset,
    )
    from decide_alternating_safe_pair_schema import schema_records
    from run_alternating_variable_packet_rooted_cegar import AGENTS, make_cell, structural_solver


SCHEMA = "alternating-two-safe-bundle-tracked-core-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pair_records(cell, menu, q_face_payment):
    if menu == "q_face":
        yield from schema_records(cell, q_face_payment)
        return
    residual = tuple(
        good for good in range(cell["m"]) if good not in (cell["x"], cell["y"])
    )
    for source in (2, 1):
        for desired_bundle in desired_bundles(cell):
            complement = tuple(good for good in residual if good not in desired_bundle)
            for q_bundle in powerset(complement):
                if not q_bundle and len(desired_bundle) > 1:
                    continue
                yield "unrestricted", source, desired_bundle, q_bundle


def solve_tracked(cell, records, timeout_seconds):
    solver, values, own = structural_solver(cell)
    labels = []
    for index, (_, source, desired_bundle, q_bundle) in enumerate(records):
        label = z3.Bool(f"safe_pair_blocker_{index}")
        solver.assert_and_track(
            z3.Not(
                pair_expression(values, own, source, desired_bundle, q_bundle)
            ),
            label,
        )
        labels.append(label)
    solver.set(timeout=max(1, int(timeout_seconds * 1000)))
    status = solver.check()
    if status != z3.unsat:
        return status, solver.reason_unknown(), ()
    core_names = {str(label) for label in solver.unsat_core()}
    core = tuple(
        record
        for index, record in enumerate(records)
        if f"safe_pair_blocker_{index}" in core_names
    )
    return status, "", core


def solve_plain(cell, records, timeout_seconds):
    solver, values, own = structural_solver(cell)
    solver.add(
        *(
            z3.Not(pair_expression(values, own, source, desired_bundle, q_bundle))
            for _, source, desired_bundle, q_bundle in records
        )
    )
    solver.set(timeout=max(1, int(timeout_seconds * 1000)))
    status = solver.check()
    return status, solver.reason_unknown() if status == z3.unknown else ""


def shrink_core(cell, records, timeout_seconds):
    solver, values, own = structural_solver(cell)
    labels = []
    for index, (_, source, desired_bundle, q_bundle) in enumerate(records):
        label = z3.Bool(f"shrink_pair_blocker_{index}")
        solver.add(
            z3.Implies(
                label,
                z3.Not(
                    pair_expression(values, own, source, desired_bundle, q_bundle)
                ),
            )
        )
        labels.append(label)
    solver.set(timeout=max(1, int(timeout_seconds * 1000)))
    active = list(range(len(records)))
    checks = []
    for index in tuple(active):
        trial = tuple(labels[other] for other in active if other != index)
        status = solver.check(*trial)
        checks.append({"removed_index": index, "status": str(status)})
        if status == z3.unsat:
            active.remove(index)
        elif status == z3.unknown:
            checks[-1]["reason_unknown"] = solver.reason_unknown()
    return tuple(records[index] for index in active), checks


def extract(
    sizes,
    timeout_seconds,
    replay_timeout_seconds,
    shrink_timeout_seconds,
    menu,
    q_face_payment,
):
    cell = make_cell(sizes)
    records = tuple(pair_records(cell, menu, q_face_payment))
    status, reason, core = solve_tracked(cell, records, timeout_seconds)
    result = {
        "schema": SCHEMA,
        "packet_sizes": list(sizes),
        "goods": list(cell["goods"]),
        "menu": menu,
        "q_face_payment": q_face_payment,
        "candidate_pair_count": len(records),
        "tracked_solver_status": str(status),
        "claim_boundary": {
            "proved": "only a replayed UNSAT core is a sufficient binary pair menu",
            "not_proved": "core extraction alone is not an arbitrary-packet theorem",
        },
    }
    if status != z3.unsat:
        result.update({"status": "UNKNOWN", "reason_unknown": reason})
        return result
    initial_core = core
    shrink_checks = []
    if shrink_timeout_seconds > 0:
        core, shrink_checks = shrink_core(cell, core, shrink_timeout_seconds)
    replay_status, replay_reason = solve_plain(cell, core, replay_timeout_seconds)
    family_counts = Counter(family for family, _, _, _ in core)
    source_counts = Counter(AGENTS[source] for _, source, _, _ in core)
    shape_counts = Counter(
        (len(desired_bundle), len(q_bundle))
        for _, _, desired_bundle, q_bundle in core
    )
    result.update(
        {
            "status": (
                "UNSAT_TRACKED_CORE_REPLAYED"
                if replay_status == z3.unsat
                else "TRACKED_CORE_REPLAY_NOT_UNSAT"
            ),
            "initial_core_pair_count": len(initial_core),
            "core_pair_count": len(core),
            "core_fraction": len(core) / len(records),
            "shrink_checks": shrink_checks,
            "family_counts": dict(sorted(family_counts.items())),
            "source_counts": dict(sorted(source_counts.items())),
            "shape_counts": [
                {"desired_size": shape[0], "q_size": shape[1], "count": count}
                for shape, count in sorted(shape_counts.items())
            ],
            "core_replay_status": str(replay_status),
            "core_replay_reason_unknown": replay_reason,
            "core_pairs": [
                {
                    "family": family,
                    "source": AGENTS[source],
                    "desired_bundle": [cell["goods"][good] for good in desired_bundle],
                    "q_bundle": [cell["goods"][good] for good in q_bundle],
                }
                for family, source, desired_bundle, q_bundle in core
            ],
        }
    )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", default="2,2,2,2")
    parser.add_argument("--timeout-seconds", type=float, default=180.0)
    parser.add_argument("--replay-timeout-seconds", type=float, default=180.0)
    parser.add_argument("--shrink-timeout-seconds", type=float, default=0.0)
    parser.add_argument("--menu", choices=("unrestricted", "q_face"), default="unrestricted")
    parser.add_argument("--q-face-payment", choices=("any", "remainder"), default="any")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sizes = tuple(int(part) for part in args.sizes.split(","))
    if len(sizes) != 4 or any(size < 1 for size in sizes):
        raise ValueError("--sizes must contain four positive integers")
    result = extract(
        sizes,
        args.timeout_seconds,
        args.replay_timeout_seconds,
        args.shrink_timeout_seconds,
        args.menu,
        args.q_face_payment,
    )
    script = Path(__file__).resolve()
    result["provenance"] = {
        "script": str(script.relative_to(script.parents[2])),
        "script_sha256": sha256(script),
        "z3_version": z3.get_version_string(),
    }
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(args.output)
    print(
        json.dumps(
            {
                key: result.get(key)
                for key in (
                    "status",
                    "candidate_pair_count",
                    "core_pair_count",
                    "source_counts",
                    "shape_counts",
                    "core_replay_status",
                    "reason_unknown",
                )
                if key in result
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
