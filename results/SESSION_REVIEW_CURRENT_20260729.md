# Superseded Research Review: Additive EFX for Four Agents and Eight Goods

> **Superseded on 2026-07-30.** The strict-positivity restriction has since
> been removed by a Lean-checked perturbation theorem, and the
> “breakthrough-level” significance language below was too strong. Use
> [`EFX48_BREAKTHROUGH_CONVERSION_20260730.md`](EFX48_BREAKTHROUGH_CONVERSION_20260730.md)
> and the revised submission for current status. This file is retained only
> as a dated session record.

**Snapshot:** 2026-07-30 EDT  
**Scope:** all work performed in the problem-selection, discovery, proof,
formalization, and certification session  
**Review type:** internal technical audit, not external peer review  
**Current verdict:** an internally verified hybrid computer-assisted proof
with a closed eight-case certificate stack and complete independent direct
cross-encoding; the frozen end-to-end audit and a fresh-source same-host replay
pass, while independent-machine reproduction and external review remain

## One-page status

The session selected and attacked the following main theorem:

> **Main theorem (current strengthening).** Every instance with four agents,
> eight indivisible goods, and nonnegative additive valuations has a complete EFX
> allocation.

The result now has a complete load-bearing proof architecture:

1. Lean reduces any hypothetical positive \(4\times8\) counterexample to one
   of eight exact terminal systems.
2. All eight terminal systems are UNSAT in the original exact-arithmetic Z3
   computation and in clean replays.
3. A separately written generator reconstructed all eight systems without
   importing the original encoder or Z3.
4. A separate parser audit connected every assertion in those generated
   formulas, including the exact canonical constants, to the terminal
   semantics formalized in Lean.
5. cvc5 generated independently checkable CPC proofs for all eight systems,
   and Ethos accepted all eight as `correct`.
6. The two published smaller-case theorems were checked against exact,
   hash-pinned paper versions and formally lifted into the local Lean model.
7. Lean's final theorem composes those inputs with the reduction. Its axiom
   audit reports only Lean's standard `propext`, `Classical.choice`, and
   `Quot.sound`; it contains no `sorryAx` or `native_decide` dependency.

This is much stronger than experimental evidence or a single solver result.
The load-bearing hybrid proof is internally closed. All eight cells have also
passed a direct-allocation cross-encoding over every one of the 40,824
labeled onto allocations. The deterministic end-to-end audit now passes and
binds the proof, audits, tools, direct cross-check, Lean build, and source
archive in a 73-entry manifest. The work is nevertheless not yet ready for an
unqualified public announcement: the frozen source archive has built in a new
project directory on the original host, but it still needs an independent-
machine replay, and no independent fair-division expert has reviewed the
mathematics. An eight-page technical manuscript and reviewer handoff now exist,
but they are not yet a submission-ready paper. The published paper proofs also
remain external trusted inputs rather than being reformalized in Lean.

### Status dashboard

| Layer | Current status | Assessment |
|---|---:|---|
| Structural proof architecture | Developed | Substantial original mathematics |
| Lean formalization of reduction | Builds | No local `sorry` or `axiom` declarations found |
| Original exact terminal solves | 8/8 UNSAT | Complete but solver-dependent |
| Clean original-formula replays | 8/8 UNSAT | Complete |
| Independent formula generation | 8/8 emitted and audited | Complete |
| Exact formula-to-semantics parser audit | 8/8 passed | Complete |
| cvc5 CPC proof generation | 8/8 | Complete; 1.668 GB / 13.812 M steps |
| Ethos checking of CPC proofs | 8/8 `correct` | Complete |
| CPC artifact manifest | 45/45 entries hash-verified | Complete |
| Published theorem variants and lifting | Exact PDFs audited; Lean wrapper builds | Complete, with paper proofs trusted externally |
| Final Lean theorem axiom audit | Standard Lean axioms only | Complete |
| Direct-allocation cross-encoding | 8/8 UNSAT over 40,824 allocations each | Complete non-load-bearing independent check |
| Explanatory core reduction | 200 partitions reduced to a deletion-minimal 130 | CPC proof accepted by Ethos |
| End-to-end release manifest | 73/73 entries verified | Frozen internal audit complete |
| Fresh-source reproduction | New project extraction, build, audits, and manifest pass | Same host and pinned dependency checkout |
| Full Ethos replay through fresh-source workflow | 8/8 `correct` | Same host |
| Human exposition | Eight-page technical manuscript and reviewer handoff | Review draft, not submission-ready |
| External mathematical review | None | Major remaining requirement |
| Publishable paper | Technical review draft written | Expansion and expert revision remain |

