#!/usr/bin/env python3
"""Regression check for lossless allocated-E resume flattening."""

import json
from pathlib import Path

from .flatten_allocated_e_cegar_resume import ROOT, load_chain, witnesses
from .run_generalized_pi_named_selector_cegar import cycle_signature


def test_form2_flattened_resume_is_lossless():
    source = ROOT / "results" / "allocated_e_capture_form2_pairlinear_bulk_cegar.json"
    chain = load_chain(source)
    signatures = {
        cycle_signature(witness)
        for _, payload in chain for witness in witnesses(payload)
    }
    flattened = json.loads((
        ROOT / "results" / "allocated_e_capture_form2_pairlinear_flattened_resume.json"
    ).read_text())
    assert len(chain) == 3
    assert len(signatures) == 23847
    assert flattened["generalized_pi_cut_count"] == len(signatures)
    assert flattened["status"] == "FLATTENED_RESUME"
