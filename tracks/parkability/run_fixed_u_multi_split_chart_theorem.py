#!/usr/bin/env python3
"""Chart-level CEGAR whose oracle matches Theorem 1's hypothesis.

`run_fixed_u_tame_menu_chart_theorem.py` reported an obstruction that did not
exist: its oracle tried a whole-role allocation and then at most *one* tame
split, while the profile it flagged is closed by a menu splitting three tame
roles at once.  The move family was narrower than the theorem being tested.

This driver removes that gap.  A certificate here fixes a *set* `S` of tame
split roles and supplies one allocation for **every** side-pattern vector of
`S`, the full product of `8^|S|` vectors -- `8` per role after the
good-relabelling quotient pins `s[g,r] = 0`.  Branch W is the case `S` empty,
so whole-role and split certificates are one uniform object.

Soundness rests on the full product and nothing less.  Covering only the
patterns a search happened to visit would leave a realization unaccounted for
and make the emitted cut unsound, so `audit_pattern_coverage` recomputes the
expected key set from `S` and refuses any certificate that does not carry every
one.  Every certificate passes that audit *and* an exact rational re-audit of
each allocation before its cut is added; `test_fixed_u_multi_split_chart.py`
deliberately narrows a certificate to the visited patterns and asserts the
audit rejects it, so the instrument cannot repeat that class of defect quietly.

Given the cut algebra `Not(OR_c closes(c)) == AND_c Not(closes(c))`, a
terminating `unsat` is the chart theorem: every fixed-`U`-admissible profile
admits a tame covering menu, hence by Theorem 1 a complete EFX allocation
within the edge budget in every physical realization.  A `sat` that survives
this oracle is the genuine failure shape.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
from fractions import Fraction
from pathlib import Path

import z3

from .decide_physical_minimum_countermodel_four_edge import support_supplier
from .run_exact_response_physical_minimum_cegar import build_physical_master, serialize
from .run_identity_aware_one_minimum_split_cegar import (
    HIGH,
    LOW,
    WHOLE,
    role_is_multi,
    role_slack_is_two,
    tame_guard,
)
from .run_identity_aware_witness_side_cegar import (
    audit_allocation,
    concrete_values,
    failure_clause,
    symbolic_values,
)
from .run_realization_free_universality_cegar import (
    audit_no_wild_split,
    classify_roles,
    decide_tame,
)
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE


# --- the side-pattern product ---------------------------------------------

def role_patterns():
    """The eight side patterns of one role, with observer r pinned."""
    others = [o for o in OWNERS if o != "r"]
    return tuple(
        {"r": 0, **dict(zip(others, bits))}
        for bits in itertools.product((0, 1), repeat=len(others))
    )


def side_pattern_vectors(split_roles):
    """Every assignment of a side pattern to each split role: 8^k vectors."""
    split_roles = tuple(split_roles)
    if not split_roles:
        return ({},)
    return tuple(
        dict(zip(split_roles, combo))
        for combo in itertools.product(role_patterns(), repeat=len(split_roles))
    )


def pattern_key(split_roles, vector):
    """A stable name for one pattern vector, used as the certificate key."""
    return "|".join(
        f"{role}:" + "".join(str(vector[role][o]) for o in OWNERS)
        for role in sorted(split_roles)
    )


def expected_pattern_keys(split_roles):
    return {
        pattern_key(split_roles, vector)
        for vector in side_pattern_vectors(split_roles)
    }


# --- pieces and their values ----------------------------------------------

def pieces_for_set(split_roles):
    split_roles = set(split_roles)
    return tuple(
        piece
        for role in GOODS
        for piece in (
            ((role, LOW), (role, HIGH)) if role in split_roles
            else ((role, WHOLE),)
        )
    )


def carries_witness(kind, bit):
    return (bit == 0) if kind == LOW else (bit == 1)


def numeric_value(totals, minima, observer, piece, vector):
    role, kind = piece
    if kind == WHOLE:
        return totals[observer][role]
    if carries_witness(kind, vector[role][observer]):
        return minima[observer][role]
    return totals[observer][role] - minima[observer][role]


def numeric_floor(totals, minima, observer, piece, vector):
    """A whole role of any width offers M; a tame split piece is one good."""
    role, kind = piece
    if kind == WHOLE:
        return minima[observer][role]
    return numeric_value(totals, minima, observer, piece, vector)


def symbolic_value(total, minimum, observer, piece, vector):
    role, kind = piece
    if kind == WHOLE:
        return total[role, observer]
    if carries_witness(kind, vector[role][observer]):
        return minimum[role, observer]
    return total[role, observer] - minimum[role, observer]


def symbolic_floor(total, minimum, observer, piece, vector):
    role, kind = piece
    if kind == WHOLE:
        return minimum[role, observer]
    return symbolic_value(total, minimum, observer, piece, vector)


# --- the concrete oracle ---------------------------------------------------

def numeric_oracle(totals, minima, split_roles, vector, edge_cap):
    pieces = pieces_for_set(split_roles)
    supplier = support_supplier()
    x = {(piece, owner): z3.Bool(f"x_{piece[0]}_{piece[1]}_{owner}")
         for piece in pieces for owner in OWNERS}
    edge = {(source, target): z3.Bool(f"e_{source}_{target}")
            for source in SUPPORT_STATE for target in OWNERS if source != target}
    solver = z3.Solver()
    for piece in pieces:
        solver.add(z3.PbEq([(x[piece, owner], 1) for owner in OWNERS], 1))
        source = supplier[piece[0]]
        for target in OWNERS:
            if target != source:
                solver.add(z3.Implies(x[piece, target], edge[source, target]))
    solver.add(z3.PbLe([(flag, 1) for flag in edge.values()], edge_cap))

    def rv(value):
        return z3.RealVal(f"{value.numerator}/{value.denominator}")

    utility = {
        (observer, target): z3.Sum(*(
            z3.If(x[piece, target],
                  rv(numeric_value(totals, minima, observer, piece, vector)),
                  z3.RealVal(0))
            for piece in pieces
        ))
        for observer in OWNERS for target in OWNERS
    }
    for observer in OWNERS:
        for target in OWNERS:
            if target == observer:
                continue
            for piece in pieces:
                solver.add(z3.Implies(
                    x[piece, target],
                    utility[observer, observer] >= utility[observer, target]
                    - rv(numeric_floor(totals, minima, observer, piece, vector)),
                ))
    if solver.check() != z3.sat:
        return None
    model = solver.model()
    return {
        owner: [list(p) for p in pieces if z3.is_true(model.eval(x[p, owner]))]
        for owner in OWNERS
    }


def exact_audit(allocation, totals, minima, split_roles, vector, edge_cap):
    """Completeness, the edge budget and EFX, re-checked outside z3."""
    placed = [tuple(p) for pieces in allocation.values() for p in pieces]
    assert sorted(placed) == sorted(pieces_for_set(split_roles)), placed
    supplier = support_supplier()
    edges = sorted({
        (supplier[role], owner)
        for owner, pieces in allocation.items()
        for role, _ in pieces
        if supplier[role] != owner
    })
    assert len(edges) <= edge_cap, edges
    for observer in OWNERS:
        own = sum(
            (numeric_value(totals, minima, observer, tuple(p), vector)
             for p in allocation[observer]),
            Fraction(),
        )
        for target in OWNERS:
            if target == observer:
                continue
            gross = sum(
                (numeric_value(totals, minima, observer, tuple(p), vector)
                 for p in allocation[target]),
                Fraction(),
            )
            for piece in allocation[target]:
                floor = numeric_floor(
                    totals, minima, observer, tuple(piece), vector
                )
                assert own >= gross - floor, (observer, target, piece)
    return edges


# --- the soundness audit ---------------------------------------------------

class PatternCoverageError(AssertionError):
    """A certificate does not carry every side-pattern vector of its split set."""


def audit_pattern_coverage(certificate):
    """Refuse any certificate that misses a single pattern vector.

    This is the guard against the defect that produced the superseded
    obstruction: a cut justified only on the patterns a search visited is
    unsound, because an unvisited pattern is a realization the certificate
    never covered.  The expected key set is recomputed from the split set, so
    the certificate cannot vouch for its own coverage.
    """
    split_roles = tuple(certificate["split_roles"])
    expected = expected_pattern_keys(split_roles)
    present = set(certificate["allocations"])
    if present != expected:
        missing = sorted(expected - present)
        extra = sorted(present - expected)
        raise PatternCoverageError(
            f"split set {split_roles} needs {len(expected)} pattern vectors, "
            f"certificate carries {len(present)}; "
            f"missing {missing[:4]}{'...' if len(missing) > 4 else ''}; "
            f"unexpected {extra[:4]}{'...' if len(extra) > 4 else ''}"
        )
    assert len(expected) == 8 ** len(split_roles), (
        len(expected), len(split_roles)
    )
    return len(expected)


def audit_split_set_is_tame(totals, minima, split_roles):
    for role in split_roles:
        assert role_is_multi(totals, minima, role), role
        assert role_slack_is_two(totals, minima, role), role


def deserialize_rows(rows):
    """Inverse of `serialize`, with observers outermost in stored records."""
    return {
        observer: {role: Fraction(amount) for role, amount in row.items()}
        for observer, row in rows.items()
    }


# --- certificates ----------------------------------------------------------

def build_certificate(totals, minima, split_roles, edge_cap):
    """One allocation per pattern vector, or None if any vector is unmet."""
    split_roles = tuple(sorted(split_roles))
    audit_split_set_is_tame(totals, minima, split_roles)
    allocations = {}
    for vector in side_pattern_vectors(split_roles):
        found = numeric_oracle(totals, minima, split_roles, vector, edge_cap)
        if found is None:
            return None
        exact_audit(found, totals, minima, split_roles, vector, edge_cap)
        allocations[pattern_key(split_roles, vector)] = found
    certificate = {
        "branch": "W" if not split_roles else "M",
        "split_roles": list(split_roles),
        "allocations": allocations,
    }
    certificate["pattern_count"] = audit_pattern_coverage(certificate)
    return certificate


def certificate_cut(certificate, total, minimum):
    """The symbolic condition under which this certificate closes a profile."""
    split_roles = tuple(certificate["split_roles"])
    clauses = [tame_guard(total, minimum, role) for role in split_roles]
    for vector in side_pattern_vectors(split_roles):
        allocation = certificate["allocations"][pattern_key(split_roles, vector)]
        bundles = {o: [tuple(p) for p in allocation[o]] for o in OWNERS}
        utility = {
            (observer, target): z3.Sum(*(
                symbolic_value(total, minimum, observer, piece, vector)
                for piece in bundles[target]
            )) if bundles[target] else z3.RealVal(0)
            for observer in OWNERS for target in OWNERS
        }
        for observer in OWNERS:
            for target in OWNERS:
                if target == observer:
                    continue
                for piece in bundles[target]:
                    clauses.append(
                        utility[observer, observer] >= utility[observer, target]
                        - symbolic_floor(total, minimum, observer, piece, vector)
                    )
    return z3.And(*clauses)


def audit_certificate_at_profile(certificate, totals, minima, edge_cap):
    """Replay every allocation in a certificate against its source profile."""
    split_roles = tuple(certificate["split_roles"])
    audit_pattern_coverage(certificate)
    audit_split_set_is_tame(totals, minima, split_roles)
    for vector in side_pattern_vectors(split_roles):
        allocation = certificate["allocations"][
            pattern_key(split_roles, vector)
        ]
        exact_audit(
            allocation, totals, minima, split_roles, vector, edge_cap
        )


# --- durable cut ledger ---------------------------------------------------

def atomic_json_write(path, payload):
    """Replace a JSON summary atomically so interruption cannot truncate it."""
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def load_cut_ledger(path):
    """Load complete JSONL records; a torn final line is a hard failure."""
    if path is None or not path.exists():
        return []
    records = []
    with path.open() as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"torn cut-ledger line {line_number} in {path}"
                ) from error
    return records


def append_cut_record(path, record):
    """Durably append a certificate before advancing the JSON summary."""
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
    with path.open("a") as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())


def cut_record(round_record, certificate):
    payload = {
        "schema": "fixed-u-multi-split-cut-v1",
        "iteration": round_record["iteration"],
        "round": round_record,
        "certificate": certificate,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["payload_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return payload


def audit_cut_record(record, edge_cap):
    payload = {k: v for k, v in record.items() if k != "payload_sha256"}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    assert record["payload_sha256"] == hashlib.sha256(canonical.encode()).hexdigest()
    assert record["schema"] == "fixed-u-multi-split-cut-v1"
    assert record["iteration"] == record["round"]["iteration"]
    totals = deserialize_rows(record["round"]["totals"])
    minima = deserialize_rows(record["round"]["minima"])
    certificate = record["certificate"]
    assert certificate["split_roles"] == record["round"]["split_roles"]
    assert certificate["branch"] == record["round"]["branch"]
    assert certificate["pattern_count"] == record["round"]["pattern_count"]
    audit_certificate_at_profile(certificate, totals, minima, edge_cap)
    return certificate


def wide_menu_split_union(totals, minima, edge_cap, timeout_seconds,
                          maximum_rounds=60):
    """Run the realization-free CEGAR, returning its status and split union.

    `solve_profile` reports only the baseline's split roles, which is a strict
    understatement: later menu allocations routinely split other tame roles.
    Proposing from the baseline alone made this driver give up on a profile
    whose closing menu was well inside its budget, so the union over *every*
    accepted allocation is what gets returned here.
    """
    role_goods, multi, tame, wild = classify_roles(totals, minima)
    side = {
        (role, observer): z3.Bool(f"u_side_{role}_{observer}")
        for role in multi for observer in OWNERS
    }
    master = z3.Solver()
    master.add(*(z3.Not(side[role, "r"]) for role in multi))
    master.add(*(z3.Not(side[role, observer])
                 for role in wild for observer in OWNERS))
    symbolic = symbolic_values(totals, minima, role_goods, side)

    union = set()

    def absorb(allocation, physical):
        audit_allocation(allocation, physical, edge_cap)
        audit_no_wild_split(allocation, wild, role_goods)
        for role in multi:
            holders = {
                owner for owner, goods in allocation.items()
                if set(goods) & set(role_goods[role])
            }
            if len(holders) > 1:
                union.add(role)
        master.add(failure_clause(allocation, symbolic))

    canonical = {(role, o): False for role in multi for o in OWNERS}
    physical = concrete_values(totals, minima, role_goods, canonical)
    status, found, _ = decide_tame(
        physical, role_goods, wild, edge_cap, timeout_seconds
    )
    if found is None:
        return (
            "UNSAT_NO_TAME_SPLIT_ALLOCATION" if status == "unsat" else "UNKNOWN",
            (),
        )
    absorb(found[0], physical)

    for _ in range(maximum_rounds):
        outcome = master.check()
        if outcome == z3.unsat:
            return (
                "UNSAT_EVERY_REALIZATION_ADMITS_A_BANKED_ALLOCATION",
                tuple(sorted(union & set(tame))),
            )
        if outcome == z3.unknown:
            return "UNKNOWN", ()
        model = master.model()
        sides = {k: z3.is_true(model.eval(f)) for k, f in side.items()}
        physical = concrete_values(totals, minima, role_goods, sides)
        status, found, _ = decide_tame(
            physical, role_goods, wild, edge_cap, timeout_seconds
        )
        if found is None:
            return (
                "UNSAT_NO_TAME_SPLIT_ALLOCATION" if status == "unsat"
                else "UNKNOWN",
                (),
            )
        absorb(found[0], physical)
    return "ROUND_LIMIT", ()


CLOSED = "closed"
CAP_BOUND = "cap_bound"
WIDE_FAMILY_FAILED = "wide_family_failed"
WIDE_FAMILY_INCONCLUSIVE = "wide_family_inconclusive"

# Only a genuine failure of the widest available family may be reported as an
# obstruction.  A limit of this instrument -- an exhausted pattern budget, or an
# inconclusive wide-family run -- halts the search under its own name and never
# borrows the language of a countermodel.
HALT_VERDICT = {
    WIDE_FAMILY_FAILED: "SAT_NO_TAME_COVERING_MENU_FOR_THIS_PROFILE",
    CAP_BOUND: "HALTED_PATTERN_BUDGET_BOUND_NOT_AN_OBSTRUCTION",
    WIDE_FAMILY_INCONCLUSIVE: "HALTED_WIDE_FAMILY_INCONCLUSIVE",
}

OBSTRUCTION_STATUSES = frozenset({WIDE_FAMILY_FAILED})


MASTER_MODES = ("qflra", "smt")


def select_master_solver(source, mode, timeout_seconds, random_seed):
    """Preserve the master assertions while changing only Z3's front end."""
    if mode == "qflra":
        solver = source
    elif mode == "smt":
        solver = z3.Solver()
        solver.add(*source.assertions())
    else:
        raise ValueError(mode)
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    return solver


