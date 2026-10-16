#!/usr/bin/env python3
"""Independently check concrete four-agent selector exit/repair certificates.

Only the standard library is used. All arithmetic is Fraction arithmetic on
positive rational strings or integers; JSON floats and booleans are rejected.
The owner vector has one entry per ORIGINAL good, so every good occurs exactly
once, either with an agent or in charity (null).

This is an endpoint checker, not a constructive implementation or independent
proof of BCFF Theorem 5.1. The existence of a suitable BCFF successor is an
external-trusted mathematical input; a supplied successor is checked directly.
Bundle nondegeneracy is decided by exhaustive subset sums, not a heuristic.
Consequently this verifier is intended for small explicit certificates.
The default 16-good computational guard can be explicitly raised by the caller;
it is a resource limit, not a mathematical restriction on the repair theorem.
"""

import argparse
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import sys


INPUT_SCHEMA = "selector-exit-trace-v1"
OUTPUT_SCHEMA = "selector-exit-trace-verification-v1"
AGENTS = range(4)
DEFAULT_MAX_GOODS = 16


class TraceValidationError(ValueError):
    """Invalid certificate; report retains any independently checked scope facts."""

    def __init__(self, message, report=None):
        super().__init__(message)
        self.report = report


def _require(condition, message):
    if not condition:
        raise TraceValidationError(message)


def _fields(value, required, optional, label):
    _require(isinstance(value, dict), f"{label} must be an object")
    _require(required <= value.keys(), f"{label} is missing required fields")
    _require(value.keys() <= required | optional, f"{label} contains unsupported fields")


def _goods_bound(m, max_goods):
    _require(type(max_goods) is int and max_goods > 0, "max_goods must be a positive integer")
    _require(m <= max_goods,
             f"{m} goods exceed max_goods={max_goods}; explicitly raise the limit to permit exponential subset checks")


def _values(raw):
    _require(isinstance(raw, list) and len(raw) == 4, "values must have exactly four rows")
    _require(all(isinstance(row, list) for row in raw), "values rows must be lists")
    m = len(raw[0])
    _require(all(len(row) == m for row in raw), "values rows must have equal length")
    parsed = []
    for i, row in enumerate(raw):
        result = []
        for g, value in enumerate(row):
            _require(type(value) in (int, str), f"values[{i}][{g}] must be an exact rational string or integer")
            try:
                rational = Fraction(value)
            except (ValueError, ZeroDivisionError) as exc:
                raise TraceValidationError(f"values[{i}][{g}] is not a rational") from exc
            _require(rational > 0, f"values[{i}][{g}] must be strictly positive")
            result.append(rational)
        parsed.append(tuple(result))
    return tuple(parsed)


def _owners(raw, m, label):
    _require(isinstance(raw, list) and len(raw) == m, f"{label} must contain exactly one owner per original good")
    _require(all(owner is None or (type(owner) is int and owner in AGENTS) for owner in raw),
             f"{label} owners must be integers 0..3 or null")
    return tuple(raw)


def _priority(raw):
    _require(isinstance(raw, list) and len(raw) == 4
             and all(type(i) is int for i in raw) and set(raw) == set(AGENTS),
             "priority must be a permutation of agents 0..3")
    return tuple(raw)


def _nondegeneracy(values):
    rows = []
    for i, row in enumerate(values):
        sums = {Fraction(0): ()}
        collision = None
        for good, value in enumerate(row):
            additions = {}
            for total, subset in sums.items():
                next_total, next_subset = total + value, subset + (good,)
                if next_total in sums:
                    collision = {"subset_a": list(sums[next_total]),
                                 "subset_b": list(next_subset), "value": str(next_total)}
                    break
                additions[next_total] = next_subset
            if collision is not None:
                break
            sums.update(additions)
        rows.append({"agent": i, "bundle_nondegenerate": collision is None,
                     "collision": collision})
    return {"all_agents": all(row["bundle_nondegenerate"] for row in rows),
            "method": "exact exhaustive subset sums", "agents": rows}


def _state(values, owner):
    bundles = tuple(tuple(g for g, holder in enumerate(owner) if holder == i) for i in AGENTS)
    pool = tuple(g for g, holder in enumerate(owner) if holder is None)
    own = tuple(sum((values[i][g] for g in bundles[i]), Fraction(0)) for i in AGENTS)
    safe = all(own[i] >= sum((values[i][g] for g in pool), Fraction(0)) for i in AGENTS)
    efx = all(own[i] >= sum((values[i][g] for g in bundles[j] if g != deleted), Fraction(0))
              for i in AGENTS for j in AGENTS for deleted in bundles[j])
    return {"owner": owner, "bundles": bundles, "pool": pool, "own": own,
            "efx": efx, "safe": safe, "in_S": efx and safe and len(pool) <= 1}


def _key(state, priority):
    return tuple(state["own"][i] for i in priority)


