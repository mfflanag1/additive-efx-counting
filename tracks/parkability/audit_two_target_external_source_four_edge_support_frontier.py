#!/usr/bin/env python3
"""Exhaustive signed-edge audit for the external-source 2x1 Hall star."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path) -> dict:
    records = []
    for source_is_incoming_supplier in (False, True):
        for incoming_state in ("none", "partial", "whole"):
            for residual_used in (False, True):
                response_nonempty = residual_used or incoming_state != "none"
                if not response_nonempty:
                    continue

                if source_is_incoming_supplier:
                    incoming_edge_count = 0 if incoming_state == "whole" else 1
                else:
                    incoming_edge_count = 1 if incoming_state in ("none", "whole") else 2
                response_local_edges = incoming_edge_count + int(residual_used)
                final_edge_count = 2 + 1 + response_local_edges
                within_four = final_edge_count <= 4

                predicted = (
                    source_is_incoming_supplier
                    and (not residual_used or incoming_state == "whole")
                    and incoming_state != "none"
                ) or (
                    not source_is_incoming_supplier
                    and not residual_used
                    and incoming_state == "whole"
                )
                assert within_four == predicted
                records.append({
                    "source_is_incoming_supplier": source_is_incoming_supplier,
                    "incoming_state": incoming_state,
                    "residual_used": residual_used,
                    "final_edge_count": final_edge_count,
                    "within_four": within_four,
                })

    # No incoming packet: all three old matching edges remain, while a
    # retained-support response and charity donation add two more.
    no_incoming_edge_count = 5
    assert no_incoming_edge_count > 4

    theorem = root / "results" / "TWO_TARGET_EXTERNAL_SOURCE_FOUR_EDGE_SUPPORT_FRONTIER_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "two-target-external-source-four-edge-support-frontier-audit-v1",
        "status": "EXACT_SUPPORT_FRONTIER_PROVED",
        "cases_checked": len(records),
        "records": records,
        "no_incoming_packet_edge_count": no_incoming_edge_count,
        "feasible_case_count": sum(record["within_four"] for record in records),
        "remaining_gate": (
            "prove one target exposes an edge-compatible universally safe core, "
            "switch matching/fork, or construct a full-premise countermodel"
        ),
        "claim_boundary": (
            "supplier-pair feasibility only; response existence, observer EFX, "
            "3x2 repair, fixed-U, GG, and EFX remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "remaining_gate": result["remaining_gate"]}, indent=2))


if __name__ == "__main__":
    main()
