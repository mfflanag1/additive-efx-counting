import z3

from fractions import Fraction

from .audit_allocated_e_physical_packet_counterprofile import (
    find_closed_disjoint_families,
)

from .run_allocated_e_seven_endpoint_physical_pi_cegar import (
    all_self_pi_witnesses,
    physical_self_pi_witnesses,
    signatures_from_result,
    symbolic_pi_cut,
    witness_signature,
)
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


def test_symbolic_singleton_charity_self_pi_cut():
    value = {(piece, observer): z3.Real(f"pc_v_{piece}_{observer}")
             for piece in GOODS for observer in OWNERS}
    least = {(piece, observer): z3.Real(f"pc_l_{piece}_{observer}")
             for piece in GOODS for observer in OWNERS}
    singleton = {piece: z3.Bool(f"pc_s_{piece}") for piece in GOODS}
    witness = {"r": ["a0.0", "gr.0"]}
    cut = symbolic_pi_cut(value, least, singleton, witness)
    solver = z3.Solver()
    solver.add(least["a0", "r"] + least["gr", "r"] > 1)
    for observer in OWNERS:
        solver.add(
            z3.If(least["a0", observer] <= least["gr", observer],
                  least["gr", observer], least["a0", observer]) <= 1
        )
    solver.add(cut)
    assert solver.check() == z3.unsat


def test_all_closed_self_pi_witnesses_are_preseeded_exactly_once():
    witnesses = list(all_self_pi_witnesses())
    signatures = {witness_signature(witness) for witness in witnesses}
    assert len(witnesses) == 1372
    assert len(signatures) == len(witnesses)
    assert {next(iter(witness)) for witness in witnesses} == set(OWNERS)

    allowed_pieces = {
        "r": {"a0", "m", "gr"},
        "q": {"gq", "a1", "j", "gr"},
        "d": {"h", "k", "q0", "l", "gr"},
        "s": {"e", "p", "gr"},
    }
    for witness in witnesses:
        source, names = next(iter(witness.items()))
        assert names
        assert {name.rsplit(".", 1)[0] for name in names} <= allowed_pieces[source]
        assert "p.1" not in names


def test_min_free_symbolic_cut_matches_literal_minimum_definition():
    value = {(piece, observer): z3.Real(f"eq_v_{piece}_{observer}")
             for piece in GOODS for observer in OWNERS}
    least = {(piece, observer): z3.Real(f"eq_l_{piece}_{observer}")
             for piece in GOODS for observer in OWNERS}
    singleton = {piece: z3.Bool(f"eq_s_{piece}") for piece in GOODS}
    witness = {"q": ["a1.0", "j.1", "gr.0"]}
    actual = symbolic_pi_cut(value, least, singleton, witness)

    rows = []
    for observer in OWNERS:
        amounts = [least["a1", observer], value["j", observer] - least["j", observer],
                   least["gr", observer]]
        minimum = amounts[0]
        for amount in amounts[1:]:
            minimum = z3.If(amount < minimum, amount, minimum)
        rows.append(z3.Sum(*amounts) - minimum <= 1)
    expected = z3.Not(z3.And(
        z3.Not(singleton["j"]),
        least["a1", "q"] + value["j", "q"] - least["j", "q"]
        + least["gr", "q"] > 1,
        *rows,
    ))
    solver = z3.Solver()
    solver.add(actual != expected)
    assert solver.check() == z3.unsat


def test_physical_self_pi_batch_finds_only_minimal_closed_cores():
    goods = ("r0", "r1", "c0")
    base = {
        "r": ("r0", "r1"),
        "q": (),
        "d": (),
        "s": (),
        "charity": ("c0",),
    }
    values = {
        owner: {name: amount for name, amount in zip(goods, (0.6, 0.6, 0.2))}
        for owner in OWNERS
    }
    witnesses = physical_self_pi_witnesses(values, base)
    signatures = {witness_signature(witness) for witness in witnesses}
    assert signatures == {
        (("r", ("r0", "r1")),),
    }


def test_dynamic_closed_family_enumerator_batches_disjoint_witnesses():
    goods = ("r0", "r1", "q0", "q1")
    base = {
        "r": ("r0", "r1"),
        "q": ("q0", "q1"),
        "d": (),
        "s": (),
        "charity": (),
    }
    values = {
        owner: {name: Fraction(3, 5) for name in goods}
        for owner in OWNERS
    }
    witnesses, counts = find_closed_disjoint_families(
        values, goods, base, minimum_size=2, maximum=10,
    )
    assert witnesses
    assert len(witnesses) <= 10
    assert set(counts) == set(OWNERS)
    for witness in witnesses:
        selected = [name for names in witness.values() for name in names]
        assert len(selected) == len(set(selected))


def test_resume_signature_ledger_restores_batch_and_single_cuts():
    payload = {
        "restored_physical_pi_signatures": [
            [["r", ["a0.0", "gr.0"]]],
        ],
        "iterations": [
            {"batch_physical_pi_signatures": [
                [["q", ["a1.0", "j.1"]]],
            ]},
            {"physical_pi_signature": [
                ["d", ["h.0", "gr.0"]],
                ["r", ["a0.1", "m.0"]],
            ]},
        ],
    }
    assert len(signatures_from_result(payload)) == 3