def _record(state, priority):
    return {"owner": list(state["owner"]), "bundles": [list(bundle) for bundle in state["bundles"]],
            "charity": list(state["pool"]), "own_utilities": [str(value) for value in state["own"]],
            "priority_utilities": [str(value) for value in _key(state, priority)],
            "is_efx": state["efx"], "charity_safe": state["safe"],
            "in_restricted_class": state["in_S"], "complete": not state["pool"]}


def _pool_replacement(values, before, after, metadata):
    """Check the pool lemma itself; the caller separately enforces rule priority."""
    _require(before["efx"], "pool replacement predecessor must be EFX")
    changed = [i for i in AGENTS if before["bundles"][i] != after["bundles"][i]]
    _require(len(changed) == 1, "pool replacement must change exactly one recipient bundle")
    recipient = changed[0]
    if "recipient" in metadata:
        _require(type(metadata["recipient"]) is int and metadata["recipient"] in AGENTS,
                 "pool replacement recipient must be an integer 0..3")
        _require(metadata["recipient"] == recipient, "pool replacement recipient disagrees with owner vectors")
    desired = after["bundles"][recipient]
    if "desired_goods" in metadata:
        goods = metadata["desired_goods"]
        _require(isinstance(goods, list) and all(type(g) is int and 0 <= g < len(values[0]) for g in goods),
                 "desired_goods must list original-good integer indices")
        _require(len(set(goods)) == len(goods), "desired_goods contains duplicate goods")
        _require(tuple(sorted(goods)) == desired, "desired_goods disagrees with the replacement bundle")
    _require(bool(desired) and set(desired) <= set(before["pool"]),
             "replacement bundle must be a nonempty subset of predecessor charity")
    expected = list(before["owner"])
    for good in before["bundles"][recipient]:
        expected[good] = None
    for good in desired:
        expected[good] = recipient
    _require(tuple(expected) == after["owner"], "pool replacement must release the old bundle and preserve all other owners")
    _require(after["own"][recipient] > before["own"][recipient], "pool replacement recipient must strictly improve")
    for size in range(len(desired)):
        for subset in combinations(before["pool"], size):
            _require(not any(sum((values[i][g] for g in subset), Fraction(0)) > before["own"][i]
                             for i in AGENTS),
                     "replacement is not minimum-cardinality among charity subsets envied by any agent")
    _require(after["efx"], "pool replacement successor must be EFX")
    return {"recipient": recipient, "desired_goods": list(desired),
            "minimum_cardinality_over_all_agents": len(desired)}


def check_pool_replacement(values, before_owner, after_owner, *, recipient=None, desired_goods=None,
                           max_goods=DEFAULT_MAX_GOODS):
    """Check the pool lemma in isolation, allowing ties but not zero/negative values.

    This does not certify a repair trace: it intentionally imposes neither the
    at-most-one-charity rule priority nor BCFF's nondegeneracy hypothesis.
    """
    parsed = _values(values)
    m = len(parsed[0])
    _goods_bound(m, max_goods)
    before = _state(parsed, _owners(before_owner, m, "before_owner"))
    after = _state(parsed, _owners(after_owner, m, "after_owner"))
    metadata = {}
    if recipient is not None:
        metadata["recipient"] = recipient
    if desired_goods is not None:
        metadata["desired_goods"] = desired_goods
    return _pool_replacement(parsed, before, after, metadata)


