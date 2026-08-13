import json
from pathlib import Path

from .audit_universal_full_owner_charity_exchange_extraction import run


def test_universal_full_owner_charity_exchange_extraction() -> None:
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "SATURATED_TERMINAL_EXCLUDED"
    assert result["path_count"] == 24
    assert result["nonself_source_count"] == 72
    assert all(result["checks"].values())
    assert result["scope"]["good_cap"] is None
    assert result["scope"]["moved_good_radius_cap"] is None


def test_universal_full_owner_charity_exchange_manifest_replays() -> None:
    root = Path(__file__).resolve().parents[2]
    expected = json.loads(
        (
            root
            / "results/universal_full_owner_charity_exchange_extraction_audit.json"
        ).read_text()
    )
    assert run(root) == expected
