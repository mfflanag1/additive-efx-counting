import json
from pathlib import Path

from .audit_charity_completed_path_root_response_anchor import run


ROOT = Path(__file__).resolve().parents[2]


def test_complete_path_root_anchor_replays():
    expected = json.loads(
        (ROOT / "results/charity_completed_path_root_response_anchor_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_complete_path_root_anchor_is_forced():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert all(record["status"] == "unsat" for record in result["records"])
