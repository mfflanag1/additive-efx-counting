#!/usr/bin/env python3
"""Audit that every form-2 response branch changes every current target."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


OWNERS = ("r", "q", "s", "d")
CYCLE_TRANSFER = {"R": ("q", "r"), "Q": ("s", "q"), "S": ("r", "s")}
D_TRANSFER = {"Dr": ("r", "d"), "Dq": ("q", "d")}
OMITTED_CORE = {"r": "R", "q": "Q", "s": "S"}


def branch_rows():
    initial = {
        "r": {"r0", "S", "Dr"},
        "q": {"q0", "R", "Dq"},
        "s": {"s0", "Q"},
        "d": {"d0"},
        "charity": {"p"},
    }
    initial_union = set().union(*initial.values())
    rows = []
    for d_core, (d_supplier, _) in D_TRANSFER.items():
        for omitted in ("r", "q", "s"):
            final = {holder: set(goods) for holder, goods in initial.items()}
            final["charity"].remove("p")
            final[omitted].add("p")
            final[d_supplier].remove(d_core)
            final["d"].add(d_core)
            for core, (supplier, recipient) in CYCLE_TRANSFER.items():
                if core == OMITTED_CORE[omitted]:
                    continue
                final[supplier].remove(core)
                final[recipient].add(core)
            assert set().union(*final.values()) == initial_union
            changed = {
                holder: final[holder] != initial[holder] for holder in initial
            }
            assert all(changed.values())
            symmetric_differences = {
                holder: sorted(final[holder] ^ initial[holder])
                for holder in initial
            }
            assert all(symmetric_differences.values())
            rows.append({
                "d_core": d_core,
                "omitted_source": omitted,
                "all_targets_changed": True,
                "symmetric_differences": symmetric_differences,
            })
    assert len(rows) == 6
    return rows


def run(root: Path):
    script = Path(__file__).resolve()
    theorem = root / "results" / "FORM2_SIX_BRANCH_ALL_TARGET_CHANGE_REPEAT_FRONTIER_20260814.md"
    rows = branch_rows()
    return {
        "schema": "form2-six-branch-all-target-change-v1",
        "status": "ALL_SIX_BRANCHES_CHANGE_ALL_FIVE_TARGETS",
        "branch_count": len(rows),
        "branches": rows,
        "record_consequence": (
            "a response at a branch target cannot be an unchanged-Y-target "
            "record; a non-new complete decorated record is cross-state"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
        "claim_boundary": (
            "cap-free physical target-change audit; whether an old cross-state "
            "record satisfies the extraction terminal is not proved"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"], "branch_count": result["branch_count"]
    }, indent=2))


if __name__ == "__main__":
    main()
