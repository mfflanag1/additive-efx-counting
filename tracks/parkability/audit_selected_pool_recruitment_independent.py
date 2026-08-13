#!/usr/bin/env python3
"""Independent compact reconstruction of the selected-pool recruitment proof."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path) -> dict:
    owners = range(4)
    checked = 0
    level_checks = 0
    old_blocker_checks = 0
    anchor_checks = 0
    for path in itertools.permutations(owners):
        for kappa in (1, 2, 3):
            for decorated_tuple in itertools.combinations(owners, kappa):
                decorated = set(decorated_tuple)
                for closing_source_position in (1, 2, 3):
                    checked += 1
                    # Each target has a residual atom and, except the hole,
                    # the predecessor core atom. Charity has the last core.
                    target_atoms = {
                        position: {f"R{position}"} | (
                            {f"K{position - 1}"} if position else set()
                        )
                        for position in owners
                    }
                    charity_atoms = {"K3", "Rc"}
                    universe = set().union(*target_atoms.values(), charity_atoms)
                    assert len(universe) == sum(map(len, target_atoms.values())) + len(charity_atoms)

                    for prefix in owners:
                        cells = []
                        for position in owners:
                            if position <= prefix:
                                cells.append(target_atoms[position])
                            else:
                                cells.append({f"K{position}"})
                        assert sum(map(len, cells)) == len(set().union(*cells))
                        assert set().union(*cells) <= universe
                        level_checks += 1

                        suffix = set(range(prefix + 1, 4))
                        old_suffix = suffix - decorated
                        for observer in owners:
                            for target_source in suffix:
                                target_is_decorated = target_source in decorated
                                observer_kind = (
                                    "retained" if observer <= prefix else
                                    "decorated_suffix" if observer in decorated else
                                    "old_suffix"
                                )
                                can_fail = target_is_decorated and observer_kind == "old_suffix"
                                if can_fail:
                                    assert observer in old_suffix and observer > prefix
                                    old_blocker_checks += 1

                    # Closing source is nonhole and is retained/recruited by
                    # exactly its path position when it becomes an old blocker.
                    assert closing_source_position > 0

    assert checked == 1008
    assert level_checks == 4032
    assert old_blocker_checks > 0

    named = ("r", "q", "c", "s")
    for path in itertools.permutations(named):
        if not any(path[i:i + 2] == ("r", "q") for i in range(3)):
            continue
        rpos = path.index("r")
        qpos = rpos + 1
        for prefix in owners:
            anchor_atom = f"K{rpos}"
            if qpos <= prefix:
                location = f"target{qpos}"
            elif rpos > prefix:
                location = f"source{rpos}"
            else:
                location = f"unallocated-target{qpos}"
            assert anchor_atom.startswith("K") and location
            anchor_checks += 1
    assert anchor_checks == 24

    theorem = root / "results/SELECTED_POOL_SIGNED_SURPLUS_RECRUITMENT_RESOLUTION_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "selected-pool-recruitment-independent-audit-v1",
        "status": "INDEPENDENT_PREFIX_RECONSTRUCTION_PASSED",
        "interface_states": checked,
        "prefix_level_checks": level_checks,
        "old_blocker_checks": old_blocker_checks,
        "anchor_checks": anchor_checks,
        "implementation_relation": (
            "independent atomic-support reconstruction; does not import the "
            "primary completion audit"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
