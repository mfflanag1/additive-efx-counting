# EFX fixed-U breakthrough handoff

**Date:** 2026-08-14

**Workspace:** `/private/tmp/efx-charity-exchange-20260812`

**Branch:** `codex/efx-fixed-u-termination-20260813`

**Latest pushed research checkpoint before this note update:** `245bc5b`
(`research: isolate exact form2 record-repeat frontier`)

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
cancellation theorem, and all-target-change frontier:

```text
10 passed in 27.84s
```

All solver processes launched after the checkpoint have exited.  Nothing
campaign-critical is running.  The worktree contains many
older unrelated untracked research traces and two pre-existing modified
files; they were deliberately neither staged nor reverted.

The active `/goal` should remain open.  The fixed rank-three theorem, general
four-agent additive EFX, and general additive EFX are all unresolved.
