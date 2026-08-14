#!/usr/bin/env python3
"""Extract a categorized full-premise core for the bounded allocated-E R2 theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

from .run_allocated_e_capture_rank_three_cegar import (
    ALLOCATED_E_BASE,
    FIXED_CORES,
    build_master,
    fixed_core_anchored_pi_free_constraints,
    generalized_self_pi_free_constraints,
    pairwise_closed_core_pi_free_constraints,
)
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, PACKETS
from .run_full_capture_rank_three_cegar import ordinary_pi_free_constraints
from .run_generalized_pi_named_selector_cegar import generalized_pi_cut


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "results" / "allocated_e_form0_pi_greedy_minimal_core.json"


def assertion_categories(value):
    categories = []
    for good, owner in value:
        categories.extend((f"positive_lower:{good}:{owner}", f"positive_upper:{good}:{owner}"))
    for owner in OWNERS:
        categories.append(f"base_normalization:{owner}")
        categories.append(f"base_charity_efx:{owner}")
        categories.extend(
            f"base_owner_efx:{owner}:{target}"
            for target in OWNERS if target != owner
        )
    categories.extend(
        f"ordinary_pi:{index}"
        for index, _ in enumerate(ordinary_pi_free_constraints(value, ALLOCATED_E_BASE))
    )
    categories.extend(
        f"generalized_self_pi:{index}"
        for index, _ in enumerate(generalized_self_pi_free_constraints(value))
    )
    categories.extend(f"fixed_response:{source}" for source in FIXED_CORES)
    anchored, _ = fixed_core_anchored_pi_free_constraints(value)
    categories.extend(f"fixed_anchored_pi:{index}" for index, _ in enumerate(anchored))
    pairwise = pairwise_closed_core_pi_free_constraints(value)
    categories.extend(f"pairwise_closed_pi:{index}" for index, _ in enumerate(pairwise))
    selected_union = set(PACKETS["A"]) | set(PACKETS["Q"]) | set(PACKETS["E"])
    complement_count = (1 << (len(GOODS) - len(selected_union))) - 1
    categories.extend(f"d_complement_capture:{index}" for index in range(complement_count))
    categories.append("d_Q_response")
    categories.extend(f"d_QH_tail:{good}" for good in PACKETS["Q"])
    categories.extend(("d_wall_A", "d_wall_Q", "d_wall_E", "d_wall_P"))
    categories.append("rank_at_most_three")
    categories.extend(
        f"exact_response_relation:{source}:{target}"
        for source in OWNERS for target in (*OWNERS, "charity")
        if source != target
    )
    return categories


def run(output: Path, timeout_seconds: int, random_seed: int):
    source = json.loads(SOURCE.read_text())
    base_solver, value = build_master(0)
    assertions = list(base_solver.assertions())
    categories = assertion_categories(value)
    if len(categories) != len(assertions):
        raise AssertionError((len(categories), len(assertions)))

    solver = z3.SolverFor("QF_LRA")
    labels = []
    records = []
    for position, (category, assertion) in enumerate(zip(categories, assertions, strict=True)):
        label = z3.Bool(f"base_assertion_{position}")
        solver.add(z3.Implies(label, assertion))
        labels.append(label)
        records.append({
            "kind": "base",
            "position": position,
            "category": category,
            "formula": assertion.sexpr(),
        })
    for position, row in enumerate(source["core"]):
        label = z3.Bool(f"higher_family_{position}")
        cut = generalized_pi_cut(value, row["witness"])
        solver.add(z3.Implies(label, cut))
        labels.append(label)
        records.append({
            "kind": "higher_family",
            "position": position,
            "original_index": row["index"],
            "signature": row["signature"],
            "formula": cut.sexpr(),
        })
    solver.set(
        timeout=timeout_seconds * 1000,
        random_seed=random_seed,
        unsat_core=True,
        **{"smt.core.minimize": True},
    )
    status = solver.check(*labels)
    result = {
        "schema": "allocated-e-form0-full-unsat-core-v1",
        "status": str(status),
        "solver": f"Z3 {z3.get_version_string()}",
        "random_seed": random_seed,
        "timeout_seconds": timeout_seconds,
        "source": "results/allocated_e_form0_pi_greedy_minimal_core.json",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "source_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "base_assertion_count": len(assertions),
        "higher_family_count": len(source["core"]),
        "claim_boundary": (
            "Categorized SMT core for one bounded allocated-E R2 master. "
            "It is a proof-discovery artifact, not a cap-free theorem."
        ),
    }
    if status == z3.unsat:
        by_name = {str(label): record for label, record in zip(labels, records, strict=True)}
        core = [by_name[str(label)] for label in solver.unsat_core()]
        result["core_count"] = len(core)
        result["core"] = core
    elif status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--random-seed", type=int, default=8663)
    args = parser.parse_args()
    result = run(args.output, args.timeout_seconds, args.random_seed)
    print(json.dumps({
        "status": result["status"],
        "base_assertion_count": result["base_assertion_count"],
        "higher_family_count": result["higher_family_count"],
        "core_count": result.get("core_count"),
        "reason_unknown": result.get("reason_unknown"),
    }, indent=2))


if __name__ == "__main__":
    main()