### Suggested review path

- **Five minutes:** read the dashboard, “problem in basic language,” and
  “level of work.”
- **Twenty minutes:** add the six-step proof idea, significant error found,
  review-depth rating, and trust boundary.
- **Technical audit:** open the final Lean theorem and axiom audit, then the
  frozen eight-cell certificate summary, semantic-binding audit, published-
  input audit, and manifest linked near the end.

## The problem in basic language

There are four people and eight indivisible goods. Each person assigns a
positive number to each good. Their value for a bundle is simply the sum of
the values of the goods in it.

An allocation is **EFX**, or *envy-free up to any good*, when the following
strong fairness test always passes:

> If person \(i\) looks at person \(j\)'s bundle, then after removing any one
> good from \(j\)'s bundle, person \(i\) does not prefer what remains to their
> own bundle.

This is stronger than merely asking whether *some* removable good eliminates
envy.

Known results give complete EFX allocations for three additive agents and,
separately, when the number of goods is at most \(n+3\). With four agents,
those boundaries cover seven goods but not eight. Thus \(4\times8\) is the
first near-diagonal case immediately outside both standard existence
theorems.

The proof strategy is contradiction. Assume there is a bad valuation table
with no EFX allocation. The work shows that such a table can be cleaned up,
renamed, and placed into one of only eight canonical patterns. Each pattern
then says that all possible ways to divide the eight goods fail. Exact
arithmetic solvers report that every such pattern is internally impossible.

## The proof idea, step by step

### 1. Turn allocation existence into a structural object

For each agent and bundle, define a threshold: the largest value left after
removing one good from that bundle. EFX says that an agent's own bundle value
is at least every other bundle's threshold.

This supports the **Reverse Parking Lemma**. It characterizes when one owned
good can be removed while preserving EFX. If no good is removable, bundles
can be rotated around a strict improvement cycle. A finite potential strictly
increases, so the rotations must terminate. The endpoint has a removable
good.

In plain terms: an EFX allocation can always be rearranged until one good can
be “parked” outside and safely returned later. This turns the parking idea
from a heuristic into an exact normal form.

### 2. Normalize a hypothetical counterexample

Multiplying all of one agent's values by a positive constant does not change
their EFX comparisons. Each row can therefore be normalized to sum to one.

The set of no-EFX instances is open. A hypothetical counterexample can be
perturbed slightly so that every agent has a strict ranking of the goods,
without creating an EFX allocation. This removes tie pathologies.

### 3. Reduce rankings to eight canonical cells

If all four agents have distinct favorite goods, a direct favorite-matching
construction gives an EFX allocation: give each agent their favorite plus
one of the four remaining goods.

Therefore a counterexample must have repeated favorites. Up to renaming
agents and goods, the repeated-favorite patterns are:

- \(2+1+1\);
- \(3+1\);
- \(2+2\); or
- \(4\), where all agents share one favorite.

In the common-favorite case, the second favorites have five possible
multiplicity patterns:

- \(1+1+1+1\);
- \(4\);
- \(3+1\);
- \(2+2\); or
- \(2+1+1\).

That gives exactly eight terminal ranking cells. Lean now checks not only
this pattern list, but also the stabilizer symmetries used to impose
lexicographic row and column order inside the cells.

### 4. Remove easy residual cases using existing theorems

Two families of valuations can be extended from known smaller EFX instances:

- if some good is a minimum for every agent, delete it, use the four-agent
  seven-good theorem, and add it back safely;
