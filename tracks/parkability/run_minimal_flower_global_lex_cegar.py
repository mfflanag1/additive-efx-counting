#!/usr/bin/env python3
"""Exact CEGAR for a globally lex-maximal minimal GG flower state."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from fractions import Fraction
from pathlib import Path

import z3


AGENTS = ("r", "q", "c", "s")
RECIPIENTS = AGENTS + ("_",)
GOODS = ("tr", "br", "tq", "bq", "tc", "bc", "z", "f")
BASE_BUNDLES = {
    "r": ("tr", "br"),
    "q": ("tq", "bq"),
    "c": ("tc", "bc"),
    "s": ("z",),
}
DISPLAYED_BUNDLES = {
    "D_r": ("tq", "f"),
    "D_q": ("tr", "f"),
    "D_c": ("tc", "f"),
    "A_q": ("tq", "br"),
    "A_r": ("tr", "bq"),
    "Z": ("z",),
    **{f"X_{agent}": goods for agent, goods in BASE_BUNDLES.items()},
}
DESIRED_SOURCES = {
    "D_r": "r",
    "D_q": "q",
    "D_c": "r",
    "A_q": "c",
    "A_r": "c",
    "Z": "c",
}


def add(entries):
    return z3.Sum(*entries) if entries else z3.RealVal(0)


def amount(value, observer, goods):
    return add(value[observer, good] for good in goods)


def base_utility(value, agent):
    return amount(value, agent, BASE_BUNDLES[agent])


def tail_constraints(value, observer, goods, bound):
    return [
        bound >= amount(value, observer, tuple(g for g in goods if g != removed))
        for removed in goods
    ]


def lex_greater(left, right):
    return z3.Or(*(
        z3.And(
            *(left[index] == right[index] for index in range(position)),
            left[position] > right[position],
        )
        for position in range(len(left))
    ))


def build_master():
    value = {
        (agent, good): z3.Real(f"v_{agent}_{good}")
        for agent in AGENTS for good in GOODS
    }
    solver = z3.SolverFor("QF_LRA")
    for entry in value.values():
        solver.add(entry >= 1)

    base = {agent: base_utility(value, agent) for agent in AGENTS}
    for observer in AGENTS:
        for goods in BASE_BUNDLES.values():
            solver.add(*tail_constraints(value, observer, goods, base[observer]))
        solver.add(base[observer] >= value[observer, "f"])
        for goods in DISPLAYED_BUNDLES.values():
            solver.add(*tail_constraints(value, observer, goods, base[observer]))

    for name, source in DESIRED_SOURCES.items():
        solver.add(amount(value, source, DISPLAYED_BUNDLES[name]) > base[source])

    solver.add(base["r"] > amount(value, "r", BASE_BUNDLES["q"]))
    solver.add(base["q"] > amount(value, "q", BASE_BUNDLES["r"]))
    for observer in ("r", "q", "s"):
        solver.add(base[observer] > amount(value, observer, BASE_BUNDLES["c"]))

    solver.add(value["q", "bq"] > value["q", "br"])
    return solver, value, base


def model_values(model, value):
    return {
        agent: {
            good: Fraction(str(model.eval(value[agent, good], model_completion=True)))
            for good in GOODS
        }
        for agent in AGENTS
    }


def numeric_amount(values, observer, goods):
    return sum((values[observer][good] for good in goods), Fraction(0))


def improvement_condition(utilities, base, target):
    if target == "flexible":
        return z3.And(utilities["r"] >= base["r"], utilities["q"] > base["q"])
    return lex_greater(
        tuple(utilities[agent] for agent in AGENTS),
        tuple(base[agent] for agent in AGENTS),
    )


def find_rivals(values, limit, target):
    recipient_index = {recipient: index for index, recipient in enumerate(RECIPIENTS)}
    owner = {good: z3.Int(f"owner_{good}") for good in GOODS}
    solver = z3.Solver()
    for good in GOODS:
        solver.add(owner[good] >= 0, owner[good] < len(RECIPIENTS))

    def assigned_amount(observer, recipient):
        return add(
            z3.If(
                owner[good] == recipient_index[recipient],
                z3.RealVal(str(values[observer][good])),
                0,
            )
            for good in GOODS
        )

    own = {agent: assigned_amount(agent, agent) for agent in AGENTS}
    for observer in AGENTS:
        for target_owner in AGENTS:
            target_total = assigned_amount(observer, target_owner)
            for good in GOODS:
                solver.add(z3.Implies(
                    owner[good] == recipient_index[target_owner],
                    own[observer]
                    >= target_total - z3.RealVal(str(values[observer][good])),
                ))
        solver.add(own[observer] >= assigned_amount(observer, "_"))

    base = {
        agent: numeric_amount(values, agent, BASE_BUNDLES[agent])
        for agent in AGENTS
    }
    solver.add(improvement_condition(
        own,
        {agent: z3.RealVal(str(base[agent])) for agent in AGENTS},
        target,
    ))
    allocations = []
    while len(allocations) < limit:
        checked = solver.check()
        if checked != z3.sat:
            return checked, allocations
        model = solver.model()
        allocation = {
            recipient: tuple(
                good
                for good in GOODS
                if model.eval(owner[good], model_completion=True).as_long()
                == recipient_index[recipient]
            )
            for recipient in RECIPIENTS
        }
        allocations.append(allocation)
        solver.add(z3.Or(*(
            owner[good] != model.eval(owner[good], model_completion=True)
            for good in GOODS
        )))
    return z3.sat, allocations


def rival_blocker(value, base, allocation, target):
    own = {
        agent: amount(value, agent, allocation[agent])
        for agent in AGENTS
    }
    efx = []
    for observer in AGENTS:
        for target_owner in AGENTS:
            efx.extend(tail_constraints(
                value, observer, allocation[target_owner], own[observer]
            ))
        efx.append(own[observer] >= amount(value, observer, allocation["_"]))
    better = improvement_condition(own, base, target)
    return z3.Not(z3.And(*efx, better))


def subset_ties(values):
    ties = set()
    subsets = tuple(
        tuple(GOODS[index] for index in range(len(GOODS)) if mask & (1 << index))
        for mask in range(1 << len(GOODS))
    )
    for agent in AGENTS:
        totals = {}
        for goods in subsets:
            total = numeric_amount(values, agent, goods)
            if total in totals:
                left = set(totals[total])
                right = set(goods)
                signature = tuple(
                    1 if good in left - right else -1 if good in right - left else 0
                    for good in GOODS
                )
                if next(entry for entry in signature if entry) < 0:
                    signature = tuple(-entry for entry in signature)
                ties.add((agent, signature))
            else:
                totals[total] = goods
    return ties


def tie_blocker(value, tie):
    agent, signature = tie
    return add(
        coefficient * value[agent, good]
        for coefficient, good in zip(signature, GOODS)
        if coefficient
    ) != 0


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(max_iterations, time_limit_s, rivals_per_iteration, target):
    solver, value, base = build_master()
    started = time.time()
    rivals = []
    tie_constraints = 0
    tie_set = set()
    trace = []
    status = "ITERATION_LIMIT"
    counterexample = None
    for iteration in range(1, max_iterations + 1):
        if time.time() - started > time_limit_s:
            status = "TIME_LIMIT"
            break
        checked = solver.check()
        if checked == z3.unsat:
            status = "UNSAT_MINIMAL_FLOWER"
            break
        if checked != z3.sat:
            status = "MASTER_UNKNOWN"
            break
        values = model_values(solver.model(), value)
        ties = subset_ties(values) - tie_set
        if ties:
            for tie in ties:
                solver.add(tie_blocker(value, tie))
            tie_set.update(ties)
            tie_constraints += len(ties)
            trace.append({
                "iteration": iteration,
                "kind": "nondegeneracy",
                "new_tie_constraints": len(ties),
                "ties": [
                    {"agent": agent, "signature": list(signature)}
                    for agent, signature in sorted(ties)
                ],
            })
            print(
                f"iteration={iteration} ties={len(ties)} pool={len(rivals)}",
                flush=True,
            )
            continue
        rival_status, allocations = find_rivals(
            values, rivals_per_iteration, target
        )
        if rival_status == z3.unsat and not allocations:
            status = "EXACT_BRIDGE_COUNTEREXAMPLE"
            counterexample = values
            trace.append({
                "iteration": iteration,
                "kind": "counterexample",
                "rival_pool_size": len(rivals),
            })
            break
        if rival_status not in (z3.sat, z3.unsat):
            status = "RIVAL_UNKNOWN"
            break
        for allocation in allocations:
            solver.add(rival_blocker(value, base, allocation, target))
            rivals.append(allocation)
        trace.append({
            "iteration": iteration,
            "kind": "rival",
            "allocation_count": len(allocations),
            "allocations": [
                {key: list(goods) for key, goods in allocation.items()}
                for allocation in allocations
            ],
        })
        print(
            f"iteration={iteration} added={len(allocations)} pool={len(rivals)}",
            flush=True,
        )

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "minimal-flower-global-lex-cegar-v1",
        "status": status,
        "solver": f"Z3 {z3.get_version_string()}",
        "target": target,
        "iterations": len(trace),
        "rival_pool_size": len(rivals),
        "nondegeneracy_constraints": tie_constraints,
        "elapsed_seconds": time.time() - started,
        "values": (
            {
                agent: {good: str(entry) for good, entry in row.items()}
                for agent, row in counterexample.items()
            }
            if counterexample is not None else None
        ),
        "trace": trace,
        "claim_boundary": (
            "an EXACT_BRIDGE_COUNTEREXAMPLE in flexible mode refutes the flexible "
            "completion statement in one positive nondegenerate minimal full-capture "
            "GG flower; UNSAT_MINIMAL_FLOWER proves that bounded symbolic cell only "
            "and is intended for analytic proof mining, not as a cap-free theorem"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-iterations", type=int, default=10000)
    parser.add_argument("--time-limit", type=float, default=1800)
    parser.add_argument("--rivals-per-iteration", type=int, default=64)
    parser.add_argument(
        "--target", choices=("flexible", "global-lex"), default="flexible"
    )
    args = parser.parse_args()
    result = run(
        args.max_iterations,
        args.time_limit,
        args.rivals_per_iteration,
        args.target,
    )
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "iterations": result["iterations"],
        "rival_pool_size": result["rival_pool_size"],
        "nondegeneracy_constraints": result["nondegeneracy_constraints"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
