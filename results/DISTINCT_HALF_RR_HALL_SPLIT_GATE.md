# Representative-Pair Hall-Witness Split

**Status:** exact exhaustive decomposition; both cap-free decision branches
remain open  
**Scope:** four agents, nine goods, strict common favorite, universal owner-
threshold failure, and four distinct half-favorite representatives  
**Not claimed:** the eight-orbit selector, complete EFX for four agents, or
general additive EFX

## The split

Write the common favorite as (0), the matched half-favorite goods as
(R=\{1,2,3,4\}), and the remaining goods as (U=\{5,6,7,8\}). For a
residual low pair (L), call a disjoint residual edge (e) a *singleton
Hall witness* when every agent rejects it at the favorite-triple threshold:

\[
v_i(e)<v_i(0)+\max_{\ell\in L}v_i(\ell)
\qquad\text{for every agent }i.
\]

Such an edge has no neighbor in the three-edge Hall graph, so every perfect
pairing containing it fails. In particular, it certifies that (L) is not a
full favorite-triple Hall cell.

Every hypothetical profile with no full Hall cell and no EFX partition in
the 780-partition eight-orbit family lies in exactly one of two branches:

1. **RR-singleton:** all six pairs (L\in\binom{R}{2}) have a singleton
   Hall witness;
2. **RR-nonsingleton:** at least one representative pair has no singleton
   witness.

In the second branch, simultaneous relabeling of agents and their matched
representatives sends the exceptional pair to (\{1,2\}). Agent ordering by
favorite value must then be omitted, because it is not compatible with
fixing an arbitrary exceptional pair. The four unmatched goods may still be
ordered by agent 0. Thus a single canonical (L=\{1,2\}) formula covers the
whole second branch.

This is an exhaustive case split, not a proof that either branch is empty.

## Why this split was selected

The verified cap-6 deletion-minimal core has 21 boundary profiles and 588
low-pair cells. Exact replay finds:

- 572 cells whose minimum Hall witness has size one;
- 9 whose minimum witness has size two; and
- 7 whose minimum witness has size three.

All 126 representative-pair cells in that corpus have a singleton witness.
Eight of the 21 profiles use singleton witnesses in all 28 cells. Across all
8,607 failed pairings, 8,255 already have a size-one witness. These are
descriptive facts about the bounded certificate, not cap-free regularities.
The deterministic census is
[efx49_distinct_half_full_cell_cap6_hall_witness_census.json](efx49_distinct_half_full_cell_cap6_hall_witness_census.json).

## Compression inside the RR-singleton branch

The six representative-pair cells are usually not six unrelated witnesses
in the certified cap-6 boundary data. In 17 of the 21 profiles, one fixed
pair of unrepresented goods is rejected by every agent at the threshold for
all six cells. Equivalently, those six existential witnesses have an edge
cover of size one. Among the other four profiles, one has minimum cover size
two and three have minimum cover size three. Across all 21 profiles the
minimum-cover histogram is therefore (17,1,3) at sizes (1,2,3).

The size-one pattern has an exact cap-free compression. For an
unrepresented edge \(e\) and agent \(i\), let \(s_i\) be the second-smallest of
the four representative values. Then \(e\) is a singleton witness for every
representative low pair exactly when

\[
v_i(e)<F_i+s_i \qquad\text{for every agent }i.
\]

