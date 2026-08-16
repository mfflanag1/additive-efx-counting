# Referee report — exactly-two-nonsingleton composition (2026-08-16)

Internal adversarial referee round, independent session, no shared context with the proving
sessions. Companion to the same-day T_{L,×} report
[`TLX_CLOSURE_REFEREE_REPORT_20260816.md`](TLX_CLOSURE_REFEREE_REPORT_20260816.md).

**VERDICT: GAP FOUND — repairable; no counterexample; not yet externally quotable.**
Architecture sound. Case exhaustiveness survived brute force; the generalized-PI interface
does NOT break. What fails: the composition never discharges packet nondegeneracy
(nonempty bottoms/tops), which three of four case theorems silently require, plus
presentation defects.

The composed claim: for four positive, nondegenerate additive agents, a globally
lexicographically maximal noncomplete partial EFX allocation in the BCFF one-charity
normal form cannot have exactly two nonsingleton bundles. Composition doc
`results/TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md` exists ONLY on
`cc/efx-fixed-u-salvage-20260814` / `codex/efx-gg-cycle-referee-20260812` /
`codex/efx-fixed-u-termination-20260813` — not on the main checkout (see G5).

## What survived (state affirmatively when quoting)

- **Exhaustiveness CLEAN — no fifth case.** Brute force over every predecessor function on
  4 vertices with 2 large bundles under the three stated facts: exactly four classes
  (48 length-two, 72 length-three, 24 adjacent, 12 alternating configurations), always
  exactly 2 genuine edges, both large bundles on the cycle, one cycle per configuration.
  Script: scratchpad referee-2ns/exhaustive.py. (Minor: doc says "a simple directed
  cycle", singular; several disjoint cycles are possible but harmless — a second cycle
  would need two more genuine edges.)
- **Generalized-PI interface: NO DRIFT.** (i) Every case theorem covers all 24 role-orders,
  so relabeling transport is harmless — the structural reason the interface cannot break;
  (ii) every escape is Pareto or explicitly order-indexed lex; hand-checked adjacent
  (3),(6),(8),(10),(11),(12),(16) + both length-three orientations; alternating 16+2+2+4
  partition verified (no overlap, no omission, half-turn images correct); (iii) the two
  nonstandard certificates (length-two two-disjoint-cycles move; adjacent source-exclusion
  cycles incl. H=∅) are valid.
- **Chordlessness not smuggled in** (atomic CEGAR's chordless assumption is not inherited;
  extra edges are routed as PI cycles).
- **No banked counterexample contradicts the claim**; all counterexample audits record
  `"unsat_orders": []`; six audit replays byte-identical under local z3.
- Uniform improvement order confirmed: maximal among ALL partial EFX allocations, rivals
  may leave any goods unallocated (ALTERNATING_GLOBAL_LEX_ATOMIC_THEOREM.md:46).

## Ranked gaps

**G1 (MEDIUM-HIGH, blocking): packet nondegeneracy undischarged.** Adjacent needs
B_q≠∅/B_r≠∅ (load-bearing for Thm 1, Thm 3, escapes (11)-(12)); alternating's
reservoir-exchange lemma assumes "B_q nonempty" and the dual-reservoir trichotomy assumes
"B_r nonempty" while the theorem statement advertises no packet bounds and omits strict
positivity; length-two hypothesizes nonempty bottoms; only length-three discharges it
(LENGTH_THREE_BCFF_COMPOSITION_AUDIT.md:17 via BCFF Obs 2.10). Failure scenario: with an
empty bottom, 6 of alternating's 8 hard orders lose their proof. THE REPAIR EXISTS IN-REPO:
ONE_LARGE_CHAMPION_CLOSURE_REDUCTION.md:239 — empty bottom ⟹ selected desired set is
X_r+f, common-safe, positivity makes r a self-f-champion; absorbing f is EFX, improves r
alone, lex improvement in every order; topology-independent. Empty tops: desired set {f},
excluded by charity dominance.

