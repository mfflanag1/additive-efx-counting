import json
from pathlib import Path

from .audit_canonical_root_response_two_stage_selector import run


ROOT = Path(__file__).resolve().parents[2]


def test_canonical_root_response_selector_replays():
    expected = json.loads(
        (ROOT / "results/canonical_root_response_two_stage_selector_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_canonical_root_response_selector_is_forced():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert all(record["status"] == "unsat" for record in result["records"])
