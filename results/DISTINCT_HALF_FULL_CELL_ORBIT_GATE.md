# Six-Orbit Conversion Gate

**Status:** six-orbit selection lemma refuted; proof-mining record  
**Scope:** four agents, nine goods, strict common favorite, universal owner-
threshold failure, and four distinct half-favorite representatives  
**Not claimed:** a proof of the full-cell dichotomy or general additive EFX

## Basic idea

Relabel the common favorite as (0), the four matched half-favorite
representatives as (R=\{1,2,3,4\}), and the four unmatched goods as
(U=\{5,6,7,8\}). A favorite-pair balanced partition has shape
(3+2+2+2), with (0) in one of the pairs.

Permuting (R) and (U) independently divides the 840 favorite-pair
partitions into only ten orbits. An orbit is determined by:

1. whether the partner of (0) lies in (R) or (U);
2. how many representative goods lie in the triple; and
3. whether each remaining pair has type (RR), (RU), or (UU).

The deletion-minimal cap-5 certificate contains 17 partitions, but all of
them lie in the following six orbits:

| favorite partner | representatives in triple | remaining pair types | orbit size |
|---|---:|---|---:|
| (R) | 0 | (RR,RU) | 48 |
| (R) | 1 | (RR,UU) | 72 |
| (R) | 1 | (RU,RU) | 144 |
| (R) | 2 | (RU,UU) | 144 |
| (U) | 2 | (RR,UU) | 72 |
| (U) | 2 | (RU,RU) | 144 |

Their union contains 624 partitions. This gives a symmetry-invariant
replacement for the arbitrary 17-template list.

## Refuted candidate lemma

> **Six-orbit selection candidate.** If no favorite-triple full Hall cell
> exists, then some partition in the six-orbit family supports EFX.

Together with the favorite-triple Hall characterization, this statement
would have closed the current universal-threshold distinct-representative
branch. It is false.

The four omitted orbits are


- (R|3|UU+UU);
- (U|0|RR+RR);
- (U|1|RR+RU); and
- (U|3|RU+UU).

Every omitted orbit is one or two shape-preserving exchanges from the
six-orbit family, but proximity alone does not preserve EFX feasibility.

## What the minimal core does and does not say

The 17-core is deletion-minimal only inside its own finite obstruction
formula. Its 17 deletion witnesses are not geometric knife edges: each has
between 301 and 550 EFX-supporting favorite-pair partitions in the full
840-partition universe. Three external partitions repair all 17 boundary
profiles.

The literal 17-template statement is also cap-specific. At value cap 6,
an exact branch-valid profile has no full Hall cell and obstructs all 17
templates, while still admitting 138 favorite-pair repairs and 2,544
labeled complete EFX allocations. Sixty of those repairs lie in the
six-orbit family. Thus the individual core cannot be promoted to a
real-valued lemma, but its symmetry closure survives this immediate test.

## Adversarial boundary and refutation

A corrected 10,000-step exact-integer annealing search, initialized from
the cap-6 core escape and the cap-20 full-cell boundary, reached a profile
with:

- no full favorite-triple Hall cell;
- 54 six-orbit repairs;
- 131 favorite-pair repairs in total; and
- a largest favorite-triple cell of size 12.

An unrestricted-real cardinal-encoding CEGAR run obstructed those 54
repairs. Its first model retained 276 new six-orbit repairs; after adding
32, the 86-cut continuation returned `unknown` at its configured
120-second limit. That run reached only a decision boundary.

A correctly scoped cap-20 CP-SAT search subsequently found the exact
profile

\[
\begin{pmatrix}
16&10&10&10&10&7&5&5&4\\
9&5&5&5&5&5&3&2&1\\
9&5&5&5&5&5&3&2&1\\
7&4&4&4&4&4&2&2&2
\end{pmatrix}.
\]

Literal replay verifies all branch assumptions, no full favorite-triple
Hall cell, and zero repairs in the six-orbit family. It has 45
favorite-pair repairs: 9 in orbit (U|0|RR+RR) and 36 in orbit
(U|1|RR+RU). It also has 900 labeled complete EFX allocations. Thus it
refutes both the six-orbit candidate and the separate, incomparable proposal that
the favorite can always be paired with one of the four representatives. Its
repair partners are goods 6, 7, and 8 only, fifteen times each, and none is
above half the favorite for any agent; rechoosing the half-favorite matching
does not rescue that proposal. It is not an EFX counterexample.

Adding both repair orbits to the original six gives a natural conservative
eight-orbit successor of 780 partitions; the single profile logically forces
only that at least one of the two be added. Equivalently, the eight-orbit
family contains exactly the favorite-pair partitions whose triple does not
consist of three representatives. Only (R|3|UU+UU) and (U|3|RU+UU),
totaling 60 partitions, remain outside it. Whether this eight-orbit selector
is valid remains open. A correctly scoped cap-20
CP-SAT formula obstructing all 780 partitions returned `UNKNOWN` after
473.93 seconds, 174,819 conflicts, and 2,840,120 branches without producing
a model. An exact-real cardinal CEGAR run began with the refuting profile's
45 repairs, found a new profile with 300 repairs outside that pool, added
128 of them, and returned `unknown` at the resulting 173-cut boundary after
a 300-second continuation. Direct exact-real Z3 replays of the full family and the
all-B and all-C rank cells separately returned `unknown` after 300, 180,
and 180 seconds. These are decision frontiers, not positive evidence or a
theorem.

