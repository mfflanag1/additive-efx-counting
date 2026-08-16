# Session Review: Additive EFX and Parkable Deletion at \((4,8)\)

> **Superseded:** the certification status below is historical. See the
> [current session review](SESSION_REVIEW_CURRENT_20260729.md) for the
> completed eight-cell CPC/Ethos certificates, final Lean theorem, axiom
> audit, and current remaining work.

**Review date:** 2026-07-29  
**Scope:** the ten-hour parkability/EFX attack, its relationship to the
existing additive-EFX research program, and the present claim boundary  
**Review type:** internal technical synthesis, not external peer review

## Executive assessment

The session produced an **exhaustive exact-linear-arithmetic closure
candidate** for a frontier fair-division problem:

> Every strictly positive additive \(4\times8\) instance appears to admit a
> complete EFX\(_0\) allocation and, equivalently, a parkable-deletion
> allocation.

The word *candidate* is essential. The analytic reduction to eight cases is
proved in the research notes, and Z3 returned `unsat` on every exact terminal
formula. Seven formulas replayed `unsat` in fresh processes; one cell was
also rebuilt using a substantially different direct-allocation encoding.
A 200-partition obstruction core and native Z3 proof terms were extracted.
However, the arithmetic proof has not been checked by an independent proof
checker, the analytic reductions have not been formalized in a proof
assistant, and no external specialist has reviewed the work.

The present result is therefore:

- **well beyond an exploratory computation;**
- **strong enough to organize a serious paper or thesis chapter;**
- **plausibly a breakthrough if independently certified and externally
  validated;**
- **not yet a theorem or a resolution of the open four-agent additive-EFX
  problem.**

The session used 10 hours 42 minutes of goal time. The frozen evidence archive
contains 27 hash-bound files occupying approximately 522 MB.

## The problem in basic language

There are four people and eight indivisible goods. Each person assigns a
positive value to each good. We want to divide all eight goods among the four
people.

An allocation is **EFX**—envy-free up to any good—when the following strong
fairness test passes:

> If person \(i\) looks at person \(j\)'s bundle, then removing *any one*
> good from \(j\)'s bundle is enough to eliminate \(i\)'s envy.

The session originally attacked a related “parkability” formulation:

1. remove one good;
2. divide the other seven goods in an EFX way;
3. “park” the removed good back with some person without destroying EFX.

At first this could have been a stronger requirement than merely finding an
EFX allocation of all eight goods. The first major theoretical discovery was
that it is not stronger.

### The rotation idea

For person \(i\) and bundle \(S\), define its EFX threshold

\[
\tau_i(S)=v_i(S)-\min_{g\in S}v_i(g).
\]

This is the value left after removing the least valuable good from \(S\), as
seen by person \(i\).

If a person owns a bundle whose threshold is at least every other bundle's
threshold, one of that person's goods can be removed safely. If nobody has
this property, point each person toward a bundle with a strictly larger
threshold. These arrows contain a directed cycle. Rotating the bundles around
that cycle preserves EFX and strictly increases a finite potential. Repeating
the operation must eventually stop at an allocation with a removable good.

Thus:

\[
\text{complete EFX exists}
\quad\Longleftrightarrow\quad
\text{parkable deletion exists}.
\]

This is the **Threshold-Cycle Normal Form Theorem**. It changed the
computational target from more than half a million
deletion/base/host combinations to the 40,824 relevant onto allocations.

### Why only eight cases remained

A second simple but powerful observation concerns favorite goods. If the four
people can be matched to four distinct favorite goods, assign each person a
favorite and pair it with one of the four remaining goods. Each person then
owns at least the value of their favorite, while the EFX threshold of every
other two-good bundle is no larger than that favorite. This immediately gives
an EFX allocation.

Therefore any generic counterexample would need repeated favorite goods. Up
to relabeling, the favorite multiplicities are

\[
4,\quad 3+1,\quad 2+2,\quad 2+1+1.
\]

The last three give three terminal cases. When all four people share one
favorite, their second favorites have five possible multiplicity patterns.
This gives five more terminal cases, for a total of eight.

