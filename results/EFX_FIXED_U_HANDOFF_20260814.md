# EFX fixed-U breakthrough handoff

**Date:** 2026-08-14

**Workspace:** `/private/tmp/efx-charity-exchange-20260812`

**Branch:** `codex/efx-fixed-u-termination-20260813`

**Latest pushed research checkpoint before this note update:** `79f7126`
(`research: eliminate residual two-target topology obstruction`)

## Frozen objective

Prove or refute:

> Every saturated root-facing rank-three fixed-`U` state admits a complete
> EFX allocation through at most four physical support-provenance packet
> edges, with unrestricted packet sizes.

This objective is not complete.  No cap-free proof and no full-premise
countermodel has been obtained.

## Durable progress in the last stage

### 1. Exact three-topology bounded checkpoint

The allocated-E form-2 master negated all `439` allocations on three packet
topologies.  The initial trace generated `19,747` closed generalized-PI cuts;
the valid continuation added `5,666`, for `25,413` unique cuts total.  It
reached its declared iteration limit without finding a generalized-PI-free
counterprofile and without proving UNSAT.

The complete witness census is:

- `2,125` three-owner closed-core families;
- `23,288` four-owner closed-core families.

The `91.64%` four-owner concentration is strong discovery evidence for a
full-owner alternating-uncrossing lemma, but it is not a theorem.

Authoritative files:

- `results/ALLOCATED_E_FORM2_THREE_TOPOLOGY_MENU_CHECKPOINT_20260814.md`
- `results/allocated_e_form2_three_topology_menu_cegar.json.gz`
- `results/allocated_e_form2_three_topology_menu_cegar_resume19747.json.gz`
- `results/allocated_e_form2_three_topology_menu_structural_audit.json`
- `tracks/parkability/run_allocated_e_form2_three_topology_menu_cegar.py`
- `tracks/parkability/audit_allocated_e_form2_three_topology_menu.py`

The independent audit reconstructs all `439` allocations and checks the
combinatorial semantics and uniqueness of every PI witness without importing
the primary driver.  It does not independently encode the QF_LRA master.

### 2. Anti-local-minimum menu expansion

The empirical three-topology cover is not a cap-free normal form.  It omits
all six canonical response branches, including the natural Hamiltonian path

```text
charity -> r -> s -> q -> d.
```

The widened exact runner contains the original three topologies plus all six
response branches: nine topologies and `973` distinct allocations.  Its code
and tests are committed:

- `tracks/parkability/run_allocated_e_form2_response_branch_menu_cegar.py`
- `tracks/parkability/test_allocated_e_form2_response_branch_menu_cegar.py`

Three widened checks have now ended without a mathematical verdict.  The
first and the 925-second continuation were intentionally interrupted; an
independent seed-991 check reached its declared 300-second timeout.  All
three record the correct `25,413` loaded cuts, zero fresh cuts, and status
`UNKNOWN`.  They are timing diagnostics, not evidence for SAT or UNSAT, and
should not be cited as a theorem or counterexample.

The committed certificate extractor
`extract_allocated_e_form2_response_branch_menu_unsat_core.py` independently
regenerates all `973` allocations and is ready to track, reduce, and replay
the PI cuts if a future run proves UNSAT.

### 3. Cap-free response-path payment identity

For the natural path, reverse response cores

```text
C_s subset B_r,  C_q subset B_s,  C_d subset B_q,
```

and give charity to `r`.  Owners `s,q,d` are automatically strictly paid.
The unique owner-payment condition is

\[
                 v_r(C_s)\le \Delta_r+v_r(p).
\]

This is one already-known branch of the earlier six-branch theorem, isolated
because it strictly improves the payment interface of the later `q-d` swap
endpoint.  No novelty is claimed for the underlying path.

Files:

- `results/FORM2_NATURAL_RESPONSE_HAMILTONIAN_PATH_PAYMENT_LEMMA_20260814.md`
- `results/form2_natural_response_hamiltonian_path_payment_audit.json`

### 4. Six failures compressed to three inequalities

On the shared-target-disjoint branch, simultaneous owner-payment failure of
all six response branches is equivalent to only three supplier-capture
inequalities.  With cycle cores

\[
 R\subseteq B_q,\quad Q\subseteq B_s,\quad S\subseteq B_r,
\]

