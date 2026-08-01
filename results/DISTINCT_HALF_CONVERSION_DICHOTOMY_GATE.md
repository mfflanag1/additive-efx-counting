# Distinct-Half Conversion Dichotomy Gate

**Status:** open conditional Hall selection lemma  
**Closed this campaign:** owner-floor existence, common-three branch,
favorite-pair rank conjecture, common-low and one-defect conversions  
**Not claimed:** the universal-threshold subcase or general additive EFX

## Exact remaining statement

Assume four agents with nonnegative additive valuations over nine goods
have:

1. a strict common favorite \(f\);
2. universal failure of the favorite-singleton owner threshold; and
3. a saturating half-favorite matching.

The common-three alternative of the half-favorite dichotomy is already
closed. In the four-distinct-representative alternative, prove:

> Either some balanced partition with \(f\) in a pair has a perfect
> EFX-feasibility matching, or there are two residual goods \(a,b\) and a
> perfect matching \(P,Q,R\) of the remaining six goods such that the three
> pairs can be matched to three distinct agents using edges
> \[
> v_i(S)\ge F_i+\max\{v_i(a),v_i(b)\}. \tag{1}
> \]

The second alternative is exactly a favorite-triple EFX allocation by the
[favorite-triple Hall characterization](FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md).
For fixed \(a,b\), failure has only three forms: one pair has no accepting
agent, two pairs have at most one accepting agent between them, or all three
pairs have at most two accepting agents between them.

This statement is the exact balanced conversion gate. A stronger
proof-mining target asks for a matching in which every pair satisfies (1)
for every agent. That observer-independent target is sufficient by the
[common-low favorite-triple lemma](COMMON_LOW_FAVORITE_TRIPLE_LEMMA.md), but
is not known to be necessary.

## Local conversion already proved

[ONE_DEFECT_FAVORITE_TRIPLE_CONVERSION_LEMMA.md](ONE_DEFECT_FAVORITE_TRIPLE_CONVERSION_LEMMA.md)
proves an optional stronger local repair into a favorite-pair allocation.
For existence, no comparison condition or exchange is needed: if two pairs
are safe for every agent and the third has at most one rejecter, the three
pairs satisfy Hall directly. Thus it suffices to force this two-safe,
one-almost-safe motif.

The literal regression audit checks 1,251 qualifying constructions:
[efx49_one_defect_favorite_triple_conversion_audit.json](efx49_one_defect_favorite_triple_conversion_audit.json).

## Why the favorite-pair-only target is closed

The strict profile

\[
\begin{pmatrix}
100&1&2&55&69&59&96&77&95\\
100&5&17&73&69&62&55&68&53\\
100&8&1&48&73&69&61&67&65\\
100&8&1&55&79&90&71&66&82
\end{pmatrix}
\]

has zero EFX-supporting partitions among all 840 favorite-pair states. It
still has 324 complete EFX allocations, all with favorite triple
\(\{f,1,2\}\). The independent all-partition and all-allocation census is
[efx49_distinct_half_favorite_pair_rank_boundary_audit.json](efx49_distinct_half_favorite_pair_rank_boundary_audit.json).

The observed exchange is exact. On the harder three-repair boundary, all
observer-independent repairs use the same forced safe edge. Weakening that
edge enough to give it one rejecter creates exactly the corresponding
favorite-pair EFX states, while the original favorite-triple partitions
remain EFX by the Hall characterization.

The reverse one-form target is also false. The strict, item-distinct profile

\[
\begin{pmatrix}
100&82&87&69&40&34&39&58&44\\
100&54&97&69&68&36&71&52&26\\
100&2&70&89&35&65&27&56&61\\
100&31&73&99&60&66&26&64&22
\end{pmatrix}
\]

has zero EFX-supporting partitions among all 420 favorite-triple states,
but 356 favorite-pair EFX partitions and 1,906 complete EFX allocations.
Its exhaustive audit is
[efx49_distinct_half_favorite_triple_boundary_audit.json](efx49_distinct_half_favorite_triple_boundary_audit.json).
Thus neither side can be discarded: the combined dichotomy is the first
surviving balanced normal form.

## Adversarial and exact decision boundary

The following attacks have not resolved the stronger
observer-independent dichotomy:

- three independent 5,000-step integer searches at favorite normalization
  100 reduced the all-safe repair family to three but not zero;
- three more searches at normalization 1,000 produced the same
  three-repair boundary;