### How each case was tested

There are exactly 1,701 ways to partition eight labeled goods into four
nonempty unlabeled bundles. For each partition, construct a bipartite graph:

- left side: the four people;
- right side: the four bundles;
- edge \(iB\): person \(i\) could own bundle \(B\) while satisfying every EFX
  comparison against the other three bundles.

That partition supports an EFX allocation exactly when this graph has a
perfect matching. A counterexample would therefore have to block a perfect
matching for **all 1,701 partitions simultaneously**.

Each of the eight formulas asks whether such a positive additive valuation
matrix exists inside one canonical favorite-pattern cell. All eight exact
QF_LRA formulas returned `unsat`.

In plain language: after the structural reductions, the solver found that
every remaining possible kind of counterexample is internally inconsistent.

## What was done during the session

### 1. Audited and recovered the old bounded campaign

The previous \(K=4\) bounded campaign was recovered and its pool hashes were
checked. A seemingly difficult SAT model was diagnosed rather than mistaken
for a counterexample: it had 294 complete EFX allocations and 576 parkable
triples, all driven by universal-minimum goods.

This exposed a major search inefficiency and motivated an exact structural
case cut.

### 2. Proved safe residual reductions

The exact-real searches excluded only analytically justified cases:

- a universal-minimum good can be deleted and parked at a source after using
  the known \(m\le n+3\) EFX theorem;
- a peelable good can be given as a singleton while the other three agents
  receive an EFX allocation;
- counterexample nonexistence is open, allowing a generic perturbation with
  strict within-row rankings and distinct normalized rows;
- a favorite-good matching directly constructs an EFX \(2222\) allocation.

These are case reductions, not heuristic assumptions.

### 3. Proved the Reverse Parking Lemma

For a complete EFX allocation, the session derived an exact owner-slack
criterion identifying which owned goods can be removed while preserving EFX.
This gives a bijection between parkable triples and owner-removable pairs.

The stronger threshold-cycle theorem then showed that parkability is a normal
form for complete EFX existence, rather than a separate stronger conjecture.

### 4. Built multiple exact computational formulations

The session implemented:

- deletion/base/host QF_LRA CEGAR;
- direct complete-allocation QF_LRA CEGAR;
- fixed-partition perfect-matching obstruction formulas;
- an alternative Hall-selector partition encoding;
- a direct-allocation terminal-cell encoding;
- assumption-core extraction and frozen standalone replay tooling;
- optimized exact counting and local-search diagnostics.

All valuation variables are exact rationals after row normalization; strict
inequalities remain strict QF_LRA inequalities rather than floating-point
approximations.

### 5. Found and explained local “coverage walls”

Searches reached matrices with only four complete EFX allocations but did not
cross into a zero-EFX chamber. The Complementary Wall Certificate explains
one obstruction exactly: as one family of four EFX allocations disappears,
a dual family becomes feasible across the same equality wall.

A second wall showed that coverage can move between completely different
bundle shapes. This invalidated several tempting but false local proof
strategies and helped motivate the global finite-cell approach.

### 6. Closed the eight canonical cells

All eight formulas included all 1,701 partitions:

| terminal cell | creating-process result | solve time |
|---|---|---:|
| \(2+1+1\) favorite multiplicities | UNSAT | 742.878 s |
| \(3+1\) favorite multiplicities | UNSAT | 4,090.177 s |
| \(2+2\) favorite multiplicities | UNSAT | 2,179.563 s |
| four common favorites, all seconds distinct | UNSAT | 59.097 s |
| four common favorites, all seconds equal | UNSAT | 5,989.274 s |
| common favorite, \(3+1\) seconds | UNSAT | 959.765 s |
| common favorite, \(2+2\) seconds | UNSAT | 555.783 s |
| common favorite, \(2+1+1\) seconds | UNSAT | 73.282 s |

Seven frozen formulas returned `unsat` in fresh standalone Z3 processes. The
longest cell's second replay was intentionally interrupted after 24 minutes
when the goal window ended; its original exact solve is retained.

### 7. Added cross-checks and proof artifacts

