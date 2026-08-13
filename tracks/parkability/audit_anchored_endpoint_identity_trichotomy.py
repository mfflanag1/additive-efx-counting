#!/usr/bin/env python3
"""Exact identity audit for the unique anchored endpoint order."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity_type(path: tuple[str, ...]) -> str:
    r_pos = path.index("r")
    q_pos = path.index("q")
    assert q_pos == r_pos + 1
    if r_pos == 0:
        return "I_root_hole_q_target"
    if r_pos == 1:
        return "II_root_target_q_middle"
    if r_pos == 2:
        return "III_root_middle_q_source"
    raise AssertionError("anchored block cannot start at endpoint position 3")


def run(root: Path) -> dict:
    source_path = root / "results/anchored_mixed_margin_path_terminal_classification_audit.json"
    source = json.loads(source_path.read_text())
    records = []
    for record in source["records"]:
        path = tuple(record["path"])
        if record["source"] != path[3]:
            continue
        assert record["outcome"] == "anchor_cycle"
        records.append({
            "path": list(path),
            "hole": path[0],
            "failed_target": path[1],
            "middle": path[2],
            "source": path[3],
            "identity_type": identity_type(path),
        })
    assert len(records) == 6
    counts = {
        kind: sum(record["identity_type"] == kind for record in records)
        for kind in sorted({record["identity_type"] for record in records})
    }
    assert counts == {
        "III_root_middle_q_source": 2,
        "II_root_target_q_middle": 2,
        "I_root_hole_q_target": 2,
    }
    script = Path(__file__).resolve()
    theorem = root / "results/ANCHORED_ENDPOINT_IDENTITY_TRICHOTOMY_20260813.md"
    return {
        "schema": "anchored-endpoint-identity-trichotomy-audit-v1",
        "status": "SIX_ENDPOINTS_REDUCED_TO_THREE_IDENTITY_TYPES",
        "endpoint_count": len(records),
        "identity_type_counts": counts,
        "records": records,
        "remaining_gates": {
            "I_root_hole_q_target": "simultaneous root-hole and q-target blockade",
            "II_root_target_q_middle": "root/q compensation fork with external sink",
            "III_root_middle_q_source": "root-preserving two-external-hole selector",
        },
        "claim_boundary": (
            "identity enumeration only; no flower-specific reverse inequality "
            "or GG closure"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "source": str(source_path.relative_to(root)),
            "source_sha256": sha256(source_path),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "counts": result["identity_type_counts"]}, indent=2))


if __name__ == "__main__":
    main()
