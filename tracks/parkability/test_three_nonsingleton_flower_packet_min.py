#!/usr/bin/env python3
"""Regression checks for the packet-minimum flower normal form."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    support = json.loads(
        (ROOT / "results" / "three_nonsingleton_flower_support_mask_audit.json").read_text()
    )
    assert support["status"] == "OPEN"
    assert support["mask_count"] == 64
    assert support["counts"] == {"unsat": 60, "sat": 4, "unknown": 0}

    family = json.loads(
        (ROOT / "results" / "three_nonsingleton_flower_packet_min_family_audit.json").read_text()
    )
    assert family["status"] == "CLASSIFIED"
    assert family["cell_count"] == 6144
    assert family["counts"] == {"IMPOSSIBLE": 5124, "sat": 1020}
    expected = {
        ("c", "c"): {"IMPOSSIBLE": 1404, "sat": 132, "unknown": 0},
        ("s", "s"): {"IMPOSSIBLE": 1416, "sat": 120, "unknown": 0},
        ("c", "s"): {"IMPOSSIBLE": 1152, "sat": 384, "unknown": 0},
        ("s", "c"): {"IMPOSSIBLE": 1152, "sat": 384, "unknown": 0},
    }
    for summary in family["summaries"]:
        key = (summary["left_bottom_source"], summary["right_bottom_source"])
        assert summary["classification_verified"]
        assert summary["counts"] == expected[key]
        signatures = summary["survivor_signature_counts"]
        assert all(entry["aq_support"] == entry["ar_support"] == "both" for entry in signatures)
        if key[0] != key[1]:
            assert len(signatures) == 16
            assert all(entry["order_count"] == 24 for entry in signatures)
        elif key == ("c", "c"):
            assert sorted(entry["order_count"] for entry in signatures) == [12, 12, 12, 24, 24, 24, 24]
        else:
            assert sorted(entry["order_count"] for entry in signatures) == [8, 8, 8, 24, 24, 24, 24]

    witness = json.loads(
        (ROOT / "results" / "three_nonsingleton_flower_full_q_capture_witness.json").read_text()
    )
    assert witness["status"] == "sat"
    assert witness["aq_support"] == witness["ar_support"] == "both"
    assert witness["empty_rest"] == ["bq_rest", "tq_rest"]

    improvement = json.loads(
        (ROOT / "results" / "three_nonsingleton_flower_full_q_capture_improvement.json").read_text()
    )
    partial = improvement["nearest_partial_improvement"]
    assert partial["status"] == "SAT"
    assert partial["minimum_moved_goods"] == 2
    assert any(good.startswith("ar_bq") for good in partial["allocation"]["r"])
    assert any(good.startswith("aq_br") for good in partial["allocation"]["q"])
    assert partial["allocation"]["_"] == ["f"]

    swap_audit = json.loads(
        (ROOT / "results" / "bilateral_swap_obstruction_audit.json").read_text()
    )
    assert swap_audit["status"] == "ALL_FORCED"
    assert len(swap_audit["records"]) == 4
    swap_theorem = (
        ROOT / "results" / "BILATERAL_SWAP_OBSTRUCTION_LEMMA_20260810.md"
    ).read_text()
    assert "Agent `r` cannot fail any comparison" in swap_theorem
    assert "Wall-to-edge consequence" in swap_theorem

    theorem = (
        ROOT
        / "results"
        / "THREE_NONSINGLETON_CYCLE_CENSUS_AND_FLOWER_REDUCTION_20260809.md"
    ).read_text()
    assert "packet-minimum normal form" in theorem
    assert "fully captures `X_q`" in theorem
    assert "5,124 of 6,144" in theorem
    assert "bottom-crossing swap/PI lemma" in theorem
    print("three-nonsingleton flower packet-minimum tests passed")


if __name__ == "__main__":
    main()
