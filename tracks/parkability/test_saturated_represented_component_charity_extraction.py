import json
from pathlib import Path

from .audit_saturated_represented_component_charity_extraction import run


ROOT = Path(__file__).resolve().parents[2]


def test_represented_component_extraction_replays() -> None:
    expected = json.loads(
        (ROOT / "results/saturated_represented_component_charity_extraction_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_represented_component_case_counts() -> None:
    result = run(ROOT)
    assert result["status"] == "ALL_SATURATED_COMPONENTS_EXCLUDED"
    assert result["component_size_counts"] == {"2": 12, "3": 48, "4": 72}
    assert all(result["checks"].values())
