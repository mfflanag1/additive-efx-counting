# EFX fixed-U breakthrough handoff

**Date:** 2026-08-14

**Workspace:** `/private/tmp/efx-charity-exchange-20260812`

**Branch:** `codex/efx-fixed-u-termination-20260813`

**Latest pushed research checkpoint before this note update:** `c805c5f`
(`research: split terminal path cross-exchange cases`)

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

### 15. Global pivot: permanent-anchor disjoint-response transfer

The higher-leverage permanent-anchor route now tests the singleton at only
the three nonroot owners, avoiding the unresolved root-held hit branch.  If a
globally minimum response is disjoint from the singleton, transport makes it
safe across all three probes and desired away from its own-source placement.

Transfer that response to its source and leave the singleton with its old
nonroot target.  A nonroot target adds only one owner pair, so the candidate
uses at most three edges.  A root target contains only the current-root and
anchor-supplier cells, so its mixed response still uses at most four edges.
Every nonroot-target response is priority-valid.  A root-target response is
priority-valid unless it captures the complete strict root margin:

```text
v_r(E) >= delta_r.
```

Thus the disjoint normalization-bypass branch no longer needs Hall matching
just to construct a bounded-edge probe.  Its survivors are root-margin
capture or an exact repeated response after the explicit transfer.  A
singleton-hitting response remains in the separately typed nonroot envelope
descent; the lemma does not conflate its changed endpoint with an original
probe.

Files:

- `results/PERMANENT_ANCHOR_NONROOT_THREE_PLACEMENT_RESPONSE_TRANSFER_LEMMA_20260814.md`
- `results/permanent_anchor_nonroot_three_placement_response_transfer_audit.json`
- `tracks/parkability/audit_permanent_anchor_nonroot_three_placement_response_transfer.py`

### 16. Root-target aggregate capture reduced to itemwise criticality

For a disjoint transported response `E` targeting the permanent-anchor root,
choose a good `g` of minimum root value.  Instead of transferring all of `E`,
give only `g` and the charity singleton to the nonroot response source.  The
source strictly improves by positivity.  Relative to the current support,
the allocation uses at most three supplier pairs whether `g` came from the
old root cell or from the anchor-supplier cell.

The root stays strictly above its base exactly when

```text
v_r(g) < delta_r.
```

If that inequality fails, minimality of `g` implies the stronger itemwise
envelope

```text
v_r(e) >= delta_r for every physical good e in E.
```

Thus the former aggregate root-capture survivor is now either an explicit
three-edge priority probe or a response in which every good individually
consumes the full root margin.  A non-EFX probe again yields a fully decorated
response/repeat continuation.  The item-critical envelope and exact-repeat
recurrence are still open; this is not termination of the root-target branch.

Files:

- `results/PERMANENT_ANCHOR_ROOT_TARGET_MINIMUM_GOOD_DIVERSION_LEMMA_20260814.md`
- `results/permanent_anchor_root_target_minimum_good_diversion_audit.json`
- `tracks/parkability/audit_permanent_anchor_root_target_minimum_good_diversion.py`

### 17. Exact bilateral frontier and direct-safety wall

The minimum-good probe was not sharp: its source already improves from any
positive root packet, so charity should compensate the root.  The strengthened
selector exchanges arbitrary packets `H subseteq B_r` and `D subseteq B_i`,
and gives the singleton to the root.  The source and root conditions are

```text
v_i(H) > v_i(D),
v_r(H)-v_r(D) < delta_r+v_r(p).
```

There is an exact support criterion.  The exchange exceeds four edges only
when the non-`q` source returns a nonempty compensator, `H` hits both root
supplier cells, and `H` leaves a proper anchor residual.  Every other packet
pair fits within four edges.

If no admissible pair works, every source-affordable compensator satisfies

```text
v_r(D) <= v_r(H)-delta_r-v_r(p).
```

In particular, every nonempty root packet costs at least
`delta_r+v_r(p)`.  More importantly, the desired response makes the complete
bundle swap `H=B_r,D=B_i` source-improving and edge-feasible.  Failure of that
probe is exactly

```text
v_r(B_i)+v_r(p) <= v_r(X_r),
```

a direct-safety wall rather than an untyped root-capture inequality.  An exact
positive-additive local witness satisfies every bilateral failure inequality,
so positivity and the two payment rows alone cannot finish the branch.  The
next proof must connect this wall to the full signed base-margin/direct-safety
terminal or use another observer/PI premise.

Equivalently, failure with the empty compensator says

```text
v_r(B_r-H)+v_r(p) <= v_r(X_r)  for every nonempty H subseteq B_r.
```

Thus every one-good deletion of the current root target, after adding
charity, is safe to the root at its old base floor.  Setting `H=A` gives the
particularly clean permanent-anchor wall
`v_r(Y_r)+v_r(p)<=v_r(X_r)`.  This complement-safety form is the sharpest
current interface to the saturated extraction machinery.

