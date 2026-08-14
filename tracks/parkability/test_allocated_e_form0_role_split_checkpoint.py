from pathlib import Path

from .audit_allocated_e_form0_role_split_checkpoint import run


def test_allocated_e_form0_role_split_checkpoint():
    root = Path(__file__).resolve().parents[2]
    source = root / "results/allocated_e_form0_role_split_pi_cegar_resume15250.json"
    result = run(root, source)
    assert result["status"] == "ROLE_SPLIT_20000_CUT_CHAIN_VERIFIED"
    assert result["distinct_family_count"] == 20000
    assert all(result["checks"].values())
