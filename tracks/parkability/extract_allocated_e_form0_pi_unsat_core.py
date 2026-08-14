#!/usr/bin/env python3
"""Extract an assumption UNSAT core from the allocated-E form-R2 exclusion."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

from .audit_allocated_e_form0_pi_exclusion import ROOT, SOURCE
from .run_allocated_e_capture_rank_three_cegar import build_master
from .run_generalized_pi_named_selector_cegar import cycle_signature, generalized_pi_cut


def effective_witnesses():
    source = json.loads(SOURCE.read_text())
    resume = source["resume"]
    prior_path = ROOT / resume["source"]
    assert hashlib.sha256(prior_path.read_bytes()).hexdigest() == resume["source_sha256"]
    witnesses = {}
    for payload in (json.loads(prior_path.read_text()), source):
        for record in payload["iterations"]:
            rows = record.get("pi_witnesses")
            if rows is None:
                one = record.get("pi_witness")
                rows = [] if one is None else [one]
            for witness in rows:
                witnesses.setdefault(cycle_signature(witness), witness)
    assert len(witnesses) == source["generalized_pi_cut_count"]
    return source, witnesses


def run(output, timeout_seconds, random_seed):
    source, witnesses = effective_witnesses()
    solver, value = build_master(0)
    labels = []
    indexed = []
    for index, (signature, witness) in enumerate(witnesses.items()):
        label = z3.Bool(f"pi_family_{index}")
        solver.add(z3.Implies(label, generalized_pi_cut(value, witness)))
        labels.append(label)
        indexed.append((signature, witness))
    solver.set(
        timeout=timeout_seconds * 1000,
        random_seed=random_seed,
        unsat_core=True,
        **{"smt.core.minimize": True},
    )
    checked = solver.check(*labels)
    result = {
        "schema": "allocated-e-form0-pi-unsat-core-v1",
        "status": str(checked),
        "solver": f"Z3 {z3.get_version_string()}",
        "timeout_seconds": timeout_seconds,
        "random_seed": random_seed,
        "full_cut_count": len(labels),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "source_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Assumption-level core for the bounded allocated-E R2 exclusion. "
            "A raw/minimized SMT core is an analytic candidate, not by itself "
            "a cap-free proof."
        ),
    }
    if checked == z3.unsat:
        core_indices = sorted(int(str(label).removeprefix("pi_family_")) for label in solver.unsat_core())
        result["core_count"] = len(core_indices)
        result["core"] = [
            {
                "index": index,
                "signature": [
                    [source_name, list(goods)] for source_name, goods in indexed[index][0]
                ],
                "witness": indexed[index][1],
            }
            for index in core_indices
        ]
    elif checked == z3.unknown:
        result["reason_unknown"] = solver.reason_unknown()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--random-seed", type=int, default=6211)
    args = parser.parse_args()
    result = run(args.output, args.timeout_seconds, args.random_seed)
    print(json.dumps({
        "status": result["status"],
        "full_cut_count": result["full_cut_count"],
        "core_count": result.get("core_count"),
        "reason_unknown": result.get("reason_unknown"),
    }, indent=2))


if __name__ == "__main__":
    main()
