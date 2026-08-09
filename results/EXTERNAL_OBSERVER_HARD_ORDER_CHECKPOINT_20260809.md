# External-observer hard-order checkpoint

**Date:** 2026-08-09
**Goal:** decide the external-observer-safe three-agent lexicographic
improvement lemma in all eight hard alternating priority orders
**Status:** six orders refuted; one half-turn pair proved on the full binary
packet grid but not cap-free

## The candidate lemma

In the alternating state

\[
p\xrightarrow f r\longrightarrow s
\xrightarrow f q\longrightarrow p,
\]

the singleton owners are \(X_p=\{x\}\) and \(X_s=\{y\}\).  For a hard
priority order beginning with one of these owners, keep that first owner's
singleton bundle exactly fixed and never give it another good.  Repartition
any subcollection of all remaining goods among the other three agents.

The resulting allocation is EFX exactly when:

1. the three active agents are internally EFX; and
2. every active bundle `Z` is deletion-safe for the fixed observer `a`:

   \[
   v_a(Z\setminus\{g\})\le v_a(X_a)
   \qquad(g\in Z).
   \]

The candidate asserts that the active three-agent utility vector can be made
lexicographically larger than its base vector in the suffix of the chosen
hard order.

## Exact eight-order classification at the atom

The strict seven-good `2+2+1+1` atom decides all eight orders.

The candidate is exactly refuted in six:

\[
(p,s,q,r),\ (p,q,r,s),\ (p,q,s,r),
(s,p,r,q),\ (s,r,p,q),\ (s,r,q,p).
\]

Each refuting profile satisfies the complete alternating structural cell,
has hundreds of rooted EFX allocations, but none lexicographically improves
the base in the recorded order.  Each nevertheless has unrestricted EFX
lexicographic escapes, so these are counterexamples to the external-observer
restriction rather than to the alternating escape or complete EFX.

The candidate survives exactly in the half-turn pair

\[
(p,s,r,q),\qquad(s,p,q,r).
\]

Each has a deletion-minimal four-rival QF_LRA certificate in the atom.  See
[`alternating_anchored_or_promoted_atomic_audit.json`](alternating_anchored_or_promoted_atomic_audit.json).

## Corrected packet experiment

For the representative order `(p,s,r,q)`, let the packet sizes be

\[
(|T_r|,|B_r|,|T_q|,|B_q|)\in\{1,2\}^4.
\]

The packet encoding now uses only a valid global symmetry break: within each
nontrivial packet, the two goods are ordered in `p`'s valuation row.  It does
not require the other agents to agree with that ordering.

Every one of the fourteen proper faces—every size vector with at least one
coordinate equal to one—is exact QF_LRA-UNSAT.  This includes:

- all four one-split eight-good cells;
- all six two-split nine-good cells; and
- all four three-split ten-good cells.

The independent aggregate replay is frozen in
[`alternating_external_observer_binary_proper_faces_audit.json`](alternating_external_observer_binary_proper_faces_audit.json),
SHA-256
`0cd7f0a6142cd53d2e2aae7a8336a382d5df8f8f7da78dfaedc61b899c574e95`.

This is a finite exact theorem, not a packet-size-independent proof.

### New analytic extraction

The four-rival certificate for the surviving seven-good order now has a
complete human wall proof. Every possible failure reduces to six pairs;
five are direct same-row strict cycles, and the sixth is a desired-set
descent through the four absent compatible families. See
[`ALTERNATING_EXTERNAL_OBSERVER_ATOMIC_WALL_LEMMA.md`](ALTERNATING_EXTERNAL_OBSERVER_ATOMIC_WALL_LEMMA.md)
and the exact extraction
[`alternating_external_observer_atomic_walls.json`](alternating_external_observer_atomic_walls.json).

The corrected one-split `B_q` face also shrinks to four rivals. In all four,
every EFX comparison except those made by `q` is structurally forced safe.
Its 36 possible blocker selections reduce to 16 exact two-to-four-wall
cores. This identifies a one-dimensional bottom-partition gate rather than
a generic three-agent repartition problem; the frozen anatomy is
[`alternating_external_observer_0213_bq2_broad_core_walls.json`](alternating_external_observer_0213_bq2_broad_core_walls.json).

## Full binary cell now decided

The earlier broad master for `(2,2,2,2)` returned `unknown` after 120 seconds.
A later reduction isolated a smaller semantic certificate: two disjoint
base-safe bundles `D,Q`, where `D` is desired by `s` or `r` and
`q(Q)>=tau_q(D)`. A direct exact formula blocking all 37,338 such pairs is
QF_LRA-UNSAT. The analytic reduction proves that any pair produces the
required rooted EFX lexicographic escape. See
[`ALTERNATING_TWO_SAFE_BUNDLE_BINARY_THEOREM.md`](ALTERNATING_TWO_SAFE_BUNDLE_BINARY_THEOREM.md).

Three targeted structured menus have since been exactly refuted inside this
cell, without refuting the rooted lemma. Each countermodel has thousands of
rooted escapes, and their successive smallest escapes require: a proper
root-offer subset, then a `T_q` cross-transfer, then an `X_r` good assigned to
`s`. The surviving invariant is the
[`singleton-return target`](ALTERNATING_SINGLETON_RETURN_TARGET.md): either
`r` receives `{y}` or `s` remains at `{y}`, followed by unrestricted
two-agent repartition. A bounded exact test processed 12 models, preserving
1,513 blockers, before returning `unknown` at 120 seconds. This is a sharper
analytic target, not a decision of the full cell.

No countermodel to the surviving rooted order is known. The full binary
cell is now an exact UNSAT theorem, pending an independent generator/solver
audit before referee-grade release.

## Structural lesson and cap-free target

No binary countermodel exists. Internal disagreement in all four packets
was necessary to evade the earlier small menus, but the two-safe-bundle
formula closes that last cell.

The corresponding cap-free target is a **safe packet-contraction lemma**:

> In a minimal rooted counterexample for `(p,s,r,q)`, at least one of
> \(T_r,B_r,T_q,B_q\) contains two goods that can be contracted into one
> supergood without destroying the alternating premises or every rooted
> lexicographic escape.

Such a contraction would reduce the number of internal packet atoms.
Iterating it would reach the seven-good atom, where the external-observer
lemma is exact UNSAT.  The obstruction is that expanding a supergood creates
two new EFX deletion comparisons; the repair lemma must reroute one child
when either comparison fails.

The cap-free
[`critical-minimum contraction lemma`](EFX_CRITICAL_MINIMUM_CONTRACTION_LEMMA.md)
now states the exact safe case: contraction preserves a candidate allocation
whenever it retains, for each observer, a minimum-value deletion good in
every mixed bundle. Therefore a minimal counterexample must cover every
mergeable pair by critical minima. The fully split binary cell is the first
cell in which all four packets can simultaneously have both children so
covered.

Proving safe contraction for one of the four packets would establish the
surviving order for arbitrary packet sizes, and half-turn symmetry would
establish the eighth order. The exact binary safe-pair theorem supplies the
finite base case for that induction.

## Breakthrough boundary

The external-observer candidate is not a universal solution for all hard
orders: six exact atomic counterexamples settle that negatively. Its
surviving symmetry pair is now proved for every packet-size vector in
`{1,2}^4` and remains a plausible cap-free lemma and a useful component of
the broader anchored-or-promoted alternating program. Complete four-agent
additive EFX is not proved here.
