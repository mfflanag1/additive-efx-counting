import json
from pathlib import Path

from .audit_root_sourced_evolved_target_return_or_capture import run


ROOT = Path(__file__).resolve().parents[2]


def test_root_sourced_evolved_target_dichotomy_replays():
    expected = json.loads(
        (ROOT / "results/root_sourced_evolved_target_return_or_capture_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_root_sourced_evolved_target_dichotomy_is_forced():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert all(record["status"] == "unsat" for record in result["records"])