def verify_trace(document, *, require_nondegenerate=True, max_goods=DEFAULT_MAX_GOODS):
    """Return a deterministic acceptance report or raise TraceValidationError.

    Setting require_nondegenerate=False permits only direct endpoint/pool-lemma
    calibration outside the frozen scope. Degenerate BCFF steps are ALWAYS
    rejected. All priorities are read from one immutable top-level permutation.
    """
    report = {"schema": OUTPUT_SCHEMA, "valid": False}
    try:
        _require(type(require_nondegenerate) is bool, "require_nondegenerate must be boolean")
        required = {"schema", "values", "priority", "base_owner", "exit_owner", "repair_steps", "outcome"}
        _fields(document, required, set(), "certificate")
        _require(document["schema"] == INPUT_SCHEMA, f"schema must be {INPUT_SCHEMA}")
        values, priority = _values(document["values"]), _priority(document["priority"])
        m = len(values[0])
        _goods_bound(m, max_goods)
        base_owner = _owners(document["base_owner"], m, "base_owner")
        exit_owner = _owners(document["exit_owner"], m, "exit_owner")
        steps = document["repair_steps"]
        _require(isinstance(steps, list), "repair_steps must be a list")
        _require(document["outcome"] in ("complete", "restricted_improvement"), "unsupported outcome")
        parsed_steps = []
        for index, step in enumerate(steps):
            label = f"repair_steps[{index}]"
            _fields(step, {"rule", "owner"}, {"recipient", "desired_goods"}, label)
            _require(step["rule"] in ("bcff_progress", "pool_replacement"), f"{label} has unsupported rule")
            if step["rule"] == "bcff_progress":
                _require(step.keys() == {"rule", "owner"}, f"{label}: recipient/desired_goods apply only to pool replacement")
            parsed_steps.append((step, _owners(step["owner"], m, f"{label}.owner")))
        degeneracy = _nondegeneracy(values)
        report.update({"input_schema": INPUT_SCHEMA, "agent_count": 4, "good_count": m,
                       "max_goods": max_goods,
                       "priority": list(priority), "arithmetic": "fractions.Fraction",
                       "bundle_nondegeneracy": degeneracy,
                       "within_frozen_scope": degeneracy["all_agents"],
                       "nondegeneracy_required": require_nondegenerate,
                       "trust_boundary": {
                           "checked": "concrete original-good endpoints, EFX, fixed-priority signs, and pool replacements",
                           "external_trusted": "BCFF Theorem 5.1 successor existence; not independently proved or constructively implemented",
                           "universal_theorem_proved_by_this_check": False}})
        _require(not require_nondegenerate or degeneracy["all_agents"],
                 "frozen scope requires bundle-nondegenerate valuations for every agent")
        base, exit_state = _state(values, base_owner), _state(values, exit_owner)
        report.update({"base": _record(base, priority), "exit": _record(exit_state, priority)})
        _require(base["in_S"], "base must be EFX, charity-safe, and have at most one unallocated good")
        _require(exit_state["efx"], "exit must be EFX, even when complete")
        original_complete = not exit_state["pool"]
        if original_complete:
            _require(not parsed_steps, "complete EFX exits require an empty repair trace")
        else:
            _require(_key(exit_state, priority) > _key(base, priority),
                     "partial exit must strictly improve the fixed-priority utility tuple over base")
        current, verified_steps = exit_state, []
        for index, (step, owner) in enumerate(parsed_steps):
            _require(not current["in_S"], f"repair_steps[{index}]: trace must stop at the first state in S")
            successor = _state(values, owner)
            detail = {"index": index, "rule": step["rule"]}
            if step["rule"] == "bcff_progress":
                _require(degeneracy["all_agents"], "BCFF progress requires bundle-nondegenerate valuations, including in relaxed mode")
                _require(len(current["pool"]) >= 2, "BCFF progress requires at least two unallocated goods")
            else:
                _require(len(current["pool"]) <= 1 and not current["safe"],
                         "pool replacement requires unsafe charity of size at most one; BCFF has rule priority")
                detail.update(_pool_replacement(values, current, successor, step))
            _require(successor["efx"], f"repair_steps[{index}]: successor must be EFX")
            _require(_key(successor, priority) > _key(current, priority),
                     f"repair_steps[{index}]: successor must strictly improve the same fixed-priority tuple")
            detail["endpoint"] = _record(successor, priority)
            verified_steps.append(detail)
            current = successor
        _require(current["in_S"], "repair trace must end in S; an out-of-class exit cannot have an empty or unfinished trace")
        _require(original_complete or _key(current, priority) > _key(base, priority),
                 "repaired endpoint must strictly improve base")
        expected_outcome = "complete" if not current["pool"] else "restricted_improvement"
        _require(document["outcome"] == expected_outcome, f"outcome must be {expected_outcome} for the final endpoint")
        report.update({"valid": True, "outcome": expected_outcome,
                       "original_exit_complete": original_complete, "repair_step_count": len(verified_steps),
                       "repair_steps": verified_steps, "final": _record(current, priority)})
        return report
    except TraceValidationError as exc:
        report["error"] = str(exc)
        exc.report = report
        raise


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_number(value):
    raise TraceValidationError(f"JSON noninteger numeric token {value!r} is forbidden; use an exact rational string")


def load_document(path):
    with Path(path).open(encoding="utf-8") as source:
        return json.load(source, object_pairs_hook=_unique_object,
                         parse_float=_reject_number, parse_constant=_reject_number)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="selector-exit-trace-v1 JSON certificate")
    parser.add_argument("--output", type=Path, help="also save a successful deterministic JSON report")
    parser.add_argument("--max-goods", type=int, default=DEFAULT_MAX_GOODS,
                        help="explicit size limit before exponential subset checks (default: 16)")
    parser.add_argument("--allow-degenerate-pool-only", action="store_true",
                        help="calibration outside frozen scope; still rejects every degenerate BCFF step")
    args = parser.parse_args(argv)
    try:
        _require(args.output is None or args.output.resolve() != args.input.resolve(),
                 "output must not overwrite the input certificate")
        report = verify_trace(load_document(args.input), require_nondegenerate=not args.allow_degenerate_pool_only,
                              max_goods=args.max_goods)
        output = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if args.output is not None:
            args.output.write_text(output, encoding="utf-8")
    except (ValueError, OSError) as exc:
        report = getattr(exc, "report", None) or {"schema": OUTPUT_SCHEMA, "valid": False, "error": str(exc)}
        print(json.dumps(report, indent=2, sort_keys=True))
        return 2
    print(output, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