they are

\[
\begin{aligned}
v_r(S)&>\Delta_r+v_r(p),\\
v_q(R)&>\Delta_q+v_q(p),\\
v_s(Q)&>\Delta_s+v_s(p).
\end{aligned}
\]

Thus the cap-free residual is not six unrelated payment tests.  It is one
three-cycle supplier-capture system, together with the already isolated
shared-target double-margin alternatives and observer continuation.

Files:

- `results/FORM2_SIX_BRANCH_PAYMENT_COMPRESSION_LEMMA_20260814.md`
- `results/form2_six_branch_payment_compression_audit.json`

### 5. Current-support spanning frontier and correction

Every one of the six canonical branch graphs is exactly a four-edge spanning
tree on charity plus all four owners.  Moreover, if such a branch is
owner-paid but not EFX, a globally minimum failed response is common-safe at
the actual probe utilities.  This is a cap-free reduction of observer
failure to one precisely decorated current response.

The provenance boundary is essential: the spanning tree is measured from
the current support state `Y`, which is the edge metric in the frozen goal.
It does **not** automatically imply that the net signed graph relative to
the older GG base `X` remains connected after packet cancellation.  An
earlier draft incorrectly called this immediate full-owner admission; commit
`d73267c` corrected the claim before using it downstream.

Files:

- `results/FORM2_SIX_BRANCH_FULL_OWNER_ADMISSION_REDUCTION_20260814.md`
- `results/form2_six_branch_full_owner_admission_audit.json`

### 6. Exact base-cancellation characterization

For a packet on a current-support edge `u -> v`, its intersection with the
old base bundle `X_v` cancels when the `X -> Y` and `Y -> Z` signed transfers
are composed; its intersections with every other base bundle become net
base-relative edges into `v`.  More globally, a vertex set `K` has no net
`X -> Z` edge across its cut exactly when its physical union is unchanged:

```text
X(K) = Z(K).
```

Thus net base-relative disconnection is equivalent to a nontrivial closed
aggregate base-support block.  It is not equivalent to return of an entire
branch packet.  An exact five-vertex counterexample shows a current spanning
path can split into two net base components even though no whole moved packet
returns to its recipient's base owner.

Files:

- `results/BRANCH_TREE_BASE_CANCELLATION_OR_CLOSED_UNION_LEMMA_20260814.md`
- `results/branch_tree_base_cancellation_closed_union_audit.json`
- `tracks/parkability/audit_branch_tree_base_cancellation_closed_union.py`

The exhaustive finite audit checked `390,625` base/final assignment pairs and
`11,718,750` proper cuts.  This theorem corrects the packetwise provenance
shortcut; it does not itself supply the response-rank or base-margin terminal.

### 7. All-target-change and exact-repeat frontier

Every one of the six canonical four-edge branches changes all four owner
bundles and charity.  Therefore a globally minimum failed response at a paid
non-EFX branch cannot be a response on an unchanged target support from the
current state `Y`.  Saturation leaves only:

1. a new fully decorated response/support record; or
2. an old cross-state record.

If the complete decoration is old, full signed-state reconstruction fixes the
entire allocation, charity bundle, graph, target support, and labels.  The
survivor is consequently an **exact paid four-edge decorated-record repeat**,
not a generic old response.  Closing that exact repeat remains the live gate.

Files:

- `results/FORM2_SIX_BRANCH_ALL_TARGET_CHANGE_REPEAT_FRONTIER_20260814.md`
- `results/form2_six_branch_all_target_change_audit.json`
- `tracks/parkability/audit_form2_six_branch_all_target_change.py`

### 8. Exact repeat does not force rank four

An exact positive-rational witness now combines an actual all-target-changing
six-branch allocation with the canonical owner-only five-response relation

```text
r -> q, q -> s, s -> r, d -> q, d -> r.
```

The branch is a four-edge spanning tree, every owner is above a declared unit
payment floor, its singleton desired cores are common-safe, and the complete
allocation is non-EFX.  Nevertheless every response targets only `r,q,s`,
so the maximum response matching has rank exactly three.  Repetition of the
complete physical record does not change that fact.

This refutes automatic admission through matching augmentation.  It is not a
full saturated GG countermodel: the remaining proof must genuinely use the
base-margin/direct-safety, generalized-PI, progress, supplier-capture, or
double-margin premises.

