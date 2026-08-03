# Star Repeated-Edge Bottom-Pair Conversion Theorem

**Status:** cap-free, proof-checked computer-assisted theorem  
**Scope:** four additive agents, nine goods, a strict common favorite, and
universal owner-threshold failure  
**Not claimed:** complete EFX for all four-agent/nine-good instances or in
general

## Statement

Let the goods be

\[
\{f,a,b,c,d,r_1,r_2,r_3,r_4\}.
\]

Suppose all four agents strictly prefer the singleton good $f$ to every
other singleton. Suppose $\{a,b\}$ is bottom-two for agents 1 and 2,
$\{a,c\}$ is bottom-two for agent 3, and $\{a,d\}$ is bottom-two for agent
4. Assume also the universal owner-threshold-failure condition used in the
common-favorite reduction.

For any selected low pair $L=\{x,y\}$ and any perfect matching $M$ of the
six goods outside $\{f,x,y\}$, form the six conversions

\[
\{f,h\},\qquad e\cup\{\ell\},\qquad M\setminus\{e\},
\]

where $(h,\ell)$ is either $(x,y)$ or $(y,x)$ and $e\in M$. Across the three
selected low pairs there are 228 distinct converted partitions. Then at
least one of the following holds:

1. one of the three selected favorite-triple Hall cells is full; or
2. one of the 228 converted partitions supports a complete EFX allocation.

Equivalently, it is impossible to Hall-fail at least one perfect matching in
each selected cell while obstructing every converted partition.

## Basic explanation

The four selected bottom pairs form a three-leaf star centered at $a$, with
the edge $\{a,b\}$ selected by two agents. No pair is bottom-two for three
agents, so the earlier three-agent-bottom theorem does not apply. This
theorem combines the exchange menus from the three distinct star edges: if
none of their Hall cells directly supplies EFX, at least one exchange must.

The 228 conversions split into 16 types under goods relabeling, with orbit
sizes 12, 3, 24, 12, 24, 6, 12, 3, 24, 6, 12, 6, 24, 24, 12, and 24.

## Symmetry reduction

The exact formula uses a 96-element relabeling group:

- swap the two agents sharing the repeated edge;
- permute the four goods outside $\{f,a,b,c,d\}$; and
- swap leaves $c$ and $d$ together with agents 3 and 4.

Every finite relabeling orbit has a lexicographically maximum normalized
valuation matrix. Such a maximum satisfies the row, free-good-column, and
leaf-reflection inequalities used by the formula, so the symmetry
constraints are without loss of generality. The deterministic symmetry
audit enumerates all 96 actions, verifies preservation of the bottom pattern
and full conversion family, and regression-checks the implemented lex leader
on 128 deterministic profiles.

## Exact certification

The full 228-partition formula returned `unsat` in all of the following:

- Z3 with the cardinality encoding of universal threshold failure, in 900.8
  seconds;
- a fresh Z3 5.0 process replaying the frozen cardinal formula, in 309.9
  seconds;
- Z3 with the independent sorting-network threshold encoding, in 325.8
  seconds; and
- pinned cvc5 1.3.3 on the syntax-normalized sorting formula, in 482.9
  seconds.

cvc5 then emitted a 51,302,181-byte CPC proof with 602,783 proof-step lines.
The independent Ethos 0.2.3 checker returned `correct`. The aggregate audit
therefore labels the conditional theorem proof-checked.

Primary records:

- [cardinality Z3 result](efx49_bottom_pattern1_conversion_selector_symmetric_cardinal_session1.json);
- [fresh-process Z3 replay](efx49_bottom_pattern1_conversion_selector_symmetric_cardinal_external_z3.json);
- [sorting-network Z3 result](efx49_bottom_pattern1_conversion_selector_symmetric_sorting_session1.json);
- [independent cvc5 replay](efx49_bottom_pattern1_conversion_selector_symmetric_sorting_cvc5.json);
- [CPC/Ethos certificate](efx49_bottom_pattern1_conversion_selector_symmetric_sorting_cpc_ethos.json);
- [checked CPC proof](efx49_bottom_pattern1_conversion_selector_symmetric_sorting.cpc);
- [aggregate theorem audit](efx49_star_repeated_bottom_pair_conversion_audit.json);
- [96-action symmetry audit](efx49_star_repeated_pattern_symmetry_audit.json); and
- [16-orbit census](efx49_bottom_pattern1_conversion_orbit_audit.json).

## Consequence and remaining boundary

This closes a second of the seven selected-bottom multiplicity patterns of
type $2+1+1$ inside the stated strict-common-favorite/universal-threshold
branch. Subsequent conversion theorems close the other five cases. Together
with the two proof-checked $2+2$ theorems, all nine repeated-edge patterns
among the 20 residual multigraphs are now eliminated. The live census
consists of the eleven $1+1+1+1$ patterns; see
[the multiplicity gate](BOTTOM_PAIR_MULTIPLICITY_GATE.md).

This is a real structural advance, not a resolution of general additive EFX.
It does not by itself close the full four-agent/nine-good cell.
