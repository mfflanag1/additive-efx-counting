# Handoff to Codex — 2026-08-17

From the Claude Code coordination session of 2026-08-16/17. This resumes your
`EFX_FIXED_U_HANDOFF_20260814.md` and the fork's gg-cycle-referee track. Everything below
is committed and pushed; branch names are given per item. Read this before trusting any
Aug-14 status line — several changed.

## 1. Priority event: (4,8) is scooped — reprioritize accordingly

**arXiv:2608.08590** (Alkassar–Fouz–Mehlhorn, posted 2026-08-09): complete EFX0 for four
additive agents and m ≤ 9. Strictly dominates efx48 (m ≤ 9 vs m = 8; EFX0), similar
hybrid method, AI-led. Their §8 "earlier independent m=8 project" is most likely their
own internal run, not us (our repo uncited; email to Mehlhorn is Max's call). DECISION
TAKEN: retire (4,8) as a standalone publication; efx48-hybrid-proof stays as a dated
artifact; salvage option = short independent-corroboration note for their Theorem 2.
THE GOOD HALF: general four-agent + the BCFF/global-lex route is UNCONTESTED, and their
paper argues certificate corpora cannot reach the general theorem (obstruction localized
at near-identical valuations, ~0.14% EFX0 density). Full memo:
`results/PRIORITY_SWEEP_20260816.md` (this branch). WINE 2026 notifications (~Oct) are a
blind spot for both cells — recheck then.

## 2. Status changes to YOUR results

### T_{L,×} floor-reset closure (fork, 34709c9): RETIRED
Adversarial referee round: GAP FOUND — the controlled floor reset's S3 (registry
admissibility) was asserted not derived, S4 (well-founded descent) absent, and the
progress form is excluded by your own frozen contracts (AUG14 admissibility audit :44-49;
charge-or-anchor contract :102-103). The supporting audits were provenance-only
(hardcoded verdict literals; the 85,725/1,371,600 "cases" mostly tautologies). A
successor-state model checker (233k instances / 35.9M successors) then REFUTED closure
eq. (5) under its own quantifier (an emptied owner desires {k} itself ⟹ D={k} legal
minimum) and localized descent to EXACTLY the L_α = K slice (100% there, 0/34M off it,
where hitting multiplicity strictly INCREASES). The nonroot envelope-descent branch is
CLEAN and survives. Honest status now in the docs: closed on the L_α = K slice, open
otherwise; route retired. See `results/TLX_CLOSURE_REFEREE_REPORT_20260816.md` and
`results/TLX_SUCCESSOR_MODEL_CHECK_20260816.md` on `codex/efx-gg-cycle-referee-20260812`.

### Two-nonsingleton composition: REPAIRED, RE-VERIFIED, and WIDENED
- Referee round: exhaustiveness brute-forced clean (no fifth case); generalized-PI
  interface holds across all 24 orders in all four cases; ONE blocking gap — packet
  nondegeneracy was undischarged in 3 of 4 case theorems. Repaired via the
  self-f-champion absorption argument (now a "Packet nondegeneracy" section proved once
  for all topologies), re-verified by the original referee, second-pass residuals fixed.
- BCFF imports audited against the arXiv LaTeX SOURCE: surface faithful; VERSION PIN =
  arXiv full build (the AAAI short build renumbers — "Observation 2.10" does not exist
  there); one drift (Lemma A.1 over-described — it gives a nondegenerate CANCELABLE
  witness + one-directional EFX transfer only) — all attributions corrected.
- **The theorem is now stated for NICE CANCELABLE valuations** (additive kept as a
  verbatim corollary). Three sweeps established zero order-closing additivity uses;
  the one τ-definition conflict that briefly blocked the widening is fixed
  (ALTERNATING_TWO_SAFE_BUNDLE_REDUCTION.md line 12 was the additive form; its proof
  body already used max-deletion). All τ-using files now carry convention banners.
- Everything consolidated on **`cc/consolidation-20260816`** (single citable lineage;
  G5 closed; all cross-branch citations live). Remaining gates: external human review
  of the BCFF 3.16/3.9 interface (only the length-two chain uses them), and real peer
  review.

### Fixed-U track: the identity-aware campaign ran to completion
Branch **`cc/efx-idwitness-20260816`**, main doc
`results/IDENTITY_AWARE_MINIMUM_WITNESS_20260816.md` (one-screen summary at top), plus
`results/IDENTITY_AWARE_SLACK_TWO_20260816.md` and
`results/FIXED_U_TAME_MENU_CHART_20260816.md`.
- **Your SAT_ONE_MINIMUM_SPLIT_SELECTOR_OBSTRUCTION is NOT real** — the driver floored
  both split pieces at M (identity-blind); with real value columns every realization
  repairs. Superseded, old artifacts untouched, dated supersession note.
- **Theorem 1 (realization-free reduction, hand-proved, verified independently by a
  second worker):** a tame covering menu in the canonical two-good model covers EVERY
  physical realization — any cardinality, any witness identity. (Key: an unsplit role
  of any width contributes exactly (T, M) to the EFX predicate.) Corollaries: the
  slack-two theorem; zero-split allocations are realization-free at any slack. All 113
  banked (T,M) profiles settled for every realization (104 zero-split, 9 tame-split).
