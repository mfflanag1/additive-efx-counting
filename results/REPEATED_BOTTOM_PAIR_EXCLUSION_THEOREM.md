# Repeated Bottom-Pair Exclusion Theorem

**Status:** cap-free, proof-checked computer-assisted theorem  
**Scope:** four additive agents, nine goods, a strict common favorite, and
universal owner-threshold failure  
**Not claimed:** complete EFX for all four-agent/nine-good instances or in
general

## Statement

Let four agents have positive additive valuations over nine goods. Suppose
all agents strictly prefer one singleton good $f$ to every other singleton,
and suppose the universal owner-threshold-failure condition used in the
common-favorite reduction holds. For each agent choose one bottom-two pair
among the eight residual goods.

If some chosen pair occurs for at least two agents, then at least one of the
following holds:

1. a selected favorite-triple Hall cell is full; or
2. a favorite-pair conversion supports a complete EFX allocation.

Consequently, in the residual branch with no favorite-pair EFX allocation
and no selected full Hall cell, the four chosen bottom pairs must be pairwise
distinct.

## Basic explanation

The chosen bottom pairs form a four-edge multigraph on the residual goods.
A pair used by three or four agents is handled by the earlier
three-agent-bottom conversion theorem. If the largest multiplicity is two,
every repeated-edge graph has one of only two multiplicity signatures:

- $2+2$: two different pairs are each selected twice; or
- $2+1+1$: one pair is selected twice and two other pairs once.

Both $2+2$ graphs were already proof-checked. The exhaustive multigraph
census shows that $2+1+1$ has exactly seven unlabeled graph patterns. The
complete conversion family closes every one of those seven. Therefore no
repeated selected bottom pair survives the branch assumptions.

This is the concise structural output of the case campaign: the live
problem is no longer “control repeated bottom pairs.” It is the genuinely
all-distinct representative case.

## The seven $2+1+1$ cases

Using the canonical indices in the exhaustive 20-pattern census, the seven
cases are 1, 2, 3, 4, 5, 7, and 8. Their complete conversion-family sizes
are 228, 225, 240, 240, 255, 255, and 270. Each case has all of the
following:

- an independently enumerated relabeling group and conversion-orbit census;
- an exact-real cardinal-threshold Z3 `unsat` result;
- a fresh-process Z3 5.0 replay of the frozen cardinal formula;
- an independent sorting-network threshold formula proved `unsat` by Z3;
- a syntax-only normalized QF_LRA formula proved `unsat` by pinned cvc5
  1.3.3; and
- a cvc5 CPC derivation accepted as `correct` by Ethos 0.2.3.

Across the seven cases, the checked CPC files contain 217,425,021 bytes and
2,512,561 proof-step lines. These totals are descriptive; the theorem rests
on the seven individually hash-pinned proofs and the exhaustive graph
census, not on a pooled heuristic run.

## Exact audit chain

The class-level audit is
[efx49_all_repeated_bottom_pair_conversions_audit.json](efx49_all_repeated_bottom_pair_conversions_audit.json).
It verifies that:

- the independent census has exactly 20 canonical patterns, including
  exactly seven of signature $2+1+1$;
- the supplied theorem records have exactly those seven pattern indices;
- every record has the expected conversion-family size and bottom-pair
  pattern;
- all four solver verdict fields are `unsat`; and
- all seven proof records report Ethos `correct`, with nonempty proof hashes,
  byte counts, and step counts.

The two $2+2$ components are documented separately in
[the disjoint theorem](DISJOINT_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md) and
[the overlapping theorem](OVERLAP_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md).
The multiplicity census is
[efx49_bottom_pair_pattern_census_audit.json](efx49_bottom_pair_pattern_census_audit.json).

## Consequence and remaining boundary

Inside the strict-common-favorite/universal-threshold branch, all nine
repeated-edge patterns are now eliminated: two of type $2+2$ and seven of
type $2+1+1$. The finite structural frontier consists exactly of the eleven
$1+1+1+1$ patterns.

This does not close the mixed-threshold branch, the complete
four-agent/nine-good case, or general additive EFX. Its highest-leverage
next use is analytic: replace the seven certified cases by a human proof
that a repeated bottom pair forces one successful conversion, then attack
the all-distinct Hall-witness geometry.
