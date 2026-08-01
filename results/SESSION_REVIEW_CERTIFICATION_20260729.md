# Session Review and Certification Snapshot: Additive EFX at \((4,8)\)

> **Superseded:** See the
> [current session review](SESSION_REVIEW_CURRENT_20260729.md), which includes
> the completed stabilizer, partition-coverage, semantic-binding, and
> published-input-lifting work.

**Snapshot:** 2026-07-29 22:37 EDT / 2026-07-30 02:37 UTC  
**Scope:** the additive-EFX research program, the ten-hour parkability attack,
and the independent-certification work performed immediately afterward  
**Review status:** self-audit and technical synthesis; not external peer review  
**Claim status:** solver-backed closure candidate, not yet a theorem

## Executive verdict

The session produced a serious candidate resolution of the first open
near-diagonal additive-EFX case:

> Every four-agent, eight-good instance with positive additive valuations
> appears to admit a complete EFX allocation.

The mathematical reduction and all eight original exact-arithmetic solver
cases are complete. The result has also passed several unusually strong
reproducibility and encoding checks. In particular:

- all eight archived formulas rebuild byte-for-byte from the original
  generator;
- a separately written SMT-LIB generator independently reconstructs the
  mathematical encoding;
- its partition obstructions agree with a definition-literal evaluator on
  all \(3{,}402\) tested partition/matrix pairs;
- its eight cell preambles agree with the original encoder on all \(592\)
  tested cell/matrix pairs;
- seven of the eight independently generated full cells now have cvc5 CPC
  proofs accepted as `correct` by the separate Ethos proof checker; and
- Lean now checks the Reverse Parking machinery, the finite-cycle argument,
  the full Threshold-Cycle Normal Form Theorem, positivity/onto,
  favorite matching, normalization, generic perturbation, relabeling, and
  exact eight-cell exhaustiveness, the matching semantics of every partition
  obstruction, and the extension arguments behind the two residual cuts.

This moves the result beyond “one solver said UNSAT.” The remaining gap is
nevertheless decisive: one full cell still lacks a separate proof-checker
certificate; the published existence theorems used by the residual cuts have
not been instantiated in Lean, the stabilizer orbits and formula-translation
boundary are not yet fully formalized; and
no EFX or computer-assisted-proof specialist has reviewed it.

The right current label is:

> **Advanced PhD/frontier-level computer-assisted mathematics with
> breakthrough potential, but not yet a certified breakthrough or a theorem.**

## The problem, in basic language

There are four people and eight indivisible goods. Each person gives every
good a positive numerical value, and the value of a bundle is the sum of its
goods.

An allocation is **EFX**—envy-free up to any good—if this demanding fairness
test always passes:

> Whenever person \(i\) compares their bundle with person \(j\)'s bundle,
> removing any one good from \(j\)'s bundle eliminates \(i\)'s envy.

The open question is whether such an allocation must exist for every
four-person additive instance. Existing theorems handle at most three
additive agents and, separately, at most \(n+3\) goods. Four agents and eight
goods is therefore the first cell just beyond both general boundaries.

The session initially used a “park one good” formulation:

1. remove one of the eight goods;
2. fairly allocate the remaining seven;
3. put the removed good back somewhere without breaking EFX.

The first major insight was that this is not merely a hopeful construction.
Every complete EFX allocation can be transformed, by rotating bundles around
carefully chosen cycles, into one from which a good can safely be removed and
parked back. Thus complete EFX existence and parkable deletion are equivalent.

The second major insight was that a generic counterexample need only be
searched in eight canonical favorite-good patterns. Each pattern can be
expressed as an exact system of rational linear inequalities. For every one
of those eight systems, the solver found that the hypothesized counterexample
conditions are mutually inconsistent.

## The approach and its inspiration

The work followed the useful pattern illustrated by the recent Jacobian
counterexample and by OpenAI's Cycle Double Cover research prompt:

1. **Demand the exact target.** A bounded experiment, a stronger-looking
   reduction, or a candidate near-counterexample does not count as resolving
   the original problem.
