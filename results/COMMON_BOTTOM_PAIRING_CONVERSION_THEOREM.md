# Common-Bottom Pairing Conversion Theorem

**Status:** cap-free, proof-checked computer-assisted theorem  
**Scope:** four additive agents, nine goods, a strict common favorite, and
universal owner-threshold failure  
**Not claimed:** the full distinct-representative lemma, complete EFX for all
four-agent instances, or general additive EFX

## Theorem

Let (f) be a strict favorite of all four agents. For each agent (i), sort
the other eight values as

\[
x_{i1}\ge\cdots\ge x_{i8},\qquad F_i=v_i(f),
\]

and assume the exact universal owner-threshold failure condition

\[
x_{i5}+x_{i6}+x_{i7}>F_i,
\qquad
x_{i3}+x_{i7}>F_i\ \text{or}\ x_{i4}+x_{i5}>F_i. \tag{1}
\]

Suppose two residual goods (a,b) are jointly bottom-two for every agent:

\[
\max\{v_i(a),v_i(b)\}
\le \min_{g\notin\{f,a,b\}}v_i(g)
\qquad(i=1,\ldots,4).                                  \tag{2}
\]

Fix any perfect pairing (M=\{E,P,Q\}) of the other six goods. Form the
favorite-triple Hall graph at threshold

\[
F_i+\max\{v_i(a),v_i(b)\}.
\]

Then one of the following holds:

1. (M) has a Hall matching to three distinct agents, so
   ({f,a,b}\mid E\mid P\mid Q) supports EFX; or
2. at least one of the six converted partitions
   
   \[
   \{f,h\}\mid (R\cup\{\ell\})\mid S\mid T,             \tag{3}
   \]
   
   supports EFX, where ((h,\ell)) is either ((a,b)) or ((b,a)),
   (R) is one edge of (M), and (S,T) are its other two edges.

The conclusion does not require a half-favorite system of distinct
representatives.

## Counting corollary

Let (H_{a,b}) be the number of Hall-valid perfect pairings in the
favorite-triple cell with lows (a,b), and let (P_f) be the total number
of EFX-supporting balanced partitions with (f) in a pair. Then

\[
P_f+H_{a,b}\ge15.                                      \tag{4}
\]

There are exactly 15 perfect pairings of six goods. For every Hall-failed
pairing, the theorem supplies a converted favorite-pair partition. These
repairs are distinct across different failed pairings: from (3), the
favorite partner identifies (h), the other common-low good identifies
(ell), the triple identifies (R), and the remaining pairs reconstruct
the original matching. This injects the (15-H_{a,b}) failed pairings into
the (P_f) favorite-pair repairs and proves (4).

In particular, if (P_f=0), then (H_{a,b}=15). The common-bottom cell is
full and the favorite-triple Hall characterization supplies complete EFX.
Thus the common-bottom subbranch of universal owner-threshold failure is
closed.

## Certification proof

Goods symmetry fixes

\[
(a,b)=(7,8),\qquad M=\{\{1,2\},\{3,4\},\{5,6\}\}.
\]

Hall failure has only three symmetry types:

1. one matching edge has zero neighboring agents;
2. two matching edges have at most one common neighboring agent; or
3. all three matching edges have at most two common neighboring agents.

For each type, the exact QF_LRA formula asserts strict positivity, the
strict common favorite, (1), all 48 bottom-order inequalities from (2), the
canonical Hall witness, and failure of every applicable conversion in (3).
Z3 returns `unsat` in all three canonical cells. The unsplit 21-witness
formula is also `unsat` under both the sorting-free cardinal encoding of
(1) and the independent sorting-network encoding. Pinned cvc5 1.3.3
independently returns `unsat` on the normalized sorting-network formula. It
also emits a 17,187,116-byte CPC proof with 218,320 proof steps; the separate
Ethos 0.2.3 checker accepts that proof as `correct`.

Primary records:

- [cardinal Z3 result](efx49_common_bottom_pairing_conversion_z3.json);
- [sorting-network Z3 result](efx49_common_bottom_pairing_conversion_sorting_z3.json);
- [independent cvc5 replay](efx49_common_bottom_pairing_conversion_sorting_cvc5.json);
- [CPC/Ethos certificate](efx49_common_bottom_pairing_conversion_sorting_cpc_ethos.json);
- [checked CPC proof](efx49_common_bottom_pairing_conversion_sorting.cpc);
- [zero-neighbor Hall cell](efx49_common_bottom_pairing_conversion_zero_neighbor_sorting_z3.json);
- [two-edge Hall cell](efx49_common_bottom_pairing_conversion_two_edges_one_neighbor_sorting_z3.json); and
- [three-edge Hall cell](efx49_common_bottom_pairing_conversion_three_edges_two_neighbors_sorting_z3.json).

The deterministic
[theorem audit](efx49_common_bottom_pairing_conversion_audit.json) pins both
encodings, the independent solver and proof-checker hashes, the three Hall
cells, and the 15-to-90 injection census.

The reconstructing generator is
[decide_common_bottom_pairing_conversion.py](../tracks/parkability/decide_common_bottom_pairing_conversion.py).

## Sharpness and discovery boundary

The theorem explains the sharp (3+12) profiles found by adversarial
search. Both have a common bottom pair, exactly three favorite-pair EFX
partitions, and exactly 12 Hall-valid pairings in that cell. Their three
Hall failures convert bijectively into their three favorite-pair repairs.
Profiles with zero favorite-pair repairs sit at the other equality case
(0+15).

The local zero-neighbor sufficient inequalities are stated separately in
[ZERO_NEIGHBOR_FAVORITE_TRIPLE_CONVERSION_LEMMA.md](ZERO_NEIGHBOR_FAVORITE_TRIPLE_CONVERSION_LEMMA.md).
The present theorem is stronger: it covers all three Hall-witness types and
needs only the bottom-two and universal-threshold assumptions.

## Strengthened successor and remaining gate

Proof mining subsequently showed that the fourth agent's 12 bottom-order
inequalities are unnecessary. The
[three-agent-bottom conversion theorem](THREE_AGENT_BOTTOM_PAIRING_CONVERSION_THEOREM.md)
proves the same conversion and counting conclusion whenever the pair is
bottom-two for any three agents.

The live branch is therefore smaller: no residual pair may be bottom-two
for three agents. After selecting one bottom pair per agent, only the
multiplicity patterns $2+2$, $2+1+1$, and $1+1+1+1$ remain. The next target
is a role-aware Hall-witness lemma for a pair shared by two agents.
