#!/usr/bin/env python3
"""Solve the widened fixed-U cut pool under equivalent Z3 normal forms.

This is a master-architecture experiment, not a new oracle.  It loads and
fully audits the certificate ledger, reconstructs the exact form-2 master and
the identical negated certificate cuts, then transfers those assertions into
one of several semantics-preserving solver pipelines.  SAT is only another
admissible profile for the widest oracle.  UNSAT needs an independent mode
replay before promotion.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path

import z3

from .run_exact_response_physical_minimum_cegar import build_physical_master, serialize
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS
from .run_fixed_u_multi_split_chart_theorem import (
    audit_cut_record,
    certificate_cut,
    load_cut_ledger,
)


MODES = ("qflra", "smt", "elim_ite", "ctx_simplify")


def solver_for_mode(mode, timeout_seconds, random_seed):
    if mode == "qflra":
        solver = z3.SolverFor("QF_LRA")
    elif mode == "smt":
        solver = z3.Solver()
    elif mode == "elim_ite":
        solver = z3.Then(
            "simplify", "propagate-values", "elim-term-ite", "solve-eqs", "smt"
        ).solver()
    elif mode == "ctx_simplify":
        solver = z3.Then(
            "simplify", "ctx-solver-simplify", "solve-eqs", "smt"
        ).solver()
    else:
        raise ValueError(mode)
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    return solver


def build_assertions(ledger_path):
    source, total, minimum = build_physical_master(2)
    records = load_cut_ledger(ledger_path)
    branch_tally = {}
    for record in records:
        certificate = audit_cut_record(record, 4)
        source.add(z3.Not(certificate_cut(certificate, total, minimum)))
        branch = certificate["branch"]
        branch_tally[branch] = branch_tally.get(branch, 0) + 1
    return tuple(source.assertions()), total, minimum, records, branch_tally


def run(ledger_path, output_path, mode, timeout_seconds, random_seed):
    started = time.monotonic()
    assertions, total, minimum, records, branch_tally = build_assertions(ledger_path)
    built = time.monotonic()
    solver = solver_for_mode(mode, timeout_seconds, random_seed)
    solver.add(*assertions)
    loaded = time.monotonic()
    status = solver.check()
    checked = time.monotonic()
    result = {
        "schema": "fixed-u-cut-pool-normal-form-decision-v1",
        "status": str(status).upper(),
        "mode": mode,
        "solver": f"Z3 {z3.get_version_string()}",
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "ledger": str(ledger_path),
        "ledger_sha256": hashlib.sha256(ledger_path.read_bytes()).hexdigest(),
        "cut_count": len(records),
        "cut_branch_tally": branch_tally,
        "assertion_count": len(assertions),
        "build_and_audit_seconds": built - started,
        "solver_load_seconds": loaded - built,
        "check_seconds": checked - loaded,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "All modes receive the exact same audited form-2 assertions and cuts. "
            "SAT is a new source profile requiring widest-oracle evaluation. "
            "UNSAT is the declared chart theorem only after independent-mode replay "
            "and a separate ledger/statement audit; it is not general fixed-U EFX."
        ),
    }
    if status == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    elif status == z3.sat:
        model = solver.model()
        result["profile_totals"] = serialize(model, total)
        result["profile_minima"] = serialize(model, minimum)
        result["profile_role_slacks"] = {
            role: str(min(
                Fraction(str(model.eval(total[role, observer], model_completion=True)))
                // Fraction(str(model.eval(minimum[role, observer], model_completion=True)))
                for observer in OWNERS
            ))
            for role in GOODS
        }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mode", choices=MODES, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--random-seed", type=int, default=0)
    args = parser.parse_args()
    result = run(
        args.ledger, args.output, args.mode,
        args.timeout_seconds, args.random_seed,
    )
    print(json.dumps({
        "status": result["status"],
        "mode": result["mode"],
        "cut_count": result["cut_count"],
        "check_seconds": result["check_seconds"],
        "reason_unknown": result.get("reason_unknown"),
    }, indent=2))


if __name__ == "__main__":
    main()

