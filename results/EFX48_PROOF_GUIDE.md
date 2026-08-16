# Proof Guide: Nonnegative Additive EFX for Four Agents and Eight Goods

**Claim.** Every nonnegative additive valuation instance with four
agents and eight indivisible goods admits a complete EFX allocation.

**Proof status.** Internally verified hybrid computer-assisted proof. The
Lean reduction and all eight terminal UNSAT certificates check. The two
smaller existence theorems are exact, pinned published inputs. The
end-to-end manifest verifies locally. External expert review and a
clean-machine release replay remain outstanding.

## 1. Exact statement

For weights \(w_{ig}\ge0\), agent \(i\)'s value for a bundle \(B\) is

\[
v_i(B)=\sum_{g\in B}w_{ig}.
\]

An allocation \(A=(A_0,\ldots,A_3)\) is complete when its bundles partition
the eight goods. It is EFX when, for all distinct agents \(i,j\) and every
good \(g\in A_j\),

\[
v_i(A_i)\ge v_i(A_j\setminus\{g\}).
\]

The formal definitions are `ValidAllocation`, `EFX`, and `AdmitsEFX` in
[`Definitions.lean`](../formal/efx48/EFX48/Definitions.lean).

## 2. Deduction chain

```text
hypothetical nonnegative 4x8 counterexample
                 │
                 ▼
uniform positive perturbation
                 │
                 ▼
row normalization + generic strict perturbation
                 │
                 ▼
published residual cuts remove easy 4x7 and 3x7 regions
                 │
                 ▼
favorite matching + relabeling + stabilizers
                 │
                 ▼
eight exact terminal ranking cells
                 │
                 ▼
1,701 partitions × 24 possible bundle matchings
                 │
                 ▼
eight exact QF_LRA formulas
                 │
                 ▼
eight cvc5 CPC proofs accepted by Ethos
                 │
                 ▼
contradiction: the 4x8 counterexample cannot exist
```

Lean proves every mathematical arrow through the eight terminal cells. A
generator-independent parser audit checks that every assertion in the
terminal formulas has the semantics specified by Lean. The CPC/Ethos layer
proves those exact formulas inconsistent.

## 3. Mathematical reduction

### 3.1 Positive approximation, normalization, and perturbation

The EFX-existence set is a finite union of closed fixed-allocation
polyhedra. Its complement is open. Therefore, adding a sufficiently small
common positive constant to every coordinate turns any hypothetical
nonnegative counterexample into a positive counterexample. This first step is
proved by `exists_positive_noEFX_perturbation` in
[`Perturbation.lean`](../formal/efx48/EFX48/Perturbation.lean).

Positive scaling of one agent's entire row preserves all EFX comparisons, so
each row can be normalized to sum to one. Because only finitely many complete
allocations exist, the set of no-EFX instances is open. A sufficiently small
sum-preserving perturbation therefore makes every row ranking strict while
preserving positivity and nonexistence.

The load-bearing formal theorems are
`exists_generic_normalized_noEFX_perturbation` and
`positive_noEFX_has_fully_generic_normalized_counterexample` in
[`StrictPerturbation.lean`](../formal/efx48/EFX48/StrictPerturbation.lean).

### 3.2 Favorite matching

If the four agents have four distinct favorite goods, assign each agent
their favorite and one of the remaining four goods. After any good is
removed from another two-good bundle, at most one good remains; it is worth
no more to the observer than their own favorite, which is already in their
bundle. The allocation is EFX.

This argument is formalized by
`favorite_injection_allocation_4x8`. The more reusable theorem
`favorite_small_bundles_efx` proves the same fairness conclusion for any
finite instance in which every agent owns a favorite and every bundle has
size at most two. The construction
`admitsEFX_of_injective_favorites_and_extra_embedding` additionally builds
such an allocation whenever the favorite map is injective and the remaining
goods embed into the agent set. The fully cardinal theorem
`admitsEFX_of_injective_favorites_of_card_le_twice` constructs that embedding
from \(m\le2n\), closing the injective-favorite case for arbitrary finite
instances in this range. See
[`FavoriteMatching.lean`](../formal/efx48/EFX48/FavoriteMatching.lean).