Files:

- `results/PERMANENT_ANCHOR_ROOT_TARGET_BILATERAL_COMPENSATOR_FRONTIER_LEMMA_20260814.md`
- `results/permanent_anchor_root_target_bilateral_compensator_frontier_audit.json`
- `tracks/parkability/audit_permanent_anchor_root_target_bilateral_compensator_frontier.py`

### 18. Incoming-root cells never create an edge obstruction

At any strict-root allocation already using at most four supplier pairs,
move a complete nonroot-supplied root cell to any nonroot owner.  The move
deletes `supplier -> root` and replaces it by at most
`supplier -> recipient`; if the recipient is the supplier, the cell simply
returns.  The edge count never increases, and the recipient strictly
improves by positivity.

Therefore every incoming root cell gives either another named four-edge
probe or the exact capture inequality

```text
v_r(K_s) >= current root margin.
```

At a permanent-anchor bilateral probe this applies independently to the
residual anchor cell, the returned compensator cell, and the charity
singleton.  Topology is now eliminated for all of them.  Only root-origin
residual support can require a fifth edge; simultaneous full-margin capture
and decorated-response recurrence remain open.

Files:

- `results/STRICT_ROOT_INCOMING_CELL_DIVERSION_OR_CAPTURE_LEMMA_20260814.md`
- `results/strict_root_incoming_cell_diversion_or_capture_audit.json`
- `tracks/parkability/audit_strict_root_incoming_cell_diversion_or_capture.py`

### 19. Same-source root-response recurrence reduced to capture

At a bilateral probe `(H,D)`, suppose the next root-target response `F` lies
in untouched original-root support and has the same source as `H`.  Return
`H` and replace it by `F`, retaining `D` and charity.  Because `F` is desired
above the source's entire probe bundle, the replacement is admissible and
strictly increases that identical source's utility.

The replacement exceeds four edges only in one exact signature: the source
is not `q`, `D` is nonempty, and `F` meets both original root supplier cells
while leaving a proper anchor residual.  Completing the anchor deletes the
extra `q -> root` edge.  Thus every case gives a four-edge strict-progress
probe unless

```text
v_r(F)-v_r(D) >= delta_r+v_r(p),
```

or the same inequality holds after anchor completion.  Exact same-source
residual recurrence is therefore no longer an untyped survivor.  The live
response cases are a different source, typed simultaneous root capture, or
the singleton-hit changed-state continuation.

Files:

- `results/PERMANENT_ANCHOR_SAME_SOURCE_ROOT_RESPONSE_REPLACEMENT_LEMMA_20260814.md`
- `results/permanent_anchor_same_source_root_response_replacement_audit.json`
- `tracks/parkability/audit_permanent_anchor_same_source_root_response_replacement.py`

### 20. Two-source root responses have one irreducible cross

Conditional on transporting two distinct-source, disjoint safe desired cores
to the same permanent-anchor root state, their simultaneous topology is now
exact.  Across 96 two-supplier presence signatures, 76 already fit within
four edges.  Returning the complete residual anchor cell to `q` repairs 16
of the 20 overflows.

The only four survivors are the same `2 x 2` cross: sources `d,s` each need
nonempty support from both the root-origin and anchor-supplier cells.  If one
source still desires one pure supplier portion, replace its mixed core by a
minimal pure subcore and return the recomputed anchor residual; this uses
three owner pairs plus charity.  Otherwise all four source/cell portions
capture their respective source's complete response margin.

Thus different-source topology reduces to a four-edge probe, root capture,
or a two-source/two-supplier cross-capture certificate.  The load-bearing
gap is now cross-state transport: responses extracted at two different
bilateral probes are not yet proved simultaneously safe and desired at one
fixed state.

Files:

- `results/PERMANENT_ANCHOR_TWO_SOURCE_ROOT_RESPONSE_TOPOLOGY_OR_CROSS_CAPTURE_LEMMA_20260814.md`
- `results/permanent_anchor_two_source_root_response_topology_or_cross_capture_audit.json`
- `tracks/parkability/audit_permanent_anchor_two_source_root_response_topology_or_cross_capture.py`

### 21. Cross-state transport is closed by safe normalization

Two consecutive different-source root responses are discovered at probes
where their respective sources are unchanged, so both cores are desired
above the fixed bundles `B_u,B_v`.  Place the singleton at the unique third
nonroot owner.  This restores the complete root target `B_r` and leaves both
sources at those fixed bundles, giving a common two-edge probe where both
cores are simultaneously desired.

If either core is unsafe there, an observer desires a one-good deletion.
Replace the core and its source, and repeat.  Cardinality strictly decreases,
so normalization terminates with a common-safe desired core.  Normalizing
both initial cores ends either in a source collision, which returns to the
one-source branch, or in two distinct safe cores at the same state.  The
latter enter shared-target uncrossing and the exact two-source topology
theorem.

