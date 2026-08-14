#!/usr/bin/env python3
"""Independent replay/audit of the allocated-E form-R2 PI exclusion."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import z3

from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE, build_master
from .run_generalized_pi_named_selector_cegar import cycle_signature, generalized_pi_cut


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "results" / "allocated_e_capture_form0_pairlinear_bulk_cegar.json"


def audit(output):
    source = json.loads(SOURCE.read_text())
    assert source["status"] == "UNSAT" and source["form_index"] == 0
    base_owner = {
        good: owner for owner, goods in ALLOCATED_E_BASE.items() for good in goods
    }
    witnesses = {}
    files = []
    # The driver loads witnesses recorded directly in the immediate resume
    # file; it does not recursively reload that file's own predecessor. Replay
    # exactly those effective constraints, then the final file's witnesses.
    resume = source["resume"]
    prior_path = ROOT / resume["source"]
    assert hashlib.sha256(prior_path.read_bytes()).hexdigest() == resume["source_sha256"]
    payloads = ((json.loads(prior_path.read_text()), prior_path), (source, SOURCE))
    for payload, path in payloads:
        files.append({
            "source": f"results/{path.name}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
        for record in payload.get("iterations", []):
            rows = record.get("pi_witnesses")
            if rows is None:
                one = record.get("pi_witness")
                rows = [] if one is None else [one]
            for witness in rows:
                signature = cycle_signature(witness)
                cores = [set(edge["desired_core"]) for edge in witness["edges"]]
                sources = {edge["source"] for edge in witness["edges"]}
                assert len(sources) == len(cores) and all(cores)
                assert all(
                    left.isdisjoint(right)
                    for index, left in enumerate(cores) for right in cores[index + 1:]
                )
                assert all(
                    base_owner[good] in sources | {"charity"}
                    for core in cores for good in core
                )
                witnesses.setdefault(signature, witness)

    assert len(witnesses) == source["generalized_pi_cut_count"]
    solver, value = build_master(0)
    for witness in witnesses.values():
        solver.add(generalized_pi_cut(value, witness))
    solver.set(timeout=1_800_000, random_seed=7919)
    checked = solver.check()
    if checked != z3.unsat:
        raise AssertionError((checked, solver.reason_unknown()))
    result = {
        "schema": "allocated-e-form0-pi-exclusion-audit-v1",
        "status": "ALLOCATED_E_FORM0_EXCLUDED_BY_GENERALIZED_PI",
        "solver": f"Z3 {z3.get_version_string()}",
        "independent_random_seed": 7919,
        "replayed_cut_count": len(witnesses),
        "solver_status": str(checked),
        "chain": files,
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "claim_boundary": (
            "Independent replay of the exact bounded allocated-E form-R2 "
            "exclusion. Every installed cut is validated as a closed disjoint "
            "desired-core family. This is not a cap-free theorem."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    output = ROOT / "results" / "allocated_e_form0_pi_exclusion_audit.json"
    result = audit(output)
    print(json.dumps({
        "status": result["status"],
        "cuts": result["replayed_cut_count"],
        "solver_status": result["solver_status"],
    }, indent=2))


if __name__ == "__main__":
    main()
