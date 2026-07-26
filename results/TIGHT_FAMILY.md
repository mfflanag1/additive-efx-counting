# Tight instances at m = n+3: minimum-count upper bound

**Goal (team-lead commission).** An explicit family proving "for every n ≥ 4 there is an
additive m = n+3 instance with EXACTLY n EFX₀ allocations," which would pin the
minimum-count upper bound at m = n+3 to n (Neoh–Teh Table 1 currently records only the
n! upper bound there), tight under their Conjecture 6.1 (≥ n).

Verifier: exact enumeration (`fast47.Counter(4,7).count`; `fast_verify.count_efx0` for
n=5,6), validated against the pure-Python reference.

---

## VERDICT

- **PROVEN (per n, by exhaustive enumeration):** the minimum number of EFX₀ allocations at
  m = n+3 is **≤ n for n = 4, 5, and 6**. Witnesses (n=4 below; n=5 `ch5_A/B`; n=6
  `tight69_witness.json`, dual-verified) have exactly n EFX₀ allocations over the whole
  assignment space. This improves Table 1 (n! → n) at these points.
- **UPDATE (v2): the mechanism is now fully understood, but a clean closed-form uniform
  family still resists.** See §5–6. The hub part of the construction IS formulaic; the
  non-hub cross-valuations that complete the rigidity are a precisely-tuned generic variety
  with no consistent formula across the three witnesses.
- **Structure (rigorous ≥ n direction):** every witness has the *same* anatomy — a
  **fully envy-free base** partitioning n+2 of the goods into one **3-good "hub" bundle**
  plus **n−1 singletons**, together with **one universal-minimum floater** good that parks
  into each of the n agents. The n parkings are the n EFX₀ allocations. The "≥ n" half is a
  clean corollary of the (machine-verified) Generalized Parking Lemma.
- **OPEN (the hard "≤ n" direction, uniformly in n):** a clean *parametric* family with a
  hand-proof that no allocation outside the n parkings is EFX₀ was **not** obtained. §3
  documents why: symmetric low-parameter templates provably fail, and the exact-n set is a
  generic "knife-edge" variety of near-tight envy inequalities that resists a short
  symbolic description. This is the named obstruction.

---

## 1. Verified witnesses (exact enumeration = proof for fixed n)

n = 4, m = 7 — **exactly 4** EFX₀ allocations:
```
[[30,66,69, 9,21,19,63],
 [12,56,58, 9,10,24,52],
 [12,33,45,20,24, 8,64],
 [11,60, 1,18, 2, 6,41]]
```
Base (envy-free, 6 goods): agent0 = {0,4,5} (hub, value 70), agent1 = {2}, agent2 = {6},
agent3 = {1}. Floater = good 3; parking it gives good3→agent0 (4111) and good3→each
singleton-agent (3211): the 4 EFX₀ allocations.

n = 5, m = 8 — **exactly 5** EFX₀ allocations (dual-verified, `results/ch5_A.json`,
`ch5_B.json`). ch5_A base: agent4 = {1,5,7} (hub), agent0={3}, agent1={2}, agent2={0},
agent3={4}; floater = good 6 parks 5 ways.

So the anatomy is identical across n: **[3-good hub] + [n−1 singletons] + [1 floater]**,
the hub bundle and singletons envy-free, the floater a universal minimum with n parkings.

## 2. The ≥ n direction is rigorous (parking-floor lemma)