Consequently a counterexample must have a noninjective favorite pattern.
Up to relabeling, the four possibilities are

\[
2+1+1,\qquad 3+1,\qquad 2+2,\qquad 4.
\]

When all four agents share a favorite, their second favorites have one of
five multiplicity patterns:

\[
1+1+1+1,\qquad 4,\qquad 3+1,\qquad 2+2,\qquad 2+1+1.
\]

These are the eight terminal cells. Their coverage and the available
row/good stabilizer reductions are proved in
[`CanonicalCoverage.lean`](../formal/efx48/EFX48/CanonicalCoverage.lean) and
[`Stabilizers.lean`](../formal/efx48/EFX48/Stabilizers.lean).

### 3.3 Published residual cuts

Two regions reduce to smaller known theorems.

1. If one good is minimum for every agent, delete it, solve the four-agent
   seven-good instance, move to an unenvied source bundle, and insert the
   deleted good there.
2. If an agent-good pair satisfies the formal `Peelable` inequalities,
   delete that agent and good, solve the three-agent seven-good instance, and
   reinsert the pair.

The first invokes Mahara's \(m\le n+3\) theorem. The second invokes the
three-agent theorem of Chaudhury, Garg, and Mehlhorn. Exact paper versions
and theorem fragments are recorded in
[`PUBLISHED_INPUT_AUDIT.md`](PUBLISHED_INPUT_AUDIT.md). The lifting from
standard published statements to the local deleted-instance interfaces is
proved in
[`PublishedLifting.lean`](../formal/efx48/EFX48/PublishedLifting.lean).

The audit found and corrected a substantive earlier error here: the deleted
agent must be excluded as an *observer* in the three-agent residual
allocation. The corrected predicate `EFXExceptObserver` retains exactly the
comparisons needed for reinsertion; see
[`Peelable.lean`](../formal/efx48/EFX48/Peelable.lean).

### 3.4 Partitions and perfect matchings

There are exactly

\[
S(8,4)=1{,}701
\]

unlabeled partitions of eight goods into four nonempty bundles. Lean checks
the restricted-growth enumeration and proves that every onto owner map is a
relabeling of one of these partitions in
[`RestrictedGrowth.lean`](../formal/efx48/EFX48/RestrictedGrowth.lean).

For a fixed partition, form a bipartite graph between agents and bundles. An
edge \(i\to B\) means that assigning \(B\) to \(i\) passes all of \(i\)'s EFX
comparisons against the other three bundles. That partition supports an EFX
allocation exactly when this \(4\times4\) graph has a perfect matching.

Thus no EFX allocation exists exactly when all 24 bundle permutations are
obstructed for every one of the 1,701 partitions. This equivalence is proved
in
[`PartitionMatching.lean`](../formal/efx48/EFX48/PartitionMatching.lean).

## 4. Terminal formulas

Each terminal QF_LRA formula asserts:

- strict positivity and row normalization;
- pairwise-distinct rows and the exact favorite/second-favorite pattern;
- sound row and unused-good stabilizer inequalities;
- exclusion of the universal-minimum and peelable residual regions;
- 27,216 agent-bundle feasibility-edge definitions; and
- 40,824 perfect-matching obstruction assertions.

The complete Lean reduction is
`positive_noEFX_reduces_to_eight_terminal_cells` in
[`TerminalCells.lean`](../formal/efx48/EFX48/TerminalCells.lean).

The independent formula generator does not import the original encoder,
partition implementation, or Z3. The semantic audit separately parses every
generated assertion, reconstructs all 1,701 partitions and their matching
clauses, and binds the ranking assertions to Lean's exact canonical
constants.

## 5. Certificate closure

All eight exact terminal formulas have:

- an original exact Z3 UNSAT result and clean replay;
- an independently regenerated formula;
- a cvc5-generated CPC proof;
- an Ethos checker verdict of `correct`; and
- formula, proof, tool, all 51 transitive signature, semantic-audit, and
  literature-input hashes in a 96-entry SHA-256 manifest;
- an ordered formula-to-proof audit matching 545,360 SMT assertions to
  545,360 permanent CPC assumptions with zero mismatches.

