# Mechanism-independent radius-three flower gate

**Date:** 2026-08-10

**Status:** literal relaxed statement refuted; intended lex-hard statement
open at a verified 37-class gate

## Target and semantic correction

The proposed target was that every hard three-nonsingleton flower
configuration has a connected redistribution of at most three goods which
preserves the earlier mutual-cycle owner `r`, strictly improves the later
owner `q`, and maintains EFX with charity.

The first exact master imposed the representative full-`X_q` flower
relations, positivity, common safety, desired bundles, and failure of every
common-safe cover.  It blocked all 6,738 structurally feasible candidate
transfers and returned SAT under Z3 4.15.3.  A solver-independent
exact-Fraction audit then checked the complete unfiltered universe:

- 72 connected one-good allocations;
- 1,770 connected two-good allocations;
- 39,552 connected three-good allocations;
- 41,394 candidates in total; and
- zero EFX candidates preserving `r` and strictly improving `q`.

The same valuation has a connected four-good endpoint, with signature

\[
q\to\mathrm{charity},\qquad q\to r,
\qquad r\to q\text{ twice},
\]

so radius four is sharp for that valuation.

However, the audit also finds eight lexicographically improving connected
allocations through radius three, the first at radius two.  In particular a
bilateral `c`--`r` swap strictly improves the earlier owner.  Such a state is
already resolved before the later-owner residual is reached.  Therefore the
model refutes the literal statement on the relaxed flower/cover master, but
does **not** refute the intended hard residual after earlier lexicographic
escapes are excluded.

## Correct lex-hard gate

The corrected bounded decision asks whether every representative flower
master has *some* connected lexicographic EFX improvement within three good
moves.  In a genuinely hard residual, all earlier-owner alternatives are
excluded, so any remaining improvement must provide the required
earlier-preserving/later-improving endpoint.

Topology-class CEGAR reduces the 41,394 allocations and 191 exact directed
topology classes to a frozen union of 37 classes containing 2,514
allocations.  Every countermodel obtained before this boundary is repaired
by at least one of those classes.  On the resulting gate:

- Z3 5.0.0 returns `unknown` at a 180-second timeout;
- Z3 4.15.3 independently returns `unknown` at the same timeout; and
- neither SAT nor UNSAT is claimed.

The exact class list is
[`flexible_lex_topology_cegar_seed37.json`](flexible_lex_topology_cegar_seed37.json).
Its census replay
[`flexible_lex_topology_cegar_seed37_audit.json`](flexible_lex_topology_cegar_seed37_audit.json)
verifies all 37 classes and all 2,514 allocations against the complete
41,394-allocation universe.

The relaxed countermodel and its exact audit are
[`flexible_later_owner_connected_radius3_refutation.json`](flexible_later_owner_connected_radius3_refutation.json)
and
[`flexible_later_owner_connected_radius3_refutation_audit.json`](flexible_later_owner_connected_radius3_refutation_audit.json).

## Mathematical consequence

Named-mechanism enumeration is no longer the right proof interface, but the
three-good bound has not been eliminated for the intended residual.  The
next proof target is the following finite dichotomy:

> Every representative hard flower valuation admits one of the 37 connected
> lex topology classes; if the first improved owner is earlier than the
> mutual-cycle later owner, the cell is already resolved, and otherwise the
> desired later-owner transfer exists.

An analytic proof should group the 37 classes by earliest improved owner and
underlying undirected shape, then derive a wall-cycle contradiction from
simultaneous failure.  A further undifferentiated solver run is unlikely to
be high leverage.

## Claim boundary

No cap-free transfer lemma, four-agent EFX theorem, or general EFX theorem is
claimed.  The relaxed countermodel is exact and the 37-class lex gate is
exactly enumerated, but the latter remains undecided.
