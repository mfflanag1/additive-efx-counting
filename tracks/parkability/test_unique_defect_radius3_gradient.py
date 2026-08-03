from fractions import Fraction

try:
    from .search_unique_defect_reciprocity_anneal import classify
    from .scan_charity_threshold_absorption import absorption_signature, eligible, tables, theta
except ImportError:
    from search_unique_defect_reciprocity_anneal import classify
    from scan_charity_threshold_absorption import absorption_signature, eligible, tables, theta


def test_nonstandard_two_good_transfer_union_is_enumerated():
    values = (
        (221, 237, 67, 45, 96, 201, 79, 202, 141),
        (209, 20, 143, 83, 114, 93, 96, 73, 109),
        (146, 21, 218, 168, 160, 10, 138, 162, 193),
        (239, 215, 101, 31, 22, 190, 7, 81, 144),
    )
    result = classify(values, (448, 48, 12, 1), 1)

    assert result["premise"]
    assert not result["reciprocal"]
    assert result["radius_three_gradient_exists"]
    assert result["elementary_gradient"]["move"] == {
        "kind": "2_good_transfer_union",
        "goods": [5, 8],
        "old_labels": [1, 0],
        "new_labels": [3, 1],
    }
    assert result["elementary_gradient"]["theta_change"] == "162841/1327670"
    assert result["elementary_gradient"]["signature"][0] == "17/940"


def test_full_unique_defect_requires_radius_four_component():
    values = (
        (23, 171, 39, 129, 183, 72, 127, 142, 15),
        (250, 51, 195, 53, 129, 107, 105, 112, 39),
        (7, 1, 247, 110, 118, 13, 164, 44, 88),
        (240, 191, 1, 207, 98, 44, 59, 159, 24),
    )
    masks = (448, 48, 12, 1)
    result = classify(values, masks, 1)

    assert result["premise"]
    assert result["elementary_gradient"] is None
    assert not result["radius_three_gradient_exists"]

    totals, thresholds = tables(values)
    row_totals = tuple(sum(row) for row in values)
    improved_masks = (192, 33, 260, 24)
    assert eligible(improved_masks, 1 << 1, totals, thresholds)
    assert (
        theta(improved_masks, totals, thresholds, row_totals)
        - theta(masks, totals, thresholds, row_totals)
        == Fraction(56811503, 319837881)
    )
    signature, witness = absorption_signature(
        improved_masks, 1 << 1, totals, thresholds, row_totals
    )
    assert [str(value) for value in signature] == [
        "65/1023",
        "59/901",
        "37/347",
        "43/198",
    ]
    assert witness == {"good": 1, "host": 2, "permutation": [0, 1, 2, 3]}

    champion_masks = (448, 1, 12, 18)
    assert eligible(champion_masks, 1 << 5, totals, thresholds)
    assert (
        theta(champion_masks, totals, thresholds, row_totals)
        - theta(masks, totals, thresholds, row_totals)
        == Fraction(22288, 354981)
    )
    champion_signature, champion_witness = absorption_signature(
        champion_masks, 1 << 5, totals, thresholds, row_totals
    )
    assert [str(value) for value in champion_signature] == [
        "49/1023",
        "101/901",
        "35/264",
        "140/1041",
    ]
    assert champion_witness == {
        "good": 5,
        "host": 1,
        "permutation": [0, 1, 2, 3],
    }
