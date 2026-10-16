# Physical cycle release: hostile review and disposition

16 October 2026. Review of the conventional derivations, not an external referee
endorsement or a formal proof certificate.

## Snapshot and disposition

Fable 5.1 run `20261016-144241-28149f1b`, completed in 250.32 seconds.
Reviewed proof SHA-256: `27069e41cb95089e86514eaab78aafd51feec9f49cd699d0b9d4e1c053cbecb5`.
The packet included the previous A1 proof and the frozen global/core calibration
JSONs. It did not include code or the full BCFF paper.

- F1: clarified that self edges are already excluded by A1, then applied shortest-
  cycle minimality to distinct endpoints. No theorem change.
- F2: explicitly stated owner-bundle-only EFX and unrestricted charity at exits.
- F3: retained the strict/nondegenerate versus weak/tied distinction.
- F4: treated BCFF as a cited import. The root and a separate source auditor read
  the primary PDF, section 2.3, Definition 3.9, Lemmas 3.13–3.14 and Theorem 3.16.
  Its all-G result was not extended to mixed cycles. The new internal proofs do
  not require an unproved mixed-cycle contraction.

The mathematical conclusions below were independently inspected against the
physical set constructions. The exact numerical assertions were separately replayed
by the new verifier; this review itself did not execute them.

A native read-only code reviewer also found no substantive defect, ran the 21
focused tests and independently compared every deletion in 12 release/return probes
(including six p-augmented winner failures across scaling variants). Its suggested
all-G augmented-winner regression was added and rerun. That code review did not rerun
the original exhaustive global-maximality census or the BCFF source audit.

## Raw proof review (before the two clarifications above)

**Provisional verdict: no substantive mathematical findings in the reviewed scope.** Most important observation: every quantifier/global-maximality step in Lemma 1, Theorem 2, Corollary 3, Theorems 4–6 and the GG external-core paragraph checks out under the stated hypotheses; the remaining items are polish or unverifiable external citations.

## Findings

**F1 (Low, polish) — Lemma 1 proof, line 52.** "A non-successor edge would close a shorter directed cycle, including a self cycle if its endpoints coincide." A chord has distinct endpoints; self edges are excluded by A1 Prop. 2 (global maximality), not by length minimization. Harmless, but the proof mixes two exclusion sources. The chord argument itself is correct: for v ≠ σ(u), the cycle v→…→u→v has length ≤ ℓ−1. The E-replacement argument correctly uses that any envied O_j is automatically inclusion-minimal (all proper subsets are p-free, hence unenvied by Cor. 3a), so "no E edge i→j" ⟺ v_i(O_j) ≤ u_i(O).

**F2 (Low, polish) — Theorem 2 / Theorem 5 / Theorem 6 implicitly use an EFX notion with no charity comparison.** "Every EFX violation has its observer in U" and the Pareto-contradictions rely on EFX being owner-bundle-only, which matches A0's "all partial EFX, no charity safety" domain (A1 §2, Prop 2). Suggest stating this once in §1; no overclaim.

**F3 (Low, polish) — Theorem 2 "precisely k−1" strictness.** Both directions (δ_i>0 via R_j≠O_i; δ_i<v_i(p) via desire) are correct; the document already confines the exact count to the nondegenerate scope (lines 112–115). Lemma 1's second inequality and Theorem 5's chain v_j(D_i)<v_j(p)≤v_j(D_j) remain valid under ties (the needed conclusion v_j(P_i)<u_j(O) only requires the weak form).

**F4 (Low, unverifiable) — BCFF correspondences (lines 60–65, 240–243).** Claims that Lemma 1's all-G conditions "establish Definition 3.9's good cycle" and that Lemmas 3.13–3.14/Thm 3.16 propagate bottom-bundle demands cannot be checked from the packet. Not a defect in the internal mathematics; mark as cited, not proved here.

**Checked and found correct (no finding):**
- Thm 2 lex improvement: all agents earlier than a are outsiders (fixed); a is an E source or w.
- Thm 4: terminal-vertex uniqueness with one run; v_i(D_i)≥v_i(p) applied to the *incoming* edge's decomposition; non-junction targets are O_σ(j), the winner core, or O_b — all common-safe; completeness contradiction uses that complete allocations are in A0's domain.
- Thm 5: pools disjoint (σ injective, D_i∩R_i=∅); contradiction direction (≤1 old-floor-unsafe pool ⇒ choose it as h ⇒ Z is EFX) is sound; "distinct pools, not observers" caveat correct.
- Thm 6: perfect matching ⇒ disjoint common-safe bundles, weak Pareto with strict pool recipients; minimal-S equality and |N_pool(S)|≤|S∩I|−1 via distinct own keepers; S∩I≠∅.
- GG paragraph: Q⊆P_i crossing argument; pairing i's Q with R_i+p (disjoint since P_i is p-free, R_i⊆O_i∖D_i); j's non-desire from Lemma 1 on both edges; hence external champion and proper crossing core.
- §3/§4 structural data (cycle 1→3→2→1, E edge at 1, Y and Z bundle formulas, 103 complete EFX, complete maximizer utilities 6464/32910) agree with the two JSON files by hand reading.

## Scope limitations
No code executed; exact wall numbers (1072/3124/2019, uniqueness of failing comparisons) only spot-checked by hand arithmetic against `values_scaled`, not replayed. Global maximality is taken from the audit JSON. BCFF content not available.

## Verdict
No findings of actual overclaim in reviewed scope; four polish/unverifiable-citation items (F1–F4).