- if an agent-good pair satisfies a “peelable” inequality, delete that agent
  and good, use the three-agent seven-good theorem, and add them back.

The smaller existence inputs are exactly the known results for at most
\(n+3\) goods and for three additive agents. The lifting constructions from
the standard theorem statements into the local deleted-good formulations are
now proved in Lean.

### 5. Enumerate every possible bundle partition

There are

\[
S(8,4)=1{,}701
\]

ways to split eight labeled goods into four nonempty *unlabeled* bundles.
Lean checks both this exact count and that the restricted-growth enumeration
covers every onto allocation up to relabeling.

For each partition, form a \(4\times4\) bipartite graph. An edge says that a
particular agent could receive a particular bundle while satisfying all EFX
comparisons. The partition yields an EFX allocation exactly when this graph
has a perfect matching.

Therefore a counterexample must obstruct all 24 perfect matchings for every
one of the 1,701 partitions.

### 6. Prove the eight exact systems inconsistent

Each terminal cell is a rational linear-arithmetic formula containing:

- positivity and row normalization;
- the two residual exclusions;
- exact favorite/second-favorite and stabilizer constraints;
- 27,216 feasibility-edge definitions; and
- 40,824 perfect-matching obstruction assertions.

Every original formula is UNSAT. All eight independently regenerated
formulas also have cvc5 CPC proof objects accepted as `correct` by Ethos.

## Main research outputs

### Structural results

1. **Reverse Parking Lemma and Threshold-Cycle Normal Form.** This gives a
   necessary-and-sufficient removal criterion and a terminating improvement
   mechanism.
2. **Favorite-Good Matching Lemma.** At \(m=2n\), distinct favorite goods
   immediately yield a complete EFX allocation.
3. **Favorite Small-Bundle Lemma.** For arbitrary finite positive additive
   instances, a valid allocation is EFX whenever every agent owns a favorite
   good and every bundle has at most two goods. This isolates the reusable
   mathematical reason behind the favorite construction for
   \(n\le m\le2n\). A second generic theorem now constructs such an
   allocation from an injective favorite map and an embedding of the
   remaining goods into the agents, and a cardinal corollary constructs that
   embedding automatically whenever \(m\le2n\).
4. **Generic eight-cell reduction.** A positive counterexample can be
   normalized, perturbed to strict rankings, and relabeled into eight cells.
5. **Stabilizer-orbit completeness.** The row and unused-column
   lexicographic constraints lose no counterexamples.
6. **Partition/matching equivalence.** No EFX allocation exists exactly when
   every valid nonempty partition has a perfect-matching obstruction.
7. **Residual extension lemmas.** Universal-minimum and peelable instances
   lift smaller EFX allocations to the full problem.
8. **Conditional end theorem.** Lean proves the \(4\times8\) result from the
   two standard published inputs and UNSAT of the eight terminal cells.

### Computational results

- Eight of eight original QF_LRA formulas: `unsat`.
- Eight of eight archived formulas replayed in fresh Z3 processes.
- Eight of eight originals rebuilt byte-for-byte in isolated processes.
- Eight of eight formulas independently regenerated.
- \(3{,}402/3{,}402\) partition/matrix differential checks passed.
- \(592/592\) cell-preamble differential checks passed.
- Eight of eight full formulas passed the generator-independent semantic
  parser audit.
- Eight CPC proofs totaling 1,668,457,899 bytes and 13,812,082 proof steps
  were accepted by Ethos.
- A 45-entry SHA-256 manifest verifies the formulas, proofs, per-cell
  certificates, semantic and literature audits, exact source PDFs, solver
  and checker binaries, signatures, Z3 replay, and rebuild audit.
- One representative terminal formula was reduced to a 200-partition UNSAT
  core and independently solved by cvc5.
- A direct allocation encoding over all 40,824 labeled onto allocations
  returned UNSAT for all eight cells. Six closed directly in Z3. The two
  hardest formulas closed in cvc5 after an audited identity-only SMT-LIB
  syntax normalization. This cross-check is not needed by the proof, but
  independently tests the partition/matching formulation.
