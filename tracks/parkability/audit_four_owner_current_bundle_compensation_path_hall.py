#!/usr/bin/env python3
"""Exhaustive Boolean/support audit of the four-owner path-Hall theorem."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    edge_names = ("th", "ta", "tb", "ah", "bh", "ab", "ba")
    cases = 0
    equivalence = True
    success_counts = {"th": 0, "tah": 0, "tbh": 0, "tabh": 0, "tbah": 0}
    for bits in itertools.product((False, True), repeat=len(edge_names)):
        e = dict(zip(edge_names, bits))
        paths = {
            "th": e["th"],
            "tah": e["ta"] and e["ah"],
            "tbh": e["tb"] and e["bh"],
            "tabh": e["ta"] and e["ab"] and e["bh"],
            "tbah": e["tb"] and e["ba"] and e["ah"],
        }
        for name, paid in paths.items():
            success_counts[name] += int(paid)
        no_path = not any(paths.values())
        hall_cut = (
            (not e["th"])
            and ((not e["ta"]) or (not e["ah"]))
            and ((not e["tb"]) or (not e["bh"]))
            and ((not e["ta"]) or (not e["ab"]) or (not e["bh"]))
            and ((not e["tb"]) or (not e["ba"]) or (not e["ah"]))
        )
        equivalence &= no_path == hall_cut
        cases += 1
    assert cases == 128 and equivalence

    # Exact support conservation for the two longest paths.
    d, ell = {0, 1}, {2}
    zt, za, zb = {3, 4}, {5}, {6, 7}
    old = {"h": d | ell, "t": zt, "a": za, "b": zb}
    tabh = {"h": ell | zb, "t": d, "a": zt, "b": za}
    tbah = {"h": ell | za, "t": d, "b": zt, "a": zb}
    universe = set().union(*old.values())
    for new in (tabh, tbah):
        assert set().union(*new.values()) == universe
        assert sum(map(len, new.values())) == len(universe)
        assert not (new["h"] & d)

    theorem = ROOT / "results/FOUR_OWNER_CURRENT_BUNDLE_COMPENSATION_PATH_HALL_THEOREM_20260814.md"
    supplier = ROOT / "results/RETIREMENT_SUPPLIER_THREE_CYCLE_OR_TWO_ROW_CUT_LEMMA_20260814.md"
    bilateral = ROOT / "results/CANONICAL_WHOLE_HIT_BILATERAL_SWAP_OR_SOURCE_UNDERPAYMENT_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "four-owner-current-bundle-compensation-path-hall-audit-v1",
        "status": "ALL_FIVE_SIMPLE_COMPENSATION_PATHS_EXHAUSTED",
        "boolean_edge_assignments_checked": cases,
        "no_path_iff_displayed_hall_cut": equivalence,
        "path_success_counts": success_counts,
        "long_path_support_conserved": True,
        "new_holder_target_avoids_named_packet": True,
        "remaining_separator": "five_path_current_bundle_hall_cut",
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, supplier, bilateral, script)
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
