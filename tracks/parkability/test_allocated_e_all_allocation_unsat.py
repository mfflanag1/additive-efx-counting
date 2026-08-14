from .audit_allocated_e_all_allocation_unsat import collect, structural_pi_signature


def test_terminal_cut_corpus_is_structurally_sound():
    from pathlib import Path

    source = Path("results/allocated_e_form2_all_allocation_atom_cegar.json").resolve()
    _, signatures, allocations = collect(source)
    assert len(signatures) == 46_683
    assert len(allocations) == 143
    assert all(structural_pi_signature(signature) for signature in signatures)
