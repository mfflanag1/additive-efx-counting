from .audit_r2_response_role_critical_compression import run


def test_r2_response_role_critical_compression(tmp_path):
    root = __import__("pathlib").Path(__file__).resolve().parents[2]
    result = run(root)
    assert result["status"] == "R2_ROLE_COMPRESSION_SCALARS_VERIFIED"
    assert result["response_role_count"] == 21
    assert result["maximum_with_retained_d_minimum"] == 22
    assert all(result["checks"].values())