2. **Maintain different representations.** The work moved among direct
   allocations, deletion/parking triples, threshold cycles, bundle
   partitions, bipartite matchings, and exact linear arithmetic.
3. **Extract a small structural mechanism.** Threshold rotation and favorite
   matching reduced a large continuous problem to eight finite symbolic
   cells.
4. **Turn discovery into a certificate.** The eight cells were frozen,
   hash-bound, rebuilt, independently regenerated, and are being converted to
   separately checked proof objects.
5. **Report the exact surviving gap.** The present evidence is strong enough
   to justify certification work, but not strong enough to erase the
   remaining trust boundary.

The Jacobian counterexample had a short explicit end certificate: check a
constant Jacobian and two distinct preimages. This EFX result is a universal
nonexistence claim about counterexamples, so its final certificate is
necessarily more involved. The analogous goal is still the same: distill a
large search into exact artifacts that independent tools and humans can
check.

## Work completed in the session

### 1. Structural mathematics

The following mathematical outputs were developed:

1. **Reverse Parking Lemma.** A necessary-and-sufficient owner-slack
   criterion identifies exactly when a good can be removed from an EFX
   owner's bundle while preserving EFX.
2. **Threshold-Cycle Normal Form Theorem.** If a complete EFX allocation
   exists, repeated rotations along strict threshold-improvement cycles
   terminate at an EFX allocation with an owner-removable good. This proves
   the equivalence between EFX existence and parkable deletion.
3. **Favorite-Good Matching Lemma.** At \(m=2n\), if the agents can be matched
   to distinct favorite goods, assigning each matched favorite with one
   leftover good gives EFX.
4. **Generic eight-cell reduction.** Any positive additive \(4\times8\)
   counterexample can be perturbed into one of three repeated-favorite cells,
   or one common-favorite cell split into five second-favorite patterns.
5. **Fixed-partition matching formulation.** For a fixed partition of the
   eight goods into four bundles, EFX assignments are exactly the perfect
   matchings of an agent-bundle feasibility graph.
6. **Complementary-wall mechanism.** Exact local analysis explains why
   eliminating one family of low-count EFX allocations can make a dual family
   appear across the same boundary.

### 2. Exact closure computation

There are \(S(8,4)=1{,}701\) unlabeled partitions of eight goods into four
nonempty bundles and \(40{,}824\) labeled onto allocations. Each terminal
formula asserts that all \(1{,}701\) partitions fail to support an EFX
matching.

All eight original exact QF_LRA formulas returned `unsat`:

| Canonical cell | Original Z3 result | Original solve time |
|---|---:|---:|
| \(2+1+1\) favorites | UNSAT | 742.878 s |
| \(3+1\) favorites | UNSAT | 4,090.177 s |
| \(2+2\) favorites | UNSAT | 2,179.563 s |
| Common favorite; all seconds distinct | UNSAT | 59.097 s |
| Common favorite; all seconds equal | UNSAT | 5,989.274 s |
| Common favorite; \(3+1\) seconds | UNSAT | 959.765 s |
| Common favorite; \(2+2\) seconds | UNSAT | 555.783 s |
| Common favorite; \(2+1+1\) seconds | UNSAT | 73.282 s |

All eight archived cells also replayed in fresh Z3 processes. The final
all-equal-second replay returned `unsat` in 4,414.370 seconds.

### 3. Core extraction and alternative encoding

One representative formula was reduced from all \(1{,}701\) partition
obstructions to a sufficient 200-partition UNSAT core:

| Bundle shape | Core partitions |
|---|---:|
| \(2222\) | 51 |
| \(3221\) | 98 |
| \(3311\) | 20 |
| \(4211\) | 30 |
| \(5111\) | 1 |

The core replayed UNSAT in Z3 and, after strict SMT-LIB normalization, in the
independent cvc5 1.3.3 solver.

The all-distinct-second cell was also encoded a different way: directly
negating all \(40{,}824\) labeled onto allocations instead of using partition
graphs. It too returned UNSAT. This is a valuable cross-check against an
error specific to the perfect-matching formulation.

### 4. Frozen reproducibility archive

The discovery archive is approximately 522 MB. Its SHA-256 manifest binds 27
evidence files, and the complete manifest recheck passes.

