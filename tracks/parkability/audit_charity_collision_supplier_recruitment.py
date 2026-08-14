#!/usr/bin/env python3
"""Audit owner-cycle classification for base-charity supplier recruitment."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


OWNERS = ("r", "q", "d", "s")
SUPPLIER = "d"


def run(output: Path):
    rows = []
    outside = 0
    internal = 0
    for size in range(2, len(OWNERS) + 1):
        for subset in itertools.combinations(OWNERS, size):
            anchor = min(subset)
            for tail in itertools.permutations(owner for owner in subset if owner != anchor):
                cycle = (anchor, *tail)
                supplier_outside = SUPPLIER not in cycle
                outside += int(supplier_outside)
                internal += int(not supplier_outside)
                represented_after = set(cycle) | {SUPPLIER}
                assert len(represented_after) == (
                    len(cycle) + 1 if supplier_outside else len(cycle)
                )
                rows.append({
                    "cycle": list(cycle),
                    "supplier_outside": supplier_outside,
                    "represented_owner_count_before": len(cycle),
                    "represented_owner_count_after_using_collision_good": len(represented_after),
                })
    result = {
        "schema": "charity-collision-supplier-recruitment-audit-v1",
        "status": "AUDIT_PASSED",
        "current_supplier": SUPPLIER,
        "cycle_cases": len(rows),
        "outside_supplier_cases": outside,
        "internal_supplier_cases": internal,
        "rows": rows,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Audits the finite owner-union growth classification. The physical "
            "fact that moving a nonempty subpacket uses its current supplier is "
            "part of the fixed-U provenance definition."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
