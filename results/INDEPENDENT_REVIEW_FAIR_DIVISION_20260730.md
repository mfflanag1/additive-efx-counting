# Independent Review 1: Fair-Division Mathematics

**Date:** 2026-07-30 EDT  
**Reviewer:** independent subagent, fair-division mathematical track  
**Repository access:** read-only  
**Verdict:** **conditional acceptance; no material mathematical issue found**

This review was conducted independently of the formal/computational review.
The reviewer did not defer to the session's prior confidence assessment.

## Conditions on the verdict

Acceptance is conditional on:

1. the eight archived QF_LRA systems being UNSAT under the stated CPC/Ethos
   interpretation;
2. the Mahara and Chaudhury--Garg--Mehlhorn theorems being accepted as
   external published inputs; and
3. the manually inspected Lean-to-SMT correspondence remaining sound.

The reviewer found no reversed inequality, missing EFX comparison, invalid
symmetry, positivity/completeness mismatch, or uncovered favorite-pattern
case.

## Layers checked

- EFX and complete-allocation definitions:
  [`Definitions.lean`](../formal/efx48/EFX48/Definitions.lean).
- Openness of no-EFX, normalization, and sum-preserving generic
  perturbation:
  [`Perturbation.lean`](../formal/efx48/EFX48/Perturbation.lean),
  [`Normalization.lean`](../formal/efx48/EFX48/Normalization.lean), and
  [`StrictPerturbation.lean`](../formal/efx48/EFX48/StrictPerturbation.lean).
- Favorite-small-bundle construction and the injective-favorite case.
- The four noninjective favorite kernels and five common-favorite
  second-choice kernels:
  [`RankingCells.lean`](../formal/efx48/EFX48/RankingCells.lean).
- Relabeling directions and cell-preserving stabilizers:
  [`Stabilizers.lean`](../formal/efx48/EFX48/Stabilizers.lean).
- Universal-minimum deletion and reinsertion:
  [`UniversalMinimum.lean`](../formal/efx48/EFX48/UniversalMinimum.lean).
- Corrected peelable agent--good reduction, including observer scope:
  [`Peelable.lean`](../formal/efx48/EFX48/Peelable.lean).
- Partition-to-perfect-matching equivalence:
  [`PartitionMatching.lean`](../formal/efx48/EFX48/PartitionMatching.lean).
- Composition into eight terminal cells:
  [`TerminalCells.lean`](../formal/efx48/EFX48/TerminalCells.lean).
- Both published-input liftings and the pinned theorem variants:
  [`PublishedLifting.lean`](../formal/efx48/EFX48/PublishedLifting.lean).
- Manual comparison of terminal predicates with the independent formula
  generator:
  [`independent_lra_generator.py`](../tracks/parkability/independent_lra_generator.py).
- The review manuscript and proof guide.

## Strongest attempted falsification

The reviewer tried to find an SMT assertion stronger than its corresponding
Lean terminal condition. Such an assertion would invalidate the implication
"Lean terminal witness implies SMT witness," and an UNSAT result would no
longer discharge the Lean terminal cell.

The manual comparison found:

- positivity and normalization: exact;
- no-universal-minimum direction: exact;
- no-peelable direction: exact;
- pairwise row inequality: exact;
- favorite and second-favorite inequalities: exact;
- stabilizer constraints: encoded adjacent comparisons follow from Lean's
  all-pairs lexicographic constraints;
- every feasibility edge: the intended EFX observer condition; and
- every matching clause: the negation of one of the 24 bundle assignments.

No offending assertion was found.

Encoding 1,701 canonical partitions was also judged sound for the required
direction. `TerminalBase` obstructs every valid nonempty partition; hence a
terminal witness necessarily obstructs each encoded canonical partition.

## Findings

### Moderate: the semantic binding is not extracted mechanically from Lean

The parser checks every SMT assertion against a separately hand-coded Python
specification in
[`audit_independent_formula_semantics.py`](../tracks/parkability/audit_independent_formula_semantics.py).
Its direct Lean parsing is largely limited to canonical vector constants. It
does not parse the Lean definitions of `ResidualCellAssumptions`,
`TerminalBase`, `FeasibleEdge`, or the stabilizers.

The reviewer manually compared those definitions and found them sound.
Nevertheless, prose saying that the audit "binds every assertion to Lean"
can sound more automatic than the present architecture warrants.

### Minor: the displayed Lean theorem is conditional

`admitsEFX_4x8_of_standard_published_inputs` takes three hypotheses:

1. the four-agent/seven-good published input;
2. the three-agent/seven-good published input; and
3. `EightTerminalCellsUnsat`.

The paper discusses this trust chain but should print the complete signature
prominently.

### Minor: stale source-archive count

The manuscript says the source archive contains 60 files. The final replay
records 66 members.

### Minor: finite-type transport is implicit

`ThreeAgentSevenGoodStandardInput` quantifies over arbitrary three-element
agent types, while the paper is stated for a canonical three-agent type.
Transport across a finite equivalence is routine and mathematically
harmless, but an explicit wrapper would make the claimed exact interface
literal.

## Published-input assessment

The pinned Mahara result supplies complete EFX for the required
four-agent/seven-good instance under the matching "remove any target good"
convention. Positive additive valuations are within its scope.

The pinned Chaudhury--Garg--Mehlhorn result supplies complete EFX for three
additive agents, so its seven-good specialization is valid.

The reviewer found the local lifting logic sound:

- positivity forces nonempty bundles in the four-by-seven use;
- universal-minimum insertion checks removal of both the inserted good and
  every old target good; and
- the peelable case excludes the deleted agent only as an observer while
  retaining the active-observer comparisons required after reinsertion.

## Unchecked dependencies

- CPC semantics and the full Ethos replay.
- The proofs inside the two published papers.
- Formal verification of the Python parser.
- Second-machine reproduction.
- Novelty.
- Any extension from strictly positive to zero-valued goods.

## Mandatory next actions

1. Independently validate the CPC/Ethos and hash chain.
2. Replace or supplement the handwritten bridge with a mechanically
   checkable implication from each Lean terminal specification to its emitted
   SMT preamble.
3. Print the full conditional Lean signature and hybrid trust chain.
4. Correct the source-archive count from 60 to 66.
5. Add the explicit three-element finite-type transport wrapper.
6. Obtain review from an active fair-division researcher before making a
   public breakthrough claim.

## Confidence

- Fair-division reduction, conditional on terminal UNSAT: **0.88**.
- Complete hybrid theorem, with computational checking outside this review:
  **approximately 0.72**.
- Novelty: not assessed.