- The all-distinct-second cell was independently rebuilt by negating all
  40,824 labeled onto allocations, rather than using partition graphs. It
  also returned UNSAT.
- Two activation-literal reductions compressed one representative terminal
  formula from 1,701 obstructions to a sufficient 200-partition UNSAT core.
- The 200-partition formula replayed UNSAT in a fresh process.
- A 96 MB native Z3 proof term was generated for the full representative
  cell.
- A proof-producing replay with Z3's internal proof checker enabled also
  returned UNSAT.
- All evidence files were frozen behind a SHA-256 manifest.

## Current research outputs

### New mathematical outputs from this session

1. **Reverse Parking Lemma.** Exact necessary-and-sufficient owner-slack
   criterion and a bijection between parkable triples and removable pairs.
2. **Threshold-Cycle Normal Form Theorem.** Constructive equivalence between
   complete EFX existence and parkable deletion; stated for normalized
   monotone goods valuations.
3. **Favorite-Good Matching Lemma.** At \(m=2n\), a matching saturating the
   agents in the weak-favorite graph yields an EFX allocation of pairs.
4. **Generic eight-cell reduction.** Any positive additive \(4\times8\)
   counterexample can be moved into one of eight strict favorite/ranking
   cells.
5. **Fixed-partition matching formulation.** EFX assignments supported on a
   fixed bundle partition are exactly perfect matchings in an
   agent–bundle feasibility graph.
6. **Complementary EFX wall mechanism.** An exact local explanation for why
   attempted EFX-count elimination can hand feasibility to a dual allocation
   family.

### New computational outputs from this session

1. Eight frozen exact-QF_LRA terminal formulas and result records.
2. Seven fresh-process terminal-cell replays.
3. One independent direct-allocation cross-encoding.
4. A twice-reduced 200-partition UNSAT core.
5. Native Z3 proof terms for a full cell and its first reduced core.
6. A 522 MB, 27-file, SHA-256-bound evidence archive.
7. New exact-LRA, partition, direct-allocation, core-extraction, replay,
   optimized-counting, and local-search code.
8. Expanded differential and regression coverage across all central
   constructions.

### Existing broader-program outputs

The current paper, which predates this session's eight-cell result, contains:

- exact count-\(n\) additive EFX witnesses at
  \((4,7),(5,8),(6,9),(4,8),(4,9),(4,10)\);
- a generalized parking criterion and exact certificates;
- a certified bounded result that every positive integer \(4\times7\)
  instance over values \(\{1,2,3,4\}\) has at least four labeled EFX
  allocations;
- an independent CNF encoding and checked DRAT proof for that bounded result.

The new \((4,8)\) closure is **not yet incorporated into the paper PDF** and
should remain a separate candidate result until its stronger certification
is complete.

## How deeply the work has been reviewed

| layer | review performed | assessment |
|---|---|---|
| Mathematical ideas | Proofs written for reverse parking, threshold cycles, favorite matching, safe cuts, generic coverage, and partition matching | Deep internal review; high confidence, but not externally refereed or proof-assistant checked |
| Definition-level implementation | Literal evaluators compared with optimized enumeration and exact threshold identities | Strong |
| Small exhaustive controls | 23 small matrices, 252 triples, 241 threshold-normal-form cases, and 258 favorite-pair constructions | Strong |
| Partition encoding | All 1,701 partitions enumerated; 384 fixed-matrix comparisons between matching-clause and Hall encodings | Strong |
| Terminal domain coverage | Exact eight-cell metadata and formula hashes audited | Strong internally |
| Solver repetition | All eight creating-process UNSAT results; seven fresh-process replays | Good, but one replay remains incomplete |
| Encoding independence | One terminal cell rebuilt using all 40,824 direct allocations | Valuable but partial |
| Proof evidence | Native Z3 proof terms and Z3 internal proof checking | Meaningful, but still inside the Z3 trust boundary |
| Independent proof checking | None for the eight-cell result | Principal unresolved gap |
| Clean build | `make verify-parkability` passes the differential, terminal-CNF, and durable-campaign suites | Strong |
| External review | None | Unreviewed |
| Novelty review | Targeted current arXiv search only | Preliminary, not a novelty determination |

