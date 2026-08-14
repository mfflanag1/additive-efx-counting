from pathlib import Path

from .audit_external_hall_full_owner_recruitment import run


def test_only_r3_represented_stars_avoid_full_owner_recruitment():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"].startswith("ONLY_R3_REPRESENTED_2X1")
    assert result["distinct_residual_decorations"] >= 3
    for row in result["residual_decorations"]:
        assert row["form"] == "R3"
        assert "d" not in row["targets"] + row["sources"]
