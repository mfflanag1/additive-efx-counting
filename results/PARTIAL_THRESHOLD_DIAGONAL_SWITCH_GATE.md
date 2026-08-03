# Diagonal-switch coarsening gate

## Exact status

Four-agent additive EFX and general additive EFX remain open.  This gate
coarsens the proved four-host edge-cell theorem, but does not yet prove the
cyclic pair-Hall cell.

For the canonical base

\[
01\mid23\mid45\mid67;\qquad f=8,
\]

the four cyclic deficient pairs are

\[
\{0,3\},\quad\{0,1\},\quad\{1,2\},\quad\{2,3\}.
\]

Requiring each pair to see exactly its corresponding host fixes 32 of the 64
host-completion edge truth values.  The source off-host subcell fixes another
24 values and leaves eight host-edge switches free, in this order:

\[
(0,1),(0,2),(1,2),(1,3),(2,0),(2,3),(3,0),(3,1).
\]

The already proved theorem fixes all 64 values.  The immediate finite target
is therefore to remove these eight remaining switch assumptions, followed by
the 24 off-host assumptions.

## Finite-pool escape is not a counterexample

The 73 global cuts and 26 whole-orbit Hall blockers from the proved exact
edge cell are satisfiable after retaining only the cyclic pair-Hall
constraints.  Exact replay confirms that the resulting valuation satisfies
every stored cut.  It nevertheless has one EFX-completable state in the full
120-state token orbit and the canonical base is not globally threshold
maximal.  Thus it proves only that the old finite pool is incomplete in the
coarser cell; it is not a counterexample to the token-orbit theorem or EFX.

Independently, each of the 120 token states can be eligible and completion-
blocked at some valuation in the pair-Hall cell.  These are different
valuations for different states.  The result does not show that all eligible
states can be blocked simultaneously.

## Local edge rigidity

Under simultaneous blockage of all 120 token states, the exact source edge
profile is satisfiable.  Holding the other 31 free edge bits fixed and
flipping one bit gives the following exact local map:

- all 24 off-host flips are UNSAT;
- five diagonal flips have persisted SAT models; and
- three diagonal flips remain UNKNOWN at the current 60-second bound.

This is a Hamming-one statement only.  Several off-host bits might change
together, and UNKNOWN is not UNSAT.

Exact full-landscape replay of the five persisted diagonal models finds one
eligible token-orbit state, zero completing token-orbit states, and no global
threshold maximum in every case.  Each has a Hall-completable strictly higher
state at owner distance two.  These models therefore supply valid global
improvement cuts rather than counterexamples.

## Local exchange lemmas falsified

In diagonal pattern 1, simultaneous token-orbit blockage does not force the
particular distance-two swap first selected from a boundary model.  A targeted
CEGAR produced an exact countermodel; its nearest higher Hall-completable
state is a different distance-two swap.

The stronger menu containing every one of the 32 balanced distance-two
exchanges is also false in the same exact diagonal cell.  The exact
countermodel has:

- one eligible token-orbit state and zero completing states;
- zero eligible strictly improving states in the 32-move menu;
- 721 eligible states in the complete 589,824-state landscape; and
- a nearest higher Hall-completable state at owner distance three, with masks
  \((10,20,33,192)\), threshold gain \(3669/28416\), and Hall margin
  \(1/74\).

Hence the proof cannot be a fixed-swap or swap-only local-gradient argument.
The balanced radius-three formula reached 21 whole-orbit blockers before a
bounded solver timeout; that run has no theorem status.

## Dynamic global-improvement pools

Dynamic CEGAR is more effective than preloading every local move.  It adds a
whole-state completion blocker only when a completing token state is found,
and adds a global cut only when exact enumeration finds a strictly higher
eligible allocation.

