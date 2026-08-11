import json
from pathlib import Path

from .audit_mixed_margin_hamiltonian_charity_path_composition import run


ROOT = Path(__file__).resolve().parents[2]


def test_mixed_margin_hamiltonian_charity_path_composition_replays():
    expected = json.loads(
        (ROOT / "results/mixed_margin_hamiltonian_charity_path_composition_audit.json").read_text()
    )
    assert run(ROOT) == expected


def test_mixed_margin_hamiltonian_charity_path_dependencies_replay():
    result = run(ROOT)
    assert result["status"] == "DEPENDENCIES_REPLAYABLE"
    assert result["dependency_count"] == 14
    assert all(record["audit_status"] in {"ALL_FORCED", "ALL_EXHAUSTED", "DEPENDENCIES_REPLAYABLE"} for record in result["records"])
