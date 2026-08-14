#!/usr/bin/env python3
"""Decide which base payments the endpoint-6 three-way releases force."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

from .run_allocated_e_capture_rank_three_cegar import build_master
from .run_allocated_e_root_retention_new_debt_cegar import RETAINED
from .run_fixed_u_full_packet_terminal_cegar import OWNERS, allocation_formula, total


ROOT = Path(__file__).resolve().parents[2]


def run(core_source: Path, endpoint_source: Path, output: Path):
    core_source = core_source.resolve()
    endpoint_source = endpoint_source.resolve()
    core = json.loads(core_source.read_text())
    endpoint6 = json.loads(endpoint_source.read_text())["allocations"][5]
    rows = []
    for index, allocation in enumerate(core["allocations"], 1):
        owner_rows = {}
        for owner in OWNERS:
            solver, value = build_master(2)
            solver.add(
                allocation_formula(endpoint6, value, "complete_efx"),
                total(value, "q", endpoint6["q"]) >= 1,
                total(value, "s", endpoint6["s"]) >= 1,
                total(value, "q", RETAINED[6]["q"]) < 1,
                total(value, owner, allocation[owner]) < 1,
            )
            status = solver.check()
            owner_rows[owner] = {
                "underpayment_status": str(status),
                "forced_paid": status == z3.unsat,
            }
        rows.append({
            "allocation_index": index,
            "allocation": allocation,
            "owners": owner_rows,
        })
    result = {
        "schema": "endpoint6-three-way-h-release-payment-analysis-v1",
        "status": "COMPLETE",
        "core_source": str(core_source.relative_to(ROOT)),
        "core_source_sha256": hashlib.sha256(core_source.read_bytes()).hexdigest(),
        "endpoint_source": str(endpoint_source.relative_to(ROOT)),
        "endpoint_source_sha256": hashlib.sha256(endpoint_source.read_bytes()).hexdigest(),
        "rows": rows,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Independent payment queries under the endpoint-6 hard premises. "
            "They do not impose PI exclusion or prove physical EFX."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core-source", type=Path, required=True)
    parser.add_argument("--endpoint-source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.core_source, args.endpoint_source, args.output), indent=2))


if __name__ == "__main__":
    main()