def close_profile(totals, minima, edge_cap, pattern_budget, timeout_seconds):
    """Close a profile, or say precisely why this oracle could not.

    Returns `(status, certificate, detail)`.  Only `WIDE_FAMILY_FAILED` is an
    obstruction, and it is reported only when the realization-free CEGAR --
    which allows arbitrarily many tame splits and is the widest family
    available -- itself reports that no tame menu exists.

    The other two negative statuses exist because this driver has already
    produced two verdicts that were artifacts of its own search limits.  If the
    wide CEGAR closes the profile but its closing menu needs a split set whose
    pattern product `8^k` exceeds the budget, that is `CAP_BOUND`: a limit of
    this instrument, not a fact about the profile, and it must never be dressed
    up as an obstruction.  If the wide CEGAR returns unknown or hits its round
    limit, that is `WIDE_FAMILY_INCONCLUSIVE` for the same reason.
    """
    certificate = build_certificate(totals, minima, (), edge_cap)
    if certificate is not None:
        return CLOSED, certificate, {"split_roles": []}

    status, proposed = wide_menu_split_union(
        totals, minima, edge_cap, timeout_seconds
    )
    if status == "UNSAT_NO_TAME_SPLIT_ALLOCATION":
        return WIDE_FAMILY_FAILED, None, {"wide_status": status}
    if status != "UNSAT_EVERY_REALIZATION_ADMITS_A_BANKED_ALLOCATION":
        return WIDE_FAMILY_INCONCLUSIVE, None, {"wide_status": status}

    # `proposed` is the union of the split roles over the *whole* covering
    # menu, not the baseline's alone.  With S equal to that union a certificate
    # must exist: every menu allocation splits inside S, and by Lemma C its EFX
    # status depends only on the pattern over the roles it splits, so each
    # vector over S is met by some menu allocation.  Subsets are tried first
    # only to keep the pattern product small.
    # Try subsets in increasing size while the cumulative oracle work stays
    # inside the budget.  A smaller split set is both cheaper to certify and a
    # smaller cut, so this is a search for the cheapest sufficient set, not a
    # shortcut around the full product: whichever set is used, its own product
    # is enumerated in full.
    spent, tried = 0, 0
    for size in range(1, len(proposed) + 1):
        cost = 8 ** size
        for split_roles in itertools.combinations(proposed, size):
            if spent + cost > pattern_budget:
                return CAP_BOUND, None, {
                    "wide_status": status,
                    "proposed_split_roles": list(proposed),
                    "pattern_product_of_full_union": 8 ** len(proposed),
                    "pattern_budget": pattern_budget,
                    "oracle_calls_spent": spent,
                    "subsets_tried": tried,
                    "next_subset_size": size,
                    "next_subset_cost": cost,
                }
            certificate = build_certificate(
                totals, minima, split_roles, edge_cap
            )
            spent += cost
            tried += 1
            if certificate is not None:
                return CLOSED, certificate, {
                    "split_roles": list(split_roles),
                    "oracle_calls_spent": spent,
                    "subsets_tried": tried,
                }
    raise AssertionError(
        "the wide covering menu splits inside "
        f"{proposed}, so a certificate on that set must exist; none was found"
    )


