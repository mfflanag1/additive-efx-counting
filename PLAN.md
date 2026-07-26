# EFX Additive-Goods Campaign Plan

Target: **EFX existence for n ≥ 4 agents, additive valuations over indivisible goods** — the
last open tower after monotone/submodular goods fell (arXiv:2604.18216, SAT; arXiv:2605.06451,
symmetric constructions) and additive chores fell (arXiv:2606.08872, tri-valued costs).

Method: the DGG playbook — exact-verifier-first, no-go lemma extraction between sessions,
simple prompts inside a disciplined harness. Success = witness OR a shrinking, theorem-bounded
live region (both are publishable; the DGG campaign proved the negative track has value).

## State of the board (as of 2026-07-23)

Proven-safe classes for additive goods (each is an instance FILTER and a REPAIR MECHANISM a
candidate must defeat):
- n ≤ 3 (Chaudhury–Garg–Mehlhorn; simplified Akrami et al.)
- m ≤ n + 3 (Mahara — **ledger task: confirm exact statement/citation**)
- ≤ 3 distinct additive valuation types (EC'25); ≤ 2 types (Mahara '23)
- Bivalued additive; identical valuations (leximin)
- Almost-full: 4 agents, EFX on all but 1 good (Berger et al.); sublinear charity via rainbow
  cycle number (Chaudhury et al.)
- EF2X exists for 4 agents, cancelable valuations (2024/25)
- 3 agents, 7 goods, ALL monotone valuations: EFX exists (UNSAT, Lean-verified encoding,
  2604.18216)

Minimal live cell: **n = 4, m ≥ 8, ≥ 4 distinct valuation types, not bivalued**.
Structural filter from almost-full theorem: in any counterexample, for EVERY partial EFX
allocation of m−1 goods, the leftover good is unplaceable. Strong — use as candidate filter
and as no-go-lemma raw material (analogue of DGG "free entry").

Known counterexample templates to mine:
- Submodular n=3 m=8 (2605.06451): agents identical up to good-relabeling; symmetry is the
  engine. Note tension: ≤3 valuation types is SAFE for additive — so relabeling-symmetric
  additive constructions are dead unless relabeling changes the type. Formalize this.
- Chores tri-valued (2606.08872): 3 chore types, 2 agent types, tight. Study why the
  goods/chores duality breaks (2-type goods is proven safe).

## Phases

### Phase 0 — Ledger (no-go map)  → verify: LEDGER.md + filters.py with tests
Pin down exact statements + citations for every safe class above. Implement each as a
machine-checkable filter (candidate instance → which theorems kill it). Resolve the two
open ledger questions: exact Mahara m-bound; any known rationality/value-magnitude bound
for a minimal counterexample (probably none — see Risk R3).

### Phase 1 — Verifier first  → verify: cross-check on known instances
`verify.py`: exact integer arithmetic, exhaustive over n^m allocations (4^8 = 65,536 —
trivial), returns ALL EFX allocations, not just existence (Track C needs counts).
`verify2.py`: independent implementation, different algorithm (ILP feasibility per
allocation-pattern), written in a separate session without reading verify.py.
Adversarial test set: submodular 2605.06451 instances (must report NO EFX), chores
counterexample translated, random safe-class instances (must report EFX), the DGG campaign's
five false-positive patterns as cautionary tests of the harness itself.
DISCIPLINE: no candidate is "found" until both verifiers agree; no claim until minimized.

### Phase 2 — Frontier map (CEGAR core)  → verify: UNSAT certificates or witness
The problem is ∃V ∀A ¬EFX(V,A): V a 4×m integer matrix, A over a finite set. CEGAR loop:
1. CP-SAT/MILP: find V (values 0..K, normalized) violating EFX on current allocation set S.
2. Exact verifier: enumerate all allocations under V; if none EFX → WITNESS (goto claim
   discipline). Else add a surviving EFX allocation to S; repeat. UNSAT at step 1 →
   theorem: "no counterexample at (n=4, m, K)".
Symmetry breaking: agent order (lex rows), good order (lex columns), gcd normalization.
Schedule: m=8, K=2,3,4,…; then m=9 (262k allocations). Every UNSAT is a bounded no-go —
log in results/, they compose into the negative-result paper.
Encoding notes: additive ⇒ only 4m integer vars (vs 25k bool vars in the monotone SAT
encoding), but arithmetic disjunctions — CP-SAT first, SMT(LIA) as cross-check on any
UNSAT we intend to cite.

### Phase 3 — Structured hunts (three parallel tracks)
- **Track A (lifting):** additivize the submodular and chores witnesses. Locate the exact
  step where additivity breaks each; formalize as no-go lemma or as a residual construction
  family. First concrete lemma target: "goods-side ≤3-type safety kills all
  relabeling-symmetric additive constructions" — proof or counterexample family.
- **Track B (model-driven):** frontier-model sessions seeded with LEDGER.md + both 2026
  constructions + failed-candidate digest. Ask for parametric families (Juang-style), not
  single instances. Simple prompts, immediate exact verification, transcript kept. Failed
  families get an autopsy line in the ledger.
- **Track C (boundary landscape):** search for instances minimizing #EFX allocations
  (CP-SAT objective / local search from safe instances). Instances with exactly 1 EFX
  allocation are the cliff edge — perturb across it. Telemetry: which known-proof invariant
  (champion argument, most-envious potential, almost-full completion) is the LAST to hold;
  that invariant is the true obstruction and the next lemma target.

### Phase 4 — No-go extraction (between every session)
Every dead class → attempted lemma. Every lemma → shrinks the live region in LEDGER.md.
Endgame criterion (DGG pattern): reduce "EFX fails for 4 additive agents" to ONE named
open lemma, or produce the witness.

## Claim discipline (unchanged from DGG)
witness → verifier #2 → minimize (m, K, sparsity, distinct values) → hand-checkable
writeup with plug-in arithmetic → Lean-verifiable encoding statement (follow 2604.18216
precedent) → only then external claim.

## Risks
- R1: EFX(additive, n=4) may be TRUE. Mitigation: the K-bounded UNSAT ladder + Phase 4
  lemmas ARE the product on that branch ("no small counterexample" + obstruction map).
- R2: Crowded field — the SAT group behind 2604.18216 is certainly attacking additive now.
  Differentiators: CEGAR-over-values (their method was set-function SAT, doesn't transfer
  directly), the lifting track, and no-go-lemma discipline. Speed matters.
- R3: No a priori bound on witness value magnitudes — K-ladder gives bounded no-gos only.
  Ledger task: derive a rationality bound (witness V, if any, can be taken at a vertex of
  the CEGAR constraint polyhedron ⇒ magnitude bound from the constraint matrix?). If it
  goes through, UNSAT at that K = full resolution for (n,m). High-value theory subtask.

## Layout
efx/
  PLAN.md  LEDGER.md  filters.py  verify.py  verify2.py  cegar.py
  tracks/{lifting,model,boundary}/   results/   transcripts/
