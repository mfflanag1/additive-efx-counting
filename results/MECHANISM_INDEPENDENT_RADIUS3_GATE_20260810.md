# Mechanism-independent radius-three flower gate

**Date:** 2026-08-10

**Status:** relaxed and basic-PI-free local statements refuted; the literal
globally hard-state statement remains open

## Target and semantic correction

The proposed target was that every hard three-nonsingleton flower
configuration has a connected redistribution of at most three goods which
preserves the earlier mutual-cycle owner `r`, strictly improves the later
owner `q`, and maintains EFX with charity.

## Final bounded resolution

The radius-three implication from the currently encoded hard-flower premises
is also false.  Allocation-level CEGAR compressed the stalled 37-class
formula to 239 exact endpoint cuts and produced a rational model whose
complete scan has no connected lexicographic EFX improvement through three
moved goods.  A binary perturbation then hardened the model without changing
that verdict:

- every value is positive;
- every row is subset-sum injective over all `2^19=524,288` bundles;
- the representative full-`X_q` flower master and every failed-cover premise
  replay exactly;
- the live inequalities
  `r(B_r)>=r(f)>r(B_q)` and `q(B_q)>q(B_r)` hold; and
- none of the 41,394 connected radius-one, radius-two, or radius-three
  allocations is an EFX lex improvement.  In particular none preserves `r`
  and strictly improves `q`.

The bound is sharp for this profile.  Its first connected later-owner escape
moves four goods along

\[
\mathrm{charity}\to c\to q\to r\to s,
\]

preserves `r`, strictly improves `q`, and maintains EFX with charity.  Its
first connected lex escape also has radius four.

The frozen valuation and solver-independent audit are
[`flexible_lex_radius3_hardened_countermodel.json`](flexible_lex_radius3_hardened_countermodel.json)
and
[`flexible_lex_radius3_hardened_countermodel_audit.json`](flexible_lex_radius3_hardened_countermodel_audit.json).
The exact radius-four witnesses are
[`flexible_later_radius3_hardened_countermodel_escape.json`](flexible_later_radius3_hardened_countermodel_escape.json)
and
[`flexible_lex_radius3_hardened_countermodel_escape.json`](flexible_lex_radius3_hardened_countermodel_escape.json).

## Hard-state audit and corrected boundary

The first hardened model is not a literal hard state.  Exact enumeration of
all common-safe desired subsets finds a genuine self-champion edge

\[
r\xrightarrow{\{f\}}r
\]

using the desired subset `{aq_br_1,f}`.  This is a one-edge PI cycle and is
forbidden at the PI-free globally maximal base of the actual flower theorem.
The diagnostic is frozen in
[`flexible_lex_radius3_hardened_countermodel_hardness_gap.json`](flexible_lex_radius3_hardened_countermodel_hardness_gap.json).

Adding all 290 no-self-champion constraints, all 20 ordinary-envy-cycle
constraints, and all 60 simple one-genuine-cycle constraints still does not
force a radius-three endpoint.  A second binary perturbation gives a positive
subset-sum-injective full-capture flower with:

- no genuine self-champion;
- no ordinary envy cycle;
- no simple PI cycle containing exactly one genuine champion edge; and
- zero EFX lex endpoints among all 41,394 connected transfers through radius
  three.

Its first later-owner endpoint has radius four and topology

\[
\mathrm{charity}\to q,qquad q\to c\text{ twice},qquad c\to s.
\]

The corresponding response relation has disjoint, internally supplied
incoming packets but no internal SDR, so it realizes the expected Hall-defect
branch rather than an immediate PI closure.  The exact profile and independent
audit are
[`flexible_lex_basic_pi_free_hardened_countermodel.json`](flexible_lex_basic_pi_free_hardened_countermodel.json)
and
[`flexible_lex_basic_pi_free_hardened_countermodel_audit.json`](flexible_lex_basic_pi_free_hardened_countermodel_audit.json).

This second model is only **basic** PI-free.  Generalized PI edge sets with
two or more genuine edges have not been exhaustively excluded, and the base
has a radius-four lex improvement, so it is not globally lex maximal.  A
radius-four global-maximality CEGAR installed 100 further endpoint cuts and
reached its iteration limit while remaining SAT; it is a resumable search,
not a verdict.  The exact trace is
[`flexible_lex_radius4_global_cegar.json`](flexible_lex_radius4_global_cegar.json).
Thus the literal theorem for a genuinely PI-free, globally
maximal hard state is neither proved nor refuted.

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

## Historical 37-class gate

The corrected bounded decision asked whether every representative flower
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

This gate is superseded by the hardened SAT countermodel above.  The exact
historical class list is
[`flexible_lex_topology_cegar_seed37.json`](flexible_lex_topology_cegar_seed37.json).
Its census replay
[`flexible_lex_topology_cegar_seed37_audit.json`](flexible_lex_topology_cegar_seed37_audit.json)
verifies all 37 classes and all 2,514 allocations against the complete
41,394-allocation universe.

## Structural decomposition and live slice

The exact shape census
[`flexible_lex_topology_shape_census.json`](flexible_lex_topology_shape_census.json)
splits the gate into two proof branches:

- 17 structurally later-compatible classes containing 1,294 allocations;
- 20 earlier-only classes containing 1,220 allocations.

Here later-compatible means that `q` receives a good and `r` does not lose a
good without receiving one.  This is necessary, not sufficient, for the
desired `r`-preserving/`q`-improving endpoint.  In a globally lex-maximal
state the earlier-only completions are forbidden, so the analytic task is to
show that simultaneous failure of both branches is impossible.

The cap-free early-root charity rotation lemma further narrows the live
residual to

\[
v_r(B_r)\ge v_r(f)>v_r(B_q),
\qquad
v_q(B_q)>v_q(B_r).
\]

These inequalities, together with eight sound global packet-item symmetry
cuts, define a reproducible 37-class QF_LRA export.  Z3 5.0.0 and official
cvc5 1.3.4 both time out on a 60-second bounded replay; neither returns a
mathematical verdict.  Exact hashes and solver provenance are recorded in
[`flexible_lex_gate37_live_solver_portfolio.json`](flexible_lex_gate37_live_solver_portfolio.json)
and
[`flexible_lex_gate37_live_export.json`](flexible_lex_gate37_live_export.json).

The relaxed countermodel and its exact audit are
[`flexible_later_owner_connected_radius3_refutation.json`](flexible_later_owner_connected_radius3_refutation.json)
and
[`flexible_later_owner_connected_radius3_refutation_audit.json`](flexible_later_owner_connected_radius3_refutation_audit.json).

## Mathematical consequence

No proof using only the flower/cover/live-polarity premises, even augmented
by the basic PI-cycle exclusions above, can force a connected three-good
endpoint: that local theorem is exactly false already for two-atom packets.
The radius-three claim can survive only by using a genuinely stronger
generalized-PI or global-maximality consequence.  Otherwise the viable target
must allow at least four moved goods or replace item radius by adaptive
transfer-component growth.

## Claim boundary

The exact models refute the bounded local radius-three implication from the
audited representative flower/cover/live-polarity premises and from its basic
PI-free strengthening.  They do not refute the literal theorem at a fully
PI-free globally maximal state, complete EFX existence, the BCFF global
program, or an unrestricted transfer-component lemma.  No four-agent or
general EFX theorem is claimed.