Thus cross-state safety and desire are no longer the missing implication.
The remaining distinct-source alternatives are root capture, overlap double
capture, or the two-source/two-supplier cross-capture certificate.

Files:

- `results/PERMANENT_ANCHOR_DIFFERENT_SOURCE_CROSS_STATE_NORMALIZATION_LEMMA_20260814.md`
- `results/permanent_anchor_different_source_cross_state_normalization_audit.json`
- `tracks/parkability/audit_permanent_anchor_different_source_cross_state_normalization.py`

### 22. Full original-root residual can always be liquidated

There is no scalar or edge-count obstruction when the permanent-anchor root
target has a nonempty original-root residual.  Write

```text
B_r = Y_r disjoint-union A,    v_r(A) > v_r(X_r).
```

Move all of `Y_r` to any nonroot owner, leave only `A` at the root, and give
the charity singleton to that same owner.  Relative to the original current
allocation this uses at most `q -> r`, `r -> i`, and `charity -> i`.  The
root remains strictly above base and the recipient strictly improves.

Algebraically,

```text
v_r(Y_r) = v_r(B_r)-v_r(A)
         < v_r(B_r)-v_r(X_r) = delta_r,
```

so the universal bilateral-failure wall
`v_r(Y_r) >= delta_r+v_r(p)` is impossible.  This is the `H=Y_r`, `D=empty`
instance of the already recorded strict-root surplus probe, not a new global
closure theorem.

The exact remaining obstruction is semantic: if the probe is non-EFX, the
frozen response/collision argument still has to handle a nonroot holder
whose repeated normalized response avoids the retired packet.  The
corollary therefore closes physical routing and payment only; it does not
close `NONROOT_NORMALIZATION_BYPASS_COLLISION_GAP_20260814.md`.

File:

- `results/PERMANENT_ANCHOR_FULL_RESIDUAL_LIQUIDATION_COROLLARY_20260814.md`

### 23. The frozen target always has nonempty original-root residual

The symbol-level interface left open in section 22 is now resolved.  Premise
ledger item 4 mandates the response `d -> r`; item 5 gives that decorated
response a nonempty desired core inside its literal physical target support.
That target is `Y_r`, so every frozen target state has `Y_r != empty`.

Consequently every target state—not merely a conditional face—admits the
complete three-edge liquidation probe with root bundle exactly `A`.  The
audit checks the strict-margin algebra and all nine anchor-source/residual-
recipient role combinations.

Files:

- `results/FIXED_U_ROOT_RESIDUAL_NONEMPTY_LIQUIDATION_REDUCTION_LEMMA_20260814.md`
- `results/fixed_u_root_residual_nonempty_liquidation_audit.json`
- `tracks/parkability/audit_fixed_u_root_residual_nonempty_liquidation.py`

### 24. Direct three-placement continuation avoids collision/reset semantics

Fix any nonroot recipient `k` for `Y_r` and place the charity singleton in
turn at the three nonroot owners.  All probes have pure root target `A`, a
strict root, and at most three edges.  A globally smallest response that
avoids `p` is safe at all three probes and desired at a placement away from
its own source.

Every nonroot-target response can then be executed within four edges.  If
the response targets the mixed residual holder, transferring the complete
`Y_r` cell deletes the only possible fifth edge.  A root-target response can
be executed within three edges after returning `Y_r` and `p` to the root,
unless

```text
v_r(E) >= delta_r + v_r(p).
```

Thus the direct route has no packet-size or topology survivor and does not
use the controlled floor reset or the disputed collision theorem.  Its
remaining branches are singleton-hit descent, a non-EFX transfer's exact
decorated recurrence, or the displayed p-augmented root capture.

Files:

- `results/FIXED_U_LIQUIDATED_ROOT_THREE_PLACEMENT_RESPONSE_FRONTIER_LEMMA_20260814.md`
- `results/fixed_u_liquidated_root_three_placement_response_frontier_audit.json`
- `tracks/parkability/audit_fixed_u_liquidated_root_three_placement_response_frontier.py`

### 25. Root capture repairs by a full-source swap or becomes direct safety

For a captured root response `E subseteq A` with source cell `S_i`, transfer
all of `S_i` to the root, return `Y_r`, give the charity singleton to the
root, and give `E` to its source.  If the anchor supplier is distinct from
the response source, its whole residual cell `Q_i=Y_q-A` also goes to the
root on the already active `q -> r` edge.  Desire above the source's complete
probe bundle pays the source even when it was holding `Y_r`.  The allocation
uses at most four edges.

It preserves the strict root exactly when

```text
v_r(E)-v_r(S_i)-v_r(Q_i) < delta_r+v_r(p).
```

Failure strengthens to

```text
v_r(S_i)+v_r(Q_i)+v_r(p) <= v_r(E)-delta_r
                          <= v_r(X_r)-v_r(Y_r)
                          <  v_r(X_r).
```

