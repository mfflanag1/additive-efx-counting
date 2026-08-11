#!/usr/bin/env python3
"""QF_LRA/support checks for the charity-completed transfer path."""

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
    xr, xq, xa = z3.Reals("xr xq xa")
    k_r, k_q, g_r, g_a, f_q = z3.Reals("k_r k_q g_r g_a f_q")
    yr, yq, ya = z3.Reals("yr yq ya")
    old_tail, new_tail, own = z3.Reals("old_tail new_tail own")
    xr_count, xq_count, xa_count, kc, gc = z3.Ints(
        "xr_count xq_count xa_count kc gc"
    )
    yr_count, yq_count, ya_count, charity_count = z3.Ints(
        "yr_count yq_count ya_count charity_count"
    )
    positive = [
        xr > 0,
        xq > 0,
        xa > 0,
        k_r > 0,
        k_q > 0,
        g_r >= 0,
        g_a >= 0,
        f_q > 0,
        own > 0,
    ]
    records = [
        checked(
            "complete_path_conserves_goods_with_external_sink",
            [
                xr_count >= gc,
                xq_count >= kc,
                xa_count >= 0,
                kc > 0,
                gc > 0,
                yr_count == xr_count - gc + kc,
                yq_count == xq_count - kc + 1,
                ya_count == xa_count + gc,
                charity_count == 0,
                yr_count + yq_count + ya_count + charity_count
                != xr_count + xq_count + xa_count + 1,
            ],
        ),
        checked(
            "complete_path_conserves_goods_without_external_sink",
            [
                xq_count >= kc,
                kc > 0,
                yr_count == xr_count + kc,
                yq_count == xq_count - kc + 1,
                charity_count == 0,
                yr_count + yq_count + charity_count
                != xr_count + xq_count + 1,
            ],
        ),
        checked(
            "root_strictly_improves",
            positive + [k_r > g_r, yr == xr - g_r + k_r, yr <= xr],
        ),
        checked(
            "joint_packet_gives_exact_q_loss",
            positive
            + [k_q > f_q, yq == xq - k_q + f_q, xq - yq != k_q - f_q],
        ),
        checked(
            "root_target_wall_forces_threshold_increase",
            positive + [own >= old_tail, own < new_tail, new_tail <= old_tail],
        ),
        checked(
            "sink_target_wall_forces_threshold_increase",
            positive + [own >= old_tail, own < new_tail, new_tail <= old_tail],
        ),
    ]
    script = Path(__file__).resolve()
    theorem = root / "results/JOINT_PACKET_CHARITY_COMPLETED_TRANSFER_PATH_LEMMA_20260811.md"
    return {
        "schema": "joint-packet-charity-completed-transfer-path-audit-v1",
        "status": "ALL_FORCED" if all(r["status"] == "unsat" for r in records) else "OPEN",
        "records": records,
        "claim_boundary": (
            "QF_LRA/support audit of the complete transfer path, owner payment, "
            "and target-wall polarities; sacrificed-owner Hall termination is outside scope"
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
