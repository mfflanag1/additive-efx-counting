# EFX Additive-Goods Campaign Plan

Target: **EFX existence for n ≥ 4 agents, additive valuations over indivisible goods** — the
last open tower after monotone/submodular goods fell (arXiv:2604.18216, SAT; arXiv:2605.06451,
symmetric constructions) and additive chores fell (arXiv:2606.08872, tri-valued costs).

Method: the DGG playbook — exact-verifier-first, no-go lemma extraction between sessions,
simple prompts inside a disciplined harness. Success = witness OR a shrinking, theorem-bounded
live region (both are publishable; the DGG campaign proved the negative track has value).

## State of the board (as of 2026-08-01)

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

New internal frontier:
- additive \((4,8)\) is internally certified safe;
- Borda-additive \((4,9)\) has a dual-encoded \(3+2+2+2\) theorem candidate;
- the same shape is solver-closed for nine distinct integer scores through
  cap 11;
- at cap 12 the balanced shape fails, but the sharpness profile has 838
  complete EFX allocations, all isolating the common favorite as a
  singleton;
- adding the 48 singleton repairs dual-encoding closes complete EFX for the
  entire rank-distinct cap-12 domain; and
- cap 13 is dual-encoding closed in all five favorite orbits under the
  broader “balanced or designated-favorite singleton” family; and
- at cap 14 the balanced-only ladder fails in the favorite-\(2+1+1\)
  orbit, but all 298 complete-EFX repairs of the frozen obstruction isolate
  one of the three designated favorite goods, so the broader structural
  alternative survives this new stress test; the enlarged 624-partition
  matching master closes that orbit, while its Hall replay times out and
  the full cap-14 theorem remains open; and
- unrestricted-real profiles show that the balanced and
  favorite-singleton branches are independently necessary, and that the
  finite cap-13 repair pool does not generalize verbatim;
- an extreme \(6+1+1+1\) singleton repair now has an exact
  residual-threshold Hall lemma, but a cap-13 profile refutes using only
  that extreme shape alongside balanced allocations; and
- the highest-leverage human gate is the scalar threshold alternative: if
  the best favorite-singleton owner slack over all three-agent EFX
  remainders is negative, prove that a balanced EFX allocation exists.
  The favorite-singleton Hall lemma now writes each residual candidate as
  one scalar threshold plus one resident perfect matching, so failure has a
  threshold certificate or a three-by-three Hall witness. The balanced-only
  boundary fails the scalar threshold on every residual partition, giving a
  clean first subcase before the mixed threshold/Hall obstruction. A
  canonical \(3+3+2\) partition reduces that subcase to the row-wise
  disjunction \(x_3+x_7>f\) or \(x_4+x_5>f\), and Hall reduces those 16
  branches to either four distinct half-favorite representatives or one
  common contested set of exactly three. The latter has an explicit
  four-pair partial EFX normal form with one unenvied low floater. A new
  lexicographic exchange lemma parks that floater and proves complete EFX
  throughout the common-three branch. Exact optimization and shape
  reductions show that the displayed disjunction together with
  \(x_5+x_6+x_7>f\) exactly characterizes universal threshold failure. The
  same condition has a sorting-free form: every residual four-set has a
  triple above \(f\), and the residual pair-sum graph has either three
  vertices of degree at least six or four of degree at least four. The
  four-distinct-representatives branch was the remaining EFX gate in this
  universal-threshold subcase and is now closed by the proof-checked theorem
  linked below. A cap-free three-set construction had already
  analytically supplies a balanced owner-floor state; the old dual
  840-partition encodings independently corroborate it. The remaining task
  is a triple-host alternating exchange that upgrades the floor state to
  EFX. A fixed-host exchange, ordinary Nash and favorite-surplus product
  selections, and even EFX restricted to the analytic construction family
  are false. The favorite-pair matching-rank route is now also exactly
  refuted: a strict branch-valid profile has no rank-four state among all
  840 favorite-pair partitions, although literal enumeration finds 324
  complete EFX allocations, all with the favorite in the common-low triple
  \(\{f,1,2\}\). A cap-free lemma proves that this alternate triple is EFX
  whenever the remaining six goods admit three pairs worth at least
  \(F_i+\max\{v_i(1),v_i(2)\}\) to every observer. The next proof target is
  the exact dichotomy “favorite-pair EFX or favorite-triple Hall
  matching,” not a bounded swap or rank-plateau lemma. For a fixed
  favorite triple, the triple column is universally feasible and the three
  pair columns only need a matching to three agents at threshold
  \(F_i+\max\{v_i(a),v_i(b)\}\). Thus the former common-low lemma is a
  complete-bipartite special case, while two universally safe pairs plus a
  third with at most one rejecter already suffice without an exchange. The
  remaining unit is an edge-labeled perfect-matching selection lemma. A
  diversified 24/9 exact master remains unknown after 300 seconds, while a
  20,000-step exact-census search found a positive knife edge with zero
  favorite-pair EFX states, exactly one common-low repair, and 252 complete
  EFX allocations. This makes “force even one repair” the sharp sufficient
  proof-mining target, with the agent-relative Hall alternative as the exact
  fallback. All hard no-favorite-pair profiles also contain a full
  15-pairing favorite-triple cell. A strict boundary refutes the stronger
  demand for three agents who accept every residual edge. The sharpest
  surviving sufficient lemma uses two universal acceptors and requires the
  outsider-rejection graph to have no perfect matching. Direct negation of
  that two-core target has a 40-cut matching CEGAR boundary, a 24-cut Hall
  boundary, a 55-cut complement-frontier timeout, a reified 183-cut
  boundary, a full cap-20 CP-SAT timeout, and a 900-second bounded CEGAR
  stall at 331 cuts; no model with zero favorite-pair repairs and no
  two-core witness has been found. A strict boundary rules
  out shrinking the search to the six
  representative-low/complementary-agent cells: its unique witness uses
  nonrepresentative lows 5 and 6. The unrestricted 168-cell target remains
  live. On six residual goods,
  Tutte reduces the required bad-graph
  condition to three exact cases: two odd components, a one-vertex deletion
  leaving three odd components, or a two-vertex edge cover. The exact
  statements are
  in
  [`results/DISTINCT_HALF_CONVERSION_DICHOTOMY_GATE.md`](results/DISTINCT_HALF_CONVERSION_DICHOTOMY_GATE.md)
  and
  [`results/UNIVERSAL_THRESHOLD_BALANCED_GATE.md`](results/UNIVERSAL_THRESHOLD_BALANCED_GATE.md).