Raw aggregate capture is therefore no longer the terminal.  The live scalar
branch is strict direct safety of the response source's entire ordinary cell,
the distinct anchor supplier's residual cell, and charity; the other live
branch is the exact decorated response after a priority-valid full-source
swap.

Files:

- `results/LIQUIDATED_ROOT_RESPONSE_FULL_SOURCE_SWAP_FRONTIER_LEMMA_20260814.md`
- `results/liquidated_root_response_full_source_swap_frontier_audit.json`
- `tracks/parkability/audit_liquidated_root_response_full_source_swap_frontier.py`

### 26. Unmerged all-unsafe reservoir-fan PI claim is corrected

The unmerged collision branch at `34709c9` contains another implication that
must not be imported as stated.  Four pairwise-disjoint safe desired cores
with four distinct sources do force generalized PI: use the closed disjoint-
core theorem on all four owners, for which base-owner closure is automatic.

But when sources repeat, a cycle in the **current supplier** graph is not
enough.  Generalized PI uses base ownership and released base packets.  An
exact four-singleton response profile has the current cycle `0 <-> 1` while
the two cycle packets are base-owned by `2,3`; sources `2,3` are missing, and
no closed desired-core family exists.

The exhaustive nonself source-map census is:

```text
image size 4:  9 maps   -> generalized PI
image size 3: 48 maps   -> one missing and one duplicated source
image size 2: 24 maps   -> multiplicity 2+2 or 3+1
```

Thus the corrected rank-three survivor is exactly a missing-source Hall
defect.  Adding a disjoint core for the missing frozen source gives four-
source PI; otherwise that source's complete response margin is captured by
the fan union.  Reversing that capture within four edges is the live branch.

Files:

- `results/NORMALIZATION_BYPASS_THREE_RESERVOIR_FAN_CORRECTION_LEMMA_20260814.md`
- `results/normalization_bypass_three_reservoir_fan_correction_audit.json`
- `tracks/parkability/audit_normalization_bypass_three_reservoir_fan_correction.py`

### 27. The `3+1` missing-source defect forces double capture

Write the duplicated source's disjoint fan cores as `D_1,D_2`, the other
represented cores as `U,V`, and the missing source's response as `C` with
strict margin `mu`.  Either choice

```text
U union V union D_j,   j in {1,2},
```

would combine with a disjoint remainder of `C` to give four-source
generalized PI.  Hence PI-freeness forces capture for both choices.  With

```text
H = C intersect (U union V),
P_j = C intersect D_j,
```

the exact inequalities are

```text
v_m(H)+v_m(P_1) >= mu,
v_m(H)+v_m(P_2) >= mu.
```

Therefore either `H` already captures the whole missing-source margin, or
the two pairwise-disjoint packets `P_1,P_2` each capture the same positive
residual margin.  The 48 source maps split exactly 24/24 according to whether
the missing owner supplies one duplicated-source core.

Files:

- `results/MISSING_SOURCE_TWO_CHOICE_FAN_DOUBLE_CAPTURE_LEMMA_20260814.md`
- `results/missing_source_two_choice_fan_double_capture_audit.json`
- `tracks/parkability/audit_missing_source_two_choice_fan_double_capture.py`

### 28. Duplicate omission pays every owner in one 24-map class

When the missing owner supplies one duplicated-source core, omit that core,
use the duplicate's other core, transfer one core to each of the three
represented sources, and give charity to the missing owner.  All represented
sources strictly improve and the missing owner retains its whole bundle plus
charity.

This is unconditionally an all-owner-payment construction with three
current-holder moves plus charity.  It is **not automatically** a four-edge
construction in the objective's metric: a later-state target may mix several
original-`Y` supplier cells.  Its exact physical condition is that the three
selected cores induce at most three distinct original-supplier/source pairs.
The other 24 maps and failure of this support condition remain live.

Files:

- `results/MISSING_SUPPLIER_DUPLICATE_OMISSION_FOUR_EDGE_PAYMENT_LEMMA_20260814.md`
- `results/missing_supplier_duplicate_omission_four_edge_payment_audit.json`
- `tracks/parkability/audit_missing_supplier_duplicate_omission_four_edge_payment.py`

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

The direct liquidated-root route now supersedes the collision-based shortcut
as the first attack.  Its shortest live implication is:

> In the frozen saturated record, simultaneous failure of the three
> liquidated-root singleton placements and their direct response transfers
> forces either the nonroot singleton-hit terminal, a new decorated record,
> release-compatible generalized PI/progress, or the represented-component
> terminal.  In the root-response branch, combine the strict direct-safety
> wall `v_r(S_i)+v_r(Q_i)+v_r(p)<v_r(X_r)` with the other signed
> observer/source rows;
> otherwise construct a full-premise positive-rational countermodel.

Do not treat the two-edge charity relay as unconditional.  Its reset-
admission theorem exists at commit `34709c9`, outside this branch's ancestry,
and explicitly requires a separate physical progress argument.  The direct
three-placement route above does not depend on it.