- Deletion-based minimization reduced one 200-partition terminal core to a
  130-partition deletion-minimal core: deleting any one survivor makes the
  reduced formula satisfiable. A 220.8 MB CPC proof with 2,032,963 steps was
  accepted by Ethos. This is explanatory work, not a prerequisite for the
  main theorem, and deletion minimality is not minimum cardinality.

### Formal outputs

The pinned Lean 4.32.1/mathlib project checks:

- the allocation and EFX definitions;
- reverse parking and threshold-cycle termination;
- the generic favorite-small-bundle EFX criterion;
- positivity, nonempty bundles, relabeling, and row normalization;
- openness of the no-EFX region and generic strict perturbation;
- favorite-pattern and second-favorite-pattern coverage;
- exact coverage by the eight terminal cells;
- stabilizer-orbit completeness;
- all 1,701 restricted-growth partitions and coverage of all onto owner maps;
- the exact matching-obstruction equivalence;
- both residual extension arguments;
- the reduction from a positive counterexample to the eight terminal cells;
  and
- lifting of standard four-agent/seven-good and
  three-agent/seven-good results into the local hypotheses; and
- the final theorem
  `admitsEFX_4x8_of_standard_published_inputs`, which composes those published
  inputs with UNSAT of the eight terminal cells.

The final theorem's permanent axiom audit reports exactly
`[propext, Classical.choice, Quot.sound]`. Four small canonical-pattern
computations that initially introduced `native_decide` axioms were replaced
with kernel-checked `decide`; the final theorem now has no
`native_decide`, `ofReduceBool`, or `sorryAx` dependency.

### Broader additive-EFX program outputs

The repository's existing ten-page counting paper is a separate, narrower
line of work. In basic terms, it asks not just whether a fair allocation
exists, but how many such allocations an instance must have. It contributes:

- explicit positive additive instances having exactly \(n\) labeled EFX
  allocations at \((4,7),(5,8),(6,9),(4,8),(4,9),(4,10)\);
- a necessary-and-sufficient generalized parking criterion for adding one
  leftover good to an EFX base allocation; and
- a computer-verified lower bound of four EFX allocations for every positive
  integer \(4\times7\) instance with values in \(\{1,2,3,4\}\).

Those results were already paper-scale, but they did not prove unrestricted
EFX existence or the conjectured additive lower bound of \(n\). The new
\((4,8)\) theorem resolves existence at one frontier cell and therefore
strengthens the broader program without settling the general counting
conjecture.

## A significant error found during review

The audit was not merely confirmatory. It found a load-bearing specification
error in the first version of the peelable reduction.

The old `DeletedAgentGoodEFX` definition demanded ordinary four-agent EFX
after deleting one agent and leaving that deleted agent with an empty bundle.
With positive values this is generally impossible: the empty agent would
envy nonempty bundles. The extension proof never needed that condition. It
only needed EFX comparisons made by the other three agents.

The definition was corrected to use `EFXExceptObserver`, which excludes the
deleted agent as an observer while retaining every comparison needed by the
extension theorem. The corrected peelable proof and all downstream modules
build.

This increases confidence that the review is probing semantics rather than
only checking syntax. It also illustrates why the remaining external review
is essential.

## How deeply has the work been reviewed?

### Strongly reviewed

- **Combinatorial coverage:** Lean proves the canonical patterns, stabilizer
  reductions, 1,701 count, and onto-coverage theorem.
- **Mathematical reduction:** the main transformations and extension
  arguments are machine-checked in Lean.
- **Encoding reproducibility:** originals rebuild byte-for-byte.
- **Encoder independence:** the second generator does not import the
  original encoder, partition code, Z3, or project encoding.
- **Formula semantics:** a separate parser checks every exact assertion in
  all eight emitted formulas, reconstructs the partition universe, and binds
  each cell to the exact canonical constants and semantic specification in
  Lean.
