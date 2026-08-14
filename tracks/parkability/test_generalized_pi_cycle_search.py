import json
from pathlib import Path

from .find_generalized_pi_cycle import (
    find_closed_core_families, find_cycle, find_cycles, run,
)
from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE


ROOT = Path(__file__).parents[2]


def test_generalized_pi_cycle_search_replays_strengthened_profiles():
    for stem in (
        "two_survivor_named_topology_form0_pi_free",
        "two_survivor_named_topology_form2_pi_free",
        "two_survivor_extended_root_reassembly_form0_pi_free",
        "two_survivor_extended_root_reassembly_form2_pi_free",
    ):
        source = ROOT / "results" / f"{stem}_decision.json"
        expected = json.loads((ROOT / "results" / f"{stem}_generalized_pi.json").read_text())
        assert run(source) == expected


def test_pi_finder_uses_declared_base_provenance():
    # With l allocated to d rather than charity, E={e,l} is not a one-edge
    # self PI: its incoming l is unavailable unless another edge releases it.
    values = {
        owner: {good: __import__("fractions").Fraction(1) for good in (
            "a0", "a1", "h", "j", "k", "q0", "l", "e", "m", "gq", "gr", "p"
        )}
        for owner in ("r", "q", "d", "s")
    }
    # Make E a minimal desired bundle while keeping every singleton undesired.
    values["s"]["e"] = __import__("fractions").Fraction(3, 5)
    values["s"]["l"] = __import__("fractions").Fraction(3, 5)
    witness, _ = find_cycle(values, ALLOCATED_E_BASE)
    if witness is not None and witness["cycle"] == ["s"]:
        assert witness["edges"][0]["incoming"] != ["l"]


def test_batch_finder_first_witness_matches_single_finder():
    profile = json.loads((
        ROOT / "results" / "two_survivor_named_topology_form0_pi_free_decision.json"
    ).read_text())
    from fractions import Fraction
    values = {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in profile["values"].items()
    }
    single, minimal_single = find_cycle(values)
    batch, minimal_batch = find_cycles(values)
    assert batch
    assert batch[0] == single
    assert minimal_batch == minimal_single


def test_closed_family_oracle_agrees_on_pi_existence():
    profile = json.loads((
        ROOT / "results" / "two_survivor_named_topology_form2_pi_free_decision.json"
    ).read_text())
    from fractions import Fraction
    values = {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in profile["values"].items()
    }
    cycle, _ = find_cycle(values)
    families, _ = find_closed_core_families(values, maximum=32)
    assert (cycle is not None) == bool(families)
