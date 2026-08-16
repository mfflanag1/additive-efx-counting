# Path Repeated-Edge Bottom-Pair Conversion Theorems

**Status:** two cap-free, proof-checked computer-assisted theorems  
**Scope:** four additive agents, nine goods, a strict common favorite, and
universal owner-threshold failure  
**Not claimed:** complete EFX for all four-agent/nine-good instances or in
general

## Statements

Let all four agents strictly prefer singleton good $f$ to every other
singleton, and assume the universal owner-threshold-failure condition used
in the common-favorite reduction. The following two selected-bottom-pair
patterns are considered:

1. **Central-edge path:** $\{a,b\},\{a,b\},\{a,c\},\{b,d\}$.
2. **End-edge path:** $\{a,b\},\{a,b\},\{a,c\},\{c,d\}$.

For any distinct selected low pair $L=\{x,y\}$ and any perfect matching $M$
of the six goods outside $\{f,x,y\}$, form the six conversions

\[
\{f,h\},\qquad e\cup\{\ell\},\qquad M\setminus\{e\},
\]

where $(h,\ell)$ is either $(x,y)$ or $(y,x)$ and $e\in M$. Each path pattern
has 240 distinct converted partitions. For either pattern, at least one of
the following holds:

1. one of the three selected favorite-triple Hall cells is full; or
2. one of its 240 converted partitions supports a complete EFX allocation.

Equivalently, in either path cell it is impossible to Hall-fail at least one
perfect matching for every selected pair while obstructing all conversions.

## Basic explanation

The repeated edge and the two singly selected edges form a four-vertex path.
The two theorems distinguish whether the repeated edge lies in the center or
at an end. Neither case has a pair ranked bottom-two by three agents, so the
earlier three-agent-bottom theorem is unavailable. Nevertheless, the three
local exchange menus collectively cover the residual obstruction in both
path geometries.

## Symmetry and exact certification

The central-edge path has a 96-action formula symmetry group and 13
conversion orbits. The end-edge path has a 48-action formula symmetry group
and 26 conversion orbits. Independent finite-group audits enumerate every
action, verify preservation of the bottom-pattern cell and the full
conversion family, and test the implemented lex leaders on 128 deterministic
orbit maxima.

| Check | Central-edge path | End-edge path |
|---|---:|---:|
| cardinal Z3 | `unsat`, 584.2s | `unsat`, 442.9s |
| fresh Z3 5.0 | `unsat`, 429.9s | `unsat`, 315.8s |
| sorting-network Z3 | `unsat`, 396.4s | `unsat`, 369.3s |
| pinned cvc5 1.3.3 | `unsat`, 420.0s | `unsat`, 304.8s |
| CPC proof bytes | 55,452,414 | 27,069,738 |
| CPC proof-step lines | 586,111 | 333,221 |
| Ethos 0.2.3 | `correct` | `correct` |

Primary aggregate records:

- [central-edge path theorem audit](efx49_bottom_pattern3_conversion_audit.json);
- [end-edge path theorem audit](efx49_bottom_pattern4_conversion_audit.json);
- [central-edge 96-action symmetry audit](efx49_path_repeated_pattern_symmetry_audit.json);
- [end-edge 48-action symmetry audit](efx49_end_repeated_path_pattern_symmetry_audit.json);
- [central-edge conversion-orbit census](efx49_bottom_pattern3_conversion_orbit_audit.json); and
- [end-edge conversion-orbit census](efx49_bottom_pattern4_conversion_orbit_audit.json).

The aggregate audits hash-pin the two Z3 formulas, cvc5-normalized formula,
CPC proof, independent solver records, symmetry census, and conversion-orbit
census.

## Consequence and remaining boundary

Together with the other conversion theorems, these results close all seven
$2+1+1$ selected-bottom-pair patterns inside the stated
strict-common-favorite/universal-threshold branch. Adding the two previously
closed $2+2$ patterns eliminates all nine repeated-edge patterns among the
20 residual multigraphs. The live census is the eleven $1+1+1+1$ patterns.

These are conditional structural theorems, not a resolution of general
additive EFX or even the complete four-agent/nine-good case.
