# EFX Literature Ledger — No-Go Map for the Additive-Goods Counterexample Hunt

**Target problem:** Does an EFX allocation always exist for **n ≥ 4 agents** with **additive** valuations over **indivisible goods**?
**Status as of 2026-07-23: OPEN.** Not resolved in either direction.

**EFX variant convention used throughout** (per the standard in the field, e.g. Wikipedia "Envy-freeness up to any item", Amanatidis et al.):
- **EFX₀** (stronger): no agent `i` envies `j` after removing **any single good** from `X_j`, *including goods that `i` values at 0*. `∀ g ∈ X_j: v_i(X_i) ≥ v_i(X_j \ {g})`.
- **EFX₊** (weaker, often just written "EFX"): the same but only over goods with **strictly positive marginal value** to the envier: `∀ g ∈ X_j with v_i(g) > 0`.
- EFX₀ ⟹ EFX₊. A counterexample to EFX₊ is also a counterexample to EFX₀ (stronger to hunt against); an existence proof for EFX₀ is stronger than one for EFX₊. **Where a source does not disambiguate, this is flagged inline.** For a hunt, the cleanest target is **EFX₀** — an EFX₀-nonexistence instance is the weakest thing to find and still counts; but note referees will care whether it also breaks EFX₊.

---

## Status alert (Question A: has the problem already fallen?)

**No.** As of 2026-07-23 there is **no published or preprinted counterexample, exhaustion, or existence proof** for **additive goods, n = 4**. The problem is explicitly restated as open in the newest (2026) papers themselves.

The 2026 wave of negative results all sit **outside** the additive-goods box:

- **arXiv 2604.18216** (Akrami, Mayorov, Mehlhorn, Srinivas, Weidenbach; Apr 20 2026, v3 May 14 2026): first EFX **nonexistence** counterexample — but for **monotone** (hence submodular) valuations, **not additive**. They explicitly write: *"For n ≥ 4, it is not known whether EFX allocations always exist even when all agents have additive valuations."*
- **arXiv 2605.06451** (Mackenzie, Suzuki; May 2026): counterexamples for **submodular and subadditive** valuations (compact, human-verifiable, symmetric). **Not additive.**
- **arXiv 2606.08872** (He, Tao, SJTU; Jul 2026): nonexistence for **additive CHORES** (tri-valued costs, n ≥ 4). This is the **chores** problem, a different problem; it does **not** transfer to goods.

Twitter/X and blog chatter through July 2026 surfaces the SAT counterexample (2604.18216) as the headline event, framed precisely as "EFX fails for monotone/submodular, additive still open." No credible claim of an additive-goods resolution was found.

**Bottom line: the additive-goods n=4 box is intact and is the live prize.** The SAT counterexample tightening to `m ≥ n+5` monotone means the *additive* frontier is now the last standing version of the original conjecture.

---

## Proven-safe classes (each = a region where a candidate CANNOT be a counterexample)

### 1. n ≤ 3 agents, additive (and beyond)
- **Chaudhury, Garg, Mehlhorn 2020** ("EFX Exists for Three Agents", EC 2020): EFX exists for **3 agents, additive** valuations, any m. Variant: **EFX₊** (the standard "EFX"; the original proof is for positive-marginal EFX). *Flag: the paper's statement is for EFX in the positive-good sense; EFX₀ for 3 additive agents is generally treated as also holding but is worth double-checking against the exact theorem if it becomes load-bearing.*
- **Strongest current 3-agent result — Akrami, Alon, B.R. Chaudhury, Garg, Mehlhorn, Mehta** ("EFX: A Simpler Approach…", arXiv 2205.07638; EC 2024 / Operations Research 2024): EFX exists for **3 agents when just ONE agent has an MMS-feasible valuation and the other two have arbitrary monotone valuations.** MMS-feasible ⊋ additive ⊋ nice-cancelable, so this strictly generalizes CGM. Also **Berger, Cohen, Feldman, Fiat 2022**: 3 agents with **nice-cancelable** valuations.
- **Filter:** any candidate must have **n ≥ 4**. Three-agent instances are dead.

### 2. Small number of goods (Mahara)
- **Mahara** ("Existence of EFX for two additive valuations" line; arXiv 2008.08798 and follow-ups): EFX exists whenever **m ≤ n + 3**, for **general (monotone) valuations**, any n. *Flag: the exact variant (EFX₀ vs EFX₊) in the small-m theorem should be confirmed if a candidate lands at exactly m = n+3; the ledger sources state it as "EFX" without disambiguating.*
- **Filter:** for n = 4, any candidate must have **m ≥ n + 4 = 8 goods**. (Note the SAT boundary below independently forbids m ≤ 7 for 3 agents; the general safe-m bound is n+3.)

### 3. Bounded number of distinct valuation types
- **Mahara 2023 — at most 2 distinct additive valuation types:** complete EFX exists for **any n** when agents draw from **≤ 2 distinct additive valuations**. Variant: EFX (standard).
- **Ghosal, HV, Nimbhorkar, Varma — "EFX Exists for Three Types of Agents"** (arXiv 2410.13580; **EC 2025**, ACM EC proceedings 10.1145/3736252.3742509): complete EFX exists for **any n** when agents draw from **≤ 3 distinct additive valuations.** Generalizes both the 3-agent case and the 2-type case.
- General companion bound (**Berger et al. / type-count charity**): with k distinct additive types, an EFX allocation exists leaving **≤ k−2 goods** unallocated (k=2 ⟹ complete).
- **Filter:** a 4-agent additive candidate must use **≥ 4 genuinely distinct valuation functions** (all four agents different). Any instance where the 4 agents collapse to ≤ 3 distinct additive valuations is safe.

### 4. Bivalued / binary / matroid-rank
- **Amanatidis, Birmpas, Filos-Ratsikas, Hollender, Voudouris 2021 — bivalued additive:** if every agent's values lie in **{a, b}** (two values, same two globally), complete EFX exists for **any n** (Max Nash Welfare is EFX). Variant: EFX (standard).
- **Babaioff, Ezra, Feige 2021 — binary submodular = matroid-rank:** EFX **and** Pareto-optimal allocations exist and are poly-time computable for **any n**, via a truthful mechanism. Binary additive (values in {0,1}) is a special case.
- **Filter:** a 4-agent additive candidate must use **≥ 3 distinct values** somewhere in the value matrix (not globally bivalued). Binary and two-value instances are dead.

### 5. Almost-full existence & charity (unallocated-goods bounds)
- **Berger, Cohen, Feldman, Fiat** ("(Almost Full) EFX Exists for Four Agents (and Beyond)", arXiv 2102.10654; AAAI 2022): every **4-agent additive** (in fact **nice-cancelable**) instance admits an EFX allocation leaving **at most 1 good unallocated**. For general n, an EFX allocation exists with **< n−1 (i.e. ≤ n−2) goods to charity**.
- **Charity via rainbow cycle number** (Chaudhury, Garg, Mehlhorn, Mehta, Misra "A Little Charity Guarantees Almost Envy-Freeness" + **Akrami, Alon, Chaudhury, Garg, Mehlhorn, Mehta** rainbow-cycle line, arXiv 2103.01628 / IJCAI 2023 / Operations Research): a **(1−ε)-EFX** allocation exists with a **sublinear** number of unallocated goods and high Nash welfare. Rainbow cycle number bound improved to **R(d) = O(d log d)**, yielding **O_ε(n^{½} · …)**-type sublinear charity (down from the earlier O(n^{4/5})). These are **approximate/partial** guarantees, not exact complete EFX.
- **Filter (the key structural squeeze):** a genuine 4-agent additive counterexample must be an instance where **no complete EFX allocation exists, yet an EFX allocation leaving exactly 1 good in charity does exist** (guaranteed by 2102.10654). So the obstruction is razor-thin: the counterexample is "1 good away" from EFX. The whole hunt is about that last good — search for instances where every way of placing the final charity good into some bundle creates strong envy.

### 6. EF2X for 4 agents (relaxation is safe, so EFX is the exact boundary)
- **Ashuri, Gkatzelis, Sgouritsa** ("EF2X Exists For Four Agents", arXiv 2412.00254; AAAI 2025): **EF2X** (envy vanishes after removing any **two** goods) exists for **4 agents** with **cancelable** valuations (⊋ additive), constructively in pseudo-poly time; poly-time for 3 agents.
- **Filter / meaning:** for 4 agents, envy can always be killed by removing 2 goods. A counterexample must therefore have envy that survives removing **1** good but dies removing **2** — a very tight "second-good" obstruction. This narrows the shape of the witness.

