#!/usr/bin/env python3
"""Exact split-packet CEGAR for the anchored-or-promoted escape target."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import z3

try:
    from .audit_threshold_two_slot_refutation import VALUES as THRESHOLD_PROFILE
    from .run_alternating_global_lex_cegar import AGENTS, atomic_json
    from .run_alternating_split_packet_cegar import (
        BASE_BUNDLES,
        BASE_OWNER,
        FLOATER,
        M,
        N,
        concrete_rival_blocker,
        desired_expression,
        integerize_model,
        numeric_efx,
        numeric_utilities,
        structural_solver,
    )
except ImportError:
    from audit_threshold_two_slot_refutation import VALUES as THRESHOLD_PROFILE
    from run_alternating_global_lex_cegar import AGENTS, atomic_json
    from run_alternating_split_packet_cegar import (
        BASE_BUNDLES,
        BASE_OWNER,
        FLOATER,
        M,
        N,
        concrete_rival_blocker,
        desired_expression,
        integerize_model,
        numeric_efx,
        numeric_utilities,
        structural_solver,
    )


SCHEMA = "alternating-anchored-or-promoted-split-cegar-v2"
POOL_SCHEMA = "alternating-anchored-or-promoted-split-pool-v2"
Owner = tuple[int | None, ...]


def root_data(root: int) -> tuple[int, tuple[int, ...]]:
    if root == 0:
        return BASE_BUNDLES[0][0], (0, 1, FLOATER)
    if root == 2:
        return BASE_BUNDLES[2][0], (4, 5, FLOATER)
    raise ValueError("root must be singleton owner p=0 or s=2")


def root_offer(root: int) -> tuple[int, ...]:
    if root == 0:
        return BASE_BUNDLES[1] + (FLOATER,)
    if root == 2:
        return BASE_BUNDLES[3] + (FLOATER,)
    raise ValueError("root must be singleton owner p=0 or s=2")


def envy_return(root: int) -> tuple[int, int]:
    if root == 0:
        return 1, BASE_BUNDLES[2][0]
    if root == 2:
        return 3, BASE_BUNDLES[0][0]
    raise ValueError("root must be singleton owner p=0 or s=2")


def numeric_mode(owner: Owner, root: int, promotion_mode: str = "selected") -> str | None:
    singleton, selected = root_data(root)
    owned = tuple(good for good, assigned in enumerate(owner) if assigned == root)
    if owned == (singleton,):
        return "anchored"
    if promotion_mode == "none":
        return None
    if promotion_mode == "selected" and owned == selected:
        return "promoted"
    if promotion_mode == "any-desired" and owned and set(owned).issubset(root_offer(root)):
        return "promoted"
    return None


def numeric_desired(values, owner: Owner, root: int) -> bool:
    owned = tuple(good for good, assigned in enumerate(owner) if assigned == root)
    base = numeric_utilities(values, BASE_OWNER)
    return (
        set(owned).issubset(root_offer(root))
        and sum(values[root][good] for good in owned) > base[root]
        and all(
            sum(values[observer][good] for good in owned if good != removed)
            <= base[observer]
            for observer in range(N)
            for removed in owned
        )
    )


def numeric_anchor_valid(owner: Owner, root: int, anchor_mode: str) -> bool:
    if numeric_mode(owner, root, "any-desired") != "anchored":
        return False
    if anchor_mode == "root-only":
        return True
    return_agent, return_good = envy_return(root)
    return tuple(good for good, assigned in enumerate(owner) if assigned == return_agent) == (
        return_good,
    )


def restricted_rival_blocker(
    values,
    base_own,
    owner: Owner,
    order: tuple[int, ...],
    promotion_mode: str,
):
    blocker = concrete_rival_blocker(values, base_own, owner, order)
    root = order[0]
    if numeric_mode(owner, root, promotion_mode) != "promoted":
        return blocker
    root_bundle = tuple(good for good, assigned in enumerate(owner) if assigned == root)
    return z3.Or(
        z3.Not(desired_expression(values, base_own, root, root_bundle)),
        blocker,
    )


def find_restricted_rivals(
    values: tuple[tuple[int, ...], ...],
    order: tuple[int, ...],
    timeout_seconds: int,
    limit: int,
    promotion_mode: str = "selected",
    anchor_mode: str = "root-only",
) -> tuple[str, list[Owner], list[tuple[int, ...]], list[str], str | None]:
    root = order[0]
    singleton, selected = root_data(root)
    owner = tuple(z3.Int(f"restricted_owner_{good}") for good in range(M))
    solver = z3.SolverFor("QF_LIA")
    solver.set(timeout=timeout_seconds * 1000)
    solver.add(*(z3.And(variable >= 0, variable <= N) for variable in owner))

    utilities = tuple(
        z3.Sum(
            *(z3.If(owner[good] == agent, values[agent][good], 0) for good in range(M))
        )
        for agent in range(N)
    )
    target_values = tuple(
        tuple(
            z3.Sum(
                *(z3.If(owner[good] == target, values[observer][good], 0)
                  for good in range(M))
            )
            for target in range(N)
        )
        for observer in range(N)
    )
    base = numeric_utilities(values, BASE_OWNER)
    anchored_terms = [
        owner[singleton] == root,
        *(owner[good] != root for good in range(M) if good != singleton),
    ]
    if anchor_mode == "root-return":
        return_agent, return_good = envy_return(root)
        anchored_terms.extend(
            [
                owner[return_good] == return_agent,
                *(owner[good] != return_agent for good in range(M) if good != return_good),
            ]
        )
    elif anchor_mode != "root-only":
        raise ValueError("anchor_mode must be root-only or root-return")
    anchored = z3.And(*anchored_terms)
    if promotion_mode == "none":
        promoted = z3.BoolVal(False)
    elif promotion_mode == "selected":
        promoted = z3.And(
            *(owner[good] == root for good in selected),
            *(owner[good] != root for good in range(M) if good not in selected),
        )
    elif promotion_mode == "any-desired":
        offer = root_offer(root)
        promoted = z3.And(
            *(owner[good] != root for good in range(M) if good not in offer),
            utilities[root] > base[root],
            *(
                z3.Implies(
                    owner[removed] == root,
                    target_values[observer][root] - values[observer][removed]
                    <= base[observer],
                )
                for observer in range(N)
                for removed in offer
            ),
        )
    else:
        raise ValueError("promotion_mode must be none, selected, or any-desired")
    solver.add(z3.Or(anchored, promoted))

    for observer in range(N):
        for target in range(N):
            for removed in range(M):
                solver.add(
                    z3.Implies(
                        owner[removed] == target,
                        utilities[observer]
                        >= target_values[observer][target] - values[observer][removed],
                    )
                )

    solver.add(
        z3.Or(
            *(
                z3.And(
                    *(utilities[order[prefix]] == base[order[prefix]]
                      for prefix in range(index)),
                    utilities[agent] > base[agent],
                )
                for index, agent in enumerate(order)
            )
        )
    )

    found = []
    found_utilities = []
    modes = []
    while len(found) < limit:
        checked = solver.check()
        if checked == z3.unsat:
            return ("unsat" if not found else "sat"), found, found_utilities, modes, None
        if checked != z3.sat:
            return ("unknown" if not found else "sat"), found, found_utilities, modes, solver.reason_unknown()
        model = solver.model()
        concrete = tuple(
            None if model.eval(variable).as_long() == N else model.eval(variable).as_long()
            for variable in owner
        )
        mode = numeric_mode(concrete, root, promotion_mode)
        if (
            mode is None
            or (mode == "anchored" and not numeric_anchor_valid(concrete, root, anchor_mode))
            or (mode == "promoted" and promotion_mode == "any-desired"
                and not numeric_desired(values, concrete, root))
            or not numeric_efx(values, concrete)
        ):
            raise AssertionError("restricted finder returned an invalid rival")
        utility = numeric_utilities(values, concrete)
        if tuple(utility[agent] for agent in order) <= tuple(base[agent] for agent in order):
            raise AssertionError("restricted finder returned a non-dominator")
        found.append(concrete)
        found_utilities.append(utility)
        modes.append(mode)
        solver.add(
            z3.Or(
                *(variable != (N if assigned is None else assigned)
                  for variable, assigned in zip(owner, concrete))
            )
        )
    return "sat", found, found_utilities, modes, None


def load_pool(
    path: Path, order: tuple[int, ...], promotion_mode: str, anchor_mode: str
) -> list[Owner]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text())
    if (
        payload.get("schema") != POOL_SCHEMA
        or payload.get("agent_order") != list(order)
        or payload.get("promotion_mode", "selected") != promotion_mode
        or payload.get("anchor_mode", "root-only") != anchor_mode
    ):
        raise ValueError("pool metadata mismatch")
    rivals = [tuple(owner) for owner in payload["rivals"]]
    if len(rivals) != len(set(rivals)):
        raise ValueError("duplicate rival in pool")
    if any(
        numeric_mode(owner, order[0], promotion_mode) is None
        or (
            numeric_mode(owner, order[0], promotion_mode) == "anchored"
            and not numeric_anchor_valid(owner, order[0], anchor_mode)
        )
        for owner in rivals
    ):
        raise ValueError("pool contains a rival outside the restricted family")
    return rivals


def save_pool(
    path: Path,
    order: tuple[int, ...],
    promotion_mode: str,
    anchor_mode: str,
    rivals: list[Owner],
) -> None:
    atomic_json(
        path,
        {
            "schema": POOL_SCHEMA,
            "agent_order": list(order),
            "promotion_mode": promotion_mode,
            "anchor_mode": anchor_mode,
            "rivals": [list(owner) for owner in rivals],
        },
    )


def run(
    order: tuple[int, ...],
    pool_path: Path,
    result_path: Path,
    max_iterations: int,
    master_timeout_seconds: int,
    rival_timeout_seconds: int,
    rivals_per_iteration: int,
    promotion_mode: str = "selected",
    anchor_mode: str = "root-only",
) -> dict:
    solver, values, own = structural_solver()
    solver.set(timeout=master_timeout_seconds * 1000)
    rivals = load_pool(pool_path, order, promotion_mode, anchor_mode)
    rival_set = set(rivals)

    _, seeds, _, _, _ = find_restricted_rivals(
        THRESHOLD_PROFILE,
        order,
        rival_timeout_seconds,
        rivals_per_iteration,
        promotion_mode,
        anchor_mode,
    )
    for owner in seeds:
        if owner not in rival_set:
            rivals.append(owner)
            rival_set.add(owner)
    for owner in rivals:
        solver.add(
            restricted_rival_blocker(
                values, own, owner, order, promotion_mode
            )
        )
    save_pool(pool_path, order, promotion_mode, anchor_mode, rivals)

    started = time.time()
    trace = []
    status = "ITERATION_LIMIT"
    final_values = None
    reason_unknown = None
    for iteration in range(1, max_iterations + 1):
        checked = solver.check()
        if checked == z3.unsat:
            status = "UNSAT_RESTRICTED_SPLIT_PACKET_CELL"
            break
        if checked != z3.sat:
            status = "MASTER_UNKNOWN"
            reason_unknown = solver.reason_unknown()
            break
        model_values = integerize_model(solver.model(), values)
        rival_status, found, utilities, modes, rival_reason = find_restricted_rivals(
            model_values,
            order,
            rival_timeout_seconds,
            rivals_per_iteration,
            promotion_mode,
            anchor_mode,
        )
        unseen = [owner for owner in found if owner not in rival_set]
        trace.append(
            {
                "iteration": iteration,
                "pool_size_before": len(rivals),
                "rival_status": rival_status,
                "found_count": len(found),
                "anchored_count": modes.count("anchored"),
                "promoted_count": modes.count("promoted"),
                "new_count": len(unseen),
                "rival_reason_unknown": rival_reason,
                "values": [list(row) for row in model_values],
                "rival_utilities": [list(utility) for utility in utilities],
            }
        )
        print(
            f"iteration={iteration} pool={len(rivals)} found={len(found)} "
            f"anchored={modes.count('anchored')} promoted={modes.count('promoted')} "
            f"new={len(unseen)}",
            flush=True,
        )
        if rival_status == "unsat":
            status = "SAT_NO_ANCHORED_OR_PROMOTED_ESCAPE"
            final_values = model_values
            break
        if rival_status == "unknown":
            status = "RIVAL_UNKNOWN"
            final_values = model_values
            reason_unknown = rival_reason
            break
        if not unseen:
            raise AssertionError("a pooled restricted rival still dominates the model")
        for owner in unseen:
            solver.add(
                restricted_rival_blocker(
                    values, own, owner, order, promotion_mode
                )
            )
            rivals.append(owner)
            rival_set.add(owner)
        save_pool(pool_path, order, promotion_mode, anchor_mode, rivals)

    result = {
        "schema": SCHEMA,
        "status": status,
        "claim_boundary": {
            "sat": "refutes the anchored-or-promoted target only in the exact eleven-good split-packet cell",
            "unsat": "proves the target only in the exact eleven-good split-packet cell until a cap-free argument is supplied",
        },
        "agent_order": list(order),
        "agent_order_names": [AGENTS[agent] for agent in order],
        "promotion_mode": promotion_mode,
        "anchor_mode": anchor_mode,
        "iterations": len(trace),
        "pool_size": len(rivals),
        "elapsed_seconds": time.time() - started,
        "reason_unknown": reason_unknown,
        "values": None if final_values is None else [list(row) for row in final_values],
        "trace": trace,
        "solver": {"name": "z3", "version": z3.get_version_string(), "logic": "QF_LRA/QF_LIA"},
    }
    atomic_json(result_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-order", default="0,3,1,2")
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--max-iterations", type=int, default=100)
    parser.add_argument("--master-timeout-seconds", type=int, default=120)
    parser.add_argument("--rival-timeout-seconds", type=int, default=60)
    parser.add_argument("--rivals-per-iteration", type=int, default=64)
    parser.add_argument(
        "--promotion-mode",
        choices=("none", "selected", "any-desired"),
        default="selected",
    )
    parser.add_argument(
        "--anchor-mode", choices=("root-only", "root-return"), default="root-only"
    )
    args = parser.parse_args()
    order = tuple(int(field) for field in args.agent_order.split(","))
    if sorted(order) != list(range(N)) or order[0] not in (0, 2):
        parser.error("order must be a permutation rooted at p=0 or s=2")
    if args.result.exists():
        parser.error("result path must not exist")
    result = run(
        order,
        args.pool,
        args.result,
        args.max_iterations,
        args.master_timeout_seconds,
        args.rival_timeout_seconds,
        args.rivals_per_iteration,
        args.promotion_mode,
        args.anchor_mode,
    )
    print(json.dumps({key: result[key] for key in ("status", "iterations", "pool_size", "elapsed_seconds")}, indent=2))


if __name__ == "__main__":
    main()