- **Solver diversity:** Z3 and cvc5 are independent solvers.
- **Proof checking:** Ethos accepts all eight cvc5 CPC proof objects.
- **Artifact integrity:** a 45-entry manifest has been checked in full.
- **Literature boundary:** exact Mahara v2 and
  Chaudhury–Garg–Mehlhorn v3 PDFs are hash-pinned, and an executable audit
  verifies the theorem, completeness, additivity, and EFX-definition
  fragments used by the Lean interfaces.
- **Formal dependency audit:** the composed final Lean theorem has no
  `sorryAx` or native-computation axiom.
- **Adversarial specification review:** it found and repaired a real
  deleted-agent semantic bug.

### Not yet reviewed enough

- No independent human expert has checked the proof.
- No fair-division specialist has confirmed novelty or the exact relationship
  to the latest literature.
- The literature results are hypotheses in Lean, not themselves formalized
  from their papers.
- Ethos and the semantic parser are ordinary software, not formally verified
  kernels.
- The technical manuscript is not yet a polished submission paper.
- The deterministic end-to-end release manifest verifies all 73 entries.
- A fresh-source same-host replay passes, but no second machine or
  cross-platform environment has reproduced the final frozen release.

### Review-depth rating

| Dimension | Rating | Meaning |
|---|---:|---|
| Internal mathematical audit | High | Core reductions are formalized |
| Computational reproducibility | Very high | Multiple rebuilds, encodings, solvers, and hashes |
| Proof-object coverage | Complete | 8/8 terminal systems checked |
| Formal trust-chain closure | High but hybrid | Lean-to-SMT bridge is exact and audited, not kernel-integrated |
| Independent expert scrutiny | None | Not yet peer reviewed |
| Overall confidence | Very strong internally | Release replay and external scrutiny still matter |

## Level of work

The most accurate classification separates the *quality of the work* from
the *status of the claim*.

| Aspect | Current level |
|---|---|
| Individual structural lemmas | Strong thesis-chapter material |
| Integrated reduction and formalization | Advanced PhD/postdoctoral or professional-research level |
| Certification engineering | Frontier computer-assisted mathematics |
| Mathematical significance if novel | Modest but real fixed-parameter contribution |
| Present research status | Internally verified theorem; not externally reviewed or publication-ready |

So the concise judgment is:

> **The proof engineering is advanced research work. The theorem itself is a
> bounded contribution at one fixed cell, not presently a field-level
> breakthrough.**

The first two of those gates now pass: all eight proofs check, and the exact
literature inputs match the formal interfaces. Same-host fresh-source
reproduction and an initial human manuscript also pass; independent-machine
reproduction and knowledgeable external review remain. If those pass, the
result would be a credible specialized research-paper contribution. A
breakthrough would require a general \(m=n+4\) theorem, a four-agent
arbitrary-\(m\) theorem, or a comparably general structural step.

## Current trust boundary

The end result currently has the form

\[
\begin{aligned}
&\text{published EFX inputs}\\
&+\ \text{Lean-checked structural reduction}\\
&+\ \text{parser-audited exact SMT translation}\\
&+\ \text{eight terminal UNSAT results}\\
&\Longrightarrow \text{nonnegative additive EFX at }(4,8).
\end{aligned}
\]

The first two lines are mathematically explicit. The third is a strong
software audit. The fourth has independently checked proof objects for all
eight cases as well as original exact solver closure.

## Already planned next steps

Completed since the first plan:

- all eight cvc5/Ethos certificates and their 45-entry manifest;
- the final published-input Lean wrapper and root import;
- a full pinned Lean build and formal axiom audit;
- exact paper-version and theorem-variant audits; and
- exact binding from the independent formulas to Lean's canonical cell
  constants.

Remaining work, in order:

1. Reproduce the frozen bundle on a genuinely independent machine or
   cross-platform environment.
2. Analyze Hall-deficient sets and threshold inequalities inside the
   deletion-minimal 130-partition core.
3. Search for a shorter analytic contradiction that could replace or
   substantially reduce the eight large proof objects.
4. Expand the technical review manuscript into a submission-ready human proof
   and transparent computer-assisted appendix.
5. Ask at least one EFX/fair-division expert and one
   computer-assisted-proof expert for adversarial review.
