# Common-Unmatched Hall-Witness Split

**Status:** exact exhaustive reduction; both cap-free branches remain open  
**Scope:** four agents, nine goods, strict common favorite, universal owner-
threshold failure, and fixed distinct half-favorite representatives  
**Not claimed:** the eight-orbit selector, complete EFX for four agents, or
general additive EFX

## The compression

Write the common favorite as (0), the four matched representatives as
(R=\{1,2,3,4\}), and the unmatched goods as (U=\{5,6,7,8\}). For an
unmatched edge (e\in\binom U2), call (e) a *common RR-cell witness* when
it is a zero-neighbor Hall witness in every one of the six cells whose
parked low pair lies in (\binom R2). Thus

\[
 v_i(e)<F_i+\max_{r\in L}v_i(r)
 \quad
 \text{for every agent }i\text{ and every }L\in\binom R2.
\tag{1}
\]

Let (s_i) be agent (i)'s second-smallest value among the four
representatives. Since

\[
 \min_{L\in\binom R2}\max_{r\in L}v_i(r)=s_i,
\]

(1) is exactly the four-inequality condition

\[
 v_i(e)<F_i+s_i\qquad(i=1,\ldots,4).
\tag{2}
\]

This turns the large Hall-witness disjunction into the following exhaustive
split.

1. **Dense unmatched branch:** no common witness exists. Equivalently, every
   (e\in\binom U2) has some agent (i) with
   (v_i(e)\ge F_i+s_i).
2. **Common-witness branch:** some common witness exists. Unmatched-good
   symmetry fixes it as (e=\{5,6\}), after which (2) supplies only four
   inequalities.

The first branch suggests a stronger standalone target: the six dense-edge
conditions may force an eight-orbit EFX state without any full-Hall premise.
Only the second branch then needs the assumption that every favorite-triple
Hall cell fails.

## Finite symmetry inside the common branch

The map sending each agent to a representative attaining its second-smallest
representative value is a function from four labeled agents to four labeled
representatives. Simultaneously permuting agents and their matched
representatives acts by conjugation. The (4^4) maps have exactly 19
conjugacy orbits.

Fixing one orbit replaces the 24-disjunction common-witness encoding by 16
order constraints and the four inequalities in (2). Ties may put one profile
in several map cells, but the 19 cells remain exhaustive. The cap-6 deletion
boundaries realize 18 of the 19 orbits; the then-unobserved identity map is
not impossible, because the later cap-15 optimization profile realizes all
19 through ties.

## Current exact boundary

Five independent positive profiles cover 708 of the 780 eight-orbit
partitions. Using those 708 partitions as exact obstruction cuts produced
the following honest solver boundaries:

- the unrestricted no-full-cell formula returned `unknown` after 600
  seconds;
- the dense unmatched branch, even after dropping the no-full-cell premise,
  returned `unknown` after 300 seconds;
- the common-witness/no-full-cell branch returned `unknown` after 300
  seconds;
- the no-common-witness/no-full-cell branch returned `unknown` in both Z3
  QF_LRA and cap-20 CP-SAT; and
- the canonical identity second-smallest-map cell returned `unknown` after
  300 seconds.

These timeouts are not evidence for either satisfiability or validity. The
primary records are the
[708-cut global boundary](efx49_distinct_half_eight_orbit_cegar_session5.json),
[dense-edge boundary](efx49_distinct_half_eight_orbit_dense_uu_cegar_session1.json),
[common-witness boundary](efx49_distinct_half_eight_orbit_common_uu_cegar_session1.json),
[no-common exact boundary](efx49_distinct_half_eight_orbit_no_common_uu_cegar_session1.json),
[no-common CP-SAT boundary](efx49_distinct_half_eight_orbit_no_common_uu_cpsat_cap20_session1.json),
and
[identity-map boundary](efx49_distinct_half_eight_orbit_common_uu_map1234_cegar_session1.json).

## New optimization boundary

The first guarded optimization reduced the positive boundary from 45 to 30
eight-orbit repairs. Two later, independently seeded exact-census anneals
reduced it to three, and a 900-second cap-100 CP-SAT optimization reproduced
that floor while retaining a bound that permits zero. Thus three is not a
proved lower bound.

In both three-repair profiles, all surviving favorite-pair states are the
three perfect pairings of (R) in one ((U|0|RR+RR)) cell. Exact full-universe
replay finds precisely 15 EFX-supporting unlabeled partitions in each
profile, all with complete feasibility graphs: 12 valid pairings in one
favorite-triple Hall cell and the three converted favorite-pair states. The
other three pairings in that Hall cell fail through one shared zero-neighbor
edge. This (12+3) structure is explained by the cap-free
[zero-neighbor conversion lemma](ZERO_NEIGHBOR_FAVORITE_TRIPLE_CONVERSION_LEMMA.md)
and frozen in its
[deterministic audit](efx49_zero_neighbor_favorite_triple_conversion_audit.json).
It is a positive boundary, not an EFX counterexample.

A stronger cap-free theorem now explains the whole basin, not only its
zero-neighbor cells. Whenever two residual goods are jointly bottom-two for
any three agents, every Hall-failed pairing has a distinct favorite-pair EFX
conversion. Thus that subbranch is closed and the live residual for global
selection has no pair shared as bottom-two by three agents; see
[THREE_AGENT_BOTTOM_PAIRING_CONVERSION_THEOREM.md](THREE_AGENT_BOTTOM_PAIRING_CONVERSION_THEOREM.md).

## Concise analytic target

It now suffices to prove both statements below.

> **Dense-(U) lemma.** If every unmatched edge (e) satisfies
> (v_i(e)\ge F_i+s_i) for some agent (i), then an eight-orbit
> favorite-pair partition supports EFX.

> **Common-witness lemma.** If one unmatched edge satisfies
> (v_i(e)<F_i+s_i) for every agent and no full favorite-triple Hall cell
> exists, then an eight-orbit favorite-pair partition supports EFX.

Inside the common-witness branch, the zero-neighbor conversion lemma reduces
the human task further: conditional on no favorite-pair EFX state, force one
failed Hall pairing whose shared rejected edge and two remaining pairs obey
the conversion inequalities. This is now the most concise analytic target
exposed by the search.

The split is exhaustive and its symmetry reduction is exact. Proving both
lemmas would close the current universal-threshold distinct-representative
branch at ((4,9)); it would not by itself resolve general additive EFX.