A cap-20 CP-SAT continuation has now reduced favorite-pair repairs to 20.
Its final profile has no two-core witness but retains a full 15-pairing
favorite-triple Hall cell. The next solver/proof target is therefore the
intermediate full-cell dichotomy before returning to the stronger two-core
selection claim.
Its first exact-real master produced one no-full-cell profile with 289
favorite-pair repairs. The next 183-cut solve hit its configured 180-second
limit; the two-solve run took 337.7 seconds, so the conditional target
remains open.
A separate cap-20 CP-SAT CEGAR trace retained 357 favorite-pair repairs;
its 412-cut continuation remained `UNKNOWN` after 600 seconds. This is a
bounded boundary, not a theorem or selection counterexample.

The same full-cell dichotomy is now independently closed on the finite
integer domain \(\{1,\ldots,5\}\). CP-SAT proves a learned 416-partition
pool infeasible; assumption extraction leaves 330 partitions, and an
independent sorting-based QF_LIA encoding returns `unsat` on that core.
The QF_LIA assumption core has since shrunk from 330 to 204 and then 193
partitions. An independent threshold CNF then shrinks to a
deletion-minimal 17-partition core; its 702,820-clause formula is `UNSAT`
in CaDiCaL, and `drat-trim` independently verifies its binary DRAT proof.
This is a bounded theorem, not a real-valued closure. The 17 literal
templates are cap-specific: a cap-6 profile obstructs all of them while
retaining 138 favorite-pair repairs. Their useful invariant is instead
that they occupy six of the ten representative/free-good partition orbits.
The resulting 624-partition orbit-selection candidate is now refuted by an
exact cap-20 profile. It has no full favorite-triple Hall cell and 45
favorite-pair repairs, all in two omitted orbits, plus 900 labeled complete
EFX allocations. Adding both repair orbits gives a natural conservative
eight-orbit successor of 780 partitions—equivalently, all favorite-pair
states whose triple is not all representatives; only two terminal orbit
types remain outside it. A correctly scoped cap-20 CP-SAT test of all 780 returned
`UNKNOWN` after 473.93 seconds without a model. Exact-real Z3 tests of the
whole family and the all-B/all-C rank cells also returned `unknown`; an
independent cardinal CEGAR reached a 173-cut exact-real boundary after one
new 300-repair trace model and a 300-second continuation. Pinned cvc5
independently timed out on both rank
cells. A diversified seed union now obstructs 708 of the 780 states, but its
600-second exact-real master still returned `unknown`. Subsequent guarded
optimization and exact-census annealing reduced the best positive boundary
from 45 to three repairs, while every exact optimizer bound still permits
zero. Two independent three-repair profiles have exactly 15 EFX-supporting
unlabeled partitions: 12 pairings in one almost-full Hall cell and the three
converted favorite-pair states. See
[`results/DISTINCT_HALF_FULL_CELL_CAP5_THEOREM.md`](results/DISTINCT_HALF_FULL_CELL_CAP5_THEOREM.md)
and
[`results/DISTINCT_HALF_FULL_CELL_ORBIT_GATE.md`](results/DISTINCT_HALF_FULL_CELL_ORBIT_GATE.md).

