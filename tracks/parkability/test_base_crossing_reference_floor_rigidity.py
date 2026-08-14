from .audit_base_crossing_reference_floor_rigidity import run


def test_base_crossing_reference_floor_rigidity() -> None:
    result = run()
    assert result["status"] == "BASE_FLOOR_EQUALITY_FACE_EXCLUDED"
    assert result["base_packet_cases_checked"] == 3840
    assert result["forbidden_base_crossings_found"] == 0
    assert result["reference_support_cases_checked"] == 256
    assert result["current_floor_foreign_transfer_cases_checked"] > 0
    assert not result["full_T_L_times_theorem_closed"]
