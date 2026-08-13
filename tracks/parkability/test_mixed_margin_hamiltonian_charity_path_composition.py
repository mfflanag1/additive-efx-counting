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
    assert result["status"] == "RESPONSE_GEOMETRY_COMPLETE_OPEN_MIXED_PAYMENT"
    assert result["dependency_count"] == 27
    assert result["exact_surviving_separator"] == "supplier-saturated mixed-cycle observer payment and two anchor reverse inequalities"
    assert any(record["audit_status"] == "TERMINATION_GAP_FOUND" for record in result["records"])
    assert any(
        record["audit_status"] == "STATED_SPLICE_NORMAL_FORM_VACUOUS"
        for record in result["records"]
    )
