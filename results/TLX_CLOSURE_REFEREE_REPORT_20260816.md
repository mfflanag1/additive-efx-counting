# Referee report — `T_{L,×}` collision-terminal closure, commit `34709c9`

Internal adversarial referee round, 2026-08-16 (independent session, no shared context with
the proving session). Requested by the closure's own pending-review flag.

**VERDICT: GAP FOUND. Do not quote externally.** The arithmetic is sound and all artifacts
reproduce bit-for-bit, but the new load-bearing operation is not shown to be an admissible
transition of the framework it plugs into, and the "strict packet progress" it produces is
explicitly excluded as progress by two of the branch's own frozen contracts. Separately, the
machine evidence cited in support (17 tests, 85,725 + 1,371,600 replayed cases) does not
test any of the contested content.

All paths below are relative to the repo root at commit `34709c9`.

---

## 1. The operation, verbatim

The "one new load-bearing operation" is the **controlled floor reset**, in
`results/STRICT_FIRST_PRIORITY_FLOOR_RESET_ADMISSION_THEOREM_20260814.md`.

Hypothesis (lines 18–24):
> Let `Y` be any explicitly specified feasible allocation with exact current suppliers and
> releases such that `v_r(Y_r)>x`. (1) **No EFX or old nonroot-floor premise is assumed for `Y`.**

Operation (lines 28–44):
> Recompute every EFX comparison at the actual allocation `Y` and replace the auxiliary
> current floor vector by `F_i^Y=v_i(Y_i) (i∈N)`. (2) Retain separately the immutable base
> certificate `(X,r,x)`, the complete physical anchor label, the full signed transfer
> decoration, and every retirement/collision record. … Equation (2) is an actual controlled
> reset, not an assertion that `Y` preserves the previous floor vector. … The reset may lower
> any later auxiliary floor, including to zero, but never lowers the protected root below `x`.

Admissibility conclusion (lines 81–88):
> The controlled reset is a valid extension of the exact signed-state transition registry
> whenever all of the following are present: 1. a fully specified feasible allocation `Y`;
> 2. current suppliers and destinations for every moved good; 3. the strict first-priority
> certificate (1); 4. the recomputed floor vector (2) and all actual EFX comparisons; and
> 5. a separate physical progress argument for every non-EFX continuation.

Its only use is the singleton supplier star,
`results/ROOT_SINGLETON_SUPPLIER_STAR_FLOOR_RESET_CLOSURE_THEOREM_20260814.md:57–71`:
`Y_r=G−k, Y_u={k}, Y_j=∅ (j∉{r,u})`, empty charity; then the claimed progress at lines
88–97: `D∩K ⊆ K−k ⊊ K`.

**Formalization.** With the augmented state `S=(Y,P,r,α,F,Σ,M,h,R,L,C)` of
`results/GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_CONTRACT_20260813.md:14`, the operation is a
state map `S ↦ S'` that (a) replaces the allocation by an arbitrary feasible `Y'` satisfying
only `v_r(Y'_r)>x`, (b) replaces `F` by `F^{Y'}_i=v_i(Y'_i)`, (c) leaves `α,Σ,L` untouched,
(d) appends new collision records to `C`. Soundness requires four separable things:

- **S1 (endpoint):** `Y'` EFX ⇒ `Y' ≻_lex X`. Needs `r` globally first-priority and `Y'`
  inside the family over which `X` is maximal.
- **S2 (response validity):** the globally minimum desired subset `D` at `Y'` is safe at `Y'`.
- **S3 (transition admissibility):** `S'` is a legal successor in the G0–G10 registry,
  satisfying the premises of whatever selector consumes it.
- **S4 (well-foundedness):** the claimed decrease is in a coordinate monotone across the
  whole transition system.

**S1 and S2 are proved. S3 is asserted, not proved. S4 is not addressed anywhere, and the
framework's own documents list it as the missing piece.**

---

## 2. Ranked findings

### G1 (closure-breaking) — the claimed progress is exactly what the branch's own governing rule forbids, and the rule was never retracted

`results/AUG14_COLLISION_CANDIDATE_TRANSITION_ADMISSIBILITY_AUDIT_20260814.md:44–49`, still
present verbatim in the committed file directly under the "Resolution update" that HEAD
prepended:
> Bare feasibility and a smaller intersection `D cap K` do not meet the second requirement.
> A response found at a counterfactual allocation cannot decrease the collision coordinate
> of the current state unless an admitted operation reaches that allocation.

