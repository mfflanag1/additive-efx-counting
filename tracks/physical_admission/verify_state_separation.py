#!/usr/bin/env python3
"""Exact physical-state checks; not a proof of universal A1 admission.

Named roles are nonempty disjoint packets of original physical goods. EFX is
checked by deleting each physical good, never by deleting an entire role.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import itertools
import json
from pathlib import Path

OWNERS = ("r", "q", "d", "s")
HOLDERS = (*OWNERS, "pool")
ROLES = ("a0", "a1", "h", "j", "k", "q0", "l", "e", "m", "gq", "gr", "p")
BASE = {"r": ("a0", "m"), "q": ("q0", "a1"), "d": ("h", "k", "gq"),
        "s": ("e", "p"), "pool": ("j", "l", "gr")}
SUPPORT = {"r": ("a0", "a1", "h"), "q": ("j", "k", "q0"),
           "d": ("m", "gq", "gr"), "s": ("l", "e"), "pool": ("p",)}
SCHEMA = "efx-physical-state-separation-v1"


class ValidationError(ValueError):
    """An exact physical premise or certificate check failed."""


def read_exact_json(path):
    """Reject ambiguous object keys and inexact/nonfinite JSON numbers."""
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValidationError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def reject_number(token):
        raise ValidationError(f"JSON numbers must be integers; use rational strings: {token}")

    try:
        return json.loads(Path(path).read_text(), object_pairs_hook=unique_object,
                          parse_float=reject_number, parse_constant=reject_number)
    except json.JSONDecodeError as exc:
        raise ValidationError("invalid JSON input") from exc


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise ValidationError("values must be exact integers, fractions, or rational strings")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValidationError("invalid rational value") from exc
    if result <= 0:
        raise ValidationError("all physical-good values must be strictly positive")
    return result


def total(row, goods):
    return sum((row[good] for good in goods), Fraction(0))


def tail(row, goods):
    goods = tuple(goods)
    return total(row, goods) - min((row[g] for g in goods), default=Fraction(0))


def expand(layout, roles):
    return {holder: tuple(g for role in names for g in roles[role])
            for holder, names in layout.items()}


def parse_profile(data):
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        raise ValidationError("unknown physical-state schema")
    roles = data.get("roles")
    if not isinstance(roles, dict) or set(roles) != set(ROLES):
        raise ValidationError("roles must contain exactly the twelve literal roles")
    goods = []
    for name in ROLES:
        packet = roles[name]
        if not isinstance(packet, (list, tuple)) or not packet:
            raise ValidationError(f"role {name} must be a nonempty physical packet")
        if any(not isinstance(g, str) or not g for g in packet):
            raise ValidationError("physical-good identifiers must be nonempty strings")
        goods.extend(packet)
    if len(set(goods)) != len(goods):
        raise ValidationError("physical roles overlap or repeat a good")
    values = data.get("values")
    if not isinstance(values, dict) or set(values) != set(OWNERS):
        raise ValidationError("values must specify exactly four observers")
    parsed = {}
    for owner in OWNERS:
        row = values[owner]
        if not isinstance(row, dict) or set(row) != set(goods):
            raise ValidationError(f"observer {owner} must value exactly the physical goods")
        parsed[owner] = {g: rational(row[g]) for g in goods}
    return {name: tuple(roles[name]) for name in ROLES}, parsed


def efx_violations(values, state):
    """Every failed physical deletion inequality, in deterministic order."""
    failures = []
    for observer in OWNERS:
        own = total(values[observer], state[observer])
        for target in OWNERS:
            if target == observer:
                continue
            for deleted in state[target]:
                residual = total(values[observer], (g for g in state[target] if g != deleted))
                if residual > own:
                    failures.append({"observer": observer, "target": target,
                                     "deleted_good": deleted, "own": str(own),
                                     "residual": str(residual)})
    return failures


def signed_transfers(roles, values):
    """Reconstruct all changes, including goods both entering and leaving pool."""
    before, after = expand(BASE, roles), expand(SUPPORT, roles)
    sources = {role: holder for holder in HOLDERS for role in BASE[holder]}
    targets = {role: holder for holder in HOLDERS for role in SUPPORT[holder]}
    moves = [{"role": role, "from": sources[role], "to": targets[role],
              "physical_goods": list(roles[role])}
             for role in ROLES if sources[role] != targets[role]]
    signed = {observer: {holder: Fraction(0) for holder in HOLDERS} for observer in OWNERS}
    for move in moves:
        for observer in OWNERS:
            amount = total(values[observer], move["physical_goods"])
            signed[observer][move["from"]] -= amount
            signed[observer][move["to"]] += amount
    for observer in OWNERS:
        for holder in HOLDERS:
            expected = total(values[observer], after[holder]) - total(values[observer], before[holder])
            if signed[observer][holder] != expected:
                raise ValidationError("signed-transfer reconstruction disagrees with physical endpoints")
        if sum(signed[observer].values()) != 0:
            raise ValidationError("signed-transfer reconstruction lost physical value")
    return {"moves": moves, "delta_by_observer_and_holder": {
        observer: {holder: str(signed[observer][holder]) for holder in HOLDERS}
        for observer in OWNERS}, "all_goods_conserved": True}


def verify_profile(data, *, require_root_wall=False):
    roles, values = parse_profile(data)
    base, support = expand(BASE, roles), expand(SUPPORT, roles)
    for observer in OWNERS:
        if total(values[observer], base[observer]) != 1:
            raise ValidationError(f"base own utility for {observer} is not normalized to 1")
        if total(values[observer], base["pool"]) > 1:
            raise ValidationError(f"base pool is unsafe for {observer}")
    failures = efx_violations(values, base)
    if failures:
        raise ValidationError("base is not physical EFX: " + json.dumps(failures[0], sort_keys=True))
    certificates = []
    holder_of = {role: holder for holder in HOLDERS for role in BASE[holder]}
    for observer in OWNERS:
        row = values[observer]
        for role in ROLES:
            holder, packet = holder_of[role], roles[role]
            complement = tuple(g for g in base[holder] if g not in packet)
            if not complement:
                raise ValidationError("literal role must be a proper subset of its base holder")
            value = total(row, packet)
            certificate = {"observer": observer, "role": role, "base_holder": holder,
                           "value": str(value), "upper_bound": "1",
                           "strict_for_this_profile": value < 1}
            if holder == observer:
                method, bound_goods = "own_proper_subset", base[holder]
            elif holder == "pool":
                method, bound_goods = "safe_pool_proper_subset", base["pool"]
            else:
                method = "foreign_physical_deletion"
                deleted = complement[0]
                bound_goods = tuple(g for g in base[holder] if g != deleted)
                certificate["deleted_good"] = deleted
            bound = total(row, bound_goods)
            if not value <= bound <= 1:
                raise ValidationError("role upper-bound certificate failed")
            certificate.update(method=method, dominating_physical_goods=list(bound_goods),
                               dominating_value=str(bound))
            certificates.append(certificate)
    a_goods = (*roles["a0"], *roles["a1"])
    wall_left, wall_right = total(values["d"], support["d"]), tail(values["d"], a_goods)
    wall_holds = wall_left < wall_right
    wall = {"holds": wall_holds, "d_value_W": str(wall_left), "d_physical_tail_A": str(wall_right)}
    if require_root_wall and not wall_holds:
        raise ValidationError("required physical root-facing wall does not hold")
    support_failures = efx_violations(values, support)
    if wall_holds:
        deleted = min(support["r"], key=lambda g: (values["d"][g], g))
        residual = total(values["d"], (g for g in support["r"] if g != deleted))
        if not wall_left < wall_right <= residual:
            raise ValidationError("root-wall implication failed")
        wall["specific_efx_violation"] = {"observer": "d", "target": "r", "deleted_good": deleted,
                                           "own": str(wall_left), "residual": str(residual)}
    return {"schema": SCHEMA, "valid": True, "physical_good_count": sum(map(len, roles.values())),
            "base_physical_efx": True, "base_pool_safe": True,
            "base_pool_cardinality": len(base["pool"]), "base_outside_at_most_one_pool_class": True,
            "support_pool_cardinality": len(support["pool"]),
            "support_physical_efx": not support_failures, "root_wall": wall,
            "role_upper_bound_certificates": certificates, "signed_transfers": signed_transfers(roles, values),
            "boundary": {"universal_A1_admission_proved": False,
                         "global_selector_or_reachability_verified": False,
                         "bundle_nondegeneracy_required_for_weak_role_bound": False,
                         "strict_role_bound_requires_nondegeneracy_or_direct_numeric_check": True,
                         "profile_scope": "literal physical BASE constraints; no other master premises inferred"}}


def base_calibration():
    """An exact base-only fixture with the root wall; not a saturated master."""
    values = {}
    scale = 1 << 13
    for owner in OWNERS:
        coarse = {role: (100 if role in BASE[owner] else 10) for role in ROLES}
        if owner == "d":
            coarse.update(a0=800, a1=800, h=500, k=490, gq=10, m=50, q0=50,
                          gr=20, j=100, l=100, e=100, p=100)
        raw = {role: scale * coarse[role] + (1 << index) for index, role in enumerate(ROLES)}
        own = sum(raw[role] for role in BASE[owner])
        values[owner] = {role: str(Fraction(raw[role], own)) for role in ROLES}
    return {"schema": SCHEMA, "roles": {role: [role] for role in ROLES}, "values": values}


def singleton_calibration():
    """A global-selector normalization counterexample, not an EFX counterexample."""
    raw = (27, 9, 3, 1)
    values = {owner: {str(g): Fraction(raw[g], raw[i]) for g in range(4)}
              for i, owner in enumerate(OWNERS)}
    count, maxima, best = 0, [], None
    for assignment in itertools.product(range(5), repeat=4):
        state = {holder: tuple(str(g) for g in range(4) if assignment[g] == i)
                 for i, holder in enumerate(HOLDERS)}
        if efx_violations(values, state):
            continue
        count += 1
        objective = tuple(total(values[owner], state[owner]) for owner in OWNERS)
        if best is None or objective > best:
            best, maxima = objective, [assignment]
        elif objective == best:
            maxima.append(assignment)
    if count != 209 or maxima != [(0, 1, 2, 3)] or values["s"]["0"] != 27:
        raise ValidationError("global singleton-bound calibration failed")
    return {"all_partial_allocations_checked": 5 ** 4, "partial_efx_count": count,
            "unique_global_lex_maximum": list(maxima[0]), "normalized_cross_singleton_value": "27",
            "violates_generic_less_than_16": True, "winner_is_complete_efx": True,
            "not_a_no_complete_efx_or_global_admission_counterexample": True}


def verify_archive(path):
    records = read_exact_json(path)
    if not isinstance(records, dict) or set(records) != {"g4_b3", "g4_b5"}:
        raise ValidationError("archive must contain exactly the two declared calibration records")
    reports = {}
    for name in sorted(records):
        flat = records[name]["valuation"]
        if set(flat) != {f"{role}:{owner}" for role in ROLES for owner in OWNERS}:
            raise ValidationError("archived valuation must contain exactly 48 role-observer entries")
        profile = {"schema": SCHEMA, "roles": {role: [role] for role in ROLES},
                   "values": {owner: {role: flat[f"{role}:{owner}"] for role in ROLES} for owner in OWNERS}}
        reports[name] = verify_profile(profile, require_root_wall=True)
    return {"records": reports,
            "boundary": "Replays base EFX, safe charity, role bounds, root wall and signed transfers only; "
                        "does not replay other master premises or prior SAT/UNSAT verdicts."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--profile", type=Path, help="JSON physical-role profile")
    source.add_argument("--archive", type=Path, help="the two-record archived atom calibration")
    parser.add_argument("--require-root-wall", action="store_true")
    args = parser.parse_args(argv)
    if args.archive:
        report = verify_archive(args.archive)
    else:
        data = read_exact_json(args.profile) if args.profile else base_calibration()
        report = verify_profile(data, require_root_wall=args.require_root_wall)
    report["singleton_bound_calibration"] = singleton_calibration()
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