Likewise, do not import that commit's claim that every current-supplier cycle
in the all-unsafe reservoir fan is generalized PI.  Section 26 gives an exact
counterexample.  The correct continuation must handle the missing-source
capture, not declare the repeated-source fan closed.

After sections 27--29 the corrected reservoir-fan target is:

> In the 24 foreign-duplicate-supplier maps, reverse the common-overlap or
> two-packet residual capture while cancelling enough original supplier
> pairs to stay within four edges.  In the other 24 maps, prove the three
> selected fan cores satisfy the original-supplier support condition or use
> a supplier completion/cancellation before invoking the all-owner-paid
> observer continuation.

## 29. Conditional liquidated-root whole-cell physical frontier

The final bounded topology census is recorded in
`LIQUIDATED_ROOT_THREE_SOURCE_PHYSICAL_COMPRESSION_FRONTIER_LEMMA_20260814.md`
and its byte-replayed JSON audit.  For each fixed anchor supplier, all 48
nonself image-three source maps were minimized over the allowed duplicate
omission and all four destinations of the complete root residual `Y_r`.

Inside this conditional normal form, exactly 42 maps use at most four
original supplier-to-destination pairs.  The
minimum distribution is 14 maps at three edges, 28 at four, and six at five.
The six survivors are precisely the root-missing, missing-supplies-duplicate
maps.  Their whole-cell construction has three nonroot source moves, the
anchor-supplier return to the root, and charity to the root.  Rerouting `Y_r`
cannot cancel one of those five pairs.

This does **not** unconditionally strengthen section 28.  The accumulated
reservoir-fan cores may mix several original-`Y` suppliers, and a response
core may depend jointly on the routed `Y_r` packet.  The census applies only
after proving that each selected core lifts to its displayed pure cell and
remains paying when `Y_r` is routed independently.  That lift is open.

This is not a proof over the actual mixed-support fan or arbitrary packet
graphs, and it does not establish observer EFX.  The immediate resume target
is the pure-cell lift or a direct treatment of the exact support set `Pi` in
section 28.

### Correction: the generic pure-cell lift is false

`PURE_CELL_RESPONSE_LIFT_LOCAL_REFUTATION_20260814.md` gives the exact
two-good witness.  At source floor `10`, a mixed core with values `6` and `5`
is desired and common-safe, while neither original-supplier component is
desired.  Therefore routing `Y_r` independently can destroy the payment
premise.  The pure-cell census remains a correct conditional combinatorial
result, but it cannot be used to close any of the 48 actual fan maps without
an additional saturation-derived support theorem.

Inside that same conditional model,
`ROOT_MISSING_ANCHOR_SUBSTITUTION_OR_CRITICAL_SPLIT_LEMMA_20260814.md`
shows that the six idealized five-edge maps have a second four-edge probe:
send the anchor to its duplicated source and omit the other target paying
that source.  Only root payment can fail.  When the duplicated source equals
the anchor supplier, a partial-anchor split gives a precise bicriteria
critical packet.  This remains conditional and is not part of the universal
fixed-`U` closure.

## 30. Three-color mixed-support compression no-go

`THREE_COLOR_MIXED_SUPPORT_HALL_COMPRESSION_REFUTATION_20260814.md`
isolates the exact reason the actual support set `Pi` cannot be controlled by
PI-freeness alone.  Base owner, frozen-`Y` supplier, and later target holder
are three different labels.

The exact six-good family has three disjoint two-good cores for sources
`1,2,3`.  Every good is base-owned by missing source `0`, so no nonempty
represented-source subfamily is base-closed and the displayed cores produce
no generalized PI.  Each core has source values `6+5>10`, while neither
singleton is desired, so both supplier components are indispensable.  The
three reversals use exactly

```text
0->1, 3->1, 0->2, 1->2, 0->3, 2->3,
```

six frozen-supplier pairs before charity.

This is not a full fixed-`U` countermodel.  It is an exact refutation of the
reduced implication “PI-free response Hall geometry implies three physical
owner pairs.”  Any universal proof must now use the signed relation between
`X`, `Y`, and the later probe—support return/cancellation, ledger growth, or
decorated recurrence—not another owner-label Hall argument.

## 31. Full-owner connectedness isolates a pure rank defect

`IMAGE_THREE_FULL_OWNER_CONNECTED_RANK_DEFECT_LEMMA_20260814.md` proves that
all 48 nonself image-three source maps are connected on all four owners.  A
disconnected four-owner nonself map would have two two-owner components; each
would be forced to swap its two vertices, making the map surjective and
contradicting image size three.

Therefore the accumulated fan does not need another owner-recruitment step.
It already forms a full-owner current-holder/source component.  The exact
obstruction is that the component has source rank three, while the saturated
represented-component extraction theorem constructs its Hamiltonian path at
rank `|C|=4`.  PI-freeness prevents the missing source's response from being
added disjointly: its strict margin is captured by both represented-core
choices.