- full exact formulas containing all 840 favorite-pair obstructions and all
  420 negated favorite-triple repairs returned `unknown` under Z3 and cvc5;
- an independent CP-SAT encoding returned `UNKNOWN` at caps 20 and 100;
- adding the empirically observed common-bottom-pair cell improved
  propagation but also returned `UNKNOWN` at cap 20.

These are solver boundaries, not positive evidence for either the stronger
dichotomy or the exact Hall gate. The executable
workbenches are:

- [run_distinct_half_conversion_dichotomy_cegar.py](../tracks/parkability/run_distinct_half_conversion_dichotomy_cegar.py);
- [decide_distinct_half_conversion_dichotomy_cpsat.py](../tracks/parkability/decide_distinct_half_conversion_dichotomy_cpsat.py); and
- [anneal_distinct_half_rank_augmentation.py](../tracks/parkability/anneal_distinct_half_rank_augmentation.py).

A deterministic diverse replay now isolates a smaller exact-real boundary:
24 favorite-pair cuts and 9 observer-independent triple-repair cuts. The
favorite-pair pool has exactly three cuts for each possible partner of
\(f\) and contains 22 distinct triple bundles. Its three exact trace models
have no common-low repair but retain 533, 256, and 257 unblocked
favorite-pair EFX partitions. Reloading the exact 24/9 pool and solving for
300 seconds returned `unknown` by timeout. The replay and solver endpoint
are frozen in
[efx49_distinct_half_conversion_dichotomy_pool_analysis.json](efx49_distinct_half_conversion_dichotomy_pool_analysis.json)
and
[efx49_distinct_half_conversion_dichotomy_cegar_session5.json](efx49_distinct_half_conversion_dichotomy_cegar_session5.json).

The latest 20,000-step exact-census search sharpens the former three-repair
boundary to one repair. It found

\[
\begin{pmatrix}
100&6&1&85&59&66&66&86&55\\
100&10&1&53&86&59&45&50&64\\
100&1&5&54&61&59&89&72&61\\
100&1&3&55&62&58&80&75&59
\end{pmatrix}.
\]

This profile satisfies the exact branch assumptions, has no EFX partition
among the 840 favorite-pair states, and has exactly one
observer-independent repair:

\[
\{0,1,2\}\mid\{3,5\}\mid\{4,6\}\mid\{7,8\}.
\]

Literal enumeration finds 252 complete EFX allocations, all of shape
\(3+2+2+2\) with favorite triple \(\{0,1,2\}\). The independent audit is
[efx49_distinct_half_conversion_dichotomy_boundary_audit.json](efx49_distinct_half_conversion_dichotomy_boundary_audit.json).
This is a positive knife edge, not a dichotomy counterexample and not an
additive-EFX counterexample.

The 15 exact Hall repairs have additional structure: they are all 15
pairings of the same favorite triple \(\{0,1,2\}\). Goods \(1,2\) are a
common bottom pair, and agents \(0,2,3\) accept every pair of the other six
goods at their respective favorite-triple thresholds. The cap-free
[three-observer full favorite-triple cell lemma](THREE_OBSERVER_FULL_TRIPLE_CELL_LEMMA.md)
shows that this scalar condition forces all 15 pairings. The earlier
zero-favorite-pair boundary has exactly the same structure; the dual-profile
audit is
[efx49_three_observer_full_triple_cell_audit.json](efx49_three_observer_full_triple_cell_audit.json).

Two further exact-census searches totaling 30,000 steps did not reduce the
15 balanced repairs, and a targeted 5,000-step search did not break the full
cell. These are finite falsification attempts, not evidence sufficient to
promote the conditional full-cell statement to a theorem.

## Next analytic unit

For fixed \(a,b\), label each edge of the six-good complete graph by the set
of agents satisfying (1). A chosen perfect matching works exactly when its
three edge labels satisfy Hall. The next proof should assume that every
perfect matching has one of the three small Hall obstructions above and map
those witnesses to a Hall obstruction in every favorite-pair
EFX-feasibility graph. The universal four-set condition, pair-degree
alternative, and half-favorite SDR must then rule out their coexistence.

The former intersection graph of edges safe for all four agents is still a
useful sufficient subgraph, and Tutte describes its failure, but it discards
too much agent-specific information. The exact object is the edge-labeled
six-vertex graph plus the three-pair Hall test.

