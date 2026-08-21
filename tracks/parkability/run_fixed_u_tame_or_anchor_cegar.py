#!/usr/bin/env python3
"""CEGAR for the corrected form-2 tame-menu-or-dynamic-anchor theorem."""

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
    symbolic_candidate_closes,
)
from .run_exact_response_physical_minimum_cegar import build_physical_master, serialize
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS
from .run_fixed_u_multi_split_chart_theorem import (
    WIDE_FAMILY_FAILED,
    audit_certificate_at_profile,
    audit_cut_record,
    certificate_cut,
    close_profile,
    select_master_solver,
)


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


def seed_anchor_candidates(calibration_path, dynamic_ledger_path):
    calibration = json.loads(calibration_path.read_text())
    candidates = [
        row["candidate"] for row in calibration["profiles"]
        if row["candidate"]["kind"] == "anchor"
    ]
    candidates.append(calibration["terminal_candidate"])
    candidates.extend(calibration["required_terminal_calibrations"].values())
    if dynamic_ledger_path.exists():
        for line in dynamic_ledger_path.read_text().splitlines():
            if not line.strip():
                continue
            candidate = json.loads(line)["candidate"]
            if candidate["kind"] == "anchor":
                candidates.append(candidate)
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


def audit_fresh_record(record, edge_cap):
    totals = fraction_rows(record, "profile_totals")
    minima = fraction_rows(record, "profile_minima")
    if record["kind"] == "menu":
        audit_certificate_at_profile(
            record["certificate"], totals, minima, edge_cap
        )
    else:
        assert record["kind"] == "anchor"
        candidate = record["candidate"]
        edges, slack = exact_audit_anchor(
            candidate["allocation"], totals, minima,
            candidate["split_role"], candidate["anchor_observer"], edge_cap,
        )
        assert [list(edge) for edge in edges] == candidate["edges"]
        assert str(slack) == candidate["minimum_certified_slack"]


def install_fresh_record(solver, record, total, minimum):
    if record["kind"] == "menu":
        solver.add(z3.Not(certificate_cut(
            record["certificate"], total, minimum
        )))
    else:
        solver.add(z3.Not(symbolic_candidate_closes(
            record["candidate"], total, minimum
        )))


def serialize_rows(rows):
    return {
        observer: {role: str(value) for role, value in row.items()}
        for observer, row in rows.items()
    }