The shortest remaining interface is now precise: uncross the captured
missing-source response to obtain rank four, or extend saturated component
extraction to this connected rank-deficient full-owner component using the
signed base-margin ledger.  Owner connectivity itself is completely closed.

## 32. Every image-three fan has one canonical Hamiltonian omission

`IMAGE_THREE_UNIQUE_HAMILTONIAN_OMISSION_AND_HOLE_LEMMA_20260814.md`
strengthens section 31.  Of the two targets feeding the duplicated source,
exactly one can be omitted so that the remaining three response edges form
an oriented spanning path

```text
missing source -> represented source -> represented source -> omitted target.
```

This holds in all 48 maps, with a unique omission in every case.  Reversing
the three path cores and sending charity to the missing source pays all three
represented sources.  The missing source is the unique possible payment
hole because its first path-target core is removed.

The complementary omission explains the previous tradeoff.  When the
missing target supplies the duplicated source, omitting it preserves the
missing owner's whole bundle and pays everyone, but leaves the short cycle
and mixed-support edge problem.  The Hamiltonian omission removes the cycle
but exposes the missing-owner deficit.

Thus rank-three owner topology is now completely normalized.  The remaining
local theorem is not path existence: it is repair of the sacrificed missing-
owner hole using its captured mandatory response, while keeping the exact
frozen-supplier pair count and observer budgets.

## 33. Eight maps close payment; four reduce to one terminal split

Fix the actual roles `m=d` and ordinary base-response target `b=q`.
`CANONICAL_PATH_BASE_RESPONSE_PREFIX_OR_TERMINAL_SPLIT_LEMMA_20260814.md`
classifies the position of `q` on the canonical path.  Among the twelve role
maps, `q` occurs in positions one, two, and three exactly four times each.

If `q` is internal—position one or two—send its base-desired `d->q` core to
`d`, reverse only the path prefix ending at `q`, and give charity to `d`.
The core alone base-pays `d`; every owner on the prefix receives a bundle it
desires above its entire current bundle; later owners are unchanged.  These
eight maps use respectively three or four current-holder edges.

If `q` is terminal, the problem collapses to one packet `P` inside the
incoming terminal core.  Writing `Delta_i` for current base surplus and `C`
for the removed `d->q` core, choose an inclusion-minimal packet satisfying

```text
v_q(P) >= v_q(C) - Delta_q.
```

It yields a three-edge paid allocation exactly when

```text
v_predecessor(P) <= Delta_predecessor.
```

Failure leaves the exact bicriteria critical packet: every item is necessary
for compensating `q`, while the whole packet is too expensive for its
predecessor to release.  This is now the only current-holder payment gate in
the four terminal maps.  Frozen-supplier expansion and observer continuation
are separate and remain open.

## 34. The four terminal maps split into two cross exchanges and two splits

The omitted response core in terminal target `q` is desired either by the
path predecessor or by the first represented path source.  The four maps
split exactly `2+2`.

`TERMINAL_PATH_OMITTED_CORE_CROSS_EXCHANGE_FRONTIER_20260814.md` handles the
predecessor case.  If the omitted core has a desired subcore disjoint from
the missing owner's base-paying `d->q` core, exchange the predecessor and
`q` cores, send `d->q` to `d`, and give charity to `d`.  The only current-
holder pairs are

```text
predecessor->q, q->predecessor, q->d, charity->d.
```

All owners are paid.  If the two `q`-target cores cannot be uncrossed, their
overlap captures the predecessor's complete response margin.  Thus these two
maps are reduced to one shared-target capture packet.

In the other two terminal maps the omitted core pays the first represented
source, not the predecessor.  They retain the terminal bicriteria packet
from section 33, plus the same disjoint-or-capture alternative at `q`.
Frozen-supplier compression and observer safety remain open in both classes.

## 35. Overlap capture is one exact bicriteria packet

The overlap branch in the two predecessor-duplicate terminal maps is no
longer an unnamed capture inequality.  If the missing-owner core `C` and
predecessor core `E` overlap in `O`, split `O` into a packet `H` sent with
`C minus E` to the missing owner and its complement sent with `E minus C`
to the predecessor.

The two payment conditions have opposite thresholds:

```text
missing owner paid     iff v_m(H) >= alpha
predecessor paid       iff v_x(H) <= gamma.
```

The full overlap always satisfies the first threshold.  Hence an
inclusion-minimal feasible `H_*` either satisfies the predecessor threshold,
giving the paid cross exchange through at most four current-holder edges, or
is an exact two-row critical packet:

```text
v_m(H_*) >= alpha,
v_m(H_* - g) < alpha for every g in H_*,
v_x(H_*) > gamma.
```

This reduction is cap-free and exact.  It does **not** show that the critical
packet is impossible under the full signed fixed-`U` premises.  It also does
not bound the number of frozen-supplier/recipient pairs induced by mixed
provenance, and it does not prove observer EFX safety.

Authoritative files:

- `results/PREDECESSOR_CROSS_EXCHANGE_OVERLAP_BICRITERIA_LEMMA_20260814.md`
- `results/predecessor_cross_exchange_overlap_bicriteria_audit.json`
- `tracks/parkability/audit_predecessor_cross_exchange_overlap_bicriteria.py`
- `tracks/parkability/test_predecessor_cross_exchange_overlap_bicriteria.py`

The next analytic target is now narrower: combine this overlap critical
packet with the terminal compensator packet and the frozen supplier labels.
Either prove their simultaneous minimality forces a release-compatible
generalized-PI family or a saturated represented-component terminal, or
freeze an exact positive-rational full-premise countermodel.  Scalar payment
inequalities alone are not enough; the signed `X -> Y -> Z` provenance ledger
must be used.

## 36. Closed cancellation blocks are outsider-safe at saturation

The net `X -> Z` graph of a paid four-edge branch may disconnect even when
its current `Y -> Z` graph is a spanning tree. Each net component is an
exact closed base-support block `K` with `X(K)=Z(K)`.

A failed EFX comparison whose observer and target lie in different blocks
produces a globally minimal current-safe decorated response across that
block cut. Its exact record is either new, giving permanent response
augmentation, or already present, in which case the two blocks already lie
in one represented-response component. Adding a genuinely cross-component
response strictly reduces the quotient component count.

The exhaustive audit enumerates all 52 partitions of the four owners plus
charity and every quotient graph, checking 1,769 cross-component response
additions. Every addition merges exactly two components, so at most four
strict mergers are possible. At saturation, maximal response-closed unions
of cancellation blocks are therefore mutually outsider-safe.

This closes one of the two explicit cancellation-admission gates from
section 6. The remaining gate is internal response rank, together with the
signed component-margin and release hypotheses. Exact repetition alone
cannot supply that rank, as the section-8 rational no-go witness shows.

Authoritative files:

- `results/CLOSED_BASE_BLOCK_CROSS_RESPONSE_MERGER_LEMMA_20260814.md`
- `results/closed_base_block_cross_response_merger_audit.json`
- `tracks/parkability/audit_closed_base_block_cross_response_merger.py`
- `tracks/parkability/test_closed_base_block_cross_response_merger.py`

## 37. Form-2 ITE-free decision checkpoint

A new exact driver replaces every nested least-good EFX expression by the
equivalent direct family `v_i(Z_i) >= v_i(Z_j-g)` for every target good.
The equivalence is independently replayed for bundle sizes one through
twelve.

The reproducible form-2 run stopped at declared iteration limits after 33
exact rational adversarial models and 264 topology-diverse cuts. Every model
had a complete EFX allocation using at most four frozen-support edges. The
minimum edge histogram is `7/19/7` for two/three/four edges. The selected
witnesses span 141 topologies, so no small fixed-topology selector is
supported.

Across all models, three response cores are invariant whole targets:
`r->q=Q`, `d->q=Q`, and `q->s=E`. The most frequent witness is the already
known path `charity->r->s->q->d`. This points back to the cap-free endpoint
capture/shared-target packet gate; another bounded iteration extension is
not the next step.

Authoritative files:

- `results/FORM2_LINEAR_ALLOCATION_CEGAR_CHECKPOINT_20260814.md`
- `results/exact_response_form2_linear_allocation_cegar_fresh_v2_20260814.json`
- `results/exact_response_form2_linear_allocation_cegar_stage2_v2_20260814.json`
- `results/exact_response_form2_linear_cegar_checkpoint_analysis.json`
- `tracks/parkability/run_exact_response_linear_allocation_cegar.py`
- `tracks/parkability/analyze_exact_response_linear_cegar_checkpoint.py`

## 38. Charity should not be sent to an already-paid missing owner

The previous terminal construction assigned `p` to missing owner `m`, even
though its ordinary core `C` alone is strictly base-paying. Assigning
charity instead to terminal owner `q` lowers the compensation threshold;
assigning it to predecessor `x` raises the permitted donor cost. Each
placement uses at most three current-holder edges.

Joint failure produces nested packets crossing both charity-subsidy corners.
This strictly weakens the terminal obstruction in section 33; the old
construction remains correct but is payment-wise dominated.

## 39. Every terminal map has a two-level four-edge selector

Push the terminal compensation backward through the path
`m->y->x->q`. Choose `P_2` from the `x` target to compensate `q`, then
choose `P_1` from the `y` target to compensate `x`. Place charity at `q`,
`x`, or `y`.

For each placement, minimize the y-value of `P_1` subject to the q and x
payment thresholds. The feasible family is always nonempty because the
full path cores are desired above the relevant complete current bundles.
The placement succeeds exactly when this minimum is within y’s surplus
budget. Success uses only

```text
q->m, x->q, y->x, charity->{q,x,y}.
```

Thus all four terminal maps are paid within four current-holder edges unless
all three exact dynamic cost tests fail.