The CPC proofs total 1,668,457,899 bytes and 13,812,082 proof steps. The
authoritative summary is
[`EIGHT_CELL_CPC_CERTIFICATES.json`](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260801-v2/EIGHT_CELL_CPC_CERTIFICATES.json);
the release-candidate manifest is
[`EIGHT_CELL_CPC_MANIFEST.sha256`](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260801-v2/EIGHT_CELL_CPC_MANIFEST.sha256).

The final Lean theorem is
`admitsEFX_4x8_of_standard_published_inputs_nonnegative` in
[`PublishedLifting.lean`](../formal/efx48/EFX48/PublishedLifting.lean). Its
permanent axiom audit reports only

```text
[propext, Classical.choice, Quot.sound]
```

and no dependency on `sorryAx`, `native_decide`, or `ofReduceBool`.

An independent direct encoding also checks all 40,824 labeled onto
allocations in each of the eight cells without using the
partition/perfect-matching representation. All eight are UNSAT: six directly
in Z3 and two in cvc5 after an audited identity-only syntax normalization.
The frozen summary is
[`DIRECT_ALLOCATION_CROSSCHECK.json`](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260801-v2/direct-allocation-crosscheck/DIRECT_ALLOCATION_CROSSCHECK.json).

The final end-to-end audit reruns the semantic and literature checks, verifies
the CPC and direct-allocation records, performs a full pinned Lean build and
axiom audit, and packages 72 transitive proof-source files. Its
[`EFX48_END_TO_END_CERTIFICATE.json`](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260801-v2/EFX48_END_TO_END_CERTIFICATE.json)
has status `verified_hybrid_proof_package`, and its
[`124-entry manifest`](../../experimental-runs/additive-efx-counting-runs/parkability/certification-20260801-v2/EFX48_END_TO_END_MANIFEST.sha256)
verifies locally.

## 6. What is and is not verified

### Verified internally

- The structural reduction compiles in pinned Lean 4.32.1/mathlib.
- The final theorem's displayed axiom boundary is clean.
- Exact paper variants match the formal interfaces.
- Every terminal formula is hash-bound to an independently parsed semantic
  specification.
- All eight terminal UNSAT claims have independently checked proof objects.
- All eight alternative direct-allocation formulas are UNSAT.
- The archived formulas and proofs match their frozen manifest.
- The complete 124-entry end-to-end manifest verifies locally.

### Remaining external trust

- The mathematical proofs in the two pinned published papers are used as
  inputs rather than re-formalized.
- Lean's kernel and mathlib are trusted.
- Ethos is a separate but ordinary checker implementation.
- The Lean-to-SMT bridge is parser-audited, not expressed as a single
  kernel-checked reflection theorem.

### Remaining release gates

- reproduce the release on a clean machine or container;
- obtain independent fair-division and formal-certification review; and
- obtain peer review of the polished computer-assisted submission.

These gates govern public confidence and presentation. They do not replace
or weaken any of the already checked load-bearing terminal certificates.

## 7. Reviewer entry points

For a mathematical review, read in this order:

1. [`Definitions.lean`](../formal/efx48/EFX48/Definitions.lean);
2. [`FavoriteMatching.lean`](../formal/efx48/EFX48/FavoriteMatching.lean);
3. [`StrictPerturbation.lean`](../formal/efx48/EFX48/StrictPerturbation.lean);
4. [`UniversalMinimum.lean`](../formal/efx48/EFX48/UniversalMinimum.lean) and
   [`Peelable.lean`](../formal/efx48/EFX48/Peelable.lean);
5. [`Stabilizers.lean`](../formal/efx48/EFX48/Stabilizers.lean);
6. [`PartitionMatching.lean`](../formal/efx48/EFX48/PartitionMatching.lean);
7. [`TerminalCells.lean`](../formal/efx48/EFX48/TerminalCells.lean); and
8. [`PublishedLifting.lean`](../formal/efx48/EFX48/PublishedLifting.lean).

For an adversarial audit, use
[`EXPERT_REVIEW_CHECKLIST.md`](EXPERT_REVIEW_CHECKLIST.md). For the current
status, open
[`SESSION_REVIEW_CURRENT_20260729.md`](SESSION_REVIEW_CURRENT_20260729.md).
