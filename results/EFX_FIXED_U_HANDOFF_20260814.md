# EFX fixed-U breakthrough handoff

**Date:** 2026-08-14

**Workspace:** `/private/tmp/efx-charity-exchange-20260812`

**Branch:** `codex/efx-fixed-u-termination-20260813`

**Latest pushed checkpoint:** `b2f6fe8` (`research: widen form2 four-edge menu`)

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

The widened solver was intentionally interrupted for this handoff before its
first check completed.  Its untracked output
`results/allocated_e_form2_response_branch_menu_cegar.json` has status
`UNKNOWN`, reason `interrupted from keyboard`, with zero new iterations and
the correct `25,413` loaded cuts.  It is not evidence and should not be cited.

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

Focused verification at checkpoint `b2f6fe8`:

```text
6 passed in 0.33s
```

The two solver processes launched after that checkpoint were interrupted and
exited.  Nothing campaign-critical is running.  The worktree contains many
older unrelated untracked research traces and two pre-existing modified
files; they were deliberately neither staged nor reverted.

The active `/goal` should remain open.  The fixed rank-three theorem, general
four-agent additive EFX, and general additive EFX are all unresolved.
