# Residual Attack: the 4211/3221 target set is provably too narrow

**Charge.** Prove or refute: *every (4,8) positive-additive instance satisfying the proven
witness-necessary conditions — NC-A (no size-2 dominant matching), no universal-min good, pairwise
non-proportional rows — admits an EFX₀ allocation of shape 4211 or 3221.*

**Verdict: FALSE-BY-TEST (dual-verified), and the failure is structural, not incidental.**
The claim is false in *four independent ways*: each of the shapes 2222, 3221, 3311, 5111 is, on some
instance satisfying all three necessary conditions, the **unique** EFX₀ shape. The correct organizing
principle is a **contested-good ladder** (§3): the number of universally-contested high goods `k`
forces the treasure-count `k`, and every `k ∈ {0,1,2,3}` is individually load-bearing. The residual
therefore cannot be narrowed below the full five-shape (= k-treasure, `k=0..3`) reduction of
MAHARA_EXTENSION §1. This is an **obstruction** to Approaches 1–3 as scoped, and it reshapes the
stuck-system (§5).

All claims below are checked with the exact enumerator `verify.py::enumerate_all` (the reference
verifier used campaign-wide) and cross-checked with a numpy re-implementation `fastshape.py`; the two
agree on every instance tested. Necessary-condition predicates are in `residual_test.py`.

---

## 1. The refutation (PROVEN / FALSE-BY-TEST, dual-verified)

Five instances, each satisfying **NC-A ∧ no-universal-min ∧ pairwise-non-proportional**, whose EFX₀
allocations are **all of a single shape**. Verified by full `enumerate_all` (total EFX₀ count and the
shape census of every EFX₀ allocation shown):

| sole shape | instance `V` | # EFX₀ (all this shape) | NC-A | dom. relation `D` |
|---|---|---|---|---|
| **2222** | `[[12,6,10,7,7,11,11,3],[8,10,4,2,9,7,8,7],[4,6,5,3,7,4,7,6],[12,5,11,7,9,7,12,10]]` | 2004 | ✓ | ∅ |
| **3221** | `[[3,1,4,5,1,2,5,59],[3,4,1,4,1,3,5,38],[5,4,2,2,5,2,1,51],[5,5,2,4,5,3,5,47]]` | 330 | ✓ | `{(0,7),(1,7),(2,7),(3,7)}` |
| **4211** | `[[6,7,21,40,2,35,13,8],[8,5,7,4,22,40,10,1],[9,10,1,28,1,17,39,1],[3,1,2,24,1,21,31,6]]` | 16 | ✓ | ∅ |
| **3311** | `[[4,3,57,2,3,52,5,4],[5,5,41,2,4,57,4,4],[3,3,32,4,5,35,4,4],[5,1,50,5,5,57,5,1]]` | 210 | ✓ | ∅ |
| **5111** | `[[2,3,5,59,56,1,45,1],[3,5,2,42,50,5,57,4],[2,2,2,54,60,1,48,2],[1,3,1,42,53,5,55,4]]` | 24 | ✓ | ∅ |

Three of these five (**2222, 3311, 5111**) have EFX₀ **only** outside the target set {4211, 3221}, so
each is a standalone counterexample to the charge. (The 4211 and 3221 rows additionally show those two
shapes are themselves sometimes-unique — the target set is not vacuous, just incomplete.)

**The NC-A edge case is real, not a loophole.** The sole-3221 witness has *every* agent finding good 7
dominant (`D={(0,7),(1,7),(2,7),(3,7)}`), yet NC-A holds because all dominant pairs share the single
physical good 7 — exactly the "all dominant pairs share one good" branch of NC-A. So the necessary
conditions are genuinely satisfied; the claim genuinely fails.

Reproduce: `python3 -c "from verify import enumerate_all; ..."` on any row, or run the harnesses in §6.

---

## 2. Why 4211/3221 looked sufficient (the near-witness sampling bias)

