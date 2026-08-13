from pathlib import Path

from .audit_endpoint_hole_core_exchange_selector import run


ROOT = Path(__file__).resolve().parents[2]


def test_endpoint_exchange_trichotomy_and_separator() -> None:
    result = run(ROOT)
    assert result["status"] == "EXACT_TRICHOTOMY_WITH_LOCAL_HOLE_SEPARATOR"
    witness = result["local_positive_rational_separator"]
    assert witness["middle_feasible_exchange_count"] > 0
    assert witness["successful_exchange_count"] == 0
    assert witness["hole_packet_inclusion_minimal"]
    assert witness["middle_core_inclusion_minimal_for_floor"]


def test_endpoint_exchange_symbolic_identities() -> None:
    result = run(ROOT)
    assert all(result["symbolic_checks"].values())
