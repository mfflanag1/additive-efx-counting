import itertools
import json
from fractions import Fraction

import pytest
import z3

from .run_fixed_u_a1_three_good_cegar import (
    OWNERS,
    TARGET_GOODS,
    TARGET_ROLE,
    append_record,
    audit_record,
    build_realization_master,
    concrete_oracle,
    exact_efx_audit,
    load_frozen,
    load_records,
    physical_goods,
    symbolic_efx,
    witness_pattern,
)


PROFILE = "results/fixed_u_wild_forced_terminal_profile_20260820.json"
REPAIR = "results/fixed_u_terminal_profile_unrestricted_physical_decision_20260820.json"


@pytest.fixture(scope="module")
def instance():
    from pathlib import Path

    return load_frozen(Path(PROFILE), Path(REPAIR))


def realization_for_subset(total, minimum, subset):
    """Construct a positive row whose exact minimum-witness set is subset."""
    row = [minimum if index in subset else None for index in range(3)]
    remainder = total - len(subset) * minimum
    complement = [index for index in range(3) if index not in subset]
    for index in complement:
        row[index] = remainder / len(complement)
    assert min(row) == minimum
    assert {index for index, amount in enumerate(row) if amount == minimum} == subset
    return row


def test_exact_domain_covers_all_1296_labelled_witness_patterns(instance):
    _, _, totals, minima, _, _ = instance
    proper_nonempty = [
        set(subset)
        for size in (1, 2)
        for subset in itertools.combinations(range(3), size)
    ]
    assert len(proper_nonempty) == 6
    for observer in OWNERS:
        total = totals[observer][TARGET_ROLE]
        minimum = minima[observer][TARGET_ROLE]
        assert total > 3 * minimum
        rows = [realization_for_subset(total, minimum, subset)
                for subset in proper_nonempty]
        assert len({tuple(row) for row in rows}) == 6
    assert len(list(itertools.product(proper_nonempty, repeat=len(OWNERS)))) == 1296


def test_master_accepts_every_row_witness_subset(instance):
    _, _, totals, minima, _, _ = instance
    proper_nonempty = [
        set(subset)
        for size in (1, 2)
        for subset in itertools.combinations(range(3), size)
    ]
    for observer in OWNERS:
        for subset in proper_nonempty:
            solver, variables = build_realization_master(totals, minima)
            row = realization_for_subset(
                totals[observer][TARGET_ROLE], minima[observer][TARGET_ROLE], subset
            )
            solver.add(*(
                variables[observer, good] == z3.RealVal(str(amount))
                for good, amount in zip(TARGET_GOODS, row)
            ))
            assert solver.check() == z3.sat


def test_concrete_oracle_witness_is_exact_and_symbolic(instance):
    _, _, totals, minima, frozen, role_goods = instance
    values = {
        (observer, good): amount
        for observer, row in frozen.items()
        for good, amount in row.items()
        if good.split(":", 1)[0] != TARGET_ROLE
    }
    for observer in OWNERS:
        row = realization_for_subset(
            totals[observer][TARGET_ROLE], minima[observer][TARGET_ROLE], {0, 1}
        )
        for good, amount in zip(TARGET_GOODS, row):
            values[observer, good] = amount

    status, allocation, reason = concrete_oracle(values, role_goods, 4, 30)
    assert (status, reason) == ("sat", None)
    exact_efx_audit(allocation, values, role_goods, 4)

    solver, variables = build_realization_master(totals, minima)
    solver.add(*(
        variables[observer, good] == z3.RealVal(str(values[observer, good]))
        for observer in OWNERS for good in TARGET_GOODS
    ))
    solver.add(z3.Not(symbolic_efx(allocation, variables, frozen)))
    assert solver.check() == z3.unsat


def test_ledger_round_trip_and_tamper_detection(tmp_path, instance):
    _, _, totals, minima, frozen, role_goods = instance
    values = {
        (observer, good): amount
        for observer, row in frozen.items()
        for good, amount in row.items()
        if good.split(":", 1)[0] != TARGET_ROLE
    }
    for observer in OWNERS:
        row = realization_for_subset(
            totals[observer][TARGET_ROLE], minima[observer][TARGET_ROLE], {0}
        )
        for good, amount in zip(TARGET_GOODS, row):
            values[observer, good] = amount
    status, allocation, _ = concrete_oracle(values, role_goods, 4, 30)
    assert status == "sat"
    edges, slack = exact_efx_audit(allocation, values, role_goods, 4)
    payload = {
        "schema": "fixed-u-a1-three-good-cut-v1",
        "iteration": 0,
        "a1_values": {
            observer: {good: str(values[observer, good]) for good in TARGET_GOODS}
            for observer in OWNERS
        },
        "witness_pattern": witness_pattern(values, minima),
        "allocation": allocation,
        "edges": [list(edge) for edge in edges],
        "minimum_efx_slack": str(slack),
    }
    ledger = tmp_path / "nested" / "cuts.jsonl"
    append_record(ledger, payload)
    records = load_records(ledger)
    assert len(records) == 1
    audit_record(records[0], totals, minima, frozen, role_goods, 4)

    data = json.loads(ledger.read_text())
    data["minimum_efx_slack"] = "999"
    ledger.write_text(json.dumps(data) + "\n")
    with pytest.raises(AssertionError):
        load_records(ledger)

    ledger.write_text('{"iteration": 0')
    with pytest.raises(ValueError, match="torn ledger"):
        load_records(ledger)


def test_frozen_instance_has_21_goods(instance):
    _, _, _, _, _, role_goods = instance
    assert len(physical_goods(role_goods)) == 21