The closure's progress *is* "a smaller intersection `D∩K` found at a counterfactual
allocation". Everything rests on *"unless an admitted operation reaches that allocation"*,
and the only warrant is the floor-reset theorem's own line 81 ("a valid extension of the
exact signed-state transition registry") — a self-declaration, not a derivation.

Against the composition's own acceptable-leaf list,
`results/GG_CYCLE_CLASS_REFEREE_COMPOSITION_20260812.md:76–78`:
> 3. **Strict finite-coordinate transition:** the source and target states stay inside one
> declared selector family and one of its explicitly ordered finite coordinates strictly
> increases.

The star's target state has two of four owners holding `∅`, the whole auxiliary floor vector
zeroed, and no flower top/bottom structure — it is in **no** declared selector family
(leaf 3 fails), it is not EFX (leaf 1 fails, see G2), and no PI cycle is produced (leaf 2
fails). The transition satisfies none of the three leaves the composition says it accepts.

And `results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md:102–103`:
> Progress must change a physical packet, response rank, or root/anchor state. **Adding
> another history label is not an outcome.**

The star changes no physical packet of the state it started from. The closure theorem
concedes the residual case is handled by record-keeping alone (`ROOT_SINGLETON_...:96–97`):
"restoring the old whole `K` hit would require a separately recorded later collision" — an
appeal to a history label the contract has ruled out.

### G2 (high) — the extracted response is manufactured by the operation and is always a singleton

At `Y=(G−k,{k},∅,∅)` with positive additive valuations and four owners, each owner holding
`∅` desires **every** single good (`v_j({g})>0=v_j(∅)`). The floor-reset theorem's `D` is
the nonempty desired subset "of globally minimum cardinality" over every source and every
target (lines 61–63). Hence `|D|=1`, always. Three consequences:

- The EFX endpoint branch is **vacuous**: `Y` is never EFX for `n≥3` with positive
  valuations, so the lexicographic-contradiction exit that motivates the construction can
  never fire. Everything runs through the non-EFX branch.
- The "EFX wall" is created *by the reset* — an owner is envious because the operation
  emptied her. The response is an artifact of the test allocation, not of the collision state.
- `D∩K ⊊ K` then reduces to "a one-element set is not a superset of a set containing `k`".
  That is why the replays are tautologies (G5): the encoded proposition really is trivial.

### G3 (high) — the descent measure is not the state's collision coordinate, and nothing bounds the successor's packet

`results/GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_CONTRACT_20260813.md:42,102`:
`L_α = {g : ∃s,F_ret, (α,g,s,F_ret) ∈ L}` — every good **ever** retired under label `α`,
monotonically growing — and the named packet is `K = A ∩ L_α` for the *current candidate's*
cell `A`. So `K` is generally a proper subset of `L_α`.

