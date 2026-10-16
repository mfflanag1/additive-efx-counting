# Independent residual-return proposal and opposite-model QA

16 October 2026. Historical review evidence, **not the accepted theorem**.
The raw independent proposal below is rejected as written: its all-G variant omitted
the p-augmented junction from the failure family, and its alternating-cycle section
was not a precise theorem. The useful one-ordinary-run construction was independently
checked and incorporated, with corrected scope, as Theorem 4 of
[the physical cycle proof](PHYSICAL_CYCLE_RELEASE_20261016.md).
The final verification record records adjudication and executable regressions.

Research run: `20261016-143119-d0493cd6`, Fable 5.1, 413.25 seconds.
Opposite-model QA: `qa-71f7e1f6ea`, Codex, verdict `revise`.
Neither review is external specialist endorsement. The raw research did not execute
an arithmetic verifier; the final repository verifier supplies that check.

## Raw independent proposal (superseded where corrected)

Nothing further is needed: the five supplied files contain the whole setting, and the verifier scripts named in A1 §8 are not present in this workspace (so I cannot suggest running them here; all calibration arithmetic below is hand-computed from the integer tables in the two JSON files and was not machine-executed).

# Result

## 0. Hypotheses actually used

From `PHYSICAL_ADMISSION_A1_20261016.md` §1–2 only:

- (H1) four additive, strictly positive valuations on a finite ground set G; fixed priority π;
- (H2) O is a lexicographic maximum over **all** partial EFX allocations F (complete ones included), with charity exactly {p} (A1 §1 lines 9–16; if the charity is empty O is itself complete EFX and nothing below is needed);
- (H3) the exhaustive augmented minimal-core graph of Prop. 1: every edge i→j carries an inclusion-minimal, hence O-common-safe, core C ⊆ O_j ∪ {p} with v_i(C) > u_i(O);
- (H4) Prop. 2 / Cor. 3a consequences: no self-champion; a p-free core is the whole O_j; a p-core is R ∪ {p} with R, D = O_j∖R both nonempty, and v_j(D) ≥ v_j(p).

Not used: bundle nondegeneracy, GG, three nonsingletons, numerical BASE, twelve roles, no-complete-EFX. (The last is not needed because F contains complete allocations, so a Pareto-improving EFX allocation — complete or not — already contradicts (H2).)

## 1. Notation

Cycle i_1→i_2→…→i_L→i_1 (L ∈ {2,3,4}), simple, with ≥2 p-cores (Cor. 3). Index mod L. Edge i_t→i_{t+1} is a **p-edge** with core R_{t+1} ∪ {p} (R_{t+1} ⊊ O_{i_{t+1}}, D_{t+1} = O_{i_{t+1}}∖R_{t+1}, both nonempty) or an **ordinary edge** with core O_{i_{t+1}}. Each vertex has a type (in,out) ∈ {o,p}². An **ordinary run** is a maximal segment of consecutive ordinary edges. With ≥2 p-edges and L ≤ 4 the only cyclic words are: pp, ppp, ppo, pppp, pppo, ppoo (zero or one ordinary run) and popo (two runs).

## 2. Lemma 1 (next-packet preference at a p-in/p-out vertex)

If i_{t-1}→i_t and i_t→i_{t+1} are both p-edges, then v_{i_t}(R_{t+1}) > v_{i_t}(R_t).

*Proof.* Champion: v_{i_t}(R_{t+1}) + v_{i_t}(p) > u_{i_t}(O) = v_{i_t}(R_t) + v_{i_t}(D_t). No self-champion on the incoming core (Cor. 3a, lines 111–113): v_{i_t}(D_t) ≥ v_{i_t}(p). Subtract. ∎

## 3. Lemma 2 (one-run contraction exchange)

Let the cycle have at most one ordinary run. Define Z:

| vertex type of i_t | Z_{i_t} | improvement | O-common-safe? |
|---|---|---|---|
| (o,o) | O_{i_{t+1}} | ordinary envy | yes (original EFX) |
| (o,p) — exactly one such vertex, if a run exists | R_{t+1} ∪ {p} | champion | yes (minimality) |
| (p,p) | D_t ∪ R_{t+1} | Lemma 1 + additivity | **not known** |
| (p,o) | D_t ∪ O_{i_{t+1}} | v(O_{i_{t+1}}) > u(O), D_t ≥ 0 | **not known** |

