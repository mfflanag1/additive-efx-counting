from .run_allocated_e_seven_endpoint_payment_cegar import run


def test_payment_cegar_imports():
    assert callable(run)
