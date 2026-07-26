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
- **No published bound of the form "a minimal additive counterexample can be taken with values ≤ f(n,m)"** was found. This appears to be **not established** — a genuine gap the hunt could exploit or would have to assume.
- What *is* known and adjacent:
  - The **monotone/submodular** counterexamples are stated with **bounded integer values** (SAT-solver output; the 2604.18216 witness uses small integer marginals, single-good values ~11–131, ≤ 256 distinct subset values). This shows small-integer witnesses suffice **once you leave additive** — a hint that if an additive witness exists it may also be small-integer, but there is **no theorem** guaranteeing this for the additive class.
  - **WLOG normalizations** standard in the field: EFX is invariant to per-agent positive scaling; one may assume rational (hence, by scaling, integer) values without loss for *any fixed instance*, but this does **not** bound the magnitude for a hypothetical minimal instance.
  - The 2605.06451 α-EFX bound (α > 1/∛2) is an **inapproximability** magnitude, not a value-magnitude bound.
- **Practical implication for the hunt:** you must **assume** a value cap (e.g. small integers, values ≤ V) to make an SMT/CEGAR/exhaustive search finite; there is currently **no proof** that a minimal additive counterexample lives under any such cap. Any exhaustion result you produce is therefore **conditional on the value bound and on m**, and should be reported as such. Establishing even a weak `f(n,m)` bound would itself be a publishable contribution and would make an exhaustion result unconditional.

### C. Why the 2604.18216 SAT encoding does not extend to additive (and stated next targets)
- The authors **explicitly leave additive open** ("For n ≥ 4, it is not known whether EFX allocations always exist even when all agents have additive valuations"), and note that even for 3 agents, general-valuation existence is only known under structural assumptions (one agent MMS-feasible).
- **Why the encoding stops at monotone/submodular (inferred from the method, partially stated):** the SAT encoding treats each agent's valuation as an **independent value per subset** (2^m free Boolean-encoded variables per agent) constrained only by monotonicity. **Additivity is a far stronger global constraint** — the 2^m subset values collapse to **m per agent** (`v_i(S) = Σ_{g∈S} v_i(g)`), with all subset comparisons forced to be consistent sums. This (a) **shrinks the model space drastically**, so the monotone SAT witness (which needs 256 distinct, non-additive subset values with wildly varying marginals) is **not realizable additively**, and (b) turns the search into reasoning over **linear arithmetic on the m base values**, which is an **SMT/ILP** problem (values, not just Booleans), not a pure SAT problem. So the tooling itself has to change: **additive needs an SMT (linear-arithmetic) or MILP/CEGAR encoding over the m·n base values**, not the subset-indicator SAT encoding used for monotone.
- **Stated / implied next targets:** additive n ≥ 4 (the headline open case); tightening the 3-agent boundary (they resolved 3 agents/7 goods positive, ≥ n+5 negative for monotone — the additive 3-agent case is already known safe by CGM, so the action is n ≥ 4). No explicit additive-specific roadmap is given in the paper beyond flagging the open problem.

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

**Search-design caveat (from Intel B):** any negative/exhaustion result is only as strong as its **value cap and m cap** — no theorem currently bounds a minimal additive witness, so state those bounds explicitly.

---

## Boundary intelligence (the m = n+4 cell)

**Decision for campaign targeting: KEEP the search cell at (4,8). Do NOT advance to m=9.** Monotone (4,8) is itself **unresolved**, so it yields no free implication that would let us skip m=8 for additive.

### 1. Is monotone (4,8) known safe or false? — OPEN (neither).
The 2604.18216 SAT results are **only for n=3**, obtained by direct SAT solving:
- **(3,7) = (n, n+4): SAFE** — UNSAT established in ~30 hours (with solver hints; m=6 ran in <1s, m=7 took >2 days, hence the hints).
- **(3,8) = (n, n+5): COUNTEREXAMPLE** — SAT witness found in ~20 hours.

For **n ≥ 4 they did NOT run SAT** — direct solving was abandoned as computationally infeasible at that size. The n ≥ 4 counterexamples at **m ≥ n+5** come from an **algebraic extension** of the (3,8) witness (Section 7), *not* from solving. Consequently:

| n=4 cell | status for MONOTONE | status for ADDITIVE |
|---|---|---|
| m ≤ 7 (= n+3) | SAFE (Mahara, general valuations) | SAFE (Mahara) |
| **m = 8 (= n+4)** | **OPEN** — never solved; too large for SAT | **OPEN — live search cell** |
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

**Practical takeaways for the hunt:** (a) the additive search must actually resolve (4,8) and (4,9) on its own — the monotone results retire neither; (b) any attempt to reuse the SAT witness fails at the additive constraint precisely in the (3,8) core, so effort is better spent on a native additive SMT/MILP search over the (4,8)/(4,9) base values than on trying to round the monotone gadget into additivity.

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
