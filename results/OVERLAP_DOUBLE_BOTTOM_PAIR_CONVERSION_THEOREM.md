# Overlapping Double-Bottom-Pair Conversion Theorem

**Status:** cap-free, proof-checked computer-assisted theorem  
**Scope:** four additive agents, nine goods, a strict common favorite, and
universal owner-threshold failure  
**Not claimed:** complete EFX for all four-agent/nine-good instances or in
general

## Statement

Let the goods be

\[
\{f,s,a,b,r_1,r_2,r_3,r_4,r_5\}.
\]

Suppose all four agents strictly prefer the singleton good $f$ to every
other singleton. Suppose $\{s,a\}$ is bottom-two for agents 1 and 2, while
$\{s,b\}$ is bottom-two for agents 3 and 4. Assume also the universal
owner-threshold-failure condition used in the common-favorite reduction.

For either selected low pair $L=\{x,y\}$ and any perfect matching $M$ of
the six goods outside $\{f,x,y\}$, form the six conversions

\[
\{f,h\},\qquad e\cup\{\ell\},\qquad M\setminus\{e\},
\]

where $(h,\ell)$ is either $(x,y)$ or $(y,x)$ and $e\in M$. Across the two
overlapping low pairs there are 165 distinct converted partitions. Then at
least one of the following holds:

1. one of the two selected favorite-triple Hall cells is full; or
2. one of the 165 converted partitions supports a complete EFX allocation.

Equivalently, it is impossible to Hall-fail at least one perfect matching in
each selected cell while obstructing every converted partition.

## Basic explanation

The shared good $s$ is bottom-two for all four agents, but neither complete
low pair need be bottom-two for three agents. This is exactly why the earlier
six-conversion local theorem does not apply. The present theorem combines all
matchings from both overlapping cells: if neither cell directly yields EFX by
Hall's theorem, at least one of the resulting exchanges must do so.

The 165 labeled conversions have only four structural types under the
240-element goods automorphism group, with orbit sizes 15, 60, 30, and 60.
Four independently found positive boundary profiles have exactly three
favorite-pair repairs, all in the final size-60 orbit. Thus the conclusion is
attained with a small but nonzero repair set; the theorem is not an artifact
of a loose search boundary.

## Symmetry reduction

The exact formula uses a 960-element relabeling group:

- swap the two agents sharing each low pair;
- permute the five goods outside $\{f,s,a,b\}$; and
- exchange the two mirrored low-pair/agent blocks.

Every finite relabeling orbit has a lexicographically maximum normalized
valuation matrix. Such a maximum satisfies the row, free-good-column, and
side-swap inequalities used by the formula, so the symmetry constraints are
without loss of generality. The deterministic symmetry audit enumerates all
960 actions, verifies preservation of the bottom pattern and the complete
conversion family, and canonicalizes all four exact three-repair boundaries.

## Exact certification

The full 165-partition formula returned `unsat` in all of the following:

- Z3 with the cardinality encoding of universal threshold failure, in 543.8
  seconds;
- a fresh Z3 process replaying the frozen cardinal formula, in 753.2 seconds;
- Z3 with the independent sorting-network threshold encoding, in 697.6
  seconds; and
- pinned cvc5 1.3.3 on the syntax-normalized sorting formula, in 672.4
  seconds.

cvc5 then emitted a 68,745,739-byte CPC proof with 767,596 proof-step lines.
The independent Ethos 0.2.3 checker returned `correct`. The aggregate audit
therefore labels the conditional theorem proof-checked.

A guarded Z3 extraction reduced the 165 obstructions to a 97-partition
assumption core, meeting the four conversion orbits in counts 6, 12, 28, and
51. Its unguarded 1,200-second replay timed out, so this core is retained only
as proof-mining evidence; it is not part of the theorem's trust chain. The
full proof-checked formula remains the primary certificate.

Primary records:

- [cardinality Z3 result](efx49_bottom_pattern0_conversion_selector_symmetric_cardinal_session1.json);
- [fresh-process Z3 replay](efx49_bottom_pattern0_conversion_selector_symmetric_cardinal_external_z3.json);
- [sorting-network Z3 result](efx49_bottom_pattern0_conversion_selector_symmetric_sorting_session1.json);
- [independent cvc5 replay](efx49_bottom_pattern0_conversion_selector_symmetric_sorting_cvc5.json);
- [CPC/Ethos certificate](efx49_bottom_pattern0_conversion_selector_symmetric_sorting_cpc_ethos.json);
- [checked CPC proof](efx49_bottom_pattern0_conversion_selector_symmetric_sorting.cpc);
- [aggregate theorem audit](efx49_overlap_double_bottom_pair_conversion_audit.json);
- [960-action symmetry audit](efx49_overlap22_pattern_symmetry_audit.json);
- [four-orbit census](efx49_bottom_pattern0_conversion_orbit_audit.json);
- [guarded 97-partition core](efx49_bottom_pattern0_conversion_selector_symmetric_cardinal_core1.json); and
- [core orbit analysis](efx49_bottom_pattern0_conversion_selector_symmetric_cardinal_core1_analysis.json).

## Consequence and remaining boundary

Together with the proof-checked disjoint double-bottom theorem, this closes
both selected-bottom multiplicity patterns of type $2+2$ inside the stated
strict-common-favorite/universal-threshold branch. The 20-pattern residual
census is reduced to the seven $2+1+1$ patterns and the eleven
$1+1+1+1$ patterns.

Subsequent work closes the triangle-with-doubled-edge $2+1+1$ pattern as
well, leaving six $2+1+1$ patterns; see
[the triangle repeated-edge theorem](TRIANGLE_REPEATED_BOTTOM_PAIR_CONVERSION_THEOREM.md).

This is a real structural advance, not a resolution of general additive EFX.
It does not by itself close the full four-agent/nine-good cell.
