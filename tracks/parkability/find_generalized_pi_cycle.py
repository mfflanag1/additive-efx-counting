#!/usr/bin/env python3
"""Find canonical generalized BCFF PI cycles in an exact rational profile.

For a common-safe desired bundle A aimed at base target X_j, the canonical
generalized edge has incoming H=A-X_j and releases S=X_j-A. Any nonminimal
desired bundle can be shrunk, decreasing H and increasing release, so
inclusion-minimal desired bundles suffice for PI-cycle existence.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

from .run_fixed_u_full_packet_terminal_cegar import BASE, GOODS, OWNERS


GOOD_INDEX = {good: index for index, good in enumerate(GOODS)}


def mask(goods):
    result = 0
    for good in goods:
        result |= 1 << GOOD_INDEX[good]
    return result


def goods_of(bits):
    return [good for index, good in enumerate(GOODS) if bits & (1 << index)]


def total(values, observer, bits):
    return sum(
        (values[observer][good] for index, good in enumerate(GOODS)
         if bits & (1 << index)),
        Fraction(),
    )


def tail(values, observer, bits):
    entries = [
        values[observer][good] for index, good in enumerate(GOODS)
        if bits & (1 << index)
    ]
    return sum(entries, Fraction()) - min(entries, default=Fraction())


def minimal_desired_masks(values, source):
    candidates = []
    for bits in range(1, 1 << len(GOODS)):
        if total(values, source, bits) <= 1:
            continue
        if any(tail(values, observer, bits) > 1 for observer in OWNERS):
            continue
        candidates.append(bits)
    candidate_set = set(candidates)
    minimal = []
    for bits in sorted(candidates, key=int.bit_count):
        # It suffices to test immediate deletions recursively: if any proper
        # desired subset exists, one inclusion-minimal desired subset exists.
        if any((sub & bits) == sub for sub in minimal):
            continue
        minimal.append(bits)
    return tuple(minimal)


def edge_options(values, base=BASE):
    base_mask = {owner: mask(base[owner]) for owner in (*OWNERS, "charity")}
    minimal = {source: minimal_desired_masks(values, source) for source in OWNERS}
    options = {}
    for source in OWNERS:
        for target in OWNERS:
            rows = []
            target_mask = base_mask[target]
            for desired in minimal[source]:
                incoming = desired & ~target_mask
                released = target_mask & ~desired
                rows.append((incoming, released, desired))
            options[source, target] = tuple(rows)
    return minimal, options


def canonical_cycles():
    for length in range(1, len(OWNERS) + 1):
        for subset in itertools.combinations(OWNERS, length):
            anchor = min(subset)
            for tail_order in itertools.permutations(
                    tuple(owner for owner in subset if owner != anchor)):
                yield (anchor, *tail_order)


def find_cycles(values, base=BASE, maximum=None):
    base_mask = {owner: mask(base[owner]) for owner in (*OWNERS, "charity")}
    charity_mask = base_mask["charity"]
    minimal, options = edge_options(values, base)
    witnesses = []
    for cycle in canonical_cycles():
        edge_pairs = tuple(
            (cycle[index], cycle[(index + 1) % len(cycle)])
            for index in range(len(cycle))
        )
        rows = [options[pair] for pair in edge_pairs]
        if any(not row for row in rows):
            continue

        def search(position, chosen, incoming_union):
            if position == len(rows):
                released_union = 0
                for incoming, released, desired in chosen:
                    released_union |= released
                if incoming_union & ~(charity_mask | released_union):
                    return None
                return tuple(chosen)
            for option in rows[position]:
                incoming, _, _ = option
                if incoming & incoming_union:
                    continue
                found = search(position + 1, (*chosen, option), incoming_union | incoming)
                if found is not None:
                    return found
            return None

        selected = search(0, (), 0)
        if selected is not None:
            witnesses.append({
                "cycle": list(cycle),
                "edges": [
                    {
                        "source": source,
                        "target": target,
                        "incoming": goods_of(option[0]),
                        "released": goods_of(option[1]),
                        "desired_core": goods_of(option[2]),
                    }
                    for (source, target), option in zip(edge_pairs, selected, strict=True)
                ],
            })
            if maximum is not None and len(witnesses) >= maximum:
                break
    return tuple(witnesses), minimal


def find_cycle(values, base=BASE):
    witnesses, minimal = find_cycles(values, base, maximum=1)
    return (witnesses[0] if witnesses else None), minimal


def find_closed_core_families(values, base=BASE, maximum=None):
    """Enumerate closed disjoint minimal-core families directly.

    By the closed disjoint-core characterization these are exactly canonical
    generalized PI witnesses, modulo an arbitrary cyclic target ordering.
    """
    minimal = {source: minimal_desired_masks(values, source) for source in OWNERS}
    base_masks = {owner: mask(base[owner]) for owner in (*OWNERS, "charity")}
    witnesses = []
    seen = set()

    for size in range(1, len(OWNERS) + 1):
        for subset in itertools.combinations(OWNERS, size):
            allowed = base_masks["charity"]
            for owner in subset:
                allowed |= base_masks[owner]
            choices = {
                source: tuple(bits for bits in minimal[source] if not bits & ~allowed)
                for source in subset
            }
            if any(not choices[source] for source in subset):
                continue
            order = tuple(sorted(subset, key=lambda source: len(choices[source])))

            def search(position, used, selected):
                if maximum is not None and len(witnesses) >= maximum:
                    return
                if position == len(order):
                    signature = tuple(sorted(selected.items()))
                    if signature in seen:
                        return
                    seen.add(signature)
                    cycle = tuple(subset)
                    successor = {
                        cycle[index]: cycle[(index + 1) % len(cycle)]
                        for index in range(len(cycle))
                    }
                    edges = []
                    for source in cycle:
                        target = successor[source]
                        desired = selected[source]
                        target_mask = base_masks[target]
                        edges.append({
                            "source": source,
                            "target": target,
                            "incoming": goods_of(desired & ~target_mask),
                            "released": goods_of(target_mask & ~desired),
                            "desired_core": goods_of(desired),
                        })
                    witnesses.append({"cycle": list(cycle), "edges": edges})
                    return
                source = order[position]
                for desired in choices[source]:
                    if desired & used:
                        continue
                    search(position + 1, used | desired, {**selected, source: desired})
                    if maximum is not None and len(witnesses) >= maximum:
                        return

            search(0, 0, {})
            if maximum is not None and len(witnesses) >= maximum:
                return tuple(witnesses), minimal
    return tuple(witnesses), minimal


def run(source: Path):
    payload = json.loads(source.read_text())
    values = {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in payload["values"].items()
    }
    witness, minimal = find_cycle(values)
    return {
        "schema": "generalized-bcff-pi-cycle-search-v1",
        "status": "GENERALIZED_PI_CYCLE_FOUND" if witness else "NO_CANONICAL_PI_CYCLE_FOUND",
        "source": f"results/{source.name}",
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "minimal_common_safe_desired_counts": {
            owner: len(rows) for owner, rows in minimal.items()
        },
        "witness": witness,
        "claim_boundary": (
            "exact canonical generalized BCFF PI-cycle search over all "
            "inclusion-minimal common-safe desired bundles in the declared "
            "twelve-good base. A found cycle refutes generalized PI-freeness. "
            "No found cycle is not a proof of full saturation or global maximality."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "counts": result["minimal_common_safe_desired_counts"],
        "witness": result["witness"],
    }, indent=2))


if __name__ == "__main__":
    main()
