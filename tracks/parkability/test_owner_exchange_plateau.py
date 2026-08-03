import itertools


def threshold(values):
    return sum(values) - min(values)


def test_strict_zero_gain_replacement_has_minimum_slot_normal_form():
    for size in range(2, 6):
        for bundle in itertools.product(range(1, 6), repeat=size):
            for position, outgoing in enumerate(bundle):
                for incoming in range(outgoing + 1, 7):
                    replaced = bundle[:position] + (incoming,) + bundle[position + 1 :]
                    assert threshold(replaced) >= threshold(bundle)
                    if threshold(replaced) != threshold(bundle):
                        continue
                    residual = bundle[:position] + bundle[position + 1 :]
                    assert outgoing < min(residual)
                    assert incoming <= min(residual)
