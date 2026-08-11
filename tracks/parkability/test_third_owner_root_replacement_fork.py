import json
from pathlib import Path

from .audit_third_owner_root_replacement_fork import run


ROOT = Path(__file__).resolve().parents[2]


def test_third_owner_root_replacement_fork_replays():
    expected = json.loads(
        (ROOT / "results/third_owner_root_replacement_fork_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_third_owner_root_replacement_fork_is_exact():
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert len(result["alternatives"]) == 3