All eight original formulas were then regenerated in separate fresh Python
processes. Every rebuilt file is byte-identical to its archived counterpart.
This rules out accidental loss, manual alteration, and nondeterministic
formula drift under the recorded Python 3.10.14/Z3 5.0.0 environment.

### 5. Independent encoding

A new generator was written without importing Z3 or the project's original
partition/encoding modules. It independently:

- enumerates the \(1{,}701\) restricted-growth partitions;
- emits positivity, normalization, residual-case, ranking, and stabilizer
  constraints;
- defines the 16 agent-bundle feasibility edges for each partition; and
- excludes all 24 perfect matchings.

The independent generator emitted all eight full formulas, each about 12 MB.
Its audits currently show:

- exact equality of the two independently enumerated partition sets;
- \(3{,}402/3{,}402\) partition-obstruction comparisons correct on two fixed
  valuation matrices; and
- \(592/592\) original-versus-independent cell-preamble comparisons equal on
  74 matrices, including witnesses, random controls, and tie controls.

These are differential tests, not a proof that every line of the generator is
correct. They materially reduce the likelihood of a shared encoding error.

### 6. Independent solver and proof checker

Pinned official binaries are archived for cvc5 1.3.3 and Ethos 0.2.3, along
with their SHA-256 hashes and the cvc5 CPC signatures.

Seven independently generated full cells have completed the full chain:

| Cell | cvc5 result | CPC proof | Ethos result |
|---|---:|---:|---:|
| All seconds distinct | UNSAT in 161.384 s | 21.2 MB / 249,283 steps | `correct` |
| \(2+1+1\) seconds | UNSAT in 119.871 s | 18.1 MB / 208,913 steps | `correct` |
| \(2+2\) seconds | UNSAT in 517.848 s | 78.9 MB / 872,213 steps | `correct` |
| \(3+1\) seconds | UNSAT in 716.892 s | 115.3 MB / 1,186,530 steps | `correct` |
| \(2+1+1\) favorites | UNSAT in 1,203.807 s | 187.3 MB / 1,890,346 steps | `correct` |
| \(2+2\) favorites | UNSAT in 2,289.236 s | 338.4 MB / 2,702,364 steps | `correct` |
| \(3+1\) favorites | UNSAT in 2,080.253 s | 459.9 MB / 3,327,798 steps | `correct` |

One cell has not yet completed this proof-producing pass.

This is the strongest current computational evidence. It separates:

- the original Z3 generator and solver;
- the independently written formula generator;
- cvc5 as a second solver and proof producer; and
- Ethos as a distinct proof checker.

Ethos is itself an ordinary software checker, not a formally verified kernel,
so the ultimate trust base still includes its implementation and the formula
semantics.

### 7. Lean formalization

A pinned Lean 4.32.1/mathlib project has built successfully from more than
1,500 dependencies and proof units. The newly added restricted-growth
enumeration now elaborates but its naive exhaustive `native_decide` check did
not finish within six minutes and was stopped pending optimization, so the
full entry point has not yet been reverified after that last addition. The
allocation model explicitly requires that every good has exactly one owner,
avoiding a common semantic gap in formalizations that state only the EFX
inequalities.

Lean currently checks:

- exact additive values, thresholds, EFX, good removal, and valid complete
  allocations;
- monotonicity under erasure, threshold attainment, the threshold
  characterization of EFX, and both directions connecting a removable owned
  good to threshold maximality;
- the finite functional-graph fact that a fixed-point-free self-map contains
  a nontrivial permutation cycle;
- preservation of nonempty bundles and valid allocation under bundle
  permutation;
- preservation of EFX under maximal-threshold moves and strict increase of a
  finite threshold potential;
- the full **Threshold-Cycle Normal Form Theorem**: any valid EFX allocation
  with nonempty bundles can be transformed into a valid EFX allocation with
  an owner-removable good; and
- the full **favorite-matching construction** at \(m=2n\): distinct favorite
  goods plus arbitrary paired leftovers form a valid complete EFX allocation;
- positivity plus \(4<8\) forces every bundle of a complete EFX allocation
  to be nonempty;
