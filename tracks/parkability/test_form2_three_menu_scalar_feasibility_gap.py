from pathlib import Path

from .audit_form2_three_menu_scalar_feasibility_gap import run


def test_form2_three_menu_scalar_gap_witness():
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "EXACT_LOCAL_SCALAR_WITNESS"
    assert all(result["checks"].values())
