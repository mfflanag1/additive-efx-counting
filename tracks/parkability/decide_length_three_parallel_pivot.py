#!/usr/bin/env python3
"""Exact scalar audit of the cap-free parallel-root pivot reduction."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def forced(name, assumptions, conclusion):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*assumptions, z3.Not(conclusion))
    checked = solver.check()
    return {"case": name, "status": "FORCED" if checked == z3.unsat else str(checked)}


def run():
    rt, rb, rtq, rf = z3.Reals("pivot_rt pivot_rb pivot_rtq pivot_rf")
    rest, rg = z3.Reals("pivot_rest pivot_rg")
    bp, peprime, peminus, pg = z3.Reals("pivot_bp pivot_peprime pivot_peminus pivot_pg")
    positive = [entry > 0 for entry in (rt, rb, rtq, rf, rest, rg, bp, peprime, pg)]
    records = [
        forced(
            "owner_and_selected_edges_order_tops",
            positive + [rf < rb, rtq + rf > rt + rb],
            rtq > rt,
        ),
        forced(
            "failed_fallback_makes_charity_beat_pivot",
            positive + [rt == rest + rg, rtq > rt, rf + rest > rtq],
            rf > rg,
        ),
        forced(
            "returned_pivot_strictly_improves_new_root",
            positive + [peminus <= bp, peprime > bp],
            peprime + pg > peminus + pg,
        ),
    ]
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    return {
        "schema": "length-three-parallel-pivot-scalar-audit-v1",
        "status": "ALL_FORCED" if all(record["status"] == "FORCED" for record in records) else "FAILED",
        "records": records,
        "claim_boundary": "exact QF_LRA audit of the three scalar implications in the analytic parallel-root pivot reduction",
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "z3_version": z3.get_version_string(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "cases": len(result["records"])}, indent=2))


if __name__ == "__main__":
    main()