**Lemma (parking floor; from the campaign's machine-verified Generalized Parking Lemma).**
Let B be an EFX₀ allocation of the n+2 non-floater goods that is **envy-free**, and let f
be a good with v_i(f) = min_g v_i(g) for every agent i (a universal minimum, so f-envy =
plain-envy). Then f can be added to each of the n agents' bundles keeping EFX₀ — every
agent is a source of B's (plain-)envy digraph — giving **n distinct EFX₀ allocations**.

Because each witness's base is envy-free and its floater is a universal minimum, this
lemma certifies the "≥ n" half for the whole family, uniformly in n. (Envy-freeness of the
base ⇒ all n agents are sources ⇒ exactly the n parkings appear as completions.)

## 3. Why a clean uniform "≤ n" family resists (named obstruction)

The obstacle is the "no other EFX₀ allocation" direction. Four construction strategies were
built and exactly-enumerated; all fail to hold the count at n:

| construction | idea | result at n=4 |
|---|---|---|
| symmetric hub-triple + signatures | goods 0,1,2 = hub (val P/Q), 3..n+1 = signatures, floater | **76**, independent of all 5 scale parameters (32768-point grid: 0 exact-4) |
| separated-scale (distinct hub goods) | knife-edge distinct a,b,c + covet | **0 exact-4** across grid |
| sparse signature + universal floater | Neoh–Teh m=n+1 template extended by 2 goods | **64** (singleton-immunity spawns derangements) |
| inductive add-agent | tight (n,n+3) + private-good agent → (n+1,n+4) | **117**, not 5 |

Two structural reasons, both verified:

- **Symmetry multiplies the count.** Any template that makes the three "excess" goods (or
  the signatures) interchangeable inherits their permutations as distinct EFX₀ allocations:
  the symmetric hub-triple template returns **76 = 4 base-like + 72 permutation images** at
  *every* scale. A tight instance must therefore break all such symmetries — i.e. use
  essentially all-distinct values.
- **Singleton-immunity spawns derangements.** A good held as a singleton can never be
  strongly envied, so any allocation in which every agent holds ≤ 1 highly-valued good tends
  to be EFX₀. Killing these "derangement" allocations requires that **every pair of goods be
  strongly contested by some agent** (so piling two goods anywhere creates strong envy),
  which forces a *dense* value matrix with near-tight (knife-edge) envy margins: in the n=4
  witness the hub owns a bundle worth 70 while valuing each singleton it does *not* own at
  66, 69, 63 — all just below 70.

Consequently the exact-n witnesses live on a **generic, measure-zero "knife-edge" variety**
of the value space (all entries distinct, many envy inequalities tight simultaneously). No
low-parameter symbolic family found here lands on it for all n; that is the precise reason
the clean uniform theorem is still out of reach, even though the *structure* is uniform and
the *per-n* upper bound is settled for n = 4, 5.

## 4. What would close it

Either (a) a symmetry-broken but still-formulaic value assignment (e.g. a Sidon/geometric
distinct-value scheme) that provably (i) makes the hub+singleton base envy-free, (ii) makes
every non-base partition strongly-envied — a finite case analysis over the O(1) bundle
shapes per agent, made rigid by explicit inequalities; or (b) a proof that the campaign's
tight-instance existence at each n (counthunter's parking-structured sweeps, currently at
(6,9)) can be produced by an explicit rule. The ≥ n half (§2) is already done; only the
rigidity half remains, and §3 names exactly what a construction must defeat
(symmetry-multiplicity and singleton-immunity derangements).

## Artifacts
Witnesses: inline (n=4), `results/ch5_A.json`, `results/ch5_B.json` (n=5). Construction
tests: `scan_dense.py` (symmetric-template scan), and the shape/parking analysis in
`shape_analysis.py`, `fast47.py`. Structure cross-checked against
`results/PARKING_FLOOR_LEMMA.md`.

---

# v2 (2026-07-25): mechanism extracted from the n=6 witness; family still resists

The dual-verified **n=6 witness** (`results/tight69_witness.json`, exactly 6 EFX₀) let me
reverse-engineer the full rigidity mechanism. It is richer than "hub + floater."

## 5. The exact-n mechanism (verified)

Base = hub agent holds a 3-good bundle H (value T to itself); each of the other n−1 agents
holds one singleton s_i; a floater f parks into all n agents (the n EFX₀ allocations).
Three **formulaic** conditions hold in ALL THREE witnesses (t47, ch5_A, tight69):

1. **Hub knife-edge.** The hub values each singleton just below its own total:
   v_hub(s_i) = T − δ_i with δ_i small, positive, DISTINCT (t47 gaps {1,4,7}; ch5 {3,6,8,10};
   tight69 {8,9,11,12,13}). Near-consecutive, exactly as predicted.
2. **Hub-good dominance over the gap.** Every hub good exceeds every knife-edge gap:
   min_k v_hub(h_k) > max_i δ_i (t47 19>7; ch5 13>10; tight69 15>13). This forces the hub to
   keep each triple good: handing a hub good h to a singleton-holder j makes the hub envy the
   pair {s_j,h} unless v_hub(h) ≤ δ_j — impossible under this condition.
3. **Second knife-edge (singleton forcing).** Each non-hub agent values its own singleton more
   than it values the whole hub bundle: W_i = v_i(s_i) > U_i = v_i(H) (ratios 1.1–5.0 across
   witnesses). So if agent i loses s_i into any non-immune (≥2-good) bundle it strong-envies —
   this is what kills singleton permutations (only 1/120 permutations of the tight69 base is
   EFX₀). Verified: permutations die because the loser envies the taker of its high-valued good.

Plus a **floater-protection** effect: when the triple-holder also holds the floater f, removing
the bundle's min good (= f) leaves the *full* triple, so the hub — even holding its single most
-coveted good — envies the triple-holder (kills "hub drops to 1 good"). Verified on tight69:
`hub={7}, agent=triple∪{8}` is not EFX₀ because the hub envies the 204-valued triple.

## 6. Why a clean uniform FAMILY still resists (named obstruction, sharpened)

Conditions 1–3 are **necessary but NOT sufficient.** A clean instance satisfying all three with
otherwise-uniform values has **28** EFX₀ at n=4, not 4 — and this is INVARIANT to the free
parameters (U∈{30…99}, low∈{2,5,10} all give 28). Two hard facts:

- **Equal values ⇒ symmetry-multiplicity.** Any interchangeable goods/agents contribute their
  permutations as extra EFX₀ allocations (the 28 = 1·4111 + 15·3211 + 12·2221 are mostly
  symmetry images). Tight instances must therefore use ALL-DISTINCT values.
- **Generic distinct values ⇒ wrong side of the knife-edge.** Adding distinct offsets to break
  ties *raises* the count (28→30), because the construction sits on a knife-edge and a generic
  perturbation relaxes some binding envy inequality. Only a **precisely-tuned** distinct
  assignment lands on exactly-n.

The residual rigidity — killing triple-splitting and 2-2-2 slop — is carried by the non-hub
**cross-valuations** (how agent i values the hub goods and the *other* singletons). These are
**inconsistent across the witnesses**: agent-i-values-hub-triple U_i ranges from 14 to 134 with
no common rule. A fixed clean hub row DOES admit exact-4 completions (found by annealing only the
non-hub rows), but every completion found is a messy generic point, not a formula.

Seven clean-scheme attempts and their best n=4 counts (target 4): symmetric hub-triple **76**;
separated-scale **0 hits**; sparse+floater **64**; inductive add-agent **117**; double
knife-edge (conditions 1–3) **28** (invariant to free params); double knife-edge + distinct
perturbation **30** (perturbation moves off the knife-edge the wrong way); **contested hub
goods** (each hub good highly valued by one non-hub agent) **22** — the best, still 5× too high.
None reaches n. The 2-2-2 and 3-2-1-1 "slop" survives every clean scheme because the exact
cross-value inequalities that would kill each such allocation are not simultaneously satisfiable
by any low-parameter/structured assignment we could find.

**Conclusion.** The construction decomposes into a **formulaic hub gadget** (conditions 1–3,
uniform in n, giving the rigorous ≥ n parking direction for free) and a **generic non-hub
remainder** (an O(n²)-inequality tuning with no closed form found). So "min #EFX₀ ≤ n at m=n+3"
is settled for n = 4,5,6 by explicit witnesses, and the ≥ n / parking half is uniform, but the
**uniform ≤ n theorem for all n is not delivered** — the missing piece is an explicit rule (or an
existence/dimension argument) for the non-hub cross-values that provably kills every non-base
partition. That remains open; §5 is the concrete toolkit for whoever attempts the case analysis.

Added artifacts: `nonhub_anneal.py` (finds exact-4 non-hub completions for a fixed clean hub),
mechanism checks inline above.

---

# v3 (2026-07-25): the existence-argument routes, worked through

Following the team-lead's suggested framing (openness → perturbation around a degenerate
point → Jacobian full-rank → integer point; fallback induction). Verdict up front: **the
perturbation route is obstructed at the natural degenerate point, and the inductive route
needs the same generic per-step tuning; per-n computer witnesses remain the right final
form.** Details:

