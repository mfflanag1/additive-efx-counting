from .decide_external_hall_star_fork_menu import menu
from .run_fixed_u_full_packet_terminal_cegar import BASE
from .run_fixed_u_rank_three_relation_cegar import build_rank_three_master
from .run_full_capture_rank_three_cegar import (
    generalized_self_pi_free_constraints, ordinary_pi_free_constraints,
)

import z3


def test_external_hall_menu_counts_and_edge_bound():
    expected = {
        0: (15, 78, 13, 46, 53),
        2: (15, 78, 15, 60, 60),
    }
    for form_index, counts in expected.items():
        union, star, fork, star_records, fork_records = menu(form_index)
        observed = (
            len(star_records), len(fork_records), len(star), len(fork), len(union)
        )
        assert observed == counts
        assert all(len(topology) <= 4 for topology in union)


def test_every_star_signature_has_charity_and_an_external_transfer():
    for form_index in (0, 2):
        _, _, _, records, _ = menu(form_index)
        for record in records:
            topology = {tuple(edge) for edge in record["topology"]}
            assert ("charity", record["target"]) in topology
            assert record["external"] != record["target"]


def test_pi_calibration_distinguishes_live_and_vacuous_cells():
    for form_index in (0, 2):
        solver, value = build_rank_three_master(
            exclude_self_responses=True,
            required_owner_cycle_form=True,
            exact_owner_cycle_response_relation=True,
            owner_cycle_form_index=form_index,
        )
        solver.add(*ordinary_pi_free_constraints(value, BASE))
        assert solver.check() == z3.sat
        solver.add(*generalized_self_pi_free_constraints(value, BASE))
        assert solver.check() == z3.unsat