- EFX existence is invariant under agent relabeling, good relabeling, and
  positive row scaling, and positive rows can be normalized to sum to one;
- the no-EFX set is open, so a hypothetical positive counterexample can be
  perturbed to have strict within-row rankings while remaining a
  counterexample;
- explicit favorite and second-favorite selectors yield strict ranking
  prefixes after that perturbation; and
- all fifteen equality kernels of four favorite labels, plus the five
  common-favorite second-label kernels, reduce under simultaneous
  agent/good relabeling to exactly the eight solver cells;
- a stronger zero-row-sum perturbation preserves row normalization while
  making every row internally tie-free and all four valuation rows distinct;
- Boolean feasibility edges have exactly the EFX meaning used in the SMT
  formulas, and the 24 perfect-matching clauses exactly characterize EFX
  assignments of a fixed four-bundle partition;
- every EFX allocation can be improved to a plain-envy-source normal form;
- adding a universally least-valued deleted good to an unenvied source
  preserves EFX; and
- assigning a peelable good as a singleton and extending a three-agent
  seven-good EFX allocation preserves EFX.

Thus Lean now checks the main structural bridge from complete EFX to
parkability and the generic reduction from any positive counterexample to a
normalized member of the eight-cell disjunction. It also checks the elementary
extension machinery behind the terminal formulas' residual cuts. The remaining
formal work is to instantiate the published \(4\times7\) and three-agent
existence theorems on the relevant subinstances, prove the optional stabilizers
orbit-complete, finish the kernel check of the 1,701 restricted-growth
partitions, and connect the Lean cell specifications to the emitted SMT-LIB
formulas.

The final repository verification run also passed the complete
`verify-parkability` suite under Python 3.10, including the 1,701-partition
enumeration, 384 original partition-encoding comparisons, 9,066 threshold
identities, terminal-CNF checks, isolated-solver checks, and the durable
\(K=4\) campaign supervisor.

## Current status by claim

| Claim | Present evidence | Status |
|---|---|---|
| Reverse-owner criterion | Written proof, tests, Lean proof in both threshold directions | Formally checked under stated hypotheses |
| Threshold-cycle normal form | Constructive proof plus Lean finite-cycle/potential proof | Formally checked for valid EFX allocations with nonempty bundles |
| Favorite-good matching | Short proof, controls, and Lean valid-allocation theorem | Formally checked |
| Eight cells cover every generic positive counterexample | Lean-checked normalization, stronger generic perturbation, selectors, kernel coverage, and relabeling | Formally checked before residual cuts and stabilizers |
| Partition obstruction has the intended EFX meaning | Lean equivalence between feasibility edges, EFX bundle assignments, and the 24 perfect matchings | Formally checked |
| Residual cuts are safe extension mechanisms | Lean proofs for universal-minimum insertion and peelable-singleton extension | Formally checked conditional on the two published smaller-instance EFX theorems |
| All original terminal formulas are UNSAT | 8/8 original exact Z3 solves | Complete solver evidence |
| Fresh standalone solver replay | 8/8 independent Z3 processes, including the 4,414.370-second hardest replay | Complete |
| Archived formulas are reproducible | 8/8 byte-identical fresh-process rebuilds | Complete |
| Independent formulas encode the intended cells | Independent source plus 3,994 differential comparisons | Strong but not deductively complete |
| Independent solver agrees | Seven full cells and one 200-partition core UNSAT in cvc5 | Partial |
| Independent proof checker accepts full-cell proofs | 7/8 Ethos-checked CPC proofs | Partial and active |
| End-to-end \(4\times8\) theorem | Requires all cells plus certified analytic coverage | **Not yet established** |

## How deeply the work has been reviewed

### Review ladder