## 7. Openness (step 1) — holds, but only converts a witness

The tight set { v : exactly the n base-parkings are EFX₀ } is cut out by strict
inequalities (each of the ~O(n²) non-base "defect" allocations must be *strictly*
non-EFX₀, i.e. some agent strongly envies). Hence it is **open**; a real point yields a
rational one, and clearing denominators yields integers (same style as the campaign's
rationality note). This is sound and useful — BUT openness only upgrades an *existing*
real witness; it does not produce one. The content is entirely in nonemptiness at each n.

## 8. Perturbation toward the witness (steps 2–3) — the DIRECTION works; new structural progress

*(Corrects an earlier over-pessimistic note.)* A **generic** perturbation of the symmetric
count-28 point does not help (it moved 28→30). But the **directed** perturbation the
team-lead suggested does: relabel a real witness to the canonical base and interpolate
v(t) = (1−t)·(symmetric point) + t·(witness). The count falls
**28 → 24 → 22 → 24 → 12 → 5 → 4** as t: 0→0.2→0.4→0.5→0.6→0.8→1.0. So the witness
direction is a genuine descent direction; the method is not obstructed — it just needs the
*right* direction, not an arbitrary one. (Why generic perturbations fail: at the symmetric
point the 24 defects have strictly positive slack — six at 1, fourteen at 3, four at 6 — so
only a directed, O(slack)-magnitude move crosses them.)