## 40. The predecessor maps reduce to one joint three-corner separator

In the two predecessor-duplicate maps, split the shared `q`-target overlap
between `m` and `x` while independently choosing the terminal packet sent
from `x` to `q`. Minimize both packets in the x row. Charity can lower the
m threshold, lower the q threshold, or raise the x budget.

A paid four-edge allocation exists unless all three subsidy corners lie
strictly below the two-packet predecessor-cost frontier. This jointly
subsumes the earlier overlap and terminal packet tests. The surviving
physical problem is now to realize these optimized packets within the
frozen-supplier edge budget and close any failed observer response.

Authoritative files:

- `results/TERMINAL_PATH_CHARITY_PLACEMENT_BICRITERIA_LEMMA_20260814.md`
- `results/TERMINAL_PATH_TWO_LEVEL_CHARITY_SELECTOR_LEMMA_20260814.md`
- `results/PREDECESSOR_TERMINAL_TWO_PACKET_CHARITY_SELECTOR_LEMMA_20260814.md`
- their three JSON audits and replay tests

The shortest live continuation on the permanent-anchor route is now:

> Combine the exact p-augmented root-complement wall, incoming-cell capture,
> overlap double capture, and two-source/two-supplier cross capture with the
> signed PI/base-margin premises.  Prove that their simultaneous occurrence
> forces release-compatible generalized PI or the saturated represented-
> component extraction terminal; otherwise produce a complete positive-
> rational fixed-`U` countermodel satisfying all four capture systems and the
> full saturation ledger.

The scalar survivors that remain are the direct-safety
wall `v_r(B_i)+v_r(p)<=v_r(X_r)`, simultaneous incoming-cell/root-residual
capture, and the two-source/two-supplier cross-capture inequalities.  A
scalar-only proof is impossible because the bilateral separator has an exact
positive-additive local witness.

The hitting branch must be handled separately through the nonroot
singleton-hit envelope descent.  Do not identify the changed descent endpoint
with one of the three original probes without proving the required
cross-state localization.

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
4. the permanent-anchor response-transport and minimum-good-diversion
   interfaces, especially the provenance edge count and the inference from a
   non-EFX probe to a correctly scoped cross-state decorated response;
5. an independent algebraic encoding of any future UNSAT core; and
6. novelty and literature positioning after, not before, a cap-free lemma is
   obtained.

It should additionally review the base-owner/current-supplier distinction in
section 26 before relying on any theorem from the unmerged `34709c9` branch.

Do not use the earlier EFX2 claim that commit `34709c9` closes every
`T_{L,times}^*` collision.  Its nonroot normalization-bypass branch is
explicitly open in `NONROOT_NORMALIZATION_BYPASS_COLLISION_GAP_20260814.md`.

## Verification and process state

Focused verification across the three- and nine-topology menus, independent
menu audit/core extraction, payment identities, spanning frontier,
cancellation theorem, all-target-change frontier, repeat-rank no-go, and
root-star leaf liquidation, two-target root-path repair, and foreign-import
cancellation, root-compensated direct return, and singleton-retained partial
return, universal incoming-cell return, and permanent-anchor nonroot response
transfer, root-target minimum-good diversion, and the exact bilateral
compensator frontier, incoming-root cell diversion, and same-source
root-response replacement, two-source topology/cross capture, and cross-state
safe normalization:

```text
24 passed in 20.35s
```

At the final pause, the five tests directly covering the bilateral frontier,
incoming-cell diversion, same-source replacement, two-source topology, and
cross-state normalization were rerun:

```text
5 passed in 0.27s
```

After adding the universal liquidation, three-placement response frontier,
and strengthened full-source/anchor-residual swap, the combined eight-test
focused chain was replayed:

```text
8 passed in 0.41s
```

After the reservoir-fan correction, missing-source double-capture split, and
duplicate-omission payment/support frontier, the combined chain reports:

```text
11 passed in 0.55s
```

After correcting the physical-compression scope, the conditional census,
independent edge-mask encoding, mixed-core counterexample, and conditional
anchor-substitution frontier, three-color support obstruction, full-owner
connected-rank-defect census, unique Hamiltonian-omission census, and
canonical path-prefix/terminal-split reduction, terminal omitted-core
cross-exchange frontier, and predecessor-overlap bicriteria reduction were
replayed together with their six immediate
liquidation/fan dependencies.  The focused chain reports:

```text
21 passed in 1.20s
```

The full-residual liquidation corollary is a direct algebraic specialization
of the already tested bilateral and strict-root-surplus constructions; it
adds no solver-generated certificate.

All solver processes launched after the checkpoint have exited.  Nothing
campaign-critical is running.  The worktree contains many
older unrelated untracked research traces and two pre-existing modified
files; they were deliberately neither staged nor reverted.

The active `/goal` should remain open.  The fixed rank-three theorem, general
four-agent additive EFX, and general additive EFX are all unresolved.