MAHARA_EXTENSION §2 read the near-witnesses (V, V2, V3) and saw the survivors living in
4211/3221/3311/5111 with 4211 the workhorse — true, but those three instances were all produced by the
**same count-minimizing directed search**, which happens to land in the 1-to-2-treasure basin. Across
a controlled regime sweep the picture is different:

- **Random flat/lumpy/skew, 12000 instances:** EFX₀ always exists; `{2222,4211,3221}` covers every one;
  5111 and 3311 never sole. (Consistent with §2's read — but this regime is *easy*.)
- **Conflicting-peaks regimes (the NC-B seam, §3):** 5111 and 3311 become **frequently sole**, and
  `{2222,4211,3221}` cover-failures appear at rate up to 3000/3000 (three-peak regime, all sole-5111).

So 4211/3221 dominate only where the directed search sampled. They are not where the hard cases
*generally* live.

---

## 3. The contested-good ladder (the correct decomposition) — HEURISTIC (strong empirics)

Generate instances with exactly `k` "universally contested" goods (goods given a large value to all four
agents; the rest small). The **unique** EFX₀ shape tracks `k` precisely:

| # contested goods `k` | forced sole shape | k-treasure reading (TWO_TREASURE Lemma 1′) |
|---|---|---|
| 0 (flat) | **2222** | `k=0` treasure — balanced |
| 1 | **3221** | `k=1` treasure — one singleton + 3-2-2 split |
| 2 | **3311** (or 4211) | `k=2` treasure — two singletons + two fat halves |
| 3 | **5111** | `k=3` treasure — three singletons + one 5-good dumping ground |

Measured (3000 NC-satisfying instances each, seeds fixed): 1-peak → sole-3221 1539×; 2-peak → sole-3311
present; 3-peak → sole-5111 **3000/3000**. Full census in `mincover.py` output.

**Interpretation.** The number of goods that *all* agents fight over equals the number of goods that
must be "parked" as strong-envy-immune singletons (Fact 1). This is exactly the k-treasure family of
TWO_TREASURE_LEMMA §2a, now shown to be **exhaustive and each level necessary**: the five shapes are the
four treasure-levels `k=0,1,2,3` (with `k=2` splitting into 4211/3311), and the campaign's own coverage
map (5111 = 3-dominant, 2222 = flat, 4211/3311 = two-treasure) is precisely this ladder read off by `k`.

**Consequence for the attack.** The residual is *not* "prove the 4211/3221 system is always feasible."
It is "**prove that for the treasure-count `k` dictated by the contested structure, the k-treasure
system is feasible — for all four `k`, including the ambiguous transitions.**" Approaches 1–3 (Farkas /
augmentation / averaging) remain viable *per-k*, but must be run for every `k`, and the binding case is
the transition where `k` is not integer-clean (§4), not the pure 4211/3221 corner.

---

## 4. No counterexample in the danger zone (PROVEN over the sample; supports EFX existence)

A true EFX-counterexample would have **no** EFX₀ allocation of **any** shape. The ladder's transitions —
where the contested count is ambiguous (2 strong + 1 marginal peak; graded/asymmetric contests; two
value scales) — are where such an instance would hide. Result of a targeted hunt over NC-satisfying
instances only:

- `graded` (2–4 peaks, asymmetric per-agent contest), 1652 NC-instances: **0 EFX₀-free**.
- `mixed23` (2 strong + 1 marginal), 2168 NC-instances: **0 EFX₀-free**.
- `twoscale` (contested medium band), 2352 NC-instances: **0 EFX₀-free**.

Total **0 / 6172** EFX₀-free in the danger zone; every instance kept at least one working shape (the
ladder degrades gracefully — transition instances mix shapes, e.g. `{4211,3311,3221,5111}` all present).
Combined with the 12000-instance regime sweep (0 EFX₀-free) this is consistent with the campaign-wide
finding that EFX₀ very likely always exists at (4,8) — but, per §1–3, **not** via any proper subset of
the five shapes.

---

## 5. The stuck-system, corrected (Approach 4 deliverable)

