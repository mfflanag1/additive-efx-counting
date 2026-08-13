from pathlib import Path

from .audit_anchored_endpoint_identity_trichotomy import run


ROOT = Path(__file__).resolve().parents[2]


def test_six_endpoints_collapse_to_three_identity_types() -> None:
    result = run(ROOT)
    assert result["status"] == "SIX_ENDPOINTS_REDUCED_TO_THREE_IDENTITY_TYPES"
    assert result["endpoint_count"] == 6
    assert set(result["identity_type_counts"].values()) == {2}
