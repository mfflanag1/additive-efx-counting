from pathlib import Path

from .audit_form0_full_owner_hamiltonian_path_payment import run


def test_form0_full_owner_path_payment():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "PATH_PAYMENT_OR_EXACT_ROOT_SEPARATOR"
    assert len(result["support_edges"]) == 4