Hall-witness mining now gives an exhaustive successor split. In the 21
cap-6 deletion boundaries, 572 of 588 low-pair cells—and all 126 cells whose
low pair consists of representatives—already fail through one residual edge
rejected by every agent. Any cap-free no-full-cell/no-eight-orbit profile
either has such a singleton witness for all six representative pairs, or
has a representative pair with no singleton witness; the latter can be
fixed as pair 1,2 after dropping favorite-value agent ordering. Direct
exact-real tests of both exhaustive branches returned `unknown` after 300
seconds. Exact profiles also refute the stronger local claim that a terminal
EFX partition can always be repaired by one representative/low-good swap.
See
[`results/DISTINCT_HALF_RR_HALL_SPLIT_GATE.md`](results/DISTINCT_HALF_RR_HALL_SPLIT_GATE.md).
The RR-singleton side now has a smaller first subgate: 17 of the 21 cap-6
boundaries use one unrepresented edge as the witness for all six RR cells,
equivalent to four second-order-statistic inequalities. The other four
boundaries need witness-edge covers of size two or three. The dedicated
exact-real common-UU gate returned `unknown` after 300 seconds with a
708-partition pool. Naming the four second-smallest representatives reduces
its 256 labeled order patterns to 19 conjugacy orbits, 18 of which already
occur in the bounded data. The complementary no-common-UU formula also
returned `unknown` after 300 seconds with a 708-partition pool. This finite
orbit split, rather than a longer monolithic timeout, is the next
solver-assisted target; the dispersed singleton and RR-nonsingleton cases
remain separate inside the complementary branch.

The three-repair boundary exposes a cap-free zero-neighbor conversion lemma.
If one failed Hall pairing has a universally rejected edge, a common
orientation of the two low goods, and the two remaining pairs satisfy three
explicit value floors, moving the lower low good onto the rejected edge
makes every bundle feasible for every agent. The open step is no longer the
conversion: conditional on no favorite-pair EFX state, select such a motif
or a full Hall cell. See
[`results/ZERO_NEIGHBOR_FAVORITE_TRIPLE_CONVERSION_LEMMA.md`](results/ZERO_NEIGHBOR_FAVORITE_TRIPLE_CONVERSION_LEMMA.md).

