# Expert Review Checklist: Additive EFX at \((4,8)\)

**Claim under review.** Every nonnegative additive valuation instance
with four agents and eight indivisible goods admits a complete EFX allocation.

**Proof style.** Hybrid computer-assisted proof:

1. two published smaller-case existence theorems;
2. a Lean-checked structural reduction to eight terminal cells;
3. an independently written exact SMT generator;
4. an executable formula-to-Lean semantic audit; and
5. eight cvc5 CPC proofs accepted by the separate Ethos checker.

**Current review status.** Internal adversarial audit is advanced. No external
fair-division or proof-certification expert has signed off.

Start with the concise
[`EFX48_REVIEWER_HANDOFF.md`](EFX48_REVIEWER_HANDOFF.md) and the rendered
[`submission manuscript`](../output/pdf/efx48-submission.pdf).

## Recommended division of review labor

### Fair-division reviewer

- Check the exact EFX convention in
  [`Definitions.lean`](../formal/efx48/EFX48/Definitions.lean).
- Check the Reverse Parking and Threshold-Cycle arguments in
  [`ReverseParking.lean`](../formal/efx48/EFX48/ReverseParking.lean) and
  [`ThresholdCycle.lean`](../formal/efx48/EFX48/ThresholdCycle.lean).
- Check favorite matching, strict perturbation, and the eight canonical
  ranking cells.
- Check that the universal-minimum and peelable residual cases really extend
  smaller EFX allocations.
- Check the exact external theorem variants in
  [`PUBLISHED_INPUT_AUDIT.md`](PUBLISHED_INPUT_AUDIT.md).
- Assess novelty using
  [`NOVELTY_AUDIT_20260729.md`](NOVELTY_AUDIT_20260729.md).

### Formal-methods reviewer

- Build the pinned Lean project and inspect
  [`AxiomAudit.lean`](../formal/efx48/AxiomAudit.lean).
- Check that the root entry point imports every proof module.
- Search for `sorry`, local `axiom`, and `opaque` declarations.
- Review the finite canonical-pattern decisions and confirm that the final
  theorem does not depend on `native_decide`.
- Inspect the parser-based semantic bridge between the emitted SMT-LIB and
  the Lean terminal specifications.
- Recheck all eight CPC proofs with the pinned Ethos binary.

### Computational fair-division reviewer

- Compare the original and independent terminal generators.
- Inspect the exact 1,701-partition universe and the 24 perfect matchings per
  partition.
- Verify the all-40,824-allocation alternative encoding in every cell.
- Review formula and proof hashes, pinned binaries, and reproducibility
  records.
- Attempt a third implementation of at least one terminal cell.

## Load-bearing mathematical chain

### 1. Definitions and completeness

- [ ] `ValidAllocation` assigns every good to exactly one owner.
- [ ] `EFX` quantifies over every target good, not merely one removable good.
- [ ] The uniform perturbation correctly reduces a nonnegative
  counterexample to a positive one.
- [ ] Strict positivity is used only after that reduction.
- [ ] With eight goods and four agents, every complete positive EFX
  allocation has nonempty bundles.

### 2. Normalization and perturbation

- [ ] The EFX-existence set is closed and the no-EFX set is open.
- [ ] Uniform positive perturbation preserves nonexistence for sufficiently
  small time.
- [ ] Positive row scaling preserves every EFX comparison.
- [ ] A positive counterexample can be row-normalized.
- [ ] The perturbation simultaneously preserves positivity, row sums, and
  nonexistence while making all row rankings strict.

### 3. Favorite and symmetry reductions

- [ ] Injective favorite labels yield EFX through the pair construction.
- [ ] Every noninjective four-label kernel reduces to
  \(2+1+1\), \(3+1\), \(2+2\), or \(4\).
- [ ] The common-favorite cell splits into exactly five second-favorite
  kernels.
- [ ] The stabilizer lexicographic constraints preserve at least one
  representative of every relevant orbit.

### 4. Residual cuts

- [ ] A universally minimum good can be deleted and safely reinserted after
  moving the smaller allocation to an unenvied source.
- [ ] The four-agent/seven-good input is exactly covered by Mahara's
  \(m\le n+3\) theorem.
