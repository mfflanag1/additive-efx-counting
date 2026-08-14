from .analyze_endpoint6_three_way_h_release_payment import run


def test_payment_analysis_driver_is_importable():
    assert callable(run)
