try:
    from .audit_bottleneck_hall_cut import audit
except ImportError:
    from audit_bottleneck_hall_cut import audit


def test_bottleneck_hall_cut_normal_form_exhaustive_n3():
    result = audit(3)

    assert result["status"] == "EXHAUSTIVE_AUDIT_PASSED"
    assert result["strict_graph_count"] == 265
    assert result["minimal_witness_count"] > 0
    assert result["residual_factorization_count"] > 0
    assert result["residual_expansion_count"] > 0