6. Perform a systematic novelty check before making a public breakthrough
   claim.

## Main local artifacts

| Artifact | Purpose |
|---|---|
| [Existing additive-EFX counting paper](../paper/main.pdf) | Ten-page paper on exact count-\(n\) witnesses, generalized parking, and the bounded \(4\times7\) result |
| [Paper source](../paper/main.tex) | LaTeX source for the current paper |
| [EFX \(4\times8\) review manuscript](../output/pdf/efx48-review-draft.pdf) | Eight-page explanation of the theorem, certificate stack, trust boundary, and core geometry |
| [External reviewer handoff](EFX48_REVIEWER_HANDOFF.md) | Review tracks, commands, limitations, and response template |
| [Remaining-gates ledger](EFX48_REMAINING_GATES_20260730.md) | Closed, active, externally blocked, and publication gates |
| [EFX \(4\times8\) LRA certificate](EFX_4X8_LRA_CERTIFICATE.md) | Main computational result and terminal-cell description |
| [EFX \(4\times8\) proof guide](EFX48_PROOF_GUIDE.md) | Human-readable deduction chain, certificate boundary, and reviewer entry points |
| [Reverse Parking Lemma](REVERSE_PARKING_LEMMA.md) | Structural normal-form result |
| [Complementary Wall Certificate](COMPLEMENTARY_WALL_CERTIFICATE.md) | Local boundary mechanism and exact certificate |
| [Original ten-hour goal](PARKABILITY_GOAL_20260729.md) | Research objective, closure standard, and planned work |
| [Lean entry point](../formal/efx48/EFX48.lean) | Imported formal proof modules |
| [Terminal-cell reduction](../formal/efx48/EFX48/TerminalCells.lean) | Main reduction and conditional theorem |
| [Stabilizer proof](../formal/efx48/EFX48/Stabilizers.lean) | Orbit-completeness proof |
| [Partition enumeration](../formal/efx48/EFX48/RestrictedGrowth.lean) | Exact 1,701 count and coverage |
| [Matching equivalence](../formal/efx48/EFX48/PartitionMatching.lean) | Partition graph semantics |
| [Published inputs](../formal/efx48/EFX48/PublishedInputs.lean) | Abstract smaller-case hypotheses and end theorem |
| [Published-input lifting and final theorem](../formal/efx48/EFX48/PublishedLifting.lean) | Formal lifting and composed \(4\times8\) theorem |
| [Final theorem axiom audit](../formal/efx48/AxiomAudit.lean) | Permanent audit of the final Lean dependency boundary |
| [Corrected peelable reduction](../formal/efx48/EFX48/Peelable.lean) | Deleted-agent extension with correct observer scope |
| [Independent generator](../tracks/parkability/independent_lra_generator.py) | Generator independent of the original SMT encoder |
| [Semantic-binding audit](../tracks/parkability/audit_independent_formula_semantics.py) | Exact formula-to-Lean-spec parser audit |
| [Published-input audit](../tracks/parkability/audit_published_inputs.py) | Hash-pinned paper theorem and definition audit |
| [Certificate finalizer](../tracks/parkability/finalize_cpc_certificates.py) | Final manifest and certificate-bundle validation |
| [Direct-allocation cross-check](../tracks/parkability/run_direct_all_cells.py) | All-\(40{,}824\)-allocation alternative encoding |
| [End-to-end finalizer](../tracks/parkability/finalize_efx48_end_to_end.py) | Reproducible frozen release and trust audit |
| [Structure of the explanatory core](CORE_200_STRUCTURE.md) | Exact 200-to-130 shrink, deletion minimality, and independently checked reduced-core proof |
| [Broader generalization map](BROADER_GENERALIZATION_MAP.md) | Dependency ladder and exact state-space estimates for \((4,9)\), \((5,9)\), and \((5,10)\) |
| [Novelty audit](NOVELTY_AUDIT_20260729.md) | Targeted comparison with the closest additive-EFX literature |
| [Expert review checklist](EXPERT_REVIEW_CHECKLIST.md) | Adversarial checklist split among fair-division, formal, and computational reviewers |