def run(base_ledger_path, anchor_calibration_path, dynamic_ledger_path,
        ledger_path, output_path, maximum_rounds, master_timeout_seconds,
        oracle_timeout_seconds, edge_cap, pattern_budget, random_seed,
        master_mode):
    source, total, minimum = build_physical_master(2)
    solver = select_master_solver(
        source, master_mode, master_timeout_seconds, random_seed
    )

    base_records = [
        json.loads(line) for line in base_ledger_path.read_text().splitlines()
        if line.strip()
    ]
    for record in base_records:
        certificate = audit_cut_record(record, edge_cap)
        solver.add(z3.Not(certificate_cut(certificate, total, minimum)))

    anchors = seed_anchor_candidates(anchor_calibration_path, dynamic_ledger_path)
    for candidate in anchors:
        solver.add(z3.Not(symbolic_candidate_closes(candidate, total, minimum)))

    records = load_records(ledger_path)
    for record in records:
        audit_fresh_record(record, edge_cap)
        install_fresh_record(solver, record, total, minimum)

    result = {
        "schema": "fixed-u-tame-menu-or-dynamic-anchor-cegar-v1",
        "status": "RUNNING",
        "form_index": 2,
        "edge_cap": edge_cap,
        "pattern_budget": pattern_budget,
        "master_mode": master_mode,
        "master_timeout_seconds": master_timeout_seconds,
        "oracle_timeout_seconds": oracle_timeout_seconds,
        "random_seed": random_seed,
        "base_ledger": str(base_ledger_path),
        "base_ledger_sha256": hashlib.sha256(base_ledger_path.read_bytes()).hexdigest(),
        "base_menu_count": len(base_records),
        "anchor_calibration": str(anchor_calibration_path),
        "anchor_calibration_sha256": hashlib.sha256(
            anchor_calibration_path.read_bytes()
        ).hexdigest(),
        "dynamic_anchor_ledger": str(dynamic_ledger_path),
        "dynamic_anchor_ledger_sha256": hashlib.sha256(
            dynamic_ledger_path.read_bytes()
        ).hexdigest(),
        "seed_anchor_count": len(anchors),
        "ledger": str(ledger_path),
        "rounds": list(records),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    atomic_write(output_path, result)

    for iteration in range(len(records), maximum_rounds):
        status = solver.check()
        if status != z3.sat:
            result["status"] = (
                "UNSAT_TAME_MENU_OR_DYNAMIC_ANCHOR_FORM2_THEOREM"
                if status == z3.unsat else "UNKNOWN_MASTER"
            )
            if status == z3.unknown:
                result["reason_unknown"] = solver.reason_unknown()
            break

        model = solver.model()
        totals, minima = concrete_profile(model, total, minimum)
        menu_status, certificate, detail = close_profile(
            totals, minima, edge_cap, pattern_budget, oracle_timeout_seconds
        )
        if certificate is not None:
            payload = {
                "schema": "fixed-u-tame-or-anchor-cut-v1",
                "iteration": iteration,
                "kind": "menu",
                "profile_totals": serialize_rows(totals),
                "profile_minima": serialize_rows(minima),
                "menu_status": menu_status,
                "menu_detail": detail,
                "certificate": certificate,
            }
        else:
            anchor_status, anchor_candidate, anchor_reason = dynamic_anchor_oracle(
                totals, minima, edge_cap, oracle_timeout_seconds
            )
            if anchor_status == "sat":
                edges, slack = exact_audit_anchor(
                    anchor_candidate["allocation"], totals, minima,
                    anchor_candidate["split_role"],
                    anchor_candidate["anchor_observer"], edge_cap,
                )
                candidate = {
                    "kind": "anchor",
                    "split_role": anchor_candidate["split_role"],
                    "anchor_observer": anchor_candidate["anchor_observer"],
                    "allocation": anchor_candidate["allocation"],
                    "edges": [list(edge) for edge in edges],
                    "minimum_certified_slack": str(slack),
                }
                payload = {
                    "schema": "fixed-u-tame-or-anchor-cut-v1",
                    "iteration": iteration,
                    "kind": "anchor",
                    "profile_totals": serialize_rows(totals),
                    "profile_minima": serialize_rows(minima),
                    "menu_status": menu_status,
                    "menu_detail": detail,
                    "candidate": candidate,
                }
            else:
                conclusive = (
                    menu_status == WIDE_FAMILY_FAILED
                    and anchor_status == "unsat"
                )
                result["status"] = (
                    "SAT_TAME_MENU_OR_DYNAMIC_ANCHOR_OBSTRUCTION"
                    if conclusive else "UNKNOWN_CORRECTED_ORACLE"
                )
                result["terminal_iteration"] = iteration
                result["terminal_profile_totals"] = serialize(model, total)
                result["terminal_profile_minima"] = serialize(model, minimum)
                result["menu_status"] = menu_status
                result["menu_detail"] = detail
                result["anchor_status"] = anchor_status
                result["anchor_reason"] = anchor_reason
                break

        record = append_record(ledger_path, payload)
        audit_fresh_record(record, edge_cap)
        install_fresh_record(solver, record, total, minimum)
        records.append(record)
        result["rounds"].append(record)
        atomic_write(output_path, result)
        if record["kind"] == "menu":
            print(iteration, "menu", record["certificate"]["split_roles"], flush=True)
        else:
            print(iteration, "anchor", record["candidate"]["split_role"],
                  record["candidate"]["anchor_observer"], flush=True)
    else:
        result["status"] = "ITERATION_LIMIT"

    result["fresh_cut_count"] = len(records)
    result["total_cut_count"] = len(base_records) + len(anchors) + len(records)
    result["claim_boundary"] = (
        "UNSAT proves the corrected theorem for the complete declared form-2 "
        "physical-minimum master: every profile has a realization-free tame "
        "side-pattern menu or a cap-free dynamic anchor. It does not prove that "
        "every saturated fixed-U state is represented by form 2."
    )
    atomic_write(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-ledger", type=Path, required=True)
    parser.add_argument("--anchor-calibration", type=Path, required=True)
    parser.add_argument("--dynamic-anchor-ledger", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-rounds", type=int, default=200)
    parser.add_argument("--master-timeout-seconds", type=int, default=300)
    parser.add_argument("--oracle-timeout-seconds", type=int, default=120)
    parser.add_argument("--edge-cap", type=int, default=4)
    parser.add_argument("--pattern-budget", type=int, default=20000)
    parser.add_argument("--random-seed", type=int, default=821)
    parser.add_argument("--master-mode", choices=("smt", "qflra"), default="smt")
    args = parser.parse_args()
    result = run(
        args.base_ledger, args.anchor_calibration, args.dynamic_anchor_ledger,
        args.ledger, args.output, args.maximum_rounds,
        args.master_timeout_seconds, args.oracle_timeout_seconds,
        args.edge_cap, args.pattern_budget, args.random_seed, args.master_mode,
    )
    print(json.dumps({
        "status": result["status"],
        "fresh_cut_count": result["fresh_cut_count"],
        "total_cut_count": result["total_cut_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