For diagonal pattern 1, the whole-Hall pool first reached 30 cumulative
iterations with 75 global cuts and 18 whole-state blockers before timing out.
The finer matching-witness encoding then closed the exact pattern: after 50
cumulative iterations, 65 global cuts and 116 individual completion blockers
make the formula UNSAT.  A fresh staged reconstruction reproduced the same
ordered cut pools and the same UNSAT verdict in 374 seconds.  All 65 selected
global witnesses are connected transfers: 18 have owner distance two, 28
distance three, and 19 distance four.

Repeated tracked extraction and core minimization shrink the preferred
certificate to 52 guarded consequences: 27 global cuts and 25 matching
blockers.  A fresh standalone replay is UNSAT in 98.91 seconds.  The retained
global moves are 12 swaps and 15 connected four-owner cycles; no three-owner
transfer remains.  Across the cyclic pattern orbit they form eight exchange
templates, alongside 15 completion-failure templates.  Independent QF_LRA
Z3 and cvc5 1.3.4 replays also return UNSAT; the smaller core is dual-solver
verified.  Its finite-menu interpretation is stated in
`PARTIAL_THRESHOLD_DIAGONAL_FINITE_MENU_LEMMA.md`.

The fixed 24-bit off-host profile is exactly invariant under cyclic
relabeling.  Pattern 1 therefore closes the full cyclic orbit
\(\{1,4,32,64\}\).  Together with the earlier pattern-0 theorem, five exact
diagonal profiles are closed.  Pattern 2 represents the other single-bit
orbit \(\{2,8,16,128\}\) and remains UNKNOWN; multi-bit profiles are not yet
classified.

For diagonal pattern 2, the whole-Hall pool reached 23 cumulative iterations
with 50 global cuts and 26 whole-state blockers before timing out.  The
fine-grained encoding reached 33 iterations with 58 global cuts and 70
individual completion blockers; a 300-second continuation made no further
progress.  Transferring the pattern-1 theorem pool, and then merging both
pools into 69 global cuts and 149 blockers, also produced 300-second UNKNOWN
checks.  Replacing maximum expressions by equivalent literal pairwise EFX
inequalities did not close this cell: both default Z3 and QF_LRA-specialized
Z3 timed out again at 300 seconds on the merged pool, without adding a cut.
Pattern 2 remains UNKNOWN.  Its timeouts are honest computational stalls, not
mathematical evidence for either satisfiability or unsatisfiability.

The literal rewrite has now been extended to eligibility and
threshold-potential upper bounds, removing every threshold `ITE`.  Symbolic
QF_LRA audits prove all expansions equivalent, and the new runner reproduces
the preferred pattern-1 core as UNSAT.  Pattern 2 still times out in both the
69-global/149-completion formulation and a compact
50-global/26-whole-Hall formulation.  Exact cube splitting closes some
polyhedral branches but plateaus on the remaining descendants, with no SAT
branch found.  The 50 compact-pool witnesses reduce to 13 cyclic connected
templates; comparison with the pattern-1 theorem core gives an 18-template
union moving at most four goods.  The precise topology target and claim
boundary are recorded in `PARTIAL_THRESHOLD_DIAGONAL_TOPOLOGY_GATE.md`.

The exact pattern-1 result is recorded in
`PARTIAL_THRESHOLD_DIAGONAL_PATTERN1_THEOREM.md`.  It is a second complete
64-edge cell, not yet a theorem with a switch left symbolically free.

## Live analytic lemma

The useful target is no longer a named move:

> **Connected switch-cell alternative.**  In each feasible diagonal pattern,
> simultaneous blockage of the fixed-core token orbit forces an eligible
> connected transfer with strictly larger normalized owner-threshold
> potential.

Global threshold maximality would exclude the second outcome.  The finite
witness pools suggest that distance four suffices in the cells reached so
far, but this is an empirical menu bound, not a theorem.  Analytically, the
four pair-Hall inequalities should be summed along the transfer component;
incoming-target walls must cancel against owner-shortfall walls around the
cycle.

The two next exact tasks are:

1. close or exclude the remaining diagonal switch patterns compatible with
   simultaneous orbit blockage in the fixed off-host subcell, using the
   pattern-1 connected cut menu as the first analytic template; and
2. replace the 24 off-host edge equalities by consequences of orbit blockage
   or by a finite set of additional edge-pattern cases.

Only after those tasks is the cyclic pair-Hall cell closed.  An arbitrary-core
lift is still required for four-agent EFX, followed by charity absorption for
general EFX.

## Reproducible artifacts

- `minimum_slot_orbit_four_host_pair_cycle_finite_pool_sat_seed.json`;
- `minimum_slot_orbit_four_host_pair_cycle_finite_pool_sat_audit.json`;
- `minimum_slot_orbit_four_host_pair_cycle_orbit_reachability_audit.json`;
- `minimum_slot_orbit_four_host_pair_cycle_edge_flexibility_audit.json`;
- `minimum_slot_orbit_four_host_pair_cycle_edge_flip_model_global_audit.json`;
- `minimum_slot_orbit_diagonal_pattern1_swap_cegar_session1.json`;
- `minimum_slot_orbit_diagonal_pattern1_countermodel_global_audit.json`;
- `minimum_slot_orbit_diagonal_pattern1_distance2_cegar_session1.json`;
- `minimum_slot_orbit_diagonal_pattern1_distance2_global_audit.json`;
- `minimum_slot_orbit_diagonal_pattern1_global_witness_cegar_session3.json`;
- `minimum_slot_orbit_diagonal_pattern1_global_witness_cegar_staged_replay.json`;
- `minimum_slot_orbit_diagonal_pattern1_global_witness_cegar_replay_audit.json`;
- `minimum_slot_orbit_diagonal_pattern1_global_witness_cegar_component_audit.json`;
- `minimum_slot_orbit_diagonal_pattern1_symmetry_audit.json`;
- `minimum_slot_orbit_diagonal_pattern1_unsat_core_pool.json`;
- `minimum_slot_orbit_diagonal_pattern1_unsat_core_replay.json`;
- `minimum_slot_orbit_diagonal_pattern1_unsat_core_replay_audit.json`;
- `minimum_slot_orbit_diagonal_pattern1_unsat_core_component_audit.json`;
- `minimum_slot_orbit_diagonal_pattern1_unsat_core_quotient_audit.json`;
- `minimum_slot_orbit_diagonal_pattern1_unsat_core_dual_replay_audit.json`;
- `minimum_slot_orbit_diagonal_pattern1_unsat_core.normalized.smt2`;
- `minimum_slot_orbit_diagonal_pattern1_unsat_core.cvc5.json`;
- `minimum_slot_orbit_diagonal_pattern1_unsat_core_pool_v5.json`;
- `minimum_slot_orbit_diagonal_pattern1_unsat_core_untracked_replay_audit_v5.json`;
- `minimum_slot_orbit_diagonal_pattern1_unsat_core_component_audit_v5.json`;
- `minimum_slot_orbit_diagonal_pattern1_unsat_core_quotient_audit_v5.json`;
- `minimum_slot_orbit_diagonal_pattern1_unsat_core_dual_replay_audit_v5.json`;
- `minimum_slot_orbit_diagonal_pattern1_unsat_core_v5_untracked.normalized.smt2`;
- `minimum_slot_orbit_diagonal_pattern1_unsat_core_v5_untracked.cvc5.json`;
- `PARTIAL_THRESHOLD_DIAGONAL_PATTERN1_THEOREM.md`; and
- `PARTIAL_THRESHOLD_DIAGONAL_FINITE_MENU_LEMMA.md`.

Shortest exact replay of the distance-two-menu countermodel:

```sh
python tracks/parkability/audit_minimum_slot_diagonal_cegar_model.py \
  --source results/minimum_slot_orbit_diagonal_pattern1_distance2_cegar_session1.json \
  --output /tmp/minimum-slot-diagonal-distance2-replay.json
```