The final verification suite reported:

- 1,701 unlabeled partition checks;
- 384 partition-encoding comparisons;
- 241 threshold-normal-form controls;
- 258 favorite-pair constructions;
- 9,066 terminal threshold identities;
- terminal-CNF guard, cut, pool, and isolated-solver checks;
- durable \(K=4\) campaign-supervisor verification.

### Confidence by claim

| claim | present confidence |
|---|---|
| Reverse Parking Lemma | High internal confidence |
| Threshold-Cycle Normal Form Theorem | High internal confidence; originality unchecked |
| Favorite-Good Matching Lemma | High internal confidence |
| Eight cells exhaust the generic positive domain | Moderately high to high, subject to specialist review of every safe reduction and stabilizer |
| Each archived formula is UNSAT | Strong solver evidence |
| The formulas faithfully encode the complete mathematical claim | Strong but not yet independently established end-to-end |
| Positive additive EFX always exists at \((4,8)\) | Serious closure candidate; theorem status withheld |

## Research-level assessment

### Thesis-chapter level

**Yes, comfortably.** The session contains multiple new lemmas, a structural
normal-form theorem, a finite canonical reduction, exact encodings, negative
results about failed proof routes, and a substantial reproducibility archive.
Even if the final closure did not survive external checking, the methods and
diagnostics would support a serious technical chapter.

### PhD-thesis level

**The broader research program is on a PhD-thesis trajectory; this session
alone is not a complete thesis.** Combined with the existing count-\(n\)
paper, generalized parking results, bounded DRAT-certified lower bound, and
the new \((4,8)\) work, there is enough technical depth for several connected
chapters. A thesis would still need a unified narrative, polished proofs,
literature synthesis, independent certification, and a clear statement of
which claims are unconditional.

### Professor/frontier-research level

**Yes in problem choice and technical ambition.** The work directly attacks
an open parameter cell adjacent to the known boundary, combines structural
fair-division arguments with computer-assisted proof methods, and produces
evidence that would merit attention from specialists. “Professor level”
describes the research maturity and frontier positioning, not the current
validation status.

### Breakthrough level

**Potentially, but conditionally.** A verified proof that every positive
additive \(4\times8\) instance has an EFX allocation would settle the first
additive parameter cell beyond the general \(m\le n+3\) existence theorem.
Recent literature still describes four-agent additive EFX existence as open.
That makes a correct, independently certified \((4,8)\) result potentially
breakthrough-quality.

It should not presently be described as a breakthrough because:

1. Z3 remains the common solver trust boundary.
2. Only one of eight cells has a separately structured direct encoding.
3. The native proof is not independently checked.
4. The analytic reduction is not formalized.
5. No external expert has audited the argument.
6. The literature search is preliminary.

## Current external research position