Files:

- `results/FORM2_ALL_TARGET_CHANGE_EXACT_REPEAT_RANK_NO_GO_20260814.md`
- `results/form2_all_target_change_exact_repeat_rank_no_go_audit.json`
- `tracks/parkability/audit_form2_all_target_change_exact_repeat_rank_no_go.py`

### 9. Root-star different-source leaf liquidation

The first different represented source after root-source double absorption
now has a direct four-edge continuation.  If `y` responds into the other
nonempty residual target `R_z`, positivity permits moving the whole `R_z` to
`y` and parking the singleton at `z`.  Relative to the saturated support,
the only supplier pairs are

```text
y -> root, z -> root, z -> y, charity -> z.
```

The root retains its permanent strict anchor and `y` strictly improves.  If
the allocation is not EFX, the singleton target cannot be responsible for a
failure.  A response involving `d` recruits all four owners; every other
survivor is confined to just two represented targets.  Thus the former
arbitrary different-source continuation has been reduced to a two-target
represented residual.  The lemma explicitly assumes both depleted residuals
are nonempty; exhaustion is the separate strict support-consumption exit.

Files:

- `results/R3_ROOT_STAR_DIFFERENT_SOURCE_LEAF_LIQUIDATION_LEMMA_20260814.md`
- `results/r3_root_star_different_source_leaf_liquidation_audit.json`
- `tracks/parkability/audit_r3_root_star_different_source_leaf_liquidation.py`

### 10. Two-target favorable root-path repair

The two-target residual has exactly three Hall-matching shapes: the internal
`x <-> y` cycle, a backward/root-loss path, and the favorable path
`z -> x -> y`, where `x` is the strict root and `z` holds the singleton.  The
internal cycle is PI.  In the favorable path, if the `z -> x` response core
lies inside `z`'s displaced supplier cell, reversing both responses and
parking the singleton at `y` creates no new owner pair.  The final support is
contained in

```text
y -> x, z -> x, z -> y, charity -> y.
```

The root and singleton source are strict.  This gives another cap-free
four-edge candidate.  The exact survivors are now the backward/root-capture
path, the singleton-source two-target star, indispensable foreign-support
import by `z`, or an exact repeated response at the explicit candidate.

Files:

- `results/R3_TWO_TARGET_ROOT_PATH_SUPPLIER_COMPATIBILITY_LEMMA_20260814.md`
- `results/r3_two_target_root_path_supplier_compatibility_audit.json`
- `tracks/parkability/audit_r3_two_target_root_path_supplier_compatibility.py`

### 11. Exact foreign-import cancellation and margin

The favorable root path has now been decomposed into five original-supplier
cells.  Its final edge count is exactly one charity edge plus five explicit
Boolean owner-pair indicators.  At most three of those indicators may remain.
This is an if-and-only-if four-edge criterion, not another sufficient menu.

In the maximal nondegenerate signature there are 208 none/proper/all response
patterns.  Exactly 69 meet the four-edge bound; 53 of those 69 genuinely use
foreign support.  Thus restricting the singleton holder's response to its own
support would incorrectly discard most edge-feasible foreign-import cases.

If no own-support subcore is desired, the foreign portion `F` of an
inclusion-minimal response carries its entire strict response margin:

```text
v_z(F) >= mu_z > 0, and v_z(g) >= mu_z for every good g in the core.
```

The surviving obstruction is therefore an edge-incompatible, item-critical
foreign packet, suitable for the signed PI/base-margin machinery.

Files:

- `results/R3_TWO_TARGET_FOREIGN_IMPORT_EDGE_CANCELLATION_AND_MARGIN_LEMMA_20260814.md`
- `results/r3_two_target_foreign_import_edge_cancellation_audit.json`
- `tracks/parkability/audit_r3_two_target_foreign_import_edge_cancellation.py`

### 12. Root-compensated direct return

A second selector omits the root's response transfer: return the singleton
holder's desired core directly, give the singleton to the protected root, and
leave the other target unchanged.  The singleton source is automatically
strict.  The root remains strict exactly when

```text
v_x(D_z) < delta_x + v_x(p).
```