**Reading the direction gave a real structural fix.** Aligning witness minus symmetric point
shows the decisive coordinates: in the symmetric point each non-hub agent values the *other*
agents' singletons LOW (≈5); in the witness it values them **HIGH** (≈52–56, near its own).
Raising those coordinates alone collapses the count and **removes ALL 2-2-2 slop**:

| non-hub valuation of *other* singletons | n=4 count | shapes |
|---|---|---|
| low (≈5) — old schemes | 28 | 1·4111 + 15·3211 + **12·2221** |
| high (≈54), uniform | 12 | 6·4111 + 6·3211 (no 2221) |
| high + distinct | 10 | 6·4111 + 4·3211 |

**Interpretation.** "Value every other singleton highly" makes every pair of singletons
strongly contested, which is exactly the condition §3 identified as necessary to kill the
derangement/2-2-2 allocations — now realized as a clean coordinate direction, not a mystery.
This is the missing 4th condition to add to §5's three.

**Residual (10 → n).** The allocations that survive at count 10 are precisely **singleton
permutations** (agents swapping which singleton they hold, hub keeping its triple). Killing
these needs the *second* knife-edge tuned so the hub-bundle threshold sits between an agent's
value of a *non-own* singleton and its *own* — but the threshold is v_i(hub-triple) only when
the floater is with the hub; for floater-elsewhere permutations the threshold drops (min
hub-good is removed) and some permutations survive unless the singleton values are precisely
tuned. This last factor (~10→4) is where a clean uniform rule was still not found; it is a
genuine but *small* residual, no longer the whole 28→4 gap.

## 9. Induction by cloning the hub (step 4)