| Layer | Depth reached | Remaining weakness |
|---|---|---|
| Mathematical discovery | Deep: several structural lemmas and an exhaustive reduction | Only internal authorship/review |
| Definition-level testing | Deep: literal, optimized, direct-allocation, and matching views | Tests sample semantics; they do not replace proof |
| Original computation | Complete across all eight exact cells | Originally shared one generator/solver stack |
| Artifact integrity | Complete manifest check and byte-identical rebuild | Rebuild uses the same original source |
| Encoding independence | Substantial: separately written standard SMT-LIB generator | Full semantic equivalence not formalized |
| Solver independence | Partial: cvc5 confirms representative core and seven full cells | One full cell remains |
| Proof independence | Partial: seven CPC proofs accepted by Ethos | One full cell remains; Ethos is not formally verified |
| Formal mathematics | Deep: reverse parking through normalized eight-cell reduction, matching semantics, and residual extension lemmas check in Lean | Published-theorem instantiation, stabilizers, restricted-growth coverage, and formula binding remain |
| External mathematical review | None | Principal social/disciplinary validation gap |
| Novelty review | Targeted current literature search | Not a systematic novelty determination |

### Overall review judgment

The work has been **deeply internally audited** and is now **partly
independently machine-checked**. It is substantially more credible than a
typical exploratory solver result. It has not yet reached the standard needed
to announce a resolution of a recognized open problem because the
independent certificate and final formal bridge are incomplete and no
external specialist has reviewed them.

## Research-level assessment

| Level | Assessment | Reason |
|---|---|---|
| Thesis chapter | **Yes, clearly** | New lemmas, structural reduction, exact encodings, negative route map, and reproducibility archive already form a substantial chapter |
| PhD thesis | **The broader program is on this trajectory** | The existing counting paper plus this work can support multiple chapters, but a thesis still needs a unified narrative, polished proofs, literature synthesis, and external evaluation |
| Professor/frontier research | **Yes in problem choice and technical maturity** | It attacks a genuine frontier cell with a sophisticated structural/computational proof strategy |
| Breakthrough | **Potential, not current status** | A fully certified \(4\times8\) theorem would be a notable advance beyond the \(m\le n+3\) boundary; the present chain is not yet complete |

The most honest single rating is:

> **Advanced PhD-level output executed at a frontier/professional research
> level, with conditional breakthrough significance.**

## Existing broader-program outputs

The current paper predates the new eight-cell closure and should be evaluated
separately. It contains:

- six positive additive instances with exactly \(n\) labeled EFX allocations,
  at \((4,7),(5,8),(6,9),(4,8),(4,9),(4,10)\);
- a necessary-and-sufficient generalized one-good parking theorem with exact
  certificates; and
- a finite theorem that every positive integer \(4\times7\) instance with
  values in \(\{1,2,3,4\}\) has at least four labeled EFX allocations,
  supported by an independently generated CNF and checked DRAT proof.

Those are already defensible focused-paper/thesis-chapter contributions. They
do not themselves prove unrestricted additive-EFX existence. The new
\((4,8)\) closure candidate is deliberately not yet incorporated into the
paper.

## Already planned next steps

### Completed since the first session review

1. Revalidated the frozen archive manifest.
2. Rebuilt all eight original formulas byte-for-byte.
3. Wrote an independent formula generator.
4. Audited all \(1{,}701\) independent partition obstructions on two fixed
   matrices.
5. Compared all eight cell preambles across 74 matrices.
6. Installed and hash-pinned cvc5, Ethos, Lean, and mathlib.
7. Proved that the cvc5-to-Ethos CPC pipeline works on a smoke example.
8. Completed seven independently checked full-cell proofs.
9. Formalized the Reverse Parking machinery, finite-cycle construction,
   Threshold-Cycle Normal Form Theorem, and favorite-matching valid EFX
   allocation in Lean.
10. Formalized positivity/onto, normalization, openness of the no-EFX set,
    strict perturbation, relabeling, favorite/second canonicalization, and
    the exact eight-cell reduction in Lean.
11. Completed the fresh standalone Z3 replay of the all-equal-second cell
    (`unsat` in 4,414.370 seconds).
12. Formalized the solver's partition-feasibility graph and its 24
    perfect-matching clauses in Lean.
13. Formalized plain-envy-source normalization and the exact EFX-preserving
    extension arguments for universal-minimum and peelable residual cuts.
14. Strengthened the perturbation theorem so normalized row sums are
    preserved and both coordinates within each row and the four rows
    themselves become pairwise distinct.

