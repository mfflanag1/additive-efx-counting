from pathlib import Path

import pytest

try:
    from .run_minimum_slot_orbit_cegar import run
except ImportError:
    from run_minimum_slot_orbit_cegar import run


def test_tracked_assertions_cannot_be_exported_as_standalone_smt2(tmp_path):
    with pytest.raises(
        ValueError,
        match="standalone SMT2 output requires untracked assertions",
    ):
        run(
            tmp_path / "result.json",
            timeout_seconds=1,
            max_iterations=1,
            seed=None,
            relabeling_mode="none",
            completion_batch_size=1,
            smt2_output=Path(tmp_path / "formula.smt2"),
            track_unsat_core=True,
        )


def test_core_minimization_requires_tracking(tmp_path):
    with pytest.raises(
        ValueError,
        match="UNSAT-core minimization requires tracked assertions",
    ):
        run(
            tmp_path / "result.json",
            timeout_seconds=1,
            max_iterations=1,
            seed=None,
            relabeling_mode="none",
            completion_batch_size=1,
            minimize_unsat_core=True,
        )
