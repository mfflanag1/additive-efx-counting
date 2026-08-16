#!/usr/bin/env python3
"""Exact CEGAR for a blocked strict lex-max one-unallocated EFX state."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from . import core
    from .anneal import atomic_json
    from .lra_master import ParkabilityLRAMaster
    from .normalize_smt2_for_cvc5 import atomic_write
except ImportError:
    import core
    from anneal import atomic_json
    from lra_master import ParkabilityLRAMaster
    from normalize_smt2_for_cvc5 import atomic_write


SCHEMA = "lexmax-partial-lra-cegar-v1"
POOL_SCHEMA = "lexmax-partial-rival-pool-v1"
Base = tuple[int, tuple[int | None, ...]]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bundles_of(
    base_owner: tuple[int | None, ...],
    n: int,
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(good for good, owner in enumerate(base_owner) if owner == agent)
        for agent in range(n)
    )


def subset_sum(
    master: ParkabilityLRAMaster,
    observer: int,
    goods: tuple[int, ...],
) -> z3.ArithRef:
    return z3.Sum(*(master.values[observer][good] for good in goods))


def lex_lt(
    left: tuple[z3.ArithRef, ...],
    right: tuple[z3.ArithRef, ...],
) -> z3.BoolRef:
    return z3.Or(
        *(
            z3.And(
                *(left[prefix] == right[prefix] for prefix in range(index)),
                left[index] < right[index],
            )
            for index in range(len(left))
        )
    )


def candidate_constraint_records(
    master: ParkabilityLRAMaster,
    floater: int,
    base_owner: tuple[int | None, ...],
) -> tuple[tuple[z3.ArithRef, ...], list[dict]]:
    bundles = bundles_of(base_owner, master.n)
    utilities = tuple(
        subset_sum(master, observer, bundles[observer])
        for observer in range(master.n)
    )
    records = []
    for observer in range(master.n):
        records.append(
            {
                "kind": "floater_nonenvy",
                "observer": observer,
                "constraint": (
                    utilities[observer] > master.values[observer][floater]
                ),
            }
        )
        for target in range(master.n):
            if observer == target:
                continue
            for removed in bundles[target]:
                remainder = tuple(
                    good for good in bundles[target] if good != removed
                )
                records.append(
                    {
                        "kind": "base_efx",
                        "observer": observer,
                        "target": target,
                        "removed": removed,
                        "constraint": (
                            utilities[observer]
                            > subset_sum(master, observer, remainder)
                        ),
                    }
                )
    for host in range(master.n):
        enlarged = bundles[host] + (floater,)
        records.append(
            {
                "kind": "blocked_host",
                "host": host,
                "constraint": z3.Or(
                    *(
                        utilities[observer]
                        < subset_sum(
                            master,
                            observer,
                            tuple(
                                good
                                for good in enlarged
                                if good != removed
                            ),
                        )
                        for observer in range(master.n)
                        if observer != host
                        for removed in enlarged
                    )
                ),
            }
        )
    return utilities, records


def add_candidate(
    master: ParkabilityLRAMaster,
    floater: int,
    base_owner: tuple[int | None, ...],
    activation: z3.BoolRef | None = None,
) -> tuple[z3.ArithRef, ...]:
    if activation is not None and not z3.is_bool(activation):
        raise ValueError("candidate activation must be Boolean")
    utilities, records = candidate_constraint_records(
        master,
        floater,
        base_owner,
    )
    master.solver.add(
        *(
            record["constraint"]
            if activation is None
            else z3.Implies(activation, record["constraint"])
            for record in records
        )
    )
    return utilities


def rival_blocker_expression(
    master: ParkabilityLRAMaster,
    candidate_utilities: tuple[z3.ArithRef, ...],
    candidate_base_owner: tuple[int | None, ...],
    rival: Base,
    agent_order: tuple[int, ...],
    lex_encoding: str,
) -> z3.BoolRef:
    floater, base_owner = rival
    bundles = bundles_of(base_owner, master.n)
    rival_utilities = tuple(
        subset_sum(master, observer, bundles[observer])
        for observer in range(master.n)
    )
    eligibility_failures = []
    for observer in range(master.n):
        eligibility_failures.append(
            rival_utilities[observer] < master.values[observer][floater]
        )
        for target in range(master.n):
            if observer == target:
                continue
            for removed in bundles[target]:
                remainder = tuple(
                    good for good in bundles[target] if good != removed
                )
                eligibility_failures.append(
                    rival_utilities[observer]
                    < subset_sum(master, observer, remainder)
                )
    if lex_encoding == "exact":
        lex_lower = lex_lt(
            tuple(rival_utilities[agent] for agent in agent_order),
            tuple(candidate_utilities[agent] for agent in agent_order),
        )
    elif lex_encoding == "bundle_nondegenerate":
        candidate_bundles = bundles_of(candidate_base_owner, master.n)
        first_changed = next(
            agent
            for agent in agent_order
            if bundles[agent] != candidate_bundles[agent]
        )
        lex_lower = (
            rival_utilities[first_changed]
            < candidate_utilities[first_changed]
        )
    else:
        raise ValueError("unknown lex encoding")
    return z3.Or(
        *eligibility_failures,
        lex_lower,
    )


def add_rival_blocker(
    master: ParkabilityLRAMaster,
    candidate_utilities: tuple[z3.ArithRef, ...],
    candidate_base_owner: tuple[int | None, ...],
    rival: Base,
    agent_order: tuple[int, ...],
    lex_encoding: str,
    activation: z3.BoolRef | None = None,
) -> None:
    if activation is not None and not z3.is_bool(activation):
        raise ValueError("rival-blocker activation must be Boolean")
    blocker = rival_blocker_expression(
        master,
        candidate_utilities,
        candidate_base_owner,
        rival,
        agent_order,
        lex_encoding,
    )
    master.solver.add(
        blocker
        if activation is None
        else z3.Implies(activation, blocker)
    )


def pool_document(
    n: int,
    m: int,
    candidate: Base,
    agent_order: tuple[int, ...],
    rivals: list[Base],
) -> dict:
    return {
        "schema": POOL_SCHEMA,
        "n": n,
        "m": m,
        "candidate": {
            "floater": candidate[0],
            "base_owner": list(candidate[1]),
        },
        "agent_order": list(agent_order),
        "rivals": [
            {"floater": floater, "base_owner": list(base_owner)}
            for floater, base_owner in rivals
        ],
    }


def load_pool(
    path: Path,
    n: int,
    m: int,
    candidate: Base,
    agent_order: tuple[int, ...],
) -> list[Base]:
    if not path.exists():
        return []
    raw = json.loads(path.read_text())
    expected_candidate = {
        "floater": candidate[0],
        "base_owner": list(candidate[1]),
    }
    if (
        raw.get("schema") != POOL_SCHEMA
        or raw.get("n") != n
        or raw.get("m") != m
        or raw.get("candidate") != expected_candidate
        or raw.get("agent_order") != list(agent_order)
        or not isinstance(raw.get("rivals"), list)
    ):
        raise ValueError("rival pool metadata does not match the search cell")
    rivals = [
        (record["floater"], tuple(record["base_owner"]))
        for record in raw["rivals"]
    ]
    if len(rivals) != len(set(rivals)) or candidate in rivals:
        raise ValueError("rival pool contains a duplicate or the candidate")
    for floater, base_owner in rivals:
        core.validate_triple(
            {
                "floater": floater,
                "base_owner": list(base_owner),
                "host": 0,
            },
            n,
            m,
        )
    return rivals


def lex_rivals(
    values: tuple[tuple[int, ...], ...],
    candidate: Base,
    agent_order: tuple[int, ...],
) -> tuple[list[Base], dict]:
    floater, base_owner = candidate
    candidate_base = core.classify_base(values, floater, base_owner)
    candidate_key = tuple(
        candidate_base["own_values"][agent] for agent in agent_order
    )
    if (
        candidate_base["base_min_efx_slack"] <= 0
        or any(
            candidate_base["own_values"][observer]
            <= values[observer][floater]
            for observer in range(len(values))
        )
        or candidate_base["parkable_hosts"]
    ):
        raise AssertionError("model violated the strict blocked candidate")

    keyed_rivals = []
    eligible_count = 0
    for other_floater in range(len(values[0])):
        for base in core.iter_efx_bases(values, other_floater):
            if not all(
                base["own_values"][observer]
                >= values[observer][other_floater]
                for observer in range(len(values))
            ):
                continue
            eligible_count += 1
            other: Base = (
                other_floater,
                tuple(base["base_owner"]),
            )
            if other == candidate:
                continue
            key = tuple(base["own_values"][agent] for agent in agent_order)
            if key >= candidate_key:
                keyed_rivals.append((key, other))
    keyed_rivals.sort(
        key=lambda item: (item[0], str(item[1])),
        reverse=True,
    )
    rivals = [other for _, other in keyed_rivals]
    return rivals, {
        "candidate_key": list(candidate_key),
        "candidate_shape": candidate_base["shape"],
        "candidate_min_efx_slack": candidate_base["base_min_efx_slack"],
        "candidate_host_min_slack": candidate_base["host_min_slack"],
        "eligible_base_count": eligible_count,
        "nonlower_rival_count": len(rivals),
    }


def run(
    *,
    n: int,
    m: int,
    candidate: Base,
    agent_order: tuple[int, ...],
    seed_paths: list[Path],
    complete_rival_radius: int,
    lex_encoding: str,
    pool_path: Path,
    result_path: Path,
    smt2_path: Path,
    add_per_iteration: int,
    max_iterations: int,
    time_limit_s: float,
    require_distinct_item_values: bool,
) -> dict:
    if (
        result_path.exists()
        or smt2_path.exists()
        or add_per_iteration < 1
        or max_iterations < 1
        or time_limit_s <= 0
        or complete_rival_radius < 0
        or lex_encoding not in {"exact", "bundle_nondegenerate"}
        or sorted(agent_order) != list(range(n))
    ):
        raise ValueError("new outputs and valid search parameters are required")
    core.validate_triple(
        {
            "floater": candidate[0],
            "base_owner": list(candidate[1]),
            "host": 0,
        },
        n,
        m,
    )
    if any(not bundle for bundle in bundles_of(candidate[1], n)):
        raise ValueError("candidate must give every agent a nonempty bundle")

    rivals = load_pool(pool_path, n, m, candidate, agent_order)
    rival_set = set(rivals)
    radius_added = 0
    if complete_rival_radius:
        for floater in range(m):
            assigned_goods = tuple(good for good in range(m) if good != floater)
            for owners in itertools.product(range(n), repeat=m - 1):
                if len(set(owners)) != n:
                    continue
                base_owner_list: list[int | None] = [None] * m
                for good, owner in zip(assigned_goods, owners):
                    base_owner_list[good] = owner
                rival = floater, tuple(base_owner_list)
                if (
                    rival != candidate
                    and rival not in rival_set
                    and sum(
                        left != right
                        for left, right in zip(candidate[1], rival[1])
                    )
                    <= complete_rival_radius
                ):
                    rivals.append(rival)
                    rival_set.add(rival)
                    radius_added += 1
    seed_imports = []
    for seed_path in seed_paths:
        raw = json.loads(seed_path.read_text())
        candidates = []
        if raw.get("values") is not None:
            candidates.append(raw["values"])
        candidates.extend(
            record["values"]
            for record in raw.get("trace", [])
            if record.get("values") is not None
        )
        for raw_values in candidates:
            values = core.validate_values(
                raw_values,
                expected_n=n,
                expected_m=m,
                lower=1,
            )
            found, audit = lex_rivals(values, candidate, agent_order)
            unseen = [rival for rival in found if rival not in rival_set]
            rivals.extend(unseen)
            rival_set.update(unseen)
            seed_imports.append({
                "path": str(seed_path.resolve()),
                "sha256": sha256(seed_path),
                "nonlower_rival_count": len(found),
                "new_rival_count": len(unseen),
                **audit,
            })
    atomic_json(
        pool_path,
        pool_document(n, m, candidate, agent_order, rivals),
    )
    master = ParkabilityLRAMaster(
        n,
        m,
        require_distinct_item_values=require_distinct_item_values,
    )
    candidate_utilities = add_candidate(
        master,
        candidate[0],
        candidate[1],
    )
    for rival in rivals:
        add_rival_blocker(
            master,
            candidate_utilities,
            candidate[1],
            rival,
            agent_order,
            lex_encoding,
        )

    started = time.time()
    trace = []
    status = "ITERATION_LIMIT"
    result_values = None
    reason_unknown = None
    for iteration in range(1, max_iterations + 1):
        solved = master.solve(time_limit_s=time_limit_s)
        if solved.status == "UNSAT":
            status = "UNSAT_CANDIDATE"
            break
        if solved.status != "SAT":
            status = "MASTER_UNKNOWN"
            reason_unknown = solved.reason_unknown
            break
        assert solved.values is not None
        values = core.validate_values(
            solved.values,
            expected_n=n,
            expected_m=m,
            lower=1,
        )
        found, audit = lex_rivals(values, candidate, agent_order)
        unseen = [rival for rival in found if rival not in rival_set]
        trace.append({
            "iteration": iteration,
            "pool_size_before": len(rivals),
            "new_nonlower_rival_count": len(unseen),
            "values": [list(row) for row in values],
            **audit,
        })
        print(
            f"iteration={iteration} pool={len(rivals)} "
            f"nonlower_rivals={len(found)} new={len(unseen)}",
            flush=True,
        )
        if not found:
            status = "STRICT_LEXMAX_BLOCKED_COUNTEREXAMPLE"
            result_values = values
            break
        if not unseen:
            raise AssertionError("model satisfies a pooled rival blocker")
        for rival in unseen[:add_per_iteration]:
            add_rival_blocker(
                master,
                candidate_utilities,
                candidate[1],
                rival,
                agent_order,
                lex_encoding,
            )
            rivals.append(rival)
            rival_set.add(rival)
        atomic_json(
            pool_path,
            pool_document(n, m, candidate, agent_order, rivals),
        )

    formula = master.to_smt2()
    atomic_write(smt2_path, formula.encode())
    if not pool_path.exists():
        atomic_json(
            pool_path,
            pool_document(n, m, candidate, agent_order, rivals),
        )
    result = {
        "schema": SCHEMA,
        "status": status,
        "meaning": (
            "a counterexample refutes only the strict lex-max direct-"
            "completion lemma, not complete EFX existence"
        ),
        "n": n,
        "m": m,
        "candidate": {
            "floater": candidate[0],
            "base_owner": list(candidate[1]),
        },
        "agent_order": list(agent_order),
        "require_distinct_item_values": require_distinct_item_values,
        "complete_rival_radius": complete_rival_radius,
        "radius_added_rival_count": radius_added,
        "lex_encoding": lex_encoding,
        "seed_imports": seed_imports,
        "iterations": len(trace),
        "pool_size": len(rivals),
        "elapsed_seconds": time.time() - started,
        "reason_unknown": reason_unknown,
        "values": (
            [list(row) for row in result_values]
            if result_values is not None
            else None
        ),
        "trace": trace,
        "pool_path": str(pool_path.resolve()),
        "pool_sha256": sha256(pool_path),
        "smt2_path": str(smt2_path.resolve()),
        "smt2_sha256": sha256(smt2_path),
    }
    atomic_json(result_path, result)
    return result


def parse_base(
    parser: argparse.ArgumentParser,
    raw: str,
    n: int,
    m: int,
) -> Base:
    fields = raw.split(",")
    if len(fields) != m or fields.count("x") != 1:
        parser.error("candidate base must have m owners with one x floater")
    floater = fields.index("x")
    try:
        owners = tuple(
            None if field == "x" else int(field)
            for field in fields
        )
    except ValueError:
        parser.error("candidate owners must be agent indices or x")
    if any(
        owner is not None and not 0 <= owner < n
        for owner in owners
    ):
        parser.error("candidate owner is outside the agent range")
    return floater, owners


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--m", type=int, default=9)
    parser.add_argument("--candidate-base", required=True)
    parser.add_argument("--agent-order", default="0,1,2,3")
    parser.add_argument("--seed", type=Path, action="append", default=[])
    parser.add_argument("--complete-rival-radius", type=int, default=0)
    parser.add_argument(
        "--lex-encoding",
        choices=("exact", "bundle_nondegenerate"),
        default="exact",
    )
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--add", type=int, default=256)
    parser.add_argument("--max-iterations", type=int, default=20)
    parser.add_argument("--time-limit", type=float, default=300)
    parser.add_argument("--require-distinct-item-values", action="store_true")
    args = parser.parse_args()
    candidate = parse_base(
        parser,
        args.candidate_base,
        args.n,
        args.m,
    )
    order = tuple(map(int, args.agent_order.split(",")))
    result = run(
        n=args.n,
        m=args.m,
        candidate=candidate,
        agent_order=order,
        seed_paths=args.seed,
        complete_rival_radius=args.complete_rival_radius,
        lex_encoding=args.lex_encoding,
        pool_path=args.pool,
        result_path=args.result,
        smt2_path=args.smt2,
        add_per_iteration=args.add,
        max_iterations=args.max_iterations,
        time_limit_s=args.time_limit,
        require_distinct_item_values=args.require_distinct_item_values,
    )
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