**G2 (MEDIUM): alternating hypothesis is a vacuous disjunction** mixing generalized-champion
(broad) and cross-bottom (narrow) family notions; narrow ⟹ broad makes the second disjunct
unsound to instantiate literally, and the repo contains a live profile where that literal
reading fails (ALTERNATING_CROSS_BOTTOM_LOCAL_OBSTRUCTION.md). Not a soundness break in the
composition's actual use; a trap for any external reader.

**G3 (MEDIUM): live contradiction** — ALTERNATING_RESERVOIR_EXCHANGE_LEMMA.md:131 claims the
trichotomy leaves (p,q,s,r),(s,r,p,q) uncovered; the cap-free theorem and trichotomy doc
credit it with those orders. The :131 sentence is STALE (alternative 2 fixes p,s at base,
improves q, r last in both orders — four-order claim correct), but two docs in one chain
assert incompatible coverage.

**G4 (MEDIUM-LOW, external): BCFF Thm 3.16 / Def 3.9** not reproduced in-repo; only
length-two invokes 3.16 (verified: the other three cases do not); repaired 159-line
length-two closes the internal-edge alternative and Def 3.9 is clause-checked in
ONE_LARGE_CHAMPION_CLOSURE_REDUCTION.md:245-256. Needs one human check against
arXiv:2102.10654. Length-two cites zero computational evidence.

**G5 (LOW-MEDIUM): version fragmentation. — CLOSED, *G5 consolidation 2026-08-16*.**
As found: main checkout carried the OLDER 149-line length-two theorem (asserts external
edges outright, lacks internal-edge exclusion), the repaired 159-line version existed only
on the three later branches, and the composition branch had only 2 of 13
adjacent_large_*.json artifacts plus one dangling audit link. Closed by branch
`cc/consolidation-20260816`, which merges `codex/efx-breakthrough-next-20260802` into the
repaired referee corpus. `ONE_LARGE_CHAMPION_CLOSURE_REDUCTION.md`, this report, the
companion T_{L,×} report and `PRIORITY_SWEEP_20260816.md` are now co-resident with the
repaired documents, and every cross-branch citation that had been rendered as inline code
with a branch caveat is now a live relative link.

**G6 (LOW): ledger overclaims.** "exact packet audit replays all 24 indexed cases" —
the packet audit models bundles as two reals (no set membership/disjointness); the
combinatorial core is analytic. Coverage test test_alternating_capfree_order_coverage.py
is hard-coded set arithmetic (asserts sizes [16,2,2,4]) and cannot detect a miscredited
lemma.

## Minimal repairs

1. One "packet nondegeneracy" paragraph in the composition doc (self-f-champion absorption,
   topology-independent) + add B_r,B_q≠∅ and positivity to the alternating and adjacent
   theorem statements. (Closes G1.)
2. Restate the alternating hypothesis on the generalized notion, or delete as vacuous with
   narrow⊆broad proved in one line. (Closes G2.)
3. Correct ALTERNATING_RESERVOIR_EXCHANGE_LEMMA.md:131. (Closes G3.)
4. Write ALTERNATING_BCFF_COMPOSITION_AUDIT.md and ADJACENT_BCFF_COMPOSITION_AUDIT.md
   mirroring the length-three premise table (its absence is why G1 went unnoticed).
5. Consolidate onto one branch; soften ledger wording; drop the coverage test from
   "Verification boundary".

After 1–3 the result is quotable AS A CONDITIONAL THEOREM — conditional on BCFF Thm 3.16 /
Def 3.9, which need a human referee against arXiv:2102.10654.

## Not checked

BCFF 3.16/3.9/3.5/Obs 2.10/Lemma A.1 (external); whether upstream reductions deliver the
two-nonsingleton normal form (Target A ladder steps 1-2, out of scope); alternating
component lemmas verified by subagent not referee; cvc5 artifacts not replayed (not
installed); CEGAR searches not re-run (frozen-input audits only, 6/6 byte-identical).
