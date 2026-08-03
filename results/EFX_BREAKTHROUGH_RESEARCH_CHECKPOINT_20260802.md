# EFX breakthrough research checkpoint — critical-cut phase

## Status

Four-agent additive EFX and general additive EFX remain unresolved.  This
checkpoint makes no existence or counterexample claim for either problem.

The active branch is `codex/efx-breakthrough-next-20260802`.  It is isolated
from the immutable threshold-Hall publication branch and the two existing
pull requests.  No new research result has been pushed from this branch.

## New cap-free analytic results

1. **Threshold-maximum swap preservation.**  Every eligible owner-minimum
   floater swap from a global normalized owner-threshold maximum remains on
   the same maximum plateau.  The incoming floater occupies a new owner-
   minimum slot.
2. **Exact swap obstruction.**  For a nonsingleton source, the new floater is
   automatically unenvied.  Ineligibility can arise only from an external
   incoming-target wall or a source-owner shortfall wall, with opposite strict
   comparisons between the old floater and released good.
3. **Completion-move trichotomy.**  Every strict increase of the exact Hall
   bottleneck margin induced by a floater swap becomes, at the completed-
   partition level, either a one-good transfer, a two-bundle swap, or a
   three-bundle augmenting path.  Reinserting the new floater into its source
   reconstructs an old completion candidate and can never strictly improve.
4. **Bottleneck Hall cut.**  At the exact bottleneck level \(\beta\), the
   weak edge graph has a perfect matching and the strict edge graph is
   Hall-deficient.  Every critical cut forces equality edges, and every
   improving successor must create a strict edge crossing the old cut.
5. **Full-cut one-bottleneck normal form.**  If the smallest strict Hall
   witness is the full agent set, the strict graph misses exactly one bundle
   and a weak optimal matching can be chosen with exactly one equality edge;
   all remaining matching edges are strict.
6. **Receiver-edge monotonicity.**  Transferring a positive good into a bundle
   strictly improves every observer's edge slack to that receiver.  Swapping
   the floater into a bundle strictly improves observer \(i\)'s receiver edge
   whenever \(i\) values the floater above the released good.
7. **Owner-separable component decomposition.**  Transfer-component gain
   decomposes for any sum of owner-level bundle functions, not only linear
   utilitarian welfare.  It therefore applies exactly to normalized owner-
   threshold potential.
8. **Full-eligibility dependency cycles.**  Component-local EFX failures and
   floater-nonenvy failures both cross transfer-component boundaries.  If no
   component state is eligible, the dependency graph contains a directed
   cycle.
9. **Minimum-slot permutation plateau.**  At a global threshold maximum, any
   eligible simultaneous permutation of one selected owner minimum from each
   bundle together with the floater stays on the same plateau.  This extends
   radius-one floater swaps to owner-minimum exchanges and arbitrary cycles.

The central source files are:

- `PARTIAL_THRESHOLD_MAXIMUM_SWAP_REDUCTION_LEMMA.md`;
- `PARTIAL_THRESHOLD_MINIMUM_SWAP_OBSTRUCTION_LEMMA.md`;
- `PARTIAL_THRESHOLD_HALL_COMPLETION_MOVE_REDUCTION_LEMMA.md`;
- `PARTIAL_THRESHOLD_MINIMUM_SLOT_PERMUTATION_LEMMA.md`;
- `PARTIAL_THRESHOLD_BOTTLENECK_HALL_CUT_LEMMA.md`;
- `PARTIAL_EFX_TRANSFER_COMPONENT_DECOMPOSITION_LEMMA.md`; and
- `PARTIAL_EFX_TRANSFER_COMPONENT_DEPENDENCY_LEMMA.md`.

## Exact finite evidence

The enriched exact-rational plateau artifact has SHA-256
`16d1d9041c32278cf243462d8bea679926cced30817c21b34b9f2f53448fcdb2`.
Across 46 positive four-agent profiles it verifies:

- 15,557 global threshold-maximal states;
- 7,655 blocked maximum states, every one with a strict Hall-margin path to a
  completing maximum state;
- all 7,655 remain reachable when every transition is required to release an
  owner minimum and insert a new owner minimum, so the path stays inside one
  fixed-core, five-token permutation orbit; the maximum restricted path length
  is two;
- 4,848 selected strict owner-minimum swaps, all preserving the maximum
  threshold plateau;
- completion moves split into 2,374 one-good transfers, 2,440 two-bundle
  swaps, and 34 three-bundle augmenting paths;
- 331 minimum critical cuts of size two, 58 of size three, and 4,459 of size
  four; and
- all 4,459 selected full-cut states have a strict gradient from one of only
  two canonical sources: the best host or the unique missing bundle.

