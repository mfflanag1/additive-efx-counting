#!/usr/bin/env python3
"""Harvest exact CEGAR cuts from SAT models in a case-decision artifact."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_minimum_slot_orbit import audit_orbit
    from .audit_threshold_plateau_exact_paths import mask_threshold, mask_value
    from .run_minimum_slot_orbit_cegar import (
        BASE,
        FLOATER,
        SCHEMA,
        TOKENS,
        global_landscape,
        masks_from_bundles,
        relabeled_state_orbit,
        state_key,
    )
except ImportError:
    from anneal import atomic_json
    from audit_minimum_slot_orbit import audit_orbit
    from audit_threshold_plateau_exact_paths import mask_threshold, mask_value
    from run_minimum_slot_orbit_cegar import (
        BASE,
        FLOATER,
        SCHEMA,
        TOKENS,
        global_landscape,
        masks_from_bundles,
        relabeled_state_orbit,
        state_key,
    )


SUPPORTED_SOURCE_SCHEMAS = {
    "pair-hall-zero-heavy-equality-case-decision-v1",
    "minimum-slot-literal-cube-cover-decision-v1",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def integer_rows(values):
    rows = []
    for row in values:
        fractions = [Fraction(value) for value in row]
        denominator = math.lcm(*(value.denominator for value in fractions))
        integers = [int(value * denominator) for value in fractions]
        divisor = math.gcd(*integers)
        rows.append([value // divisor for value in integers])
    return rows


def sat_cases(document):
    records = document.get("cases", document.get("branches", ()))
    return [record for record in records if record.get("verdict") == "sat"]


def exact_completions(values, record):
    completions = []
    for host in range(4):
        complete_masks = list(record["masks"])
        complete_masks[host] |= 1 << record["floater"]
        for permutation in itertools.permutations(range(4)):
            if all(
                mask_value(values, observer, complete_masks[permutation[observer]])
                >= mask_threshold(values, observer, complete_masks[target])
                for observer in range(4)
                for target in range(4)
                if target != permutation[observer]
            ):
                completions.append((host, permutation))
    return completions


def run(source: Path, output: Path, relabeling_mode: str, all_completions=False):
    if output.exists() or relabeling_mode not in {"none", "cyclic", "full"}:
        raise ValueError("a new output and supported relabeling mode are required")
    document = json.loads(source.read_text())
    if document.get("schema") not in SUPPORTED_SOURCE_SCHEMAS:
        raise ValueError("unsupported case-decision source")
    cases = sat_cases(document)
    if not cases or any(case.get("values") is None for case in cases):
        raise ValueError("source must contain at least one exact SAT model")

    completion_cuts = {}
    global_cuts = {}
    model_records = []
    blocked_global_models = []
    last_values = None
    for case in cases:
        values = integer_rows(case["values"])
        last_values = values
        orbit = audit_orbit(
            values,
            {"floater": FLOATER, "masks": masks_from_bundles(BASE)},
            TOKENS[:4],
            include_records=True,
        )
        completing = [record for record in orbit["records"] if record["completing"]]
        record = {
            "case": case.get("mask", case.get("branch")),
            "completing_orbit_state_count": len(completing),
        }
        if completing:
            for completion in completing:
                witnesses = (
                    exact_completions(values, completion)
                    if all_completions
                    else ((
                        int(completion["best_host"]),
                        tuple(completion["best_permutation"]),
                    ),)
                )
                if not witnesses:
                    raise AssertionError("completing orbit state has no completion")
                for host, permutation in witnesses:
                    key = (tuple(completion["assignment"]), host, permutation)
                    completion_cuts.setdefault(
                        key,
                        {
                            "assignment": list(key[0]),
                            "host": key[1],
                            "permutation": list(key[2]),
                        },
                    )
        else:
            _, fixed, higher_state = global_landscape(values)
            record["fixed_base_is_global_threshold_maximum"] = fixed is not None
            if fixed is not None:
                blocked_global_models.append(
                    {"case": record["case"], "values": values, "orbit_audit": orbit}
                )
            else:
                for state in relabeled_state_orbit(higher_state, relabeling_mode):
                    key = state_key(state)
                    global_cuts.setdefault(
                        key,
                        {
                            "floater": state["floater"],
                            "masks": list(state["masks"]),
                            **{
                                field: state[field]
                                for field in (
                                    "owner_distance",
                                    "threshold_gain_numerator",
                                    "threshold_gain_denominator",
                                )
                                if field in state
                            },
                        },
                    )
        model_records.append(record)

    result = {
        "schema": SCHEMA,
        "status": (
            "GLOBAL_MAXIMUM_BLOCKED_TOKEN_ORBIT_FOUND"
            if blocked_global_models
            else "HARVESTED_MODEL_CUT_POOL"
        ),
        "meaning": (
            "Exact completion and global-maximality consequences harvested from "
            "SAT models of an exact case split."
        ),
        "claim_boundary": (
            "This is a portable CEGAR seed, not an UNSAT theorem verdict."
            if not blocked_global_models
            else "At least one harvested model passed exact global and orbit audits."
        ),
        "source": str(source),
        "source_sha256": sha256(source),
        "relabeling_mode": relabeling_mode,
        "all_completions": all_completions,
        "values": last_values,
        "total_iterations": len(cases),
        "global_cut_count": len(global_cuts),
        "completion_cut_count": len(completion_cuts),
        "orbit_hall_cut_count": 0,
        "global_cuts": list(global_cuts.values()),
        "completion_cuts": list(completion_cuts.values()),
        "orbit_hall_cuts": [],
        "sat_model_count": len(cases),
        "model_records": model_records,
        "blocked_global_models": blocked_global_models,
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--relabeling-mode",
        choices=("none", "cyclic", "full"),
        default="cyclic",
    )
    parser.add_argument("--all-completions", action="store_true")
    args = parser.parse_args()
    result = run(
        args.source,
        args.output,
        args.relabeling_mode,
        args.all_completions,
    )
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "status",
                    "sat_model_count",
                    "global_cut_count",
                    "completion_cut_count",
                )
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
