# Disjoint Double-Bottom-Pair Conversion Theorem

**Status:** exact-real theorem with a cvc5 CPC certificate checked by Ethos  
**Scope:** four additive agents, nine goods, a strict common favorite, and
universal owner-threshold failure  
**Not claimed:** complete EFX for all four-agent/nine-good instances or in
general

## Statement

Let the goods be

\[
\{f,a,b,c,d,r_1,r_2,r_3,r_4\},
\]

and suppose all four agents strictly prefer the singleton good $f$ to every
other singleton. Suppose $\{a,b\}$ is bottom-two for agents 1 and 2 and the
disjoint pair $\{c,d\}$ is bottom-two for agents 3 and 4. Assume also the
universal owner-threshold-failure condition used in the common-favorite
reduction.

For a selected low pair $L=\{x,y\}$ and any perfect matching $M$ of the six
goods outside $\{f,x,y\}$, define its six conversions by choosing an
orientation $(h,\ell)\in\{(x,y),(y,x)\}$ and an edge $e\in M$:

\[
\{f,h\},\qquad e\cup\{\ell\},\qquad M\setminus\{e\}.
\]

Across both selected low pairs there are 180 distinct converted partitions.
Then at least one of the following holds:

1. one of the two selected favorite-triple Hall cells is full; or
2. one of the 180 converted partitions supports a complete EFX allocation.

Equivalently, it is impossible simultaneously to Hall-fail at least one
perfect matching in each selected cell and obstruct every converted
partition.

## Basic explanation

Each bottom pair offers two ways to pair one low good with the common
favorite and put the other low good into a triple. A matching of the other
six goods supplies three choices for that triple, hence six conversions.
The theorem says that disjoint repeated bottom pairs cannot defeat all of
these exchanges unless one of the original Hall cells was already strong
enough to finish the allocation directly.

Although there are 180 labeled partitions, the automorphism group of the
bottom-pair pattern has size 192 and reduces them to only four structural
types, of sizes 12, 96, 24, and 48. These four types are the appropriate
target for a concise analytic proof.

## Exact certification status

The same 72-partition sufficient CEGAR pool has returned `unsat` in:

- Z3 using the cardinality encoding of universal threshold failure;
- Z3 using the independent sorting-network encoding; and
- cvc5 1.3.3 on a syntax-normalized copy of the sorting formula.

The normalization only inserts `QF_LRA` and replaces unary sums by their
identical atom. cvc5 then produced a 35,222,160-byte CPC certificate with
434,968 proof-step lines. Ethos 0.2.3 checked the certificate and returned
`correct`. The hash-pinned aggregate audit therefore labels the conditional
lemma proof-checked.

A guarded Z3 assumption-core extraction has reduced the sufficient pool from
72 partitions to 19 and replayed the smaller sorting formula as `unsat`.
All 19 use $a$ or $b$ as the common-favorite partner—none uses $c$ or $d$—
and they meet the four conversion orbits in counts 6, 7, 4, and 2. This is a
stronger proof-mining statement: failure of the second disjoint Hall cell
forces a repair among a small menu attached to the first bottom pair. The
19-partition core is not yet claimed deletion-minimal, but it is independently
proof-checked: cvc5 returned `unsat`, produced a 22,393,447-byte CPC proof
with 280,729 proof-step lines, and Ethos returned `correct`.

Primary records:

- [cardinality Z3 result](efx49_bottom_pattern6_conversion_selector_cegar_session1.json);
- [sorting Z3 result](efx49_bottom_pattern6_conversion_selector_sorting_z3.json);
- [cvc5 result](efx49_bottom_pattern6_conversion_selector_sorting_cvc5.json);
- [normalization record](efx49_bottom_pattern6_conversion_selector_sorting_cvc5.normalization.json);
- [CPC/Ethos certificate record](efx49_bottom_pattern6_conversion_selector_sorting_cpc_ethos.json);
- [aggregate proof audit](efx49_disjoint_double_bottom_pair_conversion_audit.json);
- [four-orbit census](efx49_bottom_pattern6_conversion_orbit_audit.json);
- [19-partition Z3 core](efx49_bottom_pattern6_conversion_selector_sorting_core1.json);
- [core structure audit](efx49_bottom_pattern6_conversion_selector_sorting_core1_analysis.json);
- [compact-core CPC/Ethos record](efx49_bottom_pattern6_conversion_selector_sorting_core1_cpc_ethos.json).

## Consequence and remaining boundary

Within the strict-common-favorite/universal-threshold branch, this closes the
disjoint $2+2$ selected-bottom multigraph pattern. It does not close the
overlapping $2+2$ pattern, any of the seven
$2+1+1$ patterns, or any of the eleven all-distinct patterns. The general
additive-EFX problem therefore remains open.

The next proof-mining step is to shrink the 72-partition sufficient pool and
express its contradiction using the four conversion geometries above.