Non-participants keep O_x. If there is no ordinary run, p stays in charity (or may be added to any one participant's bundle).

Claims. (a) Z is a physical allocation of G; with one run it is **complete** (each p-in O_{i_t} is split R_t ⊔ D_t, R_t goes to i_{t-1}, D_t stays; each o-in O_{i_t} goes whole to i_{t-1}; p goes to the unique (o,p) vertex; the summands are disjoint because the cycle is simple). (b) Every participant strictly improves, every other agent is unchanged; hence v_x(Z_x) ≥ u_x(O) for all x and Z is strictly lex-improving for **every** π — no floor is reset and no comparison with (1,1,1,1) or γ (Prop. 7) is needed. (c) Every EFX comparison whose target bundle is of the first two row types holds automatically: v_x(B∖g) ≤ u_x(O) ≤ v_x(Z_x). Therefore **the only possible EFX failures are**

  (W) v_x(Z_{i_t} ∖ {g}) > v_x(Z_x), x ≠ i_t, i_t a p-in vertex, g ∈ Z_{i_t},

with Z_{i_t} = D_t ∪ R_{t+1} or D_t ∪ O_{i_{t+1}}. (d) Under (H2), Z is **not** EFX, so some (W) holds. ∎

Reading: the ordinary run is contracted away — it generates no obligations and no floor change; all obligations sit on the "junction" bundles of the p-segment, exactly one per p-in vertex. With no ordinary run (pp, ppp, pppp) the same holds for the pure R-rotation with p left in charity, and for each of the L variants that additionally hand p to one participant; all L+1 variants are Pareto-improving and all must fail (W) at a global maximum.

## 4. Two-run case popo — conditional only

Vertices (p,o),(o,p),(p,o),(o,p): two vertices need p. The analogous exchange pays one (o,p) vertex u with R only; v_u(R) ≤ u_u(O), so u is unpaid and must satisfy EFX against even the common-safe bundles. The exchange is lex-improving only if some strictly improving participant precedes u in π and v_u(R_{u+1}) ≥ max tails. The alternative of paying u with the whole O_{i_{u+1}} needs v_u(D_{u+1}) ≥ v_u(p), which is not derivable. **Labeled conditional / not closed.** (Word correspondences to the archive's GLGS etc. are only mnemonic; A1 §7 lines 319–320 warns against identifying the graphs.)

## 5. Failure of the naive transitive contraction, with exact obstruction

A tempting unconditional contraction "ordinary edge i→j followed by p-edge j→k gives a direct edge i→k (or an exit)" is false. In the nine-good calibration (`physical_admission_champion_cores_20261016.json`, cores lines 420–575; cycle 1→3→2→1, lines 576–615):

- 1→3 ordinary (core {5}); 3→2 p-core {4,8}: R_2={4}, D_2={0}; 2→1 p-core {2,3,8}: R_1={2,3}, D_1={1}.
- v_1(T_2) = v_1({0,4,8}) = 16385+16+2304 = 18705 < u_1(O) = 32782, so 1 prefers **no** subset of T_2; no edge 1→2 exists (target-2 core list has champion 3 only). Likewise v_2(T_3) = v_2({5,8}) = 6432 < 30737: no edge 2→3. Both transitive contractions are refuted on original goods.

Lemma 2 instantiated (word ppo, one run): Z = (0:{6,7}, 1:{1,5}, 2:{0,2,3}, 3:{4,8}; charity ∅), complete. Utilities 10432 (=), 38946 (>32782), 36877 (>30737), 22800 (>20512): Pareto-improving, lex-improving for 0,1,2,3. Lemma 1 checks: v_2({2,3}) = 26636 > v_2({4}) = 20496. Full EFX scan (12 comparisons, hand-computed): every comparison holds except exactly one —

  **v_1(Z_2 ∖ {3}) = v_1({0,2}) = 16385+24580 = 40965 > v_1(Z_1) = 38946.**

This is (W) with x = 1 (a cycle member), t = 2 ((p,p) vertex), junction bundle D_2 ∪ R_1 = {0,2,3}. The variant leaving D_1={1} in charity fails by the same inequality (40965 > 34848); giving p to anyone other than 3 leaves 3 unpaid (v_3({4}) = 18448 < 20512). Consistent with the exact audit's `all_partial_efx.maximizer_count = 1` (`selector_compatibility_4x9_exact_audit_20261016.json` line 709) and `globally_improving_out_of_class_efx_assignment: null` (line 2145). Note the wall is created by combining 2's residual {0} with 1's own released {2}: separately v_1(R_1)=28684 and v_1(O_2∖g) ≤ 16385 are safe — this is exactly why common-safety of the parts does not transfer to the junction.

## Limitations

- Lemma 2 yields a necessary wall (W), not an exit; nothing here claims an improving exit or ADMIT4, and the calibration shows (W) can hold at a true global maximum.
- popo remains conditional (§4); longer cycles not treated.
- Calibration arithmetic is hand-derived from the JSON integer tables, not executed; the A1 §8 scripts are absent from this workspace. Suggested verification: an exact-integer EFX scan of Z above and of the three variants, plus a check that Lemma 1's inequality and the single failing comparison (observer 1, bundle {0,2,3}, deleted good 3) reproduce.


## Opposite-model QA of that proposal

Verdict: **revise**

The candidate contains a useful and essentially correct one-ordinary-run contraction, but two claims exceed what is proved, and the `popo` boundary is not frozen precisely enough.

## Concrete findings

1. **Lemma 2’s main one-run construction is sound.**

For cycle edges \(i_t\to i_{t+1}\), the four bundle formulas conserve original physical goods. With exactly one ordinary run there is exactly one \((o,p)\) vertex, so \(p\) has a unique recipient. Participant improvements follow from:

- ordinary desire for \((o,o)\);
- champion desire for \((o,p)\);
- Lemma 1 for \((p,p)\);
- ordinary desire plus the positive retained residual for \((p,o)\).

Thus every participant strictly improves, nonparticipants remain at their original utility, and any EFX endpoint would contradict the all-partial-EFX maximality of \(O\). This preserves original utilities and the fixed priority; it does not reset floors.

The reduction of possible failures to junction bundles is also valid for this construction: original bundles and minimal cores are \(O\)-common-safe, while unions \(D_t\cup R_{t+1}\) and \(D_t\cup O_{i_{t+1}}\) need not be.

2. **The extension to the pure-\(p\) variants that give \(p\) to a participant is false as written.**

The candidate says all \(L+1\) variants “must fail (W),” but (W) only covers targets

\[
D_t\cup R_{t+1}\quad\text{or}\quad D_t\cup O_{i_{t+1}}.
\]

If \(p\) is assigned to participant \(i_s\), that target is instead

\[
D_s\cup R_{s+1}\cup\{p\}.
\]

Minimal-core safety does not control this three-part union. Failure may occur only because \(p\) was added, so it need not yield the displayed (W). The correct statement is:

- the pure rotation with \(p\) left in charity has only the stated junction walls;
- a variant assigning \(p\) has an enlarged wall family
  \[
  v_x\!\left((D_s\cup R_{s+1}\cup\{p\})\setminus\{g\}\right)>v_x(Z_x).
  \]

This matters because the requested criterion requires every claimed exit or exact unpaid inequality to be identified.

3. **The `popo` section is not a precise conditional lemma.**

It does not specify a complete allocation formula, which \((o,p)\) vertex receives \(p\), the disposition of every residual, or the exact EFX inequalities meant by “max tails.” The priority condition “some strictly improving participant precedes \(u\)” is also insufficient unless all earlier changed agents are fixed or improving and no earlier agent loses utility.

This section should either be removed from the lemma or restated as a fully quantified conditional proposition. As written, it is analysis, not a proved length-four contraction.

4. **The calibration obstruction is exact and checks out.**

From the supplied values:

\[
v_1(\{0,4,8\})=16385+16+2304=18705<32782,
\]

so positivity rules out every subset of \(T_2\) as an envied core for agent 1. Likewise,

\[
v_2(\{5,8\})=32+6400=6432<30737.
\]

Thus the claimed direct augmented edges do not exist.

For

\[
Z=(\{6,7\},\{1,5\},\{0,2,3\},\{4,8\}),
\]

the utilities are exactly

\[
(10432,38946,36877,22800),
\]

and the only observer-target tail violation is

\[
v_1(\{0,2,3\}\setminus\{3\})
=v_1(\{0,2\})=40965>38946=v_1(Z_1).
\]

So the example correctly demonstrates that separately safe pieces can create an unsafe junction. The underlying global maximality and core data are recorded in [the exact selector audit](/Users/maxf/.local/state/cross-model/efx-audit-20260927-9080c6f5d94b/20261016-143119-d0493cd6/qa-71f7e1f6ea/results/selector_compatibility_4x9_exact_audit_20261016.json) and [the champion-core audit](/Users/maxf/.local/state/cross-model/efx-audit-20260927-9080c6f5d94b/20261016-143119-d0493cd6/qa-71f7e1f6ea/results/physical_admission_champion_cores_20261016.json).

5. **The boundary is otherwise responsibly stated.**

The candidate does not assume GG, BASE, twelve roles, or no-complete-EFX, and it does not claim ADMIT4 or general EFX. Its main result is a necessary-wall lemma rather than an unconditional exit, which is consistent with the calibration.

## Required revision

Retain Lemmas 1–2, but:

- restrict (W) to the pure rotation with \(p\) unallocated and the one-run construction;
- add the enlarged \(p\)-junction wall for variants assigning \(p\);
- replace the informal `popo` discussion with a precise conditional allocation-and-EFX lemma, or explicitly state that `popo` remains untreated.

With those changes, the candidate would be a valid useful partial result rather than a complete treatment of all length-\(2,3,4\) cycle words.
