import json
from pathlib import Path

from .audit_root_response_floater_substitution_dichotomy import run


ROOT = Path(__file__).resolve().parents[2]


def test_root_response_floater_substitution_replays():
    expected = json.loads(
        (ROOT / "results/root_response_floater_substitution_dichotomy_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_root_response_floater_substitution_is_forced():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert all(record["status"] == "unsat" for record in result["records"])