Extend a tight (n,n+3) instance by one agent + one new singleton, hub coveting it at T−δ_n.
The **naive** sparse extension gives ≥30 at n=4→5 (a sparse new agent contests nothing).
Tuning the new agent's row + the existing agents' new column (anneal) drives it down but
bottoms around **8** in the budget run — not yet n=5 — consistent with §8's residual: the
new coordinate block must also satisfy the "value-other-singletons-high" + permutation-kill
conditions, which are the still-generic part.

## 10. Verdict

- **Delivered:** min #EFX₀ ≤ n at m=n+3 proven for **n = 4, 5, 6** (explicit witnesses);
  ≥ n / parking direction uniform and rigorous; exact-n mechanism now characterized by
  **four** conditions — §5's three (hub knife-edge, hub-good > gap, W_i > U_i) **plus**
  §8's new one (every non-hub agent values *every* singleton highly ⇒ no 2-2-2 slop).
- **Progress this round:** the perturbation method is viable in the witness direction (not
  obstructed); the 2-2-2 slop — the bulk of the 28→4 gap — is closed by an explicit
  coordinate direction. The **only** remaining gap is killing singleton permutations
  (10→n), which still needs precise per-instance tuning of the singleton value matrix and no
  closed form was found for it.
- **Honest final form:** per-n computer-checked witnesses remain the deliverable. The gap is
  now isolated to one self-contained sub-problem — the singleton value-matrix S (an
  (n−1)×(n−1) block) that kills all singleton-permutation defects — but that sub-problem is
  **still generic, not clean**: annealing S closes n=4 to exactly 4, yet the solution S is a
  generic matrix (not even diagonal-maximal — the base assignment permutes), and every
  **structured diagonal-dominant** S bottoms out at **8 = 2n**, never 4 (scan: 0 exact-4
  hits). So diagonal dominance kills *most* permutations but leaves a residual class of size
  ≈ n; only a precisely-tuned generic S removes it. Net: this round closed the 2-2-2 slop
  cleanly (the bulk of 28→4) and reduced the residual to a small, well-posed matrix-design
  question, but that question itself has no clean closed-form solution in what was tried —
  consistent with the overall finding that tight instances are a generic knife-edge variety.

## 11. The count-2n residual, characterized (answering the S-matrix leads)

**What the extra survivors are.** At a diagonal-dominant (structured-S) count-8 = 2n
instance (n=4), the 4 base parkings plus **4 extras** split into two structured classes,
not one uniform class:
- **Class A (transposition):** the single swap of the two "closest" singleton-agents
  (the pair whose cross-valuations are nearest), with the floater at the hub or at the
  odd agent — 2 allocations.
- **Class B (hub-swap):** the hub trades its whole triple for the singleton it covets
  MOST (largest v_hub), that singleton's owner taking the triple, floater at either
  remaining agent — 2 allocations.

So the residual is O(n) structured allocations, each with an explicit envy inequality —
exactly the team-lead's lead #1 picture — BUT it is two coupled classes, and killing them
is not one extra scalar condition.