# --- seeding ---------------------------------------------------------------

def whole_role_certificate(role_owner, edge_cap):
    assert sorted(role_owner) == sorted(GOODS), sorted(role_owner)
    supplier = support_supplier()
    edges = sorted({
        (supplier[role], owner)
        for role, owner in role_owner.items()
        if supplier[role] != owner
    })
    assert len(edges) <= edge_cap, (edges, role_owner)
    allocation = {
        owner: [[role, WHOLE] for role in GOODS if role_owner[role] == owner]
        for owner in OWNERS
    }
    certificate = {
        "branch": "W",
        "split_roles": [],
        "allocations": {pattern_key((), {}): allocation},
    }
    certificate["pattern_count"] = audit_pattern_coverage(certificate)
    return certificate


def load_seed_menu(path, edge_cap):
    seen, seeds = set(), []
    for entry in json.loads(path.read_text()):
        key = tuple(sorted(entry.items()))
        if key in seen:
            continue
        seen.add(key)
        seeds.append(whole_role_certificate(entry, edge_cap))
    return seeds


def reconstruct_cut_record(round_record, edge_cap):
    """Rebuild a pre-ledger certificate from its frozen source profile."""
    totals = deserialize_rows(round_record["totals"])
    minima = deserialize_rows(round_record["minima"])
    certificate = build_certificate(
        totals, minima, round_record["split_roles"], edge_cap
    )
    if certificate is None:
        raise AssertionError(
            f"cannot reconstruct iteration {round_record['iteration']}"
        )
    assert certificate["branch"] == round_record["branch"]
    assert certificate["pattern_count"] == round_record["pattern_count"]
    return cut_record(round_record, certificate)


