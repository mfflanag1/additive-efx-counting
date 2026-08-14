from .audit_packet_compression_hidden_minimum import audit_arity


def test_hidden_minimum_implication_across_representative_arities():
    for arity in (1, 2, 3, 5, 8, 12):
        row = audit_arity(arity)
        assert row["hidden_minimum_strictly_below_every_compressed_atom"] == "unsat"
        assert row["hidden_minimum_cannot_be_singleton_atom"] == "unsat"
        assert row["margin_chain"] == "unsat"
