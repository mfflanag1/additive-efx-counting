# Triangle Repeated-Edge Bottom-Pair Conversion Theorem

**Status:** cap-free, proof-checked computer-assisted theorem  
**Scope:** four additive agents, nine goods, a strict common favorite, and
universal owner-threshold failure  
**Not claimed:** complete EFX for all four-agent/nine-good instances or in
general

## Statement

Let the goods be

\[
\{f,a,b,c,r_1,r_2,r_3,r_4,r_5\}.
\]

Suppose all four agents strictly prefer the singleton good $f$ to every
other singleton. Suppose $\{a,b\}$ is bottom-two for agents 1 and 2,
$\{a,c\}$ is bottom-two for agent 3, and $\{b,c\}$ is bottom-two for agent
4. Assume also the universal owner-threshold-failure condition used in the
common-favorite reduction.

For any selected low pair $L=\{x,y\}$ and any perfect matching $M$ of the
six goods outside $\{f,x,y\}$, form the six conversions

\[
\{f,h\},\qquad e\cup\{\ell\},\qquad M\setminus\{e\},
\]

where $(h,\ell)$ is either $(x,y)$ or $(y,x)$ and $e\in M$. Across the three
selected low pairs there are 225 distinct converted partitions. Then at
least one of the following holds:

1. one of the three selected favorite-triple Hall cells is full; or
2. one of the 225 converted partitions supports a complete EFX allocation.

Equivalently, it is impossible to Hall-fail at least one perfect matching in
each selected cell while obstructing every converted partition.

## Basic explanation

The four selected bottom pairs form a triangle whose edge $\{a,b\}$ occurs
twice. The earlier three-agent-bottom theorem does not apply: no complete
pair has to be bottom-two for three agents. This theorem instead combines
the exchange menus from all three edges. If none of the three Hall cells
directly supplies EFX, one of those exchanges must.

The 225 conversions fall into only five types under goods relabeling, with
orbit sizes 30, 60, 60, 15, and 60.

## Symmetry reduction

The exact formula uses a 480-element relabeling group:

- swap the two agents sharing the repeated edge;
- permute the five goods outside $\{f,a,b,c\}$; and
- reflect the triangle by swapping $a$ with $b$ and agents 3 with 4.

Every finite relabeling orbit has a lexicographically maximum normalized
valuation matrix. Such a maximum satisfies the row, free-good-column, and
reflection inequalities used by the formula, so the symmetry constraints
are without loss of generality. The deterministic symmetry audit enumerates
all 480 actions, verifies preservation of the bottom pattern and the full
conversion family, and regression-checks the implemented lex leader on 128
deterministic profiles.

## Exact certification

The full 225-partition formula returned `unsat` in all of the following:

- Z3 with the cardinality encoding of universal threshold failure, in 406.2
  seconds;
- a fresh Z3 5.0 process replaying the frozen cardinal formula, in 234.2
  seconds;
- Z3 with the independent sorting-network threshold encoding, in 490.6
  seconds; and
- pinned cvc5 1.3.3 on the syntax-normalized sorting formula, in 241.8
  seconds.

cvc5 then emitted a 35,862,508-byte CPC proof with 408,508 proof-step lines.
The independent Ethos 0.2.3 checker returned `correct`. The aggregate audit
therefore labels the conditional theorem proof-checked.

Primary records:

- [cardinality Z3 result](efx49_bottom_pattern2_conversion_selector_symmetric_cardinal_session1.json);
- [fresh-process Z3 replay](efx49_bottom_pattern2_conversion_selector_symmetric_cardinal_external_z3.json);
- [sorting-network Z3 result](efx49_bottom_pattern2_conversion_selector_symmetric_sorting_session1.json);
- [independent cvc5 replay](efx49_bottom_pattern2_conversion_selector_symmetric_sorting_cvc5.json);
- [CPC/Ethos certificate](efx49_bottom_pattern2_conversion_selector_symmetric_sorting_cpc_ethos.json);
- [checked CPC proof](efx49_bottom_pattern2_conversion_selector_symmetric_sorting.cpc);
- [aggregate theorem audit](efx49_triangle_repeated_bottom_pair_conversion_audit.json);
- [480-action symmetry audit](efx49_triangle_repeated_pattern_symmetry_audit.json); and
- [five-orbit census](efx49_bottom_pattern2_conversion_orbit_audit.json).

## Consequence and remaining boundary

This closes one of the seven selected-bottom multiplicity patterns of type
$2+1+1$ inside the stated strict-common-favorite/universal-threshold branch.
Subsequent conversion theorems close the other six cases. Together with the
two proof-checked $2+2$ theorems, all nine repeated-edge patterns among the
20 residual multigraphs are now eliminated. The live census consists of the
eleven $1+1+1+1$ patterns; see
[the multiplicity gate](BOTTOM_PAIR_MULTIPLICITY_GATE.md).

This is a real structural advance, not a resolution of general additive EFX.
It does not by itself close the full four-agent/nine-good cell.