def prepare_cut_records(resume_path, ledger_path, edge_cap):
    """Audit a ledger and recover cuts absent from either crash-side artifact."""
    ledger_records = load_cut_ledger(ledger_path)
    by_iteration = {}
    for record in ledger_records:
        audit_cut_record(record, edge_cap)
        iteration = record["iteration"]
        if iteration in by_iteration:
            raise ValueError(f"duplicate cut-ledger iteration {iteration}")
        by_iteration[iteration] = record

    previous = None
    if resume_path is not None:
        previous = json.loads(resume_path.read_text())
        for round_record in previous["rounds"]:
            iteration = round_record["iteration"]
            if iteration in by_iteration:
                assert by_iteration[iteration]["round"] == round_record
                continue
            record = reconstruct_cut_record(round_record, edge_cap)
            append_cut_record(ledger_path, record)
            by_iteration[iteration] = record
    elif by_iteration:
        raise ValueError("a nonempty cut ledger requires --resume")

    if by_iteration:
        expected = list(range(max(by_iteration) + 1))
        assert sorted(by_iteration) == expected, (
            "cut ledger has an iteration gap", sorted(by_iteration)
        )
    return previous, [by_iteration[i] for i in sorted(by_iteration)]


# --- the chart loop --------------------------------------------------------