The large frozen formulas, proof objects, and audit JSON files live outside
the source directory at:

`game-theory/experimental-runs/additive-efx-counting-runs/parkability/certification-20260729`

The main frozen certification outputs are:

- [Eight-cell CPC certificate summary](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/EIGHT_CELL_CPC_CERTIFICATES.json)
  — all eight proof results, hashes, timings, sizes, and step counts;
- [Passing 45-entry CPC manifest](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/EIGHT_CELL_CPC_MANIFEST.sha256);
- [Semantic-binding audit](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/independent-generator-audit/semantic-binding.json)
  — all eight formula hashes, assertion categories, exact partition counts,
  canonical constants, and Lean terminal specifications; and
- [Published-input audit](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/literature/PUBLISHED_INPUT_AUDIT.json)
  — the exact paper hashes, theorem fragments, formal interfaces, and
  remaining external trust statement;
- [Direct-allocation cross-check summary](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/direct-allocation-crosscheck/DIRECT_ALLOCATION_CROSSCHECK.json)
  — all eight alternative encodings over the exact 40,824-allocation
  universe; and
- [Reduced-core CPC/Ethos certificate](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/core-shrinking/favorite-211.shrunk.certificate.json)
  — the separately checked proof of the 130-partition explanatory core;
- [Deletion-witness analysis](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/core-shrinking/favorite-211.deletion-witnesses.json)
  — exact valuation, matching, and Hall data for the completed core deletions;
- [Fresh-source replay record](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/EFX48_CLEAN_SOURCE_REPLAY.json)
  — source extraction, semantic audits, Lean build, axiom audit, manifest
  verification on the original host;
- [Full fresh-source/Ethos replay record](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/EFX48_CLEAN_SOURCE_FULL_ETHOS_REPLAY.json)
  — all eight frozen proof hashes and `correct` Ethos verdicts from the
  same-host replay;
- [End-to-end certificate](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/EFX48_END_TO_END_CERTIFICATE.json)
  — one machine-readable summary of the complete hybrid deduction chain; and
- [Passing 73-entry end-to-end manifest](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260729/EFX48_END_TO_END_MANIFEST.sha256)
  — frozen hashes for every load-bearing proof, audit, tool, input, build log,
  cross-check, and source-archive artifact.

## Main external papers and inspiration

- Bhaskar Ray Chaudhury, Jugal Garg, and Kurt Mehlhorn,
  [“EFX Exists for Three Agents”](https://arxiv.org/abs/2002.05119).
- Ryoga Mahara,
  [“Extension of Additive Valuations to General Valuations on the Existence
  of EFX”](https://arxiv.org/abs/2107.09901), including the \(m\le n+3\)
  existence theorem.
- Ben Berger, Avi Cohen, Michal Feldman, and Amos Fiat,
  [“(Almost Full) EFX Exists for Four Agents (and
  Beyond)”](https://arxiv.org/abs/2102.10654), the closest four-agent
  partial-allocation context.
- [The Cycle Double Cover research prompt](https://cdn.openai.com/pdf/04d1d1e4-bc75-476a-97cf-49055cd98d31/cdc_prompt.pdf),
  which supplied the exact-target, multi-representation, adversarial-audit,
  and explicit-gap discipline.
- [Formal verification of the recent explicit Jacobian
  counterexample](https://isa-afp.org/entries/Jacobian_Counterexample.html),
  a useful model for converting a striking computational discovery into a
  compact, independently checkable result.

## Bottom line

The session did not merely run a large search. It found a coherent structural
route, reduced the continuous problem to eight exact finite cells, formalized
the mathematical reduction and final conditional theorem, independently
regenerated and audited the formulas, pinned the published inputs, and
obtained separately checked proof objects for every cell.

The central theorem now has a closed internal hybrid proof stack and plainly
merits a serious paper and expert review. The correct present label is:

> **Internally verified computer-assisted theorem; advanced
> PhD/professional-frontier work; breakthrough-level potential; not yet
> independently reproduced, externally reviewed, or peer reviewed.**