Ashuri, Gkatzelis, and Sgouritsa's
[*EF2X Exists for Four Agents*](https://arxiv.org/abs/2412.00254)
states that EFX existence for four agents remains open even for additive
valuations.

Akrami, Mayorov, Mehlhorn, Srinivas, and Weidenbach's
[*A Counterexample to EFX: \(n\ge3\) Agents, \(m\ge n+5\) Items,
Submodular Valuations via SAT-Solving*](https://arxiv.org/abs/2604.18216)
gives monotone/submodular counterexamples starting at \(m=n+5\), while also
proving the positive three-agent, seven-good case by SAT solving. Its
counterexamples do not cover the additive \((4,8)=(n,n+4)\) cell studied
here. Its Lean-verified encoding and independently checked proof pipeline
provide an appropriate certification benchmark.

A targeted arXiv search performed during the session did not find a published
additive \((4,8)\) theorem. This is evidence of relevance, not a formal
novelty search.

## Already planned next steps

### Priority 1: independent certification

1. Finish a clean standalone replay of the all-four-equal-second cell.
2. Rebuild all eight formulas from a clean checkout and compare bytes and
   hashes with the archive.
3. Run at least one genuinely independent SMT/LRA solver on every cell.
4. Obtain a proof in an independently checkable format, or translate the
   Boolean/LRA proof into explicit resolution plus Farkas certificates.
5. Check the resulting proof with a separate, pinned checker.

This is the critical path. More heuristic search is no longer the bottleneck.

### Priority 2: independent encoding and formalization

1. Extend the direct-allocation cross-encoding from one cell to all eight.
2. Write an independent formula generator that shares no terminal encoding
   code with `lra_master.py`.
3. Formalize the Reverse Parking Lemma, Threshold-Cycle Normal Form Theorem,
   favorite-matching lemma, perturbation reduction, and symmetry coverage in
   Lean or another proof assistant.
4. Verify that every emitted terminal-cell assumption follows from the
   formal reduction.

### Priority 3: shrink and explain the computational proof

1. Continue deletion-based shrinking of the 200-partition core.
2. Analyze which shapes and threshold cycles are indispensable.
3. Search for a small human-readable structural contradiction suggested by
   the core.
4. Determine whether the eight solver cells can be replaced by a shorter
   analytic argument.

### Priority 4: manuscript and external review

1. Keep the result separate from the existing paper until certification.
2. Prepare a focused \((4,8)\) manuscript containing the analytic reduction,
   exact formula specification, archive, and claim boundary.
3. Ask specialists in EFX and computer-assisted proof for adversarial review.
4. Perform a systematic literature and novelty search.
5. Promote “closure candidate” to “computer-assisted theorem” only after the
   complete certification chain passes.

### Priority 5: broader research program

After certification, investigate:

- whether the favorite-matching and threshold-cycle reductions generalize to
  other \(m=2n\) cells;
- whether the 200-partition core reveals a general additive existence
  principle;
- whether related canonical-cell decompositions can attack \((4,9)\),
  allocation-count lower bounds, or valuation classes beyond additivity.

## Main local results and artifacts

### Session result

- [Solver-Backed EFX Certificate at \((4,8)\)](EFX_4X8_LRA_CERTIFICATE.md)
- [Reverse Parking Lemma and Threshold-Cycle Normal Form](REVERSE_PARKING_LEMMA.md)
- [Complete Parkable Deletion Goal Log](PARKABILITY_GOAL_20260729.md)
- [Complementary EFX Wall Certificate](COMPLEMENTARY_WALL_CERTIFICATE.md)
- [Parkability implementation and reproduction guide](../tracks/parkability/README.md)
- [Terminal certification design](../tracks/parkability/TERMINAL_CERTIFICATION.md)

### Frozen evidence

- [Favorite-cell evidence archive](../../experimental-runs/additive-efx-counting-runs/parkability/goal-20260729-favorite-cells/README.md)
- [Archive SHA-256 manifest](../../experimental-runs/additive-efx-counting-runs/parkability/goal-20260729-favorite-cells/MANIFEST.sha256)
- [Individual replay observations](../../experimental-runs/additive-efx-counting-runs/parkability/goal-20260729-favorite-cells/individual-replay-observations.json)
- [200-partition core result](../../experimental-runs/additive-efx-counting-runs/parkability/goal-20260729-favorite-cells/partition-favorite-211-core2-result.json)
- [200-partition core formula](../../experimental-runs/additive-efx-counting-runs/parkability/goal-20260729-favorite-cells/partition-favorite-211-core2.smt2)

### Existing research paper

- [Current additive-EFX counting paper](../paper/main.pdf)
- [LaTeX source](../paper/main.tex)
- [Repository research-program overview](../README.md)

## Bottom line

The session did not merely find another promising numerical pattern. It
converted the \((4,8)\) parkability question into the original EFX-existence
question, proved several useful structural reductions, reduced the continuous
positive-additive domain to eight canonical cells, and closed all eight with
exact solver formulas.

The work is already strong PhD-chapter/frontier-research material. Its
potential significance is higher: after independent certification and expert
review, it could become a genuine breakthrough result for additive EFX.
Until those gates are passed, the scientifically correct label is:

> **exhaustive exact-LRA solver-backed closure candidate, with substantial
> internal cross-checking and an unresolved independent-proof boundary.**