### 7. The 2026 SAT boundary and adjacent constructions
- **Akrami, Mayorov, Mehlhorn, Srinivas, Weidenbach — arXiv 2604.18216** (v1 Apr 20 2026 titled "monotone", v3 May 14 2026 titled "submodular"): encoding verified in **Lean**. Two exact results, both **monotone**, variant **EFX₀** (their definition: strong envy = ∃ g ∈ X_j with v_i(X_j \ {g}) > v_i(X_i), quantified over **any** g):
  - **Positive:** every instance with **3 agents and 7 goods (= n+4)** admits an EFX allocation. Also: every 3-agent monotone instance admits **tEFX**, or **EF1 and EEFX**.
  - **Negative:** EFX can **fail** for **n ≥ 3 agents, m ≥ n+5 goods** with **monotone** valuations (⟹ also submodular). Minimal witness: **3 agents, 8 goods**, non-degenerate valuations; the submodular realization needs up to 256 distinct subset values per agent, single-good marginals ranging ~11–131 — "far from additive or cardinality-based."
- **Mackenzie, Suzuki — arXiv 2605.06451** (May 2026): **3 agents, 8 goods**, **monotone subadditive**, symmetric (agents identical up to relabeling), human-verifiable; no allocation is α-EFX for any α > 1/∛2 ≈ 0.89. Strengthens the negative side to subadditive and gives a combinatorial (non-SAT) obstruction.
- **He, Tao — arXiv 2606.08872** (Jul 2026): **additive CHORES** — for every **n ≥ 4**, a nonexistence instance using **only 3 chore types and 2 agent types** (both counts **tight**); EFX **does** exist for n = 4 chores only in the bi-valued case; and every EFX allocation can fail Pareto-optimality even for bi-valued positive costs. **Chores, not goods** — informative about proof structure but not a goods counterexample.
- **Filter:** the entire negative literature lives at **m ≥ n+5** and requires **non-additive** valuations (256 distinct values / subadditive gadgets). The **additive** restriction is precisely the wall these constructions cannot cross.

---

## Intelligence

### B. Value-magnitude / rationality bounds on a minimal additive counterexample
- **No published bound of the form "a minimal additive counterexample can be taken with values ≤ f(n,m)"** was found in the literature audit.
- **Bound proved in this project:** if a counterexample exists at fixed
  \((n,m)\), one exists with positive-integer item values at most
  \(\lfloor m^{m/2}\rfloor\). The proof selects one strict violation per
  allocation, optimizes a common row margin, and applies Cramer's rule and
  Hadamard's inequality at an LP vertex. See
  [`results/SMALL_INTEGER_COUNTEREXAMPLE_BOUND.md`](results/SMALL_INTEGER_COUNTEREXAMPLE_BOUND.md).
- What *is* known and adjacent:
  - The **monotone/submodular** counterexamples are stated with **bounded integer values** (SAT-solver output; the 2604.18216 witness uses small integer marginals, single-good values ~11–131, ≤ 256 distinct subset values). This shows small-integer witnesses suffice **once you leave additive** — a hint that if an additive witness exists it may also be small-integer, but there is **no theorem** guaranteeing this for the additive class.
  - **WLOG normalizations** standard in the field: EFX is invariant to per-agent positive scaling. The new determinant argument makes this quantitative for a fixed number of goods.
  - The 2605.06451 α-EFX bound (α > 1/∛2) is an **inapproximability** magnitude, not a value-magnitude bound.
- **Practical implication for the hunt:** the cap \(K_m=\lfloor
  m^{m/2}\rfloor\) is sufficient for an unconditional fixed-\((n,m)\)
  exhaustion. Smaller-cap results remain conditional until the gap to
  \(K_m\) is covered. The bound does not cap \(m\), so it does not by itself
  decide the general conjecture.

### C. Why the 2604.18216 SAT encoding does not extend to additive (and stated next targets)
- The authors **explicitly leave additive open** ("For n ≥ 4, it is not known whether EFX allocations always exist even when all agents have additive valuations"), and note that even for 3 agents, general-valuation existence is only known under structural assumptions (one agent MMS-feasible).
- **Why the encoding stops at monotone/submodular (inferred from the method, partially stated):** the SAT encoding treats each agent's valuation as an **independent value per subset** (2^m free Boolean-encoded variables per agent) constrained only by monotonicity. **Additivity is a far stronger global constraint** — the 2^m subset values collapse to **m per agent** (`v_i(S) = Σ_{g∈S} v_i(g)`), with all subset comparisons forced to be consistent sums. This (a) **shrinks the model space drastically**, so the monotone SAT witness (which needs 256 distinct, non-additive subset values with wildly varying marginals) is **not realizable additively**, and (b) turns the search into reasoning over **linear arithmetic on the m base values**, which is an **SMT/ILP** problem (values, not just Booleans), not a pure SAT problem. So the tooling itself has to change: **additive needs an SMT (linear-arithmetic) or MILP/CEGAR encoding over the m·n base values**, not the subset-indicator SAT encoding used for monotone.
- **Stated / implied next targets:** additive n ≥ 4 (the headline open case); tightening the 3-agent boundary (they resolved 3 agents/7 goods positive, ≥ n+5 negative for monotone — the additive 3-agent case is already known safe by CGM, so the action is n ≥ 4). No explicit additive-specific roadmap is given in the paper beyond flagging the open problem.

### D. Borda-additive \(4\times9\) shape closure
- **Project result:** if each agent's nine item values are a permutation of
  \(1,\ldots,9\), then a complete EFX allocation exists with bundle shape
  \(3+2+2+2\).
- The five unique-favorite multiplicity orbits are closed without residual
  cuts or lex stabilizers. Matching-clause and Hall-selector encodings agree
  on the same 417-partition pool.
- The stabilized \(2+1+1\) cell has a 17-partition core that is UNSAT in
  CP-SAT, Z3, and pinned cvc5; its 555,808-step CPC proof is accepted by the
  independent Ethos checker.
- **Scope warning:** this is an exact equal-gap/Borda subclass. It does not
  imply anything monotone in the value cap and does not close arbitrary
  additive \(4\times9\). See
  [`results/BORDA_EFX_4X9_THEOREM.md`](results/BORDA_EFX_4X9_THEOREM.md).

### E. Unequal-rank-gap boundary and singleton repair
- The same 417 balanced partitions solver-close all five favorite orbits
  when each row consists of nine distinct integers in
  \(\{1,\ldots,10\}\) or \(\{1,\ldots,11\}\). These single-encoding results
  are discovery theorem candidates, not yet proof-checked claims.
- The balanced-shape conclusion is false at cap 12. A common-favorite
  profile has no \(3+2+2+2\) EFX allocation but has exactly 838 complete
  EFX allocations: 636 of shape \(3+3+2+1\) and 202 of shape
  \(4+2+2+1\).
- All 48 supporting unlabeled partitions isolate the common favorite as a
  singleton. This makes the next analytic gate a common-favorite
  singleton-completion lemma, not a larger balanced-partition core.
- Adding those 48 repairs to the 424-partition common-favorite pool closes
  complete EFX at cap 12 under both matching-clause and Hall-selector
  encodings. Combined with the four dual-encoded balanced-orbit closures,
  every rank-distinct \(4\times9\) profile valued in
  \(\{1,\ldots,12\}\) is a computer-assisted complete-EFX theorem
  candidate.
- A sparse countermodel-guided rebuild needs only two singleton repairs, one
  of shape (4+2+2+1) and one of shape (3+3+2+1). Both encodings close
  the same 426-partition pool, making this the preferred analytic target.
- See
  [`results/RANK_GAP_EFX_4X9.md`](results/RANK_GAP_EFX_4X9.md) and the
  frozen literal audit
  [`results/efx49_rankgap12_shape_boundary_audit.json`](results/efx49_rankgap12_shape_boundary_audit.json).
  The ten-cell dual audit is
  [`results/efx49_rankgap12_dual_encoding_audit.json`](results/efx49_rankgap12_dual_encoding_audit.json).
  The sparse common-favorite audit is
  [`results/efx49_rankgap12_sparse_common_audit.json`](results/efx49_rankgap12_sparse_common_audit.json).
  The exact analytic reduction is
  [`results/COMMON_FAVORITE_SINGLETON_REDUCTION.md`](results/COMMON_FAVORITE_SINGLETON_REDUCTION.md).
- At cap 13, balanced shape also fails in the \(3+1\) and \(2+2\) cells,
  but every literal EFX repair in the frozen witnesses isolates one of the
  designated favorite goods. Structural pools close all five
  matching-clause cells and all five Hall-selector cells. The hard
  common-favorite orbit uses the same sparse 446-partition pool in both
  encodings.