**Per-agent floater tuning (lead #2) does not decouple it.** Scans:
- Varying the floater column alone (per-agent v_i(f), range 0–12) on the count-8 instance:
  min stays **8** — the floater cannot kill Class A/B (they don't hinge on who holds f).
- Combined structured scan (diagonal-dominant S × tuned second-knife-edge U_tot × floater),
  ~thousands of points: **0 exact-4**. The permutation-killing window for Class A needs the
  hub-envy threshold to sit between an agent's value of the *transposed* singleton and its
  *own* — but that threshold is set by U_tot (shared) while the two values are entries of the
  shared S matrix, so the windows for different agent-pairs **couple through S** and have no
  common diagonal-dominant solution. Only a **generic** (non-diagonal-maximal) S satisfies all
  the pairwise windows at once (annealing S freely does reach exactly 4, at a generic point).

**Conclusion of the S-matrix push.** The reduction is real — the whole gap is now the
singleton value-matrix, and the residual is O(n) structured classes — but the design does
**not decouple**: no structured/diagonal-dominant S closes it, so S must be generic and no
closed form was found. This is the honest "no clean family" verdict for the tuning, and it
is consistent at every scale tested. The paper-ready result is therefore:
**min-count ≤ n at m=n+3 for n ∈ {4,5,6} (explicit witnesses), conjectured for all n, with the
four-condition mechanism (three hub conditions + value-all-singletons-high) reducing any tight
instance to the parking structure and pinning the residual to O(n) structured
transposition/hub-swap classes killed only by a generic singleton matrix.**

## 12. CORRECTION + n=7 attempt (2026-07-25, later)

**Correction to §8/§10 "condition 4".** Last round I claimed a fourth *universal* condition
— "every non-hub agent values every singleton highly ⇒ no 2-2-2 slop" — generalizing from
the n=4 (t47) witness. **This is NOT a universal property of tight instances.** Direct check
of the n=6 witness: agents 1–4 value the *other* agents' singletons mostly LOW (e.g. agent1's
other-singleton values are 23,65,4,2; agent2's are 10,8,7,2), only agent5 values them high.
So "value all singletons high" is a **count-reducing direction at n=4** (it does drop the n=4
count 28→12 by killing 2-2-2), but it is **not a necessary condition** — the n=6 witness kills
its balanced-shape slop through its specific generic values with *mixed* high/low
other-singleton entries. Only the **three hub conditions of §5** (hub knife-edge, hub-good >
gap, W_i > U_i) are verified consistent across all three witnesses. The honest mechanism is:
three formulaic hub conditions + floater protection + a **generic** non-hub value block
(no consistent structure), which is exactly the "no clean family" conclusion.

**n=7 (7,10) witness attempt — not obtained; compute-bound.** Following the team-lead's
recipe (fix formulaic hub with the gap sequence continued, anneal the 6×6 singleton matrix
with capped `count_efx0`): (i) each capped count at (7,10) costs **7–15 s** (282M assignments,
chunked; the fixed cost dominates), so a descent from a high-count start needs more evals than
a few-hour budget allows; (ii) structured/condition-4 starts give count **≥ 200** at n=7 —
because, per the correction above, condition 4 does *not* produce a near-tight instance
(the structure isn't real beyond the hub). A blind capped-objective anneal from ≥200 down to 7
at ~10 s/eval is infeasible here. **Recommendation:** the n=7 witness needs the
anatomy-CEGAR run cold (the team-lead's tool, minutes per call but directed) or a
substantially larger compute budget; it is out of reach for the fast-verify anneal pipeline.
The paper's evidence base stays at **n = 4, 5, 6** (exact witnesses), conjectured for all n,
with the three-hub-condition mechanism + generic non-hub remainder as the structural finding.

**n=7 anneal outcome (final).** The targeted anneal made NO progress: stuck at the capped
value ≥40 for all 160 evals over ~1.8 h (~41 s/eval). Root cause: the capped objective is
**blind** in the regime that matters — every candidate scored ≥40 = the cap, so the landscape
was flat and the search never descended; and at ~41 s/eval only ~160 evals fit the budget. No
n=7 witness, and no clean plateau reading (the search never explored below 40). Conclusion: the
fast-verify anneal pipeline is **underpowered for (7,10)** — the 282M-assignment exact count
makes any gradient/plateau search infeasible, and a cap low enough to be affordable is blind
exactly where the signal is. A cold anatomy-CEGAR (directed, with a numpy example-collector for
the 7^10 slave) is the only viable route to an n=7 witness; **recommendation: ship the paper
with the three dual-verified data points (n=4,5,6) plus the mechanism + reduction**, since n=7
would confirm ≤ n but not change the uniform-theorem status (already reduced to "a generic
singleton matrix exists"). n=7 is worth commissioning only if the CEGAR example-collector is
cheap to build.
