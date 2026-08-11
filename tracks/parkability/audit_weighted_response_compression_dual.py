#!/usr/bin/env python3
"""Audit weighted response-compression identities and dual weak bounds."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    own, budget, cost, residual = z3.Reals("own budget cost residual")
    payment = z3.SolverFor("QF_LRA")
    payment.add(
        own > 0,
        budget > 0,
        cost >= 0,
        residual == own + budget - cost,
        cost <= budget,
        residual < own,
    )
    payment_status = str(payment.check())
    assert payment_status == "unsat"

    obstruction = z3.SolverFor("QF_LRA")
    obstruction.add(
        own > 0,
        budget > 0,
        cost >= 0,
        residual == own + budget - cost,
        residual < own,
        cost <= budget,
    )
    obstruction_status = str(obstruction.check())
    assert obstruction_status == "unsat"

    margin, old_core, new_core = z3.Reals("margin old_core new_core")
    recapture = z3.SolverFor("QF_LRA")
    recapture.add(
        margin >= 0,
        old_core > 0,
        new_core > 0,
        new_core - old_core <= margin,
        margin + old_core - new_core < 0,
    )
    recapture_status = str(recapture.check())
    assert recapture_status == "unsat"

    alphas = z3.Reals("alpha_0 alpha_1 alpha_2 alpha_3")
    betas = z3.Reals("beta_0 beta_1 beta_2 beta_3")
    edge_costs = z3.Reals("edge_cost_0 edge_cost_1 edge_cost_2 edge_cost_3")
    dual_bound = z3.SolverFor("QF_LRA")
    dual_bound.add(
        *(edge_cost >= 0 for edge_cost in edge_costs),
        *(
            alphas[index] + betas[index] <= edge_costs[index]
            for index in range(4)
        ),
        z3.Sum(alphas) + z3.Sum(betas) > z3.Sum(edge_costs),
    )
    dual_status = str(dual_bound.check())
    assert dual_status == "unsat"

    observer_utility, base_utility, safe_threshold = z3.Reals(
        "observer_utility base_utility safe_threshold"
    )
    one_wall = z3.SolverFor("QF_LRA")
    one_wall.add(
        observer_utility >= base_utility,
        base_utility >= safe_threshold,
        observer_utility < safe_threshold,
    )
    one_wall_status = str(one_wall.check())
    assert one_wall_status == "unsat"

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "weighted-response-compression-dual-audit-v1",
        "status": "ALL_FORCED",
        "scalar_records": [
            {"claim": "cost_at_most_budget_pays_residual", "status": payment_status},
            {"claim": "unpaid_residual_forces_cost_above_budget", "status": obstruction_status},
            {"claim": "recapture_margin_is_exact", "status": recapture_status},
            {"claim": "assignment_dual_is_bounded_by_every_matching", "status": dual_status},
            {"claim": "common_safe_cores_leave_only_residual_wall", "status": one_wall_status},
        ],
        "claim_boundary": (
            "QF_LRA audit of payment, recapture, one-wall, and weak-duality "
            "identities; minimum-cost assignment integrality/strong duality "
            "is the standard bipartite assignment theorem"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "z3_version": z3.get_version_string(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"]}, indent=2))


if __name__ == "__main__":
    main()
