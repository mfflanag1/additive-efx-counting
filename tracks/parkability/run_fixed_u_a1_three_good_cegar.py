#!/usr/bin/env python3
"""Decide every three-good realization of a1 in the wild-forced profile.

All roles other than a1 are frozen to the canonical physical columns in the
audited repair artifact.  For each observer, the three positive a1 values sum
to the immutable total, are bounded below by the immutable minimum, and at
least one equals that minimum.  These constraints cover every labelled
minimum-witness identity pattern, including ties.

The master searches realization columns; the concrete oracle exhausts every
complete assignment of all 21 physical goods to the four owners using at most
four support-supplier/recipient pairs.  Each accepted allocation becomes an
exact symbolic EFX cut.  Master UNSAT proves the whole three-good rung; an
oracle UNSAT supplies an exact countermodel.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path

import z3

from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE


TARGET_ROLE = "a1"
TARGET_GOODS = tuple(f"{TARGET_ROLE}:{index}" for index in range(3))


def rv(amount):
    amount = Fraction(amount)
    return z3.RealVal(f"{amount.numerator}/{amount.denominator}")


def atomic_json_write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def canonical_payload(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def append_record(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    core = dict(payload)
    core["payload_sha256"] = hashlib.sha256(
        canonical_payload(payload).encode()
    ).hexdigest()
    with path.open("a") as handle:
        handle.write(canonical_payload(core) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    return core


def load_records(path):
    if not path.exists():
        return []
    records = []
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"torn ledger line {line_number}") from error
        digest = record.pop("payload_sha256")
        assert digest == hashlib.sha256(
            canonical_payload(record).encode()
        ).hexdigest()
        record["payload_sha256"] = digest
        records.append(record)
    assert [record["iteration"] for record in records] == list(range(len(records)))
    return records


def load_frozen(profile_path, repair_path):
    profile = json.loads(profile_path.read_text())
    repair = json.loads(repair_path.read_text())
    totals = {
        observer: {role: Fraction(amount) for role, amount in row.items()}
        for observer, row in profile["profile_totals"].items()
    }
    minima = {
        observer: {role: Fraction(amount) for role, amount in row.items()}
        for observer, row in profile["profile_minima"].items()
    }
    frozen = {
        observer: {good: Fraction(amount) for good, amount in row.items()}
        for observer, row in repair["terminal"]["physical_values"].items()
    }
    role_goods = {}
    for role in GOODS:
        if role == TARGET_ROLE:
            role_goods[role] = TARGET_GOODS
        else:
            role_goods[role] = tuple(sorted(
                good for good in frozen[OWNERS[0]]
                if good.split(":", 1)[0] == role
            ))
            assert role_goods[role]
            for observer in OWNERS:
                goods = role_goods[role]
                assert sum((frozen[observer][g] for g in goods), Fraction()) == totals[observer][role]
                assert min(frozen[observer][g] for g in goods) == minima[observer][role]
    return profile, repair, totals, minima, frozen, role_goods


def build_realization_master(totals, minima):
    value = {
        (observer, good): z3.Real(f"a1_three_{observer}_{good.split(':')[1]}")
        for observer in OWNERS for good in TARGET_GOODS
    }
    solver = z3.SolverFor("QF_LRA")
    for observer in OWNERS:
        row = [value[observer, good] for good in TARGET_GOODS]
        solver.add(*(entry >= rv(minima[observer][TARGET_ROLE]) for entry in row))
        solver.add(z3.Sum(*row) == rv(totals[observer][TARGET_ROLE]))
        solver.add(z3.Or(*(
            entry == rv(minima[observer][TARGET_ROLE]) for entry in row
        )))
    return solver, value


def physical_values(model, variables, frozen):
    values = {(observer, good): amount
              for observer, row in frozen.items() for good, amount in row.items()
              if good.split(":", 1)[0] != TARGET_ROLE}
    for observer in OWNERS:
        for good in TARGET_GOODS:
            values[observer, good] = Fraction(str(
                model.eval(variables[observer, good], model_completion=True)
            ))
    return values


def supplier_map():
    return {
        role: supplier
        for supplier, roles in SUPPORT_STATE.items() for role in roles
    }


def physical_goods(role_goods):
    return tuple(good for role in GOODS for good in role_goods[role])


def allocation_edges(allocation):
    supplier = supplier_map()
    return sorted({
        (supplier[good.split(":", 1)[0]], owner)
        for owner, goods in allocation.items() for good in goods
        if supplier[good.split(":", 1)[0]] != owner
    })


def exact_efx_audit(allocation, values, role_goods, edge_cap=4):
    goods = physical_goods(role_goods)
    placed = [good for bundle in allocation.values() for good in bundle]
    assert len(placed) == len(set(placed)) and sorted(placed) == sorted(goods)
    edges = allocation_edges(allocation)
    assert len(edges) <= edge_cap
    minimum_slack = None
    for observer in OWNERS:
        own = sum((values[observer, g] for g in allocation[observer]), Fraction())
        for target in OWNERS:
            if target == observer:
                continue
            gross = sum((values[observer, g] for g in allocation[target]), Fraction())
            for good in allocation[target]:
                slack = own - (gross - values[observer, good])
                assert slack >= 0, (observer, target, good, slack)
                minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
    return edges, minimum_slack


def concrete_oracle(values, role_goods, edge_cap, timeout_seconds):
    goods = physical_goods(role_goods)
    supplier = supplier_map()
    x = {(good, owner): z3.Bool(f"oracle_{good.replace(':', '_')}_{owner}")
         for good in goods for owner in OWNERS}
    edge = {(source, target): z3.Bool(f"oracle_edge_{source}_{target}")
            for source in SUPPORT_STATE for target in OWNERS if source != target}
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    for good in goods:
        solver.add(z3.PbEq([(x[good, owner], 1) for owner in OWNERS], 1))
        source = supplier[good.split(":", 1)[0]]
        for target in OWNERS:
            if target != source:
                solver.add(z3.Implies(x[good, target], edge[source, target]))
    solver.add(z3.PbLe([(flag, 1) for flag in edge.values()], edge_cap))
    utility = {
        (observer, target): z3.Sum(*(
            z3.If(x[good, target], rv(values[observer, good]), z3.RealVal(0))
            for good in goods
        ))
        for observer in OWNERS for target in OWNERS
    }
    for observer in OWNERS:
        for target in OWNERS:
            if target == observer:
                continue
            for good in goods:
                solver.add(z3.Implies(
                    x[good, target],
                    utility[observer, observer] >= utility[observer, target]
                    - rv(values[observer, good]),
                ))
    status = solver.check()
    if status != z3.sat:
        return str(status), None, solver.reason_unknown() if status == z3.unknown else None
    model = solver.model()
    allocation = {
        owner: [good for good in goods if z3.is_true(model.eval(x[good, owner]))]
        for owner in OWNERS
    }
    exact_efx_audit(allocation, values, role_goods, edge_cap)
    return "sat", allocation, None


def expression_value(observer, good, variables, frozen):
    if good in TARGET_GOODS:
        return variables[observer, good]
    return rv(frozen[observer][good])


def symbolic_efx(allocation, variables, frozen):
    utility = {
        (observer, target): z3.Sum(*(
            expression_value(observer, good, variables, frozen)
            for good in allocation[target]
        )) if allocation[target] else z3.RealVal(0)
        for observer in OWNERS for target in OWNERS
    }
    return z3.And(*(
        utility[observer, observer] >= utility[observer, target]
        - expression_value(observer, good, variables, frozen)
        for observer in OWNERS for target in OWNERS if target != observer
        for good in allocation[target]
    ))


def witness_pattern(values, minima):
    return {
        observer: [
            index for index, good in enumerate(TARGET_GOODS)
            if values[observer, good] == minima[observer][TARGET_ROLE]
        ]
        for observer in OWNERS
    }


def serialize_a1(values):
    return {
        observer: {good: str(values[observer, good]) for good in TARGET_GOODS}
        for observer in OWNERS
    }


def audit_record(record, totals, minima, frozen, role_goods, edge_cap):
    payload = {k: v for k, v in record.items() if k != "payload_sha256"}
    assert record["payload_sha256"] == hashlib.sha256(
        canonical_payload(payload).encode()
    ).hexdigest()
    values = {(observer, good): amount
              for observer, row in frozen.items() for good, amount in row.items()
              if good.split(":", 1)[0] != TARGET_ROLE}
    for observer in OWNERS:
        row = [Fraction(record["a1_values"][observer][good]) for good in TARGET_GOODS]
        assert all(entry >= minima[observer][TARGET_ROLE] for entry in row)
        assert sum(row, Fraction()) == totals[observer][TARGET_ROLE]
        assert min(row) == minima[observer][TARGET_ROLE]
        for good, amount in zip(TARGET_GOODS, row):
            values[observer, good] = amount
    edges, slack = exact_efx_audit(record["allocation"], values, role_goods, edge_cap)
    assert [list(edge) for edge in edges] == record["edges"]
    assert str(slack) == record["minimum_efx_slack"]
    assert witness_pattern(values, minima) == record["witness_pattern"]


def run(profile_path, repair_path, output_path, ledger_path, maximum_rounds,
        master_timeout_seconds, oracle_timeout_seconds, edge_cap, random_seed):
    profile, repair, totals, minima, frozen, role_goods = load_frozen(
        profile_path, repair_path
    )
    records = load_records(ledger_path)
    for record in records:
        audit_record(record, totals, minima, frozen, role_goods, edge_cap)
    master, variables = build_realization_master(totals, minima)
    master.set(timeout=master_timeout_seconds * 1000, random_seed=random_seed)
    for record in records:
        master.add(z3.Not(symbolic_efx(
            record["allocation"], variables, frozen=frozen
        )))
    result = {
        "schema": "fixed-u-a1-three-good-cegar-v1",
        "status": "RUNNING",
        "profile": str(profile_path),
        "profile_sha256": hashlib.sha256(profile_path.read_bytes()).hexdigest(),
        "repair": str(repair_path),
        "repair_sha256": hashlib.sha256(repair_path.read_bytes()).hexdigest(),
        "target_role": TARGET_ROLE,
        "target_cardinality": 3,
        "physical_good_count": len(physical_goods(role_goods)),
        "edge_cap": edge_cap,
        "labelled_witness_pattern_count": 6 ** len(OWNERS),
        "pattern_coverage": (
            "for each observer all three values are >= M, sum to T, and at least "
            "one equals M; since T>3M in every a1 row, exactly the six nonempty "
            "proper witness subsets are feasible, independently across four rows"
        ),
        "ledger": str(ledger_path),
        "rounds": [
            {k: v for k, v in record.items() if k != "allocation"}
            for record in records
        ],
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    atomic_json_write(output_path, result)

    for iteration in range(len(records), maximum_rounds):
        status = master.check()
        if status != z3.sat:
            result["status"] = (
                "UNSAT_EVERY_THREE_GOOD_A1_REALIZATION_HAS_FOUR_EDGE_EFX"
                if status == z3.unsat else "UNKNOWN_MASTER"
            )
            if status == z3.unknown:
                result["reason_unknown"] = master.reason_unknown()
            break
        values = physical_values(master.model(), variables, frozen)
        oracle_status, allocation, reason = concrete_oracle(
            values, role_goods, edge_cap, oracle_timeout_seconds
        )
        if oracle_status != "sat":
            result["status"] = (
                "SAT_THREE_GOOD_A1_FOUR_EDGE_COUNTERMODEL"
                if oracle_status == "unsat" else "HALTED_ORACLE_UNKNOWN"
            )
            result["terminal_iteration"] = iteration
            result["terminal_a1_values"] = serialize_a1(values)
            result["terminal_witness_pattern"] = witness_pattern(values, minima)
            result["oracle_status"] = oracle_status
            if reason:
                result["oracle_reason_unknown"] = reason
            break
        edges, slack = exact_efx_audit(allocation, values, role_goods, edge_cap)
        payload = {
            "schema": "fixed-u-a1-three-good-cut-v1",
            "iteration": iteration,
            "a1_values": serialize_a1(values),
            "witness_pattern": witness_pattern(values, minima),
            "allocation": allocation,
            "edges": [list(edge) for edge in edges],
            "minimum_efx_slack": str(slack),
        }
        record = append_record(ledger_path, payload)
        audit_record(record, totals, minima, frozen, role_goods, edge_cap)
        records.append(record)
        master.add(z3.Not(symbolic_efx(allocation, variables, frozen=frozen)))
        result["rounds"].append({k: v for k, v in record.items() if k != "allocation"})
        atomic_json_write(output_path, result)
        print(iteration, record["witness_pattern"], record["edges"], flush=True)
    else:
        result["status"] = "ITERATION_LIMIT"

    result["cut_count"] = len(records)
    result["claim_boundary"] = (
        "The master exactly covers every labelled three-good realization of a1 "
        "with the frozen totals/minima and every witness identity/tie pattern; all "
        "other roles remain at their audited canonical values. The oracle exhausts "
        "all complete allocations using at most four support-transfer edges. A SAT "
        "countermodel or master UNSAT is exact for this rung, not for cardinalities "
        "four through seven or for every fixed-U state."
    )
    atomic_json_write(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--repair", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--maximum-rounds", type=int, default=500)
    parser.add_argument("--master-timeout-seconds", type=int, default=300)
    parser.add_argument("--oracle-timeout-seconds", type=int, default=300)
    parser.add_argument("--edge-cap", type=int, default=4)
    parser.add_argument("--random-seed", type=int, default=0)
    args = parser.parse_args()
    result = run(
        args.profile, args.repair, args.output, args.ledger,
        args.maximum_rounds, args.master_timeout_seconds,
        args.oracle_timeout_seconds, args.edge_cap, args.random_seed,
    )
    print(json.dumps({
        "status": result["status"],
        "cut_count": result["cut_count"],
        "terminal_iteration": result.get("terminal_iteration"),
    }, indent=2))


if __name__ == "__main__":
    main()
