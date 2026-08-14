import json
from pathlib import Path

from .audit_uncompensated_split_donor_reassembly_handoff import run


ROOT = Path(__file__).resolve().parents[2]


def test_split_donor_reassembly_replays() -> None:
    expected = json.loads(
        (ROOT / "results/uncompensated_split_donor_reassembly_handoff_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_split_donor_reassembly_claim_boundary() -> None:
    result = run(ROOT)
    assert result["status"] == "ALL_FORCED"
    assert all(result["checks"].values())
    assert "not by this audit alone proved EFX" in result["claim_boundary"]