- Thus the fully dual-encoded frontier reaches the rank-distinct cap-13
  domain with the conclusion “balanced or designated-favorite singleton.”
  See
  [`results/efx49_rankgap13_theorem_audit.json`](results/efx49_rankgap13_theorem_audit.json).
- The first unrestricted-real common-favorite profile outside the sparse
  cap-13 pool still has 104 literal complete EFX allocations supported by
  39 partitions. Every one isolates the common favorite; their shapes can
  be as unbalanced as \(6+1+1+1\), every agent can be the singleton owner,
  and one owner-threshold slack is only one. Thus the singleton branch
  remains alive, but any analytic proof must allow highly unbalanced
  three-agent remainders and tight thresholds. See
  [`results/efx49_common_favorite_real_frontier_audit.json`](results/efx49_common_favorite_real_frontier_audit.json).
- A converse strict common-favorite profile has 2,231 complete EFX
  allocations supported by 514 partitions, all of shape \(3+2+2+2\), and
  no singleton EFX allocation. Hence neither the balanced branch nor the
  favorite-singleton branch subsumes the other; the analytic target must be
  their union. See
  [`results/efx49_common_favorite_real_balanced_boundary_audit.json`](results/efx49_common_favorite_real_balanced_boundary_audit.json).
- In generic position, the common-favorite threshold alternative splits
  exactly into five second-favorite multiplicity orbits. The audited raw
  vector counts are 8, 224, 168, 2,016, and 1,680, totaling all 4,096
  vectors. This is a cap-free logical decomposition, not a finite-value
  approximation. See
  [`results/efx49_common_favorite_second_orbits_audit.json`](results/efx49_common_favorite_second_orbits_audit.json).
- The extreme \(6+1+1+1\) favorite-singleton branch has an exact
  residual-threshold Hall characterization, but it does not cover every
  nonbalanced case. Four identical cap-13 rows
  \((13,12,7,6,5,4,3,2,1)\) have no balanced or \(6+1+1+1\) EFX
  allocation, while exact replay finds 480 EFX allocations on 20
  intermediate-shape favorite-singleton partitions. A separate targeted
  anneal reaches a strict-common-favorite profile with only 18 total EFX
  allocations on two partitions; all 841 positive one-row transfers
  preserving the favorite cell still have at least 18 target allocations.
  This is local-search evidence, not minimality. See
  [`results/RESIDUAL_THRESHOLD_MATCHING_LEMMA.md`](results/RESIDUAL_THRESHOLD_MATCHING_LEMMA.md)
  and
  [`results/efx49_common_favorite_boundaries_audit.json`](results/efx49_common_favorite_boundaries_audit.json).
- The common-favorite structural campaign now runs at the full sufficient
  cap \(K_9=19{,}683\). Fifteen exact learning models grew the
  balanced-or-favorite-singleton pool from 485 to 811 partitions; every
  model still had a target repair and every model had within-row ties. The
  first fully generic residual solve on 719 partitions returned unknown
  after 900 seconds. Matching and Hall replays on the stronger
  811-partition pool also returned unknown after 900 seconds. This is an
  audited open gate, not a theorem. See
  [`results/COMMON_FAVORITE_SUFFICIENT_CAP_GATE.md`](results/COMMON_FAVORITE_SUFFICIENT_CAP_GATE.md).

---

## Live region (the precise complement — where a counterexample must live)

A candidate additive-goods EFX counterexample must satisfy **all** of the following simultaneously (each row is a filter from above that it must clear):

| Constraint | Value | Source |
|---|---|---|
| Agents | **n ≥ 4** | §1 (n≤3 safe) |
| Goods | **m ≥ n + 4** (so **m ≥ 8** at n=4) | §2 (m ≤ n+3 safe) |
| Distinct valuation functions | **≥ 4** (no collapse to ≤ 3 additive types) | §3 |
| Distinct values in matrix | **≥ 3** (not globally bivalued/binary) | §4 |
| Charity gap | complete EFX fails but **1-good-charity EFX exists** | §5 (2102.10654) |
| Envy depth | envy survives removing 1 good, dies removing 2 (**EF2X holds**) | §6 |

**Sharpest characterization of the prize:** at **n = 4, m ≥ 8**, with **4 distinct additive valuations** using **≥ 3 distinct values**, find an instance where **every** complete allocation has some agent strongly-envying another (EFX₀, i.e. even after removing any single good), **yet** dropping exactly one good to charity fixes it. The obstruction is provably "one good thick" (§5) and "one good deep" (§6). Additivity is the exact wall that all existing 2026 counterexample machinery (SAT-monotone, subadditive gadgets, chores) fails to cross.

**Search-design caveat (from Intel B):** any negative/exhaustion result is
only as strong as its **value cap and m cap**. The project cap
\(K_m=\lfloor m^{m/2}\rfloor\) is sufficient for a fixed cell, so state
whether a run reaches that cap.

---

## Boundary intelligence (the m = n+4 cell)

**Updated campaign decision:** the internally certified additive
\((4,8)\) theorem advances the project search to \((4,9)\). This is an
internal theorem package, not yet a published literature result. Monotone
\((4,8)\) remains unresolved and supplies no external shortcut.

### 1. Is monotone (4,8) known safe or false? — OPEN (neither).
The 2604.18216 SAT results are **only for n=3**, obtained by direct SAT solving:
- **(3,7) = (n, n+4): SAFE** — UNSAT established in ~30 hours (with solver hints; m=6 ran in <1s, m=7 took >2 days, hence the hints).
- **(3,8) = (n, n+5): COUNTEREXAMPLE** — SAT witness found in ~20 hours.

For **n ≥ 4 they did NOT run SAT** — direct solving was abandoned as computationally infeasible at that size. The n ≥ 4 counterexamples at **m ≥ n+5** come from an **algebraic extension** of the (3,8) witness (Section 7), *not* from solving. Consequently:

| n=4 cell | status for MONOTONE | status for ADDITIVE |
|---|---|---|
| m ≤ 7 (= n+3) | SAFE (Mahara, general valuations) | SAFE (Mahara) |
| **m = 8 (= n+4)** | **OPEN** — never solved; too large for SAT | **internally certified SAFE; external literature still open** |
| m ≥ 9 (= n+5) | counterexample (algebraic extension) | OPEN (additive not reached) |

So the **m = n+4 band is open for every n ≥ 4 even for monotone valuations.** The clean "safe at n+4 / unsafe at n+5" boundary is a **proven fact only at n=3**; it is **not** a theorem across n.

### 2. Does the n+4 safety generalize across n? — NOT proven; at best implicitly conjectured.
The only *proven* general safe bound remains **Mahara's m ≤ n+3** (all n, general valuations). The paper's positive theorem is specifically **"3 agents, 7 goods"** — they do not prove a general "m ≤ n+4 ⟹ safe" statement. Some secondary summaries call m=n+5 the "minimal item count for the monotone non-existence phenomenon," but that minimality is demonstrated **only for the n=3 witness** (via the (3,7) UNSAT); there is **no proof that (n, n+4) is safe for n ≥ 4**, and no explicit published conjecture that it generalizes was found. Treat n+4-safety as an **n=3-only fact.**

### 3. Can we additivize the n=4, m=9 counterexample family? — No shortcut; it reduces to the core open problem.
The n ≥ 4 / m = n+5 family is **not a fresh combinatorial object** — it is the **(3,8) gadget plus additive padding**. Explicit construction (Section 7): with G = the 8 goods of the (3,8) witness and H = the extra goods (one per agent beyond the third),
- agents 0,1: `v̄_i(S) = v_i(S ∩ G)` (pure (3,8) gadget),
- agents i ≥ 2: `v̄_i(S) = T·|S ∩ H| + v_i(S ∩ G)` with T a large constant.
The `T·|S∩H|` term **is additive** (each H-good worth T); it merely forces the extra agents to grab their private high-value good. **All the non-additivity — and the entire EFX obstruction — lives in the `v_i(S∩G)` core, i.e. the 256-rank (3,8) monotone gadget** (Appendix A tables, one linear order over all 256 subsets per agent; single-good marginals ~11–131, "far from additive/cardinality-based"). Therefore:
- There is **no explicit additive numeric table** for (4,9) to lift — the (4,9) valuations inherit their hardness from the non-additive (3,8) core.
- **"Additivize (4,9)" ≡ "additivize the (3,8) gadget"**, which is exactly the open additive question. The extension adds no additive-friendly structure; if anything it confirms that the additive obstruction, if it exists, must be found at the **core gadget scale (small n, ~n+4/n+5 goods)**, not by padding.

