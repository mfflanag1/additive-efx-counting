from fractions import Fraction

from .run_allocated_e_form0_role_split_pi_cegar import (
    BASE, GOODS, OWNERS, find_closed_family,
)


def test_oracle_finds_selected_closed_family_when_all_owners_allowed():
    values = {
        owner: {good: Fraction(1, 100) for good in GOODS}
        for owner in OWNERS
    }
    # Give each owner a disjoint desired copy of its own base support. The
    # union is closed by construction and every deletion tail stays <= 1.
    for owner in OWNERS:
        for good in BASE[owner]:
            values[owner][good] = Fraction(3, len(BASE[owner]))
    family = find_closed_family(values)
    assert family is not None
    assert set(family) <= set(OWNERS)


def test_oracle_rejects_when_no_bundle_is_desired():
    values = {
        owner: {good: Fraction(1, 1000) for good in GOODS}
        for owner in OWNERS
    }
    assert find_closed_family(values) is None
