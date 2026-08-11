import json
from pathlib import Path

from .audit_evolved_target_minimal_source_trichotomy import run


ROOT = Path(__file__).resolve().parents[2]


def test_evolved_target_source_trichotomy_replays():
    expected = json.loads(
        (ROOT / "results/evolved_target_minimal_source_trichotomy_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_evolved_target_source_trichotomy_is_forced():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert all(record["status"] == "unsat" for record in result["records"])