- [ ] A peelable agent--good pair can be deleted and reinserted.
- [ ] The deleted agent is excluded only as an observer; no impossible EFX
  condition is imposed on its empty bundle.
- [ ] The three-agent/seven-good input is exactly covered by
  Chaudhury--Garg--Mehlhorn.

### 5. Partition/matching reduction

- [ ] The restricted-growth enumeration contains exactly
  \(S(8,4)=1{,}701\) nonempty unlabeled partitions.
- [ ] It covers every onto labeled allocation up to bundle relabeling.
- [ ] An agent--bundle edge has exactly the intended EFX feasibility
  semantics.
- [ ] A fixed partition supports EFX exactly when its \(4\times4\)
  feasibility graph has a perfect matching.
- [ ] The 24 obstruction clauses are exactly the negations of all perfect
  matchings.

### 6. Terminal formulas

- [ ] Every formula asserts positivity and row normalization.
- [ ] Both residual exclusions match their Lean predicates.
- [ ] Favorite, second-favorite, row, and column constraints match the exact
  canonical cell.
- [ ] All 27,216 edge definitions and 40,824 matching obstructions are
  present.
- [ ] The semantic audit is independent enough to catch a generator error.

### 7. UNSAT certificates

- [ ] All eight formulas were regenerated independently.
- [ ] cvc5 reports UNSAT and emits a CPC proof for every formula.
- [ ] Ethos reports `correct` for every CPC proof.
- [ ] Formula, proof, tool, signature, audit, and source-paper hashes match
  the frozen manifest.

## Highest-value adversarial questions

1. Does the strict perturbation cross any EFX-existence boundary or lose row
   normalization?
2. Are agent and good relabelings composed in the correct direction in every
   canonical cell?
3. Do the stabilizers accidentally combine symmetries that are no longer
   available after fixing a favorite pattern?
4. Does the corrected peelable predicate retain every observer comparison
   needed for reinsertion?
5. Can an EFX allocation with an empty bundle survive positivity at
   \(4\times8\)?
6. Does the SMT parser verify semantics, or merely reproduce the generator's
   assertion counts?
7. Is any formula line accepted by cvc5 under a logic or coercion different
   from the intended rational linear arithmetic?
8. Can every final theorem dependency be accounted for by the displayed
   Lean axiom audit?
9. Are the published theorem statements complete-allocation results under
   the same “remove any target good” convention?
10. Can the whole frozen package be reproduced without relying on an
    unrecorded local file or environment variable?

## Frozen artifacts

Certification root:

`game-theory/experimental-runs/additive-efx-counting-runs/parkability/certification-20260729`

Primary records:

- `EIGHT_CELL_CPC_CERTIFICATES.json`;
- `EIGHT_CELL_CPC_MANIFEST.sha256`;
- `independent-generator-audit/semantic-binding.json`;
- `literature/PUBLISHED_INPUT_AUDIT.json`; and
- `direct-allocation-crosscheck/DIRECT_ALLOCATION_CROSSCHECK.json`.

The consolidated `EFX48_END_TO_END_CERTIFICATE.json`,
`EFX48_END_TO_END_MANIFEST.sha256`, build log, and deterministic source
archive are present. `EFX48_CLEAN_SOURCE_REPLAY.json` records extraction into a
new temporary project directory followed by the semantic audits, published-
input audit, Lean build, axiom audit, and manifest verification on the
original host. `EFX48_CLEAN_SOURCE_FULL_ETHOS_REPLAY.json` additionally records
all eight proof hashes and Ethos verdicts as `correct`. The remaining
reproduction gate is an independent second-machine or cross-platform replay.

## Acceptance standard

The result is ready to submit when:

- [x] the final end-to-end manifest verifies from a fresh source extraction
  on the original host;
- [ ] a second machine or container reproduces the build and audits;
- [ ] one fair-division expert signs off on the mathematics and theorem
  variants;
- [ ] one formal/computational-proof expert signs off on the hybrid trust
  chain; and
- [ ] the novelty search is confirmed by researchers active in EFX.

External review should report disagreements or unverified items explicitly;
silence is not acceptance.
