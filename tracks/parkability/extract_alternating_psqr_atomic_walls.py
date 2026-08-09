#!/usr/bin/env python3
"""Extract failure walls for the four-rival (p,s,q,r) atomic core."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import z3

try:
    from .audit_alternating_global_lex_atomic_core import CORE_MENUS
    from .run_alternating_global_lex_cegar import (
        AGENTS,
        GOODS,
        bundles,
        lex_gt,
        rival_utilities_symbolic,
        structural_solver,
        subset_sum,
    )
except ImportError:
    from audit_alternating_global_lex_atomic_core import CORE_MENUS
    from run_alternating_global_lex_cegar import (
        AGENTS,
        GOODS,
        bundles,
        lex_gt,
        rival_utilities_symbolic,
        structural_solver,
        subset_sum,
    )


SCHEMA = "alternating-psqr-atomic-walls-v1"
ORDER = (0, 2, 3, 1)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wall_label(observer, target, removed):
    return f"{AGENTS[observer]}!>{AGENTS[target]}-{GOODS[removed]}"


def owner_record(owner):
    return {
        AGENTS[agent]: [GOODS[good] for good in bundle]
        for agent, bundle in enumerate(bundles(owner))
    }


def extract():
    menu = CORE_MENUS["".join(map(str, ORDER))]
    blocker_choices = []
    rival_records = []
    for rival_index, owner in enumerate(menu):
        solver, values, base_own = structural_solver()
        assigned = bundles(owner)
        rival_own = rival_utilities_symbolic(values, owner)
        lex = lex_gt(rival_own, base_own, ORDER)
        solver.push()
        solver.add(z3.Not(lex))
        lex_status = str(solver.check())
        solver.pop()
        possible = []
        implied_safe = []
        for observer in range(4):
            for target in range(4):
                for removed in assigned[target]:
                    remainder = tuple(
                        good for good in assigned[target] if good != removed
                    )
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
        if lex_status == "sat":
            possible.append(("not_lex", z3.Not(lex)))
        elif lex_status != "unsat":
            raise AssertionError((rival_index, "lex", lex_status))
        if not possible:
            raise AssertionError((rival_index, "no blocker"))
        blocker_choices.append(possible)
        rival_records.append(
            {
                "index": rival_index + 1,
                "allocation": owner_record(owner),
                "lex_improvement_implied": lex_status == "unsat",
                "possible_failure_walls": [label for label, _ in possible],
                "structurally_implied_safe_comparisons": implied_safe,
            }
        )

    cores = Counter()
    selection_count = 0
    for selection in itertools.product(*blocker_choices):
        selection_count += 1
        solver, _values, _own = structural_solver()
        assumptions = []
        names = {}
        for rival_index, (label, failure) in enumerate(selection, start=1):
            tag = z3.Bool(f"selected_{selection_count}_{rival_index}")
            solver.add(z3.Implies(tag, failure))
            assumptions.append(tag)
            names[str(tag)] = f"R{rival_index}:{label}"
        status = solver.check(*assumptions)
        if status != z3.unsat:
            raise AssertionError(("joint blockers feasible", selection, status))
        core = tuple(sorted(names[str(tag)] for tag in solver.unsat_core()))
        cores[core] += 1

    script = Path(__file__).resolve()
    return {
        "schema": SCHEMA,
        "status": "ALL_PSQR_ATOMIC_BLOCKER_SELECTIONS_UNSAT",
        "order": list(ORDER),
        "order_names": [AGENTS[agent] for agent in ORDER],
        "rivals": rival_records,
        "blocker_selection_count": selection_count,
        "minimal_failure_cores": [
            {"walls": list(core), "selection_count": count}
            for core, count in sorted(cores.items(), key=lambda item: (len(item[0]), item[0]))
        ],
        "claim_boundary": {
            "proved": "exact failure-wall decomposition of the four-rival atomic core",
            "not_proved": "the extension-or-handoff lemma for arbitrary packets",
        },
        "solver": {
            "name": "z3",
            "version": z3.get_version_string(),
            "logic": "QF_LRA",
        },
        "provenance": {
            "script": str(script.relative_to(script.parents[2])),
            "script_sha256": sha256(script),
        },
    }


def main():
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
