from fractions import Fraction


def realizable(total, least, singleton):
    total = Fraction(total)
    least = Fraction(least)
    return total == least if singleton else total >= 2 * least


def test_shared_packet_cardinality_realizability_boundary():
    assert realizable(1, 1, True)
    assert not realizable(2, 1, True)
    assert realizable(2, 1, False)
    assert realizable(3, 1, False)
    assert not realizable(Fraction(3, 2), 1, False)