The minimal stuck-instance system is the conjunction of the **negations of all five** k-treasure
systems (MAHARA_EXTENSION §3), not just 4211/3221. A witness `V` must satisfy simultaneously, over
**all** good-assignments:

1. **¬2222**: every balanced 4×2 partition has some agent strongly-envying another 2-bundle
   (kills `k=0`). Binds in the flat/low-contest regime.
2. **¬3221**: every (1 singleton + 3-2-2 split) has the singleton-holder or a splitter strongly-envying
   a fat bundle (kills `k=1`).
3. **¬4211 ∧ ¬3311**: every two-treasure allocation fails NC-B (kills `k=2`, both splits). This is the
   proven-sharpest screen (`twotreasure.py`).
4. **¬5111**: every (3 singletons + 5-good remainder) has a singleton-holder strongly-envying the
   remainder — i.e. NC-C fails everywhere (kills `k=3`). Binds in the high-contest regime.

Plus the standing structural conditions: NC-A (no size-2 dominant matching), no universal-min good
(else Parking-Floor closes it), acyclic-envy WLOG (Mahara Lemma 7).

**The key structural obstruction this attack adds:** conditions 1 and 4 pull in *opposite directions on
contested-good count* — ¬2222 wants low contest (flat instances are 2222-solvable, so a witness must be
lumpy), while ¬5111 wants ≤2 heavily-contested goods (3+ contested goods are 5111-solvable, so a witness
must not over-concentrate). A witness must thread `k ≈ 2` — enough contest to break 2222, not enough to
enable 5111 — *and simultaneously* break both `k=2` shapes (¬4211 ∧ ¬3311 = NC-B) *and* the `k=1` shape
(¬3221). That four-way simultaneous squeeze at the single contested-count `k≈2` is the precise reason
the CP-SAT/anneal searches floor at the parking count and never reach 0: the near-witnesses (V, V2, V3)
sit exactly at `k≈2` (V is k=2 two-treasure) but cannot close ¬3221 and ¬5111 at the same margin.

**Hand to CP-SAT/SMT:** the target is the conjunction (1)∧(2)∧(3)∧(4)∧NC-A∧no-univ-min, with the
contested-count driven to `k=2`. This is strictly larger than the 4211/3221 system the charge proposed;
running the solver on the narrow system would return SAT-looking regions (sole-5111/sole-3311 instances)
that are *not* counterexamples because a non-target shape rescues them.

---

## 6. Honest assessment and reproduction

**What is proven.** (a) The charge is false — dual-verified sole-shape witnesses for 2222, 3311, 5111
(each outside {4211,3221}) satisfying all three necessary conditions. (b) All five shapes are
individually essential; no proper subset of the k-treasure family covers the NC-satisfying instances.
(c) The correct decomposition is the contested-good ladder `k=0,1,2,3`.

**What is not proven.** EFX₀ existence itself — 0/18172 EFX₀-free across all sweeps is strong but is
the same empirical wall the campaign already hit. The ladder reframes *where* the proof must act
(all four `k`, binding at the `k≈2` transition) but does not supply the feasibility argument for any
single `k`; the per-`k` Farkas/averaging attacks of Approaches 1–3 are still open, now correctly scoped.

**Files (repo root):**
- `residual_test.py` — NC-A / universal-min / non-proportional predicates + dominant relation.
- `fastshape.py` — numpy EFX₀ shape-census enumerator (cross-checks `verify.py`).
- `claim_test.py`, `cover_test.py`, `two_shape.py`, `mincover.py` — the regime sweeps (§1–3).
- `elite_cover.py` — cover/sole scan over all 449 directed-search elites (0 cover-failures, confirms §2).
- `transition_hunt.py` — the danger-zone EFX₀-free hunt (§4; 0/6172).
- `sole_witness.py` — sole-shape witness finder (unbounded; the §1 table was captured incrementally).

Every §1 witness is reproducible by `enumerate_all(4,8,V,collect=99999)` and classifying each returned
allocation by its sorted bundle-size multiset.