These are corpus facts.  Every audited plateau already contains a completing
state, so the census does not sample a hypothetical all-blocked counterexample
plateau.

## Exact falsifications and strategy correction

The two-source gradient is false as a purely local lemma.  A fixed positive
\(4\times9\) full-cut model has no eligible strict gradient from either
canonical source, but the base is not globally threshold-maximal.  Its nearest
Hall-completable global maximum is owner distance two and improves the
threshold potential by \(95/3478\).

A second exact model also blocks all four old-good swaps between the canonical
two-good host and missing bundles.  One such swap would improve the potential
but is ineligible; the nearest completing global maximum is owner distance six
and improves the potential by \(869/13976\).

Therefore the surviving proof cannot replace true global maximality with a
fixed-radius menu or with local threshold compatibility.  The natural
off-diagonal matrix potential is also not monotone on the exact paths: 99
steps increase it, 4,738 preserve it, and 11 decrease it.

The falsification artifacts and generators are:

- `threshold_full_cut_two_source_natural_4x9_identity_session1.json`;
- `threshold_full_cut_exchange_or_gradient_min03_4x9_identity_session1.json`;
- `decide_threshold_full_cut_two_source.py`; and
- `audit_threshold_plateau_exact_paths.py`.

## Remaining four-agent theorem

The dominant full-cut branch is reduced to the following global statement:

> At a globally normalized-threshold-maximal eligible state, a full critical
> Hall cut forces either a strict two-source Hall gradient or a positive-gain
> union of transfer components.  If individual positive components are
> ineligible, their full-eligibility dependency cycle yields either an
> eligible positive union or an impossible weighted wall cycle.

This is not proved.  The immediate analytic work is to write the two canonical
source failures as component dependencies and decide the possible cycles on
four owner vertices.  Fixed-radius search is no longer justified.

The sharper formulation is now
`PARTIAL_THRESHOLD_MINIMUM_SLOT_ORBIT_COMPLETION_TARGET.md`: freeze the four
bundle cores and search analytically over the five parking tokens.  Proving
that one eligible token permutation completes would resolve the four-agent
case.

The subsequent adversarial pass has now shown, in the canonical (4\times9)
pair-base stress cell, that frozen-core orbit blockage is feasible away from a
global maximum.  An exact CEGAR reached 141 cumulative rounds with 137
completion blockers and 42 global-maximality witnesses: every blocked orbit
found still has a higher-threshold eligible base.  An independent exact-
preserving anneal improved the blocked base/global ratio to 0.961317 but did
not reach one.  At that endpoint the orbit Hall deficit is (1/55584), while
the threshold gap is (3857/55584); the gap is dominated by a core
reassignment outside the token orbit.  The live statement is consequently the
arbitrary-core generalization of the core-token exchange alternative recorded in
`PARTIAL_THRESHOLD_CORE_TOKEN_EXCHANGE_GATE.md`.  Neither the global orbit
theorem nor four-agent EFX has been proved.

A nearest-higher-state oracle then reduced the observed maximality witnesses
to 13 owner-distance-two exchanges and two owner-distance-three cycles.  The
complete balanced radius-three menu has 32 swaps and 112 cycles.  An exact
boundary valuation proves swaps alone insufficient: its blocked token orbit
has no positive eligible distance-two exchange, while the unique positive
local move is a three-owner cycle of gain \(41/1260\).  This replaces the broad
core-reassignment target by a concrete local menu to test.

The full local menu did not survive the next adversarial pass.  A compact
whole-state Hall encoding reached 120 cumulative rounds with 21 Hall cuts and
108 nearest-exchange cuts.  Its final aligned blocked model has no eligible
balanced radius-three state; the nearest higher-threshold allocation has shape
\(1+3+2+2\), owner distance four, and gain \(403/8220\).  Across the run,
nearest witnesses reached owner distance seven.  The corrected live target is
therefore the augmenting-component-cycle alternative: failed local moves must
combine into an eligible positive-gain union, with no fixed-radius bound.

The first exact subcell of that corrected target is now closed.  In the final
boundary profile, the four host completions have cyclic deficient agent pairs.
Fixing the complete four host-edge graphs, an exact formula is UNSAT after 86
cumulative CEGAR iterations with 73 global-maximality cuts and 26 whole-state
Hall blockers.  Thus a globally threshold-maximal canonical base in this exact
edge subcell must have an EFX-completable token permutation.  All 73 selected
global cuts are connected transfers.  This is a bounded edge-cell theorem,
not yet the same theorem for the coarser cyclic pair-Hall normal form; see
`PARTIAL_THRESHOLD_FOUR_HOST_EDGE_CELL_THEOREM.md`.