### Active at this snapshot

1. cvc5 proof production and Ethos checking for the independent
   all-equal-second cell.
2. Optimization and rerun of the Lean computation for the 1,701
   restricted-growth canonical partitions and their coverage of all onto
   owner maps.
3. Lean formalization of stabilizer orbit-completeness.
4. Formal semantic binding between the Lean cell specifications and emitted
   SMT-LIB.

### Critical path

1. Produce and Ethos-check CPC proofs for all eight independent full-cell
   formulas.
2. Bind the independent formulas, proofs, checker binaries, signatures, and
   result records into a new immutable manifest.
3. Instantiate or explicitly trust-bound the two published EFX existence
   inputs used by the residual cuts: four agents/seven goods and three
   agents/seven goods.
4. Finish the remaining analytic coverage in Lean: restricted-growth
   enumeration and stabilizer orbit-completeness.
5. Connect the formal cell specifications to the generated SMT formulas, or
   provide a small independently reviewable translation checker.
6. Extend the direct-allocation cross-encoding beyond one cell.
7. Shrink the 200-partition core further and mine it for a human-readable
   contradiction.
8. Prepare a focused manuscript and invite adversarial review from both EFX
   and computer-assisted-proof specialists.
9. Perform a systematic novelty search before any public priority or
   breakthrough claim.

Broader \((4,9)\), \(m=2n\), and allocation-count questions should wait until
this certification chain is complete.

## Main local results and artifacts

### New \((4,8)\) result

- [Solver-backed \(4\times8\) EFX certificate](EFX_4X8_LRA_CERTIFICATE.md)
- [Reverse Parking Lemma and Threshold-Cycle Normal Form](REVERSE_PARKING_LEMMA.md)
- [Complete parkability goal log](PARKABILITY_GOAL_20260729.md)
- [First session review](SESSION_REVIEW_20260729.md)
- [Complementary wall certificate](COMPLEMENTARY_WALL_CERTIFICATE.md)
- [Parkability implementation and reproduction guide](../tracks/parkability/README.md)
- [Terminal certification design](../tracks/parkability/TERMINAL_CERTIFICATION.md)

### Frozen and independent evidence

- [Original frozen evidence archive](../../experimental-runs/additive-efx-counting-runs/parkability/goal-20260729-favorite-cells/README.md)
- [Original SHA-256 manifest](../../experimental-runs/additive-efx-counting-runs/parkability/goal-20260729-favorite-cells/MANIFEST.sha256)
- [Independent-generator partition audit](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/independent-generator-audit/audit.json)
- [Independent cell-preamble audit](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/independent-generator-audit/cell-preambles.json)
- [Eight-formula byte-rebuild audit](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/rebuilt-formulas-isolated-v2/rebuild-audit.json)
- [All-distinct-second CPC/Ethos certificate](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/proofs/top4-second1111.independent.certificate.json)
- [\(2+1+1\)-seconds CPC/Ethos certificate](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/proofs/top4-second211.independent.certificate.json)
- [\(2+2\)-seconds CPC/Ethos certificate](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/proofs/top4-second22.independent.certificate.json)
- [\(3+1\)-seconds CPC/Ethos certificate](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/proofs/top4-second31.independent.certificate.json)
- [\(2+1+1\)-favorites CPC/Ethos certificate](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/proofs/favorite-211.independent.certificate.json)
- [\(2+2\)-favorites CPC/Ethos certificate](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/proofs/favorite-22.independent.certificate.json)
- [\(3+1\)-favorites CPC/Ethos certificate](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/proofs/favorite-31.independent.certificate.json)
- [Independent cvc5 result for the 200-partition core](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/independent-solver/partition-favorite-211-core2.cvc5.json)
- [Lean formalization entry point](../formal/efx48/EFX48.lean)
- [Lean owner-removal proof](../formal/efx48/EFX48/ReverseParking.lean)
- [Lean finite-cycle proof](../formal/efx48/EFX48/FiniteCycle.lean)
- [Lean Threshold-Cycle Normal Form](../formal/efx48/EFX48/ThresholdCycle.lean)
- [Lean favorite-matching theorem](../formal/efx48/EFX48/FavoriteMatching.lean)
- [Lean positive/onto reduction](../formal/efx48/EFX48/PositiveOnto.lean)
- [Lean normalization](../formal/efx48/EFX48/Normalization.lean)
- [Lean openness and perturbation topology](../formal/efx48/EFX48/Perturbation.lean)
- [Lean strict perturbation and normalized eight-cell theorem](../formal/efx48/EFX48/StrictPerturbation.lean)
- [Lean exact eight-cell ranking reduction](../formal/efx48/EFX48/RankingCells.lean)
- [Lean partition-to-perfect-matching semantics](../formal/efx48/EFX48/PartitionMatching.lean)
- [Lean plain-envy-source normal form](../formal/efx48/EFX48/EnvySource.lean)
- [Lean residual-cut specifications](../formal/efx48/EFX48/ResidualCuts.lean)
- [Lean universal-minimum extension](../formal/efx48/EFX48/UniversalMinimum.lean)
- [Lean peelable-singleton extension](../formal/efx48/EFX48/Peelable.lean)
- [Lean restricted-growth enumeration under active verification](../formal/efx48/EFX48/RestrictedGrowth.lean)

