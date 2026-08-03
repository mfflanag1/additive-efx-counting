# Diagonal topology gate

## Current result boundary

Four-agent additive EFX and general additive EFX remain open.  This checkpoint
does not close diagonal pattern 2.  It replaces the threshold encoding by an
exact literal formulation, maps part of the remaining pattern-2 search space,
and extracts a small connected-transfer topology target from the two
single-bit diagonal orbits.

## Exact literal threshold lemma

For an additive row `v` and nonempty bundle \(B\), define

\[
T_v(B)=\{v(B\setminus\{g\}):g\in B\}.
\]

Then the EFX threshold is \(\tau_v(B)=\max T_v(B)\).  Consequently:

\[
x\geq\tau_v(B)\iff \bigwedge_{t\in T_v(B)}x\geq t,
\qquad
x<\tau_v(B)\iff \bigvee_{t\in T_v(B)}x<t.
\]

For four owner bundles \(B_i\),

\[
\sum_i\tau_{v_i}(B_i)\leq x
\iff
\bigwedge_{(t_0,\ldots,t_3)\in\prod_iT_{v_i}(B_i)}
\sum_i t_i\leq x.
\]

These identities remove every maximum `ITE` from eligibility, EFX edges,
strict EFX failures, and threshold-potential upper bounds.  Symbolic QF_LRA
equivalence checks pass for all four uses.  The archived pattern-2 literal
master has 447 top-level assertions and zero `ITE` expressions.

As a substantive regression, the same literal runner replays the preferred
52-cut pattern-1 core as UNSAT in 229.45 seconds.  Thus the rewrite preserves
an already dual-solver-verified theorem certificate rather than only passing
small unit examples.

## Pattern-2 decision status

The merged pattern-2 formula with 69 global-improvement cuts and 149
completion blockers remains UNKNOWN after 300 seconds in the fully literal
encoding.  An exact depth-4 cube cover splits the master into six branches:
three are UNSAT and three remain UNKNOWN.  Refining those three branches gives:

- 5 UNSAT and 5 UNKNOWN leaves out of 10;
- 8 UNSAT and 5 UNKNOWN leaves out of 13; and
- 6 UNSAT and 8 UNKNOWN leaves out of 14.

The five UNKNOWN leaves of the first subcover were split again.  Of the 36
resulting leaves, 5 are UNSAT and 31 remain UNKNOWN at 90 seconds per leaf.
Two eight-leaf descendants produced eight timeouts each.  This is a bounded
negative-space map, not an UNSAT proof.  No SAT branch or valuation was found.
Independent cvc5 also timed out on a representative hard leaf.

A second replay uses the more compact pool of 50 global-improvement cuts and
26 whole-token-state Hall blockers.  The literal QF_LRA check also returns
UNKNOWN at 300 seconds, as does an independently parsed cvc5 replay.  This
rules out the hypothesis that the 149
permutation blockers alone caused the stall; it does not decide the cell.

## Exact topology extraction

Every one of the 50 pattern-2 improvement witnesses is connected.  Their raw
topology is:

- 18 two-good swaps;
- 28 balanced three-good, three-owner transfers; and
- 4 connected four-good transfers on three owners, with final bundle shape
  \(1+2+2+3\).

After simultaneous cyclic relabeling, the 50 witnesses reduce to 13 exchange
templates:

- 5 swap templates;
- 7 balanced three-owner templates; and
- 1 lopsided \(1+2+2+3\) template.

The 26 whole-state Hall blockers also reduce to 13 cyclic token-state
templates.  These are exact facts about the persisted pool, not a completeness
claim.

The proved pattern-1 core has 8 exchange templates: 3 swap templates and 5
balanced four-owner cycle templates.  Exactly the 3 swap templates are common
to the pattern-1 and pattern-2 pools.  Their union therefore has 18 connected
templates, all moving at most four goods:

- 5 swaps in total;
- 7 balanced three-owner transfers;
- 5 balanced four-owner cycles; and
- 1 lopsided three-owner transfer.

This exposes a real structural difference between the two single-bit orbits.
Pattern 1 needs full four-owner cycles, whereas the current pattern-2 boundary
needs three-owner moves and one bundle-shape-changing move.  A swap-only or
balanced-cycle-only proof cannot cover both observed mechanisms.

## Analytic conversion target

The next lemma to prove is the following fixed-profile statement.

> **Four-good connected alternative.**  In the cyclic pair-Hall cell with the
> recorded 24 off-host edges fixed, if every eligible fixed-core token state
> is EFX-completion blocked, then one of the 18 cyclic transfer templates is
> eligible and has strictly larger normalized owner-threshold potential.

Global threshold maximality would exclude the improving alternative.  The
pattern-1 theorem proves the statement in its cyclic orbit using 8 of the 18
templates.  Pattern 2 currently supplies only a candidate 13-template menu;
the solver has not proved that menu sufficient.

The analytic proof should separate the three topologies.  For balanced cycles,
the potential change is a sum of owner-local retained/incoming maxima.  The
lopsided template requires one additional inequality transferring a good from
the future singleton bundle to the future triple bundle.  That is the precise
place where a proof restricted to pair-preserving exchanges would fail.

After this lemma, the remaining gates are still substantial: remove the fixed
24 off-host edges, lift from canonical pairs to arbitrary cores, close the
four-agent one-charity-good reduction, and prove charity absorption for an
arbitrary charity set.

## Reproducible artifacts

- `minimum_slot_orbit_diagonal_pattern2_literal_master.smt2`;
- `minimum_slot_orbit_diagonal_pattern2_literal_expansion_audit.json`;
- `minimum_slot_orbit_diagonal_pattern1_literal_replay_v5.json`;
- `minimum_slot_orbit_diagonal_pattern2_literal_hall_replay_session1.json`;
- `minimum_slot_orbit_diagonal_pattern2_literal_hall_component_audit.json`;
- `minimum_slot_orbit_diagonal_pattern2_literal_hall_quotient_audit_v2.json`;
- `minimum_slot_orbit_diagonal_pattern2_literal_hall_master_cvc5.json`;
- `minimum_slot_orbit_diagonal_topology_union_audit.json`;
- `audit_minimum_slot_literal_expansion.py`;
- `split_minimum_slot_literal_cubes.py`;
- `decide_minimum_slot_literal_cube_cover.py`; and
- `audit_minimum_slot_diagonal_topology_union.py`.

Shortest symbolic audit:

```sh
python tracks/parkability/audit_minimum_slot_literal_expansion.py \
  --source results/minimum_slot_orbit_diagonal_pattern2_literal_master.smt2 \
  --output /tmp/minimum-slot-literal-expansion-audit.json
```

Topology-union replay:

```sh
python tracks/parkability/audit_minimum_slot_diagonal_topology_union.py \
  --pattern1 results/minimum_slot_orbit_diagonal_pattern1_unsat_core_pool_v5.json \
  --pattern2 results/minimum_slot_orbit_diagonal_pattern2_literal_hall_replay_session1.json \
  --output /tmp/minimum-slot-diagonal-topology-union.json
```