- **Count correction:** "173 exact adversarial profiles" is wrong everywhere it
  appears. Canonical string: "111 distinct profiles over 211 rounds (113 including
  terminal countermodels)" — stage-2 resumed from stage-1 and replayed its cuts.
- Also wrong in the Aug-14 notes: the "22-good 1/696-slack repair" conflates the R2
  critical-role compression lemma with a role minimum from the whole-role countermodel.
- **The single open gap on this rung:** a profile where EVERY complete four-edge EFX
  allocation must split a WILD role (rho ≥ 3). 180 adversarially-generated profiles
  found none (honest caveat: the template was adversely biased — all non-target roles
  forced tame multi-good — so the null result carries reduced weight). The chart-level
  question ("does every fixed-U-admissible profile admit a tame covering menu?") is
  OPEN behind a quantified barrier: covering menus can split six tame roles ⟹ 8^6 =
  262,144 pattern vectors per certificate, reached twice from independent data. Search
  will not decide it in this form. The widened driver exists
  (full-product-sound cuts, self-tests); its run died orphaned at ~208 rounds /
  0 obstructions — ADD CUT-CHECKPOINTING BEFORE RESUMING (append cuts to a jsonl).
- Two analytic routes ranked for next: (a) a premise-level obstruction to a role being
  wild AND forced at once (model: Lemma D in the chart note, which extracts an
  allocation-wide constraint from the rank-three wall); (b) a normal form that shrinks
  the 96-unknown master so the CEGAR terminates.

## 3. Chores lane (efx2, counterexample-hunt repo): now the lead publication
Tri-valued m ≤ 11 theorem still NOVEL (verified 2026-08-16; He–Tao §6 is the openness
attestation; framing law: the increment is m ∈ {7..11} past KMS's 2n barrier). The m=7
rung is now PROOF-CARRYING: 227/227 chambers with individual CaDiCaL+drat-trim binary
DRAT certificates under a sorted-row-0 quotient whose WLOG is a Lean theorem
(TriValCert/Relabel.lean); 49 chambers additionally carry unreduced certificates; proofs
are digest-pinned and deterministically regenerable, not archived. Encoding lesson that
transfers: sorted_row0 + binary DRAT was 78× end-to-end on the worst chamber (proof
23.25 GB → 20.6 MB); hardness, not clause count, drives cost (18,370× proof-size spread
at ~1× clauses). The paper (efx2/paper/main.tex, 19pp, two hostile referee rounds, zero
mathematical errors found) is complete modulo Max's author block.

## 4. Process laws established this session (they will bite you otherwise)
1. **Selector-artifact law (enforce in code, not comments):** five instances, one shape,
   across two workers — including your one-minimum-split driver. No SAT/obstruction from
   a restricted driver is banked until re-tested against the widest move family, and the
   re-test runs BEFORE the verdict is banked. Structural guards: halt names that cannot
   borrow countermodel language; test-pinned obstruction sets; deliberate-narrowing
   self-tests.
2. **A statistic offered as a bound must name the quantity it measures:** "baselines
   split ≤ 3 roles" was read as "menus split ≤ 3", became a driver's cap, and emitted a
   false SAT one worker downstream. `baseline_split_roles` UNDERSTATES covering menus —
   use `wide_menu_split_union`.
3. **Long-running computations must not live in a subagent's background shell** (three
   orphaned runs in one session). Checkpoint everything resumable.
4. Audit scripts must be checked for hardcoded verdict literals and tautological
   case-count inflation — a real counterexample would leave such suites green.
5. Worktrees of this repo are ~2.4 GB — use sparse checkouts (tracks+docs ≈ 9 MB).
6. Big-proof sweeps: ≤3 workers + a kill-below-30GB disk watchdog; ENOSPC wedges the
   whole harness.

## 5. Suggested opening moves, in order
1. Chart question: add cut-checkpointing to the widened driver, resume under a
   persistent shell; in parallel try analytic route (a) above.
2. T_0 / T_{L,⊥}: attack with the retirement lessons (any new operation must discharge
   S3/S4 explicitly against the frozen contracts; the nonroot envelope-descent pattern
   is the sound template).
3. If class generality matters for the three-nonsingleton rung: the constraint map
   (`results/THREE_NONSINGLETON_CANCELABLE_CONSTRAINT_MAP_20260816.md`) says the
   advertised weighted-dual route is additive-bound — replace it with an
   order-theoretic selector (start: LEX_SACRIFICED_RESPONSE_COMPRESSION :30-42) or
   accept additive scope now and widen later.
4. m=8 chores certification: re-measure under the reduced encoding before trusting any
   cost claim (all prior m=8 cost statements were formed under the superseded encoding).

Branches pushed: `cc/consolidation-20260816` (canonical corpus),
`codex/efx-gg-cycle-referee-20260812` (referee + repairs + maps),
`cc/efx-idwitness-20260816` (identity-aware campaign),
`cc/efx-fixed-u-salvage-20260814` (your salvaged final state),
`codex/efx-fixed-u-termination-20260813` (was local-only; now safe).
Program memory (CC-side) mirrors all of this.
