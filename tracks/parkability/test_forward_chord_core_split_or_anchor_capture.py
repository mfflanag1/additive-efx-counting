from pathlib import Path

from .audit_forward_chord_core_split_or_anchor_capture import run


ROOT = Path(__file__).resolve().parents[2]


def test_forward_chord_identity_partition() -> None:
    result = run(ROOT)
    assert result["status"] == "FORWARD_CHORD_REDUCED_TO_TWO_ANCHOR_INTERFACES"
    assert result["anchored_path_count"] == 6
    assert result["forward_order_count"] == 36
    assert result["identity_class_counts"] == {
        "adjacent_same_source_replacement": 18,
        "generic_nonadjacent_split": 6,
        "nonadjacent_anchor_source_release": 6,
        "nonadjacent_anchor_target_collision": 6,
    }


def test_forward_chord_capture_algebra() -> None:
    result = run(ROOT)
    assert all(result["symbolic_checks"].values())
    assert result["smallest_terminals"] == {
        "anchor_target": "nonempty response/anchor overlap hitting set",
        "anchor_source": "complete-residual-pool capture disjoint from protected anchor",
    }
