#!/usr/bin/env python3
"""Successor-state model checker for the `T_{L,times}` controlled-floor-reset closure.

Repair item 5 of `results/TLX_CLOSURE_REFEREE_REPORT_20260816.md`.  This is the
audit the retracted closure should have had: it instantiates genuine
`T_{L,times}^*`-shaped states over small exact-arithmetic instances, applies the
root singleton supplier star with the controlled floor reset, computes the REAL
globally minimum desired response at the star allocation, and then compares the
SUCCESSOR state's named packet against the predecessor's.

Nothing here is hardcoded: every reported boolean and every verdict is computed
from an exhaustive scan.  `--self-test` flips inputs on the primitive checkers
and on a certified witness and verifies that the verdicts move.

State format (frozen contract
`results/GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_CONTRACT_20260813.md:14`)

    S = (Y, P, r, alpha, F, Sigma, M, h, R, L, C)

instantiated here as the sub-tuple the star's own proof consumes:

    Y      current allocation (four owners + charity), exhaustively enumerated
    r      the first-priority owner of the fixed priority order, agent 0
    (X,r,x) immutable base certificate; X is COMPUTED as a globally
           lexicographically maximal partial-EFX-with-charity allocation
    alpha  physical anchor label, instantiated by its load-bearing content:
           the old common-safe desired root core A_anchor <= O = G - X_r with
           |A_anchor| >= 2 and v_r(A_anchor) > x   (closure theorem eq. (1))
    F      current protected floor vector, F_i = v_i(Y_i), with the protected
           root floor F_r >= x
    L      retirement ledger, instantiated by L_alpha <= G (nonempty)
    A      current candidate's cell, K = A cap L_alpha nonempty, K <= Y_r
           (root-holder branch)
    C      collision history; carried as the derived collision sets

See `results/TLX_SUCCESSOR_MODEL_CHECK_20260816.md` for the list of documented
simplifications and why they do not lose the G2/G3/G7 phenomena.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import time
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path

import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[2]
BIG = 10**9
ROOT_AGENT = 0
AGENTS = (0, 1, 2, 3)
CHARITY = 4


# --------------------------------------------------------------------------
# combinatorial tables (per number of goods)
# --------------------------------------------------------------------------


class Tables:
    """Allocation / subset tables for a fixed number of goods."""

    def __init__(self, m: int) -> None:
        self.m = m
        self.G = (1 << m) - 1
        self.nsub = 1 << m
        self.size = np.array([bin(s).count("1") for s in range(self.nsub)], dtype=np.int64)
        allocs = []
        for assign in product(range(5), repeat=m):
            bundles = [0] * 5
            for good, slot in enumerate(assign):
                bundles[slot] |= 1 << good
            allocs.append(tuple(bundles))
        self.alloc = np.array(allocs, dtype=np.int64)  # (5^m, 5)
        self.alloc_list = allocs
        self.subsets_by_card: dict[int, list[list[int]]] = {}

    def subsets(self, mask: int, card: int) -> list[int]:
        bits = [1 << i for i in range(self.m) if mask >> i & 1]
        return [sum(c) for c in combinations(bits, card)]


_TABLES: dict[int, Tables] = {}


def tables(m: int) -> Tables:
    if m not in _TABLES:
        _TABLES[m] = Tables(m)
    return _TABLES[m]


def bits(mask: int) -> tuple[int, ...]:
    out = []
    i = 0
    while mask:
        if mask & 1:
            out.append(i)
        mask >>= 1
        i += 1
    return tuple(out)


def popcount(mask: int) -> int:
    return bin(mask).count("1")


# --------------------------------------------------------------------------
# valuation-row tables and the repo's partial-EFX-with-charity predicate
# --------------------------------------------------------------------------


def row_tables(values: tuple[tuple[int, ...], ...], tab: Tables):
    """total[o][S] and min[o][S] over all subsets S, exact integer arithmetic."""
    idx = np.arange(tab.nsub)
    totals = np.zeros((4, tab.nsub), dtype=np.int64)
    mins = np.full((4, tab.nsub), BIG, dtype=np.int64)
    for o in range(4):
        for g in range(tab.m):
            has = ((idx >> g) & 1).astype(bool)
            totals[o] += values[o][g] * has
            mins[o] = np.where(has, np.minimum(mins[o], values[o][g]), mins[o])
    return totals, mins


def tail_value(totals, mins, sizes, o: int, mask: int) -> int:
    """v_o(mask) minus the good of mask that o values least (0 if |mask| <= 1)."""
    if sizes[mask] <= 1:
        return 0
    return int(totals[o][mask] - mins[o][mask])


def is_efx_with_charity(bundles, charity, totals, mins, sizes) -> bool:
    """Matches `tracks/parkability/audit_fixed_u_global_lex_premise.py:49-59`."""
    for o in AGENTS:
        own = int(totals[o][bundles[o]])
        for t in AGENTS:
            if own < tail_value(totals, mins, sizes, o, bundles[t]):
                return False
        if own < int(totals[o][charity]):
            return False
    return True


def lexmax_bases(tab: Tables, totals, mins, cap: int):
    """All globally lex-maximal partial EFX allocations (capped list + true count).

    Rivals range over every 5^m assignment of a good to one of four owners or
    to charity, per `ALTERNATING_GLOBAL_LEX_ATOMIC_THEOREM.md:48-51`.
    """
    A = tab.alloc
    sizes = tab.size
    n = A.shape[0]
    val = np.empty((4, 5, n), dtype=np.int64)
    tail = np.empty((4, 5, n), dtype=np.int64)
    for o in range(4):
        for t in range(5):
            sub = A[:, t]
            val[o, t] = totals[o][sub]
            sz = sizes[sub]
            tail[o, t] = np.where(sz >= 2, val[o, t] - mins[o][sub], 0)
    ok = np.ones(n, dtype=bool)
    for o in range(4):
        own = val[o, o]
        for t in range(4):
            ok &= own >= tail[o, t]
        ok &= own >= val[o, 4]
    cand = np.flatnonzero(ok)
    if cand.size == 0:
        return None, [], 0, 0
    efx_count = int(cand.size)
    vector = []
    for o in range(4):
        column = val[o, o][cand]
        best = int(column.max())
        cand = cand[column == best]
        vector.append(best)
    bases = [tuple(int(v) for v in A[i]) for i in cand[:cap]]
    return tuple(vector), bases, int(cand.size), efx_count


# --------------------------------------------------------------------------
# the operation under test: root singleton supplier star + controlled reset
# --------------------------------------------------------------------------


def star_allocation(tab: Tables, k: int, u: int):
    """`Y_r = G-k`, `Y_u = {k}`, `Y_j = empty`, empty charity.  Closure eq. (4)."""
    bundles = [0, 0, 0, 0]
    bundles[ROOT_AGENT] = tab.G ^ (1 << k)
    bundles[u] = 1 << k
    return tuple(bundles), 0


def minimum_desired_responses(tab: Tables, totals, mins, bundles, charity):
    """The REAL globally minimum desired response set at an actual allocation.

    Follows `STRICT_FIRST_PRIORITY_FLOOR_RESET_ADMISSION_THEOREM_20260814.md:57-63`
    literally: after the controlled reset the floors are F_i = v_i(Y_i), and D
    minimises cardinality "among every source and every desired subset of every
    target".  Returns (cardinality, [(source, target, subset)...], floors).

    `strict` reading = every target (what the reset theorem's minimisation
    quantifier actually says).  The caller separately filters to targets that
    are strongly envied (the charitable reading used by the closure theorem
    when it restricts D to subsets of G-k).
    """
    floors = [int(totals[i][bundles[i]]) for i in AGENTS]
    for card in range(1, tab.m + 1):
        found = []
        for j in AGENTS:
            if bundles[j] == 0:
                continue
            for sub in tab.subsets(bundles[j], card):
                for i in AGENTS:
                    if i == j:
                        continue
                    if int(totals[i][sub]) > floors[i]:
                        found.append((i, j, sub))
        if found:
            return card, found, floors
    return None, [], floors


def strongly_envied(tab, totals, mins, bundles, charity, source, target) -> bool:
    own = int(totals[source][bundles[source]])
    return own < tail_value(totals, mins, tab.size, source, bundles[target])


# --------------------------------------------------------------------------
# per-instance analysis
# --------------------------------------------------------------------------


def analyse_star(tab, totals, mins, k, u):
    """Everything G2 asks about the star allocation, computed."""
    bundles, charity = star_allocation(tab, k, u)
    sizes = tab.size
    efx = is_efx_with_charity(bundles, charity, totals, mins, sizes)
    card, responses, floors = minimum_desired_responses(tab, totals, mins, bundles, charity)
    walls = [
        (i, j)
        for i in AGENTS
        for j in AGENTS
        if i != j and strongly_envied(tab, totals, mins, bundles, charity, i, j)
    ]
    wall_targets = {j for _, j in walls}
    restricted = [t for t in responses if t[1] in wall_targets]
    # Compact each reading to its distinct response supports; the successor
    # named packet depends on a response only through its support and on
    # whether the root can be its source.
    compact = {}
    for name, pool in (("strict", responses), ("walls", restricted)):
        seen: dict[int, bool] = {}
        for source, _target, sub in pool:
            seen[sub] = seen.get(sub, False) or (source == ROOT_AGENT)
        compact[name] = tuple(seen.items())
    return {
        "compact": compact,
        "bundles": bundles,
        "charity": charity,
        "floors": floors,
        "star_is_efx": efx,
        "min_card": card,
        "responses": responses,
        "n_min_responses": len(responses),
        "walls": walls,
        "responses_restricted_to_walls": restricted,
        "min_response_can_contain_k": any(t[2] & (1 << k) for t in responses),
        "min_response_can_contain_k_wall_reading": any(
            t[2] & (1 << k) for t in restricted
        ),
        "root_is_a_source": any(t[0] == ROOT_AGENT for t in responses),
        "all_walls_against_root_bundle": all(j == ROOT_AGENT for _, j in walls),
    }


def response_pool(star, reading):
    return star["responses"] if reading == "strict" else star["responses_restricted_to_walls"]


def successor_summary(star, l_alpha, k_mask, reading):
    """Fast aggregate of the successor named packet over every legal response.

    K' = A' cap L_alpha with A' = the adopted response D (see the report's
    documented simplification 4).  Returns None when the reading admits no
    response at all.
    """
    pool = star["compact"][reading]
    if not pool:
        return None
    k_size = popcount(k_mask)
    best = None
    worst = -1
    claim5_ok = True
    root_source_hits_ledger = False
    for sub, root_source in pool:
        kp = popcount(sub & l_alpha)
        if kp > worst:
            worst = kp
        if best is None or kp < best:
            best = kp
        if (sub & k_mask) == k_mask:
            claim5_ok = False
        if root_source and (sub & l_alpha):
            root_source_hits_ledger = True
    return {
        "k_size": k_size,
        "angelic_kprime": best,
        "demonic_kprime": worst,
        "decreases_always": worst < k_size,
        "decreases_for_some_choice": best < k_size,
        "no_choice_decreases": best >= k_size,
        "can_stall": worst >= k_size,
        "claim5_holds": claim5_ok,
        "successor_packet_root_held": root_source_hits_ledger,
    }


def star_collision_multiplicity(tab, star, pre_bundles, l_alpha):
    """|{g in L_alpha : the star moves g off its current holder}|.

    This is the collision set of the candidate itself, as defined in
    `GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_COMPOSITION_THEOREM_20260813.md:69-72`,
    computed by diffing the two holder maps (not by a closed formula).
    """
    kept = 0
    for a in AGENTS:
        kept |= pre_bundles[a] & star["bundles"][a]
    return popcount(l_alpha & ~kept)


def successor_packets(star, l_alpha, k_mask, pre_holder, tab, reading="strict"):
    """Successor named packet K' = A' cap L_alpha with A' = the adopted response D.

    For every globally minimum desired response D the successor allocation is
    the star with D transferred from its target to its source; the adopted
    response is the next candidate's cell.  Returns the angelic (best-case)
    and demonic (worst-case) successor packet sizes plus the collision
    bookkeeping the frozen contract actually orders.
    """
    k_size = popcount(k_mask)
    out = []
    pool = (
        star["responses"]
        if reading == "strict"
        else star["responses_restricted_to_walls"]
    )
    for source, target, sub in pool:
        succ = list(star["bundles"])
        succ[target] ^= sub
        succ[source] |= sub
        kprime = sub & l_alpha
        holder = {}
        for a in AGENTS:
            for g in bits(succ[a]):
                holder[g] = a
        moved = [g for g in bits(l_alpha) if pre_holder.get(g) != holder.get(g)]
        out.append(
            {
                "source": source,
                "target": target,
                "response": sub,
                "successor_bundles": tuple(succ),
                "kprime": kprime,
                "kprime_size": popcount(kprime),
                "kprime_holder_is_root": bool(kprime) and all(
                    holder[g] == ROOT_AGENT for g in bits(kprime)
                ),
                "response_meets_L_minus_K": bool(sub & l_alpha & ~k_mask),
                "claim5_holds": (sub & k_mask) != k_mask,
                "star_collision_multiplicity": len(moved),
            }
        )
    sizes = [o["kprime_size"] for o in out]
    return {
        "reading": reading,
        "n_options": len(out),
        "options": out,
        "k_size": k_size,
        "angelic_kprime": min(sizes) if sizes else None,
        "demonic_kprime": max(sizes) if sizes else None,
        "packet_strictly_decreases_for_every_choice": bool(sizes) and max(sizes) < k_size,
        "packet_can_fail_to_decrease": bool(sizes) and max(sizes) >= k_size,
        "claim5_holds_for_every_choice": all(o["claim5_holds"] for o in out),
        "successor_packet_ever_root_held": any(o["kprime_holder_is_root"] for o in out),
        "max_star_collision_multiplicity": max(
            (o["star_collision_multiplicity"] for o in out), default=0
        ),
    }


def canonical_pre_state(tab, totals, x, k_mask, withheld, holder_agent=1):
    """A concrete feasible pre-state Y with K <= Y_r and L_alpha \\ Y_r = withheld.

    Root-maximal instantiation: Y_r = G - withheld (the largest root bundle
    compatible with the withheld set), withheld parked on one nonroot owner.
    Phase 2 replaces this by an exhaustive scan over every feasible Y.
    """
    yr = tab.G ^ withheld
    bundles = [0, 0, 0, 0]
    bundles[ROOT_AGENT] = yr
    bundles[holder_agent] = withheld
    holder = {}
    for a in AGENTS:
        for g in bits(bundles[a]):
            holder[g] = a
    return tuple(bundles), holder, int(totals[ROOT_AGENT][yr])


def cancellation(tab, totals, x, k, withheld):
    """Canonical cancellation `Z^-` applied to the star.

    Composition theorem :69-72 / :87 -- the candidate's collision set is the
    set of goods of L_alpha that the candidate moves off their current
    holders; `Z^-` leaves each of them with its current holder and performs
    every other transfer.  For the star that set is `withheld + {k}`
    (`withheld` moves onto the root, `k` moves off it).

    variant_B: contract-literal cancellation, k also stays with the root.
    variant_C: the referee's G7 scenario -- the deliberate sacrifice of k to u
               is kept, only the off-root retired goods are withheld.
    """
    yr_b = tab.G ^ withheld
    yr_c = yr_b & ~(1 << k)
    return {
        "withheld": withheld,
        "root_bundle_B": yr_b,
        "root_value_B": int(totals[ROOT_AGENT][yr_b]),
        "strict_B": int(totals[ROOT_AGENT][yr_b]) > x,
        "root_bundle_C": yr_c,
        "root_value_C": int(totals[ROOT_AGENT][yr_c]),
        "strict_C": int(totals[ROOT_AGENT][yr_c]) > x,
    }


# --------------------------------------------------------------------------
# sweep over a space of instances
# --------------------------------------------------------------------------


def matrix_stream(space):
    m = space["goods"]
    root_range = space["root_weights"]
    other_range = space["other_weights"]
    columns = [
        (a, b, c, d)
        for a in root_range
        for b in other_range
        for c in other_range
        for d in other_range
    ]
    if space["mode"] == "exhaustive":
        # Goods are unlabelled: the whole analysis is invariant under permuting
        # goods, so one canonical (sorted) multiset of columns per orbit is a
        # complete enumeration.
        for combo in combinations_with_replacement(columns, m):
            yield tuple(tuple(col[o] for col in combo) for o in range(4))
    else:
        rng = random.Random(space["seed"])
        seen = set()
        for _ in range(space["samples"]):
            combo = tuple(sorted(rng.choice(columns) for _ in range(m)))
            if combo in seen:
                continue
            seen.add(combo)
            yield tuple(tuple(col[o] for col in combo) for o in range(4))


def space_size(space):
    m = space["goods"]
    ncol = len(space["root_weights"]) * len(space["other_weights"]) ** 3
    if space["mode"] == "exhaustive":
        from math import comb

        return comb(ncol + m - 1, m)
    return space["samples"]


def run_space(space, verbose=True):
    m = space["goods"]
    tab = tables(m)
    sizes = tab.size
    base_cap = space.get("base_cap", 4)

    counts = {
        "matrices_scanned": 0,
        "matrices_with_efx_base": 0,
        "bases_examined": 0,
        "bases_with_anchor": 0,
        "bases_anchor_absent": 0,
        "root_strictness_eq3_checks": 0,
        "root_strictness_eq3_failures": 0,
        "star_states_checked": 0,
        "star_states_efx": 0,
        "star_min_card_1": 0,
        "star_min_card_gt_1": 0,
        "star_min_response_can_contain_k": 0,
        "star_root_is_a_source": 0,
        "star_walls_not_all_against_root": 0,
        "successor_configs_checked": 0,
        "successor_packet_decrease_always": 0,
        "successor_packet_can_stall": 0,
        "successor_claim5_violations": 0,
        "successor_packet_ever_root_held": 0,
        "successor_collision_multiplicity_increases": 0,
        "wall_successor_packet_decrease_always": 0,
        "wall_successor_packet_can_stall": 0,
        "wall_successor_claim5_violations": 0,
        "wall_successor_no_response_available": 0,
        "wall_successor_decreases_for_some_choice": 0,
        "wall_successor_no_choice_decreases": 0,
        "wall_no_choice_decreases_on_L_over_K_slice": 0,
        "cancellation_configs_rejected_no_root_protected_prestate": 0,
        "cancellation_B_failures_at_equality": 0,
        "cancellation_B_failures_below_x": 0,
        "successor_can_sustain_another_round": 0,
        "configs_with_L_alpha_equal_K": 0,
        "configs_with_L_alpha_strictly_over_K": 0,
        "wall_decrease_on_L_equal_K_slice": 0,
        "wall_decrease_on_L_over_K_slice": 0,
        "cancellation_configs_checked": 0,
        "cancellation_B_failures": 0,
        "cancellation_C_failures": 0,
    }
    witnesses = {
        "eq3_failure": None,
        "star_min_card_gt_1": None,
        "min_response_contains_k": None,
        "packet_stall": None,
        "wall_packet_stall": None,
        "wall_no_choice_decreases": None,
        "claim5_violation": None,
        "cancellation_B_failure": None,
        "cancellation_C_failure": None,
        "collision_multiplicity_increase": None,
    }

    def wants(slot, key) -> bool:
        cur = witnesses[slot]
        return cur is None or key < cur["_key"]

    def keep(slot, payload, key):
        if wants(slot, key):
            payload = dict(payload)
            payload["_key"] = key
            witnesses[slot] = payload

    t0 = time.time()
    for values in matrix_stream(space):
        counts["matrices_scanned"] += 1
        weight_sum = sum(map(sum, values))
        totals, mins = row_tables(values, tab)
        vector, bases, n_opt, n_efx = lexmax_bases(tab, totals, mins, base_cap)
        if vector is None:
            continue
        counts["matrices_with_efx_base"] += 1

        # G2: the star allocation depends only on (values, k, u), not on the base.
        star_cache = {}
        for k in range(m):
            for u in (1, 2, 3):
                star = analyse_star(tab, totals, mins, k, u)
                star_cache[(k, u)] = star
                counts["star_states_checked"] += 1
                if star["star_is_efx"]:
                    counts["star_states_efx"] += 1
                if star["min_card"] == 1:
                    counts["star_min_card_1"] += 1
                else:
                    counts["star_min_card_gt_1"] += 1
                    keep(
                        "star_min_card_gt_1",
                        {"values": values, "k": k, "u": u, "min_card": star["min_card"]},
                        (star["min_card"], values),
                    )
                if star["min_response_can_contain_k"]:
                    counts["star_min_response_can_contain_k"] += 1
                    keep(
                        "min_response_contains_k",
                        {"values": values, "k": k, "u": u},
                        (sum(map(sum, values)), values),
                    )
                if star["root_is_a_source"]:
                    counts["star_root_is_a_source"] += 1
                if not star["all_walls_against_root_bundle"]:
                    counts["star_walls_not_all_against_root"] += 1

        # Every tied lex-maximal base shares the same first coordinate, so x is
        # a function of the instance; the base enters the state only through
        # X_r (anchor availability) and the recorded witness data.
        x = vector[ROOT_AGENT]
        anchored_bases = []
        for base in bases:
            counts["bases_examined"] += 1
            xr = base[ROOT_AGENT]
            o_mask = tab.G ^ xr
            if sizes[o_mask] >= 2 and int(totals[ROOT_AGENT][o_mask]) > x:
                counts["bases_with_anchor"] += 1
                anchored_bases.append(base)
            else:
                counts["bases_anchor_absent"] += 1
        if not anchored_bases:
            continue
        base = anchored_bases[0]
        anchor = tab.G ^ base[ROOT_AGENT]  # A = O is a valid anchor core here

        row0 = totals[ROOT_AGENT]
        for k in range(m):
            k_mask = 1 << k
            counts["root_strictness_eq3_checks"] += 1
            if not int(row0[tab.G ^ k_mask]) > x:
                counts["root_strictness_eq3_failures"] += 1
                keep("eq3_failure", {"values": values, "base": base, "k": k, "x": x},
                     (values, k))

            rest = tab.G & ~k_mask
            withheld = rest
            while True:  # every subset of `rest`, descending
                l_alpha = k_mask | withheld
                yr_max = tab.G ^ withheld
                if int(row0[yr_max]) < x:
                    # No root-protected pre-state exists with this withheld set:
                    # the configuration is not a legal T_{L,x}* state at all.
                    counts["cancellation_configs_rejected_no_root_protected_prestate"] += 1
                else:
                    pre_bundles = (yr_max, withheld, 0, 0)
                    counts["cancellation_configs_checked"] += 1
                    strict_b = int(row0[yr_max]) > x
                    strict_c = int(row0[yr_max & ~k_mask]) > x
                    if not strict_b:
                        if int(row0[yr_max]) == x:
                            counts["cancellation_B_failures_at_equality"] += 1
                        else:
                            counts["cancellation_B_failures_below_x"] += 1
                    order = (popcount(withheld), weight_sum, values)
                    if not strict_b or not strict_c:
                        slots = []
                        if not strict_b:
                            counts["cancellation_B_failures"] += 1
                            slots.append("cancellation_B_failure")
                        if not strict_c:
                            counts["cancellation_C_failures"] += 1
                            slots.append("cancellation_C_failure")
                        slots = [s for s in slots if wants(s, order)]
                        if slots:
                            payload = {
                                "values": values, "base": base, "x": x, "k": k,
                                "withheld": withheld, "L_alpha": l_alpha, "K": k_mask,
                                "anchor": anchor,
                                "cancellation": cancellation(tab, totals, x, k, withheld),
                            }
                            for s in slots:
                                keep(s, payload, order)

                    for u in (1, 2, 3):
                        star = star_cache[(k, u)]
                        counts["successor_configs_checked"] += 1
                        mult = star_collision_multiplicity(tab, star, pre_bundles, l_alpha)
                        if mult > popcount(k_mask):
                            counts["successor_collision_multiplicity_increases"] += 1
                            morder = (popcount(l_alpha), weight_sum, values)
                            if wants("collision_multiplicity_increase", morder):
                                keep(
                                    "collision_multiplicity_increase",
                                    {"values": values, "base": base, "k": k,
                                     "L_alpha": l_alpha, "K": k_mask, "anchor": anchor,
                                     "pre_multiplicity": popcount(k_mask),
                                     "star_multiplicity": mult},
                                    morder,
                                )
                        for reading in ("strict", "walls"):
                            s = successor_summary(star, l_alpha, k_mask, reading)
                            pre = "" if reading == "strict" else "wall_"
                            if s is None:
                                if reading == "walls":
                                    counts["wall_successor_no_response_available"] += 1
                                continue
                            if reading == "walls":
                                if s["decreases_for_some_choice"]:
                                    counts["wall_successor_decreases_for_some_choice"] += 1
                                else:
                                    counts["wall_successor_no_choice_decreases"] += 1
                                    if withheld != 0:
                                        counts["wall_no_choice_decreases_on_L_over_K_slice"] += 1
                                    norder = (popcount(l_alpha), weight_sum, values)
                                    if wants("wall_no_choice_decreases", norder):
                                        keep(
                                            "wall_no_choice_decreases",
                                            {"values": values, "base": base, "x": x, "k": k,
                                             "u": u, "withheld": withheld, "L_alpha": l_alpha,
                                             "K": k_mask, "anchor": anchor,
                                             "k_size": s["k_size"],
                                             "angelic_kprime": s["angelic_kprime"],
                                             "demonic_kprime": s["demonic_kprime"]},
                                            norder,
                                        )
                                if withheld == 0:
                                    counts["configs_with_L_alpha_equal_K"] += 1
                                    if s["decreases_always"]:
                                        counts["wall_decrease_on_L_equal_K_slice"] += 1
                                else:
                                    counts["configs_with_L_alpha_strictly_over_K"] += 1
                                    if s["decreases_always"]:
                                        counts["wall_decrease_on_L_over_K_slice"] += 1
                            if s["decreases_always"]:
                                counts[f"{pre}successor_packet_decrease_always"] += 1
                            if s["can_stall"]:
                                counts[f"{pre}successor_packet_can_stall"] += 1
                                slot = "packet_stall" if reading == "strict" else "wall_packet_stall"
                                sorder = (popcount(l_alpha), weight_sum, values)
                                if wants(slot, sorder):
                                    keep(
                                        slot,
                                        {"values": values, "base": base, "x": x, "k": k,
                                         "u": u, "withheld": withheld, "L_alpha": l_alpha,
                                         "K": k_mask, "anchor": anchor,
                                         "k_size": s["k_size"],
                                         "demonic_kprime": s["demonic_kprime"]},
                                        sorder,
                                    )
                            if not s["claim5_holds"]:
                                counts[f"{pre}successor_claim5_violations"] += 1
                                if reading == "strict" and wants("claim5_violation", (values, k)):
                                    keep(
                                        "claim5_violation",
                                        {"values": values, "base": base, "k": k, "u": u,
                                         "L_alpha": l_alpha, "K": k_mask, "anchor": anchor},
                                        (values, k),
                                    )
                            if reading == "strict" and s["successor_packet_root_held"]:
                                counts["successor_packet_ever_root_held"] += 1
                            if reading == "walls" and s["can_stall"]:
                                # Can the stalling successor host another round?
                                # It needs a nonempty successor packet and a
                                # root still protected at the base certificate.
                                for sub, _rs in star["compact"]["walls"]:
                                    if popcount(sub & l_alpha) < s["k_size"]:
                                        continue
                                    if int(row0[star["bundles"][ROOT_AGENT] & ~sub]) >= x:
                                        counts["successor_can_sustain_another_round"] += 1
                                        break
                if withheld == 0:
                    break
                withheld = (withheld - 1) & rest

    elapsed = time.time() - t0
    if verbose:
        print(f"  {space['name']}: {counts['matrices_scanned']} matrices, {elapsed:.1f}s")
    return counts, witnesses, elapsed


# --------------------------------------------------------------------------
# phase 2: certify a witness against every feasible pre-state allocation
# --------------------------------------------------------------------------


def certify_witness(values, base, k, withheld, tab, want_nondegenerate=True):
    """Exhaustive search for a genuine pre-state Y realising the witness.

    Requirements checked (all computed):
      * Y is a feasible partition of G over four owners plus charity;
      * the root holds the named packet K;
      * L_alpha \\ Y_r == withheld (the parked retired goods are off-root);
      * the protected root floor survives: v_r(Y_r) >= x;
      * an active recipient s != r exists with a strict-capture collision
        certificate on a candidate cell A = K + B: v_s(A) > F_s and
        v_s(B) <= F_s  (branch "strict capture" of the frozen contract's
        deterministic branch partition);
      * optionally, no owner is left holding the whole instance.
    """
    totals, mins = row_tables(values, tab)
    x = int(totals[ROOT_AGENT][base[ROOT_AGENT]])
    k_mask = 1 << k
    l_alpha = k_mask | withheld
    best = None
    for bundles in tab.alloc_list:
        owners, charity = bundles[:4], bundles[4]
        if owners[ROOT_AGENT] & k_mask != k_mask:
            continue
        if (l_alpha & ~owners[ROOT_AGENT]) != withheld:
            continue
        if int(totals[ROOT_AGENT][owners[ROOT_AGENT]]) < x:
            continue
        if want_nondegenerate and owners[ROOT_AGENT] == tab.G:
            continue
        occupied = sum(1 for o in owners if o)
        key = (-occupied, popcount(charity))
        if best is not None and key >= best[0]:
            continue
        floors = [int(totals[i][owners[i]]) for i in AGENTS]
        cert = None
        free = tab.G & ~l_alpha
        for s in (1, 2, 3):
            for b in range(free + 1):
                if b & ~free:
                    continue
                a_cell = k_mask | b
                if int(totals[s][a_cell]) > floors[s] and int(totals[s][b]) <= floors[s]:
                    cert = {"recipient": s, "B": b, "A_cell": a_cell,
                            "mu_s": int(totals[s][a_cell]) - floors[s],
                            "d_s": floors[s] - int(totals[s][b])}
                    break
            if cert:
                break
        if cert is None:
            continue
        best = (key, owners, charity, floors, cert)
    if best is None:
        return None
    _, owners, charity, floors, cert = best
    return {
        "Y": [sorted(bits(o)) for o in owners],
        "charity": sorted(bits(charity)),
        "floors": floors,
        "collision_certificate": {
            "recipient": cert["recipient"],
            "candidate_cell_A": sorted(bits(cert["A_cell"])),
            "B": sorted(bits(cert["B"])),
            "mu_s": cert["mu_s"],
            "d_s": cert["d_s"],
        },
    }


def expand_witness(w, m, tab, label):
    """Turn a packed witness into fully explicit exact data."""
    if w is None:
        return None
    values = w["values"]
    totals, mins = row_tables(values, tab)
    out = {
        "label": label,
        "goods": list(range(m)),
        "valuations": {f"agent{i}": {f"g{g}": values[i][g] for g in range(m)} for i in range(4)},
        "priority_order": ["agent0(root r)", "agent1", "agent2", "agent3"],
    }
    if "base" in w:
        base = w["base"]
        x = int(totals[ROOT_AGENT][base[ROOT_AGENT]])
        out["base_X"] = [sorted(bits(b)) for b in base[:4]]
        out["base_charity"] = sorted(bits(base[4]))
        out["x_eq_v_r_X_r"] = x
        out["O_eq_G_minus_X_r"] = sorted(bits(tab.G ^ base[ROOT_AGENT]))
        out["v_r_O"] = int(totals[ROOT_AGENT][tab.G ^ base[ROOT_AGENT]])
        if "anchor" in w:
            out["anchor_core_A"] = sorted(bits(w["anchor"]))
            out["v_r_anchor"] = int(totals[ROOT_AGENT][w["anchor"]])
    for key in ("k", "u", "x", "k_size", "demonic_kprime", "pre_multiplicity",
                "star_multiplicity", "min_card"):
        if key in w:
            out[key] = w[key]
    for key, name in (("L_alpha", "L_alpha"), ("K", "K"), ("withheld", "withheld_off_root_retired")):
        if key in w:
            out[name] = sorted(bits(w[key]))
    if "cancellation" in w:
        c = w["cancellation"]
        out["cancellation"] = {
            "Z_minus_root_bundle_contract_reading": sorted(bits(c["root_bundle_B"])),
            "v_r_of_it": c["root_value_B"],
            "root_strict_survives_contract_reading": c["strict_B"],
            "Z_minus_root_bundle_referee_reading": sorted(bits(c["root_bundle_C"])),
            "v_r_of_it_referee": c["root_value_C"],
            "root_strict_survives_referee_reading": c["strict_C"],
        }
    return out


# --------------------------------------------------------------------------
# self-tests: flip an input, confirm the checker notices
# --------------------------------------------------------------------------


def self_tests():
    """Flip one input at a time and confirm every primitive detector moves."""
    checks: dict[str, bool] = {}
    info: dict[str, object] = {}
    tab4 = tables(4)
    tab5 = tables(5)

    # 1. EFX detector responds to a single flipped valuation entry.
    #    X = ({g0,g1},{g2},{g3},{g4}); the only live comparison is
    #    v_o(X_o) >= max(v_o(g0), v_o(g1)).
    alloc = (0b00011, 0b00100, 0b01000, 0b10000, 0)
    v_a = ((1, 1, 1, 1, 1), (1, 1, 2, 1, 1), (1, 1, 1, 2, 1), (1, 1, 1, 1, 2))
    ta, ma = row_tables(v_a, tab5)
    before = is_efx_with_charity(alloc[:4], alloc[4], ta, ma, tab5.size)
    v_b = ((1, 1, 1, 1, 1), (3, 1, 2, 1, 1), (1, 1, 1, 2, 1), (1, 1, 1, 1, 2))
    tb, mb = row_tables(v_b, tab5)
    after = is_efx_with_charity(alloc[:4], alloc[4], tb, mb, tab5.size)
    checks["efx_detector_true_before_flip"] = bool(before)
    checks["efx_detector_false_after_flip"] = not bool(after)

    # 2. minimum-response cardinality is computed, not assumed to be 1.
    v1 = ((1, 1, 1, 1, 1),) * 4
    t5, m5 = row_tables(v1, tab5)
    card_star, _, _ = minimum_desired_responses(tab5, t5, m5, (0b11110, 0b00001, 0, 0), 0)
    # no empty-handed owner: every floor is >= 1, so no singleton is desired
    card_full, resp_full, _ = minimum_desired_responses(
        tab5, t5, m5, (0b00011, 0b00100, 0b01000, 0b10000), 0
    )
    checks["min_card_at_star_is_1"] = card_star == 1
    checks["min_card_without_empty_owner_exceeds_1"] = (
        card_full is not None and card_full > 1
    )
    info["min_card_without_empty_owner_value"] = card_full
    # flip: empty one owner and the same instance must drop back to 1
    card_emptied, _, _ = minimum_desired_responses(
        tab5, t5, m5, (0b00111, 0b00000, 0b01000, 0b10000), 0
    )
    checks["min_card_returns_to_1_when_an_owner_is_emptied"] = card_emptied == 1

    # 3. cancellation strictness flips when one root weight is perturbed.
    #    Canonical G7 shape: X_r = {g0,g1}, O = {g2,g3}, withheld = O, k = g0.
    vg = ((3, 3, 4, 4), (1, 1, 1, 1), (1, 1, 1, 1), (1, 1, 1, 1))
    tg, _ = row_tables(vg, tab4)
    x = int(tg[0][0b0011])
    c_fail = cancellation(tab4, tg, x, 0, 0b1100)
    vg_flip = ((3, 4, 4, 4), (1, 1, 1, 1), (1, 1, 1, 1), (1, 1, 1, 1))
    tf, _ = row_tables(vg_flip, tab4)
    # same base bundle, one root weight raised -> G-withheld is now worth more
    c_pass = cancellation(tab4, tf, x, 0, 0b1100)
    checks["cancellation_fails_at_the_boundary"] = not c_fail["strict_B"]
    checks["cancellation_passes_after_one_weight_flip"] = c_pass["strict_B"]
    info["cancellation_boundary_values"] = [c_fail["root_value_B"], x, c_pass["root_value_B"]]

    # 4. lex-max detector: the reported base is EFX, undominated, and a
    #    deliberately worse EFX allocation is not reported.
    vl = ((3, 2, 2, 1), (1, 3, 2, 2), (2, 1, 3, 2), (2, 2, 1, 3))
    tl, ml = row_tables(vl, tab4)
    vector, bases, _, _ = lexmax_bases(tab4, tl, ml, 8)
    checks["lexmax_bases_are_efx"] = all(
        is_efx_with_charity(b[:4], b[4], tl, ml, tab4.size) for b in bases
    )
    dominated = False
    worse = None
    for a in tab4.alloc_list:
        if not is_efx_with_charity(a[:4], a[4], tl, ml, tab4.size):
            continue
        vec = tuple(int(tl[o][a[o]]) for o in AGENTS)
        if vec > vector:
            dominated = True
        if vec < vector and worse is None:
            worse = a
    checks["lexmax_vector_is_undominated"] = not dominated
    checks["a_strictly_worse_efx_allocation_exists"] = worse is not None
    checks["worse_allocation_not_reported_as_base"] = worse is None or worse not in bases
    info["lexmax_vector"] = list(vector) if vector else None

    # 5. successor-packet accounting reacts to the ledger content.
    #    Same star, two ledgers: one where L_alpha = K, one where L_alpha > K.
    tstar, mstar = row_tables(((1, 1, 1, 1, 1),) * 4, tab5)
    star = analyse_star(tab5, tstar, mstar, 0, 1)
    holder = {g: (ROOT_AGENT if g else ROOT_AGENT) for g in range(5)}
    tight = successor_packets(star, 0b00001, 0b00001, holder, tab5, reading="walls")
    loose = successor_packets(star, 0b00011, 0b00001, holder, tab5, reading="walls")
    checks["packet_decreases_when_ledger_equals_packet"] = tight[
        "packet_strictly_decreases_for_every_choice"
    ]
    checks["packet_stalls_when_ledger_strictly_contains_packet"] = loose[
        "packet_can_fail_to_decrease"
    ]
    info["tight_demonic_kprime_wall_reading"] = tight["demonic_kprime"]
    info["loose_demonic_kprime_wall_reading"] = loose["demonic_kprime"]
    # strict reading of the reset theorem's quantifier: the singleton target
    # {k} is desired by an emptied owner, so D = {k} is admissible and the
    # closure's equation (5) is violated.  This must differ from the wall
    # reading -- if the checker collapsed the two readings it would not.
    tight_strict = successor_packets(star, 0b00001, 0b00001, holder, tab5, reading="strict")
    checks["strict_and_wall_readings_differ"] = (
        tight_strict["claim5_holds_for_every_choice"]
        != tight["claim5_holds_for_every_choice"]
    )
    info["tight_claim5_strict_reading"] = tight_strict["claim5_holds_for_every_choice"]
    info["tight_claim5_wall_reading"] = tight["claim5_holds_for_every_choice"]

    return {"checks": checks, "info": info, "all_passed": all(checks.values())}


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------


SPACES = [
    {
        "name": "A_m5_w12_exhaustive",
        "goods": 5,
        "root_weights": (1, 2),
        "other_weights": (1, 2),
        "mode": "exhaustive",
        "base_cap": 4,
    },
    {
        "name": "B_m5_root123_others12_exhaustive",
        "goods": 5,
        "root_weights": (1, 2, 3),
        "other_weights": (1, 2),
        "mode": "exhaustive",
        "base_cap": 4,
    },
    {
        "name": "C_m6_w12_exhaustive",
        "goods": 6,
        "root_weights": (1, 2),
        "other_weights": (1, 2),
        "mode": "exhaustive",
        "base_cap": 2,
    },
    {
        "name": "D_m5_w123_sampled",
        "goods": 5,
        "root_weights": (1, 2, 3),
        "other_weights": (1, 2, 3),
        "mode": "sampled",
        "samples": 30000,
        "seed": 20260816,
        "base_cap": 4,
    },
    {
        "name": "E_m6_w123_sampled",
        "goods": 6,
        "root_weights": (1, 2, 3),
        "other_weights": (1, 2, 3),
        "mode": "sampled",
        "samples": 5000,
        "seed": 816,
        "base_cap": 2,
    },
    {
        "name": "F_m5_wideroot_probe",
        "goods": 5,
        "root_weights": (1, 2, 3, 4, 5, 6, 7, 8),
        "other_weights": (1, 2, 3),
        "mode": "sampled",
        "samples": 30000,
        "seed": 5,
        "base_cap": 4,
    },
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path)
    ap.add_argument("--only", nargs="*", help="restrict to these space names")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    st = self_tests()
    if args.self_test:
        print(json.dumps(st, indent=2, sort_keys=True))
        return

    spaces = SPACES if not args.only else [s for s in SPACES if s["name"] in args.only]
    per_space = {}
    all_counts = {}
    all_witnesses = {}
    total_time = 0.0
    for space in spaces:
        counts, wit, elapsed = run_space(space)
        total_time += elapsed
        tab = tables(space["goods"])
        expanded = {}
        for slot, w in wit.items():
            expanded[slot] = expand_witness(w, space["goods"], tab, slot)
            if expanded[slot] and slot in ("cancellation_B_failure", "cancellation_C_failure",
                                           "packet_stall"):
                cert = certify_witness(
                    w["values"], w["base"], w["k"], w.get("withheld", 0), tab
                )
                expanded[slot]["certified_pre_state"] = cert
        per_space[space["name"]] = {
            "space": {k: (list(v) if isinstance(v, tuple) else v) for k, v in space.items()},
            "declared_space_size": space_size(space),
            "counts": counts,
            "witnesses": expanded,
            "seconds": round(elapsed, 2),
        }
        for k, v in counts.items():
            all_counts[k] = all_counts.get(k, 0) + v
        for slot, w in expanded.items():
            if w is not None and all_witnesses.get(slot) is None:
                all_witnesses[slot] = {"space": space["name"], **w}

    # ---- verdicts, all computed from the counts above -----------------------
    g2_singleton = (
        all_counts["star_min_card_gt_1"] == 0 and all_counts["star_min_card_1"] > 0
    )
    g2_never_efx = all_counts["star_states_efx"] == 0 and all_counts["star_states_checked"] > 0
    g3_stall = all_counts["successor_packet_can_stall"] > 0
    g3_multiplicity = all_counts["successor_collision_multiplicity_increases"] > 0
    g7_fail_B = all_counts["cancellation_B_failures"] > 0
    g7_fail_C = all_counts["cancellation_C_failures"] > 0

    verdicts = {
        "G2_response_is_always_a_singleton": {
            "verdict": "CONFIRMED" if g2_singleton else "REFUTED",
            "min_card_1_cases": all_counts["star_min_card_1"],
            "min_card_gt_1_cases": all_counts["star_min_card_gt_1"],
        },
        "G2_star_allocation_is_never_EFX": {
            "verdict": "CONFIRMED" if g2_never_efx else "REFUTED",
            "efx_star_states": all_counts["star_states_efx"],
            "star_states_checked": all_counts["star_states_checked"],
        },
        "G2_minimum_response_may_contain_k": {
            "verdict": "CONFIRMED"
            if all_counts["star_min_response_can_contain_k"] > 0
            else "NOT_OBSERVED",
            "cases": all_counts["star_min_response_can_contain_k"],
            "root_is_a_source_cases": all_counts["star_root_is_a_source"],
        },
        "G3_packet_coordinate_can_fail_to_decrease": {
            "verdict": "CONFIRMED" if g3_stall else "REFUTED",
            "reading": "strict (the reset theorem's own minimisation quantifier)",
            "stalling_configs": all_counts["successor_packet_can_stall"],
            "configs_checked": all_counts["successor_configs_checked"],
        },
        "G3_packet_coordinate_can_fail_to_decrease_STEELMAN": {
            "verdict": "CONFIRMED"
            if all_counts["wall_successor_packet_can_stall"] > 0
            else "REFUTED",
            "reading": "response restricted to strongly-envied targets (D <= G-k),"
            " adversarial choice among equally minimal responses",
            "stalling_configs": all_counts["wall_successor_packet_can_stall"],
            "always_decreasing_configs": all_counts["wall_successor_packet_decrease_always"],
            "configs_with_no_wall_response": all_counts["wall_successor_no_response_available"],
        },
        "G3_no_legal_response_at_all_decreases_the_packet_MAXIMAL_STEELMAN": {
            "verdict": "CONFIRMED"
            if all_counts["wall_successor_no_choice_decreases"] > 0
            else "REFUTED",
            "reading": "response restricted to strongly-envied targets AND chosen"
            " favourably among equally minimal responses",
            "no_choice_decreases_configs": all_counts["wall_successor_no_choice_decreases"],
            "of_which_on_L_strictly_over_K": all_counts[
                "wall_no_choice_decreases_on_L_over_K_slice"
            ],
            "some_choice_decreases_configs": all_counts[
                "wall_successor_decreases_for_some_choice"
            ],
        },
        "closure_equation_5_holds_under_the_reset_theorems_own_quantifier": {
            "verdict": "REFUTED"
            if all_counts["successor_claim5_violations"] > 0
            else "CONFIRMED",
            "violations_strict_reading": all_counts["successor_claim5_violations"],
            "violations_wall_reading": all_counts["wall_successor_claim5_violations"],
        },
        "G3_star_increases_collision_hitting_multiplicity": {
            "verdict": "CONFIRMED" if g3_multiplicity else "REFUTED",
            "increasing_configs": all_counts["successor_collision_multiplicity_increases"],
        },
        "G7_canonical_cancellation_breaks_root_strictness": {
            "verdict": "CONFIRMED" if (g7_fail_B or g7_fail_C) else "REFUTED",
            "contract_reading_failures": all_counts["cancellation_B_failures"],
            "referee_reading_failures": all_counts["cancellation_C_failures"],
            "configs_checked": all_counts["cancellation_configs_checked"],
            "contract_reading_failures_are_exactly_at_equality": (
                all_counts["cancellation_B_failures_below_x"] == 0
                and all_counts["cancellation_B_failures_at_equality"]
                == all_counts["cancellation_B_failures"]
            ),
        },
        "stalling_successor_can_host_another_round": {
            "verdict": "CONFIRMED"
            if all_counts["successor_can_sustain_another_round"] > 0
            else "NOT_OBSERVED",
            "cases": all_counts["successor_can_sustain_another_round"],
            "of_stalling_configs": all_counts["wall_successor_packet_can_stall"],
        },
        "progress_holds_exactly_on_the_L_alpha_equals_K_slice": {
            "verdict": "CONFIRMED"
            if (
                all_counts["wall_decrease_on_L_over_K_slice"] == 0
                and all_counts["wall_decrease_on_L_equal_K_slice"]
                == all_counts["configs_with_L_alpha_equal_K"]
                and all_counts["configs_with_L_alpha_equal_K"] > 0
            )
            else "REFUTED",
            "decreasing_on_L_equals_K": all_counts["wall_decrease_on_L_equal_K_slice"],
            "L_equals_K_configs": all_counts["configs_with_L_alpha_equal_K"],
            "decreasing_on_L_strictly_over_K": all_counts["wall_decrease_on_L_over_K_slice"],
            "L_strictly_over_K_configs": all_counts["configs_with_L_alpha_strictly_over_K"],
        },
        "SOUND_eq3_root_strictness_of_the_bare_star": {
            "verdict": "CONFIRMED"
            if all_counts["root_strictness_eq3_failures"] == 0
            else "REFUTED",
            "checks": all_counts["root_strictness_eq3_checks"],
            "failures": all_counts["root_strictness_eq3_failures"],
        },
        "successor_packet_can_be_root_held_again": {
            "verdict": "CONFIRMED"
            if all_counts["successor_packet_ever_root_held"] > 0
            else "NOT_OBSERVED",
            "cases": all_counts["successor_packet_ever_root_held"],
        },
    }

    payload = {
        "schema": "tlx-successor-model-check-v1",
        "generated": "2026-08-16",
        "self_test": st,
        "aggregate_counts": all_counts,
        "verdicts": verdicts,
        "first_witnesses": all_witnesses,
        "spaces": per_space,
        "total_seconds": round(total_time, 2),
        "provenance": {
            str(Path(__file__).resolve().relative_to(ROOT_DIR)): sha256(
                Path(__file__).resolve()
            )
        },
    }
    text = json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n"
    if args.output:
        args.output.write_text(text)
        print(f"wrote {args.output}")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