Failure is therefore the exact double-margin capture
`v_x(D_z) >= delta_x + v_x(p)`, not an untyped payment hole.  The direct
selector has an independent if-and-only-if four-edge criterion: 10 of 26
nonempty three-cell signatures qualify.  Combined with the full root-path
selector, it raises signed-support coverage from 69 to 102 of the 208
five-cell signatures, rescuing 33 patterns that the first selector alone
missed.

Files:

- `results/R3_SINGLETON_SOURCE_ROOT_COMPENSATED_DIRECT_RETURN_LEMMA_20260814.md`
- `results/r3_singleton_source_root_compensated_direct_return_audit.json`
- `tracks/parkability/audit_r3_singleton_source_root_compensated_direct_return.py`

### 13. Singleton-retained partial return

Keeping the singleton at `z` removes the need for the returned packet to stay
desired: any nonempty addition strictly improves `z`.  A subpacket of the
root response fits in four edges exactly when it can be chosen from displaced
`z` support, or when the response contains the whole `y`-supplied cell so
that `y -> x` is replaced by `y -> z`.

This produces a partial-return topology for 21 of the 26 nonempty response
signatures, including 11 signatures whose whole-core direct return exceeds
the edge budget.  Only five uncompensated signatures remain.  Choose the
least root-valued packet among every available displaced-`z` singleton and
the whole `y` cell.  Either its root value is below the strict root margin and
it gives a four-edge probe, or every such packet captures the entire root
margin.

Files:

- `results/R3_SINGLETON_RETAINED_PARTIAL_RETURN_TOPOLOGY_OR_ROOT_CAPTURE_LEMMA_20260814.md`
- `results/r3_singleton_retained_partial_return_audit.json`
- `tracks/parkability/audit_r3_singleton_retained_partial_return.py`

### 14. Every two-target support signature is now covered

The five residual topology signatures were artifacts of requiring the
returned packet to lie inside the response core.  Because `z` keeps the
positive singleton, any positive incoming packet improves it.  The universal
menu is therefore: return one good from the `z -> root` cell, return the whole
`y -> root` cell, or—when neither exists—move one root-supplied good.  Each
choice reuses, replaces, or adds at most one pair, so every presence pattern
stays within four edges.

The two-target topology obstruction is eliminated completely.  Either a
minimum menu packet costs less than the root's strict margin and gives a
priority-valid four-edge probe, or every displaced-`z` singleton and the
whole displaced-`y` cell individually capture that entire margin.  The live
branch is root-critical incoming support plus observer/repeat closure, not
packet topology.

Files:

- `results/R3_SINGLETON_RETAINED_INCOMING_CELL_RETURN_LEMMA_20260814.md`
- `results/r3_singleton_retained_incoming_cell_return_audit.json`
- `tracks/parkability/audit_r3_singleton_retained_incoming_cell_return.py`

## Critical resume correction

Do **not** resume the old three-menu driver by supplying only
`allocated_e_form2_three_topology_menu_cegar_resume19747.json`.  That file
stores only its `5,666` fresh cuts; the old driver's resume loader is not
recursive.  The interrupted file
`allocated_e_form2_three_topology_menu_cegar_resume25413.json` therefore
loaded only `5,666` cuts, ended `UNKNOWN` on interruption, and is not a valid
continuation of the full pool.

The widened runner correctly accepts multiple cut sources.  Resume the live
decision with exactly:

```bash
cd /private/tmp/efx-charity-exchange-20260812
python -m tracks.parkability.run_allocated_e_form2_response_branch_menu_cegar \
  --output results/allocated_e_form2_response_branch_menu_cegar_continued.json \
  --cut-source results/allocated_e_form2_three_topology_menu_cegar.json \
  --cut-source results/allocated_e_form2_three_topology_menu_cegar_resume19747.json \
  --timeout-seconds 1800 \
  --random-seed 887 \
  --maximum-iterations 20 \
  --maximum-families-per-round 10000
```

The raw source traces remain present and untracked in this worktree.  If
starting from a clean clone, expand the two committed `.json.gz` files to the
displayed raw filenames first.

## Exact next theorem target

The highest-leverage cap-free statement is now:

> In a complete signed form-2 saturated record, either a shared-target
> response uncrosses into the six-branch menu, its overlap produces the
> certified double-margin packet, or the three simultaneous supplier-capture
> inequalities force a release-compatible generalized-PI family or the exact
> full-owner decorated-response/base-margin terminal.

