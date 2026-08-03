# Diagonal pattern 2 global-improvement theorem

## Theorem

Consider positive additive valuations for four agents and nine goods.  Fix the
canonical eligible partial allocation

\[
01\mid23\mid45\mid67;\qquad f=8,
\]

with strict owner minima \(1,3,5,7\).  For the four completions obtained by
inserting good 8 into hosts \(0,1,2,3\), require the deficient observer pairs

\[
\{0,3\},\quad\{0,1\},\quad\{1,2\},\quad\{2,3\}
\]

to see exactly their corresponding host bundle.  Fix the 24 remaining
off-host edge values to the recorded boundary profile.  Order the eight free
host-edge values as

\[
(0,1),(0,2),(1,2),(1,3),(2,0),(2,3),(3,0),(3,1)
\]

and set their bit pattern to 2: edge \((0,2)\) is present and the other seven
are absent.

Then the canonical partial allocation cannot simultaneously be a global
maximum of normalized owner-threshold potential and have every eligible
fixed-core token permutation fail EFX completion.  Equivalently, at a global
threshold maximum in this edge cell, some eligible permutation of tokens
\(1,3,5,7,8\) over fixed cores \(0,2,4,6\) admits an EFX completion.

## Cyclic corollary

The fixed 24-bit off-host edge profile and cyclic pair-Hall conditions are
invariant under simultaneous cyclic relabeling.  The exact symmetry audit
maps pattern 2 to

\[
\{2,8,16,128\}.
\]

The theorem therefore closes this full four-cell orbit.  Together with the
previous pattern-0 theorem and the pattern-1 orbit
\(\{1,4,32,64\}\), every diagonal profile of Hamming weight at most one is
closed in the fixed off-host subcell: nine profiles in total.

## Exact 63-cut certificate

The first UNSAT union used 65 global-improvement cuts, 25 completion blockers,
and 26 whole-token-state Hall blockers.  Z3's arithmetic-solver-2 profile
returned UNSAT in 62.50 seconds.  A tracked, core-minimized reconstruction
returned a 63-cut core:

- 41 global-improvement cuts;
- 22 individual completion blockers; and
- no whole-state Hall blockers.

A fresh untracked reconstruction of exactly those 63 cuts returns UNSAT in
79.25 seconds under arithmetic solver 2, 133.63 seconds under the default
profile, and 200.05 seconds under the QF_LRA profile.  A frozen external Z3
5.0.0 binary replay independently parses the archived SMT-LIB formula,
verifies its SHA-256 hash, and returns UNSAT in 78.53 seconds.  The exact
profile-replay audit passes every cut-list, edge-cell, formula-hash, normalized
formula-hash, and frozen-binary check.  Independently parsed cvc5 1.3.4 returns
UNKNOWN at the 300-second bound and is not counted as confirmation.

Every retained global witness is a connected, balanced two-good allocation.
The 41 raw moves consist of 15 swaps, 11 three-owner cycles, and 15 four-owner
cycles.  Under cyclic relabeling they reduce to 15 exchange templates:

- 4 swap templates;
- 6 balanced three-owner templates; and
- 5 balanced four-owner templates.

The 22 completion blockers reduce to 12 cyclic templates.  Thus the exact
finite-menu alternative needs neither the lopsided \(1+2+2+3\) candidate from
the exploratory pattern-2 pool nor any Boolean Hall-selector cut.

## Finite-menu interpretation

Let \(G\) be the 41 connected exchange allocations and \(C\) the 22 specified
token-state/host/matching completions in the extracted core.  Under the fixed
cell hypotheses and the minimum-slot plateau consequence, at least one of the
following holds:

1. a specified member of \(C\) has an eligible token state and its specified
   complete allocation is EFX; or
2. a member \(Y\in G\) is eligible and
   \(\Theta(Y)>\Theta(B)\).

Global maximality excludes the second alternative.  This is the exact
pattern-2 analogue of the pattern-1 finite exchange-menu lemma, with
three-owner cycles added to the shared swap/four-cycle mechanism.

## Claim boundary

This is a solver-certified theorem for one cyclic orbit of four diagonal
profiles in one fixed 24-bit off-host edge profile.  It does not classify the
remaining 247 multi-bit diagonal profiles, derive the 24 off-host values from
pair-Hall blockage, close the full cyclic pair-Hall cell, lift from canonical
pairs to arbitrary cores, or prove four-agent or general additive EFX.

The independent cvc5 replay is recorded separately.  An UNKNOWN cvc5 timeout
does not weaken the two exact Z3-profile UNSAT replays, but it is not counted
as an independent-solver confirmation.

## Reproduction

Core pool:

`results/minimum_slot_orbit_diagonal_pattern2_topology_union_hall_core_pool.json`

Fresh replay:

```sh
python tracks/parkability/run_minimum_slot_orbit_cegar.py \
  --timeout-seconds 300 --max-iterations 1 \
  --seed results/minimum_slot_orbit_diagonal_pattern2_topology_union_hall_core_pool.json \
  --relabeling-mode none --completion-batch-size 8 \
  --completion-cut-mode witness --solver-profile arith2 \
  --global-witness-mode hall_insertable --base-host-pair-hall-cycle \
  --base-host-offhost-edge-cell-source \
    results/minimum_slot_orbit_hall_state_nearest_cegar_session2_orbit_blocked_seed.json \
  --base-host-diagonal-pattern 2 \
  --output /tmp/minimum-slot-diagonal-pattern2-core-replay.json
```

Primary audits:

- `minimum_slot_orbit_diagonal_pattern2_topology_union_hall_core_replay_audit.json`;
- `minimum_slot_orbit_diagonal_pattern2_topology_union_hall_core_profile_replay_audit.json`;
- `minimum_slot_orbit_diagonal_pattern2_topology_union_hall_core_menu_audit.json`;
- `minimum_slot_orbit_diagonal_pattern2_topology_union_hall_core_component_audit.json`;
- `minimum_slot_orbit_diagonal_pattern2_topology_union_hall_core_quotient_audit.json`;
- `minimum_slot_orbit_diagonal_pattern2_symmetry_audit.json`; and
- `minimum_slot_orbit_diagonal_pattern2_topology_union_hall_core_external_z3_arith2.json`.