The subsequent coarsening pass leaves eight diagonal host-edge switches free
while fixing the source's other 24 unconstrained edge values.  Exact models
refute both a named-swap lemma and the full 32-state distance-two exchange
menu in diagonal pattern 1.  The stronger countermodel has a blocked token
orbit but is not globally maximal; its nearest higher Hall-completable state
is a connected distance-three transfer.  A finer matching-witness CEGAR then
closed the complete pattern-1 edge cell with 65 global cuts and 116 individual
completion blockers after 50 cumulative iterations.  A fresh staged replay
reproduced the same ordered pools and UNSAT verdict; all 65 global witnesses
are connected and have owner distance at most four.  Exact cyclic invariance
of the fixed off-host profile transfers the theorem to patterns 1, 4, 32, and
64.  Including the prior pattern-0 theorem, five diagonal profiles are now
closed.  At this intermediate stage, pattern 2—the other single-bit orbit—was
UNKNOWN after 58 global cuts and 70 matching blockers.  Multi-bit patterns
remain unclassified.  A merged 69-global/149-completion pool remains UNKNOWN after
fresh 300-second default and QF_LRA checks using the direct pairwise EFX
encoding.  See
`PARTIAL_THRESHOLD_DIAGONAL_PATTERN1_THEOREM.md` and
`PARTIAL_THRESHOLD_DIAGONAL_SWITCH_GATE.md` for the exact boundary and replay.

The preferred pattern-1 certificate is now a solver-minimized 52-cut UNSAT
core: 27 global cuts and 25 matching blockers.  A fresh standalone one-check
reconstruction returns UNSAT in 98.91 seconds.  Its global witnesses are
exactly 12 connected swaps and 15 connected four-owner cycles; no three-owner
move remains.  Across the cyclic pattern orbit the core has eight exchange
templates and 15 completion-failure templates.  QF_LRA Z3 and independent
cvc5 1.3.4 also return UNSAT on the normalized archived formula.  The exact
finite-menu alternative is recorded in
`PARTIAL_THRESHOLD_DIAGONAL_FINITE_MENU_LEMMA.md`.

The subsequent pattern-2 attack removes every threshold `ITE` by exact
leave-one-good-out expansions.  The literal runner reproduces the pattern-1
core as UNSAT.  Pattern 2 initially remains UNKNOWN after a nested exact cube
cover and a separate compact whole-Hall replay.  Structural extraction reduces
the pattern-2 witness pool to 13 cyclic connected templates.  Together with
the pattern-1 theorem core, the union has 18 templates: five swaps, seven
balanced three-owner transfers, five balanced four-owner cycles, and one
lopsided three-owner transfer of bundle shape 1+2+2+3.

The 18-template union then closes pattern 2.  A tracked UNSAT extraction leaves
a 63-cut core with 41 global moves and 22 completion blockers.  The core itself
uses only 15 balanced connected exchange templates—4 swaps, 6 three-owner
cycles, and 5 four-owner cycles—plus 12 completion templates.  Fresh
default, arithmetic-solver-2, and QF_LRA replays return UNSAT, and cyclic symmetry closes
patterns \(\{2,8,16,128\}\).  Together with pattern 0 and the pattern-1 orbit,
all nine diagonal profiles of Hamming weight at most one are closed in the
fixed off-host subcell.  See `PARTIAL_THRESHOLD_DIAGONAL_TOPOLOGY_GATE.md` and
`PARTIAL_THRESHOLD_DIAGONAL_PATTERN2_THEOREM.md`.

The subsequent coarsening removes all 24 off-host and eight diagonal edge
equalities.  Its current exact pool has 159 global-maximality cuts, 78 matching
blockers, and 30 whole-token Hall blockers.  This yields the first structural
lemma in the full cyclic pair-Hall cell: every owner's core good weakly
dominates both the floater and the preceding pair's token.  The core--floater
wall is confirmed by three Z3 profiles and cvc5; the predecessor-token wall is
confirmed by three Z3 profiles while cvc5 remains UNKNOWN.  Cyclic relabeling
gives both walls in all four rows.  The residual two-wall master remains open;
its fresh exact depth-six cover has 58 leaves and is not yet decided.  See
`PARTIAL_THRESHOLD_PAIR_HALL_CORE_DOMINANCE_LEMMA.md`.

After the full-cut branch, the proper critical-cut branches of sizes two and
three remain.  Only after all three branches close can the Hall-gradient lemma
be integrated with the known one-unallocated-good theorem to prove complete
EFX for four agents.

General additive EFX remains farther away.  The charity Hall-absorption
equivalence is available, but there is no theorem that absorbs one good from
an arbitrary charity set while preserving collective charity dominance.

## Verification

The focused parkability suite passes:

```text
48 passed, 35 warnings in 15.00s
```

The warnings are pre-existing pytest return-value warnings.  The new Python
generators compile successfully, and every quoted artifact parses as JSON.
