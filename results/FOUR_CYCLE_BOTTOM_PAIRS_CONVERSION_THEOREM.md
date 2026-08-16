# Four-Cycle Bottom Pairs Conversion Theorem

**Status:** cap-free, proof-checked computer-assisted theorem  
**Scope:** four additive agents, nine goods, a strict common favorite, and
universal owner-threshold failure  
**Not claimed:** the other nine unresolved all-distinct patterns, the full
four-agent/nine-good case, or general additive EFX

## Statement

Let four agents have positive additive valuations over nine goods. Suppose
all four strictly prefer one singleton good $f$ to every other singleton,
and suppose the universal owner-threshold-failure condition used in the
common-favorite reduction holds. Suppose that, after relabeling, the four
agents have selected bottom-two pairs

\[
\{1,2\},\qquad \{1,3\},\qquad \{2,4\},\qquad \{3,4\}.
\]

Then at least one of the following holds:

1. a selected favorite-triple Hall cell is full; or
2. a favorite-pair conversion generated from one of the four selected
   bottom pairs supports a complete EFX allocation.

Consequently the four-cycle selected-bottom-pair geometry cannot occur in
the residual branch with no favorite-pair EFX allocation and no selected
full Hall cell.

## Basic explanation

The four selected pairs are the edges of a cycle on four residual goods.
For each edge, pair the other six residual goods in every possible way and
perform the natural low-good/favorite conversion. Removing duplicates gives
300 balanced partitions. The exact formula asks for a branch-valid profile
that obstructs all 300. Such a profile does not exist.

## Certification

The geometry has a 192-action relabeling group. Its 300 conversions split
into five exact orbits of sizes 12, 48, 48, 96, and 96. The complete formula
returned `unsat` under:

- Z3 with the cardinal threshold encoding;
- Z3 with a separate sorting-network threshold encoding;
- a fresh Z3 5.0 replay of the frozen cardinal formula; and
- pinned cvc5 1.3.3 on the normalized sorting formula.

cvc5 emitted a 58,694,950-byte CPC proof with 696,642 proof-step lines.
Ethos 0.2.3 checked the derivation and returned `correct`.

The hash-pinned aggregate is
[efx49_bottom_pattern14_conversion_audit.json](efx49_bottom_pattern14_conversion_audit.json).
The independent structural records are the
[symmetry audit](efx49_four_cycle_pattern_symmetry_audit.json) and
[conversion-orbit audit](efx49_bottom_pattern14_conversion_orbit_audit.json).
The checked proof is
[efx49_bottom_pattern14_conversion_selector_symmetric_sorting.cpc](efx49_bottom_pattern14_conversion_selector_symmetric_sorting.cpc).

## Remaining boundary

Together with the four-disconnected-pairs theorem, this closes two of the
eleven all-distinct patterns. Nine all-distinct patterns remain. Closing
them would finish the strict-common-favorite/universal-threshold conversion
gate at $(4,9)$, but the mixed-threshold branch and general additive EFX
would remain open.