def run(output_path, form_index, seed_path, maximum_rounds, timeout_seconds,
        random_seed, edge_cap, pattern_budget, resume_path=None,
        cut_ledger_path=None, master_mode="qflra"):
    source, total, minimum = build_physical_master(form_index)
    solver = select_master_solver(
        source, master_mode, timeout_seconds, random_seed
    )

    seeds = load_seed_menu(seed_path, edge_cap) if seed_path else []
    for certificate in seeds:
        solver.add(z3.Not(certificate_cut(certificate, total, minimum)))

    previous, records = prepare_cut_records(
        resume_path, cut_ledger_path, edge_cap
    )
    if previous is not None:
        assert previous["form_index"] == form_index
        assert previous["edge_cap"] == edge_cap
        assert previous["pattern_budget"] == pattern_budget
        assert previous["seed_certificates"] == len(seeds)
        assert previous["seed_source_sha256"] == (
            hashlib.sha256(seed_path.read_bytes()).hexdigest()
            if seed_path else None
        )
    for record in records:
        solver.add(z3.Not(certificate_cut(
            record["certificate"], total, minimum
        )))

    rounds = [record["round"] for record in records]
    result = {
        "schema": "fixed-u-multi-split-chart-theorem-v2",
        "status": "RUNNING",
        "form_index": form_index,
        "edge_cap": edge_cap,
        "pattern_budget": pattern_budget,
        "master_mode": master_mode,
        "resumed_master_mode": (
            previous.get("master_mode", "legacy_qflra") if previous else None
        ),
        "seed_certificates": len(seeds),
        "seed_source": str(seed_path) if seed_path else None,
        "seed_source_sha256": (
            hashlib.sha256(seed_path.read_bytes()).hexdigest() if seed_path else None
        ),
        "oracle": (
            "one allocation for every side-pattern vector of the split set, "
            "the full 8^k product; every certificate passes "
            "audit_pattern_coverage and an exact rational re-audit of each "
            "allocation before its cut is added"
        ),
        "rounds": rounds,
        "resumed_from": str(resume_path) if resume_path else None,
        "resumed_from_sha256": (
            hashlib.sha256(resume_path.read_bytes()).hexdigest()
            if resume_path else None
        ),
        "cut_ledger": str(cut_ledger_path) if cut_ledger_path else None,
        "cut_ledger_record_count": len(records),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    atomic_json_write(output_path, result)

    for iteration in range(len(rounds), maximum_rounds):
        status = solver.check()
        if status != z3.sat:
            result["status"] = (
                "UNSAT_EVERY_ADMISSIBLE_PROFILE_HAS_A_TAME_COVERING_MENU"
                if status == z3.unsat else "UNKNOWN"
            )
            if status == z3.unknown:
                result["reason_unknown"] = solver.reason_unknown()
            break
        model = solver.model()
        totals = {
            o: {g: Fraction(str(model.eval(total[g, o], model_completion=True)))
                for g in GOODS}
            for o in OWNERS
        }
        minima = {
            o: {g: Fraction(str(model.eval(minimum[g, o], model_completion=True)))
                for g in GOODS}
            for o in OWNERS
        }
        status, certificate, detail = close_profile(
            totals, minima, edge_cap, pattern_budget, timeout_seconds
        )
        if certificate is None:
            _, _, tame, wild = classify_roles(totals, minima)
            result["status"] = HALT_VERDICT[status]
            result["halt_reason"] = status
            result["halt_detail"] = detail
            result["halt_iteration"] = iteration
            result["profile_totals"] = serialize(model, total)
            result["profile_minima"] = serialize(model, minimum)
            result["profile_tame_roles"] = list(tame)
            result["profile_wild_roles"] = list(wild)
            result["profile_role_slacks"] = {
                role: str(min(totals[o][role] // minima[o][role] for o in OWNERS))
                for role in GOODS
            }
            if status in OBSTRUCTION_STATUSES:
                # Only this branch is a claim about the chart rather than about
                # the search, so only this branch names a countermodel.
                result["countermodel_totals"] = result["profile_totals"]
                result["countermodel_minima"] = result["profile_minima"]
                result["countermodel_iteration"] = iteration
                result["countermodel_role_slacks"] = result["profile_role_slacks"]
            break
        round_record = {
            "iteration": iteration,
            "branch": certificate["branch"],
            "split_roles": certificate["split_roles"],
            "pattern_count": certificate["pattern_count"],
            "totals": serialize(model, total),
            "minima": serialize(model, minimum),
        }
        record = cut_record(round_record, certificate)
        audit_cut_record(record, edge_cap)
        # Durability order is intentional: if interrupted after this append but
        # before the summary write, resume treats the ledger as authoritative.
        append_cut_record(cut_ledger_path, record)
        solver.add(z3.Not(certificate_cut(certificate, total, minimum)))
        rounds.append(round_record)
        result["cut_ledger_record_count"] = len(rounds)
        print(iteration, certificate["branch"],
              certificate["split_roles"], certificate["pattern_count"],
              flush=True)
        atomic_json_write(output_path, result)
    else:
        result["status"] = "ITERATION_LIMIT"

    result["menu_size"] = len(seeds) + len(rounds)
    result["split_set_size_tally"] = {
        str(len(r["split_roles"])): sum(
            1 for x in rounds if len(x["split_roles"]) == len(r["split_roles"])
        )
        for r in rounds
    }
    result["claim_boundary"] = (
        "The oracle matches Theorem 1's hypothesis: a certificate carries one "
        "allocation for every side-pattern vector of its split set, and the "
        "coverage is recomputed and enforced rather than trusted.  UNSAT is "
        "therefore the chart-level theorem for the declared exact-response "
        "chart and this edge budget, not a statement about four-agent EFX.  "
        "SAT is a profile that the widest tame family does not close, which is "
        "the genuine failure shape; a wild role is still never split, so such "
        "a profile is open rather than refuted."
    )
    atomic_json_write(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--form-index", type=int, choices=(0, 2), required=True)
    parser.add_argument("--seed-menu", type=Path, default=None)
    parser.add_argument("--edge-cap", type=int, default=4)
    parser.add_argument("--pattern-budget", type=int, default=4096)
    parser.add_argument("--maximum-rounds", type=int, default=400)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--random-seed", type=int, default=0)
    parser.add_argument("--master-mode", choices=MASTER_MODES, default="qflra")
    parser.add_argument("--resume", type=Path)
    parser.add_argument(
        "--cut-ledger", type=Path, required=True,
        help="fsynced JSONL certificate ledger; required for every chart run",
    )
    args = parser.parse_args()
    result = run(args.output, args.form_index, args.seed_menu,
                 args.maximum_rounds, args.timeout_seconds, args.random_seed,
                 args.edge_cap, args.pattern_budget, args.resume,
                 args.cut_ledger, args.master_mode)
    print(json.dumps({
        "status": result["status"],
        "seed_certificates": result["seed_certificates"],
        "rounds": len(result["rounds"]),
        "menu_size": result["menu_size"],
        "split_set_size_tally": result["split_set_size_tally"],
    }, indent=2))


if __name__ == "__main__":
    main()