The bottom-pair version of that selection step is now a cap-free,
proof-checked computer-assisted theorem. It is enough that a residual pair
be jointly bottom-two for any three agents, not all four. Each failed Hall
pairing maps injectively to one of six favorite-pair EFX conversions, so
`favorite-pair repairs + valid pairings in that cell >= 15`; zero repairs
forces a full cell. Cardinal and sorting Z3 encodings, independent cvc5,
five Hall-role cells, and a 233,949-step CPC proof accepted by Ethos certify
the strengthening. The exact surviving branch has no pair shared as
bottom-two by three agents. Selecting one bottom pair per agent leaves the
patterns `2+2`, `2+1+1`, and `1+1+1+1`. The exhaustive multigraph census
has 20 patterns. The disjoint `2+2` pattern is now closed by a proof-checked
180-conversion theorem with a 19-partition certified core. The overlapping
`2+2` pattern is also closed by a proof-checked 165-conversion theorem using
a 960-element canonicalization. Its replicated three-repair equality
profiles all lie in one size-60 conversion orbit. The triangle-with-doubled-
edge `2+1+1` pattern is now also closed by a proof-checked 225-conversion
theorem. The doubled-edge three-leaf star is closed by a proof-checked
228-conversion theorem and a 96-action symmetry audit. Both repeated-edge
four-vertex paths are closed by proof-checked 240-conversion theorems. The
remaining wedge/detached-edge, detached-fork, and three-disconnected-edge
patterns are also proof-checked. All seven `2+1+1` patterns are therefore
closed. All eleven all-distinct geometries are now proof-checked. Their full
formulas pass cardinal Z3, fresh-process Z3, sorting-network Z3, pinned
cvc5, and CPC/Ethos. The eleven checked proofs total 383,418,002 bytes and
4,603,008 steps; the perfect-matching theorem further compresses to a
proof-checked canonical six-conversion core. Together with the three-agent-
bottom theorem and the nine repeated-edge patterns, this closes the entire
strict-common-favorite/universal-owner-threshold-failure branch at $(4,9)$.
The next common-favorite gate is threshold-passing but resident-Hall-
deficient.
See
[`results/THREE_AGENT_BOTTOM_PAIRING_CONVERSION_THEOREM.md`](results/THREE_AGENT_BOTTOM_PAIRING_CONVERSION_THEOREM.md)
and
[`results/BOTTOM_PAIR_MULTIPLICITY_GATE.md`](results/BOTTOM_PAIR_MULTIPLICITY_GATE.md),
with the closed pattern in
[`results/DISJOINT_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md`](results/DISJOINT_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md)
and
[`results/OVERLAP_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md`](results/OVERLAP_DOUBLE_BOTTOM_PAIR_CONVERSION_THEOREM.md).
The first closed lower-multiplicity pattern is documented in
[`results/TRIANGLE_REPEATED_BOTTOM_PAIR_CONVERSION_THEOREM.md`](results/TRIANGLE_REPEATED_BOTTOM_PAIR_CONVERSION_THEOREM.md).
The second is
[`results/STAR_REPEATED_BOTTOM_PAIR_CONVERSION_THEOREM.md`](results/STAR_REPEATED_BOTTOM_PAIR_CONVERSION_THEOREM.md).
The two path cases are
[`results/PATH_REPEATED_BOTTOM_PAIR_CONVERSION_THEOREMS.md`](results/PATH_REPEATED_BOTTOM_PAIR_CONVERSION_THEOREMS.md).
The first all-distinct theorem is
[`results/FOUR_DISCONNECTED_BOTTOM_PAIRS_CONVERSION_THEOREM.md`](results/FOUR_DISCONNECTED_BOTTOM_PAIRS_CONVERSION_THEOREM.md).
The second is
[`results/FOUR_CYCLE_BOTTOM_PAIRS_CONVERSION_THEOREM.md`](results/FOUR_CYCLE_BOTTOM_PAIRS_CONVERSION_THEOREM.md).
The class theorem is
[`results/REPEATED_BOTTOM_PAIR_EXCLUSION_THEOREM.md`](results/REPEATED_BOTTOM_PAIR_EXCLUSION_THEOREM.md).
The completed universal-threshold theorem is
[`results/COMMON_FAVORITE_UNIVERSAL_THRESHOLD_EFX_THEOREM.md`](results/COMMON_FAVORITE_UNIVERSAL_THRESHOLD_EFX_THEOREM.md).

