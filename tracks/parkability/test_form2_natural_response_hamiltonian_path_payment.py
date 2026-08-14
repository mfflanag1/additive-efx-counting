from pathlib import Path

from .audit_form2_natural_response_hamiltonian_path_payment import run


def test_form2_natural_response_hamiltonian_path_payment():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "THREE_RECIPIENTS_PAID_OR_ROOT_CAPTURE"
    assert result["support_edges"] == [
        ["charity", "r"], ["q", "d"], ["r", "s"], ["s", "q"]
    ]