A sharper sufficient target now retains exactly the information observed on
the tight boundaries. Find \(a,b\) and two agents who accept every residual
edge. Form the graph of edges rejected by both remaining agents. If that
graph has no perfect matching, then all 15 residual pairings satisfy Hall;
this is the
[two-core/Tutte corollary](FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md).
The remaining selection question is whether simultaneous favorite-pair
obstruction forces such a low pair and two-agent core.

On six residual goods the required Tutte obstruction has an exact
three-case form: the outsider-rejection graph has at least two odd components,
deleting one vertex leaves at least three odd components, or two vertices
cover every rejected edge. The proof and exhaustive \(2^{15}\)-graph audit
are in
[FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md](FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md).
This is the current human-proof case split.

The number two is sharp for this route. A strict item-distinct boundary has
no favorite-pair EFX state and has all 15 favorite-triple pairings in one
cell, but no low pair for which three agents accept every residual edge.
Exactly two agents accept every edge, while their outsider-rejection graph
has one edge and hence no perfect matching. The literal 1,260-partition and
\(4^9\)-allocation replay is
[efx49_distinct_half_two_core_boundary_audit.json](efx49_distinct_half_two_core_boundary_audit.json).

A tempting six-cell shortcut is false. Even after fixing the half-favorite
representatives to goods (1,2,3,4), the low pair need not be two of those
representatives and the core need not be the complementary two agents. A
strict boundary has zero favorite-pair states and exactly one unrestricted
two-core witness, at lows (5,6) and core agents (1,3). Its 288 literal
complete EFX allocations confirm that this retires only the canonical
strengthening, not the unrestricted target. Audit:
[efx49_distinct_half_canonical_two_core_boundary_audit.json](efx49_distinct_half_canonical_two_core_boundary_audit.json).

The negation of this two-core selection target has now been encoded three
ways. Exact-real matching-clause CEGAR produced five models with 598, 319,
228, 283, and 279 unblocked favorite-pair EFX partitions and reached a
40-cut iteration boundary. The Hall-selector replay produced three models
with 598, 270, and 383 repairs, then returned `unknown` on its 24-cut
boundary at 60 seconds. Independently, the full bounded CP-SAT formula at
integer cap 20 returned `UNKNOWN` after 300 seconds, 177,756 conflicts, and
2,240,178 branches. A fourth exact-real solve started from the 55 partitions
not covered by the union of five diverse seed profiles; it returned
`unknown` after 120 seconds before producing a first model. Reifying the
1,680 pair-acceptance predicates improved propagation enough to produce one
exact profile with 265 unblocked favorite-pair states, then returned
`unknown` on the resulting 183-cut formula. The exact replay is
[efx49_distinct_half_two_core_decision_boundary_audit.json](efx49_distinct_half_two_core_decision_boundary_audit.json).
These are computational boundaries, not a theorem and not a refutation.

Bounded CP-SAT CEGAR has now approached the conditional boundary more
closely. At cap 20 its exact repair counts fell from 398 to 143 to 20 before
the 331-cut formula returned **UNKNOWN**, including a final 900-second
continuation with no further model. The last profile is

\[
\begin{pmatrix}
15&8&11&9&10&11&11&1&1\\
15&8&12&9&11&7&12&1&1\\
14&10&6&8&11&10&8&1&1\\
14&8&8&10&8&9&6&1&1
\end{pmatrix}.
\]

It has exactly 20 favorite-pair EFX partitions, all pairing \(f\) with good
7 or 8, and 15 favorite-triple EFX partitions, all in the single full cell
\(\{f,7,8\}\). Literal enumeration finds 293 complete EFX allocations. It
has no two-core witness, no three-of-four robust low pair, and best
three-observer slack \(-1\). These facts are exactly replayed in
[efx49_distinct_half_two_core_decision_boundary_audit.json](efx49_distinct_half_two_core_decision_boundary_audit.json).

This creates a higher-leverage intermediate target:

> **Full favorite-triple Hall-cell dichotomy.** If all 840 favorite-pair
> states are Hall-obstructed, some \(a,b\) make all 15 perfect pairings of
> the other six goods satisfy the favorite-triple Hall test.

The exact gate needs only one pairing, the full-cell target asks for all 15,
and the two-core/Tutte condition is a sufficient explanation for a full
cell. The cap-20 profile proves that a full cell can survive after the
two-core explanation has disappeared. It does not refute the conditional
two-core claim because its 20 favorite-pair repairs remain. All audited
zero-favorite-pair boundaries have a full cell. The next exact decision run
should therefore forbid favorite-pair EFX and forbid every full cell; an
independently certified UNSAT result would close this universal-threshold
branch, while a model would retire the intermediate target without touching
the exact one-pairing gate.

