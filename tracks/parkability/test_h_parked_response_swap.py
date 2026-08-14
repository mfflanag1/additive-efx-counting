from .analyze_hlw_physical_response_cores import CURRENT_TARGET_PIECES


def test_swap_uses_the_declared_nonroot_rows():
    assert CURRENT_TARGET_PIECES["d"] == ("h", "l", "m", "gq", "gr")
    assert CURRENT_TARGET_PIECES["s"] == ("e", "p")
