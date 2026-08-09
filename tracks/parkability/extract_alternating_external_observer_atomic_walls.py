#!/usr/bin/env python3
"""Extract the failure-wall anatomy of the surviving atomic rooted core."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from collections import Counter
from pathlib import Path

import z3

try:
    from .audit_alternating_anchored_or_promoted_atom import ANCHORED_UNSAT_CORES
    from .run_alternating_global_lex_cegar import (
        AGENTS,
        BASE_BUNDLES,
        GOODS,
        bundles,
        lex_gt,
        rival_utilities_symbolic,
        structural_solver,
        subset_sum,
    )
except ImportError:
    from audit_alternating_anchored_or_promoted_atom import ANCHORED_UNSAT_CORES
    from run_alternating_global_lex_cegar import (
        AGENTS,
        BASE_BUNDLES,
        GOODS,
        bundles,
        lex_gt,
        rival_utilities_symbolic,
        structural_solver,
        subset_sum,
    )


SCHEMA = "alternating-external-observer-atomic-walls-v1"
ORDER = (0, 2, 1, 3)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wall_label(observer: int, target: int, removed: int) -> str:
    return f"{AGENTS[observer]}!>{AGENTS[target]}-{GOODS[removed]}"


def owner_record(owner) -> dict:
    return {
        AGENTS[agent]: [GOODS[good] for good in bundle]
        for agent, bundle in enumerate(bundles(owner))
    }


def extract() -> dict:
    menu = ANCHORED_UNSAT_CORES[ORDER]
    choices = []
    rivals = []
    for rival_index, owner in enumerate(menu):
        solver, values, base_own = structural_solver()
        assigned = bundles(owner)
        rival_own = rival_utilities_symbolic(values, owner)
        lex = lex_gt(rival_own, base_own, ORDER)
        solver.push()
        solver.add(z3.Not(lex))
        lex_failure_status = str(solver.check())
        solver.pop()

        possible = []
        implied_safe = []
        for observer in range(4):
            for target in range(4):
                for removed in assigned[target]:
                    remainder = tuple(good for good in assigned[target] if good != removed)
                    failure = rival_own[observer] < subset_sum(
                        values, observer, remainder
                    )
                    label = wall_label(observer, target, removed)
                    solver.push()
                    solver.add(failure)
                    status = str(solver.check())
                    solver.pop()
                    if status == "sat":
                        possible.append((label, failure))
                    elif status == "unsat":
                        implied_safe.append(label)
                    else:
                        raise AssertionError((rival_index, label, status))
        if lex_failure_status == "sat":
            possible.append(("not_lex", z3.Not(lex)))
        elif lex_failure_status != "unsat":
            raise AssertionError((rival_index, "lex", lex_failure_status))
        if not possible:
            raise AssertionError((rival_index, "no possible blocker"))
        choices.append(possible)
        rivals.append(
            {
                "index": rival_index,
                "allocation": owner_record(owner),
                "lex_improvement_implied": lex_failure_status == "unsat",
                "possible_failure_walls": [label for label, _ in possible],
                "structurally_implied_safe_comparisons": implied_safe,
            }
        )

    core_counts: Counter[tuple[str, ...]] = Counter()
    tuple_count = 0
    for selection in itertools.product(*choices):
        tuple_count += 1
        solver, _, _ = structural_solver()
        assumptions = []
        labels = {}
        for rival_index, (label, failure) in enumerate(selection):
            assumption = z3.Bool(f"selected_{rival_index}_{tuple_count}")
            solver.add(z3.Implies(assumption, failure))
            assumptions.append(assumption)
            labels[str(assumption)] = f"R{rival_index + 1}:{label}"
        status = solver.check(*assumptions)
        if status != z3.unsat:
            raise AssertionError(("joint blockers feasible", selection, status))
        core = tuple(sorted(labels[str(item)] for item in solver.unsat_core()))
        core_counts[core] += 1

    # The only cross-row blocker pair is R1:q!>r-bq together with failure
    # of R4 to improve r.  Isolate the structural assertions needed to
    # contradict that pair so the analytic proof does not hide behind the
    # full alternating encoding.
    original, values, _ = structural_solver()
    structural = list(original.assertions())
    pair = (
        values[3][2] < values[3][0] + values[3][1],
        values[1][3] <= values[1][1],
    )
    tracked = z3.SolverFor("QF_LRA")
    tags = []
    expressions = {}
    for index, assertion in enumerate(structural):
        tag = z3.Bool(f"structure_{index}")
        tracked.add(z3.Implies(tag, assertion))
        tags.append(tag)
        expressions[str(tag)] = assertion
    for index, assertion in enumerate(pair):
        tag = z3.Bool(f"pair_{index}")
        tracked.add(z3.Implies(tag, assertion))
        tags.append(tag)
        expressions[str(tag)] = assertion
    generator = random.Random(20260809)
    best = None
    for _ in range(32):
        ordered = list(tags)
        generator.shuffle(ordered)
        if tracked.check(*ordered) != z3.unsat:
            raise AssertionError("exceptional pair unexpectedly feasible")
        active = list(tracked.unsat_core())
        generator.shuffle(active)
        changed = True
        while changed:
            changed = False
            for tag in tuple(active):
                reduced = [item for item in active if item is not tag]
                if tracked.check(*reduced) == z3.unsat:
                    active = reduced
                    changed = True
                    break
        if best is None or len(active) < len(best):
            best = list(active)
    assert best is not None
    active = sorted(best, key=str)
    exceptional_core = [
        {"tag": str(tag), "assertion": str(expressions[str(tag)])}
        for tag in active
    ]

    return {
        "schema": SCHEMA,
        "status": "ALL_ATOMIC_BLOCKER_SELECTIONS_UNSAT",
        "order": list(ORDER),
        "order_names": [AGENTS[agent] for agent in ORDER],
        "rivals": rivals,
        "blocker_selection_count": tuple_count,
        "minimal_failure_cores": [
            {"walls": list(core), "selection_count": count}
            for core, count in sorted(
                core_counts.items(), key=lambda item: (len(item[0]), item[0])
            )
        ],
        "exceptional_pair_structural_core": exceptional_core,
        "claim_boundary": {
            "proved": "exact failure-wall decomposition of the four-rival atomic core",
            "not_proved": "the rooted lemma for non-atomic packets",
        },
        "solver": {
            "name": "z3",
            "version": z3.get_version_string(),
            "logic": "QF_LRA",
        },
        "provenance": {
            "script": str(Path(__file__).resolve().relative_to(Path(__file__).resolve().parents[2])),
            "script_sha256": sha256(Path(__file__).resolve()),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = extract()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        temporary = args.output.with_suffix(args.output.suffix + ".tmp")
        temporary.write_text(payload)
        temporary.replace(args.output)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