Equation (5) bounds only `D∩K`; it says nothing about `D∩(L_α\K)`. The successor's named
packet is `A'∩L_α` for the next candidate, which can meet retired goods outside `K`. The
theorem acknowledges these and waves at them (`ROOT_SINGLETON_...:95–96`): "A simultaneously
exposed second retirement label is kept in the signed record, but cannot put `k` into `D`."
Excluding `k` is not excluding growth of the packet coordinate. **No monotone measure is
exhibited and `|K|` is not one.** `GG_CYCLE_CLASS_REFEREE_COMPOSITION_20260812.md:84–110`
and its Uncovered premise 4 ("no single order is proved monotone across root, hole, source,
rank, and retained-support changes") already say so; the Aug-14 commits do not touch it.

### G4 (high) — this is the Aug-12 flaw pattern, in the form the earlier referee report named

`results/CLOSING_SOURCE_DELETION_RETURN_REFEREE_REPORT_20260812.md:84–95` killed the
deletion-return theorem on exactly this shape: strict payment at a candidate allocation
proved, EFX leaf proved, then "This strictness does not turn a non-EFX candidate into
progress"; the follow-on response advanced no fixed coordinate.
`GG_CYCLE_CLASS_REFEREE_COMPOSITION_20260812.md` records the self-loop: "the transition
'record the response and continue' can leave every coordinate of (1) unchanged. It is an
exact one-state recurrence in the local transition system."

The new operation has the identical skeleton — strict root at a constructed candidate, EFX
leaf, non-EFX branch extracting a minimal response — with the extra liberty of rewriting the
floor vector. Sharpened into a dichotomy against the framework's own terminal definition:
`GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_COMPOSITION_THEOREM_20260813.md:140–165` proves
termination by "the permanent history `(L,C,R,A)` is finite and ordered by inclusion, every
genuine transition inserts into it… When no insertion is possible, the complete augmented
record repeats and is exactly the `T_L^*` outcome", and line 207 defines `T_{L,×}^*` as a
state where "The complete signed state, typed floors, physical root/anchor label, retirement
and collision histories repeat." Then:

- If the star is *available* at such a state and inserts new collision/response records
  (which `ROOT_SINGLETON_...:68–70` says it does), an insertion **was** possible and the
  state was never a `T_{L,×}^*` recurrence — the theorem proves nothing about the declared
  terminal, only that the entry classification was premature.
- If the state genuinely is a recurrence (no insertion possible), the star and its response
  are already in the record, `D∩K ⊊ K` already held at the earlier occurrence, and it broke
  nothing then either.

Either horn defeats "closure".

### G5 (high, evidential) — the cited machine evidence tests none of the contested content

All four audits re-run in the venv at `/private/tmp/efx-charity-py`. **All four reproduce
the banked JSONs byte-for-byte; all 12 sha256 provenance hashes match** (8.03 s for the
largest). Determinism and provenance are sound. The content is not:

- `tracks/parkability/audit_strict_first_priority_floor_reset_admission.py` — the audit of
  the load-bearing operation. Its three z3 checks are of the form `X ∧ ¬X`: line 24
  `x >= 0, root_actual > x, root_actual <= x`; lines 31–32 `floors[i]==assigned[i]` then
  `Or(assigned[i] < floors[i])`; lines 39–40 `source_value < target-good` then
  `Not(target-good > source_value)`. Every substantive field — `old_later_floors_preserved`,
  `floor_reset_counts_as_progress`, `all_efx_comparisons_recomputed`,
  `physical_labels_retained` (lines 62–65) — is a **hardcoded literal**. The rest is four
  string-matches against the prose file. Status `STRICT_FIRST_PRIORITY_FLOOR_RESET_ADMITTED`
  is produced by three tautologies and four constants.
- `audit_root_singleton_supplier_star_floor_reset_closure.py` — the 5,407,744 "support
  cases"/"response subsets checked" are line 83
  `whole_hit_failures += int(packet <= root_packet_intersection)` where line 82 has just
  asserted `root_packet_intersection == packet - {chosen}` with `chosen ∈ packet`. That is
  "a set containing x is not a subset of itself minus x", enumerated 5.4M times over only
  **1,024 distinct pairs** (5,281× inflation). No valuations, floors, EFX comparisons or
  responses are modelled; `response_subsets_checked` is a misnomer.
  `full_T_L_times_theorem_closed: True` (line 118) is a literal.
- The **1,371,600 packet-support cases** in
  `audit_retired_packet_charge_anchor_resolution_20260814_independent.py:65–72` are the same
  tautology over **80 distinct pairs** (17,145× repetition). Its lex check (line 89)
  compares tuples whose first coordinate is drawn from `range(base+1,8)` — true by
  construction. Its "minimal-response deletion" check (lines 104–110) restates its own guard.
- The **85,725 root-margin cases** (same file, lines 42–64) are the one genuinely
  non-trivial replay: over 5 goods and weights in `{1,2,3}` it exhausts
  `v_r(G−k)>v_r(X_r)` given `A⊆O, |A|≥2, v_r(A)>v_r(X_r)`. Real — but of inequality (3),
  the part nobody disputes.
- Tests: 16 pass, 0 fail (`test_collision_candidate_transition_admissibility.py` is
  referenced but **does not exist**). Of 209 assertions across 13 test files, 72 are on
  computed values and **137 read back hardcoded literals**, plus 46 string-in-markdown
  assertions inside the audit modules. `full_T_L_times_theorem_closed: True` is a literal
  everywhere it is reported true; `imports_z3`/`imports_primary_audit` are self-declared,
  never introspected. `audit_root_global_supplier_star_floor_admissibility_gap.py` hardcodes
  `all_sacrificed_floors_zero_proved: False` in the same dict as
  `full_T_L_times_theorem_closed: True`.

**A correct counterexample to this closure would leave all 16 tests green and all four JSONs
byte-identical.** The suite is a provenance/determinism harness, not evidence for the
theorem.

### G6 (medium–high) — the operation proves too much

Its hypothesis is **any** feasible `Y` with `v_r(Y_r)>x`, with "No EFX or old nonroot-floor
premise" (line 24). The enabling inequality `v_r(G−k)>x` holds for *every* good `k` at
*every* state of the anchored GG branch, since it follows only from the permanent base-row
edge `D_r=T_q+f ⊆ G∖X_r`, `v_r(D_r)>v_r(X_r)`
(`results/GG_OLD_ROOT_CORE_EXCLUDES_EXTERIOR_DOMINANT_PACKET_THEOREM_20260814.md:17–31`) —
a property of the base `X`, not of the collision. So the operation is available
unconditionally everywhere in the branch and licenses jumping to an arbitrary root-favoring
allocation at any point. Were that an admissible registry transition, the 58 selector
lemmas, payment algebra, Hall cuts and compression stars would have been unnecessary, and
`T_0^*` and `T_{L,⊥}^*` would fall to the same move. The only thing distinguishing
`T_{L,×}` is that a packet `K` happens to be available to point at afterwards. An operation
satisfied at every state but claimed to close exactly one of three structurally parallel
terminals should be assumed unsound until the asymmetry is explained.

### G7 (medium) — the star bypasses the canonical ledger cancellation and creates unresolved collisions

`GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_COMPOSITION_THEOREM_20260813.md:69–72` defines a
candidate's collision set as the goods of `L_α` it moves off their current holders, and
line 87 mandates: "Otherwise form `Z^-` by cancelling every transfer of a good in `K`:
leave that good with its current holder and perform every other transfer of `Z`."

The star moves **every** good to the root, so it is a maximal-collision candidate. It does
not form `Z^-`; `ROOT_SINGLETON_...:68–70` instead appends the collisions to the record.
Concrete failure scenario: let `L_α ⊋ K` with retired `g ∈ L_α\K` currently held by `c`.
Canonical cancellation leaves `g` with `c`, giving `Y^-_r = G−k−g`, so
`v_r(Y^-_r)−x = v_r(O)−v_r(k)−v_r(g)`, and **positivity no longer forces this above zero**
— the exterior-dominance argument of lines 41–46 breaks as soon as more than one good is
withheld. The star's root-strictness certificate survives only because the star declines to
cancel. Whether `L_α = K` is forced in the root-holder branch is nowhere argued.

### G8 (medium, inherited not new) — `r` is not shown to be the globally first-priority owner

S1 requires it, and the star empties every owner but `r` and `u`; if any owner precedes `r`,
the star is lexicographically *worse* than `X` and the endpoint inverts. The GG normal form
fixes `r` only as the earlier of the two **mutual** owners:
`results/FLOWER_EARLY_ROOT_CHARITY_ROTATION_LEMMA_20260810.md:10` ("with `r` earlier than
`q` in the fixed priority"), `results/CROSS_STAR_HOLE_PIVOT_LEMMA_20260811.md:84` ("the
earlier mutual owner `r`"), and
`results/FLOWER_LATER_OWNER_SINGLE_REPLACEMENT_SELECTOR_LEMMA_20260810.md:10` works in "the
**representative** full-`X_q` flower cell with priority `r,q,c,s`". From Aug-11 onward ~25
files silently upgrade this to "first owner in the fixed priority"
(`ROOT_PRESERVING_TWO_HOLE_SELECTOR_LEMMA_20260811.md:11`;
`PERMANENT_ANCHOR_HITTING_RECURRENCE_CONTRACT_20260813.md:10–12`; the floor-reset theorem
line 10). No file bridges them, and the flower census closes only 580 of 864
source/priority cells
(`results/THREE_NONSINGLETON_CYCLE_CENSUS_AND_FLOWER_REDUCTION_20260809.md:272`).
Pre-existing debt, but the star is the most priority-sensitive construction in the corpus.

---

## 3. What IS sound (so the repair is not over-scoped)

- **Inequality (3), `v_r(G−k)>x` for every `k`** — correct in both support cases given
  `A⊆O`, `v_r(A)>x`, `|A|≥2`, positivity. Verified by hand; the 85,725-case replay genuinely
  confirms it.
- **`|A|≥2`** is legitimate: `T_q≠∅` is *derived*, not assumed
  (`results/LENGTH_THREE_GLOBAL_LEX_TARGET.md:63–70` — an empty top would make `{f}`
  desired, contradicting charity dominance), and `f∉T_q` since `f` is charity and `f∉X_q`.
- **Minimal-response safety (S2)** is a correct standard argument (floor-reset lines 58–71),
  with the singleton base case handled by `v_a(∅)=0`.
- **The lex-maximality family (part of S1)** admits the star: `X` is maximal "among partial
  EFX allocations" (`results/FOUR_OLD_CORE_SHORTCUT_AND_INTERFACE_REFUTATION_20260813.md:52`),
  rivals range over all `5^m` assignments including complete ones and ones with empty
  bundles (`results/ALTERNATING_GLOBAL_LEX_ATOMIC_THEOREM.md:45–51`), and the one-charity
  bound is explicitly disclaimed for rivals (same file `:66–74`).
- **The nonroot-holder branch**
  (`results/NONROOT_SAFE_WHOLE_HIT_ENVELOPE_DESCENT_THEOREM_20260814.md`) is a genuinely
  better argument: it descends a nested chain `D ⊋ D_1 ⊋ …` *within one allocation family*,
  with explicit bound `|D|−|K|+1`, and rewrites no floors. The objections above do not touch
  it.

So the holder split is exhaustive and half of it is in good shape. The defect is confined to
the root-holder half — the half the new operation was invented for.

## 4. Minimal repair, in increasing cost

1. Downgrade `T_{L,×}^*` from "closed" to "conditionally closed on admissibility of the
   controlled floor reset" in the four status-bearing docs (`RETIRED_PACKET_CHARGE_OR_
   ANCHOR_EXCHANGE_RESOLUTION_20260814.md`, `GG_CYCLE_CLASS_REFEREE_COMPOSITION_20260812.md`,
   `GLOBAL_RETIRED_ROOT_SUPPORT_LEDGER_COMPOSITION_THEOREM_20260813.md`, `results/README.md`).
   LEDGER.md and AUDIT_HISTORY.md carry no entry for this claim at all — nothing there needs
   retraction, but there is currently no cross-check on it.
2. Discharge S3 explicitly: name which of G0–G10 consumes the star's successor state and
   verify full selector premises (expected to fail: two empty bundles, zeroed floors, no
   flower decomposition ⇒ the reset *exits* the selector family = an undeclared terminal,
   not an elimination).
3. Discharge S4 explicitly: exhibit a well-founded order containing `|K|`/hitting
   multiplicity, prove the star strictly decreases it AND no other admitted operation
   increases it; must bound `D∩(L_α\K)` or restrict to `L_α=K` and prove availability.
4. Resolve G7: prove `L_α=K` in the root-holder branch, or show the star survives canonical
   cancellation, or amend the ledger contract and re-audit everything proved under it.
5. Rewrite the audits to test the claim: small exhaustive model checker over 4 agents /
   5–6 goods / integer weights instantiating an actual `T_{L,×}^*`-shaped state, applying
   the star, computing the real minimal response, and comparing the successor's packet
   coordinate against the predecessor's. The existing 85,725-case loop is the right
   skeleton; it stops one step too early.
6. Close G8: prove the flower root may be taken globally first, or close the priority orders
   where `c` or `s` precedes `r`.

## 5. Not checked

Author's intended scope of "admitted operation" (if the reset is meant to *amend* the frozen
contracts, the amendment is unwritten and everything proved under the old contract needs
re-audit); whether `L_α=K` is forced upstream (~20 of ~500 documents read); the BCFF-to-GG
reduction and fixed-priority import (composition's Uncovered premise 6); the 58 upstream
selector lemmas (Uncovered premise 5). No exact rational countermodel constructed — hence
GAP FOUND rather than FLAW FOUND; the G7 scenario is a countermodel to the star's
root-strictness under canonical cancellation, not to the theorem as stated. Repair item 5
would supply the harness a full countermodel needs.
