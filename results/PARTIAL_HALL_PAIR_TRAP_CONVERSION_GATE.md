# Pair-trap conversion gate after cap-free extraction

**Status (2026-08-02):** active breakthrough gate. Pair extraction is proved;
conversion of the forced trap is not.

## Established input

The
[owner-minimum Hall-pair extraction theorem](PARTIAL_HALL_OWNER_MINIMUM_EXTRACTION_THEOREM.md)
shows that every eligible four-agent one-floater EFX state has either:

1. an EFX completion after direct insertion or one selected owner-minimum
   transfer; or
2. a selected complete candidate whose acceptability graph has two agents and
   exactly one combined neighbor.

The theorem is cap-free in goods and valuation magnitudes. Thus the only
remaining completion route is to convert case 2 into a better eligible partial
state and contradict a well-founded selector.

## First conversion is exactly false

The simplest conversion allocates the old floater $f$, removes one selected
owner-minimum good $g_s$ as the new floater, and arbitrarily rematches the four
resulting bundles. The exact positive $4\times9$ profile
[`partial_hall_owner_minimum_substitution_counterexample.json`](partial_hall_owner_minimum_substitution_counterexample.json)
refutes the claim that this family must contain a normalized-utilitarian
improvement.

Its independent
[audit](partial_hall_owner_minimum_substitution_counterexample_audit.json)
verifies:

- the base is EFX and every agent dominates the floater;
- all 52 direct/owner-minimum complete candidates have no EFX perfect
  matching;
- 144 pair witnesses occur, including the designated first hard Hall orbit;
- only two substitution allocations are eligible and neither improves; and
- the integer profile is an exact realization of the symbolic SAT model.

This refutes one-substitution conversion, not global normalized-utilitarian
selection and not complete EFX.

## The next exchange is pinned down

The counterexample has 1,235 eligible one-floater EFX states. Its base is not
globally normalized-utilitarian maximal: 965 states have larger potential.
The nearest higher state keeps floater 8 and changes exactly two old goods:

\[
(\{0,1\},\{2,3\},\{4,5\},\{6,7\};8)
\longrightarrow
(\{0,7\},\{2,3\},\{4,5\},\{1,6\};8).
\]

Thus goods 1 and 7 are swapped between bundles 0 and 3. The exact normalized
potential gain is

\[
\frac{11}{1072}>0.
\]

This establishes the minimum conversion radius in that profile: one
owner-minimum substitution is insufficient, while a two-good swap succeeds.

## Exchange hierarchy exposed by exact local models

The two-good-swap target is itself too narrow as a local statement. Three
exact positive $4\times9$ profiles now separate successive exchange menus.
These profiles deliberately retain selected EFX completions, so they refute
only propositions that use the designated pair trap without the global
``all selected completions fail'' hypothesis.

1. With all 12 swaps between bundle 3 and bundles 0, 1, and 2 blocked, the
   nearest higher eligible state is an ordinary one-good transfer.
2. After adding all 24 one-good transfer partitions, only 12 higher eligible
   states remain. Every one contains the same three-cycle on bundles
   $0,2,3$, with one of the two goods of bundle 0 chosen as its first edge.
3. After blocking those two three-cycles, the nearest higher eligible state
   changes three ownership positions: an owner-minimum good becomes the new
   floater, the old floater enters a second bundle, and one good moves onward
   to a third bundle. The surviving motif is therefore a floater-coupled
   augmenting path.

The exact profiles and audits are:

- [`partial_hall_owner_minimum_swap_star_local_profile.json`](partial_hall_owner_minimum_swap_star_local_profile.json)
  and its [audit](partial_hall_owner_minimum_swap_star_local_profile_audit.json);
- [`partial_hall_owner_minimum_transfer_swap_star_local_profile.json`](partial_hall_owner_minimum_transfer_swap_star_local_profile.json)
  and its [audit](partial_hall_owner_minimum_transfer_swap_star_local_profile_audit.json);
- [`partial_hall_owner_minimum_transfer_cycle023_swap_star_local_profile.json`](partial_hall_owner_minimum_transfer_cycle023_swap_star_local_profile.json)
  and its [audit](partial_hall_owner_minimum_transfer_cycle023_swap_star_local_profile_audit.json).

This hierarchy aligns the new pair-extraction theorem with the existing
[connected augmenting-exchange target](PARTIAL_HALL_CONNECTED_EXCHANGE_TARGET.md),
transfer-component decomposition, and dependency-cycle lemmas. The credible
conversion object is a connected exchange path or cycle, not a fixed swap.

## Live theorem target

Let $X$ be normalized-utilitarian-maximal among all eligible four-agent
one-floater EFX allocations. Apply owner-minimum pair extraction. If no
selected complete candidate has an EFX matching, use its two-agent/one-neighbor
trap to construct either:

1. an eligible improving connected exchange; or
2. a directed cycle of failed exchange components whose EFX-wall inequalities
   and normalized-potential gains contradict selector maximality.

The goods must be selected by their structural roles—owner minimum, violating
residual witness, host, source, destination, and common neighbor—not by fixed
indices or a finite valuation corpus. The exact hierarchy above shows that
paths through the floater vertex and ordinary bundle cycles are both
indispensable.

## Computational proof route

The arbitrary-bundle conversion master is generated by
[`decide_partial_hall_owner_minimum_substitution_conversion.py`](../tracks/parkability/decide_partial_hall_owner_minimum_substitution_conversion.py).
For the two-good-per-bundle size cell, the unbranched Z3 and cvc5 masters both
time out. Branching by the 58 Hall-witness symmetry orbits closes orbit 0 from
the pair assertion alone. Orbit 1 is feasible and the exact maximality CEGAR
learns 13 substitution blockers before producing the counterexample above.

The strengthened exact-two-goods master now contains owner-minimum
substitutions, all 24 one-good transfers, the 12 structurally selected swaps,
and the two mined three-cycles. Seventy-six exact maximality blockers are
known. For the first hard Hall orbit, the unbranched formula, all three
first-level trap-witness branches, and the first branch split through three
inequalities all return `UNKNOWN (TIMEOUT)`. The specialized QF_LRA solver
and an all-selected-minimum valuation chamber do not change that boundary.
These are not theorem verdicts.

The next proof step is analytic rather than another monolithic solve: combine
the designated pair trap with the cap-free transfer-component dependency
cycle, and derive the weighted wall inequality that either terminates an
augmenting path in an eligible improving state or contradicts normalized
potential maximality. A positive result must cover all Hall role orbits and
bundle-size patterns; a fixed-cell UNSAT result is not the target.

The later cap-80 integer run and its tied-minimum correction are frozen in
[PARTIAL_HALL_CONVERSION_CHECKPOINT_20260802.md](PARTIAL_HALL_CONVERSION_CHECKPOINT_20260802.md).
In particular, the first apparent integer counterexample is invalid for the
full owner-minimum family because an alternate tied minimum completes. The
repaired unique-minimum branch remains `UNKNOWN` with 93 learned blockers.