Indeed, the smallest value of
\(\max\{v_i(r),v_i(r')\}\) over the six representative pairs is precisely
\(s_i\). This replaces 24 agent-cell inequalities by four order-statistic
inequalities. It suggests a two-stage analytic split:

1. a **common-UU branch**, where one unrepresented edge satisfies these
   four inequalities; and
2. a **dispersed branch**, where all six RR cells have singleton witnesses
   but no unrepresented edge witnesses all six.

This is a compression of the proof search, not a cap-free regularity claim.
The four dispersed cap-6 boundaries already show that the common-UU branch
is not exhaustive. The exact-real runner now has a scope-guarded option that
fixes the common edge as \(\{5,6\}\) under unmatched-good symmetry.

Naming each agent's second-smallest representative gives 256 labeled
patterns, but simultaneous relabeling of agents and their representatives
acts by conjugation and leaves only 19 functional-digraph orbits. Ties are
handled by allowing every representative attaining the second order
statistic. Eighteen of the 19 orbits appear among the 17 common-UU cap-6
profiles; only the identity pattern, where every agent names its own
representative, is absent. Thus the symmetry split is exhaustive and small,
but the bounded data do not justify discarding any substantial class. A
708-pool exact-real test of that unobserved identity cell also returned
`unknown` after 300 seconds.

## Exact-real boundary

Both exhaustive branches were encoded over normalized strictly positive
reals, with the full no-Hall-cell condition and all 780 eight-orbit
partitions obstructed:

- the RR-singleton branch returned `unknown` after 300 seconds;
- the canonical RR-nonsingleton-(\{1,2\}) branch returned `unknown` after
  300 seconds.

The compressed common-UU branch with fixed witness \(\{5,6\}\) and a
708-partition seed pool also returned `unknown` after 300 seconds. This
motivates the 19-orbit second-order-statistic split above rather than a
longer monolithic timeout. The boundary record is
[efx49_distinct_half_eight_orbit_common_uu_cegar_session1.json](efx49_distinct_half_eight_orbit_common_uu_cegar_session1.json).
The complementary formula, which forbids every common unrepresented witness
and therefore contains both the dispersed-singleton and RR-nonsingleton
regimes, returned `unknown` after 300 seconds with a 708-partition seed pool.
Its record is
[efx49_distinct_half_eight_orbit_no_common_uu_cegar_session1.json](efx49_distinct_half_eight_orbit_no_common_uu_cegar_session1.json).
Together these two formulas are exhaustive, but neither timeout has positive
evidentiary weight.
The first high-frequency second-smallest orbit, represented by
\((1,1,1,2)\), also returned `unknown` after a 60-second smoke test with
the earlier 316-partition pool; see
[efx49_distinct_half_eight_orbit_common_uu_map1112_cegar_session1.json](efx49_distinct_half_eight_orbit_common_uu_map1112_cegar_session1.json).

A cap-20 optimization first improved the positive boundary from 45 to 30
eight-orbit repairs. Independent exact-census anneals and a cap-100 CP-SAT
run later reached three repairs, all in one ((U|0|RR+RR)) cell. The exact
optimizer bound still permits zero, so three is not a proved floor. Those
three repairs convert the three missing pairings of a 12-of-15 Hall cell;
the cap-free mechanism is the
[zero-neighbor conversion lemma](ZERO_NEIGHBOR_FAVORITE_TRIPLE_CONVERSION_LEMMA.md).
The earlier 30-repair checkpoint remains frozen in the
[Hall-split gate audit](efx49_distinct_half_rr_hall_split_gate_audit.json).

The all-28-cell singleton strengthening also returned `unknown` in Z3 after
300 seconds. A syntax-normalized QF_LRA replay with pinned cvc5 1.3.3 ran for
300 seconds and produced no verdict. A separate cap-20 CP-SAT encoding of
the same strengthening returned `UNKNOWN` after 600.15 seconds, 305,875
conflicts, and 3,898,077 branches without a model. These outcomes are solver
boundaries, not evidence that the selector is true.

Primary artifacts:

- [Hall-split gate audit](efx49_distinct_half_rr_hall_split_gate_audit.json);
- [RR-singleton Z3 boundary](efx49_distinct_half_full_cell_real_eight_orbit_rr_singleton_session1.json);
- [RR-nonsingleton Z3 boundary](efx49_distinct_half_full_cell_real_eight_orbit_rr_nonsingleton12_session1.json);
- [all-cell singleton Z3 boundary](efx49_distinct_half_full_cell_real_eight_orbit_singleton_session1.json);
- [all-cell singleton cvc5 boundary](efx49_distinct_half_full_cell_real_eight_orbit_singleton_sorting_formula.cvc5.json); and
- [all-cell singleton cap-20 CP-SAT boundary](efx49_distinct_half_full_cell_eight_orbit_singleton_cpsat_cap20_session1.json).

## A failed local shortcut

A tempting stronger claim was that an EFX partition in either terminal
orbit can be converted to the six-orbit family by swapping one representative
out of its all-representative triple. Exact rational profiles refute that
claim in both terminal symmetry types, even under the full hard-branch
assumptions and with no full Hall cell. The two profiles still have 335 and
473 favorite-pair EFX partitions, respectively, including many global
six-orbit repairs. Therefore any valid exchange proof must globally re-pair
bundles; one local swap is insufficient.

The refuting profiles are
[terminal type R](efx49_distinct_half_terminal_exchange_R_session1.json) and
[terminal type U](efx49_distinct_half_terminal_exchange_U_session1.json).
The weaker global statement—some six-orbit repair exists, without requiring
one prescribed swap—remains open: direct exact-real tests in both terminal
types returned `unknown` after 300 seconds. Their boundaries are
[type R](efx49_distinct_half_terminal_to_six_R_session1.json) and
[type U](efx49_distinct_half_terminal_to_six_U_session1.json).

The later radius-two terminal family gives a sharp finite boundary. At cap 5
it is dual-verified in all seven terminal/matching cells, but at cap 20 its
full 138-state union is false even when every full Hall cell is forbidden.
The global Hall-witness split therefore remains the live successor. See the
[terminal-exchange gate](DISTINCT_HALF_TERMINAL_EXCHANGE_GATE.md).

## Remaining analytic target

The equivalent order-statistic formulation is isolated in
[DISTINCT_HALF_COMMON_UU_SPLIT_GATE.md](DISTINCT_HALF_COMMON_UU_SPLIT_GATE.md).
The cleanest human target exposed by the refined split is now staged:

> First prove that the dense unmatched-edge condition forces an eight-orbit
> EFX state without a Hall premise. Then prove that one canonical common
> unmatched witness plus failure of every full Hall cell also forces such a
> state.

These clauses are exhaustive and symmetry-correct. Proving both would
establish the eight-orbit selector; it would still close only the current
four-agent/nine-good structural branch, not general additive EFX.
