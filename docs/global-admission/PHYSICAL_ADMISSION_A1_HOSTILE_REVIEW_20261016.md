# Independent Fable proof review (verbatim)

Review run: `20261016-141401-5d457504`; model `claude-fable-5-1`.
Completed in 207.25 seconds. Tool-free source/proof snapshot review, not an
executed verification or external specialist endorsement. See the companion
verification record for adjudication and post-review additions.

**Provisional verdict: no invalid steps found in Propositions 1–7 as stated; two precision/overstatement findings (Low), several unverifiable source claims.**

Most important: Proposition 1 requires |P_O| = 1 (it uses "j strictly prefers T_j = O_j ∪ {p}"), so Section 1's sentence that the arguments "do not otherwise require the no-complete-EFX hypothesis" (l.13–14) should say they require a nonempty (hence singleton) charity, which A0 gives only under no-complete-EFX or by direct assumption.

## Findings

**1. Low — Scope qualifier imprecise (PHYSICAL_ADMISSION, l.9–14, l.35–37).** If O is a complete lex-maximum, T_j = O_j and the family in Prop 1 may be empty. Everything in §2 is conditional on P_O = {p}. Verification: state "assume |P_O| = 1" explicitly as the antecedent of Props 1–3.

**2. Low — Consequence of Props 4/7 understated, not overstated (l.110–114, l.173–189).** Checked: B has ≥3 pool goods; by BCFF Thm 5.1 (A0 §2) B always admits a strict lex-improving EFX successor. Hence P1 ∧ P3 ∧ "P10 at B" is unsatisfiable under nondegeneracy, and every `efx_lex` cut in the frozen CEGAR (`lex_improves` tests `==1`/`>1`, terminal script l.151–158) is an improvement over B, not over O. The ledger row P10 says "cannot attach to B" but does not record that attaching it is contradictory. Not an error; a missing sharp statement.

**3. Verified correct (no action):**
- Prop 1: minimality ⇒ v_i(C∖g) ≤ u_i(O) for all i,g; monotonicity makes single deletions sufficient. Cores are either O_j (ordinary envy) or contain p.
- Prop 2: cores ⊆ O_target ∪ {p}, targets distinct on a simple cycle ⇒ no nonparticipant intersection; EFX via common-safety + own utility nondecreasing; strict Pareto ⇒ contradicts F-maximality without any pool-safety requirement. Self-edge case included.
- Cor 3: finite digraph with in-degree ≥1 at each vertex has a simple cycle; pairwise-disjoint cores excluded ⇒ some two cores meet, only possible at p; {p} unenvied by safety ⇒ each p-core has a target good. "Every decorated simple cycle" is justified.
- Prop 4: |pool(B)| ≥ 3 ≠ 1; strictness via nondegeneracy (equal tuples ⇒ equal bundles ⇒ equal charity).
- Prop 5: tail_d(A∪H) ≥ v_d((A∪H)∖g*) ≥ v_d(A∖g*) = tail_d(A); role-deletion tail ≤ physical tail. Correct.
- Prop 6: all 48 master atoms are proper subsets of their B-bundle (r,q,s: 2 roles; d, pool: 3) ⇒ each bounded by 1 via base==1, EFX tail ≤1, pool ≤1; `<16` redundant. Four-good example: 5⁴=625; Σ C(4,k)·4!/(4−k)! = 209 ✓; M ≥ 2 already suffices (M ≥ 3 harmless).
- Prop 7: positive coordinatewise scaling preserves lex order; w(Z) = 1 + d exactly.

**4. Source fidelity (verified against packet):** B and Y tables match `BASE`/`SUPPORT_STATE`; (3),(4) of the root-facing lemma match `d:(h,k,gq)` and `Q:(j,k,q0)`; the lemma's own boundary disclaims deriving (3), nonempty Q₀, and EFX of (10); census lists exactly the eight words and claims only GG reduction. P7 wall appears only in the rank-three master (l.135), not `build_master` — the checkpoint's "if assumed" phrasing is consistent.

**5. ADMIT4 distinction:** the checkpoint correctly labels the 4-good example (complete EFX exists) and the 9-good calibration (imported maximality) as calibrations, not ADMIT4 evidence.

## Scope limitations
Not in packet: the "historical ledger" `<16` claim (l.158), `extract_champion_cores.py`, `verify_state_separation.py`, the 5⁹ enumeration, `run_fixed_u_full_packet_batch_cegar.py`, `physical_tail`, and the P1–P15 definitions. Their characterizations are unverified. BCFF Thm 5.1 taken as external.

## Verdict
Findings (minor precision only); no invalid mathematical step identified in the reviewed propositions; branch theorem correctly labeled open.