### Existing paper and research program

- [Current additive-EFX counting paper](../paper/main.pdf)
- [Paper source](../paper/main.tex)
- [Accomplishments and claim ledger](../ACCOMPLISHMENTS.md)
- [Thesis research program](../docs/THESIS_RESEARCH_PROGRAM.md)

## Main external papers and methodological references

- [OpenAI prompt for the Cycle Double Cover proof program](https://cdn.openai.com/pdf/04d1d1e4-bc75-476a-97cf-49055cd98d31/cdc_prompt.pdf)
- [Terence Tao, “A digestion of the Jacobian conjecture counterexample”](https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/)
- [Chaudhury, Garg, and Mehlhorn, *EFX Exists for Three Agents*](https://arxiv.org/abs/2002.05119)
- [Mahara, *Extension of Additive Valuations to General Valuations on the Existence of EFX*](https://arxiv.org/abs/2107.09901)
- [Berger, Cohen, Feldman, and Fiat, *(Almost Full) EFX Exists for Four Agents (and Beyond)*](https://arxiv.org/abs/2102.10654)
- [Prakash HV et al., *EFX Exists for Three Types of Agents*](https://arxiv.org/abs/2410.13580)
- [Ashuri, Gkatzelis, and Sgouritsa, *EF2X Exists for Four Agents*](https://arxiv.org/abs/2412.00254)
- [Akrami et al., *A Counterexample to EFX ... Submodular Valuations via SAT-Solving*](https://arxiv.org/abs/2604.18216)
- [cvc5 documentation: CPC proof output and Ethos checking](https://cvc5.github.io/docs/cvc5-1.3.2/proofs/output_cpc.html)

The current literature check is consistent with additive EFX for four agents
remaining open, and with \(m\le n+3\) being the adjacent general existence
boundary. That check is preliminary and should not be treated as a complete
priority search.

## Bottom line for a non-specialist

The work has found a plausible way to prove that four people can always split
eight goods according to one of the strongest standard fairness rules. The
argument reduces infinitely many possible value tables to eight exact cases,
and every case has been ruled out as a possible counterexample by exact
algebraic solvers. The computations have been reproduced and independently
re-encoded; seven of eight cases now also carry proofs accepted by a separate
checker. The central mechanism that turns an arbitrary EFX allocation into a
“remove one good, then park it back” allocation is checked in Lean. Lean also
checks the positive perturbation, normalization, relabeling, favorite
matching, exact eight-cell coverage, partition-matching semantics, and the
two residual extension mechanisms.

That is an unusually strong research result. It is not yet the finished
theorem because the eighth machine proof, the published smaller-instance
theorem bridge, stabilizer formalization, the exact formal link from the
mathematics to the formulas, and external expert review still matter. If
those checks pass, the work should be treated as a potentially breakthrough
computer-assisted result. Until then, “high-quality closure candidate” is the
scientifically accurate description.
