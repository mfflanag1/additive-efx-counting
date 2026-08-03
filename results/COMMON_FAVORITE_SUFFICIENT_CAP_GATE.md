# Common-Favorite Sufficient-Cap Gate at \(4\times9\)

**Status:** open computational gate  
**Scope:** four agents, nine goods, one strict common favorite  
**Decision cap:** \(K_9=19{,}683\)  
**Not claimed:** EFX existence in this cell or in general

## What would be sufficient

Let good \(0\) be every agent's strict favorite. Consider the 2,226
unlabeled partitions that either

1. have shape \(3+2+2+2\); or
2. isolate \(\{0\}\) as a singleton.

If any such partition has a perfect matching in its agent--bundle
EFX-feasibility graph, it supports a complete EFX allocation. Therefore an
infeasibility proof for a master requiring all 2,226 partitions to be
matching-deficient would prove EFX existence in the residual
common-favorite cell.

This structural family need not contain an EFX allocation for profiles
already covered by another theorem. The intended conclusion combines the
master with the following safe reductions:

- a universal-minimum good reduces to the certified \(4\times8\) theorem;
- a peelable agent--good pair reduces to the three-agent theorem; and
- a profile with at most three valuation types is already known to admit
  EFX.

## Why the finite cap is complete

If a positive-additive counterexample exists at \(4\times9\), the
[small-integer counterexample bound](SMALL_INTEGER_COUNTEREXAMPLE_BOUND.md)
gives one with all item values in

\[
\{1,\ldots,19{,}683\}.
\]

EFX nonexistence is an open finite system of strict linear inequalities.
Consequently a counterexample can also be perturbed so that every row has
distinct item values and a unique favorite, without changing any selected
allocation violation. A genuine counterexample cannot fall into any of the
safe reduction classes above.

Thus the residual bounded master may soundly require:

- no universal-minimum good;
- no peelable agent--good pair;
- pairwise distinct valuation rows;
- distinct item values within every row; and
- strict favorite pattern \((0,0,0,0)\).

An independently checked infeasibility verdict at the sufficient cap would
settle this favorite orbit for arbitrary positive real values. A timeout
does not.

## Learned structural pool

The cap-13 dual theorem uses 446 structural partitions. The first
unrestricted-real frontier profile avoids all 446 but has 104 literal EFX
allocations on 39 new favorite-singleton partitions. Importing all 39 grows
the real structural boundary to 485 partitions.

At the full integer cap, three uncut CEGAR sessions learned 326 additional
partitions:

| Session | Pool before | Pool after | Exact models |
|---|---:|---:|---:|
| 1 | 485 | 661 | 5 |
| 2 | 661 | 719 | 5 |
| 3 | 719 | 811 | 5 |

Every one of the 15 models still supports a target partition. Every model
also has within-row item ties; most additionally have a universal minimum,
a peelable pair, or repeated valuation rows. They are useful repair
generators but do not lie in the fully generic residual.

Primary artifacts:

- [`efx49_common_favorite_structural_integer19683_pool.json`](efx49_common_favorite_structural_integer19683_pool.json);
- [`efx49_common_favorite_structural_integer19683_session1.json`](efx49_common_favorite_structural_integer19683_session1.json);
- [`efx49_common_favorite_structural_integer19683_session2.json`](efx49_common_favorite_structural_integer19683_session2.json); and
- [`efx49_common_favorite_structural_integer19683_session3.json`](efx49_common_favorite_structural_integer19683_session3.json).

## Current residual verdicts

The first matching-clause residual solve used the 719-partition boundary and
returned `MASTER_UNKNOWN` after 900 seconds:
[`efx49_common_favorite_structural_integer19683_residual_session1.json`](efx49_common_favorite_structural_integer19683_residual_session1.json).

Matching-clause and Hall-selector replays on separate frozen copies of the
stronger 811-partition pool both returned `MASTER_UNKNOWN` after 900
seconds. The complete learning chain, model replays, pool reconstruction,
proto hashes, and dual timeouts are frozen in
[`efx49_common_favorite_sufficient_cap_audit.json`](efx49_common_favorite_sufficient_cap_audit.json).
The audit status is a verified research frontier, not a theorem verdict.

## Exact universal-threshold compression

For an owner with favorite value \(F\), sort the eight residual values as
\(x_1\ge\cdots\ge x_8\). Universal owner-threshold failure is exactly

\[
x_5+x_6+x_7>F
\quad\text{and}\quad
\bigl(x_3+x_7>F\ \text{or}\ x_4+x_5>F\bigr).
\]

The proof is
[`OWNER_THRESHOLD_SHAPE_ENVELOPE.md`](OWNER_THRESHOLD_SHAPE_ENVELOPE.md).
It replaces all 966 residual-partition clauses per owner by a sorting
network and two rank conditions. On the same 427-partition learned pool,
the compact CP-SAT formula uses 5,140 comparison variables rather than
6,012 and no longer carries 3,864 owner-partition clauses. It still
returned `MASTER_UNKNOWN` after 60 seconds:
[`efx49_common_universal_threshold_envelope_balanced_learned_session1.json`](efx49_common_universal_threshold_envelope_balanced_learned_session1.json).
The direct 427- and 1,260-partition encodings both returned unknown after
300 seconds:
[`efx49_common_universal_threshold_balanced_learned_session1.json`](efx49_common_universal_threshold_balanced_learned_session1.json)
and
[`efx49_common_universal_threshold_balanced_full1260_session1.json`](efx49_common_universal_threshold_balanced_full1260_session1.json).

Hall's theorem splits this exact subcase into a proved common-three branch
and a remaining branch with four distinct half-favorite representatives.
After normalizing one such matching to goods \(1,2,3,4\), the compact
full-cap master over all 1,260 balanced partitions again returned unknown
after 300 seconds:
[`efx49_distinct_half_universal_threshold_envelope_full1260_session1.json`](efx49_distinct_half_universal_threshold_envelope_full1260_session1.json).
The cap-14 replay and its representative-stabilized variant also returned
unknown after 120 seconds. These are focused frontier formulas, not
positive or negative verdicts.

## Human conversion target

The fixed 446-partition cap-13 list is refuted over arbitrary reals, and the
extreme \(6+1+1+1\) residual family is not a cover. The surviving analytic
statement must quantify over the three-agent EFX remainder:

> either a balanced EFX matching exists, or some owner of the common
> favorite and some three-agent EFX allocation of the remaining goods
> satisfy the owner's threshold.

The exact owner threshold is proved in
[COMMON_FAVORITE_SINGLETON_REDUCTION.md](COMMON_FAVORITE_SINGLETON_REDUCTION.md).
The current solver pool is evidence for candidate repair motifs, not a
substitute for this selection theorem.