The first such exact-real CEGAR run is now frozen. Starting from the same
55-partition complement frontier, it found one profile with no full Hall
cell but 289 unblocked favorite-pair EFX partitions. That profile has 304
balanced EFX partitions in total, 15 favorite-triple repairs spread across
cells of maximum size 12, and 1,381 labeled complete EFX allocations. The
next 183-cut solve hit its configured 180-second solver limit; the two-solve
run took 337.7 seconds in total and returned **UNKNOWN**. Exact replay and
both-polarity encoding controls are
[efx49_distinct_half_full_cell_decision_boundary_audit.json](efx49_distinct_half_full_cell_decision_boundary_audit.json)
and
[efx49_distinct_half_full_cell_encoding_audit.json](efx49_distinct_half_full_cell_encoding_audit.json).
This is a solver boundary, not a counterexample to the conditional
dichotomy and not a theorem.

There are now proof-certified bounded closures through cap 6. At cap 5, a
deletion-minimal 17-partition threshold-CNF core has a checked DRAT proof.
At cap 6, CP-SAT closes a 401-partition pool, QF_LIA independently closes
its 359-partition core and shrinks it to 175, and threshold CNF reduces to a
deletion-minimal 21-partition core. Its 1,145,090-clause formula is `UNSAT`
in CaDiCaL, with a binary DRAT proof independently accepted by `drat-trim`.
Consequently the stated branch has a complete EFX allocation throughout
both finite domains. This does not extend by scaling to arbitrary ratios
and does not settle the exact-real gate. Artifacts and trust boundaries:
[DISTINCT_HALF_FULL_CELL_CAP5_THEOREM.md](DISTINCT_HALF_FULL_CELL_CAP5_THEOREM.md)
and
[DISTINCT_HALF_FULL_CELL_CAP6_THEOREM.md](DISTINCT_HALF_FULL_CELL_CAP6_THEOREM.md).

The deletion-minimal certificate now gives a more precise analytic target.
Relabel the four matched half-favorite goods as representatives and the
other four residual goods as unmatched. The 840 favorite-pair partitions
form ten symmetry orbits; all 17 certificate partitions lie in six of
them, whose union has 624 partitions. The 17 literal templates are not
cap-free—a cap-6 profile obstructs all of them while retaining 138
favorite-pair repairs—but 60 repairs of that profile remain in the
six-orbit family. That symmetry closure is nevertheless false: an exact
cap-20 profile has no full Hall cell, zero six-orbit repairs, 45 repairs in
two omitted orbits, and 900 labeled complete EFX allocations. The refuted
selection lemma and its semantic audit are in
[DISTINCT_HALF_FULL_CELL_ORBIT_GATE.md](DISTINCT_HALF_FULL_CELL_ORBIT_GATE.md).

A separate cap-20 CP-SAT CEGAR run found a no-full-cell profile with 357
favorite-pair repairs. After adding all 357 repairs to the 55-partition
complement seed, the 412-cut continuation remained **UNKNOWN** after 600
seconds. The trace profile has no favorite-triple EFX partition and 3,563
labeled complete EFX allocations. The same decision-boundary audit replays
the trace, its resume source, the 21-megabyte model hash, and its exact
allocation census. This is a bounded solver boundary only.

The one-repair boundary shows that a proof of the stronger sufficient
statement cannot average over a large repair family: it must force even a
unique residual pairing. The six-orbit and representative-partner
shortcuts are now retired. A natural conservative next compression is the
eight-orbit family obtained by adding both repair orbits—equivalently, all
favorite-pair states whose triple is not all representatives. Its first
780-partition cap-20 test is
`UNKNOWN`, and an exact-real cardinal CEGAR reached a 173-cut `unknown`
boundary. The full 840-partition dichotomy remains the fallback. The
ultimate, logically weaker theorem needs only one
edge-labeled Hall pairing. Whether simultaneous obstruction of all 840
favorite-pair states forces one all-safe repair is a possible stronger
analytic stepping stone, not the current decision target.

The still more compressed three-observer scalar route
\(x_5+x_6\ge F+x_7\), as well as the edge-local demand that every residual
pair have three acceptors, is refuted by the strict two-core boundary above.
Neither may be used as the remaining selection claim.