**Practical takeaways for the hunt:** (a) the project has resolved
\((4,8)\) internally and must now resolve \((4,9)\) on its own; the monotone
results retire neither cell externally; (b) any attempt to reuse the SAT
witness fails at the additive constraint precisely in the (3,8) core, so
effort is better spent on a native additive SMT/CP-SAT search over the base
values than on trying to round the monotone gadget into additivity.

---

## Novelty check (rotation preserves EFX0 → un-envied source)

**Verdict: REDISCOVERY, not a new theorem.** theory1's SOURCE_LEMMA is the standard envy-cycle-elimination lemma of **Lipton, Markakis, Mossel, Saberi 2004**, restated in essentially every EFX paper's preliminaries. It must be cited, not claimed. The *use* of the lemma to constrain the search is fine; the lemma itself is textbook.

### 1. The rotation-preserves-EFX0 / un-envied-source statement — ALREADY PUBLISHED (verbatim match).
Closest statement found, **verbatim**, from **Mahara, "Existence of EFX for Two Additive Valuations"** (arXiv:2008.08798v4), Preliminaries:

> **Lemma 7** (attributed to Lipton et al. [23]). *"Let X be an EFX allocation such that E_X has a dicycle. Then, there exists another EFX allocation Y such that E_Y is acyclic and Y Pareto dominates X."*

This is theory1's lemma, exactly:
- **"rotation preserves EFX0"** = "there exists another EFX allocation Y" (the swap permutes ownership without changing bundle contents, so EFX is preserved; the argument is **variant-agnostic** — it holds identically for EFX0 and EFX+, since the "remove any good" test only sees bundle contents, which are unchanged).
- **"strictly increases the utilitarian potential"** = a **corollary of "Y Pareto dominates X"** (Pareto domination with at least one strict envy edge ⟹ the utilitarian sum strictly increases). Mahara/Lipton state the stronger Pareto-domination fact.
- **"terminates at an allocation whose envy graph has a source"** = "E_Y is acyclic" (a finite acyclic digraph has a source). Hence **"every instance with an EFX0 allocation has one with an un-envied bundle"** is the immediate corollary that these papers use routinely.

