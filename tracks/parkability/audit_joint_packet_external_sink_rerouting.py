#!/usr/bin/env python3
"""QF_LRA checks for joint-packet external-sink rerouting."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked(name: str, constraints) -> dict:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    return {"claim": name, "status": str(solver.check())}


def run(root: Path) -> dict:
    xr, xq, xa, k_r, k_q, g_r, g_a = z3.Reals(
        "xr xq xa k_r k_q g_r g_a"
    )
    yr, yq, ya = z3.Reals("yr yq ya")
    xr_count, xq_count, xa_count, k_count, g_count = z3.Ints(
        "xr_count xq_count xa_count k_count g_count"
    )
    yr_count, yq_count, ya_count = z3.Ints("yr_count yq_count ya_count")
    old_root_tail, new_root_tail, old_sink_tail, new_sink_tail, own = z3.Reals(
        "old_root_tail new_root_tail old_sink_tail new_sink_tail own"
    )
    positive = [
        xr > 0,
        xq > 0,
        xa > 0,
        k_r > 0,
        k_q > 0,
        g_r > 0,
        g_a > 0,
        own > 0,
    ]
    records = [
        checked(
            "rerouting_conserves_owner_pool",
            [
                xr_count >= g_count,
                xq_count >= k_count,
                xa_count >= 0,
                k_count > 0,
                g_count > 0,
                yr_count == xr_count - g_count + k_count,
                yq_count == xq_count - k_count,
                ya_count == xa_count + g_count,
                yr_count + yq_count + ya_count
                != xr_count + xq_count + xa_count,
            ],
        ),
        checked(
            "root_strictly_improves",
            positive + [k_r > g_r, yr == xr - g_r + k_r, yr <= xr],
        ),
        checked(
            "external_sink_strictly_improves",
            positive + [ya == xa + g_a, ya <= xa],
        ),
        checked(
            "root_target_wall_forces_threshold_increase",
            positive + [own >= old_root_tail, own < new_root_tail, new_root_tail <= old_root_tail],
        ),
        checked(
            "sink_target_wall_forces_threshold_increase",
            positive + [own >= old_sink_tail, own < new_sink_tail, new_sink_tail <= old_sink_tail],
        ),
    ]
    script = Path(__file__).resolve()
    theorem = root / "results/JOINT_PACKET_EXTERNAL_SINK_REROUTING_LEMMA_20260811.md"
    return {
        "schema": "joint-packet-external-sink-rerouting-audit-v1",
        "status": "ALL_FORCED" if all(r["status"] == "unsat" for r in records) else "OPEN",
        "records": records,
        "claim_boundary": (
            "QF_LRA audit of connected rerouting support, owner payment, and "
            "target-wall polarities; sacrificed-owner Hall termination is outside scope"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "records": result["records"]}, indent=2))


if __name__ == "__main__":
    main()
