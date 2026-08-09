#!/usr/bin/env python3
"""Exact dominance construction for refuting the strict same-offer bridge."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .run_alternating_split_packet_cegar import (
        BASE_BUNDLES,
        BASE_OWNER,
        FLOATER,
        GOODS,
        M,
        concrete_rival_blocker,
        desired_expression,
        integerize_model,
        numeric_efx,
        numeric_utilities,
        structural_solver,
        subset_sum,
    )
except ImportError:
    from run_alternating_split_packet_cegar import (
        BASE_BUNDLES,
        BASE_OWNER,
        FLOATER,
        GOODS,
        M,
        concrete_rival_blocker,
        desired_expression,
        integerize_model,
        numeric_efx,
        numeric_utilities,
        structural_solver,
        subset_sum,
    )


SCHEMA = "alternating-strict-bridge-dominance-v1"
ORDER = (0, 2, 3, 1)
X = BASE_BUNDLES[0][0]
Y = BASE_BUNDLES[2][0]
OFFER = BASE_BUNDLES[1] + (FLOATER,)
OUTSIDE_ACTIVE = (2, 5, 6, 7)
OUTSIDE_OWNER = (1, 1, 0, None, None, 0, 0, 0, 3, 2, 1)


def powerset(pool):
    for size in range(1, len(pool) + 1):
        yield from itertools.combinations(pool, size)


def tau_exceeds(values, observer, bundle, bound):
    return z3.Or(
        *(
            bound
            < subset_sum(
                values,
                observer,
                tuple(good for good in bundle if good != removed),
            )
            for removed in bundle
        )
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decide(
    timeout_seconds: int,
    enforce_promotion: bool = True,
    enforce_s: bool = True,
    enforce_q: bool = True,
) -> dict:
    solver, values, own = structural_solver()
    solver.set(timeout=max(1, timeout_seconds * 1000))
    solver.add(desired_expression(values, own, 0, OUTSIDE_ACTIVE))
    solver.add(z3.Not(concrete_rival_blocker(values, own, OUTSIDE_OWNER, ORDER)))

    # If p receives a desired subset E of the original offer, every bundle
    # disjoint from E and y is too small for both r and s to tolerate E.
    # Hence both would need the unique good y, so no such EFX allocation exists.
    promotion_conditions = 0
    all_goods = tuple(range(M))
    for active in powerset(OFFER):
        available_without_y = tuple(
            good for good in all_goods if good not in active and good != Y
        )
        condition = desired_expression(values, own, 0, active)
        if enforce_promotion:
            solver.add(
                z3.Implies(
                    condition,
                    tau_exceeds(
                        values,
                        1,
                        active,
                        subset_sum(values, 1, available_without_y),
                    ),
                )
            )
            solver.add(
                z3.Implies(
                    condition,
                    tau_exceeds(
                        values,
                        2,
                        active,
                        subset_sum(values, 2, available_without_y),
                    ),
                )
            )
        promotion_conditions += 1

    # Rooted lex improvement at s: q cannot tolerate s's bundle using all
    # goods still available after fixing p=x.
    residual = tuple(good for good in all_goods if good != X)
    s_conditions = 0
    for active in powerset(residual):
        q_available = tuple(
            good for good in residual if good not in active
        )
        if enforce_s:
            solver.add(
                z3.Implies(
                    subset_sum(values, 2, active) > own[2],
                    tau_exceeds(
                        values,
                        3,
                        active,
                        subset_sum(values, 3, q_available),
                    ),
                )
            )
        if enforce_s and active != (Y,):
            total = subset_sum(values, 2, active)
            solver.add(z3.Or(total < own[2], total > own[2]))
        s_conditions += 1

    # If s keeps y and q strictly improves, r cannot tolerate q's bundle
    # using every good left after fixing x,y. Equality at q is unique to X_q.
    suffix_pool = tuple(good for good in all_goods if good not in (X, Y))
    q_conditions = 0
    for active in powerset(suffix_pool):
        r_available = tuple(
            good for good in suffix_pool if good not in active
        )
        if enforce_q:
            solver.add(
                z3.Implies(
                    subset_sum(values, 3, active) > own[3],
                    tau_exceeds(
                        values,
                        1,
                        active,
                        subset_sum(values, 1, r_available),
                    ),
                )
            )
        if enforce_q and active != BASE_BUNDLES[3]:
            total = subset_sum(values, 3, active)
            solver.add(z3.Or(total < own[3], total > own[3]))
        q_conditions += 1

    checked = solver.check()
    result = {
        "schema": SCHEMA,
        "solver_status": str(checked),
        "promotion_condition_count": promotion_conditions,
        "s_condition_count": s_conditions,
        "q_condition_count": q_conditions,
        "outside_active": [GOODS[good] for good in OUTSIDE_ACTIVE],
        "outside_owner": list(OUTSIDE_OWNER),
        "enforced_blocks": {
            "promotion": enforce_promotion,
            "s_improvement": enforce_s,
            "q_improvement": enforce_q,
        },
        "claim_boundary": {
            "sat": (
                "candidate unrestricted strict-bridge counterexample; exhaustive "
                "rooted/promoted replay is still required"
            ),
            "unsat": "refutes only this dominance construction",
            "unknown": "no mathematical decision",
        },
    }
    if checked == z3.sat:
        model = integerize_model(solver.model(), values)
        if not numeric_efx(model, OUTSIDE_OWNER):
            raise AssertionError("outside allocation did not replay as EFX")
        base = numeric_utilities(model, BASE_OWNER)
        outside = numeric_utilities(model, OUTSIDE_OWNER)
        result.update(
            {
                "status": "SAT_DOMINANCE_COUNTEREXAMPLE_CANDIDATE",
                "values": [list(row) for row in model],
                "base_utilities": list(base),
                "outside_utilities": list(outside),
            }
        )
    elif checked == z3.unsat:
        result["status"] = "UNSAT_DOMINANCE_CONSTRUCTION"
    else:
        result.update({"status": "UNKNOWN", "reason_unknown": solver.reason_unknown()})
    script = Path(__file__).resolve()
    result["provenance"] = {
        "script": str(script.relative_to(script.parents[2])),
        "script_sha256": sha256(script),
        "z3_version": z3.get_version_string(),
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--omit-promotion", action="store_true")
    parser.add_argument("--omit-s", action="store_true")
    parser.add_argument("--omit-q", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = decide(
        args.timeout_seconds,
        not args.omit_promotion,
        not args.omit_s,
        not args.omit_q,
    )
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(args.output)
    print(json.dumps({key: result[key] for key in ("status", "solver_status")}, indent=2))


if __name__ == "__main__":
    main()
