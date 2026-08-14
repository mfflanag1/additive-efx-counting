"""Independent edge census and replay for root-missing anchor substitution."""

import itertools
import json
from collections import Counter
from pathlib import Path

from .audit_root_missing_anchor_substitution_or_critical_split import run


ROOT = Path(__file__).resolve().parents[2]


def test_anchor_substitution_replays_and_independently_counts():
    result = run()
    expected = json.loads(
        (ROOT / "results/root_missing_anchor_substitution_or_critical_split_audit.json").read_text()
    )
    assert result == expected
    assert result["survivor_map_count"] == 6
    assert result["labelled_anchor_map_count"] == 18
    assert result["substitution_edge_histogram"] == {"3": 6, "4": 12}
    assert result["supplier_alignment_histogram"] == {"aligned": 6, "misaligned": 12}
    assert result["all_substitutions_at_most_four_edges"]
    assert result["root_threshold_nonempty_under_wall"]
    assert result["source_split_identity"]
    assert not result["pure_cell_lift_proved"]
    assert not result["accumulated_fan_application_proved"]

    counts = Counter()
    for q in (1, 2, 3):
        for f in itertools.product(range(4), repeat=4):
            if any(f[t] == t for t in range(4)) or set(f) != {1, 2, 3}:
                continue
            a = f[0]
            if f.count(a) != 2:
                continue
            u = next(t for t in (1, 2, 3) if f[t] == a)
            pairs = {("c", 0)}
            if q != a:
                pairs.add((q, a))
            pairs.update((t, f[t]) for t in (1, 2, 3) if t != u)
            counts[(q == a, len(pairs))] += 1
    assert counts == {(True, 3): 6, (False, 4): 12}
    assert not result["observer_safety_proved"]
    assert not result["misaligned_wall_closed"]
    assert not result["fixed_u_theorem_proved"]
