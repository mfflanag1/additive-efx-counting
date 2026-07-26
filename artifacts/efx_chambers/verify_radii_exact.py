#!/usr/bin/env python3
"""Independent standard-library verifier for the six EFX0 chamber radii."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import time
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE_MANIFEST = ROOT / "repro/counting_witnesses/instances.json"
CERTIFICATES = HERE / "certificates.json"
MANIFEST = HERE / "MANIFEST.json"

CERTIFICATE_KEYS = {
    "id",
    "source",
    "source_sha256",
    "n",
    "m",
    "expected_efx0_count",
    "status",
    "allocation_space",
    "efx0_count",
    "nontrivial_efx_zero_constraints",
    "efx_allocations_with_nontrivial_zero",
    "tautological_zero_constraints",
    "minimum_raw_efx_slack",
    "efx_normalized_margin",
    "non_efx_kill_margin",
    "positive_orthant_margin",
    "certified_open_radius",
    "certified_closed_radius",
}
FRACTION_KEYS = {"numerator", "denominator", "fraction"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_fraction(record: object, label: str) -> Fraction:
    require(isinstance(record, dict), f"{label} must be an object")
    require(set(record) == FRACTION_KEYS, f"{label} has unexpected fields")
    numerator = record["numerator"]
    denominator = record["denominator"]
    require(
        type(numerator) is int
        and type(denominator) is int
        and denominator > 0,
        f"{label} has an invalid numerator or denominator",
    )
    value = Fraction(numerator, denominator)
    require(value.numerator == numerator, f"{label} numerator is not reduced")
    require(value.denominator == denominator, f"{label} denominator is not reduced")
    require(record["fraction"] == str(value), f"{label} text is inconsistent")
    return value


def load_provenance() -> dict:
    manifest = json.loads(MANIFEST.read_text())
    require(
        set(manifest)
        == {
            "schema",
            "artifact",
            "base_git_commit",
            "working_tree_note",
            "source_manifest",
            "source_manifest_sha256",
            "files",
            "commands",
        },
        "provenance manifest has unexpected fields",
    )
    require(manifest["schema"] == 1, "unsupported provenance schema")
    require(manifest["artifact"] == "efx_chambers", "wrong provenance artifact")
    require(
        manifest["source_manifest"]
        == str(SOURCE_MANIFEST.relative_to(ROOT)),
        "wrong provenance source manifest",
    )
    require(
        manifest["source_manifest_sha256"] == sha256(SOURCE_MANIFEST),
        "provenance source-manifest hash mismatch",
    )
    files = manifest["files"]
    require(isinstance(files, dict) and files, "provenance files must be nonempty")
    for relative, expected_hash in files.items():
        require(type(relative) is str, "invalid provenance path")
        require(
            type(expected_hash) is str and len(expected_hash) == 64,
            f"invalid provenance digest for {relative}",
        )
        path = ROOT / relative
        require(path.is_file(), f"missing provenance file: {relative}")
        require(sha256(path) == expected_hash, f"hash mismatch: {relative}")
    return manifest


def load_inputs() -> tuple[list[dict], dict[str, dict]]:
    source_manifest = json.loads(SOURCE_MANIFEST.read_text())
    require(source_manifest.get("schema") == 1, "unsupported source schema")
    sources = source_manifest.get("instances")
    require(isinstance(sources, list) and sources, "missing source instances")
    source_ids = [source.get("id") for source in sources]
    require(
        len(source_ids) == len(set(source_ids)),
        "duplicate source instance id",
    )

    certificate = json.loads(CERTIFICATES.read_text())
    require(
        set(certificate)
        == {
            "schema",
            "source_manifest",
            "source_manifest_sha256",
            "witnesses",
        },
        "certificate has unexpected top-level fields",
    )
    require(certificate["schema"] == 1, "unsupported certificate schema")
    require(
        certificate["source_manifest"]
        == str(SOURCE_MANIFEST.relative_to(ROOT)),
        "certificate names the wrong source manifest",
    )
    require(
        certificate["source_manifest_sha256"] == sha256(SOURCE_MANIFEST),
        "certificate source-manifest hash mismatch",
    )
    witnesses = certificate["witnesses"]
    require(isinstance(witnesses, list), "certificate witnesses must be a list")
    expected_by_id = {}
    for record in witnesses:
        require(
            isinstance(record, dict) and set(record) == CERTIFICATE_KEYS,
            "certificate witness has unexpected fields",
        )
        witness_id = record["id"]
        require(
            type(witness_id) is str and witness_id not in expected_by_id,
            f"duplicate or invalid certificate id: {witness_id}",
        )
        expected_by_id[witness_id] = record
    require(
        set(expected_by_id) == set(source_ids),
        "source and certificate witness ids differ",
    )
    return sources, expected_by_id


def validate_instance(instance: object, source: dict, expected: dict) -> list[list[int]]:
    require(isinstance(instance, dict), f'{source["id"]}: instance must be an object')
    n = instance.get("n")
    m = instance.get("m")
    values = instance.get("values")
    require(type(n) is int and n >= 2, f'{source["id"]}: invalid n')
    require(type(m) is int and m >= 1, f'{source["id"]}: invalid m')
    require(
        isinstance(values, list)
        and len(values) == n
        and all(isinstance(row, list) and len(row) == m for row in values),
        f'{source["id"]}: malformed valuation matrix',
    )
    require(
        all(type(value) is int and value > 0 for row in values for value in row),
        f'{source["id"]}: values must be positive integers',
    )
    require(expected["n"] == n and expected["m"] == m, f'{source["id"]}: shape mismatch')
    require(
        expected["allocation_space"] == n**m,
        f'{source["id"]}: allocation-space mismatch',
    )
    return values


def subset_tables(
    values: list[list[int]],
) -> tuple[
    list[int],
    list[list[int]],
    list[list[int]],
    list[list[int]],
]:
    m = len(values[0])
    size = 1 << m
    cardinality = [mask.bit_count() for mask in range(size)]
    totals = []
    minima = []
    minimum_goods = []
    for row in values:
        row_totals = [0] * size
        row_minima = [0] * size
        row_minimum_goods = [-1] * size
        for mask in range(1, size):
            bit = mask & -mask
            good = bit.bit_length() - 1
            rest = mask ^ bit
            row_totals[mask] = row_totals[rest] + row[good]
            if rest == 0 or (row[good], good) < (
                row_minima[rest],
                row_minimum_goods[rest],
            ):
                row_minima[mask] = row[good]
                row_minimum_goods[mask] = good
            else:
                row_minima[mask] = row_minima[rest]
                row_minimum_goods[mask] = row_minimum_goods[rest]
        totals.append(row_totals)
        minima.append(row_minima)
        minimum_goods.append(row_minimum_goods)
    return cardinality, totals, minima, minimum_goods


def definition_forms(values, assignment):
    """Yield every EFX0 form, including support-zero identities."""
    n = len(values)
    m = len(assignment)
    bundles = [[] for _ in range(n)]
    for good, owner in enumerate(assignment):
        bundles[owner].append(good)
    counts = [len(bundle) for bundle in bundles]
    totals = [[0] * n for _ in range(n)]
    for observer in range(n):
        for owner in range(n):
            totals[observer][owner] = sum(
                values[observer][good] for good in bundles[owner]
            )
    for removed_good in range(m):
        target = assignment[removed_good]
        for observer in range(n):
            if observer == target:
                continue
            slack = (
                totals[observer][observer]
                - totals[observer][target]
                + values[observer][removed_good]
            )
            support = counts[observer] + counts[target] - 1
            yield {
                "observer": observer,
                "target": target,
                "removed_good": removed_good,
                "slack": slack,
                "support": support,
            }


def exact_best_violation(values, assignment) -> tuple[Fraction | None, dict | None]:
    best = None
    witness = None
    for form in definition_forms(values, assignment):
        if form["support"] == 0:
            require(form["slack"] == 0, "support-zero form is not an identity")
            continue
        if form["slack"] < 0:
            candidate = Fraction(-form["slack"], form["support"])
            if best is None or candidate > best:
                best = candidate
                witness = form
    return best, witness


def analyze_efx_allocation(
    values,
    assignment,
    alpha: Fraction,
) -> dict:
    nontrivial_zero = 0
    tautologies = 0
    raw_minimum = None
    alpha_witness = None
    for form in definition_forms(values, assignment):
        slack = form["slack"]
        support = form["support"]
        if support == 0:
            require(slack == 0, "support-zero form is not an identity")
            tautologies += 1
            continue
        require(slack >= 0, "pair-tight classification disagrees with definition")
        raw_minimum = slack if raw_minimum is None else min(raw_minimum, slack)
        if slack == 0:
            nontrivial_zero += 1
        margin = Fraction(slack, support)
        require(margin >= alpha, "claimed alpha is not a universal lower bound")
        if margin == alpha and alpha_witness is None:
            alpha_witness = form
    return {
        "nontrivial_zero": nontrivial_zero,
        "tautologies": tautologies,
        "raw_minimum": raw_minimum,
        "alpha_witness": alpha_witness,
    }


def verify_witness(source: dict, expected: dict) -> dict:
    started = time.perf_counter()
    witness_id = source["id"]
    require(expected["id"] == witness_id, f"{witness_id}: id mismatch")
    require(expected["source"] == source["path"], f"{witness_id}: source mismatch")
    require(
        expected["source_sha256"] == source["sha256"],
        f"{witness_id}: source digest mismatch",
    )
    require(
        expected["expected_efx0_count"] == source["expected_efx0_count"],
        f"{witness_id}: expected count mismatch",
    )
    source_path = ROOT / source["path"]
    require(source_path.is_file(), f"{witness_id}: missing source file")
    require(sha256(source_path) == source["sha256"], f"{witness_id}: bad source hash")
    instance = json.loads(source_path.read_text())
    values = validate_instance(instance, source, expected)
    n = len(values)
    m = len(values[0])

    alpha = parse_fraction(
        expected["efx_normalized_margin"], f"{witness_id}.alpha"
    )
    beta = parse_fraction(
        expected["non_efx_kill_margin"], f"{witness_id}.beta"
    )
    positivity = parse_fraction(
        expected["positive_orthant_margin"], f"{witness_id}.positivity"
    )
    open_radius = parse_fraction(
        expected["certified_open_radius"], f"{witness_id}.open_radius"
    )
    closed_radius = parse_fraction(
        expected["certified_closed_radius"], f"{witness_id}.closed_radius"
    )
    require(expected["status"] == "CERTIFIED", f"{witness_id}: expected certification")
    require(alpha > 0 and beta > 0 and positivity > 0, f"{witness_id}: nonpositive margin")
    require(
        positivity == min(min(row) for row in values),
        f"{witness_id}: positivity margin mismatch",
    )
    require(
        open_radius == min(alpha, beta, positivity),
        f"{witness_id}: open radius mismatch",
    )
    require(
        closed_radius == open_radius / 2,
        f"{witness_id}: closed radius mismatch",
    )

    cardinality, totals, minima, _minimum_goods = subset_tables(values)
    total_allocations = n**m
    assignment = [0] * m
    bundles = [(1 << m) - 1] + [0] * (n - 1)
    efx_allocations = []
    nontrivial_zero_constraints = 0
    efx_allocations_with_zero = 0
    tautological_zero_constraints = 0
    minimum_raw_efx_slack = None
    alpha_equality = None
    beta_equality = None
    beta_allocations_checked = 0

    for allocation_index in range(total_allocations):
        certified_non_efx = False
        saw_negative = False
        possible_beta_equality = False

        for observer in range(n):
            own_mask = bundles[observer]
            own_value = totals[observer][own_mask]
            own_size = cardinality[own_mask]
            observer_totals = totals[observer]
            observer_minima = minima[observer]
            for target in range(n):
                if target == observer:
                    continue
                target_mask = bundles[target]
                if target_mask == 0:
                    continue
                support = own_size + cardinality[target_mask] - 1
                if support == 0:
                    continue
                slack = (
                    own_value
                    - observer_totals[target_mask]
                    + observer_minima[target_mask]
                )
                if slack >= 0:
                    continue
                saw_negative = True
                violation = -slack
                comparison = (
                    violation * beta.denominator
                    - beta.numerator * support
                )
                if comparison > 0:
                    certified_non_efx = True
                    break
                if comparison == 0:
                    if beta_equality is not None:
                        certified_non_efx = True
                        break
                    possible_beta_equality = True
            if certified_non_efx:
                break

        if certified_non_efx:
            beta_allocations_checked += 1
        elif saw_negative:
            exact_best, exact_witness = exact_best_violation(values, assignment)
            require(exact_best is not None, "negative allocation has no violation")
            require(
                exact_best >= beta,
                f"{witness_id}: claimed beta is not a universal lower bound",
            )
            beta_allocations_checked += 1
            if exact_best == beta and beta_equality is None:
                require(possible_beta_equality, "beta equality lost in pair reduction")
                beta_equality = {
                    "allocation": list(assignment),
                    "constraint": exact_witness,
                }
        else:
            detail = analyze_efx_allocation(values, assignment, alpha)
            efx_allocations.append(list(assignment))
            nontrivial_zero_constraints += detail["nontrivial_zero"]
            tautological_zero_constraints += detail["tautologies"]
            if detail["nontrivial_zero"]:
                efx_allocations_with_zero += 1
            raw = detail["raw_minimum"]
            if raw is not None:
                minimum_raw_efx_slack = (
                    raw
                    if minimum_raw_efx_slack is None
                    else min(minimum_raw_efx_slack, raw)
                )
            if detail["alpha_witness"] is not None and alpha_equality is None:
                alpha_equality = {
                    "allocation": list(assignment),
                    "constraint": detail["alpha_witness"],
                }

        if allocation_index + 1 == total_allocations:
            continue
        good = 0
        while good < m:
            old_owner = assignment[good]
            bit = 1 << good
            bundles[old_owner] ^= bit
            new_owner = old_owner + 1
            if new_owner < n:
                assignment[good] = new_owner
                bundles[new_owner] |= bit
                break
            assignment[good] = 0
            bundles[0] |= bit
            good += 1
        require(good < m, "allocation odometer terminated early")

    require(
        len(efx_allocations) == expected["efx0_count"],
        f"{witness_id}: EFX0 count mismatch",
    )
    require(
        expected["efx0_count"] == expected["expected_efx0_count"],
        f"{witness_id}: certificate expected-count mismatch",
    )
    require(
        beta_allocations_checked == total_allocations - len(efx_allocations),
        f"{witness_id}: not every non-EFX allocation received a beta witness",
    )
    require(alpha_equality is not None, f"{witness_id}: no alpha equality witness")
    require(beta_equality is not None, f"{witness_id}: no beta equality witness")
    require(
        nontrivial_zero_constraints
        == expected["nontrivial_efx_zero_constraints"],
        f"{witness_id}: nontrivial equality count mismatch",
    )
    require(
        efx_allocations_with_zero
        == expected["efx_allocations_with_nontrivial_zero"],
        f"{witness_id}: equality-allocation count mismatch",
    )
    require(
        tautological_zero_constraints
        == expected["tautological_zero_constraints"],
        f"{witness_id}: tautology count mismatch",
    )
    require(
        minimum_raw_efx_slack == expected["minimum_raw_efx_slack"],
        f"{witness_id}: raw EFX slack mismatch",
    )

    return {
        "id": witness_id,
        "status": "PASS",
        "allocation_space": total_allocations,
        "efx0_count": len(efx_allocations),
        "efx0_allocations": sorted(efx_allocations),
        "alpha": str(alpha),
        "beta": str(beta),
        "open_radius": str(open_radius),
        "closed_radius": str(closed_radius),
        "alpha_equality_witness": alpha_equality,
        "beta_equality_witness": beta_equality,
        "non_efx_allocations_with_beta_witness": beta_allocations_checked,
        "seconds": round(time.perf_counter() - started, 6),
    }


def tight_pair_profile(values, assignment) -> tuple[bool, Fraction | None]:
    n = len(values)
    bundles = [0] * n
    for good, owner in enumerate(assignment):
        bundles[owner] |= 1 << good
    cardinality, totals, minima, _ = subset_tables(values)
    best = None
    for observer in range(n):
        own_mask = bundles[observer]
        own_value = totals[observer][own_mask]
        own_size = cardinality[own_mask]
        for target in range(n):
            if target == observer or bundles[target] == 0:
                continue
            target_mask = bundles[target]
            support = own_size + cardinality[target_mask] - 1
            if support == 0:
                continue
            slack = (
                own_value
                - totals[observer][target_mask]
                + minima[observer][target_mask]
            )
            if slack < 0:
                candidate = Fraction(-slack, support)
                best = candidate if best is None else max(best, candidate)
    return best is None, best


def reduction_regression() -> dict:
    matrices = [
        [[1, 1, 1], [1, 1, 1]],
        [[1, 3, 2], [2, 1, 4]],
        [[3, 1, 4, 2], [2, 5, 1, 3], [4, 2, 3, 1]],
    ]
    checked = 0
    for values in matrices:
        n = len(values)
        m = len(values[0])
        for assignment_tuple in itertools.product(range(n), repeat=m):
            assignment = list(assignment_tuple)
            forms = list(definition_forms(values, assignment))
            direct_best = max(
                (
                    Fraction(-form["slack"], form["support"])
                    for form in forms
                    if form["support"] > 0 and form["slack"] < 0
                ),
                default=None,
            )
            direct_efx = direct_best is None
            tight_efx, tight_best = tight_pair_profile(values, assignment)
            require(
                (direct_efx, direct_best) == (tight_efx, tight_best),
                "tight-pair reduction disagrees with every-good definition",
            )
            checked += 1
    return {"status": "PASS", "allocations_checked": checked}


def obstruction_regression() -> dict:
    values = [[1, 1, 1], [1, 1, 1]]
    obstructed_allocations = 0
    zero_constraints = 0
    witness = None
    for assignment_tuple in itertools.product(range(2), repeat=3):
        assignment = list(assignment_tuple)
        forms = list(definition_forms(values, assignment))
        if all(form["slack"] >= 0 for form in forms):
            zeros = [
                form
                for form in forms
                if form["support"] > 0 and form["slack"] == 0
            ]
            zero_constraints += len(zeros)
            if zeros:
                obstructed_allocations += 1
                if witness is None:
                    witness = (assignment, zeros[0])
    require(witness is not None, "equality obstruction was not detected")

    assignment, form = witness
    perturbed = [[Fraction(value) for value in row] for row in values]
    bundles = [[] for _ in range(2)]
    for good, owner in enumerate(assignment):
        bundles[owner].append(good)
    delta = Fraction(1, 4)
    for good in bundles[form["observer"]]:
        perturbed[form["observer"]][good] -= delta
    for good in bundles[form["target"]]:
        if good != form["removed_good"]:
            perturbed[form["observer"]][good] += delta
    require(
        all(value > 0 for row in perturbed for value in row),
        "obstruction perturbation left the positive orthant",
    )
    original_forms = list(definition_forms(values, assignment))
    perturbed_forms = list(definition_forms(perturbed, assignment))
    require(all(form["slack"] >= 0 for form in original_forms), "bad obstruction witness")
    require(
        any(form["slack"] < 0 for form in perturbed_forms),
        "zero form did not obstruct an arbitrarily small perturbation",
    )

    identity_values = [[1], [1]]
    for assignment_tuple in itertools.product(range(2), repeat=1):
        forms = list(definition_forms(identity_values, list(assignment_tuple)))
        require(all(form["slack"] >= 0 for form in forms), "one-good allocation is not EFX0")
        require(
            all(form["support"] == 0 for form in forms),
            "one-good zero form is unexpectedly nontrivial",
        )
    return {
        "status": "PASS",
        "nontrivial_zero_constraints": zero_constraints,
        "efx_allocations_with_nontrivial_zero": obstructed_allocations,
        "positive_perturbation_breaks_efx0": True,
        "support_zero_identities_ignored": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", action="append", default=[], metavar="ID")
    args = parser.parse_args()

    started = time.perf_counter()
    provenance = load_provenance()
    sources, expected_by_id = load_inputs()
    requested = set(args.only)
    selected = [
        source
        for source in sources
        if not requested or source["id"] in requested
    ]
    require(
        {source["id"] for source in selected}
        == (requested or {source["id"] for source in sources}),
        "unknown requested witness id",
    )

    reduction = reduction_regression()
    obstruction = obstruction_regression()
    results = []
    for source in selected:
        result = verify_witness(source, expected_by_id[source["id"]])
        results.append(result)
        print(
            f'PASS {result["id"]}: count={result["efx0_count"]}, '
            f'alpha={result["alpha"]}, beta={result["beta"]}, '
            f'seconds={result["seconds"]:.3f}',
            flush=True,
        )

    output = {
        "schema": 1,
        "status": "PASS",
        "method": (
            "independent standard-library certificate checker with exact "
            "integer/Fraction arithmetic"
        ),
        "provenance_manifest_sha256": sha256(MANIFEST),
        "base_git_commit": provenance["base_git_commit"],
        "tight_pair_definition_regression": reduction,
        "equality_obstruction_regression": obstruction,
        "witnesses": results,
        "seconds": round(time.perf_counter() - started, 6),
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