A later cap-20 optimization run improved the hard positive boundary from 45
to 30 eight-orbit repairs. They split as 6 in (U|0|RR+RR) and 24 in
(U|1|RR+RU); no other favorite-pair repairs exist. The profile has no full
Hall cell and 684 complete EFX allocations. Its objective bound still allows
all 780 targets to be obstructed, so this is neither a selector refutation
nor a finite-cap theorem. See the
[Hall-split gate audit](efx49_distinct_half_rr_hall_split_gate_audit.json).
Independent later searches reduce the positive checkpoint to three repairs
without proving a floor; see the
[zero-neighbor conversion lemma](ZERO_NEIGHBOR_FAVORITE_TRIPLE_CONVERSION_LEMMA.md).

The exact-real artifacts are the
[full-family Z3 boundary](efx49_distinct_half_full_cell_real_eight_orbit_session1.json),
[all-B boundary](efx49_distinct_half_full_cell_real_eight_orbit_BBBB_session1.json),
and
[all-C boundary](efx49_distinct_half_full_cell_real_eight_orbit_CCCC_session1.json).
Pinned cvc5 1.3.3 independently timed out after 300 seconds on the normalized
[all-B](efx49_distinct_half_full_cell_real_eight_orbit_BBBB_session1.cvc5.json)
and
[all-C](efx49_distinct_half_full_cell_real_eight_orbit_CCCC_session1.cvc5.json)
formulas.

## Hall-witness split after the orbit compression

The cap-6 deletion boundaries contain 588 low-pair Hall cells. Exact replay
finds minimum witness size one in 572 cells, size two in 9, and size three in
7. In particular, all 126 cells whose low pair consists of two
representatives have a zero-neighbor edge. This observation yields an
exhaustive split for a hypothetical no-full-cell/no-eight-orbit profile:
either all six representative-pair cells have a zero-neighbor edge, or some
representative-pair cell does not. In the second case simultaneous relabeling
of agents and representatives fixes the exceptional cell as pair 1,2, while
favorite-value agent ordering must be dropped.

Direct exact-real formulas for both exhaustive branches returned `unknown`
after 300 seconds. The stronger all-28-cell singleton branch also returned
`unknown` in Z3, and pinned cvc5 1.3.3 produced no verdict after 300 seconds.
A cap-20 CP-SAT replay of that stronger branch also returned `UNKNOWN` after
600.15 seconds without a model.
A separate local shortcut is false: exact rational profiles in both terminal
orbits have no full Hall cell and no EFX repair reachable by one
representative/low-good swap, although many globally re-paired six-orbit
repairs remain. See
[the representative-pair split record](DISTINCT_HALF_RR_HALL_SPLIT_GATE.md)
and its deterministic
[cap-6 witness census](efx49_distinct_half_full_cell_cap6_hall_witness_census.json).

The sharpest tested local successor uses all eight-orbit states within two
single-good swaps of a terminal state, exactly 138 targets in either terminal
orbit. At cap 5 this implication is now a dual-verified bounded theorem:
after symmetry reduction, CP-SAT and Z3 QF_LIA both close all seven canonical
terminal/matching cells without assuming the absence of a full Hall cell.
This is a proof-mining result rather than a new
existence range, because the stronger full-cell theorem is already certified
through cap 6. The unrestricted radius-two implication is false at cap 20. See the
[terminal-exchange gate](DISTINCT_HALF_TERMINAL_EXCHANGE_GATE.md).
The decisive profile blocks the union of all 138 local states and has no full
Hall cell, while retaining 290 global eight-orbit repairs, all at distance
three or four. This retires the local route without touching the 780-state
selector or the exhaustive Hall-witness split.

A sequence of guarded searches improved the sharp no-full-cell boundary
from 45 to 30 and then to three eight-orbit repairs. The three states form
one perfect-pairing cell and are the conversions of the missing matchings in
a 12-of-15 Hall cell. The optimizer bound still permits zero, and each
profile is positive EFX rather than a counterexample. Hall-witness mining
also gives a cleaner exhaustive split based on whether one unmatched edge is
a zero-neighbor witness in all six representative-pair cells. See the
[common-unmatched witness gate](DISTINCT_HALF_COMMON_UU_SPLIT_GATE.md).

The hash-pinned semantic replay is
[efx49_distinct_half_full_cell_orbit_gate_audit.json](efx49_distinct_half_full_cell_orbit_gate_audit.json).
Its primary inputs are the
[17-core](efx49_distinct_half_full_cell_cap5_minimal_core.json),
[cap-6 escape](efx49_distinct_half_full_cell_integer_core17_cap6.json),
[annealing boundary](efx49_distinct_half_six_orbit_anneal_session1.json),
the [exact-real CEGAR boundary](efx49_distinct_half_six_orbit_cegar_session1.json),
the [refuting profile](efx49_distinct_half_six_orbit_refutation_profile.json),
the [eight-orbit cap-20 boundary](efx49_distinct_half_full_cell_eight_orbit_cpsat_cap20_session1.json),
and the [eight-orbit exact-real CEGAR boundary](efx49_distinct_half_eight_orbit_cegar_session2.json).

## Trust boundary

The ten-orbit census and every quoted repair count are recomputed
semantically from literal EFX feasibility. The cap-6 escape and both search
profiles are positive EFX instances, not counterexamples to existence. The
CEGAR endpoint is `unknown`, while the later finite profile is a decisive
counterexample to the six-orbit selection statement. A proof of general EFX
still needs a broader cap-free exchange or Hall-witness argument.
