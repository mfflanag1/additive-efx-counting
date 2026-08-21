#!/usr/bin/env python3
"""Crash-safe CEGAR for the complete form-2 dynamic-anchor theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from fractions import Fraction
from pathlib import Path

import z3

from .fixed_u_dynamic_anchor import (
    candidate_signature,
    dynamic_anchor_oracle,
    exact_audit_anchor,
    exact_audit_whole,
    placement_edges,
    symbolic_candidate_closes,
    whole_role_oracle,
)
from .run_exact_response_physical_minimum_cegar import build_physical_master, serialize
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS
from .run_fixed_u_multi_split_chart_theorem import select_master_solver


def canonical_payload(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def atomic_write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def append_record(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    record = dict(payload)
    record["payload_sha256"] = hashlib.sha256(
        canonical_payload(payload).encode()
    ).hexdigest()
    with path.open("a") as handle:
        handle.write(canonical_payload(record) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    return record


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
        assert hashlib.sha256(canonical_payload(record).encode()).hexdigest() == digest
        record["payload_sha256"] = digest
        assert record["iteration"] == len(records)
        records.append(record)
    return records


def fraction_rows(raw, key):
    return {
        observer: {role: Fraction(value) for role, value in row.items()}
        for observer, row in raw[key].items()
    }


def audit_candidate(candidate, totals, minima, edge_cap):
    if candidate["kind"] == "whole":
        edges, slack = exact_audit_whole(
            candidate["allocation"], totals, minima, edge_cap
        )
    else:
        edges, slack = exact_audit_anchor(
            candidate["allocation"], totals, minima,
            candidate["split_role"], candidate["anchor_observer"], edge_cap,
        )
    assert [list(edge) for edge in edges] == candidate["edges"]
    assert str(slack) == candidate["minimum_certified_slack"]


def seed_candidates(path):
    raw = json.loads(path.read_text())
    candidates = [row["candidate"] for row in raw["profiles"]]
    candidates.append(raw["terminal_candidate"])
    candidates.extend(raw["required_terminal_calibrations"].values())
    unique = {}
    for candidate in candidates:
        unique.setdefault(candidate_signature(candidate), candidate)
    return list(unique.values())


def concrete_profile(model, total, minimum):
    totals = {
        observer: {
            role: Fraction(str(model.eval(total[role, observer], model_completion=True)))
            for role in GOODS
        }
        for observer in OWNERS
    }
    minima = {
        observer: {
            role: Fraction(str(model.eval(minimum[role, observer], model_completion=True)))
            for role in GOODS
        }
        for observer in OWNERS
    }
    return totals, minima


def close_profile(totals, minima, edge_cap, oracle_timeout_seconds):
    status, allocation, reason = whole_role_oracle(
        totals, minima, edge_cap, oracle_timeout_seconds
    )
    if status == "unknown":
        return "unknown", None, {"whole_reason": reason}
    if status == "sat":
        edges, slack = exact_audit_whole(allocation, totals, minima, edge_cap)
        return "sat", {
            "kind": "whole",
            "allocation": allocation,
            "edges": [list(edge) for edge in edges],
            "minimum_certified_slack": str(slack),
        }, None
    status, anchor_candidate, reason = dynamic_anchor_oracle(
        totals, minima, edge_cap, oracle_timeout_seconds
    )
    if status != "sat":
        return status, None, reason
    edges, slack = exact_audit_anchor(
        anchor_candidate["allocation"], totals, minima,
        anchor_candidate["split_role"], anchor_candidate["anchor_observer"],
        edge_cap,
    )
    return "sat", {
        "kind": "anchor",
        "split_role": anchor_candidate["split_role"],
        "anchor_observer": anchor_candidate["anchor_observer"],
        "allocation": anchor_candidate["allocation"],
        "edges": [list(edge) for edge in edges],
        "minimum_certified_slack": str(slack),
    }, None


def run(seed_path, ledger_path, output_path, maximum_rounds,
        master_timeout_seconds, oracle_timeout_seconds, edge_cap,
        random_seed, master_mode):
    source, total, minimum = build_physical_master(2)
    solver = select_master_solver(
        source, master_mode, master_timeout_seconds, random_seed
    )
    seeds = seed_candidates(seed_path)
    seen = set()
    for candidate in seeds:
        signature = candidate_signature(candidate)
        assert signature not in seen
        seen.add(signature)
        solver.add(z3.Not(symbolic_candidate_closes(candidate, total, minimum)))

    records = load_records(ledger_path)
    for record in records:
        totals = fraction_rows(record, "profile_totals")
        minima = fraction_rows(record, "profile_minima")
        audit_candidate(record["candidate"], totals, minima, edge_cap)
        signature = candidate_signature(record["candidate"])
        assert signature not in seen
        seen.add(signature)
        solver.add(z3.Not(symbolic_candidate_closes(
            record["candidate"], total, minimum
        )))

    result = {
        "schema": "fixed-u-dynamic-anchor-cegar-v1",
        "status": "RUNNING",
        "form_index": 2,
        "edge_cap": edge_cap,
        "master_mode": master_mode,
        "master_timeout_seconds": master_timeout_seconds,
        "oracle_timeout_seconds": oracle_timeout_seconds,
        "random_seed": random_seed,
        "seed": str(seed_path),
        "seed_sha256": hashlib.sha256(seed_path.read_bytes()).hexdigest(),
        "seed_candidate_count": len(seeds),
        "ledger": str(ledger_path),
        "rounds": list(records),
        "normal_form": (
            "rho=2 needs exactly the two-good witness endpoints; rho>=3 also "
            "needs the endpoints of [M,T-2M], and all higher cardinalities nest"
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    atomic_write(output_path, result)

    for iteration in range(len(records), maximum_rounds):
        status = solver.check()
        if status != z3.sat:
            result["status"] = (
                "UNSAT_DYNAMIC_ANCHOR_EXTRACTION_THEOREM"
                if status == z3.unsat else "UNKNOWN_MASTER"
            )
            if status == z3.unknown:
                result["reason_unknown"] = solver.reason_unknown()
            break
        model = solver.model()
        totals, minima = concrete_profile(model, total, minimum)
        oracle_status, candidate, reason = close_profile(
            totals, minima, edge_cap, oracle_timeout_seconds
        )
        if oracle_status != "sat":
            result["status"] = (
                "SAT_DYNAMIC_ANCHOR_OBSTRUCTION"
                if oracle_status == "unsat" else "UNKNOWN_ORACLE"
            )
            result["terminal_iteration"] = iteration
            result["terminal_profile_totals"] = serialize(model, total)
            result["terminal_profile_minima"] = serialize(model, minimum)
            result["oracle_status"] = oracle_status
            if reason is not None:
                result["oracle_reason"] = reason
            break
        signature = candidate_signature(candidate)
        if signature in seen:
            raise AssertionError("oracle returned an already installed candidate")
        payload = {
            "schema": "fixed-u-dynamic-anchor-cut-v1",
            "iteration": iteration,
            "profile_totals": {
                observer: {role: str(value) for role, value in row.items()}
                for observer, row in totals.items()
            },
            "profile_minima": {
                observer: {role: str(value) for role, value in row.items()}
                for observer, row in minima.items()
            },
            "candidate": candidate,
        }
        record = append_record(ledger_path, payload)
        audit_candidate(candidate, totals, minima, edge_cap)
        records.append(record)
        seen.add(signature)
        solver.add(z3.Not(symbolic_candidate_closes(candidate, total, minimum)))
        result["rounds"].append(record)
        atomic_write(output_path, result)
        print(iteration, candidate["kind"], candidate.get("split_role"),
              candidate.get("anchor_observer"), flush=True)
    else:
        result["status"] = "ITERATION_LIMIT"

    result["fresh_candidate_count"] = len(records)
    result["total_candidate_count"] = len(seeds) + len(records)
    result["claim_boundary"] = (
        "UNSAT proves the dynamic-anchor theorem for the complete declared "
        "form-2 physical-minimum master. SAT refutes only that theorem until "
        "an unrestricted physical allocation oracle independently returns UNSAT."
    )
    atomic_write(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-rounds", type=int, default=500)
    parser.add_argument("--master-timeout-seconds", type=int, default=300)
    parser.add_argument("--oracle-timeout-seconds", type=int, default=30)
    parser.add_argument("--edge-cap", type=int, default=4)
    parser.add_argument("--random-seed", type=int, default=821)
    parser.add_argument(
        "--master-mode", choices=("smt", "qflra"), default="smt",
    )
    args = parser.parse_args()
    result = run(
        args.seed, args.ledger, args.output, args.maximum_rounds,
        args.master_timeout_seconds, args.oracle_timeout_seconds,
        args.edge_cap, args.random_seed, args.master_mode,
    )
    print(json.dumps({
        "status": result["status"],
        "seed_candidate_count": result["seed_candidate_count"],
        "fresh_candidate_count": result["fresh_candidate_count"],
        "total_candidate_count": result["total_candidate_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