The exact remaining common-favorite branch is now the mixed threshold/Hall
gate. Two exact cap-20 profiles have 114 and 273 threshold-passing
owner--partition pairs but no Hall-valid favorite-singleton partition; all
complete EFX support is balanced. A third profile blocks the six one-good
favorite-pair repairs of a fixed passing \(3+3+2\) partition, so the next
lemma must select a rank-maximal passing pair and permit an owner-changing
alternating exchange. Begin with the rank-two/zero-neighbor Hall case and a
radius-two exchange family. See
[`results/MIXED_THRESHOLD_HALL_GATE.md`](results/MIXED_THRESHOLD_HALL_GATE.md),
[`results/efx49_common_favorite_mixed_hall_boundaries_audit.json`](results/efx49_common_favorite_mixed_hall_boundaries_audit.json),
and
[`results/efx49_common_favorite_mixed_hall_local6_boundary_audit.json`](results/efx49_common_favorite_mixed_hall_local6_boundary_audit.json).
The first radius-two decision gate blocks 63 balanced neighbors. Direct
cap-6 and cap-20 masters remain `UNKNOWN`; a cap-6 CEGAR rebuild learned 488
singleton obstructions across six models before another `UNKNOWN`. See
[`results/efx49_common_favorite_mixed_hall_radius2_gate_audit.json`](results/efx49_common_favorite_mixed_hall_radius2_gate_audit.json).
Before the exchange step, isolate the rank-selection lemma. All three exact
mixed profiles attain resident rank two and admit a rank-two pass with a
zero-neighbor bundle. Bounded cap-20 CEGAR learned 49 zero-neighbor motifs
before timeout and 66 rank-two motifs across two iterations, without proof
or counterexample. See
[`results/efx49_common_favorite_mixed_selection_gate_audit.json`](results/efx49_common_favorite_mixed_selection_gate_audit.json).
The rank-one branch is reduced analytically to a common-column bundle and
one strict density inequality per resident. Owner switching either reaches
rank two or leaves a three-resident density wall/all-four-common-column
case. The common-triple conversion-or-singleton dichotomy is now refuted
even under the no-singleton hypothesis: all six one-good transfers can fail,
while the nearest EFX repair is distance two. The exact next target is the
radius-two implication, compressed from 63 states and nine origin signatures
to the 21-state family where the favorite receives a contested-triple good.
That family remains open after a 302-cut CEGAR boundary. See
[`results/RANK_ONE_COMMON_COLUMN_NORMAL_FORM.md`](results/RANK_ONE_COMMON_COLUMN_NORMAL_FORM.md).

The two terminal partition orbits now have a sharper local proof-mining
boundary. One-swap exchange is false, but every cap-5 terminal EFX state in
the structural branch has an eight-orbit EFX repair within two swaps, even
without excluding full Hall cells. The
claim is nonvacuous and dual-verified across all seven canonical
terminal/matching cells by CP-SAT and Z3 QF_LIA. It does not extend the
finite existence ladder. A 91-target unrestricted-real core test first
returned `unknown`, but a later cap-20 optimization refuted the full
implication.
See
[`results/DISTINCT_HALF_TERMINAL_EXCHANGE_GATE.md`](results/DISTINCT_HALF_TERMINAL_EXCHANGE_GATE.md).
For the first canonical R-cell, neither natural half of the 138 states is
sufficient. More decisively, a cap-20 profile with no full Hall cell blocks
their entire union while retaining 336 favorite-pair EFX partitions and
1,439 complete EFX allocations elsewhere. Radius two is retired. The next
human step returns to the global 780-state eight-orbit-or-full-Hall
dichotomy; the refuting profile's nearest eight-orbit repair is at distance
three.
See
[`results/TERMINAL_RADIUS_TWO_EXCHANGE_CANDIDATE.md`](results/TERMINAL_RADIUS_TWO_EXCHANGE_CANDIDATE.md).

The certified ladder now extends through \(\{1,\ldots,6\}\). At cap 6,
CP-SAT closes a 401-partition pool, QF_LIA independently closes its
359-partition core and shrinks it to 175, and threshold CNF reduces to a
separately verified deletion-minimal 21-partition core. The final
1,145,090-clause formula has a binary DRAT proof accepted by `drat-trim`.
This extension closes the earlier cap-6 escape to the cap-5 literal core;
it remains finite-domain only. See
[`results/DISTINCT_HALF_FULL_CELL_CAP6_THEOREM.md`](results/DISTINCT_HALF_FULL_CELL_CAP6_THEOREM.md).

The matching computational gate now uses the full sufficient cap
\(K_9=19{,}683\). Its scope and reduction chain are frozen in
[`results/COMMON_FAVORITE_SUFFICIENT_CAP_GATE.md`](results/COMMON_FAVORITE_SUFFICIENT_CAP_GATE.md).

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
- R3: The magnitude question is now closed for every fixed cell: the
  small-integer witness lemma gives
  \(K_m=\lfloor m^{m/2}\rfloor\). An UNSAT exhaustion through that cap fully
  resolves \((n,m)\). The remaining risk is computational—the cap is finite
  but still far too large for literal matrix enumeration.

## Layout
efx/
  PLAN.md  LEDGER.md  filters.py  verify.py  verify2.py  cegar.py
  tracks/{lifting,model,boundary}/   results/   transcripts/