The lemma traces to **Lipton, Markakis, Mossel, Saberi, "On approximately fair allocations of indivisible goods," EC 2004** (envy-graph + cycle elimination: swapping along a cycle keeps the set of bundles fixed, no agent's utility decreases, and the number of envy edges strictly drops, terminating at an acyclic graph with a source). It is reproduced in CGM, Plaut–Roughgarden usage, the charity line, and Mahara Lemma 7 above.

### 2. theory1's distinction from Lipton (complete vs. partial + add-good) is CORRECT but also already understood.
theory1 is right that classic envy-cycle *elimination* drops to EF1 / ½-EFX because it **adds a good to the new source**, and that pure rotation adds nothing. But the literature already separates these two steps cleanly: the **swap step alone preserves full EFX** (Mahara Lemma 7, stated for full EFX, not ½-EFX), and only the **subsequent good-adding step** degrades the guarantee. So the "insight" is the standard reading, not a new one.
- **Minor correction for honesty:** the property that makes rotation safe is **"swap without adding a good," not "complete allocation."** Lemma 7 holds for *partial* EFX allocations too — the swap never adds goods regardless of completeness. So framing completeness as the essential ingredient is slightly off; the essential ingredient is that rotation ≠ good-insertion.

### 3. The "parking/slack" framing (EFX0 base of M−1 goods + add last good to a source) — ALSO the standard charity-line argument.
This is exactly the invariant of the **almost-full / charity** papers. From **Berger, Cohen, Feldman, Fiat, "(Almost Full) EFX Exists for Four Agents"** (arXiv:2102.10654, AAAI 2022) and **Chaudhury, Kavitha, Mehlhorn, Sgouritsa, "A Little Charity Guarantees Almost Envy-Freeness"** (arXiv:1907.04596, SICOMP): the algorithm **"maintains the invariant that X is EFX and the envy-graph is acyclic"**, removes cycles "without destroying desirable properties" (Lemma 7 again), and allocates remaining goods to a **source/unenvied** agent. The reason 4-agent additive gets stuck at **one** leftover good is precisely that **adding that last good to a source can create strong envy toward the source** — which is theory1's "slack" obstruction, already the crux of the almost-full result. So the parking framing is not new either; it *is* the 2102.10654 proof structure.

**Net methodological guidance:** cite Lipton et al. 2004 (and Mahara Lemma 7 / CGM as restatements) for the rotation lemma; cite 2102.10654 + 1907.04596 for the "acyclic-envy-graph + last-good-to-source" framing. The lemma is sound and useful as a **search-pruning invariant** ("WLOG a candidate counterexample's envy graph, on any EFX0 sub-allocation, is acyclic with a source"), but it cannot headline a paper as a new theorem. The genuinely open content remains the *additive existence question itself*, which this lemma does not touch.

---

## Variant map for zero-valued goods (EFX0 vs EFX+)

**Headline: for ADDITIVE goods, EFX0-with-zeros is NOT a separate open target — it is existence-equivalent to the all-positive EFX+ question at every (n,m). Zeros are not a soft target; the campaign's all-positive restriction is WLOG and fully general.**

**The reduction that collapses the split (Amanatidis, Birmpas, Filos-Ratsikas, Hollender, Voudouris, "Maximum Nash Welfare and Other Stories About EFX," IJCAI 2020 / TCS, arXiv:2001.09838):** computing an EFX0 allocation of an additive instance `I` reduces to computing an EFX (=EFX+) allocation of the instance `I'` obtained by **replacing every 0 with a small ε > 0** (same number of distinct values; for rationals ε ≥ 1/D is poly-size). An EFX+ allocation of the all-positive `I'` is an **EFX0** allocation of `I`.

Consequences (both directions, size-preserving, same (n,m), additive-only):
- **All-positive theorem ⟹ zeros theorem.** If every all-positive additive (n,m) instance has an EFX allocation (e.g. an UNSAT from `cegar_z3.py`), then **every additive (n,m) instance *including zero values* has an EFX0 allocation** — apply the theorem to `I'`. **This corrects the caveat in `cegar_z3.py` ("Zero-valued goods NOT covered (EFX0/EFX+ split)"): via the MNW perturbation reduction, an all-positive UNSAT DOES upgrade to a full EFX0 result covering zeros.** The all-positive search is not weaker.
- **Zeros counterexample ⟹ all-positive counterexample.** Contrapositive: if `I` (with zeros) has no EFX0 allocation, then `I'` (all-positive) has no EFX+ allocation, at the **same (n,m)** with the same distinct-value count. So a zeros-based witness converts to an all-positive witness for free — **hunting with zeros buys nothing.**

**Which existence results cover which variant (additive goods):**
- **n ≤ 3 (CGM 2020):** gives **EFX0** (and hence EFX+). Confirmed in the literature: "for indivisible goods, an EFX0 (and hence EFX) allocation always exists for at most three agents." (Directly, or via the reduction from CGM's EFX+.)
- **Mahara m ≤ n+3:** stated for general/monotone valuations; for the **additive** slice it gives EFX0 via the reduction. (For genuinely monotone/non-additive valuations the reduction does not apply — see below.)
- **Bivalued / 2-value (MNW, Amanatidis et al. 2021):** Max Nash Welfare is **EFX0** for 2-value instances (their result is explicitly EFX0, not just EFX+), any n.
- **Almost-full 4 agents (2102.10654) and the whole additive frontier:** whatever is proven all-positive transfers to EFX0-with-zeros by the reduction.

**Is EFX0-with-zeros open at small n for pure goods? NO.** It exists for n ≤ 3 (above) and for 2 agents. The **Aleksandrov–Walsh [2020]** nonexistence example (2 agents, identical additive, no allocation satisfies the strongest variant) is for **goods-and-BADS (mixed) / the two-sided variant "EFX±0"**, **not pure goods** — so it does **not** give a pure-goods small-n EFX0 counterexample. There are **no known EFX0-with-zeros counterexamples for pure additive goods at any n** (existence there is exactly the open n≥4 question, equivalent to the all-positive case).

**Where the split IS real:** for **monotone / submodular** valuations the perturbation reduction fails (it relies on additivity), so EFX0 and EFX+ can genuinely differ. The 2604.18216 SAT work uses **EFX0** (strong envy = ∃ *any* g ∈ X_j with v_i(X_j\{g}) > v_i(X_i)); its monotone counterexamples are therefore EFX0-nonexistence (the stronger statement), and its (3,7) positive result is also EFX0. This is fine for us but does not bear on the additive question, where the two variants coincide.

**Net for the campaign:** keep searching all-positive. It loses nothing, and an all-positive UNSAT can be *stated* as an EFX0 theorem including zeros (cite 2001.09838 for the reduction). Do not spin up a separate zeros search.

## Novelty check 2 (Parking-Floor Lemma)

**Claim (theory1):** for a *universal-minimum* good `f` (every agent's least-valued good), the EFX0 completions of an EFX0 base allocation of `M \ {f}` are **exactly** the envy-graph **sources** of the base — i.e. base + `f`→agent i is EFX0 **iff** i is unenvied in the base.

**Correctness: the lemma is TRUE, and the universal-min hypothesis is load-bearing.**
- **Sufficiency (source ⟹ EFX0 completion):** giving the *universally minimum* good to an unenvied i keeps EFX0 — for any envier j, the worst removal from `X_i ∪ {f}` is removing `f` itself (it is j's least-valued good), leaving `v_j(X_i) ≤ v_j(X_j)` since i was unenvied. The "universal min" is exactly what makes `f` the worst-case removal; a non-minimum good could break this.
- **Necessity (non-source ⟹ not EFX0):** if some j plain-envies i in the base (`v_j(X_i) > v_j(X_j)`), then after adding `f`, removing `f` from `X_i ∪ {f}` leaves `v_j(X_i) > v_j(X_j)` — strong envy, EFX0 violated. (Holds for any `f`, needs only EFX0.)

**Novelty: PARTIAL — the sufficiency direction is standard; the exact iff/counting is at most a minor unpublished sharpening.**
- The **⟸ direction ("a source can safely receive the leftover/minimum good") is the standard charity-line argument** — CGM "A Little Charity" (arXiv:1907.04596) and Berger–Cohen–Feldman–Fiat (arXiv:2102.10654), which maintain "X is EFX and the envy-graph is acyclic" and allocate remaining goods to sources; also the "at most k sources / give good to a source" reasoning surfaced in the counting-and-variants line (AAAI). The reason 4-agent additive gets stuck at one leftover good is precisely that a non-source cannot absorb it — the necessity direction, implicitly known.
- The **exact bijection "EFX0 completions = sources" for a universal-minimum good**, stated as a *counting* identity, was **not found verbatim** in the literature. It is a correct, easy consequence of standard envy-graph reasoning specialized to the minimum good.
- **Verdict:** more original than the rotation lemma (which was a verbatim rediscovery of Lipton et al.), but still incremental. Usable as a **lemma-in-service** (e.g. to enumerate/prune completions in the search), presented with explicit acknowledgment of the charity-line precedent for sufficiency. **Not headline material**, and the necessity/counting angle should be double-checked against the AAAI "Counting and Variants" paper (arXiv/AAAI 33536) before any claim of originality, since that paper studies exactly EFX-completion counting.

## Competition sweep (arXiv cs.GT, July 15–23 2026)

**No competitor.** No new posting on EFX for additive goods, four agents, or computer/SAT/SMT search for EFX counterexamples in the July 15–23 window. The July 2026 cs.GT fair-division items are off-target: **2607.03463** "Random Serial Dictatorship is √2-Envy-Free" (EC 2026), **2607.01059** "Fair Allocation under Conflict Constraints via Strong Colorability", **2607.10232** "Best-of-Both-Worlds Fairness for Mixed Goods and Chores". The most recent on-topic negative results remain the early-July / June batch already in this ledger (2606.08872 additive chores; 2605.06451 subadditive; 2604.18216 SAT-monotone). **The additive-goods n=4 prize is still uncontested.**

## Cap-14 favorite-211 boundary (2026-07-31)

- A rank-distinct cap-14 profile with favorite pattern \((0,0,1,2)\) has
  no balanced \((3,2,2,2)\) EFX allocation. This refutes the balanced-only
  cap ladder, not EFX existence.
- Exhaustive literal and partition replay finds 298 complete EFX
  allocations on 85 partitions, all of shapes \(3+3+2+1\) or
  \(4+2+2+1\).
- Every repair isolates one of goods \(0,1,2\), exactly the goods that are a
  designated strict favorite. The broader balanced-or-designated-favorite-
  singleton target therefore survives the first cap-14 obstruction.
- Frozen audit:
  [`results/efx49_rankgap14_favorites211_boundary_audit.json`](results/efx49_rankgap14_favorites211_boundary_audit.json).
- The enlarged 624-partition structural master is matching-infeasible. Its
  hash-identical Hall replay timed out after 1,200 seconds. The
  all-distinct-favorites orbit is dual-closed, while the other three cap-14
  orbits remain active. No cap-14 theorem is claimed.
- Requiring that value 14 actually occur is sound because cap 13 is closed,
  but did not settle the residual cells. The common-favorite matching pool
  grew from 482 to 498 before a second-iteration timeout; \(3+1\) and
  \(2+2\) matching runs timed out on pools 560 and 535; and the
  \(2+1+1\) Hall replay timed out on the 624-partition pool. All four
  statuses are `MASTER_UNKNOWN`.

## Common-three cap-free closure (2026-07-31)

- Exact optimization over \(3+3+2\) and \(4+2+2\), plus threshold-preserving
  reductions of the other three shapes, shows that universal failure of the
  common-favorite singleton threshold is exactly
  \(x_3+x_7>f\) or \(x_4+x_5>f\), together with
  \(x_5+x_6+x_7>f\). Thus at least five residual goods exceed
  \(f/3\), and their total value exceeds \(7f/3\). See
  [`results/OWNER_THRESHOLD_SHAPE_ENVELOPE.md`](results/OWNER_THRESHOLD_SHAPE_ENVELOPE.md).
- The resulting half-favorite graph either has four distinct
  representatives or consists of the same three goods for every agent.
- The common-three branch is now proved complete-EFX safe. A Hall matching
  first constructs four valid anchor--low pairs with one low floater. In a
  lexicographically maximal valid state with the intended host last, any
  blocked insertion gives an earlier agent a strictly improving host pair;
  the host can absorb the displaced anchor with one of two available lows
  because at most one low is bad. This contradicts maximality.
- The result is cap-free and analytic, not a finite-value solver closure.
  It proves an anchor-separated \(3+2+2+2\) EFX allocation throughout this
  branch. The distinct-representatives branch and mixed threshold/Hall
  obstruction remain open.
- Proof:
  [`results/COMMON_THREE_LEXICOGRAPHIC_PARKING_LEMMA.md`](results/COMMON_THREE_LEXICOGRAPHIC_PARKING_LEMMA.md).
- The distinct-representatives branch now has a cap-free analytic
  triple-aware starting theorem: some one-triple/three-pair partition,
  with the common favorite in a pair, can be assigned so each owner gets at
  least its favorite value. The proof needs only
  \(x_5+x_6+x_7>f\), three half-favorites per row, and a saturating
  half-favorite matching. It classifies four three-element set systems and
  explicitly places the host's least or second-least good. Matching-clause
  and Hall-obstruction QF_LRA formulas independently close all 840
  partitions. This is not yet EFX; only envy of the triple remains.
- Proof:
  [`results/DISTINCT_HALF_DENSITY_FLOOR_LEMMA.md`](results/DISTINCT_HALF_DENSITY_FLOOR_LEMMA.md).
- The analytic construction is not itself an EFX normal form. A strict
  branch-valid profile has 728 bottom-aware high-pair owner-floor
  allocations and zero EFX allocations among them, while the same profile
  has 1,364 complete EFX allocations. Exact replay:
  [`results/efx49_distinct_half_structured_floor_boundary_audit.json`](results/efx49_distinct_half_structured_floor_boundary_audit.json).
- Two stronger normal forms are false even in strict generic position:
  four favorite-dominating pairs need not exist, and the triple need not be
  globally bounded by every observer's favorite. The owner-floor allocation
  remains a useful first alternative, but the live completion statement
  must also permit moving the favorite into a common-low triple. See
  [`results/DISTINCT_HALF_FAVORITE_GATE.md`](results/DISTINCT_HALF_FAVORITE_GATE.md).

## Distinct-half rank-augmentation boundary (2026-07-31)

- The order-statistic threshold envelope has a cap-free sorting-free
  equivalent. Every residual four-set must contain a triple above the
  favorite, and the pair-sum graph must have either at least three vertices
  of degree at least six or at least four vertices of degree at least four.
  The proof is
  [`results/OWNER_THRESHOLD_PAIR_DEGREE_ENCODING.md`](results/OWNER_THRESHOLD_PAIR_DEGREE_ENCODING.md),
  with a separate 2,695-check regression audit.
- Ordinary Nash-product maximization and favorite-surplus-product
  maximization over favorite-pair owner-floor allocations are false. Across
  1,000 deterministic exact-branch profiles they have 21 and 22 weak
  failures respectively; the witnesses still possess balanced EFX
  allocations. No utility-product maximality route remains live.
- A subsequent candidate used the maximum matching rank of the exact
  four-agent/four-bundle EFX-feasibility graph on all 840 favorite-pair
  balanced partitions. Shape-preserving single-good exchanges form a
  21-regular state graph with 8,820 edges.
- The candidate is false. A strict exact-branch profile has matching-rank
  histogram \(20,237,583,0\) on the 840 states. Yet it has 324 complete EFX
  allocations; all put the favorite in the common-low triple
  \(\{f,1,2\}\). A second strict profile refutes the former radius-two
  strengthening: its shortest augmentation needs two rank-preserving swaps
  before the improving swap.
- The exact boundaries are
  [`results/DISTINCT_HALF_RANK_AUGMENTATION_GATE.md`](results/DISTINCT_HALF_RANK_AUGMENTATION_GATE.md).
- A new cap-free lemma proves the common-low triple immediately EFX when
  each remaining pair is worth at least
  \(F_i+\max\{v_i(a),v_i(b)\}\) to every observer. This is a sufficient
  special case of the exact favorite-triple Hall criterion below. See
  [`results/COMMON_LOW_FAVORITE_TRIPLE_LEMMA.md`](results/COMMON_LOW_FAVORITE_TRIPLE_LEMMA.md).
- The boundary also yields a cap-free one-defect conversion: if two pairs
  are universally safe and a third has one rejecter, a two-edge Hall
  matching moves the favorite back into a pair. The proof and 1,251-case
  literal regression audit are
  [`results/ONE_DEFECT_FAVORITE_TRIPLE_CONVERSION_LEMMA.md`](results/ONE_DEFECT_FAVORITE_TRIPLE_CONVERSION_LEMMA.md)
  and
  [`results/efx49_one_defect_favorite_triple_conversion_audit.json`](results/efx49_one_defect_favorite_triple_conversion_audit.json).
- A sharper cap-free characterization removes that comparison condition
  for existence. For a fixed favorite triple \(\{f,a,b\}\), the triple is
  feasible for every agent, and each remaining pair is feasible for agent
  \(i\) exactly when its value is at least
  \(F_i+\max\{v_i(a),v_i(b)\}\). The partition supports EFX if and only if
  the three pair vertices have a Hall matching to three agents. Consequently
  two universally safe pairs and one pair with at most one rejecter already
  suffice. See
  [`results/FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md`](results/FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md)
  and its 108,360-check regression audit.
- The favorite-triple-only normal form is independently false. A strict
  item-distinct exact-branch profile has zero EFX states among all 420
  favorite-triple partitions, but 356 favorite-pair EFX partitions and
  1,906 complete EFX allocations. Together with the reverse boundary above,
  this proves both sides of the combined dichotomy are necessary. Audit:
  [`results/efx49_distinct_half_favorite_triple_boundary_audit.json`](results/efx49_distinct_half_favorite_triple_boundary_audit.json).
- A concise two-core/Tutte corollary captures the tight positive boundary.
  If two agents accept every residual edge for some parked low pair, all 15
  pairings support EFX exactly when the graph of edges rejected by both
  outsiders has no perfect matching. Three universal acceptors are not
  forced: a strict boundary has exactly a two-agent core and a one-edge bad
  graph, yet all 15 pairings work. See
  [`results/FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md`](results/FAVORITE_TRIPLE_HALL_CHARACTERIZATION.md)
  and
  [`results/efx49_distinct_half_two_core_boundary_audit.json`](results/efx49_distinct_half_two_core_boundary_audit.json).
- The two-core low pair is not canonically tied to the half-favorite SDR. A
  strict exact-branch profile with zero favorite-pair EFX states has no
  witness whose lows are two representatives and whose core agents are the
  complementary representatives' agents. Its unique unrestricted witness
  uses nonrepresentative lows 5 and 6. This removes a six-cell shortcut but
  leaves the full 168-cell target live. Audit:
  [`results/efx49_distinct_half_canonical_two_core_boundary_audit.json`](results/efx49_distinct_half_canonical_two_core_boundary_audit.json).
- Directly forbidding every two-core/Tutte witness produced exact-real
  CEGAR boundaries of 40 matching cuts and 24 Hall-selector cuts. The Hall
  master returned `unknown` at 60 seconds; the matching trace still had
  hundreds of favorite-pair repairs per model. A separate exact-real master
  on the 55 partitions outside the union of five diverse seed profiles
  returned `unknown` after 120 seconds before producing a model. Reifying
  the pair-acceptance predicates found one profile with 265 remaining
  favorite-pair repairs, then returned `unknown` on the 183-cut formula. A
  full cap-20 CP-SAT formula also returned `UNKNOWN` after 300 seconds and
  2.24 million branches. No theorem or selection counterexample is claimed.
  Replay:
  [`results/efx49_distinct_half_two_core_decision_boundary_audit.json`](results/efx49_distinct_half_two_core_decision_boundary_audit.json).
- A bounded CP-SAT CEGAR continuation sharpened the conditional frontier:
  its successive exact models retained 398, 143, and 20 favorite-pair EFX
  partitions. The last cap-20 profile has 35 balanced EFX partitions—20
  favorite-pair states and all 15 pairings of the favorite triple
  \(\{f,7,8\}\)—and 293 labeled complete EFX allocations. It has no
  two-core witness. The 331-cut continuation remained `UNKNOWN` after 900
  seconds. This proves that the two-core explanation can disappear
  while a full Hall cell remains, without refuting the conditional two-core
  claim because the 20 first-alternative repairs survive.
- The higher-leverage intermediate target is now: zero favorite-pair repairs
  force a full 15-pairing favorite-triple Hall cell. It is weaker than the
  two-core selection statement and stronger than the exact one-pairing Hall
  gate. Every audited zero-favorite-pair boundary satisfies it.
- A separately polarity-audited exact encoding now forbids every full Hall
  cell directly. Its first complement CEGAR model has no full cell but 289
  favorite-pair repairs; the next 183-cut formula returned **UNKNOWN**.
  Exact enumeration finds 304 balanced EFX partitions and 1,381 labeled
  complete EFX allocations in the trace profile. This neither proves nor
  refutes the conditional full-cell target.
- A separate cap-20 CP-SAT CEGAR trace has no full Hall cell and 357
  favorite-pair repairs. After all 357 repairs were added to the 55-cut
  complement seed, the 412-cut continuation remained `UNKNOWN` after 600
  seconds. Exact replay finds no favorite-triple repair and 3,563 labeled
  complete EFX allocations. This is a bounded solver boundary only.
- The full-cell dichotomy is independently closed on the strictly positive
  cap-5 integer domain. CP-SAT proves a 416-partition obstruction pool
  infeasible and extracts a sufficient 330-partition core; a sorting-based
  QF_LIA formula is `unsat` in Z3 and shrinks to 193 partitions. A third,
  independently generated threshold CNF shrinks further to a
  deletion-minimal 17-partition core. Its 702,820-clause formula is
  `UNSAT` in CaDiCaL; its 44,563,875-byte binary DRAT proof is accepted by
  the independently built `drat-trim` checker.
  Thus every cap-5 profile in this exact structural branch has complete EFX.
  This finite theorem neither scales to arbitrary value ratios nor closes
  the real-valued branch. See
  [`results/DISTINCT_HALF_FULL_CELL_CAP5_THEOREM.md`](results/DISTINCT_HALF_FULL_CELL_CAP5_THEOREM.md)
  and its hash-pinned audit.
- The same branch is now proof-certified through cap 6. CP-SAT closes a
  401-partition pool; an independent QF_LIA replay closes its 359-partition
  core and shrinks to 175; and an independent threshold CNF shrinks to a
  verified deletion-minimal 21-partition core. The final 1,145,090-clause
  CNF is `UNSAT`, and `drat-trim` accepts its 75,953,525-byte binary DRAT
  proof. This is still a bounded result, not a cap-free theorem. See
  [`results/DISTINCT_HALF_FULL_CELL_CAP6_THEOREM.md`](results/DISTINCT_HALF_FULL_CELL_CAP6_THEOREM.md).
- The cap-5 theorem's deletion-minimal core is now symmetry-classified.
  The 840 favorite-pair partitions form ten orbits under independent
  permutation of the four matched representatives and four unmatched
  goods; all 17 core partitions lie in six orbits whose union has 624
  partitions. The literal 17-template claim is cap-specific: a cap-6
  profile obstructs every core template while retaining 138 favorite-pair
  repairs and 2,544 labeled complete EFX allocations. Sixty of those
  repairs remain in the six-orbit family.
- The resulting six-orbit candidate is false. An exact cap-20 profile has
  no full favorite-triple Hall cell, zero six-orbit repairs, 45
  favorite-pair repairs in the omitted (U|0|RR+RR) and (U|1|RR+RU)
  orbits, and 900 labeled complete EFX allocations. It also refutes the
  separate, incomparable representative-partner selector. Adding both
  repair orbits gives a natural conservative eight-orbit successor of 780
  partitions—exactly the states whose triple is not all representatives—
  leaving two terminal orbit types. Its first correctly scoped cap-20 CP-SAT test
  returned `UNKNOWN` after 473.93 seconds without a model. Exact-real Z3
  tests of the full family and the all-B/all-C rank cells also returned
  `unknown`; a cardinal CEGAR reached a 173-cut exact-real boundary after
  one new 300-repair trace model and a 300-second continuation. Pinned cvc5 independently timed out on
  both rank cells. A later 708-partition exact-real pool also returned
  `unknown` after 600 seconds. Guarded optimization and independent
  exact-census anneals have since reduced the best positive checkpoint from
  30 to three repairs, but the exact bound still permits zero and proves no
  floor. The
  semantic audit is in
  [`results/DISTINCT_HALF_FULL_CELL_ORBIT_GATE.md`](results/DISTINCT_HALF_FULL_CELL_ORBIT_GATE.md).
- Hall-witness mining of the 21 cap-6 deletion boundaries finds a
  size-one witness in 572 of 588 low-pair cells and in all 126
  representative-pair cells. This yields an exhaustive cap-free decision
  split: either all six representative pairs have a universally rejected
  residual edge, or one representative pair has no such edge and can be
  fixed canonically as pair 1,2 after removing the incompatible agent-order
  symmetry. Exact-real Z3 tests of both branches returned `unknown` at 300
  seconds; pinned cvc5 also produced no verdict on the stronger all-cell
  singleton branch. Separately, exact rational profiles refute a one-swap
  terminal-to-six-orbit exchange, so any successful exchange must re-pair
  globally. See
  [`results/DISTINCT_HALF_RR_HALL_SPLIT_GATE.md`](results/DISTINCT_HALF_RR_HALL_SPLIT_GATE.md).
- The RR-singleton data admit a sharper compression. Seventeen of 21 cap-6
  boundaries use one unrepresented edge as the singleton witness in all six
  representative-pair cells; the other four have minimum witness-edge cover
  size two or three. The common-edge condition is exactly four
  second-order-statistic inequalities. Its 256 labeled representative maps
  have 19 conjugacy orbits, 18 already present in the bounded data. Exact-real
  common-edge and no-common-edge formulas both returned `unknown` after 300
  seconds, so this is a proof-search decomposition, not a theorem.
- Two independent three-repair profiles expose the same canonical mechanism:
  one favorite-triple Hall cell has 12 valid pairings, its three failed
  pairings share a zero-neighbor edge, and moving the commonly lower parked
  good onto that edge creates exactly three favorite-pair EFX states. The
  conversion is now a cap-free analytic lemma with a symbolic UNSAT check.
  The remaining conditional selection claim—force this motif or a full Hall
  cell when every favorite-pair state is obstructed—is open. See
  [`results/ZERO_NEIGHBOR_FAVORITE_TRIPLE_CONVERSION_LEMMA.md`](results/ZERO_NEIGHBOR_FAVORITE_TRIPLE_CONVERSION_LEMMA.md).
- The bottom-pair selection theorem is now strictly stronger than the
  common-bottom result. A residual pair need be jointly bottom-two for only
  three agents: every Hall-failed residual pairing still has a distinct
  favorite-pair EFX conversion. Therefore
  (P_f+H_{a,b}\ge15), and no favorite-pair EFX state forces a full Hall
  cell. Cardinal and sorting Z3 encodings, pinned cvc5, five exact Hall-role
  cells, and a 233,949-step CPC proof accepted by Ethos certify the theorem.
  The remaining branch has bottom-pair multiplicity at most two, hence one
  of the patterns `2+2`, `2+1+1`, or `1+1+1+1`. See
  [`results/THREE_AGENT_BOTTOM_PAIRING_CONVERSION_THEOREM.md`](results/THREE_AGENT_BOTTOM_PAIRING_CONVERSION_THEOREM.md).
- The residual bottom-pair choices now have an exhaustive symmetry audit.
  Among 30,681 labeled four-edge multisets with edge multiplicity at most
  two, exactly 20 unlabeled patterns remain: 2 of type `2+2`, 7 of type
  `2+1+1`, and 11 of type `1+1+1+1`. The first `2+2` gate refines to 9
  disjoint and 4 overlapping matching orbits. The full 180-conversion family
  now closes the disjoint pattern cap-free: cardinal and sorting Z3, cvc5,
  and an Ethos-checked CPC proof agree, with a separately certified
  19-partition core. The full 165-conversion family also closes the overlap
  pattern cap-free after a 960-element canonicalization: two Z3 encodings,
  fresh-process replay, cvc5, and a 767,596-step Ethos-checked CPC proof
  agree. Four independent searches reach the same exact three-repair `12+3`
  motif, with all repairs in one size-60 conversion orbit. Both `2+2`
  patterns are closed. The triangle-with-doubled-edge `2+1+1` pattern is
  also closed by a 225-conversion theorem: cardinal and sorting Z3, a fresh
  Z3 replay, cvc5, and a 408,508-step Ethos-checked CPC proof agree. The
  doubled-edge three-leaf star is closed by a 228-conversion theorem with a
  96-action canonicalization and a 602,783-step CPC proof accepted by Ethos.
  The central-edge and end-edge paths are closed by proof-checked
  240-conversion theorems, with Ethos accepting their 586,111- and
  333,221-step proofs. The remaining three repeated-edge patterns are also
  proof-checked. The seven-case aggregate covers 1,713 case-partitions with
  217,425,021 bytes and 2,512,561 proof steps accepted by Ethos. Therefore
  every repeated selected bottom pair is excluded from the no-repair,
  no-full-cell branch. All eleven all-distinct patterns are now also
  proof-checked. Their full formulas pass cardinal and sorting Z3, fresh
  replay, pinned cvc5, and CPC/Ethos; the eleven checked proofs total
  383,418,002 bytes and 4,603,008 proof steps. The perfect-matching case
  further reduces to a proof-checked canonical six-conversion core. Together
  with the three-agent-bottom theorem, this closes the entire strict-common-
  favorite/universal-owner-threshold-failure branch. The next
  common-favorite gate is threshold-passing but resident-Hall-deficient.
  See
  [`results/BOTTOM_PAIR_MULTIPLICITY_GATE.md`](results/BOTTOM_PAIR_MULTIPLICITY_GATE.md)
  and
  [`results/COMMON_FAVORITE_UNIVERSAL_THRESHOLD_EFX_THEOREM.md`](results/COMMON_FAVORITE_UNIVERSAL_THRESHOLD_EFX_THEOREM.md).
- The sharpest tested local exchange boundary uses the 138 eight-orbit
  states within two swaps of a terminal state. At cap 5 this is a
  nonvacuous, dual-verified theorem: the terminal stabilizers reduce all
  EFX matchings to seven canonical cells, and both CP-SAT and Z3 QF_LIA
  close every cell without a full-Hall-cell assumption. It is structurally
  informative but does not enlarge the
  existing cap-6 existence theorem. The unrestricted implication is false:
  a cap-20 profile has terminal EFX and no full Hall cell but zero
  radius-two eight-orbit repairs; its 290 eight-orbit repairs all occur at
  distance three or four. See
  [`results/DISTINCT_HALF_TERMINAL_EXCHANGE_GATE.md`](results/DISTINCT_HALF_TERMINAL_EXCHANGE_GATE.md).
- In the first canonical R-cell, the 138 radius-two targets split into 66
  preserving the favorite bundle and 72 changing its partner. The
  same-favorite selector is refuted by exact-real and cap-20 profiles with
  no full Hall cell; all their nearby repairs change the partner. The
  complementary new-partner selector is also false: a cap-20 no-full-cell
  optimization profile has zero repairs among those 72 states and 12 among
  the same-favorite states. A later optimal cap-20 profile refutes their full
  138-state union as well, while retaining 336 favorite-pair repairs and
  1,439 complete EFX allocations. Hence no radius-two selection rule
  survives; the global eight-orbit/Hall-witness dichotomy is again the live
  analytic target. See
  [`results/TERMINAL_RADIUS_TWO_EXCHANGE_CANDIDATE.md`](results/TERMINAL_RADIUS_TWO_EXCHANGE_CANDIDATE.md).
- Tutte's condition on the six residual goods has only three possible
  witness types: at least two odd components; a one-vertex deletion leaving
  at least three odd components; or a two-vertex cover of every rejected
  edge. The proof is cap-free, and all \(2^{15}\) labeled graphs were
  exhaustively checked in
  [`results/efx49_six_vertex_tutte_classification_audit.json`](results/efx49_six_vertex_tutte_classification_audit.json).
- A direct exact-real conversion master has reached a diversified boundary
  of 24 favorite-pair cuts and 9 common-low-repair cuts; the 300-second
  endpoint is `MASTER_UNKNOWN`. Separately, adversarial exact-census search
  found a branch-valid profile with no favorite-pair EFX partition and
  exactly one common-low repair. Exhaustive replay finds 252 complete EFX
  allocations, so this is a positive knife edge rather than a
  counterexample. The frozen gate is
  [`results/DISTINCT_HALF_CONVERSION_DICHOTOMY_GATE.md`](results/DISTINCT_HALF_CONVERSION_DICHOTOMY_GATE.md).
- The three-observer and three-of-four-edge full-cell lemmas remain valid
  sufficient statements, but their conditional selection claims are
  refuted by strict profiles. The two-core/Tutte condition above is the
  sharpest surviving full-cell selection target.
  The mixed threshold/Hall branch remains open after this
  universal-threshold subcase.

## Mixed threshold/Hall boundary (2026-08-01)

- The universal-owner-threshold-failure branch is closed by the cap-free,
  proof-checked strict-common-favorite theorem. The remaining exact branch
  has a threshold-passing owner--partition pair but no pair passing both the
  owner and resident Hall gates.
- Two cap-20 CP-SAT witnesses were replayed by direct literal enumeration.
  They contain 114 and 273 threshold-passing owner--partition pairs and no
  favorite-singleton EFX partition. They have 606 and 396 supporting
  unlabeled partitions, respectively, all of shape \(3+2+2+2\), and 1,532
  and 1,494 labeled complete EFX allocations.
- A third exact profile blocks every favorite-singleton partition and all six
  one-good favorite-pair conversions of a fixed passing \(3+3+2\) residual
  partition. It still has 387 balanced supporting partitions and 1,097
  labeled EFX allocations; the nearest repair is two transfers away.
- These are shortcut refutations, not EFX counterexamples. They force the
  next proof target to select a rank-maximal passing pair and allow an
  owner-changing alternating exchange into the balanced branch.
- See
  [`results/MIXED_THRESHOLD_HALL_GATE.md`](results/MIXED_THRESHOLD_HALL_GATE.md),
  [`results/efx49_common_favorite_mixed_hall_boundaries_audit.json`](results/efx49_common_favorite_mixed_hall_boundaries_audit.json),
  and
  [`results/efx49_common_favorite_mixed_hall_local6_boundary_audit.json`](results/efx49_common_favorite_mixed_hall_local6_boundary_audit.json).
- The radius-two successor blocks 63 balanced neighbors of the fixed
  \(3+3+2\) state. Direct cap-6 and cap-20 masters remain `UNKNOWN` after
  180 and 300 seconds. A cap-6 CEGAR rebuild learned 488 singleton
  obstructions across six models before its next 60-second master returned
  `UNKNOWN`. See
  [`results/efx49_common_favorite_mixed_hall_radius2_gate_audit.json`](results/efx49_common_favorite_mixed_hall_radius2_gate_audit.json).
- The rank-selection precursor is exactly false. Symmetry-reduced cap-20
  continuations grew the rank-two and zero-neighbor pools to 119 and 69
  motifs; a cap-4 continuation then found a two-type profile with exactly
  three threshold passes, all of rank one, and no favorite-singleton EFX
  partition. Independent replay finds 195 balanced supporting partitions
  and 3,690 complete allocations. The repaired four-type selector is also
  false: a cap-4 profile with four pairwise bundle-order-inequivalent rows
  has three rank-one passes, no singleton support, 599 balanced supporting
  partitions, and 3,878 complete allocations. See
  [`results/efx49_common_favorite_rank2_selection_refutation_audit.json`](results/efx49_common_favorite_rank2_selection_refutation_audit.json)
  and
  [`results/efx49_common_favorite_fourtype_rank2_refutation_audit.json`](results/efx49_common_favorite_fourtype_rank2_refutation_audit.json).
- The rank-one Hall branch has a proved common-column normal form: all three
  residents accept only one bundle, whose post-removal value strictly
  exceeds both side-bundle totals in every resident row. Owner switching
  gives two exact successor cases. More decisively, profiles with no
  favorite-singleton EFX partition refute the six one-good transfers, the
  21-state contested-partner family, and now the 30-state bridge union. The
  final cap-6 witness has three identical residents, blocks all 966 singleton
  partitions and all 30 target states, and still has 264 supporting
  partitions and 2,790 complete allocations. Its singleton failures split
  exactly into 927 three-resident/two-neighbor Hall witnesses and 39
  all-agent/three-neighbor witnesses. Fifteen nearest repairs occupy two
  further origin orbits, defining a 45-state successor. A first exact
  campaign blocks all 45 and reaches a six-singleton Hamming-two local
  minimum. The identical-resident cap-6 subcell is now dual-encoded `UNSAT`
  with one shared 392-partition pool, while the unequal-resident decision
  remains `UNKNOWN` after 900 seconds. Quotienting a duplicated resident row
  gives 12 distinct matching clauses or seven exact weighted Hall cases; the
  latter reduction agrees with literal matching on all 4,096 neighborhood
  graphs. Both possible adjacent equality cases are dual-encoded `UNSAT`
  through cap 5 with the same pool. The corresponding cap-6 masters remain
  `UNKNOWN`, placing the next repeated-row frontier at cap 6. See
  [`results/RANK_ONE_RADIUS_TWO_BRIDGE_GATE.md`](results/RANK_ONE_RADIUS_TWO_BRIDGE_GATE.md).

## Single-wall continuation boundary (2026-08-01)

- The row-merge continuation route reduces a first generic failure to one
  deleted moving-agent edge and a minimal Hall witness of size 2, 3, or 4.
- Exact positive-real models refute every one-good pivot for all three sizes.
  Sizes 2 and 3 refute every partition within two good transfers; their
  nearest EFX partitions are distance three. The post-wall profiles retain
  16 and 40 complete EFX allocations.
- The size-4 example blocks radius one and has 57 complete EFX allocations at
  minimum distance two. For the same seven-good shape, a radius-two
  obstruction is UNSAT in both Z3 and cvc5. This is a bounded solver theorem,
  not a general exchange lemma.
- Two eight-good radius-two masters returned `UNKNOWN` after 300 seconds.
  The next cap-free target is a Hall-directed exchange chain or global
  potential, not a universal one- or two-good transfer menu.
- See
  [`results/SINGLE_WALL_PIVOT_GATE.md`](results/SINGLE_WALL_PIVOT_GATE.md)
  and
  [`results/row_merge_single_wall_radius_refutation_audit.json`](results/row_merge_single_wall_radius_refutation_audit.json).

---

### Primary sources
- CGM 3 agents: EC 2020; simplifications Akrami et al. arXiv 2205.07638 (OR 2024).
- Mahara small-m & 2 types: arXiv 2008.08798 and follow-ups.
- 3 types: Ghosal–HV–Nimbhorkar–Varma, arXiv 2410.13580, EC 2025.
- Bivalued: Amanatidis et al. 2021. Matroid-rank: Babaioff–Ezra–Feige 2021.
- Almost-full 4 agents: Berger–Cohen–Feldman–Fiat, arXiv 2102.10654, AAAI 2022.
- Charity / rainbow cycle: CGMMM "A Little Charity…"; Akrami et al. arXiv 2103.01628, IJCAI 2023 / OR.
- EF2X 4 agents: Ashuri–Gkatzelis–Sgouritsa, arXiv 2412.00254, AAAI 2025.
- SAT counterexample: Akrami–Mayorov–Mehlhorn–Srinivas–Weidenbach, arXiv 2604.18216 (2026).
- Submodular/subadditive counterexamples: Mackenzie–Suzuki, arXiv 2605.06451 (2026).
- Additive chores nonexistence: He–Tao, arXiv 2606.08872 (2026).
- Partial n≥4 goods (structural): Kumar–Roy, arXiv 2507.09600 — EFX exists if 2 agents have arbitrary set-monotonic and the rest **size-monotonic** valuations (additive is not size-monotonic, so this does not crack additive goods).