For a paid non-EFX branch, this now factors through two exact alternatives.
If a net base-relative cut appears, it is a closed aggregate base-support
block `X(K)=Z(K)`, not necessarily an edgewise base return.  Independently,
all five current targets change, so saturation reduces any non-new response
to an exact paid four-edge cross-state decorated-record repeat.

The immediate theorem target is therefore:

> Prove that an exact paid four-edge decorated-record repeat satisfies the
> represented-component base-margin/direct-safety terminal, or forces
> release-compatible generalized PI/progress; otherwise construct an exact
> positive rational saturated countermodel to that implication.

Do not attempt to discharge this statement by deriving rank four from exact
repetition alone; the witness in section 8 rules out that shortcut in the
applicable owner-only response geometry.

For the root-source represented-star branch, apply section 9 before returning
to generic repeat analysis.  Its remaining local target is the signed
two-target residual: either return the singleton holder's existing supplier
cell without adding an edge, or prove that every indispensable foreign-support
import activates PI, support refinement, or full-owner admission.  The two
later-source stars still terminate at the anchor critical-packet separator.

This should be attacked using the complete signed support-drainage and
response-saturation record.  Scalar inequalities alone cannot close it: the
exact rational witness in
`FORM2_THREE_MENU_SCALAR_FEASIBILITY_GAP_20260814.md` already proves that
such a scalar-only argument is impossible.

## Verdict-dependent next actions

If the widened run is `UNSAT`:

1. Extract a tracked PI-cut core using an independently generated 973-member
   allocation menu.
2. Replay the core alone.
3. Audit every core witness combinatorially in a checker that does not import
   the master or menu generator.
4. Partition the core into three-owner versus four-owner families and mine
   the shortest support-pattern implication.
5. State the result only as a twelve-atom bounded theorem until the
   three-supplier-capture implication is proved cap-free.

If it is `SAT_NO_GENERALIZED_PI`:

1. Freeze the exact rational values and independently verify every premise.
2. Enumerate every complete allocation using at most four physical supplier
   pairs, not only the nine-topology menu.
3. If an outside-menu EFX allocation exists, add its topology and explain the
   missing analytic branch.
4. Only a profile satisfying the complete saturated premise ledger items
   1--12 and defeating every four-edge allocation can refute the frozen
   theorem.

If it again reaches `UNKNOWN` or an iteration limit, do not keep extending
the empirical three-topology campaign.  Preserve the exact cut pool and move
effort to the three supplier-capture/full-owner implication above.

## Review still required

External or genuinely independent review remains necessary for:

1. statement integrity of the saturated fixed-`U` premise ledger, especially
   that items 7--12 are noncircular continuation exclusions;
2. the claimed interface from a paid non-EFX branch to a fully decorated
   response with the exact signed margins required by the full-owner theorem;
3. the `UNIVERSAL_FULL_OWNER_CHARITY_EXCHANGE_EXTRACTION_THEOREM_20260812.md`
   proof, whose present audit checks its declared algebraic/graph identities
   but does not independently derive every GG continuation implication;
4. an independent algebraic encoding of any future UNSAT core; and
5. novelty and literature positioning after, not before, a cap-free lemma is
   obtained.

Do not use the earlier EFX2 claim that commit `34709c9` closes every
`T_{L,times}^*` collision.  Its nonroot normalization-bypass branch is
explicitly open in `NONROOT_NORMALIZATION_BYPASS_COLLISION_GAP_20260814.md`.

## Verification and process state

Focused verification across the three- and nine-topology menus, independent
menu audit/core extraction, payment identities, spanning frontier,
cancellation theorem, all-target-change frontier, repeat-rank no-go, and
root-star leaf liquidation, two-target root-path repair, and foreign-import
cancellation, root-compensated direct return, and singleton-retained partial
return and universal incoming-cell return:

```text
17 passed in 22.33s
```

All solver processes launched after the checkpoint have exited.  Nothing
campaign-critical is running.  The worktree contains many
older unrelated untracked research traces and two pre-existing modified
files; they were deliberately neither staged nor reverted.

The active `/goal` should remain open.  The fixed rank-three theorem, general
four-agent additive EFX, and general additive EFX are all unresolved.
